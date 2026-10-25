# Note cards

Note cards are optional summaries an AI writes for each section of your notes. This page says what they cost and what leaves your computer if you turn them on.

> [!IMPORTANT]
> Cards are off until you give Phygital Engram your own AI key. With no key, nothing is sent anywhere and search works fully. The rest of this page is about what happens after you turn cards on.

<details>
<summary><b>Table of contents</b></summary>

- [What a card is](#what-a-card-is)
- [Why cards help](#why-cards-help)
- [What leaves your computer](#what-leaves-your-computer)
- [What it costs](#what-it-costs)
- [Turn cards on](#turn-cards-on)
- [Turn cards off](#turn-cards-off)
- [How cards stay honest](#how-cards-stay-honest)

</details>

## What a card is

A card is a short helper text that an AI model writes once for one section of one note. It is stored in your index beside the section and searched together with it. Your notes are not changed, so you never see cards in them.

Here is a made-up example. The section is a meeting note under the heading `Picture-Book > Cover > Due dates`. Its card could say:

| Part | Example |
|---|---|
| Context | From the Picture-Book project: when the cover art is due |
| Summary | Marta moved the cover deadline to the 15th. Final files go to the printer on the 22nd |
| Questions people might ask | When is the cover due? Who moved the deadline? When do files go to print? |
| Exact facts | Cover due the 15th. Files to printer on the 22nd |

## Why cards help

Search matches words. Say you ask *when does the artwork have to be ready?* and the note says "cover due on the 15th". The words do not overlap. The card holds "when is the cover due?", so the section is found.

In version 0.1.1, cards are the main help for questions that use different words than the note. [Limits](limits.md) explains why there is no search by meaning.

## What leaves your computer

If you turn cards on, this goes out for each section that needs a card:

- The text of that section (secrets already blanked), its heading path, its note title and the first section of the same note. These go to your AI provider. That is Anthropic's API, using the model `claude-haiku-5-5`. For a saved AI chat, the first 16,000 characters go.
- The card comes back and is stored in your index.

These never leave:

- Private folders.
- Password files, key files and anything blanked as a secret.
- Your questions. Cards are made from notes, not from what you ask.

To keep something from being sent, put `engram: skip` near the top of that note, or list the folder in `exclude_paths`. See [settings](settings.md) and [privacy](privacy.md).

## What it costs

You pay your AI provider directly. Phygital Engram adds nothing.

| When | What to expect |
|---|---|
| First time | In the author's case, about 4,800 notes cost about $6 in all. Cards are made in rounds, most important folders first |
| After that | Only new or changed sections get a card, so a few cents a month |
| Deleting the index | Cards live inside the index file. Delete the file and you pay again. A rebuild (not a delete) keeps them |

To see a price first, run the estimate. It makes no card and sends nothing.

```bash
python3 engram.py cards --estimate
```

You should see a line with how many sections need a card and about how many tokens that is.

## Turn cards on

1. Make an API key in your AI provider's console. Name it something like `phygital-engram` so you can find it later.
2. Put the key in the environment, or in a `.env` file next to the program. Never put it in a note or in `config.json`.

```bash
export ANTHROPIC_API_KEY="paste-your-key-here"
```

3. Run the estimate, then make a small batch first.

```bash
python3 engram.py cards --limit 50
```

You should see how many cards were made, how many failed, and how many sections still need one.

4. Check that search still looks right. When you are happy, run it again without `--limit`.

## Turn cards off

- To stop making new cards, remove the key from the environment or the `.env` file. Search keeps working with the cards you already have.
- To remove the cards you have, delete the index file in your data folder. It rebuilds from your notes, without cards.
- To never use them, leave the key out. Nothing is ever sent.

## How cards stay honest

An AI writes the card, so it can be wrong. Two rules limit the harm:

- A question or fact is kept only if it shares at least one real word with the section. Made-up ones are dropped.
- Cards add to a section's text for search. They never replace it. A result always shows the real note, heading and date, never the card alone.

If a card leads you to the wrong note, report it: see [troubleshooting](troubleshooting.md).
