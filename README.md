# Google ADK Agents

A collection of seven learning agents built with the
[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/).
Each folder is a self-contained ADK agent with its own tools,
model and environment file.

| Agent | What it does | Extra key needed |
| --- | --- | --- |
| [`chat_bot`](chat_bot) | Plain LLM assistant, no tools | — |
| [`google_agent`](google_agent) | Web search via built-in Google Search | — |
| [`tavily_search_agent`](tavily_search_agent) | Web search via Tavily (LangChain tool) | `TAVILY_API_KEY` |
| [`code_execution_agent`](code_execution_agent) | Writes and runs Python for calculations | — |
| [`world_clock_agent`](world_clock_agent) | Current time/date for any IANA timezone | — |
| [`combined_agent`](combined_agent) | Search + code execution + clock in one agent | `TAVILY_API_KEY` |
| [`refund_agent`](refund_agent) | Stateful SQLite refund workflow with confirmation | — |

---

## Quick start

Copy-paste this from the repository root to get the first agent running:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install google-adk langchain-tavily
Copy-Item chat_bot\.env.example chat_bot\.env
notepad chat_bot\.env              # paste your Gemini API key, save, close
adk web
```

Then open **http://localhost:8000**, pick `chat_bot` from the dropdown
and say hello. Stop the server with `Ctrl+C`.

If `Activate.ps1` fails with *"running scripts is disabled on this
system"*, run this once and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

## Requirements

- Python 3.12 (developed on 3.12.7)
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)
- A [Tavily](https://app.tavily.com) API key for the two Tavily-based agents

## Setup

### 1. Virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # Bash/macOS: source .venv/bin/activate
```

**Activate it in every new terminal.** The `adk` command only exists
inside the activated environment — this is the single most common
reason the project appears not to run. Your prompt shows `(.venv)`
when it is active.

### 2. Dependencies

```powershell
pip install google-adk langchain-tavily
```

Versions this project was built against:

| Package | Version |
| --- | --- |
| `google-adk` | 2.14.1 |
| `google-genai` | 2.34.0 |
| `langchain-tavily` | 0.2.18 |

### 3. API keys

Each agent reads its **own** `.env` from its own folder — there is no
shared root `.env`. Copy the template into every agent you want to run:

```powershell
# One agent
Copy-Item chat_bot\.env.example chat_bot\.env

# Or all seven at once
Get-ChildItem -Path *\.env.example | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $_.Directory ".env")
}
```

```bash
# Bash equivalent
for d in */; do cp "$d/.env.example" "$d/.env"; done
```

Then open each `.env` and paste your real keys.

| Variable | Purpose |
| --- | --- |
| `GOOGLE_GENAI_USE_VERTEXAI` | `FALSE` for API-key auth, `TRUE` for Vertex AI |
| `GOOGLE_API_KEY` | Gemini API key — needed by all seven agents |
| `TAVILY_API_KEY` | Tavily key — only `combined_agent` and `tavily_search_agent` |

`.env` and `.env.local` are gitignored. `.env.example` is the only env
file that is committed, so real keys never leave your machine.

### 4. Database (only for `refund_agent`)

```powershell
python refund_agent\setup_database.py
```

Run once. It creates `campusx.db` with the demo students and refuses to
overwrite an existing file.

## Running an agent

Always run from the **repository root**, not from inside an agent
folder — ADK treats each subdirectory as one agent.

### Browser UI (recommended)

```powershell
adk web
```

Open **http://localhost:8000** and choose the agent from the dropdown.
All seven appear in the list. `Ctrl+C` stops the server.

Use `adk web` for `refund_agent` specifically — its `request_refund`
tool pauses for a confirmation dialog that only the UI can show.

### Terminal

```powershell
adk run chat_bot
adk run world_clock_agent
```

Pass the agent's folder name to start an interactive chat, or append a
message for a single answer and exit:

```powershell
adk run world_clock_agent "what time is it in Karachi?"
```

`Ctrl+C` leaves interactive mode.

### Which to try first

| Goal | Agent |
| --- | --- |
| Just check the setup works | `chat_bot` |
| See a custom tool being called | `world_clock_agent` |
| See the most complete example | `refund_agent` (via `adk web`) |

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `adk : The term 'adk' is not recognized` | Virtual environment is not active — run `.venv\Scripts\Activate.ps1` |
| `Activate.ps1 cannot be loaded ... disabled on this system` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry |
| Agent dropdown in `adk web` is empty | You ran `adk web` from inside an agent folder — `cd` back to the repo root |
| `Missing key inputs argument` / auth error | That agent has no `.env`, or `GOOGLE_API_KEY` is still the placeholder |
| `campusx.db was not found` | Run `python refund_agent\setup_database.py` |
| Tavily agent errors on search | `TAVILY_API_KEY` missing from that agent's `.env` |
| Port 8000 already in use | `adk web --port 8080` |

## Project structure

```
Google-ADK-Agent/
├── .gitignore              # secrets, .venv, __pycache__, *.db, .adk/
├── README.md
├── chat_bot/
│   ├── __init__.py         # exposes agent for ADK discovery
│   ├── agent.py            # defines root_agent
│   ├── .env.example        # committed template
│   ├── .env                # your keys (ignored)
│   └── README.md
├── code_execution_agent/
├── combined_agent/
├── google_agent/
├── refund_agent/
│   ├── agent.py
│   ├── tools.py            # six refund tools
│   ├── setup_database.py   # creates campusx.db demo data
│   └── campusx.db          # generated (ignored)
├── tavily_search_agent/
└── world_clock_agent/
```

Each agent follows the same ADK contract: `__init__.py` re-exports
`agent`, and `agent.py` defines a module-level `root_agent`.

## Notes

- `refund_agent` is a **demo**. It writes to a local SQLite file and
  never transfers real money.
- Generated artifacts (`.adk/session.db`, `campusx.db`, `__pycache__/`)
  are intentionally untracked — delete them freely.
