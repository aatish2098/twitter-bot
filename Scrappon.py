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
from Scraper import fetch_tweet_content
from tweety.constants import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING
from tweety.filters import SearchFilters

from usernames import usernames  # Your array of usernames


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
            "username": tweet.author.name,
            "tweet_text": cleaned_text,
            "created_on": tweet.created_on
        }
        # Insert into MongoDB
        tweets_collection.insert_one(doc)
        print("added tweet by",tweet.author.name)


async def fetch_and_store_tweets():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Knowledge']
    tweets_collection = db.OldTweets
    app = TwitterAsync("session")
    await app.sign_in(os.environ['username'], os.environ['password'])

    topic_keywords = set(word.lower() for topic in topics for word in topic.split())
    trendings = await app.get_trends()
    for trending in trendings:
        if trending._get_name().lower() in topic_keywords:
            print(trending._get_name())
            trending_tweets = await app.search(trending._get_name(), filter_=SearchFilters.Latest(), pages=2,
                                               wait_time=2)

            for tweet in trending_tweets:
                tweet_detail = fetch_tweet_content(tweet.id)
                if trending._get_name() in tweet_detail:
                    cleaned_text = clean_tweet_text(tweet_detail)
                    add_to_mongo(tweet, cleaned_text, tweets_collection)
            return

    tweets = await app.get_list_tweets(list_id=1877641960028082596, pages=2, wait_time=2)
    # tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    for tweet in tweets:
        if isinstance(tweet, SelfThread):
            continue
            # Don't know how to fix without large overhead and causing rate limiting
            # for thread in tweet.tweets:
            #     tweet_detail = await app.tweet_detail(
            #         f"https://twitter.com/{thread.author.username}/status/{thread.id}")
        else:
            tweet_detail = fetch_tweet_content(tweet.id)
        # Check each tweet for matches
        if any(word.lower() in topic_keywords for word in tweet_detail.split()):
            cleaned_text = clean_tweet_text(tweet_detail)
            add_to_mongo(tweet, cleaned_text, tweets_collection)


# MAIN ENTRY POINT
if __name__ == "__main__":
    asyncio.run(fetch_and_store_tweets())
