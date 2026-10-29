"""A stand-in for engram.py, so the connector tests do not need the real search. Prints made-up answers."""
import json
import sys

a = sys.argv[1:]
import os
if os.environ.get("FAKE_ENGRAM_LOG"):
    open(os.environ["FAKE_ENGRAM_LOG"], "a").write(a[0] + "\n")
if a[:1] == ["search"]:
    if "nothing" in a[1]:
        print("[]")
    elif "--folder" in a:
        print(json.dumps([{"id": 9, "path": a[a.index("--folder") + 1] + "/note.md", "heading": "note", "snippet": "in the folder", "why": ""}]))
    elif "locked" in a[1]:
        print(json.dumps([{"id": "p1", "path": "Memory/finances/q3.md", "heading": "Q3", "private": True, "snippet": "Private. Open only when asked."}]))
    else:
        print(json.dumps([{"id": 7, "path": "Projects/Picture-Book/notes/schedule.md", "heading": "schedule > Schedule", "snippet": "Marta moved the [cover] to the 15th.", "why": "your words in the heading"}]))
elif a[:1] == ["get"]:
    print("PRIVATE OPENED" if "--private" in a else json.dumps({"id": a[1], "text": "full section"}))
elif a[:1] == ["around"]:
    print(json.dumps({"id": a[1], "before": [], "after": []}))
elif a[:1] == ["ingest"]:
    print("indexed 3 | total 3 files")
elif a[:1] == ["map"]:
    print("- Projects (8 notes): Picture book and zine work")
elif a[:1] == ["health"]:
    print("OK    Index: last update 0 min ago")
else:
    sys.exit(2)
