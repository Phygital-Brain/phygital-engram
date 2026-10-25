# Changelog

## 0.2.0 (2026-10-25)

- The search page: `python3 engram.py page` opens a small page on your own computer, in the Phygital Engram look (dark, and light that follows your system), with search, a read-only view of your notes, the health check and the test score. It listens on `127.0.0.1` only and loads nothing from the internet. A link like `/?q=your+question` opens it with a question already asked.

## 0.1.1 (2026-10-25)

- One-line install. `install.sh` (Mac and Linux) downloads the program, builds the index and connects Claude Code. The Claude Code plugin now asks for your notes folder when you install it.
- The AI connector on your computer builds the index when it starts and updates it every 10 minutes, so there is no separate step.
- A `~` in the index folder path is now expanded.
- Python 3.11 or newer is the tested minimum. The sample test gives the same result on 3.11, 3.13 and 3.15.
- The README starts with the install lines, and the guides say what was tested.

## 0.1.0 (2026-10-25)

- First release: the search itself (`engram.py`, `engram_lib/`, `config.json`), the documentation, a sample test with made-up notes, and a Docker image on the Packages page.
- The connector for AI apps (`mcp/server.py`) with four read-only tools: `search_notes`, `open_result`, `around_result`, `check_index`.
- The server version (`mcp/serve.py`): the same four tools at an https address behind a passphrase login, for phones, the Claude website, ChatGPT and any computer. Comes with a Dockerfile, a Compose file, a Caddyfile and `tests/test_serve.py`. Tested with 11 automated tests, Claude Code over HTTP and the login page in a browser. The Docker image builds on GitHub. Not tested on a real server, on a phone, the Claude website or ChatGPT.
- A Claude Code plugin and the Claude Desktop extension file, `phygital-engram.mcpb`, attached to the release.
- Left out of this version: the small local web page, and saving Claude Code sessions.
