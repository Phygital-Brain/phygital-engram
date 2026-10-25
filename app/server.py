#!/usr/bin/env python3
"""Phygital Engram search page: a small page on your own computer. Ask a question, read your notes, check the index.

It listens only on 127.0.0.1, answers only requests addressed to itself, and never changes your notes."""
import json, os, sys, threading, time, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engram_lib import config, evaluate, health, ingest  # noqa: E402
from engram_lib.db import connect, schema_ok  # noqa: E402
from engram_lib.search import search, get, around  # noqa: E402

PORT = int(os.environ.get("ENGRAM_PAGE_PORT", "8787"))
HOST = "127.0.0.1"
MAX_QUERY_CHARS, MAX_QUERY_WORDS, MAX_RESULTS = 500, 20, 50

PAGE_HEADERS = {
    # Notes may hold clipped emails: no remote images (tracking pixels), no outside scripts, no framing.
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
                               "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; "
                               "form-action 'self'",
}
PAGE = (Path(__file__).parent / "index.html").read_text()
LOCK = threading.Lock()


def stats(cfg):
    if not cfg["db"].exists() or not schema_ok(cfg["db"]):
        return {"files": 0, "chunks": 0, "cards": 0, "last": None}
    con = connect(cfg["db"])
    q = lambda sql: con.execute(sql).fetchone()[0]
    last = con.execute("SELECT v FROM meta WHERE k='last_ingest'").fetchone()
    return {"files": q("SELECT COUNT(*) FROM files WHERE source='vault'"),
            "chunks": q("SELECT COUNT(*) FROM chunks"),
            "cards": q("SELECT COUNT(*) FROM cards WHERE model != 'fake'"),
            "last": float(last[0]) if last else None}


GENERIC = {"top", "log", "notes", "rules", "routing", "index", "overview", "summary", "links", "todo", "tasks",
           "status", "work log", "readme", "info", "details", "plan", "next", "done", "open", "files modified"}


def examples(cfg, n=6):
    """Example searches taken from real notes, different every time. Each one is tried first and kept only if it
    really finds its own note in the top 5, so a click always lands somewhere real. Main shelf only: never archives,
    copied code, hidden notes or private (finance) notes."""
    import random, re
    if not cfg["db"].exists() or not schema_ok(cfg["db"]):
        return []
    con = connect(cfg["db"])
    skip_types = tuple(cfg.get("type_weights", {})) or ("",)  # batches, logs, queues make poor examples
    rows = con.execute("SELECT c.heading, c.file_path FROM chunks c JOIN files f ON f.path = c.file_path "
                       "WHERE f.source='vault' AND f.shelf='main' AND f.hidden=0 "
                       "AND c.file_path NOT LIKE '%CLAUDE.md' "
                       f"AND lower(coalesce(c.type,'')) NOT IN ({','.join('?' * len(skip_types))}) "
                       "ORDER BY random() LIMIT 160", skip_types).fetchall()
    out, seen_q, seen_p = [], set(), set()
    for heading, path in rows:
        parts = [x.strip() for x in heading.split(" > ")]
        for cand in reversed(parts):  # the deepest heading first, then the note title
            q = re.sub(r"[`*_#\[\]()|:]", " ", cand)
            q = re.sub(r"[\u2014\u2013]", " ", q)                    # no em or en dashes
            q = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", q).replace("-", " ")
            q = re.sub(r"^\s*\d+[a-z]?[.)]?\s+", "", q)              # "4. Deep Signal", "7c. ..." -> no number
            q = " ".join(q.split())
            words = q.split()
            if not (2 <= len(words) <= 6) or len(q) > 48 or q.lower() in GENERIC or sum(c.isdigit() for c in q) > 4:
                continue
            if q.lower() in seen_q or path in seen_p:
                break
            hits = [r["path"] for r in search(cfg, q, 5, con=con, private=False)]
            if path in hits:
                out.append(q)
                seen_q.add(q.lower())
                seen_p.add(path)
            break
        if len(out) == n:
            break
    con.close()
    return out


# ---------- Files tab: read-only view of the vault ----------
# Password files, any capitals: shown locked, never opened.
import re  # noqa: E402
PASSWORD_FILE = re.compile(
    r"(^|/)(\.env(\.[^/]*)?|\.envrc|\.dev\.vars|\.npmrc|\.netrc|\.git-credentials|\.pgpass|"
    r"id_(rsa|ed25519|ecdsa)(\.pub)?|credentials|secrets|credentials\.(json|ya?ml|toml|txt)|"
    r"secrets?\.(json|ya?ml|toml|txt)|tokens?\.json|service-account[^/]*\.json)(/|$)|\.(key|pem|p12|pfx|keystore|jks)$",
    re.I)

IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
               ".webp": "image/webp", ".svg": "image/svg+xml"}
TEXT_EXT = {".md", ".markdown", ".txt", ".csv", ".json", ".yml", ".yaml", ".html", ".css", ".js", ".py", ".sh", ".toml"}


def vault_path(cfg, rel):
    """Resolve a path inside the vault: (full path, relative path, lock) or None.
    None for anything outside the vault (../, absolute paths, symlinks pointing out) and for hidden system folders.
    lock is "private" for the finance folders (shown, opened only on an explicit ask), "secret" for .claudeignore
    files such as .env and keys (shown so you know they exist, never opened), or None."""
    from engram_lib.ingest import read_ignore, is_ignored, is_private
    vault = cfg["vault"].resolve()
    rel = (rel or "").strip().lstrip("/")
    full = (vault / rel).resolve()
    if full != vault and vault not in full.parents:
        return None
    rel = "" if full == vault else str(full.relative_to(vault))
    parts = rel.split("/") if rel else []
    if any(p in cfg["skip_dirs"] for p in parts) or any(p.startswith(".") for p in parts[:-1]):
        return None  # system folders (.obsidian, .git, .context ...) are app files, not notes
    if not rel:
        return full, rel, None
    if is_private(rel, cfg) or is_private(rel + "/", cfg):
        return full, rel, "private"
    if is_ignored(rel, read_ignore(vault)) or PASSWORD_FILE.search(rel):
        return full, rel, "secret"
    if parts[-1].startswith("."):
        return None  # other hidden files (.DS_Store, .claudeignore ...) stay out
    return full, rel, None


def list_dir(cfg, rel):
    got = vault_path(cfg, rel)
    if not got or not got[0].is_dir() or got[2] == "secret":
        return None
    full, rel, lock = got
    out = []
    for e in os.scandir(full):
        child = f"{rel}/{e.name}" if rel else e.name
        g = vault_path(cfg, child)
        if not g:
            continue
        st = e.stat()
        out.append(dict(name=e.name, path=child, dir=e.is_dir(), size=st.st_size, mtime=st.st_mtime, lock=g[2]))
    out.sort(key=lambda x: (not x["dir"], x["name"].lower()))
    return out


def read_file(cfg, rel, allow_private=False):
    got = vault_path(cfg, rel)
    if not got or not got[0].is_file():
        return None
    full, rel, lock = got
    ext = full.suffix.lower()
    st = full.stat()
    base = dict(path=rel, full_path=str(Path(cfg["display_vault"]) / rel), size=st.st_size, mtime=st.st_mtime, lock=lock)
    if lock == "secret":
        return dict(base, kind="locked", note="Secret file (keys, passwords, tokens): its contents are never shown.")
    if lock == "private" and not allow_private:
        return dict(base, kind="locked", note="Private. Open it only when you need it.")
    if ext in IMAGE_TYPES:
        return dict(base, kind="image")
    if ext not in TEXT_EXT or st.st_size > 2_000_000:
        return dict(base, kind="binary")
    text = full.read_text(errors="replace")
    return dict(base, kind="md" if ext in (".md", ".markdown") else "text", text=text)


NOTE_INDEX = {"t": 0, "paths": []}


