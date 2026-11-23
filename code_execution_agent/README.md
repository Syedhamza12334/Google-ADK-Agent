# code_execution_agent

An assistant that writes and runs Python to answer questions, using
ADK's `BuiltInCodeExecutor`. Code runs in Gemini's sandbox, not on
your machine.

| | |
| --- | --- |
| Agent name | `root_agent` |
| Model | `gemini-2.5-flash` |
| Executor | `BuiltInCodeExecutor` |
| Keys | `GOOGLE_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env
```

## Run

```powershell
adk run code_execution_agent
```

## Behaviour

The instruction steers the model to write and execute Python whenever
a question involves calculation or data analysis, then explain the
result rather than dumping raw output.

Try: *"What is the compound interest on 50,000 at 7.5% for 12 years?"*
or *"Find the standard deviation of 12, 19, 4, 27, 31."*

Because the sandbox is server-side, it has no network access and no
view of your local files.
