#!/usr/bin/env python3
"""Phygital Engram: a fast search for a folder of Markdown notes. Reads the notes, never writes to them.

  python3 engram.py ingest [--rebuild]       build or update the index
  python3 engram.py search "question"        short ranked results [-n 10] [--json] [--source vault|chat] [--plain]
                                             [--folder Projects/decisions]
  python3 engram.py get ID [--note]          full section (or whole note) for a result ID
  python3 engram.py get pID --private        open a private (finances) result, only when the person asked
  python3 engram.py around ID                the sections before and after a result, and notes from the same day
  python3 engram.py usage                    how much real use has been counted (learning from use)
  python3 engram.py cards [--limit N] [--fake] [--estimate] [--import FILE]   Haiku note cards
  python3 engram.py test                     score tests/questions.json and tests/holdout.json
  python3 engram.py health                   per-source check; exit code 1 means a problem
  python3 engram.py stats                    what is in the index
  python3 engram.py page                     open the search page in your browser (only on this computer)
"""
import argparse, json, sys, time

from engram_lib import cards, config, evaluate, health, ingest
from engram_lib.db import connect
from engram_lib.search import search, get, around
from engram_lib import usage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("ingest"); p.add_argument("--rebuild", action="store_true")
    p = sub.add_parser("search"); p.add_argument("question"); p.add_argument("-n", type=int)
    p.add_argument("--json", action="store_true"); p.add_argument("--source")
    p.add_argument("--plain", action="store_true", help="words only: no recency, weights, exact or cards")
    p.add_argument("--folder", help="only notes inside this folder, like Projects/decisions")
    p = sub.add_parser("get"); p.add_argument("id"); p.add_argument("--note", action="store_true")
    p.add_argument("--private", action="store_true", help="open a private (p...) result; only when the person asked")
    p = sub.add_parser("cards"); p.add_argument("--limit", type=int); p.add_argument("--fake", action="store_true")
    p.add_argument("--estimate", action="store_true")
    p.add_argument("--import", dest="import_file", metavar="FILE", help="load cards from a cards file")
    p = sub.add_parser("around"); p.add_argument("id")
    sub.add_parser("test"); sub.add_parser("health"); sub.add_parser("stats"); sub.add_parser("usage"); sub.add_parser("page")
    a = ap.parse_args()
    cfg = config.load()

    if a.cmd == "ingest":
        s = ingest.run(cfg, rebuild=a.rebuild)
        print(("REBUILT. " if s["rebuilt"] else "") +
              f"indexed {s['indexed']}, unchanged {s['unchanged']}, removed {s['removed']}, hidden {s['hidden']}, "
              f"ignored {s['ignored']} | total {s['files']} files, "
              f"{s['chunks']} sections | {s['seconds']}s")
        for e in s["errors"][:10]:
            print("  warning:", e)
    elif a.cmd == "search":
        t = time.time()
        opts = dict(recency=False, weights=False, exact=False, use_cards=False) if a.plain else {}
        rows = search(cfg, a.question, a.n, source=a.source, log=not a.plain, folder=a.folder, **opts)
        for r in rows:
            r["snippet"] = r["snippet"].replace("\x02", "[").replace("\x03", "]")
        if a.json:
            print(json.dumps(rows, indent=2))
        else:
            for r in rows:
                tag = (" EXACT" if r["exact"] else "") + (" LOCKED" if r.get("private") else "")
                print(f"#{r['id']:<6} [{r['source']}{tag}] {r['path']}\n        {r['heading']}\n        {r['snippet'][:220]}"
                      + (f"\n        why: {r['why']}" if r.get("why") else ""))
            print(f"({(time.time() - t) * 1000:.0f} ms)  Full text: python3 engram.py get ID")
    elif a.cmd == "get":
        r = get(cfg, a.id, a.note, allow_private=a.private, log=True)
        print(json.dumps(r, indent=2) if r else "not found")
    elif a.cmd == "around":
        r = around(cfg, a.id)
        print(json.dumps(r, indent=2, ensure_ascii=False) if r else "not found (private results have no surroundings)")
    elif a.cmd == "page":
        import os, runpy
        runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "server.py"), run_name="__main__")
    elif a.cmd == "usage":
        u = usage.status(cfg, connect(cfg["db"]))
        print(f"{u['notes']} notes seen, {u['opens']} opens counted; learning from use is "
              + ("ON" if u["active"] else f"off until {u['needed']} opens"))
    elif a.cmd == "cards":
        if a.import_file:
            s = cards.import_file(cfg, a.import_file)
            print(f"loaded {s['cards']:,} section cards and {s['chat_cards']} chat cards; "
                  f"{s['sections_with_card']:,} sections here have a card")
        elif a.estimate:
            e = cards.estimate(cfg)
            print(f"{e['sections']:,} sections and {e['chats']} AI conversations need a card: about "
                  f"{e['input_tokens']:,} input and {e['output_tokens']:,} output tokens with {cfg['cards']['model']}.")
        else:
            s = cards.run(cfg, a.limit, a.fake)
            print(f"made {s['done']} section cards and {s['chats']} chat cards, failed {s['failed']}, "
                  f"sections still to do {s['remaining']:,} | "
                  f"tokens in {s['input_tokens']:,} out {s['output_tokens']:,}")
            for e in s["errors"]:
                print("  error:", e)
    elif a.cmd == "test":
        evaluate.run(cfg)
    elif a.cmd == "health":
        checks, problems = health.check(cfg)
        print("\n".join(health.lines(checks)))
        sys.exit(1 if problems else 0)
    elif a.cmd == "stats":
        con = connect(cfg["db"])
        for src, n, c in con.execute("SELECT f.source, COUNT(DISTINCT f.path), COUNT(c.id) FROM files f "
                                     "LEFT JOIN chunks c ON c.file_path=f.path GROUP BY f.source"):
            print(f"{src}: {n} files, {c} sections")
        print("cards:", con.execute("SELECT COUNT(*) FROM cards").fetchone()[0])
        print("top folders:")
        for folder, n in con.execute("SELECT substr(path,1,instr(path||'/','/')-1) AS d, COUNT(*) FROM files "
                                     "WHERE source='vault' GROUP BY d ORDER BY 2 DESC LIMIT 12"):
            print(f"  {folder}: {n}")


if __name__ == "__main__":
    main()
