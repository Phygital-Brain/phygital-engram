# Settings

Where each setting lives, what it does, and the few you are likely to change.

> [!NOTE]
> Every default on this page comes from `config.json` in version 0.1.1. The defaults are general. They are a starting point, so check them against your own folders.

<details>
<summary><b>Table of contents</b></summary>

- [Where settings come from](#where-settings-come-from)
- [The settings most people change](#the-settings-most-people-change)
- [Where your notes and data are](#where-your-notes-and-data-are)
- [What gets read](#what-gets-read)
- [How notes are cut up](#how-notes-are-cut-up)
- [Ranking](#ranking)
- [Folder levels and hints](#folder-levels-and-hints)
- [Learning from use, links and callouts](#learning-from-use-links-and-callouts)
- [AI chat notes](#ai-chat-notes)
- [Private folders](#private-folders)
- [Secrets and ID numbers](#secrets-and-id-numbers)
- [Note cards](#note-cards)
- [Speed and housekeeping](#speed-and-housekeeping)
- [Files in your data folder](#files-in-your-data-folder)
- [The connector](#the-connector)
- [The server version](#the-server-version)

</details>

## Where settings come from

There are two places, and the second wins.

1. **A `config.json` file** next to the program. It holds a default for every setting.
2. **Three environment variables**, set in your terminal or in a `.env` file next to the program. They override the file.

| Environment variable | Default | Effect |
|---|---|---|
| `ENGRAM_VAULT` | `~/Notes`, the `vault` path in `config.json` | The notes folder to read. Set this first |
| `ENGRAM_DATA` | the program's own folder | Where the index and other data files are kept. It must be outside the notes folder. If it is inside, the program refuses to run |
| `ANTHROPIC_API_KEY` | none | Your own key for note cards. Without it, no cards are made and search still works. Never put it in a note or in `config.json` |

Do not put real keys in this repository. Git ignores the `.env` file.

## The settings most people change

If you change only a few, look at these seven.

| Setting | Why you would change it |
|---|---|
| `vault` (or `ENGRAM_VAULT`) | Point it at your own notes folder |
| `exclude_paths` | Folders to leave out, such as a copy of a website or test files. It is empty by default |
| `skip_dirs` | Hidden or tool folders to skip |
| `path_weights` | Which of your folders count more or less. The defaults are general: change them to fit your layout |
| `evergreen_paths` | Folders whose notes never fade with age |
| `status_weights` | If you use status words other than `done`, `paused` and `archived` |
| `cards` | The AI model for cards, or leave cards off |

## Where your notes and data are

| Name | Default | Effect |
|---|---|---|
| `vault` | `~/Notes` | The notes folder. Overridden by `ENGRAM_VAULT` |
| `db` | `data/engram.sqlite` | The index file. Moves with `ENGRAM_DATA` |

## What gets read

| Name | Default | Effect |
|---|---|---|
| `skip_dirs` | `.context`, `.obsidian`, `.git`, `.claude`, `node_modules`, `.trash` | Folders that are never read |
| `exclude_paths` | none | Paths (with `*`) to leave out. Add yours here |
| `max_file_bytes` | 2,000,000 | Notes bigger than this are skipped |
| `skip_markers` | `engram: skip`, `#engram-skip` | A note with one of these near the top is not indexed. Use it for notes you never want found |
| `hide_status` | `superseded`, `deprecated`, `replaced` | Notes with these statuses are hidden from results |

Phygital Engram also respects a `.claudeignore` file in the notes folder. Anything it lists is skipped.

## How notes are cut up

| Name | Default | Effect |
|---|---|---|
| `chunk_max_chars` | 2000 | The longest a section may be before it is split in two |
| `chunk_min_chars` | 150 | Sections shorter than this join the next one |
| `chunk_overlap_chars` | 200 | How much two split pieces share, so no sentence is lost at the cut |

## Ranking

How the signals work together is explained in [search ranking](search-ranking.md).

| Name | Default | Effect |
|---|---|---|
| `recency.boost` | 0.5 | How much newer notes count. 0.5 means a note from today counts 1.5x |
| `recency.half_life_days` | 180 | After this many days the extra boost is halved |
| `evergreen_paths` | `*CLAUDE.md`, `*AGENTS.md`, `Context/*`, `*/decisions/*`, `Library/*` | Notes here never fade with age |
| `evergreen_exclude` | none | Exceptions to `evergreen_paths` |
| `status_weights` | archived 0.4, closed 0.5, done 0.6, paused 0.7, legacy 0.3 | Multiplier for notes with this `status` |
| `type_weights` | batch 0.4, queue 0.4, log 0.5 | Multiplier for notes with this `type` |
| `exact_boost` | 0.15 | How much an exact match (a version, an ID, a "quoted" phrase) lifts a result |
| `results_default` | 10 | How many results a search returns if you do not ask for a number |
| `max_chunks_per_file_in_results` | 2 | The most sections one note may show in a list |
| `shelves.enabled` | `true` | Puts archive folders on a separate "background" shelf |
| `shelves.background_paths` | `*/archive/*`, `archive/*` | What counts as background |
| `shelves.mode` | `after` | `after`: background results follow the main ones. `merge`: all results are ranked together |
| `shelves.background_query` | `and` | `and`: background notes must match every word. This is fast and precise |
| `shelves.max_in_results` | 3 | The most background results shown after the main ones |
| `common_words.enabled` | `true` | Skips very common words in big indexes |
| `common_words.min_sections` | 200,000 | Applies only when the index has this many sections |
| `common_words.doc_share` | 0.25 | A word found in more than this share of sections is skipped |

## Folder levels and hints

| Name | Default | Effect |
|---|---|---|
| `path_weights` | `*/archive/*` 0.35, `archive/*` 0.35, `Library/*` 0.6, `*CLAUDE.md` 2.0, `*AGENTS.md` 2.0, `Context/*` 1.6 | A list of `match` and `weight` pairs. The weight applies to notes whose path matches. The first match wins. Capital letters do not matter. Add rules for your own folders |
| `folder_hints.boost` | 2.0 | How much a hint lifts notes in the folder it points at |
| `folder_hints.rules` | A list of `when` (a pattern in the question) and `folders`. Three rules: `decision` points to `*/decisions/*`, `daily` or `journal` to `Daily/*`, `client` or `clients` (and "worked with" or "worked for") to `*/Clients/*` | Words in the question that point at a folder. Add your own rules for your own folder names |

## Learning from use, links and callouts

| Name | Default | Effect |
|---|---|---|
| `usage.enabled` | `true` | Counts which results are shown and opened |
| `usage.min_total_opens` | 50 | Nothing happens until this many real opens are counted |
| `usage.open_boost` | 0.3 | The most a note rises for being opened often |
| `usage.opens_for_full_boost` | 5 | Opens a note needs to get the full boost |
| `usage.ignored_after_shown` | 20 | A note shown this many times and never opened sinks a little |
| `usage.ignored_factor` | 0.85 | How far it sinks |
| `usage.half_life_days` | 90 | Old counts lose half their weight after this many days |
| `backlinks.enabled` | `true` | Notes that many other notes link to count a little more |
| `backlinks.boost` | 0.1 | The size of that boost |
| `backlinks.cap` | 30 | Links counted up to this number |
| `callouts.enabled` | `true` | Text inside callouts like `> [!important]` counts like tags |

## AI chat notes

These settings are for chats you save by hand as notes. Leave them alone if you do not.

| Name | Default | Effect |
|---|---|---|
| `conversations.path` | `AI Conversations/` | Where saved chats live, inside the notes folder |
| `conversations.age_steps` | half weight until 182 days, then a quarter | Older chats count less |
| `conversations.expire_days` | 365 | After this many days, a chat leaves search. It is never deleted |
| `conversations.max_in_results` | 3 | The most chat results after the notes |
| `conversations.value_factor` | high 1.5, medium 1.0, low 0.6 | How much a chat counts by its rated value |
| `conversations.keep_weight` | 1.0 | A chat marked `keep: true` stops fading |
| `conversations.decision_factor` | 1.3 | Chats that contain a decision count more |
| `conversations.linked_note_factor` | 0.7 | A chat that links to a note counts less than the note |
| `conversations.superseded_factor` | 0.5 | A newer chat on the same topic halves the older one |
| `conversations.half_life_days`, `high_value_ages_at`, `decision_expire_factor` | 60, 0.5, 1.5 | How fast chats fade, and how long valuable ones last |

## Private folders

| Name | Default | Effect |
|---|---|---|
| `private.enabled` | `true` | Uses the locked index for the folders below |
| `private.paths` | `Finances/`, `Memory/finances/` | Folders that are findable but locked. They are matched from the top of the notes folder, and capital letters do not matter. A match shows only the file and heading |
| `private.db` | `data/private.sqlite` | The separate index file for them |
| `private.id_patterns` | tax IDs, bank numbers, card numbers | Patterns that are blanked before storing |

See [privacy](privacy.md) for what "locked" means.

## Secrets and ID numbers

| Name | Default | Effect |
|---|---|---|
| `redact_patterns` | Patterns for API keys, tokens, private keys, `SECRET=` or `PASSWORD=` lines, labelled tax IDs, bank numbers, card numbers | Anything that matches becomes `[REDACTED]` before it is stored. Add your own pattern if your key format is not covered |

## Note cards

| Name | Default | Effect |
|---|---|---|
| `cards.model` | `claude-haiku-5-5` | The AI model that writes cards |
| `cards.sources` | `vault`, `chat` | What gets cards: notes and saved chats |
| `cards.max_tokens` | 1500 | The longest answer the model may write for one card |
| `cards.workers` | 12 | How many cards are written at the same time |

Cards need `ANTHROPIC_API_KEY`. Without it, no cards are made and nothing is sent. See [cards](cards.md).

## Speed and housekeeping

| Name | Default | Effect |
|---|---|---|
| `store_text_once` | `true` | Keeps the text once, not twice, which halves the disk space used. It needs SQLite 3.43 or newer and turns itself off with an older one |
| `tidy_every_days` | 7 | How often the index is tidied after an update, so it does not slowly get slower |
| `speed_warn_ms` | 300 | The health check warns if a search takes longer than this |

## Files in your data folder

| File | What it is | Safe to delete? |
|---|---|---|
| `engram.sqlite` | The index | Yes. It rebuilds from your notes |
| `private.sqlite` | The index for private folders | Yes. It rebuilds |

Deleting the index loses no notes. Cards live inside the index, so deleting it means paying for cards again.

## The connector

The connector for AI apps (`mcp/server.py`, see [tools.md](tools.md)) has one setting of its own. It also passes `ENGRAM_VAULT` and `ENGRAM_DATA` on to the search.

| Name | Default | What it does |
|---|---|---|
| `PHYGITAL_ENGRAM_CLI` | The `engram.py` next to the `mcp` folder | The path to the search program the connector runs. Change it only if you keep the program somewhere else |

## The server version

The server version (`mcp/serve.py`, see [setup-own-server.md](setup-own-server.md)) is set with environment variables, usually in a `.env` file next to `docker-compose.yml`. It also passes `ENGRAM_VAULT` and `ENGRAM_DATA` on to the search.

| Name | Default | What it does |
|---|---|---|
| `PUBLIC_URL` | None. Required | Where the server is reached, like `https://notes.example.com`. It must start with `https://`, or the server refuses to start |
| `LOGIN_HASH` | None | The fingerprint of your passphrase. Make it with `python3 mcp/serve.py hash`. Use this one |
| `LOGIN_PASSPHRASE` | None | Your passphrase in plain text, 8 or more characters. Use it only if you cannot use `LOGIN_HASH`. One of the two is required |
| `HOST` | `127.0.0.1` | The address the server listens on |
| `PORT` | `8765` | The port the server listens on |
| `PHYGITAL_ENGRAM_REFRESH_MINUTES` | `10` | How often the index is updated while the connector or the server runs. `0` means once at start, then never |
| `PHYGITAL_ENGRAM_TRUST_PROXY` | Off | Set to `1` when a proxy like Caddy sits in front, so the visitor's address is read from it. Needed for the 5-wrong-passphrases pause to count the right address |
| `ALLOWED_REDIRECT_HOSTS` | `claude.ai,claude.com,chatgpt.com,openai.com,vscode.dev` | The AI apps allowed to log in. Others are refused |
| `NOTES_DIR` | None. Required in Compose | The folder of notes on the server, mounted read-only |
| `PHYGITAL_ENGRAM_DOMAIN` | None. Required in Compose | Your domain. Compose builds `PUBLIC_URL` from it and Caddy gets the certificate for it |

The server refuses to start without a passphrase of 8 or more characters, or without an https `PUBLIC_URL`. It pauses a login for 15 minutes after 5 wrong passphrases from one address.
