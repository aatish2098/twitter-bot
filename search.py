from phi.agent import Agent
from phi.tools.website import WebsiteTools
import os
from phi.model.openai.like import OpenAILike

# agent = Agent(
#     model=OpenAILike(
#         id="meta-llama/Llama-3.3-70B-Instruct",
#         api_key=os.environ["OPENAI_API_KEY"],
#         base_url="https://api.hyperbolic.xyz/v1",
#     ),
#     tools=[WebsiteTools()], show_tool_calls=True)
# agent.print_response("", markdown=True)
#
# from phi.agent import Agent
# from phi.tools.duckduckgo import DuckDuckGo


# agent = Agent(
#     model=OpenAILike(
#         id="meta-llama/Llama-3.3-70B-Instruct",
#         api_key=os.environ["OPENAI_API_KEY"],
#         base_url="https://api.hyperbolic.xyz/v1",
#     ),
# tools=[DuckDuckGo()], show_tool_calls=True)
# agent.print_response("Get latest news on Marcus Rashford on 11 January, 2025 ", markdown=True)


from phi.agent import Agent
# from phi.tools.googlesearch import GoogleSearch
# from phi.agent import Agent, RunResponse
# from phi.utils.pprint import pprint_run_response
# from typing import Iterator
#
#
#
# agent = Agent(
#     model=OpenAILike(
#         id="meta-llama/Llama-3.3-70B-Instruct",
#         api_key=os.environ["OPENAI_API_KEY"],
#         base_url="https://api.hyperbolic.xyz/v1",
#     ),
#     tools=[GoogleSearch()],
#     description="You are a news agent that helps users find the latest news.",
#     instructions=[
#         "Given a topic by the user, respond with 4 latest news items about that topic.",
#         "Search for 10 news items and select the top 4 items.",
#         "Search in English.",
#     ],
#     show_tool_calls=True,
#     debug_mode=True,
# )
# response_stream: Iterator[RunResponse] = agent.run(message = "Marcus Rashford")
#
# pprint_run_response(response_stream, markdown=True, show_time=True)

from phi.agent import Agent
from phi.tools.spider import SpiderTools

agent = Agent(
    name="Banter Ball",
    agent_id="banterball-agent",
    introduction="Yo, I'm Banter Ball. Just for fun.",
    model=OpenAILike(
        id="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.hyperbolic.xyz/v1",
    ),
system_prompt = """
You are a witty Gen-Z football fanatic named 'BanterBall'. 
and you love banter with fans. 
You speak in Gen-Z slang, occasionally dropping playful roasts. 
sometimes use profanities but not often
but feel free to use humor and mild sarcasm.
""",
agent_data = {
    "favorite_team": "Manchester United",
    "favorite_player": "Cristiano Ronaldo",
    "preferred_style": "Gen-Z banter, mild sarcasm, witty roasts",
},
use_default_system_message=False,
task="Create entertaining, gen-z friendly tweets about football",
prevent_hallucinations=True,
expected_output="Output a short tweet in first-person voice.",
prevent_prompt_leakage=True,
add_name_to_instructions=False,
add_datetime_to_instructions=True
)


agent.print_response("""@ChelseaFC Joao Felix is so unserious NGL!
Joao Felix for me needs to start on the left in the Premier league. Him left, Palmer 10 & Sancho on the right please
#Chelsea 5-0 Morecambe: Tosin becomes unlikely Blues goalscorer as Joao Felix shows his class 🤩🔵

✍️ @NJEmms
@CFC_OBED We need to find a Balance for Joao Felix and Palmer to play together
Joao Felix should be considered more in the premier league. They are just wasting him
Joao Felix is a starter
I hope I don’t see Joao Felix hype on my TL yuno
Joao Felix I almost forgave you for what you did to the bug with your game today
A brilliant performance from Joao Felix... 💤🔵
Only Joao Felix fans are allowed to like this post. 

Special talent 💙👊
@ChelseaFC Joao Felix, they can never make me hate you
@ChelseaFC The half time subs changed the game. We should play Veiga more in DM. T. George is the real deal. Sancho is a very good player. Nkunku with his goal. Joao Felix with his goals. Tosin my MOTM.
Joao Felix best player on earth btw
First clean sheet of 2025.

Tosin Adaribioyo '40 '70
Christopher Nkunku 50'
Joao Felix 75' 77'

#Chels1905 #CFC
Oh, bravo! Tosin, Nkunku, and Joao Felix must be so proud, picking on a minor club. True champions! 😂
#FAcup
Joao Felix with freedom Is one of the most dangerous Players in the World 🥶
Tosin and Joao Felix were able to make it from anywhere on the pitch today. 

5-0 win for the Blues over Morecambe in the 3rd round of the FA cup. 

Let’s go!!
@Adeyanju22 Joao Felix made the final 😭
@Jaythekeed @the_akinola make he Dey joke now, he rates Joao Felix but he no rate Jackson 🤣🤣🤣🤣
Joao Felix and Palmer can play together.
Full-Time.

Chelsea 5-0 Morecambe

⚽️⚽️ 39', 70' Tosin Adarabioyo
⚽️ 50' Christopher Nkunku
⚽️⚽️ 75', 77' Joao Felix

📊 Statistics

81% - 19% Ball Possession
28 - 7 Shots
Our Wines & Spirit POS System helps you manage stock,accurate reporting,MPESA integration,Receipting etc📞0716413386

#MUFC Chelsea Adarabioyo Nkunku Joao Felix Liverpool Chiesa Diego Jota Trent Danns #FACup Tosin Kairo Atalanta Reece James Nunez Lavia Kvara Napoli Marmoush
Joao Felix they can never make me hate you
@ChelseaFC Joao Felix🛐🛐
Guys hating on Joao Felix are too cringe man honestly
I can never hate Joao Felix
This This Tops A Playoff W starts here:

Generate a fresh tweet about Joao Felix. Keep it under 280 characters and write it referring the above tweets and with focus to be genuine, use 2 or 3 hashtags and fewer emojis""",
                     markdown=True)
