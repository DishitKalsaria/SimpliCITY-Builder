# Changelog

## v0.2.1 — Environment-first visual refinement (unreleased candidate)

### Release quality and maintainability hardening

- Hardened dense 7–8-object plaque widths on narrow phones, and added a second collision-safe placement order when the standard pass leaves a label unplaced.
- Browser QA now waits for font readiness before measuring; added five targeted plaque stress cases to the browser CI gate without reducing distance, clipping or overlap requirements.

- Closed the remaining v0.2.1 style and stale-gallery-documentation gaps; aligned mypy target to CI Python 3.11 while keeping the Python 3.9+ runtime contract.
- Added direct CLI artwork-sanitizer and browser-smoke assertions to cover validation, failure states, viewport checks and opt-in accessibility.
- Expanded compact one-line suites and semicolon statements into reviewable blocks without changing Python syntax trees or generated scenes.
- Corrected all three scene generator semicolon lint violations; removed unused imports and duplicate test imports without changing generated HTML output for the representative six-world comparison.
- Expanded the existing type-check gate to include the portfolio generator and marked its raising validation helper `NoReturn` so invalid inputs stay rejected with correctly narrowed types.
- Strengthened offline, mocked publishing tests for explicit approval, matched GitHub account/repository metadata, existing repositories, public-bundle boundaries, and local error recovery.
- Added in-process build/check/experience-validation tests for more meaningful coverage, a Python 3.9 syntax guard, and release-document consistency tests.
- Consolidated v0.2.1 changelog entries into a single version heading; corrected contribution instructions and the 11-demo versus eight-baseline distinction in testing documentation.

### Environment-first scenes, layouts and browser coverage

- Expanded procedural scene generation to meeting rooms, playgrounds and agricultural farms, with scene-specific layouts, interior/exterior depth, coherent materials and chapter-aware object silhouettes.
- Corrected scaled landmark placement for 5–8 sections without disturbing the approved four-object legacy scene layouts; added compact seven/eight-object phone plaques and a visible small-phone tour icon.
- Changed theme classification to token-boundary matching to avoid terms such as `smart` accidentally selecting `art`/festival themes.
- Added three standalone fictional interactive demos and reusable inputs; added a browser scene-matrix script and unit regression coverage for 1–8 landmarks.
- Visual quality remains subject to owner review; offline SVG is not claimed to provide bespoke cinematic artwork for arbitrary prompts.

### Theme art-direction and visual refinement

- Added family-specific landscape grammars, placement variants, matching color/material constraints and terrain-based landmark foundations for volcanic, ocean, space, guardian and original toon worlds.
- Promoted AI-authored desktop/mobile safe SVG to the host-preferred experience, with a concise scene-authoring reference, mandatory render/look/revise when browser tools exist, and honest fallback declarations.
- Added toon and volcanic interactive demos with actual preview captures, an original browser tour recording, and a gallery contact-sheet generator.
- Extended browser CI to eight demos, axe-core WCAG checks, and eight visual regression candidates; final visual-owner approval and GitHub Actions remain release gates.
- Shortened README; split long artwork guidance in SKILL.md; updated golden baseline documentation and removed technology-family `network` matching.

### Visual definition and scenic-image workflow

- New volcanic visual family with differentiated interactive citadel, forge, observatory and refinery landmarks.
- Richer cinematic procedural scene grammar: textured atmosphere, themed terrain, distant ridge structures, environmental lighting, connected destinations and architectural landmark foundations.
- Portrait-specific terrain distribution retained; authored photo experiences remain image-anchored and unchanged.
- Adds optional first-class `--scenic-image` for reviewed scenery-only art with mandatory authored desktop/mobile SVG landmark layouts; source-photo anchoring stays separate.
- Fixes unintended source-photo pan/fit resizing of non-photo scenic images, keeping scenic art full-bleed.
- No remote image API, JavaScript dependency or change to factual source-grounding; scenic composition remains subject to human visual approval.
- Updated live demo output candidates and visual checks; human visual approval is still required before release.

## v0.2.0 — Chat-first, source-neutral interactive experiences (implementation; stable release pending acceptance)

