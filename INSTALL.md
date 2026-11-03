# Install SimpliCITY Builder v0.2.0

**Needs a chat or agent with code execution and file output; a text-only chat cannot run the generator.**

## Best option: import the skill into a capable AI chat

After v0.2.0 is tagged and the release succeeds, download the GitHub Release asset **`simplicity-builder.zip`**, extract it if the host requires a folder, and import `simplicity-builder/`. The ZIP contains every required generator, validator, HTML template, reference and example. An AI host must also read attachments/links with its own tools; installation does not grant unsupported abilities.

For Claude custom Skills, use its supported skill upload feature with code execution enabled, where available. For Claude Code, copy the folder to `.claude/skills/simplicity-builder/`. For Codex, copy to `.agents/skills/simplicity-builder/`. Other hosts must support file reading, Python execution and downloadable outputs. We have not verified a universal `npx skills add` command for this repository; none is advertised.

**Chat message after installation:** `SimpliCITY Builder: make me a world of guardians. Résumé attached.` Or `SimpliCITY Builder: make this photo an interactive landscape.`

## Without installing: repo link + two-line prompt

```text
Fetch https://github.com/DishitKalsaria/SimpliCITY-Builder and follow AI_START_HERE.md (review the source before executing it).
Build and validate an interactive HTML experience from my attachment or link; give me the downloadable file. Do not publish.
```

Full GitHub clone and codeload sandbox commands: [AI_START_HERE.md](AI_START_HERE.md). A link alone does not install the skill.

## Quick offline verification

From the extracted **skill folder**, no repository root needed:

```bash
python3 scripts/build.py --input examples/fairytale-sample.json --output demo.html
python3 scripts/check.py examples/fairytale-sample.json demo.html
python3 scripts/build.py --input references/experience-sample.json --output experience.html
python3 scripts/check.py references/experience-sample.json experience.html
```

For a real photograph the host must inspect the image, add normalized source object boxes, and pass the original image with `--source-image`; otherwise the photo build deliberately fails. The bundled `examples/photo-sample.json` and `examples/synthetic-lakeside.png` demonstrate this with fictional test art.

Python 3.9+ stdlib is sufficient for the core. Optional `pypdf` reads text PDFs; scanned PDFs need an OCR-capable host. Optional Playwright + Chromium enables actual browser testing, social screenshots and visual QA. No image-generation model is bundled.

**Privacy:** Do not publish the source documents, private résumé extraction or evidence reports. Deliver the offline HTML first; public hosting requires separate owner approval. See [SECURITY.md](SECURITY.md) and [PUBLISHING.md](PUBLISHING.md).
