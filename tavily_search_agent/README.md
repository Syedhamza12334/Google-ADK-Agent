# tavily_search_agent

The same job as [`google_agent`](../google_agent), but search runs
through [Tavily](https://tavily.com) wrapped as an ADK tool via
LangChain. Handy when you want control over result count and topic,
or richer source snippets.

| | |
| --- | --- |
| Agent name | `root_agent` |
| Model | `gemini-3.5-flash` |
| Tools | `TavilySearch` via `LangchainTool` |
| Keys | `GOOGLE_API_KEY`, `TAVILY_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env   # needs BOTH keys
```

Get a Tavily key at [app.tavily.com](https://app.tavily.com).
Requires `langchain-tavily` (installed at the repo root).

## Run

```powershell
adk run tavily_search_agent
```

## Configuration

Search behaviour is set in `agent.py`:

```python
tavily_search = TavilySearch(
    max_results=5,
    topic="general",
)
```

Raise `max_results` for broader coverage, or switch `topic` to
`"news"` / `"finance"` for domain-tuned results.
