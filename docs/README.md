# GitHub Pages demo gallery

This folder hosts a **demo gallery** at `index.html` and eleven linked, standalone, interactive experience samples:

- `fairytale.html` generated from `docs/demo-inputs/fairytale-sample.json`
- `space.html` generated from `docs/demo-inputs/space-sample.json`
- `festival.html` generated from `docs/demo-inputs/custom-sample.json`
- `clockwork.html` generated from `docs/demo-inputs/clockwork-sample.json`
- `photo.html` generated from `simplicity-builder/examples/photo-sample.json` and the synthetic image
- `guardian.html` generated from `simplicity-builder/examples/guardian-academy.json` (fictional prompt; new source-neutral input)

An additional, unlisted **v0.2.1 volcanic visual-reference candidate** lives at `volcanic.html`, generated from `simplicity-builder/examples/volcanic-sample.json`. It is intentionally not promoted in the public gallery until the owner approves the art.

The JSON files are **developer input**, not the visitor-facing demo. Screenshots in `assets/` are captured from the actual generated HTML. All sample profiles are fictional.

After uploading the folder, enable Pages (this cannot be confirmed automatically here) in Settings → Pages → Deploy from a branch → `main` → `/docs`. The gallery then lives at <https://dishitkalsaria.github.io/SimpliCITY-Builder/>.

To regenerate a résumé example from repository root:

```bash
python3 simplicity-builder/scripts/build.py --input docs/demo-inputs/fairytale-sample.json --output docs/fairytale.html
```

Do not replace the demos with real people’s résumé content without approval. If you modify the generator or sample inputs, regenerate the affected HTML and preview image.

To regenerate the v0.2.1 general-input demo: `python3 simplicity-builder/scripts/build.py --input simplicity-builder/examples/guardian-academy.json --output docs/guardian.html`. Screenshots are actual browser captures; visual inspection remains necessary.

**Share metadata:** `docs/demo-inputs/` is the only place that stores demo-specific canonical/share URLs. Reusable `examples/` and installable skill fixtures deliberately omit `world.share` so copying an example never points a new portfolio back at this demo gallery.

The v0.2.1 environment-first expansion adds `meeting-room.html`, `playground.html` and `farm.html`, generated respectively from `simplicity-builder/examples/{meeting-room,playground,farm}-sample.json`. These are procedural fallback examples, **not cinematic-quality certifications**. Each includes accessible clickable objects and independently composed portrait SVGs.
