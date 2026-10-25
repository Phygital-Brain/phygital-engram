# Connect your AI app

For when Phygital Engram works in your terminal and you want your AI app to search your notes for you. You will leave with one app connected and a first question answered.

> [!IMPORTANT]
> Pre-release. The connector worked in Claude Code, loaded from a config file. Every other app and install route below is untested, and there is no release to download. Those steps are written from each app's documentation. If one fails, please [open an issue](https://github.com/Phygital-Brain/phygital-engram/issues/new?template=bug_report.yml).

<details>
<summary><b>Table of contents</b></summary>

- [Before you start](#before-you-start)
- [Claude Code](#claude-code)
- [Claude Desktop](#claude-desktop)
- [Claude website and phone app](#claude-website-and-phone-app)
- [ChatGPT](#chatgpt)
- [Codex](#codex)
- [Cursor, VS Code and Gemini CLI](#cursor-vs-code-and-gemini-cli)
- [Other MCP apps](#other-mcp-apps)
- [Check it works](#check-it-works)
- [What we tested](#what-we-tested)

</details>

## Before you start

MCP is a plug for AI apps. Phygital Engram includes one small connector, `mcp/server.py`. Your app starts it when needed. It runs on your computer and talks to the app directly. Nothing goes through the internet.

You need:

1. Phygital Engram installed and an index built, as in [setup-computer.md](setup-computer.md).
2. The full path to the program folder. In the steps below it is written as `/path/to/phygital-engram`.
3. Your notes folder and your data folder. They are set with `ENGRAM_VAULT` and `ENGRAM_DATA`. The data folder must be outside your notes.

## Claude Code

The plugin route, once the repository is public:

```bash
claude plugin marketplace add Phygital-Brain/phygital-engram
```

```bash
claude plugin install phygital-engram@phygital-engram
```

The plugin starts the connector. It reads `ENGRAM_VAULT` and `ENGRAM_DATA` from your environment, so set them in your shell profile.

The manual route works today:

```bash
claude mcp add phygital-engram --env ENGRAM_VAULT=/path/to/notes --env ENGRAM_DATA=/path/to/index -- python3 /path/to/phygital-engram/mcp/server.py
```

You should see `phygital-engram` when you run:

```bash
claude mcp list
```

## Claude Desktop

The one-click extension is the easy way: [claude-desktop-extension.md](claude-desktop-extension.md).

To set it up by hand, open **Settings, Developer, Edit Config** and add this to `claude_desktop_config.json`, then restart the app:

```json
{
  "mcpServers": {
    "phygital-engram": {
      "command": "python3",
      "args": ["/path/to/phygital-engram/mcp/server.py"],
      "env": {
        "ENGRAM_VAULT": "/path/to/notes",
        "ENGRAM_DATA": "/path/to/index"
      }
    }
  }
}
```

## Claude website and phone app

These apps reach a connector over the internet, so Phygital Engram has to run on a server you own, over HTTPS, behind a login. Then it works on your phone too. The author runs the working version this way. That server version is not in this repository yet, and the connector here runs on your computer only. It is next on the [roadmap](roadmap.md).

## ChatGPT

Same as above: it works once Phygital Engram runs on a server you own. Not in this repository yet.

## Codex

```bash
codex mcp add phygital-engram --env ENGRAM_VAULT=/path/to/notes --env ENGRAM_DATA=/path/to/index -- python3 /path/to/phygital-engram/mcp/server.py
```

## Cursor, VS Code and Gemini CLI

These apps read a list of MCP servers from a settings file. Add one entry like the Claude Desktop snippet above: the command `python3`, the argument with the path to `mcp/server.py`, and the two environment settings. The file is `~/.cursor/mcp.json` for Cursor, `.vscode/mcp.json` for VS Code (which calls the list `servers`) and `~/.gemini/settings.json` for Gemini CLI. Not tested.

## Other MCP apps

Any app that starts MCP servers over stdio can use it. Give it the command `python3`, one argument (the path to `mcp/server.py`) and the two settings. See [settings.md](settings.md) for every setting.

## Check it works

Ask your AI app: *"Search my notes for the Picture-Book schedule and tell me where you found it."*

You should see it call `search_notes`, and then answer with a note name and a date. If it says it cannot find the tool, see [troubleshooting.md](troubleshooting.md). The tools are listed in [tools.md](tools.md).

## What we tested

| What | Result |
|---|---|
| The four tools, run over stdio against the real search on the 24-note sample, 2026-10-25 | Worked. A private result was found and refused when asked to open |
| 10 automated tests of the connector, with a stand-in search | Pass |
| Claude Code 2.1.310, loaded from a config file, asked to find the Picture-Book schedule, 2026-10-25 | Worked. It started the connector, called `search_notes` and `open_result`, and answered with the note and the right dates |
| The Claude Code plugin and the `claude mcp add` route | Not tested |
| Claude Desktop, Codex, Cursor, VS Code, Gemini CLI | Not tested |
