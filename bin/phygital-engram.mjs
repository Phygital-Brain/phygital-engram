#!/usr/bin/env node
// Starts the Phygital Engram connector (mcp/server.py) with Python 3.11 or newer.
// Set ENGRAM_VAULT to your notes folder and ENGRAM_DATA to a folder outside it.
import { spawn, spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const python = ["python3", "python"].find((p) => {
  const r = spawnSync(p, ["-c", "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"]);
  return r.status === 0;
});
if (!python) {
  console.error("Phygital Engram needs Python 3.11 or newer. Install it from python.org, then try again.");
  process.exit(1);
}
const child = spawn(python, [join(root, "mcp", "server.py"), ...process.argv.slice(2)], { stdio: "inherit" });
child.on("exit", (code, signal) => process.exit(signal ? 1 : code ?? 0));
for (const s of ["SIGINT", "SIGTERM"]) process.on(s, () => child.kill(s));
