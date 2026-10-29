"""The folder filter: a search with --folder returns only notes inside that folder. Uses the made-up sample notes."""
import json
import os
import shutil
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



class FolderMap(unittest.TestCase):
    """engram.py map: the main folders, their note counts, and a line from README.md, AGENTS.md or CLAUDE.md."""

    def test_map_lists_folders_and_reads_agents_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            notes = Path(tmp) / "notes"
            shutil.copytree(NOTES, notes)
            (notes / "Projects" / "AGENTS.md").write_text("# Projects\n\nOne folder per book or zine, with its [[schedule]].\n")
            env = dict(os.environ, ENGRAM_VAULT=str(notes), ENGRAM_DATA=str(Path(tmp) / "data"))
            run = lambda *a: subprocess.run([sys.executable, str(ROOT / "engram.py"), *a], capture_output=True,
                                            text=True, timeout=120, env=env, check=True).stdout
            run("ingest")
            lines = run("map").splitlines()
        self.assertIn("- Projects (9 notes): One folder per book or zine, with its schedule.", lines)
        self.assertTrue(any(x.startswith("- Daily (3 notes): recent: ") for x in lines), lines)

if __name__ == "__main__":
    unittest.main()
