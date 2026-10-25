# Check the test yourself

Run the benchmark yourself on made-up notes, and compare it with the result we got.

## What is here

| Path | What it is |
|---|---|
| `sample-notes/` | 24 made-up Markdown notes about a picture book, a client and a home server. No real person, client or secret |
| `questions.json` | 16 questions, each with the one note that should come up. These are the "tuning" questions |
| `holdout.json` | 10 more questions, kept apart. Nothing is tuned on them |

The notes are small on purpose, so you can read all of them in a few minutes and check every answer by eye.

## What the sample notes test

| Note | What it checks |
|---|---|
| `CLAUDE.md` | Rule notes count more and never fade |
| `Context/` | Context notes count more |
| `Projects/Picture-Book/archive/old-schedule.md` | An old archived note must not beat the new schedule |
| `Memory/decisions/2026-08-30-harbour-press.md` | A note marked `superseded` is hidden |
| `Daily/scratch.md` | A note with `engram: skip` is never indexed |
| `Memory/finances/` | A private folder is findable but locked: you see only the file and heading |
| `Projects/Home-Server/server.md` | Exact strings (a version number) match letter for letter. It also holds a made-up password line that must be blanked before it is stored |
| `Projects/Zine-Club/notes/log.md` | A log note ranks lower than a normal note |
| `Library/` | Outside material counts less |

## Run it

Phygital Engram never writes to your notes, so it is safe to point it at this folder. Keep its own data folder outside the notes. From the repository folder:

```bash
export ENGRAM_VAULT="$PWD/tests/sample-notes"
export ENGRAM_DATA="$HOME/phygital-engram-sample-data"
```

Build the index:

```bash
python3 engram.py ingest --rebuild
```

You should see `indexed 22`, `hidden 1` (the superseded note) and `ignored 1` (the note marked `engram: skip`).

Score the questions:

```bash
python3 engram.py test
```

Check the index is healthy:

```bash
python3 engram.py health
```

You should see a list of lines starting with `OK`.

> [!NOTE]
> Version 0.1.1 is an early release, so command and setting names may still change. If a command here does not work, check [docs/settings.md](../docs/settings.md) and [docs/setup-computer.md](../docs/setup-computer.md).

## The result we got

Measured on 2026-10-25 with the working version, on a Mac, without note cards.

| Set | Questions | Right note first | In the top 5 | In the top 10 |
|---|---|---|---|---|
| Tuning | 16 | 14 | 15 | 15 |
| Hidden | 10 | 10 | 10 | 10 |

Each search took under 1 millisecond on these 22 notes. Health check: every line `OK`, 1 note hidden, 1 skipped on purpose, 1 private note findable as "where only".

One question was missed, and we left it in: *which printer did we choose* came back with the schedule note first, because it also mentions the printer. The decision note it should find was not in the top 10.

> [!IMPORTANT]
> This small sample is not the same as the numbers on the benchmark picture. Those come from one person's own notes (about 4,800 of them), which are private and cannot be shared. With only 22 notes, plain word matching scores almost the same as the full ranking (a word-only run got 14 first and 15 in the top 5 too). The extra signals, like folder, age and status, start to matter when you have hundreds or thousands of notes. See [docs/benchmarks.md](../docs/benchmarks.md).

## Add your own questions

A question file is a list. Each item has the question, the note that should come up, a phrase it should hold, and a kind:

```json
{
  "q": "when is the cover due",
  "expect_files": ["Projects/Picture-Book/notes/schedule.md"],
  "expect": ["cover to the 15th of November"],
  "kind": "fact"
}
```

The kinds used here are `fact`, `exact` (versions, IDs), `paraphrase` (different words than the note), `decision` and `evergreen` (rules that never fade). Write the question the way you would ask it, not the way the note is written.

To test your own notes, point `ENGRAM_VAULT` at your folder, write 20 or more questions with notes you know, and keep a few apart as a hidden set that you never tune on.
