# Privacy

For anyone asking where their notes go. At the end you know what leaves your computer, what is kept and where, and how to delete all of it.

> [!NOTE]
> Nothing collected. No account, no tracking.

## What leaves your computer

Nothing leaves it. Searching runs on your computer. Phygital Engram makes no network calls of its own and sends no usage numbers anywhere.

There is one optional exception. If you turn on [note cards](cards.md), the text of each section goes to the AI service whose key you set, so it can write a short card. Secrets are blanked before anything is sent, and sections from private folders are never sent. If you don't turn cards on, nothing is sent.

## Encryption at a glance

Phygital Engram does not encrypt your notes or its index. They are plain files on your disk, protected by your computer's login and disk encryption. If you need your notes locked, turn on your computer's disk encryption. A private folder (see [Safety](safety.md#private-folders)) hides text from search results, but it does not encrypt anything.

## What's kept and where

| What | Where | Who can read it |
|---|---|---|
| Your notes | The folder you set as `ENGRAM_VAULT` | You, and anyone with access to your computer. Never changed by Phygital Engram |
| The index: sections, headings, dates, search tables | `ENGRAM_DATA`, in a database file | Anyone with access to that folder. Secrets and labelled numbers are blanked in it |
| Note cards (optional) | `ENGRAM_DATA`, in the same database | Same. Kept by content, so a rebuild does not lose them |
| A count of which results you opened | `ENGRAM_DATA` | Same. Used to learn from real use after enough opens |
| Your API key for cards (optional) | An environment variable or a `.env` file in the program folder, which is never synced | You. Never written to a note or to the index |

Your questions are not stored. Only counts of which notes were shown and opened are kept, and they never leave your computer.

## What the AI app sees

Phygital Engram does not control your AI app. It returns a short list of results: the note path, the heading, a piece of text and a "why" line. The app may send that text to its AI service. This is why secrets are blanked first and private folders show no text.

Check your AI app's own privacy settings. See also [Safety](safety.md#what-you-should-do).

## The server version

If you run the server version (`mcp/serve.py`), the notes sit on a server you run, and your AI apps reach it over HTTPS. What travels: search results, from your server to your AI app, over HTTPS. What is stored on the server: `oauth.json` in `ENGRAM_DATA` (client information and key fingerprints, never a usable key) and the index. Your notes are mounted read-only. Nothing is sent to us.

The full list of what it defends against, and what it does not, is in the [threat model](threat-model.md). Setup is in [setup-own-server.md](setup-own-server.md).

## Logs

The program prints to your terminal and writes no log file. The health check reports problems in the terminal. If you run it as a scheduled task, your system's own log may keep what it printed.

## Deleting everything

1. Delete the folder you set as `ENGRAM_DATA`. This removes the index, the cards and the usage counts.
2. Delete the `phygital-engram` program folder.
3. If you set an API key for cards, remove it from your environment or `.env` file. You can also revoke it in your AI account.

Your notes are never touched. Deleting the index loses nothing, because the next `ingest` rebuilds it from your notes.
