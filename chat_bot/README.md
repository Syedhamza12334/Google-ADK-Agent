# chat_bot

The simplest agent in this repo: a plain Gemini assistant with no tools.
Useful as a baseline to confirm your API key and ADK install work.

| | |
| --- | --- |
| Agent name | `root_agent` |
| Model | `gemini-3.5-flash` |
| Tools | none |
| Keys | `GOOGLE_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env   # then paste your Gemini API key
```

## Run

From the repository root:

```powershell
adk run chat_bot
# or: adk web   and pick chat_bot
```

## Behaviour

Answers from the model's own knowledge only. It cannot search the web,
so anything after the model's training cutoff may be wrong or outdated —
use [`google_agent`](../google_agent) or
[`tavily_search_agent`](../tavily_search_agent) for current information.
