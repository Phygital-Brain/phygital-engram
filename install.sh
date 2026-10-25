#!/bin/sh
# Phygital Engram installer for Mac and Linux.
#
#   curl -fsSL https://raw.githubusercontent.com/Phygital-Brain/phygital-engram/main/install.sh | sh -s -- "$HOME/Notes"
#
# What it does, in order:
#   1. checks that git and Python 3.11 or newer are there
#   2. checks your notes folder (it only reads it, and never writes to it)
#   3. downloads the program into ~/.phygital-engram/app
#   4. builds the index in ~/.phygital-engram/data, which is outside your notes
#   5. connects it to Claude Code if you have it, or prints the lines for other AI apps
#
# Settings, all optional:
#   PHYGITAL_ENGRAM_HOME    where the program and its data go (default ~/.phygital-engram)
#   PHYGITAL_ENGRAM_SOURCE  where to download from (default the GitHub repository)
set -eu

NOTES="${1:-}"
HOME_DIR="${PHYGITAL_ENGRAM_HOME:-$HOME/.phygital-engram}"
APP="$HOME_DIR/app"
DATA="${2:-$HOME_DIR/data}"
SOURCE="${PHYGITAL_ENGRAM_SOURCE:-https://github.com/Phygital-Brain/phygital-engram.git}"

say() { printf '%s\n' "$*"; }
stop() { printf 'Stopped: %s\n' "$*" >&2; exit 1; }

if [ -z "$NOTES" ]; then
  stop "tell me where your notes are. Example: sh install.sh \"\$HOME/Notes\""
fi

# 1. tools
command -v git >/dev/null 2>&1 || stop "git is not installed. Install it, then run this again."
command -v python3 >/dev/null 2>&1 || stop "Python 3 is not installed. Install Python 3.11 or newer from python.org, then run this again."
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
  || stop "your Python is $(python3 --version 2>&1). You need 3.11 or newer. Install it from python.org, then run this again."

# 2. your notes
[ -d "$NOTES" ] || stop "the notes folder $NOTES does not exist."
NOTES="$(cd "$NOTES" && pwd)"
[ -f "$NOTES/CLAUDE.md" ] || stop "there is no file named CLAUDE.md at the top of $NOTES. Phygital Engram needs it to know the folder is your notes and fully copied. It can be an empty file. Phygital Brain makes one for you. Create it, then run this again."
# the data folder must be outside your notes: check this BEFORE creating anything
INSIDE="$(python3 - "$NOTES" "$DATA" <<'PY'
import os, sys
n = os.path.realpath(sys.argv[1])
d = os.path.realpath(os.path.expanduser(sys.argv[2]))
print("yes" if d == n or d.startswith(n + os.sep) else "no")
PY
)"
[ "$INSIDE" = "no" ] || stop "the data folder $DATA is inside your notes folder. Pick a folder outside it."
mkdir -p "$DATA"
DATA="$(cd "$DATA" && pwd)"

# 3. the program
mkdir -p "$HOME_DIR"
if [ -d "$APP/.git" ]; then
  say "Updating Phygital Engram in $APP"
  git -C "$APP" pull --ff-only --quiet
else
  say "Downloading Phygital Engram into $APP"
  git clone --depth 1 --quiet "$SOURCE" "$APP"
fi

# 4. the index
say "Building the index (this reads your notes, and changes nothing in them)"
ENGRAM_VAULT="$NOTES" ENGRAM_DATA="$DATA" python3 "$APP/engram.py" ingest

# 5. connect
SERVER="$APP/mcp/server.py"
if command -v claude >/dev/null 2>&1; then
  claude mcp remove phygital-engram --scope user >/dev/null 2>&1 || true
  claude mcp add phygital-engram --scope user --env "ENGRAM_VAULT=$NOTES" --env "ENGRAM_DATA=$DATA" -- python3 "$SERVER" >/dev/null
  say ""
  say "Done. Claude Code can now search your notes. Open it and ask:"
  say "  Search my notes for ... and tell me where you found it."
else
  say ""
  say "Done. Claude Code was not found, so add this to your AI app's list of MCP servers:"
  say ""
  say "  command: python3"
  say "  argument: $SERVER"
  say "  ENGRAM_VAULT=$NOTES"
  say "  ENGRAM_DATA=$DATA"
  say ""
  say "Steps for each app: https://github.com/Phygital-Brain/phygital-engram/blob/main/docs/connect-your-ai.md"
fi
say ""
say "Try it in the terminal too:"
say "  ENGRAM_VAULT=\"$NOTES\" ENGRAM_DATA=\"$DATA\" python3 \"$APP/engram.py\" search \"your question\""
