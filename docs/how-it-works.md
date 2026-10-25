# How it works

This page is for anyone curious about what happens inside. You will learn what Phygital Engram reads, what it keeps, and why a search takes milliseconds.

<details>
<summary><b>Table of contents</b></summary>

- [The pieces](#the-pieces)
- [Two rules it never breaks](#two-rules-it-never-breaks)
- [What happens when your notes change](#what-happens-when-your-notes-change)
- [What happens when you ask](#what-happens-when-you-ask)
- [What's stored](#whats-stored)
- [Why it is fast](#why-it-is-fast)
- [How a result is opened](#how-a-result-is-opened)
- [Note cards, the optional extra](#note-cards-the-optional-extra)
- [Health and tests](#health-and-tests)
- [The code](#the-code)

</details>

<p align="center"><img src="images/how-it-works.png" alt="Five steps from your notes to your agent: your notes, a list of them kept outside your folder, the ranking, a short list of results with note, heading and date, and your agent opening the best one and answering." width="640"></p>

## The pieces

Phygital Engram has four pieces.

| Piece | What it is | What it does |
|---|---|---|
| Your notes folder | A folder of Markdown (`.md`) files, in any app you like | Holds your notes. Phygital Engram only reads it |
| The index | One small database file, kept outside your notes folder | Stores every section of every note so it can be searched in milliseconds |
| The search | The part that takes a question and ranks sections | Finds the best sections and says why it picked each one |
| Your agent | Claude, ChatGPT, Codex or any AI app you use | Asks the question, reads the short result, and answers you |

Phygital Engram finds notes. It does not answer for you. Your agent writes the answer. The result is short, so your agent reads a few lines instead of dozens of notes.

You can use it from the command line (typed commands) and from a small page on your own computer. An AI connector (MCP, a plug for AI apps) is in the repository too. It runs this command line for every call and gives your AI app four read-only tools. It worked in Claude Code and has not been tried in other apps yet. See [Tools](tools.md).

## Two rules it never breaks

1. **It only reads your notes.** It never writes, moves, renames or deletes a note. If you point its data folder inside your notes folder, it refuses to start.
2. **Your notes stay the original.** You can delete the index at any time and rebuild it from your notes. That takes about 15 seconds for roughly 5,000 notes.

## What happens when your notes change

These steps run in order every time the index updates, whether by hand or on a schedule you set.

1. **Safety check.** If the notes folder looks wrong, nothing changes. For example, your top rule file may be missing because a sync is half done. Another update already running also stops this one.
2. **Find the notes.** Every `.md` file is read. These are skipped: hidden folders (`.obsidian`, `.git`, `.claude`, `.trash`), anything in your ignore file, files over 2 MB, and notes with an `engram: skip` line near the top. Only notes that changed since last time are read again.
3. **Blank the secrets.** Lines that look like keys, tokens or passwords become `[REDACTED]`. Labelled tax IDs, bank numbers (IBANs) and card numbers are blanked too. See [safety](safety.md).
4. **Read the info block.** The fields at the top of a note (`date`, `updated`, `type`, `project`, `status`, `tags`, `keep`, `valid_until`) help decide how the note ranks.
5. **Work out the date.** It uses the first one it finds: `updated`, `date`, a date in the file name, the file's own time.
6. **Cut into sections.** Each note is cut at its headings. A section keeps its heading path, like `Picture-Book > Cover > Due dates`. Very small sections join the next one. Very long ones are split with a small overlap, so no sentence is lost at the cut.
7. **Weigh and hide.** Each section gets a weight from its folder, status and type (see [search ranking](search-ranking.md)). Notes marked superseded, deprecated or replaced, or past their `valid_until` date, are hidden.
8. **Remove deleted notes.** A note you deleted leaves the index. If more than a fifth of all notes vanish at once, it refuses and keeps the old index, because the copy it saw is probably incomplete.
9. **Private folders go to their own index.** See [privacy](privacy.md).

If you change a setting that affects the index (weights, patterns, section sizes), the next update rebuilds by itself.

## What happens when you ask

Say you ask your agent: *when is the Picture-Book cover due?*

1. **Your agent sends the question.** A longer question is cut to 500 characters and 20 words.
2. **Words are matched.** The question's words are compared with the word index. Rare words count more than common ones. Words match by their root, so "dashes" finds "dash".
3. **Exact strings are checked.** Version numbers, IDs, file paths, host names and anything in "quotes" are also matched letter for letter. They count a little more.
4. **The weights are applied.** These are folder level, status, type, how new the note is, and a few light extras. [Search ranking](search-ranking.md) covers each one.
5. **The list is shaped.** You get at most two sections per note and at most 50 results. Background folders come after the main ones.
6. **Each result gets a "why" line.** For example: "your words in the heading, Projects, from today".
7. **Your agent gets a short list.** Each result has the note's path, the heading, a short snippet with your words marked, the date, and the why line.
8. **Your agent opens what it needs.** It asks for the full section of the one or two results that matter. See [how a result is opened](#how-a-result-is-opened).

On the author's notes (about 4,800), the whole search takes 9 to 37 milliseconds. See [benchmarks](benchmarks.md) for what was measured and how.

## What's stored

| What | Where | Who can read it |
|---|---|---|
| Your notes | Your notes folder, untouched | You, and any app you already use on it |
| The index (sections, word index, dates, weights) | One database file in the data folder, outside your notes | You. It holds the text of your notes, so treat it like your notes |
| Note cards (optional) | Inside the same index, kept even when the index is rebuilt | You. Only made if you turn them on |
| Learning from use (counts of what was shown and opened) | Inside the index | You. Only counts are kept, never your questions |
| Private folders | A second database file, with text locked until you ask | You |

There is no account, no cloud copy and no tracking.

## Why it is fast

- Your notes are cut up and indexed ahead of time, not when you ask.
- The word index is SQLite's built-in full-text search. SQLite is a small database that already comes with Python, so there is nothing extra to install.
- Ranking works in two steps. First it ranks small facts only (id, scores, weights, dates). Only the few results shown get their text fetched and their snippets built.
- The index keeps the text once, not twice.
- A 500,000-note test copy still answered in 0.23 seconds.

## How a result is opened

A search result is short on purpose. Your agent can ask for more in three ways:

| Action | What your agent gets |
|---|---|
| Open a result | The full section, or the whole note |
| Around a result | The sections before and after it, and notes from the same day |
| Private result | The text of a locked note, only after you ask |

## Note cards, the optional extra

If you add an AI key, Phygital Engram can write one short card for every section. A card has a line of context, a summary, 3 to 5 questions someone might ask, and up to 6 exact facts. Cards help when you ask in different words than the note uses. Without a key, search still works. See [cards](cards.md).

## Health and tests

- **Health check.** One line per area: index, notes copy, privacy (no secret files or ID numbers in the main index), cards and speed. Each line is OK, WARN or FAIL, with the fix. Speed warns over 300 milliseconds.
- **Test score.** You can write test questions, each with the note that should come first. The score shows how many land in the top 1, 5 and 10. See [benchmarks](benchmarks.md).

## The code

It is written in Python, and the search itself uses only the standard library. The AI connector (`mcp/server.py`, Python, standard library only) is in this repository. The search code (`engram.py`) is not yet. It is being tuned first and arrives with release 0.1.0. This is a pre-release, and there is no download yet. See the [roadmap](roadmap.md). When the search code lands, a folder map goes here and in `AGENTS.md`.
