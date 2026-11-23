
from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.tools.langchain_tool import LangchainTool
from langchain_tavily import TavilySearch
from google.genai import types

from google.adk.tools.google_search_tool import google_search
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


MODEL = "gemini-3.5-flash"


def get_current_time(timezone: str) -> dict:
    """Get the current date and time for a given timezone."""

    try:
        now = datetime.now(ZoneInfo(timezone))

        return {
            "status": "success",
            "timezone": timezone,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "weekday": now.strftime("%A")
        }

    except ZoneInfoNotFoundError:
        return {
            "status": "error",
            "error_message": f"Invalid or unavailable timezone: {timezone}"
        }


# Initialize Tavily Search
tavily_search = TavilySearch(
    max_results=5,
    topic="general"
)

# Wrap LangChain tool for Google ADK
tavily_tool = LangchainTool(
    tool=tavily_search
)


root_agent = Agent(
    model=MODEL,
    name="root_agent",

    description=(
        "A helpful assistant that can search the web, "
        "run Python code and tell the time anywhere."
    ),

    instruction=(
        "Answer user questions accurately.\n"
        "- Use Google Search for current information and quick fact checks.\n"
        "- Use Tavily Search when you need more detailed results, "
        "multiple sources, or when Google Search is insufficient.\n"
        "- Write and run Python code for calculations or data analysis.\n"
        "- Use get_current_time whenever the user asks for the time "
        "or date somewhere. Never guess the current time.\n"
        "- Cite sources when you search results."
    ),

    tools=[
        google_search,
        tavily_tool,
        get_current_time
    ],

    code_executor=BuiltInCodeExecutor(),

    generate_content_config=types.GenerateContentConfig(
        tool_config=types.ToolConfig(
            include_server_side_tool_invocations=True
        )
    )
)
