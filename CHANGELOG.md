# Changelog

## v0.1.4 — Quality testing candidate (not tagged)

- Fixed duplicate SVG `class` attributes on animated landmarks; sparse constellations and hollow shapes now accept bounding-box interaction in supporting browsers, with the accessible list always available.
- Added optional independently composed `world.scene_svg_mobile` for portrait and small-phone readability, with exactly one active landmark scene at any time.
- Added `world.artwork_mode: image-assisted` and a local `--background-image` PNG/JPEG/WebP embedding option. Output stays offline and image creation is optional.
- Introduced an art-direction brief, visual QA rubric, reusable SVG artwork references and a richer hand-composed space example.
- Strengthened browser QA and regression coverage, and documented image privacy, optional visual generation, and traceable résumé review.
- This candidate must pass external agent résumé-to-world and visual evaluation before Git tagging and distributing a final ZIP.

## v0.1.3 — Landmark-first polish (release candidate)

- Real named SVG objects replace overlay pin icons; focus, click/tap, hover labels and keyboard action derive from each object's geometry.
- Original layered example artwork revised, with safer ambient motion and reduced-motion handling.
- New `world.landmarks` records; legacy v0.1.2 `world.hotspots` accepted but their coordinates are ignored.
- Optional complete Open Graph and Twitter-card metadata using a publicly hosted preview image.
- Expanded schema documentation with enforced field lengths and current examples.
- Unified link-based trust guidance around a pinned tag; clarified that external `skills-ref` is not a CI gate.
- README wording and release documentation updated, with mobile and desktop browser regression checks.

## v0.1.2 — Interactive-world release candidate (2026-10-30)

- Replace scrolling hero/card layout with a viewport-sized explorable world and one labelled, keyboard-accessible overlay hotspot per career section.
- Enforce no document scrolling on desktop and mobile; allow accessible internal scroll in details, location list and recruiter view.
- Add data-driven interface copy, exact coordinate-based hotspots and consistent built-in SVG icons; preserve arbitrary imaginative themes.
- Add résumé entry highlights, numerical metrics and authenticated attributed quote entries.
- Add safe predefined CSS motion with reduced-motion support, reusable SVG composition examples, print/recruiter view, and Open Graph metadata.
- Add conservative local `verify_facts.py` evidence report and strict mode (not semantic truth guarantee).
- Expand browser checks for hotspot navigation, search, recruiter view, viewport overflow and screen-reader labels.
- Add brand/IP originality guidance, pinned-tag instructions and release checksums. Maintain zero runtime network dependencies.
- **Not yet claimed:** real-world cross-host résumé-upload acceptance, universal AI app compatibility, or automated subjective art review.

## v0.1.1 — Prior published baseline

Previous version as tagged by project maintainer. Archived historical release information remains in Git history.
