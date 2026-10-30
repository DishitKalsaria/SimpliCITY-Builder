# SimpliCITY Builder ✦

**Your résumé tells your story. Your imagination builds its world.**

Turn a résumé + a creative prompt into an **interactive, mobile-friendly portfolio**. Walk through planets, enchanted buildings, floating islands—or any world you imagine. Click illustrated landmarks to explore real career stories.

**Version:** v0.1.5 · **Release candidate** (external agent testing pending)

[**Explore live demos**](https://dishitkalsaria.github.io/SimpliCITY-Builder/) · [**Install the skill**](INSTALL.md) · [**Publish & share**](PUBLISHING.md)

![Four fictional worlds created with SimpliCITY Builder](docs/assets/gallery-preview.webp)

## Try it with a link

Upload your résumé to a capable AI assistant, then paste:

```text
Use SimpliCITY Builder from https://github.com/DishitKalsaria/SimpliCITY-Builder.
Read AI_START_HERE.md and simplicity-builder/SKILL.md from a reviewed version.
Make me a floating city of planets from my attached résumé.
Generate and validate a downloadable interactive HTML portfolio.
Keep facts accurate, exclude private contact details and do not publish it.
```

**Requirements:** The AI must be able to retrieve repository files, read the résumé, run Python and return a file. A GitHub URL alone does **not** install or activate a skill. Use [link-only instructions](docs/LINK_ONLY.md) if retrieval is blocked.

Alternatively, [install the skill](INSTALL.md) in a supported coding agent and say **“SimpliCITY Builder, make me a fairytale land.”**

## See what it builds

| World | Interactive site | Fictional source input |
|---|---|---|
| Fairytale | [Explore](https://dishitkalsaria.github.io/SimpliCITY-Builder/fairytale.html) | [JSON](examples/fairytale-sample.json) |
| Space | [Explore](https://dishitkalsaria.github.io/SimpliCITY-Builder/space.html) | [JSON](examples/space-sample.json) |
| Music festival | [Explore](https://dishitkalsaria.github.io/SimpliCITY-Builder/festival.html) | [JSON](examples/custom-sample.json) |
| Clockwork museum | [Explore](https://dishitkalsaria.github.io/SimpliCITY-Builder/clockwork.html) | [JSON](examples/clockwork-sample.json) |

Examples are illustrative, **not preset restrictions**. Publishing the live demo gallery requires GitHub Pages enabled on `main` → `/docs`.

## Create locally

Requires Python 3.9+; the generator itself has no pip dependencies.

```bash
python3 -m unittest discover -s tests -v
python3 simplicity-builder/scripts/build_portfolio.py --input examples/space-sample.json --output space-demo.html
python3 simplicity-builder/scripts/validate.py examples/space-sample.json space-demo.html
```

Open `space-demo.html` in your browser. Optional visual/interaction testing uses Chromium and Playwright; see [TESTING.md](TESTING.md).

## Publish and share (optional)

Once **you have approved all public résumé information**, prepare a GitHub Pages-ready site and LinkedIn preview:

```bash
python3 simplicity-builder/scripts/publish_portfolio.py prepare \
  --html space-demo.html --account YOUR_GITHUB_USERNAME \
  --repo my-career-world --out private/publish-ready
```

This creates **`site/index.html`, `site/social-preview.jpg`, a publication checklist, and a draft LinkedIn post**. It does **not upload anything**. A preview screenshot requires optional Playwright; alternatively supply `--preview your-image.jpg`.

You can upload the `site/` contents manually to GitHub Pages or use the **explicitly approved** GitHub CLI flow. See [PUBLISHING.md](PUBLISHING.md). Visitors explore the live world by clicking the LinkedIn preview; it cannot run directly inside a LinkedIn post.

## What makes it different?

- **World-first navigation:** The illustrated objects themselves are clickable SVG landmarks—not icon pins or a themed card list.
- **No-page-scroll exploration:** The world fills the screen; long details scroll inside accessible panels. Includes mobile layouts, keyboard access, search and recruiter view.
- **Freedom to imagine:** Original SVG artwork, safe animation and optional image-assisted backgrounds. No fixed theme library.
- **Truth and privacy:** Résumé evidence checks, no invented achievements, no trackers, and no automatic publishing.
- **Portable:** A standalone offline HTML file, with no remote runtime dependencies.

## Guides

[Install](INSTALL.md) · [AI-agent instructions](AI_START_HERE.md) · [Publishing & LinkedIn](PUBLISHING.md) · [Testing](TESTING.md) · [Compatibility](COMPATIBILITY.md) · [Schema](simplicity-builder/references/portfolio-schema.md) · [Security](SECURITY.md) · [Release process](RELEASING.md)

**Creator:** [Dishit Kalsaria](https://github.com/DishitKalsaria) · [Original Simpli-City portfolio](https://dishitkalsaria.github.io/Simpli-City/) · [MIT License](LICENSE). SimpliCITY Studio is a possible future platform, not a feature of this skill.

**Release status:** v0.1.5 is for external acceptance testing. GitHub Actions/unit tests and sample browser checks are necessary, but real résumé-to-world workflows in target AI apps must be verified before declaring it stable. See [Release acceptance](RELEASE_ACCEPTANCE.md).
