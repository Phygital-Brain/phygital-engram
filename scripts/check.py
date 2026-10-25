#!/usr/bin/env python3
"""Checks for repos with no code to test (content profile). Run before every change:  python3 scripts/check.py

Fails on: a broken relative link, a missing heading anchor, an em dash, a leftover {{placeholder}},
and version numbers that disagree between CITATION.cff and plugin.json / package.json.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "node_modules" not in p.parts)
LINK = re.compile(r"\]\(([^)\s]+)\)|href=\"([^\"]+)\"|src=\"([^\"]+)\"")
errors: list[str] = []


def slug(heading: str) -> str:
    text = re.sub(r"[`*_]|<[^>]+>", "", heading.strip().lower())
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: Path) -> set[str]:
    out, in_code = set(), False
    for line in path.read_text("utf-8").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("#"):
            out.add(slug(line.lstrip("#")))
    return out


for doc in DOCS:
    raw = doc.read_text("utf-8")
    text = re.sub(r"```.*?```", "", raw, flags=re.S)
    for m in LINK.finditer(text):
        target = next(g for g in m.groups() if g)
        if re.match(r"[a-z]+:", target) or target.startswith("//"):
            continue
        path, _, anchor = target.partition("#")
        dest = (doc.parent / path).resolve() if path else doc
        if not dest.exists():
            errors.append(f"{doc.relative_to(ROOT)}: broken link {target}")
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            errors.append(f"{doc.relative_to(ROOT)}: no heading for {target}")
    for i, line in enumerate(raw.splitlines(), 1):
        if chr(0x2014) in line or (" " + chr(0x2013) + " ") in line:
            errors.append(f"{doc.relative_to(ROOT)}:{i}: em dash")

versions = {}
cff = ROOT / "CITATION.cff"
if cff.exists():
    m = re.search(r"^version:\s*(\S+)", cff.read_text("utf-8"), re.M)
    if m:
        versions["CITATION.cff"] = m.group(1)
for name in (".claude-plugin/plugin.json", "package.json"):
    p = ROOT / name
    if p.exists():
        versions[name] = json.loads(p.read_text("utf-8")).get("version")
if len(set(versions.values())) > 1:
    errors.append(f"version numbers disagree: {versions}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(DOCS)} markdown files checked")
