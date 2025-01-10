import asyncio
import os
import re
from deep_translator import GoogleTranslator
from tweety import TwitterAsync
from pymongo import MongoClient
from tweety.types import SelfThread

from topics import topics
from Scraper import fetch_tweet_content
from tweety.constants import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING
from tweety.filters import SearchFilters

from usernames import usernames  # Your array of usernames


# CLEANING TWEET TEXT
def clean_tweet_text(tweet_text: str) -> str:
    tweet_text = re.sub(r"http\S+", "", tweet_text)  # remove urls
    translated=GoogleTranslator(source="auto", target="en").translate(tweet_text).strip()
    return translated



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
            trending_tweets = await app.search(trending._get_name(), filter_=SearchFilters.Latest(),pages=1,wait_time=2)
            for tweet in trending_tweets:
                tweet_detail = fetch_tweet_content(tweet.id)
                cleaned_text = clean_tweet_text(tweet_detail)
                print(cleaned_text)
                # Check if tweet has more than 3 words
                if len(cleaned_text.split()) > 3:
                    # Prepare doc for MongoDB
                    doc = {
                        "tweet_id": str(tweet.id),
                        "username": tweet.author,
                        "tweet_text": cleaned_text,
                        "created_on": tweet.created_on
                    }
                    # Insert into MongoDB
                    tweets_collection.insert_one(doc)

    tweets = await app.get_list_tweets(list_id=1877641960028082596, pages=2, wait_time=2)
    for tweet in tweets:
        if isinstance(tweet, SelfThread):
            continue
            # Don't know how to fix without large overhead
            # for thread in tweet.tweets:
            #     tweet_detail = await app.tweet_detail(
            #         f"https://twitter.com/{thread.author.username}/status/{thread.id}")
        else:
            tweet_detail = fetch_tweet_content(tweet.id)
        # Check each tweet for matches
        if any(word.lower() in topic_keywords for word in tweet_detail.text.split()):
            cleaned_text = clean_tweet_text(tweet_detail)
            # Check if tweet has more than 3 words
            if len(cleaned_text.split()) > 3:
                # Prepare doc for MongoDB
                doc = {
                    "tweet_id": str(tweet.id),
                    "username": tweet.author,
                    "tweet_text": cleaned_text,
                    "created_on": tweet.created_on
                }
                # Insert into MongoDB
                tweets_collection.insert_one(doc)

    # tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    # for tweet in tweets:
    #    print(tweet)
    # for target_username in usernames:
    #     try:
    #         user = await app.get_user_info(target_username)
    #         # Get up to 15 "pages" of tweets (scraping logic)
    #         all_tweets = await app.get_user_media(user, 6,2)
    #         # Process each tweet
    #
    #         for tweet in all_tweets:
    #             # Fetch full tweet text
    #             print(tweet)
    #             tweet_detail = await app.tweet_detail(f"https://twitter.com/{target_username}/status/{tweet.id}")
    #             tweet_text = tweet_detail._get_tweet_text()
    #             cleaned_text = clean_tweet_text(tweet_text)
    #
    #             # Check if tweet has more than 3 words
    #             if len(cleaned_text.split()) > 3:
    #                 # Prepare doc for MongoDB
    #                 doc = {
    #                     "tweet_id": str(tweet.id),
    #                     "username": target_username,
    #                     "tweet_text": cleaned_text,
    #                     "created_on": tweet_detail.created_on
    #                 }
    #                 # Insert into MongoDB
    #                 tweets_collection.insert_one(doc)
    #
    #                 print(f"Stored tweet from {target_username}: {cleaned_text[:60]}...")
    #     except tweety.exceptions.RateLimitReached:
    #         print("Rate limit reached, wait now")
    #         await asyncio.sleep(900)  # Wait 15 minutes
    #     except Exception as e:
    #         print("Some other exception",e)


# MAIN ENTRY POINT
if __name__ == "__main__":
    asyncio.run(fetch_and_store_tweets())
