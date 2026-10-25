"""Tests for the search page (app/server.py). It starts the page on a free port, on the made-up sample notes.
It checks that the page answers only itself, never leaves your computer, never opens secret files, and never changes notes."""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        r = urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError as e:
        r = e
    return r.status if hasattr(r, "status") else r.code, r.read().decode("utf-8", "replace")


class SearchPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        cls.notes = cls.tmp / "Notes"
        shutil.copytree(ROOT / "tests" / "sample-notes", cls.notes)
        (cls.notes / ".env").write_text("TOKEN=made-up-not-real\n")  # a secret file the page must never open
        (cls.notes / ".claudeignore").write_text(".env\n")
        cls.before = {str(p.relative_to(cls.notes)): p.read_bytes() for p in cls.notes.rglob("*") if p.is_file()}
        cls.port = free_port()
        cls.base = f"http://127.0.0.1:{cls.port}"
        env = dict(os.environ, ENGRAM_VAULT=str(cls.notes), ENGRAM_DATA=str(cls.tmp / "data"), ENGRAM_PAGE_PORT=str(cls.port),
                   ENGRAM_NO_BROWSER="1")
        subprocess.run([sys.executable, str(ROOT / "engram.py"), "ingest", "--rebuild"], env=env, check=True,
                       capture_output=True, timeout=60)
        cls.proc = subprocess.Popen([sys.executable, str(ROOT / "engram.py"), "page"], env=env,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                if get(cls.base + "/")[0] == 200:
                    break
            except OSError:
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError("the page did not start")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=10)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_page_has_the_name_and_no_outside_addresses(self):
        status, html = get(self.base + "/")
        self.assertEqual(status, 200)
        self.assertIn("Phygital Engram", html)
        outside = [u for u in re.findall(r"""(?:src|href)=["'](https?://[^"']+)""", html)]
        self.assertEqual(outside, [], "the page must not load anything from the internet")

    def test_search_finds_the_right_note_first(self):
        status, body = get(self.base + "/api/search?q=when+is+the+cover+due")
        self.assertEqual(status, 200)
        rows = json.loads(body)["rows"]
        self.assertEqual(rows[0]["path"], "Projects/Picture-Book/notes/schedule.md")

    def test_it_answers_only_itself(self):
        self.assertEqual(get(self.base + "/api/search?q=cover", {"Host": "evil.example"})[0], 403)
        self.assertEqual(get(self.base + "/api/search?q=cover", {"Origin": "https://evil.example"})[0], 403)

    def test_it_cannot_leave_the_notes_folder(self):
        self.assertEqual(get(self.base + "/api/files/read?path=../../etc/passwd")[0], 404)
        self.assertEqual(get(self.base + "/api/files/read?path=/etc/passwd")[0], 404)

    def test_secret_files_are_never_shown(self):
        status, body = get(self.base + "/api/files/read?path=.env")
        text = json.dumps(json.loads(body)) if status == 200 else body
        self.assertNotIn("made-up-not-real", text)

    def test_private_notes_stay_locked(self):
        status, body = get(self.base + "/api/files/read?path=Memory/finances/2026-q3-income.md")
        d = json.loads(body)
        self.assertEqual(d.get("kind"), "locked")
        self.assertNotIn("9,000", body)

    def test_notes_are_never_changed(self):
        get(self.base + "/api/search?q=cover")
        after = {str(p.relative_to(self.notes)): p.read_bytes() for p in self.notes.rglob("*") if p.is_file()}
        self.assertEqual(after, self.before)


if __name__ == "__main__":
    unittest.main()
