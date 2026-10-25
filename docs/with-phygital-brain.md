# With Phygital Brain

For people who use [Phygital Brain](https://github.com/Phygital-Brain/phygital-brain) and want its notes found faster. At the end you know how the two fit together and what rule to give your agent.

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

The layout of a Phygital Brain also helps the search. Rules files (`CLAUDE.md`), the context pages and the decisions folder count more by default. Archive folders count less. See [How results are ranked](search-ranking.md).

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
