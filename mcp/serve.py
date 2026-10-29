#!/usr/bin/env python3
"""Phygital Engram, server version. Lets AI apps on your phone, the web and your computer search your notes
through one address, over HTTPS, behind a passphrase login.

It gives the same four read-only tools as the computer version (server.py) and runs the same search program.
The difference is the front door: AI apps sign in with OAuth. You type your passphrase once, on a page of your
own server, and the app gets a key that expires after an hour and renews itself.

Commands:
  python3 mcp/serve.py              start the server
  python3 mcp/serve.py hash         ask for a passphrase and print LOGIN_HASH=... for your settings

Settings (environment variables):
  PUBLIC_URL                         where the server is reached, like https://notes.example.com (https required)
  LOGIN_HASH or LOGIN_PASSPHRASE     the passphrase, 8+ characters. Prefer LOGIN_HASH
  HOST, PORT                         where to listen (default 127.0.0.1 and 8765)
  PHYGITAL_ENGRAM_REFRESH_MINUTES    how often to update the index (default 10, 0 = never)
  PHYGITAL_ENGRAM_TRUST_PROXY        1 when a proxy like Caddy sits in front (reads the visitor's address from it)
  ALLOWED_REDIRECT_HOSTS             AI apps allowed to log in (default: claude.ai, claude.com, chatgpt.com, openai.com, vscode.dev)
  ENGRAM_VAULT, ENGRAM_DATA          your notes and the index folder, read by the search program
"""
import asyncio
import base64
import getpass
import hashlib
import hmac
import html
import json
import logging
import os
import secrets
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Annotated
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import server as local  # the computer version: tools, instructions and the call into the search program

MIN_PASSPHRASE = 8
SCOPE = "phygital-engram"
DEFAULT_REDIRECT_HOSTS = "claude.ai,claude.com,chatgpt.com,openai.com,vscode.dev"
FAIL_WINDOW, FAIL_LIMIT, FAIL_LIMIT_ALL = 15 * 60, 5, 50
ACCESS_TTL, REFRESH_TTL, MAX_CLIENTS, MAX_FORM = 3600, 90 * 24 * 3600, 50, 4096
DATA = Path(os.environ.get("ENGRAM_DATA") or Path.home() / ".local" / "share" / "phygital-engram").expanduser()
OAUTH_FILE = DATA / "oauth.json"
PAGE_HEADERS = {
    "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
    "X-Frame-Options": "DENY", "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer",
    "Cache-Control": "no-store", "Content-Type": "text/html; charset=utf-8",
}


# ---------- passphrase ----------

def hash_passphrase(passphrase: str, iterations: int = 600_000) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, iterations)
    return f"pbkdf2:{iterations}:{base64.b64encode(salt).decode()}:{base64.b64encode(digest).decode()}"


def check_hash(passphrase: str, stored: str) -> bool:
    try:
        _, iters, salt, digest = stored.split(":")
        got = hashlib.pbkdf2_hmac("sha256", passphrase.encode(), base64.b64decode(salt), int(iters))
        return hmac.compare_digest(got, base64.b64decode(digest))
    except (ValueError, TypeError):
        return False


def passphrase_ok(passphrase: str) -> bool:
    stored = os.environ.get("LOGIN_HASH", "")
    if stored:
        return check_hash(passphrase, stored)
    plain = os.environ.get("LOGIN_PASSPHRASE", "")
    return bool(plain) and hmac.compare_digest(passphrase.encode(), plain.encode())


def fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def private_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(text)
    os.replace(tmp, path)


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return default


# ---------- the AI app login (OAuth) ----------

class Lockout:
    """Five wrong passphrases from one address in 15 minutes pause that address. Fifty from anywhere pause all."""

    def __init__(self):
        self.failures: list[tuple[float, str]] = []

    def locked(self, ip: str) -> bool:
        cutoff = time.time() - FAIL_WINDOW
        self.failures = [f for f in self.failures if f[0] > cutoff]
        return len(self.failures) >= FAIL_LIMIT_ALL or sum(1 for _, who in self.failures if who == ip) >= FAIL_LIMIT

    def failed(self, ip: str) -> None:
        self.failures.append((time.time(), ip))


