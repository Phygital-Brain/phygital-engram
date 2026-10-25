# Search ranking

Why one note comes first and another tenth: every signal that moves a result, and which ones you can change.

<details>
<summary><b>Table of contents</b></summary>

- [The short version](#the-short-version)
- [An example, step by step](#an-example-step-by-step)
- [The nine steps](#the-nine-steps)
- [Folder levels](#folder-levels)
- [Status and type](#status-and-type)
- [Newer counts more](#newer-counts-more)
- [What nothing ever does](#what-nothing-ever-does)
- [Change the ranking](#change-the-ranking)

</details>

<p align="center"><img src="images/ranking.png" alt="Six steps that decide the order of results: your words, exact things like versions and file paths, where the note lives, whether it is done or old, how new it is, and a tidy list with at most 2 sections per note." width="640"></p>

## The short version

A search finds sections that share your words. It lifts the ones you probably mean: rule files, current notes, and notes in the folder you hinted at. It pushes down likely old or noisy ones: archive folders, logs and finished work. Then it explains each result in one line.

## An example, step by step

Made-up notes, made-up question. You ask: *what are our decisions about the Picture-Book cover?*

| Note | Folder | What happens |
|---|---|---|
| `Projects/Picture-Book/decisions/2026-09-12-cover-colours.md` | decisions | Has "decision", "cover" and "Picture-Book" in the heading. The word "decisions" in your question also points at folders named `decisions` (step 7), and notes there never fade. First |
| `Projects/Picture-Book/README.md` | normal | Has "cover" and "Picture-Book" many times, but no decision words. Second |
| `Projects/Picture-Book/notes/cover-ideas.md` | normal | Matches "cover". Its status is `done`, so it counts 0.6x. Third |
| `archive/2025/old-cover-brief.md` | background | Matches "cover", but archive folders count 0.35x and come after the main notes. Last |

Each result comes back with a why line, like "your words in the heading, decision, 12 days old".

## The nine steps

### 1. Words

The question is cut into words, and filler words (the, a, of) are dropped. The index compares the rest with every section. Rare words count more than common ones. Words match by root, so "dashes" finds "dash" and "deciding" finds "decided". A match in the **file name** counts most. Next come the **heading**, then **tags** and the **note card** (if you made cards), then the **body**.

### 2. Exact matches

Version numbers, IDs, file paths, host names and anything you put in "quotes" are also matched letter for letter. An exact match adds a boost you can tune (`exact_boost`) and is marked EXACT in the result. So a search for `v2.4.1` finds the note with `v2.4.1`, not the one about version 2.

### 3. Folder levels

Notes in some folders count more than others. See [Folder levels](#folder-levels) below.

### 4. Status and type

Finished and quiet work counts less. See [Status and type](#status-and-type) below.

### 5. Newer counts more

Newer notes count up to 1.5 times as much. The boost halves every 180 days. Notes in "core" folders never fade. See [Newer counts more](#newer-counts-more).

### 6. Light extras

These small signals only break ties.

- **Callouts.** Text inside Obsidian-style callouts (`> [!important] Decision`) counts like tags, because people put the key point there.
- **Links.** A note that many other notes link to gets a small boost, up to 10 percent.
- **Learning from use.** This starts after 50 real opens are counted. Then a note you open often rises a little (up to 30 percent). A note shown 20 times but never opened sinks a little (down to 85 percent). Only counts are kept, never your questions.

### 7. Folder hints

Words in your question can point at a folder. Notes in that folder count 2x for that search. These are the three rules in `config.json`. You can add your own.

| You say | Boosted folder |
|---|---|
| "decision", "decisions" | any folder named `decisions` (`*/decisions/*`) |
| "daily", "journal" | `Daily/` |
| "client", "clients", "worked with", "worked for" | any folder named `Clients` (`*/Clients/*`) |

A hint only boosts. It never filters. If the hint is wrong, the right note is still found, a little lower. The words *check*, *show*, *tell*, *find* and *please* are ignored.

### 8. The shape of the answer

- At most 2 sections per note, so one long note cannot fill the list.
- Background folders (archive folders) come after the main notes, at most 3. If the main notes did not fill the list, more can follow.
- AI chat notes you saved come after the notes, at most 3.
- Private matches come last, locked, at most 2.
- Every result has a short why line.

### 9. Limits

A question is cut to 500 characters and 20 words. At most 50 results come back. The default is 10.

## Folder levels

These are the levels in the `config.json` that ships with version 0.1.1. They are general. If your folders have other names, set your own in `path_weights` and `evergreen_paths`. See [settings](settings.md). Capital letters do not matter in these rules.

| Level | Folders | Weight | Fades with age? |
|---|---|---|---|
| Core | Rule files (`*CLAUDE.md`, `*AGENTS.md`) | 2x | Never |
| Core | `Context/` | 1.6x | Never |
| Core | Any folder named `decisions` (`*/decisions/*`) | 1x | Never |
| Normal | Everything else (projects, daily notes, resources) | 1x | Yes |
| Outside material | `Library/` | 0.6x | Never |
| Background | `archive/` at the top, or any `archive` folder below it | 0.35x | Yes |

## Status and type

The `status` and `type` in a note's info block change its weight.

| Status | Weight | Why |
|---|---|---|
| `archived` | 0.4x | Put away on purpose |
| `closed` | 0.5x | Finished |
| `done` | 0.6x | Finished |
| `paused` | 0.7x | Not active now |
| `legacy` | 0.3x | Old way of doing it |
| `superseded`, `deprecated`, `replaced` | Hidden | Another note took over |

| Type | Weight | Why |
|---|---|---|
| `batch`, `queue` | 0.4x | Machine-made lists |
| `log` | 0.5x | Run records |

A note with `valid_until: 2026-12-31` hides itself the day after that date. A note with `keep: true` never fades or expires. A note with `engram: skip` near the top is not indexed at all.

## Newer counts more

A note from today is multiplied by 1.5. The extra half halves every 180 days. A note from six months ago gets about 1.25x, and one from two years ago about 1.03x. Core notes, such as your rules and context, never fade.

## What nothing ever does

- Nothing hides a note on a guess. Folder hints, links and learning from use only change the order.
- Nothing is deleted. Hidden notes stay in your folder and are only left out of results.
- Nothing is sent anywhere. All of this runs on your computer.

## Change the ranking

The ranking is made of settings. Most people change three things: which folders are core, which are background, and which statuses count less. See [settings](settings.md). To check that a change helped, write 10 to 20 test questions and run the test score. See [benchmarks](benchmarks.md).
