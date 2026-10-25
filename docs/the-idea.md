# The idea behind it

Why a plain search can work better than a bigger setup, in four ideas.

<details>
<summary><b>Table of contents</b></summary>

- [The problem](#the-problem)
- [The fix](#the-fix)
- [Idea 1: date everything](#idea-1-date-everything)
- [Idea 2: your notes are the intake](#idea-2-your-notes-are-the-intake)
- [Idea 3: write for the question](#idea-3-write-for-the-question)
- [Idea 4: plain search is enough](#idea-4-plain-search-is-enough)
- [Keep it fresh](#keep-it-fresh)
- [What the name means](#what-the-name-means)

</details>

## The problem

A chat with an AI ends, and what you told it goes with it. Notes fix that. But once you have thousands of them, your agent cannot read them all.

The obvious fix is to paste everything into the AI's window. That has two problems.

- **The AI treats everything it reads as equally true.** An old price and a new price look the same to it. It has no sense of which note is current.
- **More text makes answers worse.** The AI gets slower, costs more, and starts missing things buried in the middle. People call this "context rot".

## The fix

Keep your notes outside the AI. When you ask a question, search first. Give the AI only the best few matches. It reads a short list instead of a whole folder.

A search like this takes milliseconds, so it adds no wait. Phygital Engram is that search, built for notes.

## Idea 1: date everything

Every note has a date. Newer notes count more, and old ones fade. In Phygital Engram the boost halves every 180 days. Rule notes and context notes are the exception: they never fade, because a rule written a year ago is still the rule.

This is what keeps the old price from beating the new one. See [search-ranking.md](search-ranking.md) for the exact numbers.

## Idea 2: your notes are the intake

A search is only as good as the notes you save. The habit of saving things as dated, named notes with clear headings matters more than the search itself.

Phygital Engram reads the notes you already have. It does not fetch your email or your chats. If you want an email thread or an AI chat to be findable, save it as a Markdown note in your folder. [Phygital Brain](https://github.com/Phygital-Brain/phygital-brain) sets up that habit for you: it builds the folders and keeps each note's date, status and tags in order. See [with-phygital-brain.md](with-phygital-brain.md).

## Idea 3: write for the question

People rarely search with the same words they wrote the note in. So each section can get a short card, written once by an AI with your own key. A card holds:

- a summary, in different words than the note
- the question someone would type to find it
- exact facts: an error message, a command that worked, the reason behind a decision

Cards are optional. Search works without them, and they help most when your question and the note use different words. See [cards.md](cards.md).

## Idea 4: plain search is enough

Phygital Engram matches words. It is the same kind of search that has worked since the 1990s (it is called BM25). On top of that it adds the date, the folder a note lives in, and its status.

We also tried search by meaning, which turns text into numbers and compares them. In our test it was about 45 times slower and only a little better, so we left it out. The numbers are in [benchmarks.md](benchmarks.md). On a personal pile of notes, a simple search that knows about dates and folders does the job.

## Keep it fresh

Things drift. Notes move, folders change, a setting breaks without a sound. So Phygital Engram has a health check that says if the index is out of date, if anything private slipped in, and if searches have become slow. Run it now and then.

## What the name means

An engram is a memory trace, the mark a memory leaves in the brain. The name fits because the tool finds what your notes remember. "Phygital" ties it to Phygital Brain. It is not related to other projects called Engram.

## What next

Back to the [README](../README.md), or try it in [getting-started.md](getting-started.md).
