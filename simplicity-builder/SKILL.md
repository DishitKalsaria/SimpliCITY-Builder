---
name: simplicity-builder
description: Transform a user's uploaded résumé or CV and any imaginative prompt into a truthful, interactive, downloadable portfolio world. Trigger for "SimpliCITY Builder", resume-to-world requests, portfolio worlds, and custom themes (space, fairytale, museum, or anything invented). Build the HTML website, not only a design plan.
license: MIT
compatibility: Requires Python 3.9+, local filesystem and code execution to build files. The AI host must read the attached PDF, DOCX, or text résumé.
metadata:
  author: Dishit Kalsaria
  version: "0.2.0"
---

# SimpliCITY Builder

**Promise:** The résumé tells the story; the user's imagination chooses the world.

Build an actual offline, interactive `index.html` from the uploaded résumé and creative prompt. Examples of *possible* worlds are fairytales, space, museums and graffiti; **never restrict the setting to these examples**.

## Workflow (execute, don't just describe)

1. Read the user's résumé using the AI host's native PDF/DOCX/text capabilities. The generator accepts verified JSON. The bundled `scripts/extract_resume.py` can extract local TXT/DOCX and (with optional `pypdf`) text-based PDF files when native host extraction fails; it does **not** infer career facts. Read `references/resume-review.md`. If no résumé is available, request one or accept pasted career details. Never invent roles, project results, qualifications, dates, or links. The world metaphor may be fictional; the career facts may not.
2. Interpret the **exact creative prompt**. Invent world geography, atmospheric colors, title, navigation labels, section metaphors and coherent visual details. Use any lowercase-hyphenated `world.theme` name; no preset list constrains it.
3. Map grounded résumé facts into `portfolio.json` using `references/portfolio-schema.md`. Career information is real and legible inside every region. Use 1–8 meaningful sections with entries only where supported. Preserve important role and project facts; consolidate sections and split entries if necessary rather than silently dropping content. Do not copy names or accomplishments from example data.
4. For a world outside the starter scenes, create a distinctive `world.scene_svg` vector illustration of the requested environment following `references/illustration-rules.md`. Safe internal SVG gradients, shapes with transforms and stroke caps are supported. Validate a raw SVG first via `scripts/check_artwork.py` to avoid failed full builds. This is the principal way to make user-created themes visually distinct. If the scene cannot be validated, use the built-in fallback as a last resort and clearly disclose that the requested world art was simplified. For recognized starter worlds, bundled fallback scenes remain available. Supply dark palette colors for readability. Never fetch unlicensed external imagery.
5. Keep contact details, private links, home address, and phone number out of the output by default. Only include user-approved public links. Generate a **local file**; do not upload the résumé or publish the resulting site automatically. Do not echo résumé contents in public logs.
6. Save the structured model and execute:

   ```bash
   python3 scripts/build_portfolio.py --input /absolute/path/portfolio.json --output /absolute/path/index.html
   python3 scripts/validate.py /absolute/path/portfolio.json /absolute/path/index.html
   ```

   Paths are relative to this skill's `scripts/` folder if running from inside the skill directory. Locate these files from the skill's actual installation location. Never assume the user has cloned the repository.
7. Open and test the site in a browser at desktop and mobile widths. If Playwright/Chromium are available, run the bundled browser smoke test from the repo root: `python3 scripts/browser_smoke.py /absolute/path/index.html --screenshots /absolute/path/private/screenshots`. Inspect screenshots for contrast, layout, and theme fit (the smoke test cannot judge design quality). If a browser is unavailable, report that explicitly. Give the user the generated `index.html` as a downloadable file, plus optional `portfolio.json`. Remind them to review facts and personal information before publishing.

## Quality contract

- The result is **functional interactive HTML**, not an AI image, screenshot, vague plan, or untested code snippet.
- Content must be grounded in user-supplied career evidence; no synthetic accomplishments.
- Arbitrary themes are allowed. Use actual thematic illustration, not the same generic graphic with a renamed heading where possible.
- Navigation remains discoverable and keyboard accessible; all important details are selectable text.
- The generated site works offline as one HTML file with no JavaScript framework, external tracking or fonts.
- Avoid extra clarification when the résumé and imaginative prompt are sufficient; choose safe defaults.
- If the AI environment has no file or code execution capability, **say so**. Offer to generate files in a capable environment; do not pretend the link alone installs the skill.
- Cite *provided* résumé information in a private review note when supported, but do not add sensitive source content to the public site.

Read `references/world-rules.md`, `references/portfolio-schema.md`, `references/illustration-rules.md`, and `references/resume-review.md` for constraints. Sample JSON is fictional test material only.

## Invocation examples

- "SimpliCITY Builder, turn my attached résumé into an underwater city."
- "SimpliCITY, make me a fairytale land."
- "Use SimpliCITY Builder to create a floating garden of islands around my career."
