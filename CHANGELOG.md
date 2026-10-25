# Changelog

## 0.1.0 (not released yet)

- Pre-release: the documentation, the brand, the repository files and a sample test with made-up notes.
- The connector for AI apps (`mcp/server.py`) with four read-only tools: `search_notes`, `open_result`, `around_result`, `check_index`.
- The server version (`mcp/serve.py`): the same four tools at an https address behind a passphrase login, for phones, the Claude website, ChatGPT and any computer. Comes with a Dockerfile, a Compose file, a Caddyfile and `tests/test_serve.py`. Tested with 10 automated tests and Claude Code over HTTP. Not tested in Docker, on a real server, in a browser login, on a phone, the Claude website or ChatGPT.
- A Claude Code plugin and a Claude Desktop extension build. The search code is added with this version.
