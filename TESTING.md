# Test SimpliCITY Builder v0.1.5

## Automated tests

```bash
python3 -m unittest discover -s tests -v
python3 simplicity-builder/scripts/build_portfolio.py --input examples/space-sample.json --output space-demo.html
python3 simplicity-builder/scripts/validate.py examples/space-sample.json space-demo.html
```

All four examples are also built by GitHub Actions. The test suite checks SVG security, landmark labels, motion classes, mobile scene, résumé evidence, social metadata and publishing safety. An HTML validator pass is **not** a visual quality score.

## Real browser test (optional dependency)

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/browser_smoke.py docs/fairytale.html docs/space.html docs/festival.html docs/clockwork.html --screenshots private/screenshots
```

Review screenshots manually for recognizable artwork, clear focal points, overlap/clipping, text contrast, landmark click areas and smartphone framing. The body must never scroll in desktop/mobile mode; accessible long dialogs may scroll internally.

## Publishing test — no upload

```bash
python3 simplicity-builder/scripts/publish_portfolio.py prepare \
  --html docs/space.html --account DemoUser --repo my-world --out private/test-publish
```

Inspect `site/index.html`, `site/social-preview.jpg`, `LINKEDIN_POST.txt` and the review checklist. **This command never publishes.** If Playwright is absent, pass `--preview docs/assets/space-social.jpg` instead.

The `deploy` command requires explicit `--approve-public`, GitHub CLI authentication and an unused repository name. Only test remote deployment on a user-owned account with approval.

## End-to-end AI tests

[RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) defines installed-skill, link-only and publication acceptance. Record actual results before marking compatible AI apps as verified. The skill cannot guarantee that a link-only chat will have code execution.
