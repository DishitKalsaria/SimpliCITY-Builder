# SimpliCITY Builder v0.2.1 — GitHub setup

Apply the v0.2.1 source package to your existing `main` checkout only after reviewing the diff and preserving `.git/`. The candidate was built from the final locally available v0.2.0 source ZIP; reconcile any newer files from live `main` before applying. The current live repository revision was not retrieved here.

```bash
git status --short
python3 -m unittest discover -s tests -v
git diff --check
```

Enable the gallery from **Settings → Pages → Deploy from a branch → `main` → `/docs` → Save**. Confirm `docs/index.html`, `.nojekyll` and the six linked `.html` demos (plus optional unlisted `volcanic.html` visual-reference candidate) are committed. Verify actual public URLs; GitHub Pages is separate from GitHub Releases.

The workflow in `.github/workflows/test.yml` tests pushed changes; `.github/workflows/release.yml` runs when a `v*` tag is pushed, verifies it matches the declared skill version and publishes a portable skill ZIP. **Do not tag until [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) passes.**

Suggested repository topics: `ai-skill`, `agent-skills`, `portfolio`, `resume`, `html-generator`. Topics are a GitHub repository setting and are not changed by this package.
