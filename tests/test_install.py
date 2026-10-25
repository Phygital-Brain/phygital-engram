"""Tests for install.sh: its safety checks, which need no network. A full install is checked by hand."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "install.sh"


@unittest.skipUnless(shutil.which("sh") and shutil.which("git") and shutil.which("python3"), "needs sh, git and python3")
class InstallerChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.notes = self.tmp / "Notes"
        self.notes.mkdir()
        (self.notes / "CLAUDE.md").write_text("")
        (self.notes / "a.md").write_text("A note.\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_it(self, *args):
        env = dict(os.environ, HOME=str(self.tmp), PHYGITAL_ENGRAM_SOURCE="/nonexistent")
        return subprocess.run(["sh", str(SCRIPT), *args], capture_output=True, text=True, timeout=60, env=env)

    def test_needs_a_notes_folder(self):
        p = self.run_it()
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("where your notes are", p.stderr)

    def test_notes_folder_must_have_claude_md(self):
        (self.notes / "CLAUDE.md").unlink()
        p = self.run_it(str(self.notes))
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("CLAUDE.md", p.stderr)

    def test_data_folder_inside_notes_is_refused_and_nothing_is_created(self):
        before = sorted(p.name for p in self.notes.iterdir())
        for data in (self.notes / "data", self.notes, self.notes / ".." / "Notes" / "x"):
            p = self.run_it(str(self.notes), str(data))
            self.assertNotEqual(p.returncode, 0)
            self.assertIn("inside your notes folder", p.stderr)
        self.assertEqual(sorted(p.name for p in self.notes.iterdir()), before)
        self.assertFalse((self.tmp / ".phygital-engram").exists())


if __name__ == "__main__":
    unittest.main()
