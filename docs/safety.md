# Safety

For anyone who wants to know what Phygital Engram can do to their notes before using it. At the end you know what it promises, what it cannot promise, and what to do yourself.

![A picture of the ownership promise: your notes stay in your folder, Phygital Engram only reads them, and its own files live somewhere else.](images/ownership.png)

## The risks in plain words

Your notes may hold things you would not want shared: client names, tax numbers, a password pasted by mistake. A search tool reads all of them. So there are three questions. Can the tool change your notes? Can it leak them? Can someone use it to push bad instructions at your AI agent?

## What it does about it

- **It only reads.** It never writes, moves, renames or deletes a note. Its own files (the index) live in a separate folder. If you point that folder inside your notes, the program refuses to start.
- **It blanks secrets.** Lines such as `SECRET=...`, `TOKEN=...`, `PASSWORD=...`, API keys and private keys become `[REDACTED]` before anything is stored. They never reach search results, or an AI service if you use [note cards](cards.md).
- **It blanks labelled numbers.** Tax IDs, social security numbers, IBANs and card numbers that carry a label are blanked in every note, not only in private folders.
- **It never reads password files.** Files such as `.env`, key files, `tokens.json` and `credentials.json` (in any capital letters) are not read or indexed.
- **It can lock folders.** See [Private folders](#private-folders).
- **It labels what it returns.** Results are marked as note content, information only, never instructions.
- **It runs on your computer.** Searching makes no network calls. See [Privacy](privacy.md).
- **It skips what you tell it to.** These are not indexed: a note with `engram: skip` near the top, hidden folders, files listed in `.claudeignore`, and files over 2 MB.
- **It stops on a broken copy.** If more than a fifth of your notes vanish at once, it assumes the folder is half copied and keeps the old index.

## Private folders

A private folder can be found but not read in search. A search shows the file and heading, not the text. To open the text, you ask for it by its number on purpose. An AI agent should do that only when you asked.

Every word of your question must match, and at most two results are shown. This stops unrelated questions from showing private notes by accident. Private text is never sent to an AI service for note cards. You choose the private folders in [Settings](settings.md).

## What you should do

1. **Keep a backup of your notes.** Phygital Engram never changes them, but your computer might.
2. **Keep secrets out of notes.** Put API keys in the service's own settings, or in an `.env` file that is not synced. The blanking above is a safety net.
3. **Start with a copy.** Try it on a copy of your folder first.
4. **Mark private folders** before you connect an AI agent.
5. **Read your AI app's privacy settings.** That app decides what happens to a result.
6. **Set the key for note cards in the settings,** never in a note.

## What it does not protect against

> [!WARNING]
> No outside party has audited Phygital Engram. These are known limits, not a full list.

- **Bad text inside a note.** A note can hold text that tries to steer an AI agent, such as "ignore your rules and...". The label "information, never instructions" helps, but it does not block this. Take care with notes from other people, such as pasted emails or web pages.
- **Secrets in odd formats.** The blanking looks for known patterns and labels. A password pasted as a bare word in a sentence is not caught.
- **What your AI app does next.** Once an agent has a result, the app decides what to do with it, including where to send it.
- **Other people on your computer.** Anyone who can open your files can read the index and the notes. Use your computer's own protection.
- **Notes you did not mean to put there.** It indexes what is in the folder and cannot tell what is private. Mark those folders.

## If something goes wrong

Delete the index folder (`ENGRAM_DATA`). That removes everything Phygital Engram stored, and your notes stay as they are. You can rebuild it afterwards. See [Privacy](privacy.md#deleting-everything).

## The server version

If you run the server version (`mcp/serve.py`), the notes sit on a server you run, and your AI apps reach it over HTTPS. Every request needs a login key, which you get by typing your passphrase on a page of your own server. The server stores only `oauth.json` (the apps that logged in, and fingerprints of their keys) and the index. It never opens a private result, the same as the computer version. It is not tested on a real server and nobody has audited it.

The full list of what it defends against, and what it does not, is in the [threat model](threat-model.md). Setup is in [setup-own-server.md](setup-own-server.md).

## Found a security problem?

Please don't open a public issue. Use the private report. The steps are in [SECURITY.md](../SECURITY.md).
