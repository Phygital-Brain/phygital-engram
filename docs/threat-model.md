# Threat model

Who Phygital Engram keeps out, who it cannot, and what nobody has checked yet. Read it if you run the server version.

> [!WARNING]
> Not audited. No outside person has reviewed this code for security. The server version holds the text of your notes, and it is reachable from the internet. Treat it as you would any server that holds private files.

## What it protects

| Risk | What stops it |
|---|---|
| A stranger searches your notes | Every request needs a key. A key comes only from the login page, after your passphrase. Without a key the server answers `401` |
| Someone guesses your passphrase | Five wrong tries from one address pause that address for 15 minutes. Fifty from anywhere pause every login. The passphrase is stored as a salted hash (`LOGIN_HASH`) |
| A stolen key | A key works for one hour and renews itself. Keys are stored only as fingerprints, so the file on disk cannot be used as a key |
| A fake AI app steals a login | An app can only send you back to an allowed address (`ALLOWED_REDIRECT_HOSTS`, plus `localhost`). The login page names the app and where it returns |
| Your passphrase in the open | The server refuses to start when `PUBLIC_URL` is not `https://` |
| An AI changes your notes | There is no tool that writes. Every tool is read-only, and the notes folder is mounted read-only in the Compose setup |
| An AI opens a private note | A private result can be found, and no tool opens it. The tool refuses |
| A note that tries to give the AI orders | Everything a tool returns is labelled as note content, never instructions. That helps, but it is not a guarantee: see below |
| Another site tricks your browser | The login page has no scripts, cannot be framed, and sends no referrer. The server checks the address it was reached at |
| Secrets in your notes reach an AI | Secret lines, labelled tax IDs, IBANs and card numbers are blanked before they are stored. Password files are never read |

## What it cannot protect

- **Someone who has your passphrase.** They can log in as you and read every note the index holds, except private ones.
- **Someone who controls your server.** They can read the notes folder and the index directly.
- **An AI model following orders hidden in a note.** If a note says "ignore your instructions", a model may still obey. The label helps, and the tools cannot change anything, but a model could still repeat or act on that text elsewhere. Do not put untrusted text in notes you let an AI read.
- **What the AI service does with the results.** Search results are sent to the AI app you use, and that company handles them under its own rules.
- **A phone or computer that is lost and unlocked,** where an AI app is already signed in.
- **Notes that look harmless to the blanking step.** It catches labelled secrets and common key formats. A password written as plain prose is not caught.

## Not checked yet

- No security audit.
- No test of the Docker setup, Caddy, or a real server (see [setup-own-server.md](setup-own-server.md#what-we-tested)).
- No test from a phone or the Claude website with this repository.

Found a problem? Report it privately: see [../SECURITY.md](../SECURITY.md).
