"""The folder filter: a search with --folder returns only notes inside that folder. Uses the made-up sample notes."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = Path(__file__).resolve().parent / "sample-notes"


class FolderFilter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = tempfile.TemporaryDirectory()
        cls.env = dict(os.environ, ENGRAM_VAULT=str(NOTES), ENGRAM_DATA=cls.data.name)
        cls.run_cli("ingest")

    @classmethod
    def tearDownClass(cls):
        cls.data.cleanup()

    @classmethod
    def run_cli(cls, *args):
        p = subprocess.run([sys.executable, str(ROOT / "engram.py"), *args], capture_output=True, text=True,
                           timeout=120, env=cls.env)
        if p.returncode:
            raise AssertionError(p.stderr)
        return p.stdout

    def search(self, q, *extra):
        return [r["path"] for r in json.loads(self.run_cli("search", q, "--json", "-n", "20", *extra))]

    def test_only_notes_inside_the_folder(self):
        everywhere = self.search("cover")
        self.assertTrue(any(not p.startswith("Projects/Picture-Book/") for p in everywhere))
        inside = self.search("cover", "--folder", "Projects/Picture-Book")
        self.assertTrue(inside)
        self.assertTrue(all(p.startswith("Projects/Picture-Book/") for p in inside), inside)

    def test_slashes_around_the_folder_are_fine(self):
        self.assertEqual(self.search("cover", "--folder", "/Projects/Picture-Book/"),
                         self.search("cover", "--folder", "Projects/Picture-Book"))

    def test_unknown_folder_finds_nothing(self):
        self.assertEqual(self.search("cover", "--folder", "No_Such%Folder"), [])


if __name__ == "__main__":
    unittest.main()
