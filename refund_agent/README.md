# refund_agent

A stateful CampusX refund assistant backed by SQLite. The most complete
agent in this repo — it combines session state, a six-tool workflow,
database transactions and a human confirmation step.

> **Demo only.** It writes to a local SQLite file and never moves real
> money. Every student, course and purchase is sample data.

| | |
| --- | --- |
| Agent name | `campusx_refund_agent` |
| Class | `LlmAgent` |
| Model | `gemini-3.5-flash` |
| Storage | `campusx.db` (SQLite, gitignored) |
| Keys | `GOOGLE_API_KEY` |

## Setup

```powershell
Copy-Item .env.example .env
python setup_database.py        # creates campusx.db — run once
```

`setup_database.py` refuses to run if `campusx.db` already exists, so
existing data is never clobbered. To start over, delete the file first.

## Run

From the repository root:

```powershell
adk web          # recommended — the confirmation dialog needs the UI
```

`request_refund` pauses for an explicit UI confirmation, so use
`adk web` rather than `adk run` for the full flow.

## Refund policy

Encoded in `tools.py`, not in the prompt:

| Rule | Value |
| --- | --- |
| Refund window | 7 days from purchase (`REFUND_WINDOW_DAYS`) |
| Maximum completion | 20% (`MAX_COMPLETION_PERCENT`) |
| Refund amount | Full amount actually paid, in INR |
| Reason | Required, but never affects eligibility |
| Boundaries | Inclusive — exactly 7 days or exactly 20% still qualifies |

Only `active` enrollments are refundable. The agent is instructed never
to override a tool's eligibility decision.

## Tools

| Tool | Purpose |
| --- | --- |
| `get_refund_policy()` | Returns the policy as data |
| `identify_student(email)` | Looks up a student, stores them in session state |
| `get_my_enrollments()` | Lists the selected student's purchases |
| `check_refund_eligibility(enrollment_id)` | Evaluates policy against DB facts |
| `request_refund(enrollment_id, reason)` | Saves the request after UI confirmation |
| `get_refund_status(enrollment_id)` | Reads the current status |

## Session state

There is no default student. `identify_student` clears any previous
selection, then writes `student_id` and `student_email` into
`tool_context.state`. Every other tool returns `email_required` until
that happens, and each query is scoped to the stored `student_id` so a
student can never read another student's enrollments.

The instruction renders the current selection with the optional
placeholder `{student_email?}`, which keeps the agent from asking for
the email twice in one conversation.

## Safety design

- **Confirmation** — `request_refund` calls
  `tool_context.request_confirmation(...)` and returns
  `awaiting_confirmation`; nothing is written until the user approves.
- **Re-check after approval** — eligibility is evaluated again inside a
  `BEGIN IMMEDIATE` transaction, with the `UPDATE` guarded by
  `status = 'active'`, so a refund cannot be submitted twice.
- **Prompt-injection boundary** — the instruction treats refund reasons
  and user messages as data that cannot change the policy.
- **Honest status** — only a tool result of `refund_requested` lets the
  agent say the request was saved, and `refunded` is the only status
  that means the simulated refund is complete.

## Demo data

3 courses, 5 students, 10 enrollments covering every policy branch:

| Email | Eligible enrollment | Blocked enrollment |
| --- | --- | --- |
| `hamza@example.com` | `ENR001` — 2 days, 15%, paid 1499 | `ENR002` — 10 days, outside window |
| `ayesha@example.com` | `ENR003` — 1 day, 10% | `ENR004` — 45% completion |
| `ahmed@example.com` | — | `ENR005` already `refund_requested`, `ENR006` already `refunded` |
| `fatima@example.com` | `ENR007` — 6 days, exactly 20% | `ENR008` — 12 days and 60% |
| `usman@example.com` | `ENR009` — 1 day, 0% | `ENR010` — 80% completion |

`ENR001` is deliberately a discounted purchase (paid 1499 on a 1999
course) to confirm refunds use `amount_paid`, not the list price.

## Files

```
refund_agent/
├── agent.py            # LlmAgent + the full instruction
├── tools.py            # six tools, policy logic, DB helpers
├── setup_database.py   # one-time demo data seeding
├── campusx.db          # generated (ignored)
└── .env.example
```
