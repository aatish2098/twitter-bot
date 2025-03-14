from typing import Iterator, Any
from phi.knowledge import AgentKnowledge
from phi.model.openai import OpenAIChat
from phi.run.response import RunResponse
import os
from phi.model.openai.like import OpenAILike
from phi.agent import Agent
from phi.vectordb.qdrant import Qdrant


# def fetch_with_raw_tweets(tweets_str: str, topic: str) -> str:
#     tweet_content = ""
#     agent = Agent(
#         name="Banter Ball",
#         agent_id="banterball-agent",
#         introduction="Yo, I'm Banter Ball. Just for fun.",
#         model=OpenAILike(
#             id="meta-llama/Llama-3.3-70B-Instruct",
#             api_key=os.environ["HYPERBOLIC_API_KEY"],
#             base_url="https://api.hyperbolic.xyz/v1",
#         ),
#         system_prompt="""
# You are a Gen-Z football fanatic named 'BanterBall'.
# and you love banter with fans.
# You speak in Gen-Z slang, dropping roasts on players, managers and clubs.
# sometimes use profanities, not often
# but feel free to use humor and mild sarcasm.
# """,
#         agent_data={
#             "favorite_team": "Manchester United",
#             "favorite_player": "Cristiano Ronaldo",
#             "preferred_style": "Gen-Z banter, mild sarcasm, roasts",
#         },
#         use_default_system_message=False,
#         task="Create gen-z friendly tweets about football roasting other fans or players or managers or clubs",
#         prevent_hallucinations=True,
#         guidelines=["Sometimes rage bait", "Stay roasting, sometimes offensive"],
#         expected_output="Output a short tweet in first-person voice.",
#         prevent_prompt_leakage=True,
#         add_name_to_instructions=False,
#         add_datetime_to_instructions=True,
#         parse_response=True)
#
#     response_stream: Iterator[RunResponse] = agent.run(
#         f"{tweets_str}\n\nGenerate a tweet by analyzing these tweets. Keep it under 280 characters and write it referring the above tweets and with focus to be hurtful and sometimes rage bait, do not use hashtag, at maximum one hashtag and sometimes add emojis"
#     )
#     # Assuming response_stream is an iterator of RunResponse objects
#     for response in response_stream:
#         # Check if the tuple contains the 'content' key
#         if isinstance(response, tuple) and response[0] == "content":
#             tweet_content = response[1].replace('"', '').replace("'", '')
#             print(f"{tweet_content}")
#
#     return tweet_content


def generate_notification_reply(tweet: str, vectordb: Qdrant) -> str:
    knowledge_base = AgentKnowledge(
        vector_db=vectordb,
        num_documents=10,
    )
    print("running search")
    tweets = knowledge_base.search(query=tweet)
    reference = ''
    for tweet in tweets:
        tweetdict = tweet.to_dict()
        reference += tweetdict.get("content", "") + "\n"
    print("Reference", reference)
    tweet_content = ""
    print("agent start")
    agent = Agent(
        name="Banter Ball",
        agent_id="banterball-agent",
        introduction="Yo, I'm Banter Ball. Just for fun.",
        # model=OpenAILike(
        #     id="meta-llama/Llama-3.3-70B-Instruct",
        #     api_key=os.environ["HYPERBOLIC_API_KEY"],
        #     base_url="https://api.hyperbolic.xyz/v1",
        # ),
        model=OpenAIChat(id="gpt-4o"),
        system_prompt="""
    You are a football fanatic named 'BanterBall'. 
    You speak in slang languages, dropping roasts on players, managers and clubs. 
    sometimes use profanities,
    use humor and mild sarcasm when possible, it should be very casual always and mocking at times.
    Do not be repetitive with your language.
    """,
        use_default_system_message=False,
        task="Create gen-z tweets about football roasting other fans or players or managers or clubs",
        prevent_hallucinations=True,
        guidelines=["Sometimes rage bait", "Keep roasting, sometimes hostile"],
        expected_output="Output a tweet in first-person voice or just output LIKE or I don't know.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True,
        add_history_to_messages=True,
        num_history_response=5)

    response_stream: Iterator[RunResponse] = agent.run(
        f"{tweet} You have been given someone's tweet to whom you should reply or like or do nothing if not much relevant data available."
        f" Here are some similar tweets on the topic recently \n {reference}"
        f"\n \n Generate a reply by analyzing these tweets and the user's tweet given in the beginning."
        f" Keep it under 280 characters with focus to be very relevant and write in gen-z language use slangs"
        f"Do not use hashtages and maximum one  emojis."
        f"If you don't feel any relevancy in tweets given, then do not hallucinate and reply with 'I do not know'."
        f"Don't be repetitive with your language, keep mixing it up")
    print(f"processed tweet: {tweet}")
    print(response_stream)
    # Iterate through the response_stream
    for response in response_stream:
        # Ensure the response is a tuple and has "content" as the first element
        if isinstance(response, tuple) and response[0] == "content":
            tweet_content = response[1]  # Extract the content
            tweet_content = tweet_content.replace('"', '').replace("'", '')  # Clean up quotes
            print(f"Extracted Tweet Content: {tweet_content}")

    # Check if tweet_content was successfully extracted
    if tweet_content:
        print("Final Tweet Content:", tweet_content)
    else:
        print("No tweet content found in the response stream.")
    return tweet_content


