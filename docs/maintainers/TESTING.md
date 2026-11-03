# SimpliCITY Builder v0.2.0 — testing

## Core regression and standalone package (Python 3.9+, stdlib only)

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py --tag v0.2.0 --output simplicity-builder.zip
mkdir -p /tmp/simplicity-install
cd /tmp/simplicity-install && unzip -q /path/to/repo/simplicity-builder.zip
python3 simplicity-builder/scripts/build.py --input simplicity-builder/examples/fairytale-sample.json --output demo.html
python3 simplicity-builder/scripts/check.py simplicity-builder/examples/fairytale-sample.json demo.html
python3 simplicity-builder/scripts/build.py --input simplicity-builder/references/experience-sample.json --output exhibit.html
python3 simplicity-builder/scripts/check.py simplicity-builder/references/experience-sample.json exhibit.html
```

The tests cover legacy résumé inputs, source-neutral content, theme families, SVG safety, publishing safeguards, metadata versions and package portability. A passed HTML validator does not mean the agent understood a document/photo or that the scene is artistically finished.

## Required pre-push CI parity checks for contributors

Run **before committing**, particularly on Windows. This reproduces the exact Ruff selector and mypy targets used by GitHub Actions, followed by the unit tests. It fails if required developer tools are missing instead of silently skipping them.

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/ci_preflight.py all
```

For source/commit comparisons without installing tools: `python3 scripts/ci_preflight.py fingerprint`. The preflight prints SHA256 for both type-checked files; compare these hashes against your local Git commit and the commit hash displayed by GitHub Actions. The script shares its lint/type commands with the workflow to avoid local/CI drift.

The developer tools are **not runtime dependencies**. The generator itself uses Python's standard library. For the separate coverage check used by CI:

```bash
coverage run --source=simplicity-builder/scripts -m unittest discover -s tests -q
coverage report
```

## Photo and one-item smoke tests

```bash
python3 simplicity-builder/scripts/build.py --input simplicity-builder/examples/photo-sample.json --source-image simplicity-builder/examples/synthetic-lakeside.png --output private/photo.html
python3 simplicity-builder/scripts/check.py simplicity-builder/examples/photo-sample.json private/photo.html
python3 simplicity-builder/scripts/build.py --input simplicity-builder/examples/link-sample.json --output private/featured.html
python3 simplicity-builder/scripts/check.py simplicity-builder/examples/link-sample.json private/featured.html
```

The photo fixture is deliberately synthetic and includes host-supplied observed object boxes. Omitting `--source-image` or an object `anchor` must fail. Real photographs and live URL extraction still require compatible AI host tools.

## Browser visual QA (optional)

```bash
python3 -m playwright install chromium
python3 simplicity-builder/scripts/browser_smoke.py docs/fairytale.html docs/space.html docs/festival.html docs/clockwork.html docs/guardian.html private/photo.html private/featured.html --screenshots private/screenshots
```

If Chromium or Playwright is missing, explicitly report the browser test as skipped. Inspect screenshots manually for theme recognition, readable hint/footer text, landmark silhouettes, focus/hover, mobile clipping and excessive generic art. Run desktop, small phone, landscape and keyboard interactions; long dialogs may scroll internally but the document should not.

## Publishing and external acceptance

Test prepare mode using fictional data; the `prepare` command never deploys:

```bash
python3 simplicity-builder/scripts/publish_portfolio.py prepare --html docs/space.html --account DemoUser --repo demo-world --preview docs/assets/space-social.jpg --out private/test-publish
```

Do not run `deploy` on a real account without owner approval. [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) covers cross-host chat inputs, live GitHub Pages URLs, screenshots, installation and privacy checks. Actual AI host and link retrieval compatibility must be recorded, not inferred from CI.

## v0.2.0 polished browser and privacy acceptance

The stdlib generator can run without any optional packages. For visual tests, install pinned `playwright==1.57.0` and Chromium. The browser checker measures 44px targets, visible plaques, plaque-to-plaque and plaque-to-landmark collisions, edge-fill presence, source-anchor alignment, mobile photo coverage (at least 55%), and header/contrast issues. **These are geometry/proxy checks, not a visual-quality or factual-truth certificate.** The GitHub workflow also runs deliberately broken pages that must FAIL their checks.

```bash
python3 simplicity-builder/scripts/browser_smoke.py docs/guardian.html docs/photo.html --screenshots private/screenshots
python3 scripts/check_visual_baselines.py --screenshots private/screenshots --tolerance 0.25
```

**To explicitly refresh goldens after reviewing desktop/mobile screenshots**, run:

```bash
python3 scripts/update_visual_baselines.py --screenshots private/screenshots --accept
```

Review the resulting tracked PNG changes before committing. Browser/font/OS differences can trigger false positives; CI's 25% changed-pixel tolerance should not be adjusted without investigating. Golden comparison is required in CI, but does not substitute for manual image review. The photo and guardian fixtures are fictional/synthetic.

**Optional local axe-core:** obtain `axe.min.js` from a trusted installation and run `python3 simplicity-builder/scripts/browser_smoke.py docs/guardian.html --axe-script /path/to/axe.min.js`. If unavailable, the checker explicitly prints `SKIP axe-core`. Interactive SVG landmarks must be reachable by Tab and have accessible names. Visible plaques are text labels of those focusable landmarks, not separate focus stops.

**Private factual review:** `python3 simplicity-builder/scripts/build.py --input /path/to/content.json --output /tmp/index.html --review-sheet private/review.md --source-text private/extracted.txt`. Keep `private/` out of static publishing paths. The review lists source excerpts, anchors, dates/numbers and open questions, and states that passing evidence checks does **not** establish semantic truth.
