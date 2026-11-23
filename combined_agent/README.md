# combined_agent

Everything from the single-purpose agents in one place: Google Search,
Tavily Search, Python execution and the world clock.

| | |
| --- | --- |
| Agent name | `root_agent` |
| Model | `gemini-3.5-flash` (`MODEL` constant) |
| Tools | `google_search`, `TavilySearch`, `get_current_time` |
| Executor | `BuiltInCodeExecutor` |
| Keys | `GOOGLE_API_KEY`, `TAVILY_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env   # needs BOTH keys
```

## Run

```powershell
adk run combined_agent
```

## How the tools coexist

Mixing a built-in tool (`google_search`) and a server-side code
executor with custom function tools needs this explicitly enabled:

```python
generate_content_config=types.GenerateContentConfig(
    tool_config=types.ToolConfig(
        include_server_side_tool_invocations=True
    )
)
```

Without it the server-side tool calls are not surfaced back to the
agent loop alongside the custom ones.

## Routing

The instruction tells the model which tool to reach for:

- **Google Search** — current information and quick fact checks
- **Tavily Search** — detailed results, multiple sources, or when
  Google Search is insufficient
- **Python** — calculations and data analysis
- **`get_current_time`** — any time or date question; never guessed

Change the model for every tool at once with the `MODEL` constant at
the top of `agent.py`.
