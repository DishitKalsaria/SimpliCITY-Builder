# v0.2.1 quality-hardening audit

**Status:** Updated v0.2.1 release candidate. No deployment, release tag, or visual redesign was performed.

## Non-negotiable product principles

1. **Environment-first, never template-constrained.** The Builder must support scenes from meeting rooms and farms to fantasy worlds, while keeping interactable objects semantically appropriate to their environment.
2. **Preserve exact output during code cleanup.** Refactoring and quality fixes must not silently alter a scene, reposition landmarks, or change screen-reader interaction.
3. **Source-grounded or explicitly fictional.** Do not fabricate real-world facts, photo observations or résumé accomplishments to fill a scene.
4. **Offline-first and portable.** A generated viewer should not need a subscription, network session or new runtime package; development dependencies stay optional.
5. **Human-controlled publishing.** Preparing a local public bundle is separate from uploading. Deployment requires explicit approval, correct authenticated ownership and safeguards against overwriting repositories.
6. **Visual quality is judged in the browser.** Passing collision, sizing and accessibility tests is necessary but does not certify a compelling composition.

## Corrections made in this patch

- Removed the three `E702`-causing semicolon assignments in `scene_art.py` without altering their calculations.
- Removed unused imports (including `build.py`'s unused theme imports) and a duplicated import in the tests.
- Marked the `build_portfolio.py` validation helper as `NoReturn`, improving static narrowing for rejected inputs, and included the file in the pre-push mypy target set.
- Consolidated multiple v0.2.1 changelog headings and corrected contribution and gallery/browser documentation.
- Added in-process build, check and experience validation tests and mocked publishing-deployment tests for approval, GitHub ownership, existing repository protection, public output restrictions and failed Pages setup.
- Added release-consistency checks for the single-version changelog, 11-demo gallery, CI coverage and Python 3.9 syntax parsing.

## Completed checks (local run)

| Check | Result |
| --- | --- |
| Python `unittest discover` | **141 passed** |
| In-process unit-test coverage across builder scripts | **76%** (reported earlier: 67%) |
| `publish_portfolio.py` coverage | **84%** (reported earlier: 51%) |
| Browser smoke (11 demo worlds × 5 viewports) | **55 passed** |
| Browser scene matrix (16 supported families, new environments 1–8 landmarks) | **250 passed** |
| Stored visual baselines | **8 passed, 0% changed pixels locally** |
| Generated HTML compared with original v0.2.1 archive | **6/6 byte-identical** (meeting room, playground, farm, guardian, space, volcanic) |
| Static unused-import scan | **No findings** |
| Semicolon token check for `scene_art.py` | **No findings** |
| Python 3.9 AST syntax parse for installed scripts | **Passed** |

## Release gates not yet certified

- **Ruff and mypy:** The exact pinned binaries could not be installed in the offline review environment. `python scripts/ci_preflight.py all` must be rerun with `requirements-dev.txt` installed before pushing. The original E702 lines have been removed and the reported mypy narrowing errors addressed, but neither result is represented as a successfully executed Ruff/mypy run.
- **Default Ruff style rules:** The original audit reported approximately 347 broad style findings. The patch removes dead imports and CI-breaking semicolons, **not** every legacy long line and one-line statement. Broad reformatting should be a separate behavior-preserving review, not blended into environment functionality changes.
- **axe-core:** Not available for this local browser run; GitHub Actions installs axe-core and runs the mandatory accessibility check.
- **Browser checker in-process coverage:** `browser_smoke.py` still measures only 19% under the Python unit coverage configuration. Its main scenarios are instead executed in the separate browser job; this is a measurement boundary, not a claim that the browser checks are missing.
- **Actual deployment:** Only mocked publishing was exercised. GitHub ownership and Pages publication require explicit human approval and live external verification.
- **Artistic acceptance:** No claim of bespoke cinematic excellence is made for the procedural SVG fallback. Owner review of representative and unfamiliar worlds remains required.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python scripts/ci_preflight.py all
coverage run --source=simplicity-builder/scripts -m unittest discover -s tests -q
coverage report
python simplicity-builder/scripts/browser_smoke.py docs/fairytale.html docs/space.html docs/festival.html docs/clockwork.html docs/guardian.html docs/photo.html docs/volcanic.html docs/toon.html docs/meeting-room.html docs/playground.html docs/farm.html --screenshots private/screenshots --axe-script node_modules/axe-core/axe.min.js
python scripts/check_environment_matrix.py
python scripts/check_visual_baselines.py --screenshots private/screenshots --tolerance 0.25
python scripts/package_release.py --label v0.2.1
```

**Review standard:** do not treat this candidate as CI-approved until the Ruff, mypy and axe-core gates pass in the actual deployment environment, and the human owner approves the rendered visuals.
