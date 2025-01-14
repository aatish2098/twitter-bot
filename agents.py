from typing import Iterator, Any
from phi.knowledge import AgentKnowledge
from phi.knowledge.json import JSONKnowledgeBase
from phi.model.openai import OpenAIChat
from phi.run.response import RunResponse
from phi.agent import Agent
from phi.vectordb.qdrant import Qdrant
from phi.utils.pprint import pprint_run_response
from qdrantfunctions import fetch_on_topic
from searchdefi import get_scanner_project


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


def analysis_of_contract(address: str, chainid: int) -> str:

    print("running search")
    scanner=get_scanner_project(address, chainid)
    scanner=str(scanner)
    print("agent start")
    agent = Agent(
        name="Crypto AI agent",
        agent_id="cypto-ai-agent",
        introduction="You are a Crypto and Blockchain expert analyzing trending coins, market trends, and blockchain developments.",
        model=OpenAIChat(id="gpt-4o"),
        # model=OpenAILike(
        #     id="meta-llama/Llama-3.3-70B-Instruct",
        #     api_key=os.environ["HYPERBOLIC_API_KEY"],
        #     base_url="https://api.hyperbolic.xyz/v1",
        # ),
        system_prompt=""" 
        You analyze cryptocurrencies, blockchain projects, and market trends. 
        You are given details of coin and you've to assess it and tell if its good or not.
        """,
        use_default_system_message=False,
        task="Give comprehensive assessment for the coin details provided",
        prevent_hallucinations=True,
        guidelines=["Provide accurate and concise crypto analysis"],
        expected_output="Output your analysis in first-person voice or just output I don't know.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True)

    response_stream = agent.run(
        f"{scanner} \n\nYou have been given the Scanned results of a token\n\n"
        f" by analyzing these metrics, give a comprehensive analysis of your own."
        f" Tell the pros and cons and if the analysis shows project is promising or not."
        f"If you don't feel any relevancy, then do not hallucinate and reply with 'I do not know'.")
    print(response_stream.content)
    pprint_run_response(run_response=response_stream,markdown=True)
    # Iterate through the response_stream
    return response_stream


def generate_with_vector_search(topic: str, vectordb: Qdrant) -> str:
    knowledge_base = AgentKnowledge(
        vector_db=vectordb,
        num_documents=10,
    )
    print("running search")
    tweets = knowledge_base.search(query=topic)
    reference = ''
    for tweet in tweets:
        tweetdict = tweet.to_dict()
        reference += tweetdict.get("content", "") + "\n"
    print("Reference", reference)
    agent = Agent(
        name="Crypto AI agent",
        agent_id="cypto-ai-agent",
        introduction="You are a Crypto and Blockchain expert analyzing trending coins, market trends, and blockchain developments.",
        model=OpenAIChat(id="gpt-4o"),
        system_prompt=""" 
        You analyze cryptocurrencies, blockchain projects, and market trends in one or two lines. 
        If relevant, include data such as price movements, market cap, or trading volume. 
        Do not be repetitive with your language; check the history of your responses to maintain variety.
        """,
        use_default_system_message=False,
        task="Create engaging and insightful crypto-related tweets based on current trends, historical context, and reference tweets to engage with the crypto community.",
        prevent_hallucinations=True,
        guidelines=["Provide accurate and concise crypto analysis"],
        expected_output="Output a tweet in first-person voice or just output I don't know.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True,
        add_history_to_messages=True,
        num_history_response=5,
        knowledge_base=knowledge_base,
        add_context=True)

    response_stream = agent.run(
        f"{reference}You have been given tweets from a number of popular accounts on the {topic} for the last 24 hours or so\n\n"
        f"Based on the latest news and what popular accounts have said make a tweet."
        f"Generate one tweet by analyzing these tweets and make a tweet of your own."
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
