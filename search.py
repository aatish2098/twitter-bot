from typing import Iterator
from phi.knowledge import AgentKnowledge
from phi.run.response import RunResponse
import os
from phi.model.openai.like import OpenAILike
from phi.agent import Agent
from phi.vectordb.qdrant import Qdrant


def fetch_with_raw_tweets(tweets_str: str, topic: str) -> str:
    tweet_content = ""
    agent = Agent(
        name="Banter Ball",
        agent_id="banterball-agent",
        introduction="Yo, I'm Banter Ball. Just for fun.",
        model=OpenAILike(
            id="meta-llama/Llama-3.3-70B-Instruct",
            api_key=os.environ["HYPERBOLIC_API_KEY"],
            base_url="https://api.hyperbolic.xyz/v1",
        ),
        system_prompt="""
You are a Gen-Z football fanatic named 'BanterBall'. 
and you love banter with fans. 
You speak in Gen-Z slang, dropping roasts on players, managers and clubs. 
sometimes use profanities, not often
but feel free to use humor and mild sarcasm.
""",
        agent_data={
            "favorite_team": "Manchester United",
            "favorite_player": "Cristiano Ronaldo",
            "preferred_style": "Gen-Z banter, mild sarcasm, roasts",
        },
        use_default_system_message=False,
        task="Create gen-z friendly tweets about football roasting other fans or players or managers or clubs",
        prevent_hallucinations=True,
        guidelines=["Sometimes rage bait", "Stay roasting, sometimes offensive"],
        expected_output="Output a short tweet in first-person voice.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True)

    response_stream: Iterator[RunResponse] = agent.run(
        f"{tweets_str}\n\nGenerate a tweet by analyzing these tweets. Keep it under 280 characters and write it referring the above tweets and with focus to be hurtful and sometimes rage bait, do not use hashtag, at maximum one hashtag and sometimes add emojis"
    )
    # Assuming response_stream is an iterator of RunResponse objects
    for response in response_stream:
        # Check if the tuple contains the 'content' key
        if isinstance(response, tuple) and response[0] == "content":
            tweet_content = response[1].replace('"', '').replace("'", '')
            print(f"{tweet_content}")

    return tweet_content


def generate_with_vector_search(vectordb: Qdrant) -> str:
    knowledge_base = AgentKnowledge(
        vector_db=vectordb,
        num_documents=10,

    )
    tweets=knowledge_base.search(query="Ronaldo")
    reference=''
    for tweet in tweets:
        tweetdict = tweet.to_dict()
        reference += tweetdict['content'] + "\n"
    tweet_content = ""
    agent = Agent(
        name="Banter Ball",
        agent_id="banterball-agent",
        introduction="Yo, I'm Banter Ball. Just for fun.",
        model=OpenAILike(
            id="meta-llama/Llama-3.3-70B-Instruct",
            api_key=os.environ["HYPERBOLIC_API_KEY"],
            base_url="https://api.hyperbolic.xyz/v1",
        ),
        system_prompt="""
    You are a Gen-Z football fanatic named 'BanterBall'. 
    and you love banter with fans. 
    You speak in Gen-Z slang, dropping roasts on players, managers and clubs. 
    sometimes use profanities, not often
    but feel free to use humor and mild sarcasm.
    """,
        agent_data={
            "favorite_team": "Manchester United",
            "favorite_player": "Cristiano Ronaldo",
            "preferred_style": "Gen-Z banter, mild sarcasm, roasts",
        },
        use_default_system_message=False,
        task="Create gen-z friendly tweets about football roasting other fans or players or managers or clubs",
        prevent_hallucinations=True,
        guidelines=["Sometimes rage bait", "Stay roasting, sometimes offensive"],
        expected_output="Output a short tweet in first-person voice.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True,
        knowledge=knowledge_base)

    response_stream: Iterator[RunResponse] = agent.run(
        f"{reference} You have been given tweets from a number of popular accounts\n\nGenerate 4-5 tweets by analyzing these tweets. Keep it under 280 characters and write it referring the above tweets and with focus to be hurtful and sometimes rage bait, do not use hashtag, at maximum one hashtag and sometimes add emojis. If you don't feel any relevancy in tweets given then do not hallicunate, and send I do not know"
    )
    # Assuming response_stream is an iterator of RunResponse objects
    for response in response_stream:
        # Check if the tuple contains the 'content' key
        if isinstance(response, tuple) and response[0] == "content":
            print(f"{tweet_content}")
            tweet_content = response[1].replace('"', '').replace("'", '')

    return tweet_content