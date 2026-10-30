---
name: simplicity-builder
description: Turn an attached résumé or CV and a freely imagined world prompt into a truthful, clickable, no-page-scroll portfolio website. Use for "SimpliCITY Builder", "make my résumé a fairytale land", cosmic portfolio, fantasy, graffiti or any invented world. Generate and validate downloadable HTML, not just a mockup.
license: MIT
compatibility: Python 3.9+, local files and code execution for building; host must read an uploaded résumé. Optional Chromium browser testing.
metadata:
  author: Dishit Kalsaria
  version: "0.1.2"
---

# SimpliCITY Builder v0.1.2

**Promise:** Your résumé tells your story. Your imagination builds its world.

## Execute this workflow

1. Read the user's attached résumé via host tools or local `scripts/extract_resume.py`. For DOCX/TXT, stdlib is sufficient; a text PDF needs optional `pypdf`. Scanned PDFs require OCR or pasted text. Read `references/resume-review.md`. Never manufacture qualifications, numbers, employers, endorsements, dates or links. Do not echo private résumé data in logs.
2. Interpret **any** user theme. A space voyage, fairyland, clockwork ocean, musical jungle, etc. are all allowed. Compose a distinctive `world.scene_svg` illustration and title, location metaphors, open-ended colors, `world.copy`, and `world.hotspots` (one labelled location per section). Never constrain people to starter themes. Use original unbranded art when a request references protected characters, logos or franchises, and tell the user of the substitution. See `references/world-rules.md` and `references/art-components.md`.
3. Ground `portfolio.json` in the résumé. Maintain real roles, projects, dates, skills, evidence-based metrics, bullet highlights, attributed quotes (when documented), and optional user-approved public links. See `references/portfolio-schema.md`. Use only confirmed data and omit contact details by default. Fact verification is necessary but not sufficient. Create a private résumé evidence report, especially for numbers and endorsements. For any ambiguous fact, omit or mark for owner review.
4. **World navigation is essential.** The map has accessible named hotspots tied to each section; the location list and recruiter view are fallbacks. The document MUST NOT vertically or horizontally scroll at desktop or mobile sizes. Longer detail content may scroll *within accessible modal panels*. Every hotspot must have an understandable accessible label and visible title. Do not make badges float over the scene; the surrounding header/footer are safe zones.
5. Generate inert SVG (max 25,000 characters) using the accepted shapes and internal gradients. Safe styles are bundled as CSS classes (`motion-float`, `motion-twinkle`, `motion-drift`, `motion-pulse`); no user-supplied CSS/JavaScript. Respect reduced motion. Preflight `scene_svg` with `scripts/check_artwork.py` and consult `references/illustration-rules.md`.
6. Locally save `portfolio.json` and extracted résumé text in a private working folder. Run from the skill folder (adjust paths):

   ```bash
   python3 scripts/verify_facts.py --input /path/to/portfolio.json --resume-text /path/to/private-resume.txt --strict --report /path/to/private-review.json
   python3 scripts/build_portfolio.py --input /path/to/portfolio.json --output /path/to/index.html
   python3 scripts/validate.py /path/to/portfolio.json /path/to/index.html
   ```

   If strict evidence checking flags accurate paraphrases/false positives, investigate and record the owner's review; never simply disable it and declare all facts validated. The report tests exact tokens, **not semantic truth**.
7. Test desktop, mobile and compact sizes in real Chromium when possible: from repo root `python3 scripts/browser_smoke.py /path/to/index.html --screenshots /path/to/private/screenshots`. Inspect screenshots manually for visual coherence, labels/overlap, contrast and factual relevance. If browser tools are missing, disclose this.
8. Deliver a downloadable single offline `index.html` and optional JSON. The page must work with no external trackers, fonts or CDN. Do not publish automatically. Ask the owner to review facts and personal information before sharing.

## Quality gates

- **No-page-scroll** at supported device widths; internally scrolling dialogs permitted for accessible long content, printing exempt.
- Hotspots are the primary navigation and each has keyboard focus and clear labelled destination.
- Responsive mobile scene plus searchable locations and recruiter/print view.
- `world.copy` allows all narrative interface labels to be customized. User-provided theme controls scene, art, colors and metaphor.
- Résumé bullets via `highlights`, numerical evidence via `metrics`, endorsements via grounded `quote` entries.
- No invented accomplishments, no silent omission of major résumé sections, no unlicensed logos or character replicas.
- Browser execution is required for an actual UI test. Link-only use works only with repo/file access and code execution, never universally.

Skill entry points: "SimpliCITY Builder, make me a fairytale land"; "Build an underwater career archipelago from my résumé"; "Transform my CV into a neon music-world".