def generate_with_vector_search(topic: str, tweets: list[str], vectordb: Qdrant) -> str:
    knowledge_base = AgentKnowledge(
        vector_db=vectordb,
        num_documents=10, )
    for tweet in tweets:
        tweet
    tweetsquery = knowledge_base.search(query=tweets)
    reference = ''
    for tweete in tweetsquery:
        tweetdict = tweete.to_dict()
        reference += tweetdict.get("content", "") + "\n"
    print("agent start")
    tweet_content = ""
    agent = Agent(
        name="Banter Ball",
        agent_id="banterball-agent",
        introduction="You are a football twitter account posting on latest news",
        model=OpenAIChat(id="gpt-4o"),
        system_prompt="""
        You are a football fan named 'BanterBall'. 
        and you love engaging on football twitter. 
        You comment on players, managers and clubs in one line just like their tweets
        There are going to be tweets like this(https://https://t.co/0iFfiux7Io),
        if you use those links, strictly match the exact language of the tweet also as the tweet is highly related to the image which is the link here
        and sometimes if dates of tweet match include some stats 
        Do not be repetitive with your language, check history for that
        """,
        use_default_system_message=False,
        task="Create tweets football based on the current trends and previous tweets reference to engange with other accounts of football fans",
        prevent_hallucinations=True,
        guidelines=["Match the tone and writing style of tweets provided", "Slight changes for tweets with links"],
        expected_output="Output a tweet in first-person voice or just output LIKE or I don't know.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True,
        add_history_to_messages=True,
        num_history_response=5)

    response_stream = agent.run(
        f"{reference} You have been given tweets from a number of popular accounts\n\n"
        f"Generate one tweet by analyzing these tweets and make a tweet of your own. "
        f"Currently the {topic} is trending and recent tweets are: {tweets} \n\n"
        f"Based on the latest news and what popular accounts have said make a tweet."
        f"make a tweet and keep it a one liner and focus to be relevant and slang."
        f"Similary match the tone of the tweets I've provided you, use slangs as they have used."
        f"Reframe some tweets to make it funnier or slight changes only."
        f"If using image in the tweet, make sure you keep the other subject matter same ore make slightest enhancement"
        f" but do not use hashtag (at maximum one hashtag), and sometimes add emojis."
        f"If you don't feel any relevancy in tweets given, then do not hallucinate and reply with 'I do not know'."
    )
    # Assuming response_stream is an iterator of RunResponse objects
    for response in response_stream:
        try:
            # Handle tuple-based responses
            if isinstance(response, tuple):
                # Check if the tuple contains 'content' as the first element
                if response[0] == "content":
                    tweet_content = response[1].replace('"', '').replace("'", "")
                    print(f"Generated Tweet Content: {tweet_content}")
                    break
                else:
                    print(f"Unexpected response structure: {response}")
            else:
                # If response is not a tuple, print it for debugging
                print(f"Unexpected response structure: {response}")
        except Exception as e:
            print(f"Error processing response: {e}")

    return tweet_content
