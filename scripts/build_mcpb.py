"""Build the Claude Desktop extension: dist/phygital-engram-<version>.mcpb. Run from the repository root:

    python3 scripts/build_mcpb.py

A .mcpb file is a zip with manifest.json at the top. It holds the connector (server/server.py) and the
search it runs (engram.py, engram_lib/, config.json), so the folder layout matches the repository:
server/server.py finds ../engram.py. Claude Desktop asks the person for the notes folder and the data
folder when they install it. The person needs Python 3 on their computer.

Before version 0.1.0 the search code is not in the repository yet. The build then stops, unless you
pass --allow-missing to check the rest.
"""
import importlib.util
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
version = json.load(open(".claude-plugin/plugin.json"))["version"]
allow_missing = "--allow-missing" in sys.argv

spec = importlib.util.spec_from_file_location("server", "mcp/server.py")
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

engine = ["engram.py", "config.json"]
engine_dirs = ["engram_lib"]
missing = [p for p in engine + engine_dirs if not os.path.exists(p)]
if missing and not allow_missing:
    sys.exit(f"The search code is not in the repository yet (missing: {', '.join(missing)}). Use --allow-missing to build anyway.")

manifest = {
    "manifest_version": "0.3",
    "name": "phygital-engram",
    "display_name": "Phygital Engram",
    "version": version,
    "description": "Your notes, found in milliseconds. Phygital Engram is a fast, private, read-only search for your second brain, or any folder of Markdown notes.",
    "long_description": "Lets Claude search a folder of your Markdown notes and open the best result, with the note, heading and date as the source. Phygital Engram only reads your notes. It keeps its own files in a separate folder, collects nothing, and sends nothing anywhere. Private folders are findable but stay locked. Needs Python 3 on your computer.",
    "author": {"name": "Phygital-Brain", "url": "https://github.com/Phygital-Brain"},
    "homepage": "https://github.com/Phygital-Brain/phygital-engram",
    "documentation": "https://github.com/Phygital-Brain/phygital-engram/blob/main/docs/connect-your-ai.md",
    "support": "https://github.com/Phygital-Brain/phygital-engram/issues",
    "repository": {"type": "git", "url": "https://github.com/Phygital-Brain/phygital-engram"},
    "license": "Apache-2.0",
    "icon": "icon.png",
    "keywords": ["search", "markdown", "notes", "second-brain"],
    "server": {
        "type": "python",
        "entry_point": "server/server.py",
        "mcp_config": {
            "command": "python3",
            "args": ["${__dirname}/server/server.py"],
            "env": {"ENGRAM_VAULT": "${user_config.notes_folder}", "ENGRAM_DATA": "${user_config.data_folder}"},
        },
    },
    "user_config": {
        "notes_folder": {"type": "directory", "title": "Your notes folder", "description": "The folder of Markdown notes to search. Phygital Engram only reads it.", "required": True},
        "data_folder": {"type": "directory", "title": "Folder for the index", "description": "Where Phygital Engram keeps its own files. Pick a folder OUTSIDE your notes folder.", "required": True},
    },
    "tools": [{"name": t["name"], "description": t["description"].split(".")[0]} for t in server.TOOLS],
    "compatibility": {"platforms": ["darwin", "win32", "linux"], "runtimes": {"python": ">=3.11"}},
}

os.makedirs("dist", exist_ok=True)
out = f"dist/phygital-engram-{version}.mcpb"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    z.write("mcp/server.py", "server/server.py")
    z.write("LICENSE", "LICENSE")
    z.write("NOTICE", "NOTICE")
    z.write("docs/images/icon.png", "icon.png")
    for f in engine:
        if os.path.exists(f):
            z.write(f, f)
    for d in engine_dirs:
        for base, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            for f in files:
                if not f.startswith("."):
                    z.write(os.path.join(base, f))
print(f"{out}: {os.path.getsize(out) // 1024} KB, version {version}" + (f" (without: {', '.join(missing)})" if missing else ""))
