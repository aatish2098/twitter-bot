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

from qdrantfunctions import store_with_embedding, fetch_qdrant
from agents import generate_with_vector_search,analysis_of_contract
from topics import get_trending
from searchweb import search_internet
from dotenv import load_dotenv


# CLEANING TWEET TEXT
def clean_tweet_text(tweet: Any) -> str:
    cleaned=re.sub(r"https?:\/\/\S+", "", tweet.text)
    if tweet.language != "en" or tweet.language != "en-gb":
        translated = GoogleTranslator(source="auto", target="en").translate(cleaned)
    else:
        return cleaned
    return translated


def add_to_qdrant(coin: list, tweet: Any, cleaned_text) -> Document:
    global doc
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
    meta_data["symbol"] = coin[1]
    meta_data["name"] = coin[0]
    print(f"Generated embeddings for the tweet: {tweet.text}")
    doc = Document(meta_data=meta_data, content=cleaned_text, embeddings=embeddings, name=coin[0])
    return doc


# def add_to_mongo(tweet: Any, cleaned_text: str, tweets_collection: Collection) -> None:
#     # Check if tweet has more than 3 words
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client['Knowledge']
#     tweets_collection = db.OldTweets
#     if len(cleaned_text.split()) > 3:
#         # Prepare doc for MongoDB
#         doc = {
#             "tweet_id": str(tweet.id),
#             "username": tweet.author.username,
#             "Verified": tweet.author.verified,
#             "tweet_text": cleaned_text,
#             "created_on": tweet.created_on,
#             "all_details": tweet
#         }
#         # Insert into MongoDB
#         existing_doc = tweets_collection.find_one({"tweet_id": str(tweet.id)})
#         # fetch and add to DB logic, to reply later if met threshold
#         if existing_doc:
#             tweets_collection.update_one(
#                 {"tweet_id": str(tweet.id)},
#                 {"$set": doc}
#             )
#             # print(f"Updated tweet by {tweet.author.username}")
#         else:
#             # Insert new tweet
#             # print(f"Adding new tweet by {tweet.author.username}")
#             tweets_collection.insert_one(doc)


async def fetch_and_store_list():
    load_dotenv()
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])
    tweet_lists = [1602917243742035968, 1011591069782499328]
    trending = get_trending()
    all_entries = []
    for coin in trending:
        name = coin["name"]
        symbol = coin["symbol"]
        dollar_symbol = f"${symbol}"
        coin_array = [name, symbol, dollar_symbol]
        all_entries.append(coin_array)
    doclist = []
    for list_id in tweet_lists:
        tweets = await app.get_list_tweets(list_id=list_id, pages=3, wait_time=2)
        # tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
        for tweet in tweets:
            if isinstance(tweet, SelfThread):
                for thread in tweet.tweets:
                    if len(thread.text) > 30:
                        for coin in all_entries:
                            if any(detail in coin for detail in thread.text.split()):
                                cleaned_text=clean_tweet_text(thread)
                                doclist.append(add_to_qdrant(coin,thread, cleaned_text))
            else:
                if len(tweet.text) > 30:
                    for coin in all_entries:
                        if any(detail in coin for detail in tweet.text.split()):
                            cleaned_text = clean_tweet_text(thread)
                            doclist.append(add_to_qdrant(coin, tweet, cleaned_text))
    store_with_embedding(doclist)


# async def fetch_and_reply_notification() -> str:
#     load_dotenv()
#     app = TwitterAsync("session")
#     await app.sign_in(os.environ['username'], os.environ['password'])
#     # tweets = await app.get_tweet_notifications(pages=3, wait_time=2)
#     tweets1 = await app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING, pages=1)
#     for tweet in tweets1.tweets:
#         if isinstance(tweet, SelfThread):
#             for thread in tweet.tweets:
#                 cleaned_text = clean_tweet_text(thread)
#                 # generate_notification_reply(cleaned_text,fetch_qdrant())
#         else:
#             cleaned_text = clean_tweet_text(tweet)
#             if str(tweet.author.username) == "great_o1d":
#                 continue
#             elif len(cleaned_text) >= 10:
#                 tweet_content = generate_notification_reply(cleaned_text, fetch_qdrant())
#                 await app.create_tweet(text=tweet_content, reply_to=tweet.id)


async def create_tweet_on_trending_topic(topic: str):
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])

    await app.create_tweet(text=generate_with_vector_search(topic, fetch_qdrant()))

# MAIN ENTRY POINT
if __name__ == "__main__":
    dotenv_path = os.path.join(os.getcwd(), '.env')
    load_dotenv(dotenv_path=dotenv_path)
    print(get_trending())
    # asyncio.run(fetch_and_reply_notification())
    # asyncio.run(fetch_and_store_list())
    # search_internet("ETH")
    address = "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
    chain_id = 12
    analysis_of_contract(address=address,chainid=chain_id)
    # asyncio.run(create_tweet_on_trending_topic("AIXBT"))
    # asyncio.run(fetch_and_post_on_trending())
