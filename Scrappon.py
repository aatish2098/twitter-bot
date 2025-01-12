import asyncio
import os
import re
from deep_translator import GoogleTranslator
from phi.document import Document
from phi.embedder.openai import OpenAIEmbedder
from tweety import TwitterAsync
from pymongo import MongoClient
from tweety.constants import HOME_TIMELINE_TYPE_FOLLOWING
from tweety.types import SelfThread
from typing import Any
from pymongo.collection import Collection

from ballknowledge import store_with_embedding, fetch_qdrant
from search import generate_with_vector_search, generate_notification_reply
from topics import topics
from tweety.filters import SearchFilters
from dotenv import load_dotenv


# CLEANING TWEET TEXT
def clean_tweet_text(tweet_text: str) -> str:
    translated = GoogleTranslator(source="auto", target="en").translate(tweet_text)
    return translated


def add_to_qdrant(tweet: Any, cleaned_text: str) -> Document:
    global doc
    if len(cleaned_text.split()) > 3:
        embeddings = OpenAIEmbedder().get_embedding(cleaned_text)
        meta_data = {"tweet_id": tweet.get("id")}
        # Created_on (ISO date string)
        # Usually nested like: "created_on": {"$date": "..."}
        created_on = None
        if "created_on" in tweet:
            created_on = tweet["created_on"]
        meta_data["created_on"] = created_on
        # Username & Verified
        # Usually inside tweet["author"]
        author = tweet.get("author", {})
        meta_data["username"] = author.get("username")
        meta_data["verified"] = author.get("verified")
        # Likes & Views
        meta_data["likes"] = tweet.get("likes")
        meta_data["views"] = tweet.get("views")
        print(f"Generated embeddings for the tweet: {cleaned_text}")
        doc = Document(meta_data=meta_data, content=cleaned_text, embeddings=embeddings, name=meta_data['username'])
    return doc


def add_to_mongo(tweet: Any, cleaned_text: str, tweets_collection: Collection) -> None:
    # Check if tweet has more than 3 words
    if len(cleaned_text.split()) > 3:
        # Prepare doc for MongoDB
        doc = {
            "tweet_id": str(tweet.id),
            "username": tweet.author.username,
            "Verified": tweet.author.verified,
            "tweet_text": cleaned_text,
            "created_on": tweet.created_on,
            "all_details": tweet
        }
        # Insert into MongoDB
        existing_doc = tweets_collection.find_one({"tweet_id": str(tweet.id)})
        # fetch and add to DB logic, to reply later if met threshold
        if existing_doc:
            tweets_collection.update_one(
                {"tweet_id": str(tweet.id)},
                {"$set": doc}
            )
            # print(f"Updated tweet by {tweet.author.username}")
        else:
            # Insert new tweet
            # print(f"Adding new tweet by {tweet.author.username}")
            tweets_collection.insert_one(doc)


async def fetch_and_post_on_trending():
    load_dotenv()
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    topic_keywords = set(word.lower() for topic in topics for word in topic.split())
    trendings = await app.get_trends()
    for trending in trendings:
        trending_now = str(trending._get_name())
        print(f"This {trending_now} starts here:")
        if trending_now in topics or trending_now.lower() in topic_keywords:
            trending_tweets = await app.search(trending._get_name(), filter_=SearchFilters.Latest(), pages=1,
                                               wait_time=2)
            tweets_gen = []
            for tweet in trending_tweets:
                if trending_now or trending_now.lower() in tweet.text:
                    cleaned_text = clean_tweet_text(tweet.text)
                    tweets_gen.append(cleaned_text)
            if len(tweets_gen) > 15:

                tweet_content = generate_with_vector_search(topic=trending_now, tweets=tweets_gen,
                                                            vectordb=fetch_qdrant())
                await app.create_tweet(text=tweet_content)


async def fetch_and_store_list(tweets_collection: Collection):
    load_dotenv()
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    tweet_lists = [1451872529140813829, 1345098781314973697, 234769357, 1313187923429404672, 33445961,
            1238730743569772544, 1877641960028082596, 104274535, 1459083476892893185, 1523307912856285184,
            1460898747349667840]
    for list_id in tweet_lists:
        tweets = await app.get_list_tweets(list_id=list_id, pages=1, wait_time=2)
        # tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
        topic_keywords = set(word.lower() for topic in topics for word in topic.split())
        doclist = []
        for tweet in tweets:
            if isinstance(tweet, SelfThread):
                for thread in tweet.tweets:
                    if any(word.lower() in topic_keywords for word in thread.text.split()):
                        cleaned_text = clean_tweet_text(thread.text)
                        doclist.append(add_to_qdrant(tweet, cleaned_text))
                        add_to_mongo(thread, cleaned_text, tweets_collection)
            else:
                if any(word.lower() in topic_keywords for word in tweet.text.split()):
                    cleaned_text = clean_tweet_text(tweet.text)
                    doclist.append(add_to_qdrant(tweet, cleaned_text))
                    add_to_mongo(tweet, cleaned_text, tweets_collection)
        store_with_embedding(doclist)


async def fetch_and_reply_notification() -> str:
    load_dotenv()
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    # tweets = await app.get_tweet_notifications(pages=3, wait_time=2)
    tweets1 = await app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING, pages=1)
    for tweet in tweets1.tweets:
        if isinstance(tweet, SelfThread):
            for thread in tweet.tweets:
                cleaned_text = clean_tweet_text(thread.text)
                # generate_notification_reply(cleaned_text,fetch_qdrant())
        else:
            cleaned_text = clean_tweet_text(tweet.text)
            if str(tweet.author.username) == "great_o1d":
                continue
            elif len(cleaned_text) >= 10:
                tweet_content = generate_notification_reply(cleaned_text, fetch_qdrant())
                await app.create_tweet(text=tweet_content, reply_to=tweet.id)


# MAIN ENTRY POINT
if __name__ == "__main__":
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path=dotenv_path)
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Knowledge']
    tweets_collection = db.OldTweets
    # tweets_generated = generate_with_vector_search(fetch_qdrant())
    # asyncio.run(fetch_and_reply_notification())
    asyncio.run(fetch_and_post_on_trending())
    # asyncio.run(fetch_and_store_list(tweets_collection))
    # asyncio.run(fetch_and_post_on_trending())
