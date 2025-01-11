from typing import Iterator
from phi.run.response import RunResponse
import os
from phi.model.openai.like import OpenAILike
from phi.agent import Agent


def fetch_with_raw_tweets(tweets_str: str,topic: str) -> str:
    tweet_content=""
    agent = Agent(
        name="Banter Ball",
        agent_id="banterball-agent",
        introduction="Yo, I'm Banter Ball. Just for fun.",
        model=OpenAILike(
            id="meta-llama/Llama-3.3-70B-Instruct",
            api_key=os.environ["OPENAI_API_KEY"],
            base_url="https://api.hyperbolic.xyz/v1",
        ),
        system_prompt="""
You are a witty Gen-Z football fanatic named 'BanterBall'. 
and you love banter with fans. 
You speak in Gen-Z slang, occasionally dropping playful roasts. 
sometimes use profanities, not often
but feel free to use humor and mild sarcasm.
""",
        agent_data={
            "favorite_team": "Manchester United",
            "favorite_player": "Cristiano Ronaldo",
            "preferred_style": "Gen-Z banter, mild sarcasm, witty roasts",
        },
        use_default_system_message=False,
        task="Create entertaining, gen-z friendly tweets about football",
        prevent_hallucinations=True,
        guidelines=["No hate speech", "Stay comedic, sometimes offensive"],
        expected_output="Output a short tweet in first-person voice.",
        prevent_prompt_leakage=True,
        add_name_to_instructions=False,
        add_datetime_to_instructions=True,
        parse_response=True)

    response_stream: Iterator[RunResponse] = agent.run(
        f"{tweets_str}\n\nGenerate a fresh tweet about {topic}. Keep it under 280 characters and write it referring the above tweets and with focus to be genuine, use 2 or 3 hashtags and sometimes add emojis"
    )
    # Assuming response_stream is an iterator of RunResponse objects
    for response in response_stream:
        # Check if the tuple contains the 'content' key
        if isinstance(response, tuple) and response[0] == "content":
            tweet_content = response[1].replace('"', '').replace("'", '')
            print(f"{tweet_content}")

    return tweet_content
