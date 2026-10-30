# SimpliCITY Builder ✦

**Your résumé tells your story. Your imagination builds its world.**

Turn a résumé and a creative prompt into a **working, explorable portfolio website**. Imagine a miniature solar system, fairytale kingdom, graffiti city, floating library—or a world no one has imagined yet.

SimpliCITY Builder is a free, open-source **Agent Skill and Python generator**. It produces a responsive, offline HTML portfolio with clickable illustrated landmarks, accessible navigation, and a recruiter view—not just an image.

**Version:** v0.1.5 · [See release acceptance and compatibility status](RELEASE_ACCEPTANCE.md)

**[Explore live demos](https://dishitkalsaria.github.io/SimpliCITY-Builder/)** · **[Use in an AI chat](#option-1-paste-the-link-and-prompt)** · **[Install the skill](#option-2-install-the-skill)** · **[Publish and share](#publish-and-share-optional)**

![Four fictional worlds created with SimpliCITY Builder](docs/assets/gallery-preview.webp)

## See what it builds

These are **interactive websites**, not screenshots or JSON previews. The sample inputs are fictional and the themes are examples—not a fixed catalog.

| World | Playable demo | Fictional source input |
|---|---|---|
| Fairytale kingdom | [Explore fairytale](https://dishitkalsaria.github.io/SimpliCITY-Builder/fairytale.html) | [JSON](examples/fairytale-sample.json) |
| Space / planets | [Explore space](https://dishitkalsaria.github.io/SimpliCITY-Builder/space.html) | [JSON](examples/space-sample.json) |
| Midnight festival | [Explore festival](https://dishitkalsaria.github.io/SimpliCITY-Builder/festival.html) | [JSON](examples/custom-sample.json) |
| Clockwork museum | [Explore clockwork](https://dishitkalsaria.github.io/SimpliCITY-Builder/clockwork.html) | [JSON](examples/clockwork-sample.json) |

The demos are served through GitHub Pages from `main` → `/docs`.

## Two ways to use it

### Option 1: Paste the link and prompt

In an AI assistant that can **retrieve repository files, read a résumé, run Python, and return downloadable files**, attach your résumé and paste:

```text
Use SimpliCITY Builder from https://github.com/DishitKalsaria/SimpliCITY-Builder.
Read AI_START_HERE.md and simplicity-builder/SKILL.md from the reviewed v0.1.5 source.
I've attached my résumé. SimpliCITY Builder, make me a floating city of planets in space.
Build and validate an interactive, downloadable HTML portfolio.
Do not invent career facts, show private contact details, or publish anything.
```

Replace the imaginative world phrase with any theme. **Pasting a URL does not install a skill or grant code-execution capabilities.** Review executable code and prefer the pinned `v0.1.5` tag rather than a mutable `main` branch. If a GitHub page cannot be fetched, see [trusted retrieval fallbacks](docs/LINK_ONLY.md) and [AI-host compatibility](COMPATIBILITY.md).

### Option 2: Install the skill

Install the [`simplicity-builder/`](simplicity-builder/) folder or the dedicated Skill ZIP from the matching GitHub Release in a compatible agent:

- **Claude:** Upload the Skill ZIP through custom Skills, where supported with code execution.
- **Claude Code:** Add `simplicity-builder/` under `.claude/skills/` in a project or user skill directory.
- **OpenAI Codex:** Add `simplicity-builder/` under `.agents/skills/` in a project or user skill directory.

Then upload your résumé and ask: **“SimpliCITY Builder, make me a fairytale land.”** See [INSTALL.md](INSTALL.md) for setup instructions and capability limits.

## What can I customize?

**The art is the navigation.** A career section belongs to a real illustrated SVG object (`id="landmark-<section-id>"`): a planet, saloon, windmill, creature, or crystal spire. Users select those objects directly—without icon pins or guessed screen coordinates. Keyboard navigation and a searchable location list are available as alternatives.

- **Any imagined setting:** World names, landmarks, story, colors, lighting, labels, and narrative copy come from the user's prompt and reviewed résumé data.
- **Richer career stories:** `highlights[]`, `metrics[]`, attributed `quote` entries, and customizable `world.copy` preserve readable details instead of merging everything into paragraphs.
- **Original artwork:** Safe SVG shapes, internal gradients, transforms, motion classes, reusable composition guidance, and an optional separately composed mobile scene (`world.scene_svg_mobile`).
- **Optional image-assisted mode:** An original PNG, JPEG, or WebP background can be embedded offline where the AI host or user supplies artwork; separate SVG landmarks remain interactive. Image generation is not required.
- **Factual safeguards:** The AI must review and map the résumé into structured JSON; `verify_facts.py` flags potentially unsupported claims. Exact matching is **not** proof of semantic truth.

See the [portfolio schema](simplicity-builder/references/portfolio-schema.md), [world rules](simplicity-builder/references/world-rules.md), [illustration rules](simplicity-builder/references/illustration-rules.md), and [art-direction guidance](simplicity-builder/references/art-direction.md).

## Testing locally

The JSON-to-HTML generator requires **Python 3.9+** and has no mandatory pip dependencies. From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 simplicity-builder/scripts/build_portfolio.py --input examples/fairytale-sample.json --output fairytale-demo.html
python3 simplicity-builder/scripts/validate.py examples/fairytale-sample.json fairytale-demo.html
```

Open `fairytale-demo.html` in your browser. For optional real-browser checks and screenshots, install Playwright and Chromium:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/browser_smoke.py fairytale-demo.html --screenshots private/screenshots
```

A local résumé text extractor is available for TXT/DOCX, and for **text-based** PDF with optional `pypdf`. It extracts text; it does not interpret qualifications. Scanned PDFs require OCR or pasted text. See [TESTING.md](TESTING.md) and [résumé review rules](simplicity-builder/references/resume-review.md).

## Publish and share (optional)

**Nothing is made public automatically.** After the owner reviews the portfolio and approves the public content, the publisher can prepare a GitHub Pages bundle and a LinkedIn-sized social-preview image:

```bash
python3 simplicity-builder/scripts/publish_portfolio.py prepare \
  --html fairytale-demo.html --account YOUR_GITHUB_USERNAME \
  --repo my-career-world --out private/publish-ready
```

This creates files for an optional deployment; **it does not upload or post anything**. GitHub Pages hosts the interactive site, while LinkedIn displays a clickable link preview (not an interactive embed). Publication requires explicit approval; authorized GitHub CLI deployment is optional. See [PUBLISHING.md](PUBLISHING.md).

## Repository guide

| Path | Purpose |
|---|---|
| [`AI_START_HERE.md`](AI_START_HERE.md) | Agent entry point for link + prompt |
| [`simplicity-builder/SKILL.md`](simplicity-builder/SKILL.md) | Installable portable Agent Skill |
| `simplicity-builder/references/` | Résumé schema, evidence review, world and illustration rules |
| `simplicity-builder/scripts/` | Generator, validator, résumé extraction and publishing tools |
| `simplicity-builder/assets/template.html` | Responsive standalone website template |
| `examples/` | Fictional inputs—no personal résumés |
| `tests/` | Unit, schema, SVG, evidence, publishing and regression tests |
| `docs/` | GitHub Pages four-world demo gallery |
| `.github/workflows/test.yml` | Automated checks for pushes and pull requests |
| [INSTALL.md](INSTALL.md) | Installing and invoking the skill |
| [COMPATIBILITY.md](COMPATIBILITY.md) | AI-host support, including unverified paths |
| [TESTING.md](TESTING.md) | Local tests, browser QA and limitations |
| [PUBLISHING.md](PUBLISHING.md) | Owner-approved GitHub Pages and LinkedIn sharing |
| [RELEASING.md](RELEASING.md) | v0.1.5 tags, package generation and checksums |
| [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md) | External testing criteria and remaining gates |

## Accessibility and visual quality

Across **desktop, tablet, and mobile**, visitors navigate with clickable, keyboard-focusable, clearly labelled named SVG objects. The main page remains within the viewport, with **no vertical or horizontal document scrolling**. Location search, long career details and recruiter content can scroll *inside* accessible panels. The site respects reduced-motion preferences and provides a print-friendly recruiter view.

Automated browser tests check functional interactions and layout errors. **Screenshots still need human review** for legibility, composition, thematic coherence and mobile polish.

## Privacy, accuracy and security

Résumé uploads are subject to the **AI host's privacy policies**. The local generator and résumé extractor do not upload files. Their HTML output contains **no trackers, analytics, remote fonts or external runtime dependencies**. Optional publishing tools may access GitHub **only with the owner's explicit authorization**.

Contact details are excluded by default. All career facts must remain grounded in the résumé; imaginative locations never justify inventing credentials, metrics or achievements. The evidence verifier reports possible inconsistencies but does not guarantee factual truth. SVG artwork is sanitized against scripts and remote resources.

**Review the generated site, personal details, art and links before publishing.** Never commit original résumés, extracted private text or fact-review reports to public GitHub repositories. See [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits, license and distribution

Created and maintained by **[Dishit Kalsaria](https://github.com/DishitKalsaria)**, creator of the original [Simpli-City interactive portfolio](https://dishitkalsaria.github.io/Simpli-City/) ([source](https://github.com/DishitKalsaria/Simpli-City)). The original portfolio remains the personal flagship; SimpliCITY Builder is the reusable skill. **SimpliCITY Studio** is a possible future platform, not part of this release.

Released under the [MIT License](LICENSE). © 2026 Dishit Kalsaria.

**Distribution and trust:** Use the immutable `v0.1.5` tag, package the installable Skill ZIP from that tagged commit, publish SHA256 checksums with the release, and record external AI-host results before claiming universal compatibility. See [RELEASING.md](RELEASING.md).
