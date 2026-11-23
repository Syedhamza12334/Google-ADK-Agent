
from google.adk.agents.llm_agent import Agent
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_current_time(timezone: str) -> dict:
    """Get the current date and time for a given timezone.

    Args:
        timezone: IANA timezone, e.g. Asia/Karachi,
                  Europe/Berlin, America/New_York.

    Returns:
        Current date, time, weekday and timezone.
    """

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


root_agent = Agent(
    model="gemini-2.5-flash",
    name="clock_agent",

    description="An assistant that provides current time and date worldwide.",

    instruction="""
    You are a helpful time and date assistant.

    1. Identify the city or country provided by the user.
    2. Convert the location into its correct IANA timezone.
    3. Call the get_current_time tool.
    4. Display the current date, time, weekday and timezone.
    5. If the tool returns an error, explain it to the user.
    6. Never guess the current time.
    """,

    tools=[get_current_time]
)
