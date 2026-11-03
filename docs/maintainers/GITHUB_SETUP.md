# SimpliCITY Builder v0.2.0 — GitHub setup

Merge the v0.2.0 source package into your existing clone only after reviewing the diff and preserving `.git/`. The package is based on the latest locally available v0.1.5 source, not a verified live `main` snapshot.

```bash
git status --short
python3 -m unittest discover -s tests -v
git diff --check
```

Enable the gallery from **Settings → Pages → Deploy from a branch → `main` → `/docs` → Save**. Confirm `docs/index.html`, `.nojekyll` and the four `.html` demos are committed. Verify actual public URLs; GitHub Pages is separate from GitHub Releases.

The workflow in `.github/workflows/test.yml` tests pushed changes; `.github/workflows/release.yml` runs when a `v*` tag is pushed, verifies it matches the declared skill version and publishes a portable skill ZIP. **Do not tag until [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) passes.**

Suggested repository topics: `ai-skill`, `agent-skills`, `portfolio`, `resume`, `html-generator`. Topics are a GitHub repository setting and are not changed by this package.
