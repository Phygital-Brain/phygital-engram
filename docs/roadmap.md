# Roadmap

Nothing here is promised or has a date.

This page shows where Phygital Engram may go. At the end you know what is wanted, what is only an idea, and what we have decided against.

## Wanted

In this order:

1. **Test the server version.** It is built (`mcp/serve.py`, see [Setup on your own server](setup-own-server.md)) and its 11 automated tests pass. Claude Code connected to it over HTTP. The login page also worked in a browser, on a desktop and a phone-sized screen. The Docker image builds on GitHub, but it is not tested with Compose and Caddy, on a real server, on a real phone, in the Claude website or in ChatGPT. Writing down what works comes first, before anything new.
2. **Test the connector in more AI apps.** The connector is built (see [Tools](tools.md)) and worked in Claude Code on the sample notes. Next is the Claude Code plugin route, Claude Desktop, Codex, Cursor, VS Code and Gemini CLI, and writing down what works.
3. **Test the Claude Desktop extension.** It ships with release 0.1.0 as `phygital-engram.mcpb` (see [Claude Desktop extension](claude-desktop-extension.md)). It has not been tried inside Claude Desktop yet.
4. **Sourced facts.** Return the single line that answers, with its note, heading and date, instead of a whole section. In a small test on the author's notes it cut the reading from about 3,100 to about 1,000 characters per question. It matches words only and needs more work.
5. **A small built-in meaning model.** A small model inside the program, with no separate AI server, to match meaning as well as words. Only if it stays fast, with almost no added time to a search.
6. **Windows and Linux checks.** Test on more systems and write down what works.
7. **More languages.** Docs and word-root matching for languages other than English.

Also wanted, no order: **package install**, one command instead of downloading the files, and **a small local web page** to search and check your index. It is planned and not in 0.1.0.

## Maybe

- **An updater.** Update by itself every week.

## Not planned

- **Cloud sync.** Your notes stay where they are. Use your own drive to sync them.
- **An AI that answers by itself.** Phygital Engram finds. Your agent answers.
- **Meaning search through a separate AI server.** We tried it with a model on the same computer. It helped a little and made each search about 45 times slower. Speed matters more to us.
- **Editing your notes.** It only reads, and it will stay that way.

## How to ask for something

Open a **Feature request** under [Help and feedback](../README.md#help-and-feedback). Say what you were trying to do. If you want to build it yourself, see [CONTRIBUTING.md](../CONTRIBUTING.md).
