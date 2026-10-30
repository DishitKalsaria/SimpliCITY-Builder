# Update the existing SimpliCITY Builder repository

Use your **existing Git clone** in VS Code. Do not initialize Git again or copy an outer folder into the repo.

- Extract the v0.1.5 update/source ZIP; merge its **contents**, including hidden `.github/`, into your cloned repo. Preserve `.git/` and inspect replacements.
- Remove obsolete proposal/acceptance files and old committed ZIPs if present; the current guides are `PUBLISHING.md` and `RELEASE_ACCEPTANCE.md`. Run `git rm --ignore-unmatch PUBLISHING_IDEA.md V014_ACCEPTANCE.md tests/test_v014.py` to remove the three superseded tracked files.
- Check for private résumés, `portfolio.json`, screenshots, `.env` values and other secrets before staging.

```bash
python3 -m unittest discover -s tests -v
git status --short
git add -A
git diff --cached --stat
git diff --cached --check
git commit -m "Prepare SimpliCITY Builder v0.1.5 publishing and sharing"
git push origin main
```

Confirm GitHub Actions passes and the Pages demo gallery works. The CI workflow runs local tests and Chromium checks; it does **not** run an external Agent Skills reference validator.

For **external testing**, see [RELEASING.md](RELEASING.md) for creating `v0.1.5-rc.1` and distributing verified assets. Publish the final `v0.1.5` tag only after acceptance tests succeed.
