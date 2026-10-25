# Setup on your own server

Put Phygital Engram on a server you own, so your phone, the Claude website and other AI apps can search your notes from anywhere. You end up with an address like `https://notes.example.com/mcp`, and you type a passphrase once.

> [!IMPORTANT]
> First release, version 0.1.0. The server version is written and tested on a computer, but it has not been run in Docker, on a real server or from a phone with this repository. A Docker image is published with the release at `ghcr.io/phygital-brain/phygital-engram` (the Packages page). The Compose file below builds the image from this repository. Read [What we tested](#what-we-tested) before you rely on it.

<details>
<summary><b>Table of contents</b></summary>

- [What you need](#what-you-need)
- [How your notes reach the server](#how-your-notes-reach-the-server)
- [With Docker Compose](#with-docker-compose)
- [Check it works](#check-it-works)
- [Connect your AI app](#connect-your-ai-app)
- [Without Docker](#without-docker)
- [Behind your own reverse proxy](#behind-your-own-reverse-proxy)
- [Backups](#backups)
- [Update, stop or remove it](#update-stop-or-remove-it)
- [If it doesn't work](#if-it-doesnt-work)
- [What we tested](#what-we-tested)

</details>

## What you need

- A server that is always on, with Docker and Docker Compose. A small one is enough.
- A domain name, pointed at the server's IP address. HTTPS is needed so your passphrase is never sent in the open. Caddy gets the certificate for you.
- Your notes on that server, in a folder. See the next section.
- 15 minutes.

## How your notes reach the server

Phygital Engram reads the notes where they are. It does not copy them in by itself. Pick one way to keep a copy of your notes folder on the server:

| Way | How |
|---|---|
| A sync app | Install your cloud drive's sync app on the server (most cloud drives and Syncthing have one) and let it fill a folder |
| A scheduled copy | A copy tool, run on a schedule, copies from your drive to the server every few minutes |
| Git | Your notes are a Git repository and the server pulls it |

The server mounts that folder **read-only**. Phygital Engram can read the notes and cannot change them. Every 10 minutes it updates its index from the folder. You can change that with `PHYGITAL_ENGRAM_REFRESH_MINUTES`.

> [!WARNING]
> Your notes will sit on a server on the internet. Anyone who gets into that server can read them. Keep it updated, use a firewall that allows only ports 80 and 443, and read [safety.md](safety.md) and [threat-model.md](threat-model.md) first. Mark private folders as private before the first index.

## With Docker Compose

1. Point your domain at the server. Wait until `ping notes.example.com` shows your server's address.

2. Get the repository onto the server:

   ```bash
   git clone https://github.com/Phygital-Brain/phygital-engram.git
   ```

   ```bash
   cd phygital-engram
   ```

3. Make your passphrase hash. Pick 8 or more characters, ideally a few random words. The hash is saved instead of the passphrase:

   ```bash
   python3 mcp/serve.py hash
   ```

   You should see one line that starts with `LOGIN_HASH=pbkdf2:`. You need Python 3 and the MCP SDK for this (`pip install -r requirements-server.txt`). Without them, use `LOGIN_PASSPHRASE` in the next step, which is less safe because it is kept as plain text.

4. Copy the settings file and fill it in:

   ```bash
   cp .env.example .env
   ```

   Open `.env` and set `PHYGITAL_ENGRAM_DOMAIN` (your domain), `NOTES_DIR` (the folder with your notes, for example `/srv/notes`) and `LOGIN_HASH` (the line from step 3). Keep `.env` private. It is never committed.

5. Start it:

   ```bash
   docker compose up -d
   ```

   The first start builds the image, asks Caddy for a certificate, and builds the index.

## Check it works

Open `https://notes.example.com/health` in a browser. You should see `ok`.

Then check the index. In the server folder:

```bash
docker compose exec app python /app/engram.py health
```

You should see lines starting with `OK`.

## Connect your AI app

The address to give your AI app is `https://notes.example.com/mcp`. Step by step for each app: [connect-your-ai.md](connect-your-ai.md). The first time, the app opens a page on your server, you type the passphrase, and you tap **Allow**.

## Without Docker

You need Python 3.14 and the files from this repository.

```bash
python3 -m venv .venv
```

```bash
.venv/bin/pip install -r requirements-server.txt
```

Then set the same settings as above in your shell and run:

```bash
PUBLIC_URL=https://notes.example.com ENGRAM_VAULT=/srv/notes ENGRAM_DATA=/var/lib/phygital-engram LOGIN_HASH='...' .venv/bin/python mcp/serve.py
```

It listens on `127.0.0.1:8765`. Put a reverse proxy with HTTPS in front, and keep it running with a service manager such as systemd. It refuses to start if `PUBLIC_URL` is not `https://`, or if there is no passphrase.

## Behind your own reverse proxy

If you already run nginx or Caddy, send your domain to `127.0.0.1:8765` and pass the visitor's address in the `X-Forwarded-For` header. Set `PHYGITAL_ENGRAM_TRUST_PROXY=1` so that the lockout counts wrong passphrases per visitor. Without a proxy that sets this header, leave it unset.

## Backups

You only need to keep your notes. The index is rebuilt from them in about 15 seconds for 5,000 notes. The `app-data` volume also holds the login keys. If you lose it, each AI app just asks you to log in again.

## Update, stop or remove it

Update: pull the new version and rebuild.

```bash
git pull
```

```bash
docker compose up -d --build
```

Stop: `docker compose down`. Remove everything, including the index and keys: `docker compose down -v`. Your notes are never touched. More in [updates.md](updates.md).

## If it doesn't work

- **`/health` does not open.** The domain does not point at the server yet, or ports 80 and 443 are closed in the firewall. Check Caddy: `docker compose logs caddy`.
- **The container stops at once.** Read why: `docker compose logs app`. It refuses to start with no passphrase, with a passphrase under 8 characters, or with a `PUBLIC_URL` that is not `https://`.
- **"Nothing changed" in the logs.** The notes folder is empty, or it has no `CLAUDE.md` file at the top. The search uses that file to check that your notes are fully copied. See [troubleshooting.md](troubleshooting.md).
- **Your AI app says it cannot log in.** The app's address may not be allowed. Add its host to `ALLOWED_REDIRECT_HOSTS`.
- **Too many wrong tries.** Five wrong passphrases from one address pause that address for 15 minutes.

## What we tested

| What | Result |
|---|---|
| 11 automated tests of the server: login, wrong passphrase, lockout, key renewal, the four tools, a private result refused, unsafe starts refused. Python 3.14, MCP SDK 2.3.0, a stand-in search, 2026-10-25 | Pass |
| Claude Code 2.1.310 connected to the server over HTTP with a login key, on the sample notes, 2026-10-25 | Worked. It called `search_notes` and answered correctly |
| The login page in a real browser, on a desktop and a phone-sized screen, 2026-10-25 | Worked. A wrong passphrase showed an error, the right one sent the browser back to the app, and the page fits a phone screen |
| The server building its own index when it starts on an empty data folder, 2026-10-25 | Worked. The index was there within seconds |
| A real phone, the Claude website or ChatGPT connecting to this repository's server | Not tested |
| Docker, Docker Compose, Caddy and the certificate | Not tested: Docker was not available where this was written |
| A real server on the internet | Not tested |

The author runs their own tuned version of the search on their own server and uses it from a phone. That setup is separate from the files in this repository.
