# Optional GitHub Pages publishing + LinkedIn sharing

Publishing is **not part of generating an experience** and may never happen automatically. Review the final site and obtain explicit owner approval before any remote action. Do not publish source files or photos, extracted text, private evidence reports, API keys or full private input JSON.

From an installed skill folder (Python 3.9+):

```bash
python3 scripts/publish_portfolio.py prepare \
  --html /path/to/index.html \
  --account USERNAME --repo my-career-world \
  --out /path/to/private/publish-ready
```

Preparation is offline and produces `site/index.html`, `.nojekyll`, and a social-preview image, plus an owner checklist and editable LinkedIn post. If Chromium/Playwright isn't available, use `--preview /path/to/approved.jpg` to supply an original JPEG/PNG/WebP image. Preparation does **not** publish.

**Manual publish:** upload only the contents of the `site/` folder to a **new public repository** in the owner's account; then Settings → Pages → Deploy from branch → `main` → `/(root)` → Save. Check the URL publicly.

**Optional CLI publish:** only after owner authorization and `gh auth login`, run `python3 scripts/publish_portfolio.py deploy --bundle /path/to/private/publish-ready --account USERNAME --repo my-career-world --approve-public`. This creates a new public repo with `gh`, refuses name collisions, and attempts to enable GitHub Pages. If Pages enabling fails, give the manual Settings instructions. A publish command starting is **not** proof the site is live.

**LinkedIn:** supply the public link and draft `LINKEDIN_POST.txt`. The owner pastes them into a post, checks the preview and clicks Post. The actual interactive website opens after clicking the link; LinkedIn does not embed custom HTML interaction. Optional attribution: “Created with SimpliCITY Builder” and the GitHub URL. No automatic LinkedIn API posting is provided.
