# GitHub Pages demo

This directory hosts a fully generated, **fictional** sample portfolio at `index.html`, with its screenshot in `assets/`.

After pushing the repository, enable GitHub Pages in Settings → Pages → Build and deployment → Deploy from a branch, branch `main`, folder `/docs`. The public demo URL will be `https://dishitkalsaria.github.io/SimpliCITY-Builder/` once Pages has deployed.

To regenerate this demo locally:

```bash
python3 simplicity-builder/scripts/build_portfolio.py --input examples/fairytale-sample.json --output docs/index.html
```

Do not replace `docs/index.html` with a portfolio built from someone's real résumé without approval.
