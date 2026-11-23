"""Date search: a time phrase in the question ("last week", "in September") lifts notes dated inside that range.
The pure tests use a fixed day. The search test writes two made-up notes in a temporary folder."""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engram_lib.search import date_range  # noqa: E402

TODAY = dt.date(2026, 11, 23)  # a Monday


def days(q, today=TODAY):
    rng, rest = date_range(q, today)
    if rng is None:
        return None, rest
    start = dt.datetime.fromtimestamp(rng[0]).date()
    last = dt.datetime.fromtimestamp(rng[1]).date() - dt.timedelta(days=1)
    return (start, last), rest


class DateRange(unittest.TestCase):
    def test_today_and_yesterday(self):
        self.assertEqual(days("notes from today")[0], (TODAY, TODAY))
        self.assertEqual(days("what happened yesterday")[0], (dt.date(2026, 11, 22),) * 2)

    def test_weeks(self):
        self.assertEqual(days("this week")[0], (dt.date(2026, 11, 23), TODAY))
        self.assertEqual(days("last week")[0], (dt.date(2026, 11, 16), dt.date(2026, 11, 22)))

    def test_months(self):
        self.assertEqual(days("this month")[0], (dt.date(2026, 11, 1), TODAY))
        self.assertEqual(days("last month")[0], (dt.date(2026, 10, 1), dt.date(2026, 10, 31)))
        self.assertEqual(days("last month", dt.date(2027, 1, 10))[0], (dt.date(2026, 12, 1), dt.date(2026, 12, 31)))

    def test_last_n(self):
        self.assertEqual(days("last 10 days")[0], (dt.date(2026, 11, 13), TODAY))
        self.assertEqual(days("past 2 weeks")[0], (dt.date(2026, 11, 9), TODAY))

    def test_month_names(self):
        self.assertEqual(days("pitch in September")[0], (dt.date(2026, 9, 1), dt.date(2026, 9, 30)))
        self.assertEqual(days("in December")[0], (dt.date(2025, 12, 1), dt.date(2025, 12, 31)))
        self.assertEqual(days("May 2026 invoices")[0], (dt.date(2026, 5, 1), dt.date(2026, 5, 31)))
        self.assertEqual(days("during december 2026")[0], (dt.date(2026, 12, 1), dt.date(2026, 12, 31)))

    def test_plain_words_are_not_dates(self):
        self.assertEqual(days("I may need a march"), (None, "I may need a march"))
        self.assertEqual(days("cover drafts"), (None, "cover drafts"))

    def test_time_phrase_leaves_the_question(self):
        self.assertEqual(days("pitch drafts last week")[1], "pitch drafts")
        self.assertEqual(days("pitch in September")[1], "pitch")
        self.assertEqual(days("today")[1], "")


class DateBoost(unittest.TestCase):
    """Two notes with the same words. The one dated last month comes first only when the question says so."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        notes = Path(cls.tmp.name) / "notes"
        (notes / "Projects").mkdir(parents=True)
        (notes / "CLAUDE.md").write_text("Test notes.\n")  # the engine needs this file at the top
        today = dt.date.today()
        first = today.replace(day=1)
        last_month = (first - dt.timedelta(days=1)).replace(day=10)
        for name, when in (("old-plan", last_month), ("new-plan", today)):
            (notes / "Projects" / f"{name}.md").write_text(
                f"---\ndate: {when.isoformat()}\n---\n\n## Garden plan\n\nWhere the tomato beds go.\n")
        cls.env = dict(os.environ, ENGRAM_VAULT=str(notes), ENGRAM_DATA=str(Path(cls.tmp.name) / "data"))
        cls.run_cli("ingest")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @classmethod
    def run_cli(cls, *args):
        p = subprocess.run([sys.executable, str(ROOT / "engram.py"), *args], capture_output=True, text=True,
                           timeout=120, env=cls.env)
        if p.returncode:
            raise AssertionError(p.stderr)
        return p.stdout

    def first(self, q):
        return json.loads(self.run_cli("search", q, "--json"))[0]["path"]

    def test_newer_note_wins_without_a_date(self):
        self.assertEqual(self.first("tomato beds"), "Projects/new-plan.md")

    def test_dated_note_wins_with_a_date(self):
        self.assertEqual(self.first("tomato beds last month"), "Projects/old-plan.md")


if __name__ == "__main__":
    unittest.main()
