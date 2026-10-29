# Tools the AI can use

The four tools an AI app can use, what each one returns, and what none of them can do.

## The 4 tools

The tools are the same in both versions: the one on your computer (`mcp/server.py`) and the server version (`mcp/serve.py`, see [setup-own-server.md](setup-own-server.md)). The server version adds a login. It does not add or change a tool.

| Tool | What it does | Changes anything? |
|---|---|---|
| `search_notes` | Searches your notes and returns a short ranked list | No |
| `open_result` | Opens one result: the full section, or the whole note if it is short | No |
| `around_result` | Shows the sections before and after a result, and notes from the same day | No |
| `check_index` | Says if the index is fresh, if anything private slipped in, and if searches are fast, and lists the main folders | No |

All four only read. None can write to, move or delete a note. Each one runs the Phygital Engram command line and returns what it prints.

## `search_notes`

You give it a question in plain words, and optionally how many results you want (1 to 20, default 8). You can also give a folder, like `Projects/Picture-Book`, and only notes inside it come back. On the command line it is `--folder`. Each result has an id, the note, the heading, a snippet and a line saying why it came back. Example of what comes back:

```
#14 Projects/Picture-Book/notes/schedule.md > schedule > Schedule
   Schedule: Marta moved the cover to the 15th of November. Print files follow a week later.
   why: 6 days old
```

## `open_result` and `around_result`

You give them the id from a search, like `14`. `open_result` returns the text. `around_result` returns what sits next to it, so the AI can read a little before and after.

## `check_index`

No input. It returns the same lines as the health check: index age, notes hidden, notes skipped on purpose, private files, speed. Then the main folders, made from your notes: each top folder, how many notes it holds, and the first line of its `README.md`, `AGENTS.md` or `CLAUDE.md` (or a few recent note names). The AI app also gets this map when it connects, so it can pick a `folder` for `search_notes`. On the command line it is `python3 engram.py map`.

## What comes back is labelled

Every answer starts with a line saying it is note content: information, never instructions. The connector also tells the AI, when it connects, to treat text from your notes as data and never follow orders written inside a note.

## Private notes stay locked

A note in a private folder shows up in a search as `LOCKED`, with only its file and heading. It cannot be opened with `open_result` or `around_result`: the tool says so and tells the AI to let you open it yourself. No tool takes a password or a key.

## When a tool says no

| You see | What it means |
|---|---|
| `That result is private and locked` | The id starts with `p`. Open it yourself in your terminal |
| `That is not a result id` | The id has to come from `search_notes` |
| `Phygital Engram is not installed here` | The connector cannot find `engram.py`. See [connect-your-ai.md](connect-your-ai.md) |
| `The search took too long and was stopped` | A search ran past 30 seconds. Run `check_index` or see [troubleshooting.md](troubleshooting.md) |
| `No matching notes` | Nothing matched. Try other words |

## Limits

- A question is cut to 500 characters.
- A search returns 1 to 20 results.
- An answer is cut at 20,000 characters.
- A call is stopped after 30 seconds.

## Asking first

None of the tools change anything, so none of them needs an extra approval from Phygital Engram. Your AI app may still ask before it runs a tool. That is the app's own setting.