def build_provider(public: str, redirect_hosts: list[str], lockout: Lockout):
    from mcp.server.auth.provider import (AccessToken, AuthorizationCode, AuthorizationParams, AuthorizeError,
                                          RefreshToken, RegistrationError, TokenError, construct_redirect_uri)
    from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

    class Provider:
        def __init__(self):
            self.lock = threading.Lock()
            self.pending: dict[str, tuple[float, str, AuthorizationParams]] = {}
            self.codes: dict[str, AuthorizationCode] = {}
            data = read_json(OAUTH_FILE, {})
            self.clients = {k: OAuthClientInformationFull.model_validate(v) for k, v in data.get("clients", {}).items()}
            self.access = {k: AccessToken.model_validate(v) for k, v in data.get("access", {}).items()}
            self.refresh = {k: RefreshToken.model_validate(v) for k, v in data.get("refresh", {}).items()}

        def save(self) -> None:
            now = time.time()
            self.access = {k: v for k, v in self.access.items() if not v.expires_at or v.expires_at > now}
            self.refresh = {k: v for k, v in self.refresh.items() if not v.expires_at or v.expires_at > now}
            private_write(OAUTH_FILE, json.dumps({
                "clients": {k: v.model_dump(mode="json") for k, v in self.clients.items()},
                "access": {k: v.model_dump(mode="json") for k, v in self.access.items()},
                "refresh": {k: v.model_dump(mode="json") for k, v in self.refresh.items()},
            }, indent=1))

        def redirect_ok(self, uri) -> bool:
            p = urlparse(str(uri))
            host = (p.hostname or "").lower()
            if host in ("localhost", "127.0.0.1", "::1"):
                return p.scheme in ("http", "https")
            return p.scheme == "https" and any(host == h or host.endswith("." + h) for h in redirect_hosts)

        async def get_client(self, client_id: str):
            return self.clients.get(client_id)

        async def register_client(self, client_info) -> None:
            bad = [str(u) for u in (client_info.redirect_uris or []) if not self.redirect_ok(u)]
            if bad:
                raise RegistrationError("invalid_redirect_uri", f"Redirect not allowed: {', '.join(bad)}")
            with self.lock:
                cutoff = time.time() - 3600  # an app that registered but never logged in is forgotten after an hour
                signed_in = {t.client_id for t in self.access.values()} | {t.client_id for t in self.refresh.values()}
                for cid in [c for c, v in self.clients.items() if (v.client_id_issued_at or 0) < cutoff and c not in signed_in]:
                    del self.clients[cid]
                while len(self.clients) >= MAX_CLIENTS:
                    del self.clients[min(self.clients, key=lambda k: self.clients[k].client_id_issued_at or 0)]
                self.clients[client_info.client_id] = client_info
                self.save()

        async def authorize(self, client, params) -> str:
            if not self.redirect_ok(params.redirect_uri):
                raise AuthorizeError("invalid_request", "Redirect not allowed")
            req = secrets.token_urlsafe(24)
            with self.lock:
                self.pending = {k: v for k, v in self.pending.items() if v[0] > time.time()}
                while len(self.pending) >= 500:  # waiting logins are capped, so nobody can fill the memory
                    del self.pending[min(self.pending, key=lambda k: self.pending[k][0])]
                self.pending[req] = (time.time() + 600, client.client_id, params)
            return f"{public}/login?req={req}"

        def describe(self, req: str):
            entry = self.pending.get(req)
            if not entry or entry[0] < time.time():
                return None
            client = self.clients.get(entry[1])
            name = " ".join((client.client_name if client else "").split())[:80] or "An AI app"
            return name, urlparse(str(entry[2].redirect_uri)).hostname or "?"

        def complete_login(self, req: str, passphrase: str, ip: str):
            """The address to send the person back to on success, None on a wrong passphrase."""
            with self.lock:
                if lockout.locked(ip):
                    raise PermissionError("Too many wrong tries. Wait 15 minutes.")
                entry = self.pending.get(req)
                if not entry or entry[0] < time.time():
                    raise LookupError("This login link has expired. Start the connection again in your AI app.")
                if not passphrase_ok(passphrase):
                    lockout.failed(ip)
                    return None
                del self.pending[req]
                _, client_id, params = entry
                code = secrets.token_urlsafe(32)
                self.codes[code] = AuthorizationCode(
                    code=code, scopes=params.scopes or [SCOPE], expires_at=time.time() + 300, client_id=client_id,
                    code_challenge=params.code_challenge, redirect_uri=params.redirect_uri,
                    redirect_uri_provided_explicitly=params.redirect_uri_provided_explicitly,
                    resource=params.resource, subject="owner")
            return construct_redirect_uri(str(params.redirect_uri), code=code, state=params.state)

        async def load_authorization_code(self, client, authorization_code: str):
            code = self.codes.get(authorization_code)
            if code and code.client_id == client.client_id and code.expires_at > time.time():
                return code
            return None

        def issue(self, client_id: str, scopes, resource):
            now = int(time.time())
            access, refresh = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            a_key, r_key = fingerprint(access), fingerprint(refresh)
            self.access[a_key] = AccessToken(token=a_key, client_id=client_id, scopes=scopes, expires_at=now + ACCESS_TTL,
                                             resource=resource, subject="owner")
            self.refresh[r_key] = RefreshToken(token=r_key, client_id=client_id, scopes=scopes, expires_at=now + REFRESH_TTL,
                                               resource=resource, subject="owner")
            self.save()
            return OAuthToken(access_token=access, token_type="Bearer", expires_in=ACCESS_TTL, refresh_token=refresh,
                              scope=" ".join(scopes))

        async def exchange_authorization_code(self, client, authorization_code):
            with self.lock:
                if self.codes.pop(authorization_code.code, None) is None:
                    raise TokenError("invalid_grant", "Code already used")
                return self.issue(client.client_id, authorization_code.scopes, authorization_code.resource)

        async def load_refresh_token(self, client, refresh_token: str):
            tok = self.refresh.get(fingerprint(refresh_token))
            if tok and tok.client_id == client.client_id and (not tok.expires_at or tok.expires_at > time.time()):
                return tok.model_copy(update={"token": refresh_token})
            return None

        async def exchange_refresh_token(self, client, refresh_token, scopes):
            with self.lock:
                if self.refresh.pop(fingerprint(refresh_token.token), None) is None:
                    raise TokenError("invalid_grant", "Refresh token already used")
                return self.issue(client.client_id, scopes or refresh_token.scopes, refresh_token.resource)

        async def load_access_token(self, token: str):
            tok = self.access.get(fingerprint(token))
            if tok and (not tok.expires_at or tok.expires_at > time.time()) and self.for_us(tok.resource):
                return tok.model_copy(update={"token": token})
            return None

        def for_us(self, resource) -> bool:
            if not resource:
                return True
            r = str(resource).rstrip("/").lower()
            return r in (public.lower(), f"{public.lower()}/mcp")

        async def revoke_token(self, token) -> None:
            with self.lock:
                self.access = {k: v for k, v in self.access.items() if v.client_id != token.client_id}
                self.refresh = {k: v for k, v in self.refresh.items() if v.client_id != token.client_id}
                self.save()

    return Provider()


