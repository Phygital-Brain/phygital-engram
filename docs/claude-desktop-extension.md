# Claude Desktop extension

Install Phygital Engram in Claude Desktop with one click and no config file.

> [!IMPORTANT]
> Pre-release. The extension is built by a script and checked by a workflow when a release is published. No release exists yet, so there is no file to download. Nothing here has been tested inside Claude Desktop.

## What you need

- Claude Desktop, the latest version, on Mac, Windows or Linux.
- Python 3 on your computer.
- Phygital Engram's search, with an index built. The extension bundles it from version 0.1.0.

## Install

1. Download [phygital-engram.mcpb](https://github.com/Phygital-Brain/phygital-engram/releases/latest/download/phygital-engram.mcpb). It will work once the first release is published.
2. Open Claude Desktop, go to **Settings, Extensions**, and drag the file in.
3. Pick **Your notes folder** and **Folder for the index**, then **Install**. The index folder must be outside your notes folder.

## First use

Ask Claude: *"Search my notes for the Picture-Book schedule and tell me where you found it."* You should see it use `search_notes` and answer with a note name and a date.

## Change the settings

Open the extension in **Settings, Extensions** and change either folder.

## Where things are

Your notes stay where they are. The index sits in the folder you picked for it. The extension itself is kept by Claude Desktop.

## Update

Download the new `.mcpb` and drag it in over the old one. Your index and notes are not touched.

## Remove

Remove the extension in **Settings, Extensions**. Then delete the index folder if you like. Your notes are never changed.

## If it doesn't work

- **"Python not found".** Install Python 3 and restart Claude Desktop.
- **No results.** The index is empty. Build it once from the terminal: see [setup-computer.md](setup-computer.md).
- **It refuses to start.** The index folder is inside your notes folder. Pick a folder outside it.

## How it's built

`scripts/build_mcpb.py` packs the connector and the search into one `.mcpb` file. A workflow builds it for each published release and checks it with Anthropic's own validator. Nothing is built from unreleased code.
