# Threat model

Who Phygital Engram keeps out, where its limits are, and what we would like to check next. Read it if you run the server version.

> [!NOTE]
> Phygital Engram has not had an outside security review yet. It is built to keep your notes private, and this page says how. If you find a gap, please tell us: see [../SECURITY.md](../SECURITY.md).

## How it protects your notes

| Risk | What stops it |
|---|---|
| A stranger searches your notes | Every request needs a key. A key comes only from the login page, after your passphrase. Without a key the server answers `401` |
| Someone guesses your passphrase | Five wrong tries from one address pause that address for 15 minutes. Fifty from anywhere pause every login. The passphrase is stored as a salted hash (`LOGIN_HASH`) |
| A stolen key | A key works for one hour and renews itself. Keys are stored only as fingerprints, so the file on disk cannot be used as a key |
| A fake AI app steals a login | An app can only send you back to an allowed address (`ALLOWED_REDIRECT_HOSTS`, plus `localhost`). The login page names the app and where it returns |
| Your passphrase sent in the open | The server refuses to start when `PUBLIC_URL` is not `https://` |
| An AI changes your notes | There is no tool that writes. Every tool is read-only, and the notes folder is mounted read-only in the Compose setup |
| An AI opens a private note | A private result can be found, and no tool opens it. The tool refuses |
| A note that tries to give the AI orders | Everything a tool returns is labelled as note content, never instructions. That helps a lot, and it is not a guarantee: see the next section |
| Another site tricks your browser | The login page has no scripts, cannot be framed, and sends no referrer. The server checks the address it was reached at |
| Secrets in your notes reach an AI | Secret lines, labelled tax IDs, IBANs and card numbers are blanked before they are stored. Password files are never read |

## Where the limits are

Some things no tool can do for you. These stay in your hands:

- **Your passphrase.** Anyone who has it can log in as you and read what the index holds, except private notes. Pick a few random words and keep it in a password manager.
- **Your server.** Whoever controls the machine can read the notes folder and the index directly. Keep it updated and open only ports 80 and 443.
- **Text hidden in a note.** If a note says "ignore your instructions", an AI model may still follow it. The label helps and the tools cannot change anything, but a model could repeat or act on that text elsewhere. Keep untrusted text out of notes you let an AI read.
- **What your AI service does with results.** Search results go to the AI app you use, and that company handles them under its own rules.
- **A phone or computer that is lost and unlocked,** where an AI app is already signed in. Use a screen lock.
- **Secrets written as plain prose.** The blanking step catches labelled secrets and common key formats. A password written in a sentence is not caught, so keep passwords out of your notes.

## What we would like to check next

These are open invitations. If you try one, tell us what you find.

- A security review by someone outside the project.
- The Docker setup, Caddy and a real server on the internet. See [setup-own-server.md](setup-own-server.md#what-we-tested).
- The login from a real phone, the Claude website and ChatGPT.

Found a problem? Report it privately: see [../SECURITY.md](../SECURITY.md).