# ---------- the login page ----------

def page(body: str, status_title: str = "Phygital Engram") -> str:
    return ("<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(status_title)}</title><style>body{{font:18px/1.5 system-ui,sans-serif;margin:0;background:#0B0D12;color:#F1EDE4}}"
            "main{max-width:26rem;margin:12vh auto;padding:0 1.25rem}h1{font-size:1.4rem}.card{background:#161A22;border:1px solid #2A303C;"
            "border-radius:10px;padding:1.5rem}input{width:100%;box-sizing:border-box;font:inherit;padding:.7rem;margin:.5rem 0 1rem;"
            "background:#07080C;color:inherit;border:1px solid #2A303C;border-radius:6px}button{font:inherit;font-weight:700;padding:.7rem 1.2rem;"
            "background:#FFD60A;color:#0B0D12;border:0;border-radius:6px}.err{color:#ff9d8f}.m{color:#A7A39A;font-size:.9rem}</style></head>"
            f"<body><main>{body}</main></body></html>")


def login_page(app: str, back: str, req: str, error: str = "") -> str:
    err = f"<p class=err role=alert>{html.escape(error)}</p>" if error else ""
    return page(
        f"<div class=card><h1>Phygital Engram</h1><p><b>{html.escape(app)}</b> wants to search your notes. It can read them and cannot change them.</p>"
        f"{err}<form method=post action=/login><input type=hidden name=req value='{html.escape(req)}'>"
        "<label>Your passphrase<input type=password name=passphrase autocomplete=current-password autofocus required></label>"
        f"<button>Allow</button></form><p class=m>After you allow, you go back to {html.escape(back)}.</p></div>")


