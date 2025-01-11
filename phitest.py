import os
from phi.agent import Agent, RunResponse
from phi.model.openai.like import OpenAILike

agent = Agent(
    model=OpenAILike(
        id="meta-llama/Llama-3.3-70B-Instruct",
        api_key=os.environ["OPENAI_API_KEY"],
        base_url="https://api.hyperbolic.xyz/v1",
    )
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")
