# Troubleshooting

## If something goes wrong

For when Phygital Engram does not do what you expected. Each problem below says what you see, why it happens and what to do. At the end it works, or you know how to report it.

Start with the check that finds most problems:

```bash
python3 engram.py health
```

You should see a list of checks. Each one that is not marked OK says what to do.

## Install

### "python3: command not found"

**What you see:** the terminal says the command was not found.
**Why:** Python is not installed, or the terminal was open before you installed it.
**Fix:** install Python from python.org, close the terminal, open a new one, and run `python3 --version`.

### "No such file" when you run the command

**What you see:** `can't open file ... engram.py`.
**Why:** the terminal is not in the program folder.
**Fix:** go into the folder with `cd phygital-engram`, then run the command again.

### "Refusing to run: db path is inside the vault"

**What you see:** the program stops and names the path.
**Why:** `ENGRAM_DATA` points inside your notes folder. Phygital Engram never puts its own files in your notes.
**Fix:** set `ENGRAM_DATA` to a folder outside your notes, for example `~/.phygital-engram`. See [Settings](settings.md).

### "Vault not found or not synced"

**What you see:** `Vault not found or not synced. Nothing changed.`
**Why:** the notes folder does not exist, or it has no `CLAUDE.md` file at the top. The search needs that file: it checks that the folder is your notes and fully copied. Phygital Brain folders have one.
**Fix:** check the path in `ENGRAM_VAULT`. If your folder has no `CLAUDE.md`, create an empty one at the top, then build the index again.

## The index

### The first index is slow

**Why:** the first run reads every note. About 5,000 notes take seconds to a minute. Many very large files take longer.
**Fix:** wait. Later runs read only what changed.

### "More than a fifth of the notes vanished, refusing"

**What you see:** the update stops and says it refuses.
**Why:** if a fifth of your notes seem gone at once, the program assumes the copy is half done. It keeps the old index.
**Fix:** check that your notes folder is complete and synced. If you did delete that many, rebuild:

```bash
python3 engram.py ingest --rebuild
```

You should see `REBUILT.` at the start of the line.

### A note is missing from search

**Why:** it may be skipped on purpose. These are not read: hidden folders (`.obsidian`, `.git`), files over 2 MB, files listed in `.claudeignore`, and notes with an `engram: skip` line near the top.
**Fix:** run `python3 engram.py stats` to see what is in the index. Remove the skip line or move the note, then run `ingest` again.

## Search finds nothing

**What you see:** an empty list.
**Why:** your words match nothing, or the note uses other words.
**Fix:**

1. Try fewer words, or one distinctive word from the note.
2. Put an exact name or number in quotes.
3. Look further down. Older notes in archive folders come after the main ones.
4. Try [note cards](cards.md), which help when your words differ from the note's.

## The wrong note comes first

**Why:** the order comes from many signals, not only your words. A note in a core folder counts more. A newer note counts more. A note marked `archived`, `closed` or `done` counts less. See [How results are ranked](search-ranking.md).
**Fix:**

1. Read the `why:` line under the result. It says what made it rank high.
2. Search again with `--plain` to turn off the extras and see the words-only order.
3. If one note always ranks too high, change its `status` or move it to an archive folder.
4. If many results look wrong, tell us. Use the **Bug** form in [Help and feedback](../README.md#help-and-feedback). Say which question you asked and which note you expected.

## A note is hidden

**What you see:** you know a note exists, and it never comes back.
**Why:** a note is hidden when its status is `superseded`, `deprecated` or `replaced`, or when its `valid_until` date has passed.
**Fix:** change the status or the date in the note, then run `ingest`. The note comes back on the next search.

## Search is slow

**What you see:** a search takes more than a few hundred milliseconds. The health check warns above 300 ms.
**Why:** the index is very large and on a slow disk, or the notes folder is on a network drive.
**Fix:** put `ENGRAM_DATA` on a fast local disk. Keep the notes folder on a local disk too, or copy it. Run `python3 engram.py health` to see the speed check.

## Note cards

### "No API key"

**Why:** cards need a key from your own AI account. Without it, search still works and no cards appear.
**Fix:** [Note cards](cards.md) shows how to set the key. Never put the key in a note.

### Cards stop partway

**Why:** a round has a limit (1,500 cards in the working version), or the AI service returned an error.
**Fix:** run the cards command again. Cards already made are kept, and you do not pay for them twice.

## A private folder

### Its text does not show

**Why:** this is on purpose. A match in a private folder shows only the file and heading, and every word of your question must match.
**Fix:** open the note yourself, or ask for it by its number. See [Safety](safety.md#private-folders).

### A private folder shows up in normal results

**Why:** the folder is not marked private, or its name is spelled differently from the setting.
**Fix:** check the private folder setting in [Settings](settings.md), then rebuild with `--rebuild`. Then run `python3 engram.py health`. It checks that no private or password files are in the main index.

## Still stuck?

- Search the [FAQ](faq.md).
- Ask in the **Question** form in [Help and feedback](../README.md#help-and-feedback).
- Send a security problem to the private report in [SECURITY.md](../SECURITY.md), not to a public issue.
