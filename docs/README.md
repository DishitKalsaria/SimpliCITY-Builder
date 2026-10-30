# GitHub Pages demo gallery

This folder hosts a **demo gallery** at `index.html` and four standalone, interactive portfolio samples:

- `fairytale.html` generated from `examples/fairytale-sample.json`
- `space.html` generated from `examples/space-sample.json`
- `festival.html` generated from `examples/custom-sample.json`
- `clockwork.html` generated from `examples/clockwork-sample.json`

The JSON is **developer input**, not the visitor-facing demo. Screenshots in `assets/` are captured from the actual generated HTML. All sample profiles are fictional.

After uploading the folder, enable Pages in Settings → Pages → Deploy from a branch → `main` → `/docs`. The gallery then lives at <https://dishitkalsaria.github.io/SimpliCITY-Builder/>.

To regenerate an example from repository root:

```bash
python3 simplicity-builder/scripts/build_portfolio.py --input examples/fairytale-sample.json --output docs/fairytale.html
```

Do not replace the demos with real people’s résumé content without approval. If you modify the generator or sample inputs, regenerate the affected HTML and preview image.
