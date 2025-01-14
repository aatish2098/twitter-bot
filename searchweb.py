from typing import Optional, Iterator

from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.run.response import RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from phi.utils.pprint import pprint_run_response
from pydantic import BaseModel, Field


class NewsArticle(BaseModel):
    title: str = Field(..., description="Title of the article.")
    url: str = Field(..., description="Link to the article.")
    summary: Optional[str] = Field(..., description="Summary of the article if available.")
    date: Optional[str] = Field(..., description="Date of the article")


class SearchResults(BaseModel):
    articles: list[NewsArticle]


def search_internet(topic: str):
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGo()],
        instructions=["Given a topic, search for the top 5 articles."],
        response_model=SearchResults,
        structured_outputs=True,
    )
    Response = agent.run(message=topic)
    agent.print_response(Response,markdown=True)
    print(Response.content.articles[0])
    # Collect URLs from the articles
    urlarr = [article.url for article in Response.content.articles]
    print(urlarr)
    to_expand=urlarr[0]
    agentarticle = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[Newspaper4k()], debug_mode=True, show_tool_calls=True,
    )
    print(f"Expanding URL: {to_expand}")
    try:
        article_details = agentarticle.run(message=f"Expand the article from this URL: {to_expand}")
        print("Article Details:", article_details)
    except Exception as e:
        print(f"Error while fetching article details: {e}")
