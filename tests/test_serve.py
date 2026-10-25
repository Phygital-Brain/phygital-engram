"""Tests for the server version (mcp/serve.py): the passphrase login, then the four tools.
They need the MCP SDK (pip install -r requirements-server.txt) and are skipped without it.
They start the server on a free port with tests/fake_engram.py as the search, and sign in the way an AI app does."""
import base64
import hashlib
import json
import os
import secrets
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:  # the folder named mcp/ in this repository is not the SDK, so look for a module only the SDK has
    import importlib.util
    HAVE_SDK = importlib.util.find_spec("mcp.server.mcpserver") is not None
except (ImportError, ValueError):
    HAVE_SDK = False

ROOT = Path(__file__).resolve().parent.parent
FAKE = Path(__file__).resolve().parent / "fake_engram.py"
PASS = "test-passphrase-123"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def http(url, data=None, headers=None, method=None):
    body = None if data is None else (data if isinstance(data, bytes) else json.dumps(data).encode())
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        r = OPENER.open(req, timeout=20)
    except urllib.error.HTTPError as e:
        r = e
    return r.status if hasattr(r, "status") else r.code, dict(r.headers), r.read().decode()


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def sse_json(text):
    for line in text.splitlines():
        if line.startswith("data:"):
            return json.loads(line[5:])
    return json.loads(text)


