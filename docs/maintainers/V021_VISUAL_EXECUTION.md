# v0.2.1 Visual Excellence — execution and release checklist

This candidate is **not an approved stable release**. All visual and marketing content requires owner review. Maintain the existing `main` checkout; apply the source package only after reviewing its differences, never replace `.git`.

## Implementation map

| Priority | Feature | Main files | Candidate status | Acceptance evidence |
|---|---|---|---|---|
| P0 | Theme-driven spatial grammar and two repeatable variants | `simplicity-builder/scripts/scene_art.py`; `tests/test_theme_composition_v021.py` | Implemented for five anchor families | Automated family coordinate, palette and variant checks; inspect the 8-world contact sheet |
| P0 | Volcanic crater, connected lava, ash, ember, warm grounded landmarks | `scene_art.py`, `simplicity-builder/examples/volcanic-sample.json`, `docs/volcanic.html` | Implemented procedural reference | Browser desktop/phone geometry and human assessment of distinctness |
| P0 | Ocean vertical depth, space orbit grammar, guardian citadel, toon ink and bold shapes | `scene_art.py`, `simplicity-builder/examples/toon-sample.json`, `docs/toon.html` | Implemented procedural fallback | Each family differs in coordinates, backdrop and palette; smoke and visual review |
| P0 | AI-authored safe SVG as preferred agent route; procedural fallback | `simplicity-builder/SKILL.md`, `simplicity-builder/references/scene-authoring.md`, SVG sanitizer/checker | Instructions and tool contract implemented; **host creates the art**, builder does not autonomously compose cinematic art | Test independent AI host creates *both* desktop/mobile safe SVGs and browser-reviews them |
| P0 | Cinematic source artwork under actual interactive landmarks | `simplicity-builder/scripts/build.py`, `build_portfolio.py`, `template.html` | Optional prior scenic-image route retained, with explicit aligned SVG required | Review original scenic image, mobile crop, clickable coordinates and offline HTML |
| P1 | Mandatory render–look–revise **when the AI host has a browser** | `SKILL.md`, `references/scene-authoring.md`, `scripts/browser_smoke.py` | Agent instructions implemented; not enforceable in hosts lacking browser access | Save and review actual screenshots; no unsupported visual-quality claims |
| P1 | Distinct layouts/palette regression checks | `tests/test_theme_composition_v021.py` | Implemented | Unit tests green |
| P1 | Volcanic and toon gallery/preview/baseline/browser coverage | `docs/index.html`, `docs/assets/*-preview.webp`, `.github/workflows/test.yml`, `tests/visual-golden/` | Implemented | 8 HTML outputs current; 40 viewport checks; manual acceptance of eight golden candidates |
| P1 | axe-core accessibility gate in GitHub Actions | `.github/workflows/test.yml`, `simplicity-builder/scripts/browser_smoke.py` | Integrated into CI; **axe itself unverified offline** | Install axe-core, execute the exact browser CI step, no accessibility violations |
| P1 | Visual contact sheet from real desktop + phone screenshots | `scripts/contact_sheet.py` | Implemented | Deterministic eight-world contact sheet, fail on missing screenshots |
| P2 | Subtle effects, themed plaques, larger footer, reduced motion | `simplicity-builder/assets/template.html`, `scene_art.py` | Implemented modestly | Browser prefers-reduced-motion checks, human legibility checks |
| P2 | Guided tour recording and public showcase draft | `scripts/record_tour.py`, `docs/assets/volcanic-tour.webm`, `docs/maintainers/LINKEDIN_SHOWCASE.md`, `README.md` | Real-browser recording generated, **not posted** | Owner approves content and future LinkedIn publishing |
| P2 | Keyword/theme precedence and documentation hygiene | `scene_art.py`, `README.md`, `SKILL.md`, `docs/maintainers/RELEASE_ACCEPTANCE.md` | Implemented by intent; original `fix-theme-matching.patch` was not supplied | Test franchise-style original toon, no technology match on `network`; review condensed docs |

## Important scope boundary

The user supplied cinematic generated artwork as the **visual ceiling**, not an automatic guarantee of the procedural renderer. The source now has original themed fallback compositions and an AI-authored scene specification, but one individually human-curated, cinematic gold-standard scene for **every** family is **not complete**. No installed code can guarantee a third-party AI host will make high-quality original art or have a browser. These are external visual acceptance tasks, not unit-test passes.

## Required pre-commit tests on Windows or a Linux workstation

```bash
python -m pip install -r requirements-dev.txt
python scripts/ci_preflight.py all
python -m unittest discover -s tests -v
python scripts/package_release.py --label v0.2.1
python -m playwright install chromium
python simplicity-builder/scripts/browser_smoke.py docs/fairytale.html docs/space.html docs/festival.html docs/clockwork.html docs/guardian.html docs/photo.html docs/volcanic.html docs/toon.html --screenshots private/screenshots
python scripts/contact_sheet.py --screenshots private/screenshots --output private/screenshots/contact-sheet.png --worlds fairytale space festival clockwork guardian photo volcanic toon
python scripts/check_visual_baselines.py --screenshots private/screenshots --tolerance 0.25
```

To match **GitHub accessibility CI**, also install `axe-core@4.10.3` with npm and add `--axe-script node_modules/axe-core/axe.min.js` to the browser smoke command. If unavailable, call the accessibility audit **unverified** (not passed).

## Human review and release gates

- [ ] Inspect the desktop/mobile contact sheet and individual large screenshots; accept the procedural art as meaningfully more diverse than v0.2.0.
- [ ] Confirm landmark labels, silhouettes, lighting, scaling, and no overlapping or cropped plaques on real devices.
- [ ] Review two distinct layouts on each principal family, not just generated scene counts.
- [ ] Test AI-host-authored SVG generation from a fresh résumé, original prompt and a source-neutral document; save both layouts and evidence that the host actually inspected screenshots.
- [ ] Review axe-core results and keyboard/screen reader usability; fix all serious violations rather than only raising tolerance.
- [ ] Confirm CI Ruff, mypy, full tests, all 11 browser HTML worlds, privacy checks and source archives pass **on the exact commit**.
- [ ] Confirm source contains no confidential or real résumé content, secrets, local output screenshots, caches or generated ZIPs before `git add -A`.
- [ ] Review Markdown links, current version, gallery and video, including any host-specific README claims.
- [ ] Check the GitHub Pages gallery **only after pushing**, and approve video/LinkedIn post separately.
- [ ] No release tag until external AI-chat output quality, real accessibility audit and user visual approval are complete.

## Simple direct-to-main workflow after acceptance

```bash
git switch main
git pull --ff-only origin main
# Preserve .git; overlay the approved update or complete source package.
python scripts/ci_preflight.py all
git status --short
git diff --check
git add -A
git diff --cached --stat
git diff --cached --check
git commit -m "Improve v0.2.1 theme-driven visual worlds and review gates"
git push origin main
```

Wait for GitHub Actions to finish and compare its tested commit SHA with `git rev-parse HEAD`; rerunning an old failed workflow does not verify a new commit.
