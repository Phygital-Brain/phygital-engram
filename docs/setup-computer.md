# Set up on your computer

Try Phygital Engram on your own notes, free, with nothing sent anywhere. It takes about 10 minutes, and you end up searching your notes from the terminal.

> [!NOTE]
> These steps match version 0.1.0, the first release. The search program (`engram.py`) is in this repository. Want it in one line instead? See [Install in one line](../README.md#install-in-one-line).

## Before you start

- **A folder of Markdown notes** on your computer. A copy is fine, and safer for a first try.
- **A file named `CLAUDE.md` at the top of that folder.** It can be empty. The search checks for it before it indexes, so it never builds an index from a half-copied folder. Phygital Brain makes this file for you. If your folder has none, create an empty one. Without it, indexing stops and nothing changes.
- **A second folder for the index, outside your notes.** It refuses to run if that folder is inside your notes.
- **Python.** It needs Python 3.11 or newer. The sample test gives the same result on Python 3.11, 3.13 and 3.15. The Mac that ships with Python 3.9 is too old: install a newer one from python.org. Check yours:

```bash
python3 --version
```

You should see `Python 3.11` or newer. If the command is not found, install Python from python.org and open a new terminal window.

- **Free space.** The index is small. For about 5,000 notes it was a few tens of megabytes.
- **Nothing else to install.** The search uses only what comes with Python, including the SQLite database.

## 1. Get the files

Download the latest release from the [releases page](https://github.com/Phygital-Brain/phygital-engram/releases) and unzip it, or use the green **Code** button on GitHub. If you use Git, run this instead:

```bash
git clone https://github.com/Phygital-Brain/phygital-engram.git
```

You should see a new `phygital-engram` folder.

## 2. Open a terminal in the folder

On a Mac, open **Terminal**. On Windows, open **PowerShell**. On Linux, open your terminal. Then go into the folder:

```bash
cd phygital-engram
```

## 3. Tell it where your notes are

On Mac and Linux:

```bash
export ENGRAM_VAULT="$HOME/Notes"
export ENGRAM_DATA="$HOME/.phygital-engram"
```

On Windows PowerShell:

```bash
$env:ENGRAM_VAULT = "$HOME\Notes"
$env:ENGRAM_DATA = "$HOME\.phygital-engram"
```

`ENGRAM_VAULT` is your notes folder. `ENGRAM_DATA` is where Phygital Engram keeps its own files. It must be outside your notes. If you point it inside, the program stops and tells you. See [Settings](settings.md).

## 4. Build the index

```bash
python3 engram.py ingest
```

You should see a line that says how many notes were indexed and how many seconds it took.

## 5. Check it works

```bash
python3 engram.py search "a word you know is in one of your notes"
```

You should see results with the note path, heading and a short piece of text. Then run this:

```bash
python3 engram.py health
```

You should see checks marked OK. If something is not OK, see [Troubleshooting](troubleshooting.md).

## 6. Keep it fresh

Run `ingest` again whenever you want the index to catch up. Only changed notes are read again, so it is fast. You can also set your computer to run it every few minutes.

## 7. Make it safer

- Leave your notes folder as it is. Phygital Engram never writes to it. See [Safety](safety.md).
- Mark private folders so their text stays locked. See [Settings](settings.md).
- Keep your API key out of your notes if you turn on [note cards](cards.md).

## Where things are

| What | Where |
|---|---|
| Your notes | The folder you set in `ENGRAM_VAULT`. Never changed |
| The index and its helper files | The folder you set in `ENGRAM_DATA` |
| The program | The `phygital-engram` folder you downloaded |
| Settings | `config.json` in the program folder, and the two settings above |

## Update

See [Updates](updates.md).

## Remove

Delete the `phygital-engram` folder and the folder you set in `ENGRAM_DATA`. Your notes are untouched. See [Privacy](privacy.md#deleting-everything).

## What we tested

| What | Result |
|---|---|
| macOS, Python 3.15, about 5,000 notes, 2026-10-25 | Works. Index in seconds, searches in about 11 ms |
| Linux server, Python 3.14, about 4,800 notes, 2026-10-25 | Works. Searches in 9 to 37 ms |
| Windows | Not tested |
| Linux on a desktop | Not tested |
| Python older than 3.14 | Not tested |

The numbers come from the author's own notes and were taken with the author's own settings. See [Benchmarks](benchmarks.md).
