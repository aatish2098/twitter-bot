import asyncio
import os
import re
from deep_translator import GoogleTranslator
from tweety import TwitterAsync
from pymongo import MongoClient
from tweety.types import SelfThread
from typing import Any
from pymongo.collection import Collection
from topics import topics
from tweety.filters import SearchFilters


# CLEANING TWEET TEXT
def clean_tweet_text(tweet_text: str) -> str:
    tweet_text = re.sub(r"http\S+", "", tweet_text)  # remove urls
    translated = GoogleTranslator(source="auto", target="en").translate(tweet_text).strip()
    return translated


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


async def fetch_and_store_trending(tweets_collection: Collection):
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    topic_keywords = set(word.lower() for topic in topics for word in topic.split())
    trendings = await app.get_trends()
    for trending in trendings:
        if trending._get_name().lower() in topic_keywords:
            trending_tweets = await app.search(trending._get_name(), filter_=SearchFilters.Latest(), pages=2,
                                               wait_time=2)
            print(f"This {trending._get_name()} starts here:")
            for tweet in trending_tweets:
                if trending._get_name() in tweet.text:
                    cleaned_text = clean_tweet_text(tweet.text)
                    print(cleaned_text)
                    add_to_mongo(tweet, cleaned_text, tweets_collection)


async def fetch_and_store_list(tweets_collection: Collection):
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    tweets = await app.get_list_tweets(list_id=1877641960028082596, pages=2, wait_time=2)
    # tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    topic_keywords = set(word.lower() for topic in topics for word in topic.split())
    for tweet in tweets:
        if isinstance(tweet, SelfThread):
            for thread in tweet.tweets:
                if any(word.lower() in topic_keywords for word in thread.text.split()):
                    cleaned_text = clean_tweet_text(thread.text)
                    add_to_mongo(thread, cleaned_text, tweets_collection)
        else:
            if any(word.lower() in topic_keywords for word in tweet.text.split()):
                cleaned_text = clean_tweet_text(tweet.text)
                add_to_mongo(tweet, cleaned_text, tweets_collection)


# MAIN ENTRY POINT

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Knowledge']
    tweets_collection = db.OldTweets
    # asyncio.run(fetch_and_store_list(tweets_collection))
    asyncio.run(fetch_and_store_trending(tweets_collection))
