# google_agent

A search-grounded assistant using ADK's built-in `google_search` tool,
which is executed server-side by the Gemini API.

| | |
| --- | --- |
| Agent name | `root_agent` |
| Model | `gemini-2.5-flash` |
| Tools | `google_search` (built-in) |
| Keys | `GOOGLE_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env
```

## Run

```powershell
adk run google_agent
```

## Behaviour

The instruction tells the model to search when it needs current
information or wants to verify a fact. Grounding happens inside the
Gemini API, so no third-party search key is required.

`google_search` is a built-in tool and cannot be mixed freely with
custom function tools on every model — see
[`combined_agent`](../combined_agent) for the configuration that lets
built-in and custom tools coexist.
