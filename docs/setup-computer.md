# Set up on your computer

For when you want to try Phygital Engram on your own notes, free, with nothing sent anywhere. About 10 minutes. At the end you can search your notes from the terminal.

> [!NOTE]
> The program files are added to this repository with the first release. These steps are for the working version. Command names may change before 0.1.0, and this page will change with them.

## Before you start

- **A folder of Markdown notes** on your computer. A copy is fine, and safer for a first try.
- **Python.** The working version runs on Python 3.14 (the server) and was tried on Python 3.15 (a Mac). Older versions are not tested. Check yours:

```bash
python3 --version
```

You should see `Python 3.14` or newer. If the command is not found, install Python from python.org and open a new terminal window.

- **Free space.** The index is small. For about 5,000 notes it was a few tens of megabytes.
- **Nothing else to install.** The search uses only what comes with Python, including the SQLite database.

## 1. Get the files

Download this repository as a zip from the green **Code** button on GitHub, then unzip it. If you use Git, run this instead:

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

The numbers come from the author's own notes and were taken before tuning. See [Benchmarks](benchmarks.md).
