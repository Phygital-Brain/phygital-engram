"""Secret blanking with the default config.json patterns. Every key below is made up."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engram_lib.ingest import make_redactor  # noqa: E402

FAKE = "abcdefghijklmnopqrstuvwx1234"


class Redact(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.redact = staticmethod(make_redactor(json.loads((ROOT / "config.json").read_text())))

    def test_secret_forms_are_blanked(self):
        for text in (f"API_KEY = {FAKE}", f'{{"api_key": "{FAKE}"}}', f"X-API-Key: {FAKE}",
                     f"-----BEGIN RSA PRIVATE KEY-----\n{FAKE}\n-----END RSA PRIVATE KEY-----",
                     f"-----BEGIN PGP PRIVATE KEY BLOCK-----\n{FAKE}\n-----END PGP PRIVATE KEY BLOCK-----"):
            self.assertNotIn(FAKE, self.redact(text), text)

    def test_plain_words_stay(self):
        text = "A token of thanks. The password reset email came."
        self.assertEqual(self.redact(text), text)


if __name__ == "__main__":
    unittest.main()
