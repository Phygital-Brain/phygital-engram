# Security policy

Phygital Engram reads a folder of your Markdown notes and keeps a search index of them on your computer. It can see everything in the folders you point it at, so security reports are very welcome.

It is not related to other projects that happen to be called Engram. Problems in those go to their own maintainers.

## Supported versions

Only the newest release gets security fixes. Updating is the fix. See [docs/updates.md](docs/updates.md).

| Version | Security fixes |
|---|---|
| 0.1.x (the latest release, [see Releases](https://github.com/Phygital-Brain/phygital-engram/releases/latest)) | Yes |
| Anything older | No, please update |

## Reporting a problem

Please **don't** open a public issue, discussion or pull request for a security problem.

1. Go to the **Security** tab of this repository and click **[Report a vulnerability](https://github.com/Phygital-Brain/phygital-engram/security/advisories/new)**. Only the maintainer sees it.
2. Tell me what's in the next section.
3. Never send real passwords, keys, tokens or private data. Use test data.

There's no email contact. Use private reporting.

## What to include

- The version and how you run it (command line or the local page).
- Your operating system and your AI app, if it matters.
- What you found, and which part of the code it's in, if you know.
- The steps to reproduce it.
- What an attacker could do with it, and what they need first.

## What happens next

| When | What |
|---|---|
| Within 3 days | You get a first answer saying the report arrived |
| Within 10 days | I confirm the problem (or explain why it isn't one) and agree on a plan |
| Usually within 30 days | A fixed release is published |
| After the release | The advisory is published, with a CVE when it's useful |

This is a project run in spare time, so a date can slip. If it does, you'll hear why. Please keep the problem private until the fixed release is out, or until 90 days have passed, whichever comes first.

## Credit

If you'd like, you're named in the published advisory and in [CHANGELOG.md](CHANGELOG.md). Tell me the name or GitHub account to use, or say you'd rather stay anonymous. There's no paid bug bounty.

## Testing in good faith

If you follow this policy, I won't take any action against you for your research. Please:

- test only on your own data and your own computer or server, or ones you have permission to test
- never open, read or change other people's data
- stop and report as soon as you see someone else's data
- don't run denial-of-service tests against someone else's server

## In scope

- Anything that could reveal a secret, a key or private contents to someone who shouldn't have them (search results, the local page, error messages, logs, files on disk). This includes a secret that the blanking step missed.
- Any way to make Phygital Engram write to, move or delete a note, or put its index inside your notes folder.
- Any way to open a private (locked) result without being asked, including through the AI connector.
- Any way to make the connector run anything other than its fixed search commands, or return text as instructions instead of note content.
- Any way to use the local page from another website, or from another computer on your network when it is not meant to be reachable.
- Any change that damages your data, or sends your notes to a service without you turning that on.

## Out of scope

- An AI model following instructions hidden in a file (prompt injection). That's a known limit of today's AI models. The defences are in [docs/safety.md](docs/safety.md), and improvements are welcome as normal issues.
- A user asking the AI to do something harmful to their own data, after the approvals.
- Weak passwords or passphrases chosen by a user.
- What's listed under "What it does not protect against" in [docs/safety.md](docs/safety.md).
- Problems in your sync app, your AI app, or Python itself. Please report those to them.
- Problems in a dependency that this project doesn't use in a harmful way.
- Missing security headers or reports from automated scanners without a real attack that works.

## Keeping your own setup safe

- Update when a new release comes out.
- Keep the data folder where only you can read it. The index holds your note text.
- Mark private folders as private before the first index.
- Keep backups of your notes. Phygital Engram never changes them, but backups are good anyway.
- More in [docs/safety.md](docs/safety.md) and [docs/privacy.md](docs/privacy.md).