# ---------- the server ----------

_provider = None


def client_ip(request) -> str:
    if os.environ.get("PHYGITAL_ENGRAM_TRUST_PROXY") == "1":
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[-1].strip()[:64]
    return (request.client.host if request.client else "")[:64]


def build_server(public: str):
    from pydantic import Field
    from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
    from mcp_types import ToolAnnotations
    from starlette.requests import Request
    from starlette.responses import RedirectResponse, Response

    global _provider
    hosts = [h.strip() for h in (os.environ.get("ALLOWED_REDIRECT_HOSTS") or DEFAULT_REDIRECT_HOSTS).split(",") if h.strip()]
    lockout = Lockout()
    provider = _provider = build_provider(public, [h.lower() for h in hosts], lockout)
    server = MCPServer(
        "phygital-engram", instructions=local.INSTRUCTIONS, title="Phygital Engram", version=local.VERSION,
        auth_server_provider=provider,
        auth=AuthSettings(
            issuer_url=public, resource_server_url=f"{public}/mcp", validate_token_resource=False,
            client_registration_options=ClientRegistrationOptions(enabled=True, valid_scopes=[SCOPE], default_scopes=[SCOPE]),
            revocation_options=RevocationOptions(enabled=True), required_scopes=[SCOPE]),
    )
    read = ToolAnnotations(read_only_hint=True, destructive_hint=False, idempotent_hint=True, open_world_hint=False)

    async def run(name: str, args: dict) -> str:
        ok, text = await asyncio.to_thread(local.call, name, args)
        if not ok:
            raise ToolError(text)
        return text

    descriptions = {t["name"]: t["description"] for t in local.TOOLS}

    @server.tool(name="search_notes", title="Search notes", description=descriptions["search_notes"], annotations=read)
    async def search_notes(
        query: Annotated[str, Field(description="The question, in plain words (up to 500 characters)")],
        limit: Annotated[int, Field(ge=1, le=20, description="How many results (default 8)")] = 8,
        folder: Annotated[str, Field(description="Optional: only search inside this folder of the notes, like \"Projects/decisions\"")] = "",
    ) -> str:
        return await run("search_notes", {"query": query, "limit": limit, "folder": folder})

    @server.tool(name="open_result", title="Open a result", description=descriptions["open_result"], annotations=read)
    async def open_result(id: Annotated[str, Field(description="A result id from search_notes")]) -> str:
        return await run("open_result", {"id": id})

    @server.tool(name="around_result", title="See what is around a result", description=descriptions["around_result"], annotations=read)
    async def around_result(id: Annotated[str, Field(description="A result id from search_notes")]) -> str:
        return await run("around_result", {"id": id})

    @server.tool(name="check_index", title="Check the index", description=descriptions["check_index"], annotations=read)
    async def check_index() -> str:
        return await run("check_index", {})

    own = {urlparse(public).hostname or "", "127.0.0.1", "localhost"}

    @server.custom_route("/login", methods=["GET", "POST"])
    async def login(request: Request) -> Response:
        if (request.url.hostname or "") not in own:
            return Response("Wrong address.", status_code=421, headers=PAGE_HEADERS)
        if request.method == "GET":
            req = request.query_params.get("req", "")
            info = provider.describe(req)
            if not info:
                return Response(page("<div class=card><p>This login link has expired. Start the connection again in your AI app.</p></div>"),
                                status_code=410, headers=PAGE_HEADERS)
            return Response(login_page(info[0], info[1], req), headers=PAGE_HEADERS)
        body = await request.body()
        if len(body) > MAX_FORM:
            return Response("Too large.", status_code=413)
        form = {k: v[0] for k, v in parse_qs(body.decode("utf-8", "replace"), keep_blank_values=True).items()}
        req = form.get("req", "")
        info = provider.describe(req)
        try:
            back = await asyncio.to_thread(provider.complete_login, req, form.get("passphrase", ""), client_ip(request))
        except PermissionError as e:
            return Response(login_page(*(info or ("An AI app", "it")), req, str(e)), status_code=429, headers=PAGE_HEADERS)
        except LookupError as e:
            return Response(page(f"<div class=card><p>{html.escape(str(e))}</p></div>"), status_code=410, headers=PAGE_HEADERS)
        if back is None:
            return Response(login_page(*(info or ("An AI app", "it")), req, "That passphrase is not right."),
                            status_code=401, headers=PAGE_HEADERS)
        return RedirectResponse(back, status_code=302, headers={"Cache-Control": "no-store", "Referrer-Policy": "no-referrer"})

    @server.custom_route("/health", methods=["GET"])
    async def health(request: Request) -> Response:
        return Response("ok")

    return server


