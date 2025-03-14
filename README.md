# twitter-bot
This repo can act as framework for interacting with any twitter community, just change the listid in ```Scrappon.py``` and topics array should be replaced by your domain's array

Don't do ```pip install -r requirements.txt```, its just a pip freeze and not curated yet

This bot solves the problem for rate limiting by fetching tweet ids with a personal account but getting tweet details through Selenium.

### Logic for fetching and storing tweets to db (1-4 done)

1. When any trending topic in my locale matches a topic mentioned in ```topics.py```
2. Iterating through my custom list of users and getting tweets from there
3. Add logic to get notifications tweets and use it for storing tweets in my db
4. Add logic to keep data redundant by using ```twitter_id``` (don't add to db if not unique)
5. The polling of data needs some logic so that fetching is done in a such a way that it is up-to-date and within the rate limiting (fixed)
6. Add likes counter in the db too, help us tell what is good data and send to ai agent when forming tweet

### Bot logic

1. the bot should be seeing the notifications as prompt and reply to them using data on that prompt from the db within the last 3 days to maintain relevance of the tweet
2. Fetch the latest tweets in my db by the number of likes and vector embeddings and use those tweets to form an opinion
3. The bot should not reply to every notification, it should form a decision if to like or reply and then proceed
4. Once an opinion is formed, reply to the tweet or just like it, one of these actions will happen
5. New original tweets idea will be posted if something which is trending is also in our topic list and our db has relevant data


### Pain points

1. Figure out vector embeddings for this and how to use it best way possible along with tweet likes
2. How will memory be managed and reply to mentions, should have some context from previous tweets
3. Maintain a consistent personality
4. Scheduler for polling data, tweeting and replying


### Fetch Latest Tweets by Likes + Vector Embeddings
Combining Relevance:

Option A: First do a vector embedding search to see which tweets semantically match the user’s mention. Then from those results, pick the top ones sorted by likes.

Option B: Use a heuristic that factors in both semantic relevance + popularity (likes). You might do a quick filter for tweets with “at least X likes” to ensure they’re meaningful.

Maintain a list of footballers famous and clubs famous, keep iterating and checking if there multiple tweets in the last few hours or minutes based on created_on, then we make a tweet


### Update 12-01-2025

1. Add notifications for famous accounts, who you want to consider replying or not based on available infor and tweet germane to it o not
2. The notification tweets will be ran through every hour and based on tweet_id, we upsert so no duplicates
3. Trending can work as it is, just add more context using vector database and recent tweets to figure out, ran through every hour and checked if too similar to previous 3 tweets then skip
4. After going through lists, see if you want to make any original tweet if the list has lots of commonality going on
5. Add logic for Reply with LIKE or reply with tweet_content or reply I don't know as per hallucination mechanism
6. Every tweet is scheduled between 2 - 15 min and put out
7. For increasing knowledge, keep fetching from lists and following to get high quality data every one hour or so, make another list so that as much good info as possible is with us
8. Polling is run on different account and posting on different -- later

Use separate list for major clubs and transfer news and football news, fetch around 200-300 tweets from each in every few minutes and feed to database
list=[208149258,1451872529140813829,1345098781314973697,234769357,1313187923429404672,33445961,1238730743569772544,1877641960028082596,104274535,1459083476892893185,1523307912856285184,1460898747349667840]