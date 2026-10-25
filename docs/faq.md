# FAQ

For people who have never used a terminal. At the end you have an answer, or you know where to ask. If your question is not here, ask in [Help and feedback](../README.md#help-and-feedback) and we will add it.

## The basics

<details><summary><b>What is Phygital Engram?</b></summary>

It is a fast, private search for a folder of Markdown notes. Ask "What did Marta say about the Penguin Kids cover?" and it finds the note and the section that answers. It also shows the note, heading and date. See [How it works](how-it-works.md).

</details>

<details><summary><b>Is it free?</b></summary>

Yes. It is open source under the Apache-2.0 license, so you can use it, change it and share it. Searching costs nothing. [Note cards](cards.md) are optional and use your own AI account.

</details>

<details><summary><b>Do I need to code?</b></summary>

No. You copy a few commands into a terminal. [Getting started](getting-started.md) shows each one and what you should see. If you can follow a recipe, you can do it.

</details>

<details><summary><b>What does "Engram" mean here?</b></summary>

An engram is a stored memory trace. The name fits because the tool finds what your notes remember. "Phygital" ties it to Phygital Brain. More in [The idea behind it](the-idea.md).

</details>

<details><summary><b>How is this different from my agent reading the folder itself?</b></summary>

Reading a big folder is slow and costs a lot. In a test on the author's notes, a plain word search for ten questions matched about 104 notes. That is roughly 237,000 tokens of text, more than an AI can read at once. Phygital Engram returned about 1,100 tokens per question, with the source on each result. Numbers and limits are in [Benchmarks](benchmarks.md).

</details>

<details><summary><b>How fast is it?</b></summary>

On the author's notes (about 4,800), a search took 9 to 37 milliseconds on a server and about 11 milliseconds on a laptop. A test copy of 500,000 notes still answered in 0.23 seconds. We measured this on 2026-10-25, before tuning, on one person's notes. Yours will differ. See [Benchmarks](benchmarks.md).

</details>

<details><summary><b>Is it an AI that answers my questions?</b></summary>

No. It finds notes. Your AI agent reads what it finds and writes the answer. See [Limits](limits.md).

</details>

<details><summary><b>How is it different from other projects called Engram?</b></summary>

It is not related to them, and not made by or affiliated with them. Several AI memory projects use the name. Phygital Engram only searches a folder of Markdown notes you already keep. It does not store memories for you or run a database of facts.

</details>

<details><summary><b>Does it work with Phygital Brain?</b></summary>

Yes, and it was made to. Phygital Brain keeps your notes in a tidy folder with rules for your agent. Phygital Engram makes finding things in that folder fast. Neither needs the other. See [With Phygital Brain](with-phygital-brain.md).

</details>

<details><summary><b>Is meaning search coming?</b></summary>

Not as we tried it. Meaning search needs an AI model that turns words into numbers. We tried one running on the same computer. It helped a little and made each search about 45 times slower, so we chose speed. Optional [note cards](cards.md) cover most of the gap. A tiny built-in model may be tried later. See the [roadmap](roadmap.md). Nothing there is promised.

</details>

## Your notes and safety

<details><summary><b>Does it send my notes anywhere?</b></summary>

No. Searching runs on your computer and makes no network calls. The one exception is optional. If you turn on note cards, the text of the sections that need a card goes to the AI service whose key you set. Secrets are blanked first, and private folders are never sent. See [Privacy](privacy.md).

</details>

<details><summary><b>Can it change or delete my notes?</b></summary>

No. It only reads. It never writes, moves, renames or deletes a note, so there is nothing to undo. Its own files live in a separate folder, and it refuses to start if that folder is inside your notes. You can delete the index it builds at any time and rebuild it in seconds. See [Safety](safety.md).

</details>

<details><summary><b>What happens to passwords, keys and tax numbers in my notes?</b></summary>

Lines that look like secrets, such as `PASSWORD=...`, `TOKEN=...`, API keys and private keys, become `[REDACTED]` before anything is stored. Numbers labelled as a tax ID, an IBAN or a card number are blanked too. Files such as `.env`, key files and `credentials.json` are never read. Folders you mark as private are locked: a search shows the file and heading, and the text opens only when you ask. See [Safety](safety.md).

</details>

<details><summary><b>Can my AI be tricked by something written in a note?</b></summary>

It can. Results are labelled as note content, information only, never instructions. That helps, but a note can still hold text that tries to steer an AI. Be careful with notes from other people. See [What it does not protect against](safety.md#what-it-does-not-protect-against).

</details>

<details><summary><b>Is it audited or certified?</b></summary>

No. No outside party has audited it. [Safety](safety.md) lists the rules it follows, and the code is open for anyone to check.

</details>

<details><summary><b>Does it track me?</b></summary>

No. There is no account, no telemetry and no tracking. The local web page loads no outside images and cannot be shown inside other sites.

</details>

## Compatibility

<details><summary><b>Which AI apps work with it?</b></summary>

The repository has an MCP connector (`mcp/server.py`) with four read-only tools. It worked in Claude Code on the sample notes. We have not tested it in Claude Desktop, Codex, Cursor, VS Code or Gemini CLI, so those are not listed as working yet. ChatGPT and the Claude website and phone app are supported through the server version (`mcp/serve.py`), set up with [Setup on your own server](setup-own-server.md). It is not tested on those apps with this repository yet. See [Connect your AI](connect-your-ai.md) and [Tools](tools.md). You can also run it in the terminal or on the local web page.

</details>

<details><summary><b>What does "MCP" mean?</b></summary>

It is short for Model Context Protocol. Think of it as a plug that lets AI apps use a tool. Phygital Engram includes a connector built on it. The [glossary](glossary.md) explains the other words you will see.

</details>

<details><summary><b>Which notes can it read?</b></summary>

Markdown files ending in `.md`, in any subfolder. It does not read PDFs, images, Word files or spreadsheets. It skips files over 2 MB and hidden folders such as `.obsidian` and `.git`.

</details>

<details><summary><b>Does it work with Obsidian?</b></summary>

Yes. It reads the same files Obsidian shows. It needs no Obsidian plugin and does not touch the `.obsidian` folder.

</details>

<details><summary><b>Does it work with Baalda, Logseq or plain files?</b></summary>

It works on any folder of `.md` files. We tested it on one folder, the author's. Other apps that store notes as Markdown should work the same way, but we have not tested them.

</details>

<details><summary><b>Which computers does it run on?</b></summary>

We tested a Mac and a Linux server. We have not tested Windows or Linux desktops. See [What we tested](setup-computer.md#what-we-tested).

</details>

<details><summary><b>Which languages does it support?</b></summary>

The docs are in English only for now. Search matches words in any language. Only the word-root matching ("dashes" finds "dash") is tuned for English, so notes in other languages are found by exact words. See [Limits](limits.md).

</details>

<details><summary><b>Can I use it from my phone?</b></summary>

Yes, through the server version. Phone apps reach a connector over HTTPS, so the computer version does not reach your phone. The server version runs on a server you own, behind a passphrase login. Set it up with [Setup on your own server](setup-own-server.md). It is not tested on a phone with this repository yet. The author uses the working version from a phone through their own server. See the [roadmap](roadmap.md).

</details>

## Running it

<details><summary><b>How long does the first index take?</b></summary>

From seconds to a minute for a few thousand notes. About 15 seconds for roughly 5,000 notes on a laptop. After that it reads only changed notes.

</details>

<details><summary><b>How do I keep the index fresh?</b></summary>

Run the `ingest` command again, or schedule it. It reads only what changed. See [Set up on your computer](setup-computer.md#6-keep-it-fresh).

</details>

<details><summary><b>Where are its files kept?</b></summary>

In the folder you set as `ENGRAM_DATA`, outside your notes. See [Privacy](privacy.md#whats-kept-and-where).

</details>

<details><summary><b>How do I update it?</b></summary>

Download the new version and replace the program folder. Your settings and index stay. See [Updates](updates.md).

</details>

<details><summary><b>How do I remove it?</b></summary>

Delete the program folder and the `ENGRAM_DATA` folder. Your notes stay as they are. See [Privacy](privacy.md#deleting-everything).

</details>

<details><summary><b>Why is a result I expected not first?</b></summary>

Order comes from several signals: your words, folders, status and how new a note is. Each result has a line giving its reason. See [How results are ranked](search-ranking.md) and [Troubleshooting](troubleshooting.md#the-wrong-note-comes-first).

</details>

<details><summary><b>Can I hide a note from search?</b></summary>

Yes. Use any one of these:

- Put the line `engram: skip` near the top of the note.
- Set its status to `superseded`, `deprecated` or `replaced`.
- Give it a `valid_until` date that has passed.

You can also skip whole folders in the settings. See [Settings](settings.md).

</details>

<details><summary><b>Can I teach it which folders matter more?</b></summary>

Yes. Folder weights are in `config.json`. Core folders count more and archive folders count less. The defaults are in [How results are ranked](search-ranking.md), and the options are in [Settings](settings.md).

</details>

## Cost and cards

<details><summary><b>What are note cards?</b></summary>

A card is a short summary, a few questions someone might ask, and a few exact facts. An AI model writes one for each section of a note, once. Cards help when your question uses different words than the note. See [Note cards](cards.md).

</details>

<details><summary><b>Do I need cards?</b></summary>

No. Search works without them. They only help when your question shares no words with the note.

</details>

<details><summary><b>What do cards cost?</b></summary>

They use your own AI account. For about 4,800 notes the first round cost about 6 US dollars. After that you pay only for new and changed sections, a few cents. Check your own account's prices first. An estimate command shows the size before you start.

</details>

<details><summary><b>Does a card send my whole vault to an AI?</b></summary>

Only if you turn cards on, and then only the sections that need a card. Secrets are blanked first. Private folders are never sent. See [Privacy](privacy.md).

</details>

## Still have a question?

- Search this repository's [issues](https://github.com/Phygital-Brain/phygital-engram/issues) first.
- Ask in the **Question** form under [Help and feedback](../README.md#help-and-feedback).
- A security problem is not a public question: use the private report in [SECURITY.md](../SECURITY.md).
- To change the docs or the code, see [CONTRIBUTING.md](../CONTRIBUTING.md).
