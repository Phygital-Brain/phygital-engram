# Limits

For when you want to know what Phygital Engram cannot do, or does only to a point. At the end you know what to expect before you start.

## What it does not do

| Limit | Why | What to do |
|---|---|---|
| It finds notes, it does not answer | It is a search. Your agent reads the result and writes the answer | Ask your agent. It reads the short list and answers |
| No search by meaning | It matches words, word roots, exact strings and signals like folder and date. Different words for the same idea can be missed | Turn on [cards](cards.md), or ask in two ways. A try with meaning search was too slow: see [benchmarks](benchmarks.md) |
| Markdown only | Only `.md` files are read | Export other files to Markdown first. PDFs, images and Word files are not searched |
| English-tuned word roots | "dashes" finds "dash" in English. Other languages match whole words and exact strings, but roots are not tuned | Use exact words in other languages, or add cards |
| No sync, no phone app | It runs on one computer against one folder | Keep your notes in a cloud drive. A server version for phones is wanted: see the [roadmap](roadmap.md) |
| The AI connector is untested in AI apps | It was only run over stdio against the sample notes. It runs on your computer, so ChatGPT and the Claude website and phone app cannot use it | Use the command line and the local page, or try the connector and report what happens: see [Connect your AI](connect-your-ai.md) |
| Reads only | It never edits notes | You or your agent change notes with your usual tools |

## Size and speed

| Thing | Limit |
|---|---|
| A question | Cut to 500 characters and 20 words |
| Results per search | At most 50, 10 by default |
| Sections per note in one list | At most 2 |
| A single note | Over 2 MB is skipped |
| Notes | Tested to 500,000 notes in a copy, which answered in 0.23 seconds. Tuned on about 5,000 |
| Time to build the index | About 15 seconds for roughly 5,000 notes. Longer for more |

## Things it will not index

- Hidden folders such as `.obsidian`, `.git`, `.claude`, `.trash`.
- Anything listed in your `.claudeignore` file.
- Notes with `engram: skip` near the top.
- Password and key files (`.env`, `tokens.json`, `credentials.json` and the like). They are never read.
- Notes with status `superseded`, `deprecated` or `replaced`, or past their `valid_until` date. They are hidden from results.

## Tuned on one person's notes

The folder weights in the working version fit one folder layout. On a different layout the ranking still works, but results get better once you set your own folder levels: see [settings](settings.md). Defaults for other layouts are not ready yet.

More in the [FAQ](faq.md) and the [roadmap](roadmap.md).
