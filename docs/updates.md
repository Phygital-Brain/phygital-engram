# Updates

For when a new version comes out. At the end you are on the latest version and you know how to go back.

## Know when there's an update

New versions appear on the repository's [releases page](https://github.com/Phygital-Brain/phygital-engram/releases). Click **Watch**, then **Custom**, then **Releases** to get an email. Each release lists what changed in [CHANGELOG.md](../CHANGELOG.md).

## Update by hand

1. Download the new version from the releases page and unzip it. If you used Git, run this instead:

```bash
git pull
```

2. If you downloaded a zip, replace the old program folder with the new one. If you changed `config.json`, keep your settings: copy your version over the new one, or compare the two first.
3. Rebuild the index if the release notes say the index changed:

```bash
python3 engram.py ingest --rebuild
```

You should see `REBUILT.` at the start of the line. This takes seconds for a few thousand notes. Phygital Engram also rebuilds by itself on the next run when a setting that affects the index has changed.

4. Check it works:

```bash
python3 engram.py health
```

## Update every week by itself

Not built yet. An automatic updater is on the [roadmap](roadmap.md). Until then, check the releases page when you like.

## Staying on one version

You don't have to update. An old version keeps working. Update if a release says it fixes a security problem. See [SECURITY.md](../SECURITY.md) for how problems are handled.

## Going back

Download the older version from the releases page and replace the program folder. Then rebuild the index:

```bash
python3 engram.py ingest --rebuild
```

An older version can read a newer index only if the release notes say so. A rebuild is safer and takes seconds.

## What an update never touches

- Your notes. Phygital Engram never changes them, in any version.
- Your API key, if you use [note cards](cards.md). It lives outside the program folder.
- Note cards already made. They are kept by content, so a rebuild does not lose them.
