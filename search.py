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
    model=OpenAILike(
        id="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.hyperbolic.xyz/v1",
    ))
agent.print_response("""A Pedri masterclass tomorrow is all I ask Lord
@Mario___RM Balde >> Fran García

Cubarsí >> Asencio

Araujo >> Rudiger

Pedri >> Camavinga

I agree with the rest
@sammy__dray Rodri
Bed
Pedri
GOETZE?????? Pedri & Foden go think say dem di play pass GOETZE 😂😂😂

Dey play

Mario Goetze 2013-2016 man was a little magician in midfield
@Josemaguti3 @Mario___RM X Pedri? 🤣🤣🤣🤣Have they put poison in your food?
@faisalosophy_ @YashRMFC Players behind the ball are CM. It like putting Bruno in a Modric or Kroos conversation because Bruno have more goals, assist, key passes etc.

I am not an hater... I won't say olmo is better Valverde... Same way I won't say Bellingham is better than Pedri.
Pedri and Bellingham are gonna settle the better midfielder debate on Sunday by one of them scoring and then they both make out hardcore style
@Joshua_Ubeku Pedri rodri Jude
@Nawas_masood Pedri is clr off both of them
@thicknation_00 @Big0lBean @PandaNoComply I can understand people saying Messi is better then The Goat.

But Pedri then. Bellingham? No not even in Pedri dream he is better
Because Pedri doesn't have the balls to protect his teammates
Morning Gavi and Pedri trophy pics 🏆 👿

These are the recent tweets about Pedri, base your opinion and make a joke about in gen-z style to get engagment on twitter, use basic hashtags and fewer emojis""", markdown=True)
