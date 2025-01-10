import asyncio
import re

import tweety.exceptions
from qdrant_client.http import models as qdrant_models
from tweety import TwitterAsync
from pymongo import MongoClient
from tweety.filters import SearchFilters

from usernames import usernames  # Your array of usernames


# CLEANING TWEET TEXT
def clean_tweet_text(tweet_text: str) -> str:
    tweet_text = re.sub(r"http\S+", "", tweet_text)  # remove urls
    return tweet_text.strip()


async def fetch_and_store_tweets():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Knowledge']
    tweets_collection = db.OldTweets
    app = TwitterAsync("session")
    await app.sign_in("great_o1d", "Application@2025")
    for target_username in usernames:
        try:
            user = await app.get_user_info(target_username)
            # Get up to 15 "pages" of tweets (scraping logic)
            all_tweets = await app.get_user_media(user, 6,2)
            # Process each tweet
            for tweet in all_tweets:
                # Fetch full tweet text
                print(tweet)
                tweet_detail = await app.tweet_detail(f"https://twitter.com/{target_username}/status/{tweet.id}")
                tweet_text = tweet_detail._get_tweet_text()
                cleaned_text = clean_tweet_text(tweet_text)

                # Check if tweet has more than 3 words
                if len(cleaned_text.split()) > 3:
                    # Prepare doc for MongoDB
                    doc = {
                        "tweet_id": str(tweet.id),
                        "username": target_username,
                        "tweet_text": cleaned_text,
                        "created_on": tweet_detail.created_on
                    }
                    # Insert into MongoDB
                    tweets_collection.insert_one(doc)

                    print(f"Stored tweet from {target_username}: {cleaned_text[:60]}...")
        except tweety.exceptions.RateLimitReached:
            print("Rate limit reached, wait now")
            await asyncio.sleep(900)  # Wait 15 minutes
        except Exception as e:
            print("Some other exception",e)


# MAIN ENTRY POINT
if __name__ == "__main__":
    asyncio.run(fetch_and_store_tweets())
