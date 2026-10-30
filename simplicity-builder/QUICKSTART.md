# Quickstart for an AI assistant

If this skill is installed, read `SKILL.md`, read the attached résumé with your available document tools, create `portfolio.json` from grounded facts and the user's arbitrary theme prompt, then preflight SVG, run `scripts/verify_facts.py` against privately extracted résumé text, followed by `scripts/build_portfolio.py` and `scripts/validate.py`. Keep a no-page-scroll world with named SVG landmark objects (not overlay pins) and mobile accessible navigation. Return `index.html` as a downloadable artifact. No extra software is required for viewing output. For text extraction, use the bundled `scripts/extract_resume.py` when host reading is unavailable; see `references/resume-review.md`. Preflight custom SVGs using `scripts/check_artwork.py` and test HTML in a browser when possible. Do not claim to have built files unless you executed the generator.

For a link-only invocation, first retrieve the repository's `AI_START_HERE.md` and `simplicity-builder/SKILL.md`, then obtain the generator, HTML template and schema as files before attempting execution. A URL is not a runnable installation. If code execution or site retrieval is not available, explain the limitation and propose a capable host.

## Optional original raster background (v0.1.4 testing)

Set `world.artwork_mode` to `image-assisted` only if you have a local, original PNG/JPEG/WebP you are permitted to publish. Run:

```bash
python3 scripts/build_portfolio.py --input /path/to/portfolio.json --background-image /path/to/original.png --output /path/to/index.html
```

The image is embedded; SVG landmarks remain clickable. With no image available, use the default `svg` mode. The host may choose an independent `world.scene_svg_mobile` to compose phone landmarks without shrinking the desktop layout.