- Final visual/trust correction: collision-aware name plaques with free-space placement; full-bleed ambient scene layers, mobile photo crop/fit and object navigator, responsive title; hard photo-box area/overlap guards and new negative Chromium tests.
- Source-photo privacy: stdlib JPEG APP1/APP13, PNG EXIF/text and WebP EXIF/XMP stripping without pixel re-encoding; optional Pillow downscale to 2000px; 10 MB sanitized image / 16 MB HTML caps and privacy warnings.
- `--review-sheet` creates a private factual/anchor/numeric review record. Résumé chat flow saves private extracted text for source evidence comparison when available. A successful check never certifies factual truth.
- Guided Start / Previous / Next / Exit tours, optional `--theme` re-rendering, desert and noir theme packs, optional local axe-core audits, golden screenshot CI comparisons and explicit baseline-update script.

- Visual-experience correction: actual photo-bound objects with normalized, responsive source-image anchors (missing image/anchors fail); always-visible name plaques; single-item featured-story UI; natural copy and consistent offline typography. Adds full-stage scenes, automatically composed portrait mobile art, depth layers, per-family colors and distinct landmark motifs, contact shadows and subtle lighting; extends optional browser geometry/contrast checks and source-photo demo.
- Adds one unified `build.py` / `check.py` command pair for both schemas; the older script names remain compatible. Source-neutral factual items require evidence excerpts or observed photo details, with optional private source-text comparison and numeric cross-checks.
- Moves maintainer-only documentation under `docs/maintainers/`, tests both schemas in tag-release CI, and removes franchise references from public skill metadata.
- Adds `source/experience/chapters` input for a reviewed photo, document, accessible link, résumé or fictional prompt; preserves the legacy résumé JSON generator and offline HTML output.
- Adds World, Explore and Explain presentation modes, with original theme-aware procedural SVG fallback families (superhero/guardian, space, nature, ocean, museum, technology, fantasy and festival) and optional host-provided original SVG/raster art. No image-generation model is bundled.
- Chat-first execution guidance: direct host attachment reading; one-question theme fallback; independent build/validation; downloadable HTML; optional quality pass and opt-in sharing only.
- Self-contained skill ZIP includes browser checker, new source-neutral builder/validator, fictional examples and existing publishing/verification tools.
- Aligns metadata, docs and release tooling to v0.2.0; adds tag-checked automated GitHub Release packaging, portability tests, optional development checks, and refreshed accessibility/contrast text.
- Documents unsupported host capabilities, link retrieval trust, gallery verification and stable-release acceptance requirements without claiming external testing completed.

### Final development-branch touch-ups (unreleased v0.2.0)

- Kept visible name plaques within measured distance of their landmark; removed distant fallback rails; added negative tests for detached plaques and clipped owner subtitles.
- Rebuilt procedural mobile scenes on a portrait viewBox with larger, vertically distributed landmarks; isolated foreground interactive objects from edge-to-edge scenery to remove fitted-scene seams.
- Curated synthetic photo anchor to include all illustrated mountain peaks; photo crop now labels the focused object and retains access to other objects through the photo navigator. Semantic anchor accuracy still requires visual review.
- Moved gallery-specific `world.share` URL/image metadata into `docs/demo-inputs/`, keeping reusable and installable samples neutral.

- Restored full-depth ambient scene layers and round celestial bodies across desktop/mobile viewports. Improved mobile photo framing with restrained context crop.

## v0.1.5 — Public release

- Optional opt-in GitHub Pages publication bundle with local social preview screenshot, Open Graph/Twitter-card metadata, and editable LinkedIn draft.
- Optional authorized `gh` deployment to a *new* user-owned repository; fails closed without explicit public approval and never overwrites existing repositories.
- Lean README, updated installation and link-only instructions, publishing privacy checklist, external acceptance plan and source/skill checksum packaging.
- Retains no-scroll interactive SVG landmarks, mobile scenes, image-assisted artwork, art-direction guidance, résumé evidence and UI quality tests.
- Publishing metadata, input validation and no-auto-publish regression tests; no LinkedIn API integration or automatic posting.

## v0.1.4 — Quality testing candidate

- Improved art direction, optional image-assisted backgrounds, separate mobile compositions, SVG art kit and screenshot QA.
- Fixed duplicated SVG `class` attributes on animated landmarks and validation of sparse interactive shapes.
- CI hotfix: validator counts actual SVG landmark classes instead of exact HTML string matching.

## v0.1.3 — Landmark-first exploration

- Named and clickable SVG landmark objects replaced overlay pins.
- Link-only retrieval guidance, social metadata options and mobile accessibility checks.

## v0.1.2 — Full-screen world navigation

- No-page-scroll, mobile layout and accessible location list.
- Rich résumé highlights, metrics, attributed quotes and review safeguards.

## v0.1.1 — Earlier prototype baseline

- Initial open-ended résumé-to-world generator and examples.
