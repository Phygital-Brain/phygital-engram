# Examples

For when you are not sure what to ask. At the end you have a list of questions that work well.

The notes in these examples are made up: a picture book called *Penguin Kids*, a publisher contact named Marta, and a project folder called `Picture-Book`. Yours will have other names. The questions work the same way.

## How to ask

Ask the way you would ask a person who has read all your notes. Full questions work better than keyword lists. You can also type a few exact words, a version number, or a phrase in "quotes".

- *When is the cover for the penguin book due?*
- *What did we decide about the printer?*
- *"print-ready PDF"*

On the command line, type `python3 engram.py search "your question"`. Once an AI app is connected, the app asks for you. The repository has a connector for this, but it has not been tried inside AI apps yet. See [Connect your AI](connect-your-ai.md).

## Find a fact

Phygital Engram is best at questions about one fact in one note.

- *What is the deadline for the Penguin Kids cover?*
- *Which printer did we pick for the picture book?*
- *What did Marta say about the page count?*
- *Which version of the app is running on my server?*

Each result shows the note, the heading and the date, so you can check the answer yourself.

## Find a decision

Words like "decision" point the search at your decisions folder, if you have one. See [How results are ranked](search-ranking.md).

- *What did we decide about the print run?*
- *Why did we drop the hardback idea?*
- *Which decisions about Picture-Book are still open?*

## Find a person or a client

Words like "client" point the search at your people folder.

- *What did I last talk about with Marta?*
- *Which client was my biggest one in 2022?*
- *Who at the publisher handles rights?*

## Find what you did on a day

Words like "daily" point the search at your daily notes.

- *What did I do on the day we sent the first sketches?*
- *Show me my daily notes from the week of the book fair.*

Ask for what is around a result and you also get the sections before and after it, plus notes from the same day. On the command line that is `python3 engram.py around ID`.

## Find something you only half remember

You remember the idea but not the words. [Note cards](cards.md) help here. A card is a short summary and a few likely questions, written once for each section.

- *That note about charging for rush jobs.*
- *The thing about page bleed and the printer.*

> [!NOTE]
> Without cards, the search matches words, word roots and exact strings, not meaning. If your question shares no word with the note, the note may not come back. See [Limits](limits.md).

## Find the exact string

Put it in quotes, or type it. Versions, file paths, host names and IDs count extra when they match letter for letter.

- *"v2.4.1"*
- *"Picture-Book/outputs"*

## Let your agent search first

If you use Phygital Engram beside [Phygital Brain](with-phygital-brain.md), tell your agent once:

*Before you answer about my past work, projects or decisions, search my notes with Phygital Engram first, then open the best results.*

The agent then looks up notes instead of reading whole folders. [With Phygital Brain](with-phygital-brain.md) has the rule as written in the brain's rules file.

## Check that it is fair

- *Show me why this result came first.* Every result has a short "why" line: your words in the heading, the folder, how new it is.
- *Search again, words only.* The command line has `--plain`, which turns off the extras so you can see the difference.

## What next

- [Getting started](getting-started.md) if you have not built the index yet.
- [FAQ](faq.md) for short answers.
- [Troubleshooting](troubleshooting.md) if a search misses a note you know is there.
