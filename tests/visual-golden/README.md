# Manually reviewable browser screenshot baselines

These four Chromium screenshots were captured from the **fictional, generated** guardian and synthetic-photo examples at fixed 1440×900 desktop and 390×844 mobile viewports. They are a qualitative reference, not evidence that arbitrary photos or AI art are understood.

To compare optional new screenshots after installing Pillow, run `python3 scripts/compare_screenshots.py tests/visual-golden/photo-mobile.png private/screenshots/photo-mobile.png --max-changed 0.15`. Difference is a **review alert**, not automatic aesthetic approval; browser/font differences can cause noise. Update baselines only after explicit visual acceptance.

**v0.2.0 last-touch candidate:** These regenerated golden images still require repository-owner visual approval before merge or release. Passing a pixel-difference gate is not an artistic-quality certification.
