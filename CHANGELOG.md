# Changelog

## 0.1.0 (2026-10-25)

- First release: the search itself (`engram.py`, `engram_lib/`, `config.json`), the documentation, a sample test with made-up notes, and a Docker image on the Packages page.
- The connector for AI apps (`mcp/server.py`) with four read-only tools: `search_notes`, `open_result`, `around_result`, `check_index`.
- The server version (`mcp/serve.py`): the same four tools at an https address behind a passphrase login, for phones, the Claude website, ChatGPT and any computer. Comes with a Dockerfile, a Compose file, a Caddyfile and `tests/test_serve.py`. Tested with 11 automated tests and Claude Code over HTTP. Not tested in Docker, on a real server, in a browser login, on a phone, the Claude website or ChatGPT.
- A Claude Code plugin and the Claude Desktop extension file, `phygital-engram.mcpb`, attached to the release.
- Left out of this version: the small local web page, and saving Claude Code sessions.
