# With Phygital Brain

How Phygital Engram fits beside Phygital Brain, and the rule to give your agent.

## How they fit

Phygital Brain builds a folder of notes and the rules your agent follows. Phygital Engram searches that folder. One makes the notes, the other finds them.

| | Phygital Brain | Phygital Engram |
|---|---|---|
| What it is | A second brain: folders, templates, rules, routines | A fast search over a notes folder |
| What it does with your notes | Your agent reads and writes them, with your approval | Only reads them |
| Needs the other? | No | No |

Phygital Brain works without search, and Phygital Engram works on any folder of Markdown notes. Used together, your agent looks things up instead of reading whole folders.

## Why it helps

A brain grows. After a few months it holds hundreds of notes: daily notes, decisions, people, projects. An agent that reads folder by folder wastes time and memory. With Phygital Engram it asks for the best few sections and opens only those. Each result names the note, heading and date, so the agent can say where an answer came from.

A Phygital Brain also gives the search what it looks for, and we checked it on the example brain from the Phygital Brain repository (2026-10-25, with an empty `CLAUDE.md` added):

- The top `CLAUDE.md` is there. The search needs it before it indexes, and it counts more in the ranking.
- Phygital Brain's `.claudeignore` lists `Memory/finances/`. The search skips everything listed there, and in our check a note in that folder never showed up. `Memory/finances/` is also private by default, so it is locked even without the ignore file.
- A brain's `Memory/decisions/` folder matches the `*/decisions/*` rule. Notes there never fade, and the word "decision" in a question points at them.
- Notes marked `done` or `archived`, and notes in an `archive` folder, count less.

One thing is not set up for you. `About/` is not boosted by default, so those notes count as normal notes. To lift them, add a rule for `About/*` to `path_weights` (and to `evergreen_paths` if they should never fade): see [Folder levels and hints](settings.md#folder-levels-and-hints). Try your own questions before and after, because a change can help one question and hurt another. In our small check on the example brain, giving `About/` extra weight pushed a note about services above the decision we were looking for. See [How results are ranked](search-ranking.md).

The matching guide inside Phygital Brain is [Fast search with Phygital Engram](https://github.com/Phygital-Brain/phygital-brain/blob/main/docs/search-with-phygital-engram.md).

## The rule for your agent

Add one line to your brain's main rules file (`CLAUDE.md`):

> Before answering about my past work, projects, decisions, people or notes, search with Phygital Engram first, then open the best results. If it finds nothing or is not available, read the files instead.

The second sentence matters. If Phygital Engram is not installed, is down, or finds nothing, your agent reads files as it always did. Nothing breaks.

> [!NOTE]
> The repository has a connector that lets your AI app use Phygital Engram directly, and it worked in Claude Code. It has not been tried in other apps yet. For a phone or the web there is a server version: see [Setup on your own server](setup-own-server.md). See [Connect your AI](connect-your-ai.md). In an app without it, the rule only helps an agent that can run terminal commands.

## The Brain Keeper does not depend on it

The Brain Keeper is the scheduled task that tidies your brain each work day. It reads your notes the normal way and never calls Phygital Engram. If you remove Phygital Engram, the Brain Keeper works as before.

## What stays separate

- Phygital Engram never writes to your brain. Your agent still asks before it creates, moves, renames or deletes a note.
- Its index lives outside your brain folder.
- You can delete the index at any time. Your brain is untouched.

## Setting it up

1. Set up a brain with Phygital Brain. See its [getting started](https://github.com/Phygital-Brain/phygital-brain/blob/main/docs/getting-started.md).
2. Install Phygital Engram: [Set up on your computer](setup-computer.md). Point `ENGRAM_VAULT` at your brain folder.
3. Build the index: [Getting started](getting-started.md).
4. Add the rule above to your brain's `CLAUDE.md`.

## What next

- [Examples](examples.md) for questions that work well.
- [FAQ](faq.md) for short answers.
