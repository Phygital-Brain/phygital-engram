# Connect your AI app

Once Phygital Engram works in your terminal, connect it to the AI app you use, so the app can search your notes for you.

> [!IMPORTANT]
> Version 0.2.0. The computer version worked in Claude Code, loaded from a config file, and Claude Code also worked with the server version over HTTP. Every other app and install route below is untested. Those steps are written from each app's documentation. If one fails, please [open an issue](https://github.com/Phygital-Brain/phygital-engram/issues/new?template=bug_report.yml).

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

MCP is a plug for AI apps. Phygital Engram has two ways to plug in:

- **On your computer** (`mcp/server.py`). Your app starts it when needed. It talks to the app directly and nothing goes through the internet. Use this for Claude Code, Claude Desktop, Codex and other apps on the same computer as your notes.
- **On a server** (`mcp/serve.py`). It runs all day at an address like `https://notes.example.com/mcp`, behind a passphrase login. Use this for your phone, the Claude website and ChatGPT, and from any computer. See [setup-own-server.md](setup-own-server.md).

Both give your AI the same four read-only tools.

You need:

1. Phygital Engram installed and an index built, as in [setup-computer.md](setup-computer.md).
2. The full path to the program folder. In the steps below it is written as `/path/to/phygital-engram`.
3. Your notes folder and your data folder. They are set with `ENGRAM_VAULT` and `ENGRAM_DATA`. The data folder must be outside your notes.

## Claude Code

The plugin route is one line from your terminal. Change `$HOME/Notes` to your notes folder:

```bash
claude plugin marketplace add Phygital-Brain/phygital-engram && claude plugin install phygital-engram@phygital-engram --config notes_folder="$HOME/Notes"
```

Or inside Claude Code, type this, and Claude Code asks you for the notes folder:

```
/plugin install phygital-engram --marketplace Phygital-Brain/phygital-engram
```

The plugin starts the connector. The connector builds the index when it starts and updates it every 10 minutes. The index goes in `~/.phygital-engram` unless you pass `--config data_folder=...`, and it must be outside your notes. To change the notes folder later, run `/plugin configure phygital-engram@phygital-engram` in Claude Code. We tested the install from a local copy and a search through Claude Code. The install straight from GitHub has not been tried.

The terminal installer does the same for Claude Code, and prints the lines for other apps if it does not find Claude Code. On a Mac or Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/Phygital-Brain/phygital-engram/main/install.sh | sh -s -- "$HOME/Notes"
```

With npm, if you have Node.js (`npx` fetches the newest version each time you start Claude Code):

```bash
claude mcp add phygital-engram --env ENGRAM_VAULT="$HOME/Notes" --env ENGRAM_DATA="$HOME/.phygital-engram/data" -- npx -y @phygital-brain/engram
```

The manual route, if you downloaded the files yourself:

```bash
claude mcp add phygital-engram --env ENGRAM_VAULT=/path/to/notes --env ENGRAM_DATA=/path/to/index -- python3 /path/to/phygital-engram/mcp/server.py
```

You should see `phygital-engram` when you run:

```bash
claude mcp list
```

To use your own server instead, from any computer:

```bash
claude mcp add --transport http phygital-engram https://notes.example.com/mcp
```

Then run `/mcp` inside Claude Code to log in with your passphrase.

## Claude Desktop

The one-click extension is the easy way: [claude-desktop-extension.md](claude-desktop-extension.md). To use your own server instead, add it as a custom connector under **Settings, Connectors**, as in the Claude website steps below.

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

These apps reach your notes through the server version, so Phygital Engram has to run on a server you own: see [setup-own-server.md](setup-own-server.md). Then:

1. Open the Claude website, go to **Settings, Connectors, Add custom connector**.
2. Give it a name, like Phygital Engram, and paste your address: `https://notes.example.com/mcp`.
3. Claude opens a page on your server. Type your passphrase and tap **Allow**.
4. Start a chat and switch the connector on. Connectors you add on the website also appear in the phone app.

You should see Claude call `search_notes` when you ask about your notes. Not tested with this repository's server. The author's own setup, which is separate, works this way from a phone.

## ChatGPT

ChatGPT can use remote MCP servers, so it also needs the server version: [setup-own-server.md](setup-own-server.md). Add your address `https://notes.example.com/mcp` as a custom connector in ChatGPT's connector settings and log in with your passphrase when it asks. The menu names change often, so follow ChatGPT's current help for custom MCP connectors. Not tested.

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
| Claude Code connected to the server version over HTTP, with a key from the login flow, on the sample notes, 2026-10-25 | Worked. It called `search_notes` and answered correctly |
| 11 automated tests of the server version | Pass |
| The Claude Code plugin loaded from a folder (`claude --plugin-dir`), 2026-10-25; `claude plugin validate` passes | Worked. Claude Code started the connector and `search_notes` found the schedule |
| The login page in a real browser, on a desktop and a phone-sized screen, 2026-10-25 | Worked. A wrong passphrase showed "That passphrase is not right", the right one sent the browser back to the app, and the page fits a phone screen |
| The plugin installed from the marketplace, and the `claude mcp add` route | Not tested |
| Your phone, the Claude website and ChatGPT with this repository's server | Not tested |
| Claude Desktop, Codex, Cursor, VS Code, Gemini CLI | Not tested |
