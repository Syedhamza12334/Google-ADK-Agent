# world_clock_agent

Reports the current date and time anywhere in the world using a custom
Python function tool — the smallest useful example of a hand-written
ADK tool in this repo.

| | |
| --- | --- |
| Agent name | `clock_agent` |
| Model | `gemini-2.5-flash` |
| Tools | `get_current_time(timezone)` |
| Keys | `GOOGLE_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env
```

## Run

```powershell
adk run world_clock_agent
```

## The tool

```python
def get_current_time(timezone: str) -> dict:
    """Get the current date and time for a given timezone."""
```

Takes an IANA timezone (`Asia/Karachi`, `Europe/Berlin`,
`America/New_York`) and returns `date`, `time`, `weekday` and
`timezone`, resolved with the standard-library `zoneinfo`.
An unknown zone returns `{"status": "error", ...}` instead of raising.

The agent's job is to turn a city or country name into the right IANA
zone, call the tool, and never guess the time itself.

The docstring and type hint are what ADK sends to the model as the
tool schema — keep them accurate when you edit the function.