def refresh_loop(minutes: int) -> None:
    """Keep the index fresh: run the search program's ingest now and then. Only reads the notes."""
    cli = local.CLI
    while True:
        try:
            subprocess.run([sys.executable, str(cli), "ingest"], capture_output=True, timeout=1800, cwd=str(cli.parent))
        except Exception as e:  # a failed refresh must never stop the server
            print(f"Index refresh failed: {type(e).__name__}", file=sys.stderr)
        time.sleep(minutes * 60)


def serve() -> None:
    public = (os.environ.get("PUBLIC_URL") or f"http://localhost:{os.environ.get('PORT') or 8765}").rstrip("/")
    host = urlparse(public).hostname or "localhost"
    if not os.environ.get("LOGIN_HASH") and len(os.environ.get("LOGIN_PASSPHRASE", "")) < MIN_PASSPHRASE:
        sys.exit(f"Set a passphrase first: LOGIN_HASH (run: python3 mcp/serve.py hash) or LOGIN_PASSPHRASE ({MIN_PASSPHRASE}+ characters).")
    if not public.startswith("https://") and host not in ("localhost", "127.0.0.1"):
        sys.exit("PUBLIC_URL must start with https:// . Your passphrase is typed on this server's login page.")
    if public.startswith("http://"):
        print(f"Note: PUBLIC_URL is not an https address, so only this computer can use it ({public}).", file=sys.stderr)
    if not local.CLI.exists():
        sys.exit(f"The search program was not found: {local.CLI}. Set PHYGITAL_ENGRAM_CLI or put engram.py next to the mcp folder.")
    minutes = int(os.environ.get("PHYGITAL_ENGRAM_REFRESH_MINUTES", "10") or 0)
    if minutes > 0:
        threading.Thread(target=refresh_loop, args=(minutes,), daemon=True).start()
    from mcp.server.transport_security import TransportSecuritySettings
    server = build_server(public)
    print(f"AI apps connect to: {public}/mcp", file=sys.stderr)
    logging.getLogger("uvicorn.access").addFilter(lambda r: "req=" not in r.getMessage() and "code=" not in r.getMessage())
    server.run(
        "streamable-http", host=os.environ.get("HOST") or "127.0.0.1", port=int(os.environ.get("PORT") or 8765),
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[host, f"{host}:*", "127.0.0.1:*", "localhost:*"],
            allowed_origins=[f"https://{host}", "https://claude.ai", "https://claude.com", "https://chatgpt.com",
                             "https://openai.com", "https://vscode.dev", "http://localhost:*", "http://127.0.0.1:*"]))


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if cmd == "hash":
        first = getpass.getpass("New passphrase: ")
        if len(first) < MIN_PASSPHRASE:
            sys.exit(f"Too short: at least {MIN_PASSPHRASE} characters.")
        if getpass.getpass("Again: ") != first:
            sys.exit("The two do not match.")
        print(f"LOGIN_HASH={hash_passphrase(first)}")
    elif cmd == "serve":
        serve()
    else:
        print((__doc__ or "").strip())
        sys.exit(0 if cmd in ("help", "-h", "--help") else f"Unknown command {cmd!r}.")


if __name__ == "__main__":
    main()
