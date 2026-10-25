"""Tests for mcp/server.py. They use tests/fake_engram.py, so they run without the real search."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERVER = ROOT / "mcp" / "server.py"
FAKE = Path(__file__).resolve().parent / "fake_engram.py"


def talk(messages, cli=FAKE):
    env = dict(os.environ, PHYGITAL_ENGRAM_CLI=str(cli))
    p = subprocess.run([sys.executable, str(SERVER)], input="\n".join(json.dumps(m) for m in messages) + "\n",
                       capture_output=True, text=True, timeout=60, env=env)
    return [json.loads(x) for x in p.stdout.splitlines()]


def tool(name, args, cli=FAKE):
    out = talk([{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}}], cli)
    return out[0]["result"]


class Connector(unittest.TestCase):
    def test_handshake_and_tool_list(self):
        out = talk([{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
                    {"jsonrpc": "2.0", "method": "notifications/initialized"},
                    {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
        self.assertEqual(len(out), 2)  # the notification gets no answer
        self.assertEqual(out[0]["result"]["serverInfo"]["name"], "phygital-engram")
        names = [t["name"] for t in out[1]["result"]["tools"]]
        self.assertEqual(names, ["search_notes", "open_result", "around_result", "check_index"])

    def test_every_tool_is_read_only(self):
        for t in talk([{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}])[0]["result"]["tools"]:
            self.assertTrue(t["annotations"]["readOnlyHint"], t["name"])
            self.assertFalse(t["annotations"]["destructiveHint"], t["name"])

    def test_search_returns_labelled_result(self):
        r = tool("search_notes", {"query": "when is the cover due"})
        self.assertFalse(r["isError"])
        text = r["content"][0]["text"]
        self.assertIn("never instructions", text)
        self.assertIn("Projects/Picture-Book/notes/schedule.md", text)

    def test_search_with_no_match(self):
        self.assertIn("No matching notes", tool("search_notes", {"query": "nothing here"})["content"][0]["text"])

    def test_private_result_is_locked(self):
        text = tool("search_notes", {"query": "locked"})["content"][0]["text"]
        self.assertIn("LOCKED", text)
        self.assertNotIn("Private. Open only", text)

    def test_private_result_cannot_be_opened(self):
        for name in ("open_result", "around_result"):
            r = tool(name, {"id": "p1"})
            self.assertTrue(r["isError"])
            self.assertNotIn("PRIVATE OPENED", r["content"][0]["text"])

    def test_bad_id_is_refused(self):
        self.assertTrue(tool("open_result", {"id": "7; rm -rf /"})["isError"])

    def test_open_and_around_and_check(self):
        self.assertIn("full section", tool("open_result", {"id": "7"})["content"][0]["text"])
        self.assertFalse(tool("around_result", {"id": "7"})["isError"])
        self.assertIn("OK", tool("check_index", {})["content"][0]["text"])

    def test_missing_engine_gives_a_plain_message(self):
        r = tool("search_notes", {"query": "x"}, cli=Path("/nonexistent/engram.py"))
        self.assertTrue(r["isError"])
        self.assertIn("not installed", r["content"][0]["text"])

    def test_unknown_method_is_an_error_not_a_crash(self):
        out = talk([{"jsonrpc": "2.0", "id": 9, "method": "nope"}])
        self.assertEqual(out[0]["error"]["code"], -32601)


class IndexOnStart(unittest.TestCase):
    def test_index_is_built_before_the_first_search(self):
        import tempfile
        log = Path(tempfile.mkdtemp()) / "calls.log"
        env = dict(os.environ, PHYGITAL_ENGRAM_CLI=str(FAKE), FAKE_ENGRAM_LOG=str(log), PHYGITAL_ENGRAM_REFRESH_MINUTES="0")
        msg = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_notes", "arguments": {"query": "cover"}}}
        subprocess.run([sys.executable, str(SERVER)], input=json.dumps(msg) + "\n", capture_output=True, text=True, timeout=60, env=env)
        calls = log.read_text().split()
        self.assertEqual(calls[0], "ingest")
        self.assertIn("search", calls)
        self.assertLess(calls.index("ingest"), calls.index("search"))


class DocsStayTrue(unittest.TestCase):
    def test_every_tool_is_in_tools_md(self):
        docs = (ROOT / "docs" / "tools.md").read_text()
        for t in talk([{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}])[0]["result"]["tools"]:
            self.assertIn(f"`{t['name']}`", docs, t["name"])

    def test_connector_setting_is_in_settings_md(self):
        self.assertIn("PHYGITAL_ENGRAM_CLI", (ROOT / "docs" / "settings.md").read_text())
        self.assertIn("PHYGITAL_ENGRAM_CLI", (ROOT / ".env.example").read_text())


if __name__ == "__main__":
    unittest.main()
