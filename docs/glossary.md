# Glossary

Every term used in these docs, in plain words.

| Word | What it means here |
|---|---|
| Agent | The AI app that works for you, such as Claude, ChatGPT or Codex. It asks Phygital Engram a question and writes the answer |
| Background notes | Notes in archive folders or copied code. They are searched too, but they come after the main notes |
| Card (note card) | A short summary an AI writes once for a section: context, a summary, questions people might ask, and exact facts. Optional. See [cards](cards.md) |
| Core notes | Your rule files and context notes. They count more and never fade with age |
| Folder hint | A word in your question that points at a folder, like "decisions". It lifts that folder's notes. It never hides others |
| Hidden note | A note left out of results because its `status` says it was replaced, or its `valid_until` date passed. It stays in your folder |
| Index | The small database file that makes search fast. It is built from your notes and can be deleted and rebuilt at any time |
| Info block | The lines at the very top of a note between two `---` lines (also called frontmatter). They hold `date`, `status`, `tags` and more |
| Learning from use | A light ranking step that notices which results you open. It starts after 50 opens and keeps counts, not questions |
| MCP | Short for Model Context Protocol. A standard plug that lets an AI app use a tool. Phygital Engram includes a connector (`mcp/server.py`) that gives an AI app four read-only tools. See [tools](tools.md) |
| Notes folder | The folder of Markdown files that Phygital Engram reads. It never changes it |
| Private folder | A folder whose notes can be found but not read until you ask. A match shows only the file and heading |
| Ranking | The order of results, best first |
| Result | One section of one note that matched your question |
| Section | A piece of a note, cut at its headings. Search works on sections, not whole notes |
| Source | Where a result comes from: the note, the heading and the date |
| Status | A word in a note's info block, like `active`, `done` or `paused`. Finished work counts less |
| Why line | One short line on each result that says why it came back |

Next, read [how it works](how-it-works.md) or go back to the [README](../README.md).