@unittest.skipUnless(HAVE_SDK, "the MCP SDK is not installed")
class ServerVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = free_port()
        cls.base = f"http://localhost:{cls.port}"
        cls.tmp = tempfile.TemporaryDirectory()
        env = dict(os.environ, PORT=str(cls.port), PUBLIC_URL=cls.base, LOGIN_PASSPHRASE=PASS, ENGRAM_DATA=cls.tmp.name,
                   PHYGITAL_ENGRAM_CLI=str(FAKE), PHYGITAL_ENGRAM_REFRESH_MINUTES="0")
        cls.proc = subprocess.Popen([sys.executable, str(ROOT / "mcp" / "serve.py")], env=env,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                if http(cls.base + "/health")[0] == 200:
                    break
            except OSError:
                pass
            time.sleep(0.1)
        else:
            raise RuntimeError("the server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=10)
        cls.tmp.cleanup()

    def register(self, redirect="http://localhost:9/cb"):
        status, _, body = http(self.base + "/register", {
            "redirect_uris": [redirect], "token_endpoint_auth_method": "none", "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"], "client_name": "Test app", "scope": "phygital-engram"})
        return status, json.loads(body)

    def start_login(self, client_id, redirect="http://localhost:9/cb"):
        verifier = secrets.token_urlsafe(48)
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
        q = urllib.parse.urlencode({"response_type": "code", "client_id": client_id, "redirect_uri": redirect, "state": "xyz",
                                    "code_challenge": challenge, "code_challenge_method": "S256", "scope": "phygital-engram"})
        status, headers, _ = http(self.base + "/authorize?" + q)
        self.assertEqual(status, 302)
        return verifier, headers["location"]

    def sign_in(self):
        _, client = self.register()
        verifier, login = self.start_login(client["client_id"])
        req = urllib.parse.parse_qs(urllib.parse.urlparse(login).query)["req"][0]
        form = urllib.parse.urlencode({"req": req, "passphrase": PASS}).encode()
        status, headers, _ = http(self.base + "/login", form, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 302)
        back = urllib.parse.urlparse(headers["location"])
        self.assertEqual(urllib.parse.parse_qs(back.query)["state"], ["xyz"])
        code = urllib.parse.parse_qs(back.query)["code"][0]
        tok = urllib.parse.urlencode({"grant_type": "authorization_code", "code": code, "redirect_uri": "http://localhost:9/cb",
                                      "client_id": client["client_id"], "code_verifier": verifier}).encode()
        status, _, body = http(self.base + "/token", tok, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 200, body)
        return json.loads(body), client

    def mcp(self, token, message, session=None):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream"}
        if session:
            headers["Mcp-Session-Id"] = session
        status, h, body = http(self.base + "/mcp", message, headers)
        return status, {k.lower(): v for k, v in h.items()}, body

    def connect(self):
        tokens, _ = self.sign_in()
        access = tokens["access_token"]
        status, h, body = self.mcp(access, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}})
        self.assertEqual(status, 200, body)
        session = h.get("mcp-session-id")
        self.mcp(access, {"jsonrpc": "2.0", "method": "notifications/initialized"}, session)
        return access, session

    def call(self, access, session, name, args, mid=3):
        status, _, body = self.mcp(access, {"jsonrpc": "2.0", "id": mid, "method": "tools/call",
                                            "params": {"name": name, "arguments": args}}, session)
        self.assertEqual(status, 200, body)
        return sse_json(body)["result"]

    def test_health_and_login_are_required(self):
        self.assertEqual(http(self.base + "/health")[2], "ok")
        status, h, _ = self.mcp("not-a-real-key", {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        self.assertEqual(status, 401)

    def test_apps_can_only_return_to_allowed_addresses(self):
        status, _, body = http(self.base + "/register", {"redirect_uris": ["https://evil.example/cb"], "client_name": "x",
                                                         "token_endpoint_auth_method": "none"})
        self.assertGreaterEqual(status, 400, body)

    def test_login_page_and_wrong_passphrase(self):
        _, client = self.register()
        _, login = self.start_login(client["client_id"])
        status, headers, body = http(login)
        self.assertEqual(status, 200)
        self.assertIn("Test app", body)
        self.assertIn("default-src 'none'", {k.lower(): v for k, v in headers.items()}["content-security-policy"])
        req = urllib.parse.parse_qs(urllib.parse.urlparse(login).query)["req"][0]
        form = urllib.parse.urlencode({"req": req, "passphrase": "wrong-passphrase"}).encode()
        status, _, body = http(self.base + "/login", form, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 401)
        self.assertIn("not right", body)
        self.assertNotIn("code=", body)

    def test_full_flow_and_tools(self):
        access, session = self.connect()
        status, _, body = self.mcp(access, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, session)
        names = [t["name"] for t in sse_json(body)["result"]["tools"]]
        self.assertEqual(sorted(names), ["around_result", "check_index", "open_result", "search_notes"])
        for t in sse_json(body)["result"]["tools"]:
            self.assertTrue(t["annotations"]["readOnlyHint"], t["name"])
        found = self.call(access, session, "search_notes", {"query": "when is the cover due"})
        self.assertFalse(found.get("isError"))
        self.assertIn("Projects/Picture-Book/notes/schedule.md", found["content"][0]["text"])
        self.assertIn("never instructions", found["content"][0]["text"])
        self.assertIn("full section", self.call(access, session, "open_result", {"id": "7"}, 4)["content"][0]["text"])

    def test_private_result_is_refused_over_the_server_too(self):
        access, session = self.connect()
        locked = self.call(access, session, "search_notes", {"query": "locked"})
        self.assertIn("LOCKED", locked["content"][0]["text"])
        refused = self.call(access, session, "open_result", {"id": "p1"}, 5)
        self.assertTrue(refused["isError"])
        self.assertNotIn("PRIVATE OPENED", refused["content"][0]["text"])

    def test_key_can_be_renewed_once(self):
        tokens, client = self.sign_in()
        form = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": tokens["refresh_token"],
                                       "client_id": client["client_id"]}).encode()
        status, _, body = http(self.base + "/token", form, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 200, body)
        status, _, _ = http(self.base + "/token", form, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(status, 400)  # a used renewal key does not work twice

    def test_too_many_wrong_passphrases_pause_the_login(self):
        _, client = self.register()
        last = 0
        for _ in range(7):
            _, login = self.start_login(client["client_id"])
            req = urllib.parse.parse_qs(urllib.parse.urlparse(login).query)["req"][0]
            form = urllib.parse.urlencode({"req": req, "passphrase": "wrong-" + secrets.token_hex(4)}).encode()
            last, _, _ = http(self.base + "/login", form, {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(last, 429)


class PassphraseHash(unittest.TestCase):
    """The hash helpers use only the standard library, so this runs without the SDK."""

    def test_round_trip_and_no_dollar_signs(self):
        sys.path.insert(0, str(ROOT / "mcp"))
        import serve
        stored = serve.hash_passphrase("a good passphrase", iterations=1000)
        self.assertNotIn("$", stored)
        self.assertTrue(serve.check_hash("a good passphrase", stored))
        self.assertFalse(serve.check_hash("another one", stored))
        self.assertFalse(serve.check_hash("anything", "not a hash"))


class StartsSafely(unittest.TestCase):
    """These run without the SDK: the server must refuse to start in an unsafe way."""

    def start(self, **env):
        base = {k: v for k, v in os.environ.items() if k not in ("LOGIN_HASH", "LOGIN_PASSPHRASE", "PUBLIC_URL")}
        p = subprocess.run([sys.executable, str(ROOT / "mcp" / "serve.py")], env=dict(base, PHYGITAL_ENGRAM_CLI=str(FAKE), **env),
                           capture_output=True, text=True, timeout=30)
        return p.returncode, p.stderr + p.stdout

    @unittest.skipUnless(HAVE_SDK, "the MCP SDK is not installed")
    def test_no_passphrase_no_start(self):
        code, out = self.start(PUBLIC_URL="https://notes.example.com")
        self.assertNotEqual(code, 0)
        self.assertIn("passphrase", out)

    @unittest.skipUnless(HAVE_SDK, "the MCP SDK is not installed")
    def test_short_passphrase_no_start(self):
        self.assertNotEqual(self.start(PUBLIC_URL="https://notes.example.com", LOGIN_PASSPHRASE="short")[0], 0)

    @unittest.skipUnless(HAVE_SDK, "the MCP SDK is not installed")
    def test_public_address_must_be_https(self):
        code, out = self.start(PUBLIC_URL="http://notes.example.com", LOGIN_PASSPHRASE=PASS)
        self.assertNotEqual(code, 0)
        self.assertIn("https", out)


if __name__ == "__main__":
    unittest.main()