def note_index(cfg):
    """All visible note paths (for [[link]] clicks), refreshed at most every 30 seconds."""
    if time.time() - NOTE_INDEX["t"] > 30:
        paths = []
        vault = cfg["vault"]
        for root, dirs, files in os.walk(vault):
            rel_root = os.path.relpath(root, vault)
            rel_root = "" if rel_root == "." else rel_root
            dirs[:] = [d for d in dirs if (g := vault_path(cfg, f"{rel_root}/{d}" if rel_root else d)) and g[2] != "secret"]
            for f in files:
                rel = f"{rel_root}/{f}" if rel_root else f
                g = vault_path(cfg, rel)
                if f.lower().endswith(".md") and g and g[2] != "secret":
                    paths.append(rel)
        NOTE_INDEX.update(t=time.time(), paths=paths)
    return NOTE_INDEX["paths"]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, body, ctype="application/json", code=200):
        data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if ctype == "text/html":
            for k, v in PAGE_HEADERS.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def local_only(self):
        """Answer only requests addressed to this page's own address. A web page elsewhere could otherwise use a
        trick (DNS rebinding) to read your notes through this page."""
        host = (self.headers.get("Host") or "").lower()
        origin = (self.headers.get("Origin") or "").lower()
        ok_hosts = (f"127.0.0.1:{PORT}", f"localhost:{PORT}")
        # A page from another website may send requests here; the browser marks them with its Origin. Refuse them.
        if host not in ok_hosts or (origin and origin not in tuple("http://" + h for h in ok_hosts)):
            self.send({"error": "not allowed"}, code=403)
            return False
        return True

    def do_GET(self):
        if not self.local_only():
            return
        u = urlparse(self.path)
        p = {k: v[0] for k, v in parse_qs(u.query).items()}
        cfg = config.load()
        try:
            if u.path == "/":
                return self.send(PAGE, "text/html")
            if u.path == "/marked.min.js":  # Markdown library (marked v4.3.0, MIT), the same one the workspace uses
                return self.send((Path(__file__).parent / "marked.min.js").read_text(), "text/javascript")
            if u.path == "/api/files/list":
                r = list_dir(cfg, p.get("path", ""))
                return self.send({"entries": r} if r is not None else {"error": "not available"}, code=200 if r is not None else 404)
            if u.path == "/api/files/read":
                r = read_file(cfg, p.get("path", ""), allow_private=p.get("private") == "1")
                return self.send(r if r else {"error": "not available"}, code=200 if r else 404)
            if u.path == "/api/files/raw":  # images only, for showing them in the Files tab
                got = vault_path(cfg, p.get("path", ""))
                if (not got or got[2] or not got[0].is_file() or got[0].suffix.lower() not in IMAGE_TYPES
                        or got[0].stat().st_size > 15_000_000):
                    return self.send({"error": "not available"}, code=404)
                data = got[0].read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", IMAGE_TYPES[got[0].suffix.lower()])
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.end_headers()
                self.wfile.write(data)
                return
            if u.path == "/api/files/index":
                return self.send({"paths": note_index(cfg)})
            if u.path == "/api/examples":
                return self.send({"examples": examples(cfg)})
            if u.path == "/api/stats":
                s = stats(cfg)
                s["vault_name"] = Path(cfg["display_vault"]).name
                s["vault_path"] = cfg["display_vault"]
                return self.send(s)
            if u.path == "/api/search":
                smart = p.get("smart", "1") == "1"
                q = " ".join(p.get("q", "")[:MAX_QUERY_CHARS].split()[:MAX_QUERY_WORDS])
                n = min(max(int(p.get("n", 10)), 1), MAX_RESULTS)
                t = time.time()
                rows = search(cfg, q, n, recency=smart, weights=smart,
                              exact=smart, use_cards=smart, source=p.get("source") or None,
                              log=smart and p.get("log", "0") == "1", private=p.get("showprivate", "1") == "1")
                return self.send({"rows": rows, "ms": round((time.time() - t) * 1000)})
            if u.path == "/api/get":
                r = get(cfg, p.get("id", "0"), p.get("note") == "1", allow_private=p.get("private") == "1",
                        log=p.get("log", "0") == "1")
                return self.send(r or {"error": "not found"})
            if u.path == "/api/around":
                return self.send(around(cfg, p.get("id", "0")) or {"error": "nothing around this result"})
            if u.path == "/api/health":
                checks, problems = health.check(cfg)
                return self.send({"checks": checks, "ok": not problems})
            self.send({"error": "not found"}, code=404)
        except SystemExit as e:
            self.send({"error": str(e)}, code=400)
        except ValueError:
            self.send({"error": "bad request: a number was expected"}, code=400)
        except Exception as e:
            print(f"error: {type(e).__name__}: {e}", flush=True)
            self.send({"error": "Something went wrong on the server."}, code=500)

    def do_POST(self):
        if not self.local_only():
            return
        cfg = config.load()
        if not LOCK.acquire(blocking=False):
            return self.send({"error": "Busy with another job, try again in a moment."}, code=409)
        try:
            if self.path == "/api/ingest":
                s = ingest.run(cfg)
                return self.send(s)
            if self.path == "/api/test":
                return self.send(evaluate.run(cfg, verbose=False))
            self.send({"error": "not found"}, code=404)
        except SystemExit as e:
            self.send({"error": str(e)}, code=400)
        except Exception as e:
            print(f"error: {type(e).__name__}: {e}", flush=True)
            self.send({"error": "Something went wrong on the server."}, code=500)
        finally:
            LOCK.release()


def main():
    try:
        srv = ThreadingHTTPServer((HOST, PORT), Handler)
    except OSError:
        print(f"Already running. Opening http://127.0.0.1:{PORT}")
        webbrowser.open(f"http://127.0.0.1:{PORT}")
        return
    url = f"http://127.0.0.1:{PORT}"
    print(f"Phygital Engram is running at {url}\nPress Control+C to stop it.")
    if not os.environ.get("ENGRAM_NO_BROWSER"):
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
