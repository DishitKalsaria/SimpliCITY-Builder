# Chat-first quickstart — SimpliCITY Builder v0.2.0

Needs a chat/agent with code execution and file output; a text-only chat cannot run the generator.

1. Read the attachment or accessible link with the tools the host already provides. Use `scripts/extract_resume.py` only if needed; it does not interpret photos or OCR scanned documents.
2. Use `references/experience-schema.md` to create `experience.json` from verified non-résumé content, or `references/portfolio-schema.md` for résumé JSON. If no theme is requested, ask one brief creative-world question, then proceed.
3. Build: `python3 scripts/build.py --input /path/to/content.json --output /path/to/index.html` (detects both schemas).
4. Independently validate: `python3 scripts/check.py /path/to/content.json /path/to/index.html` (optionally `--source-text /private/extracted.txt`).
5. Return the downloadable HTML file. Use `/mnt/user-data/outputs/index.html` on hosts that expose that path; otherwise use their supported file-output location. Do not claim a real browser check unless it ran.

For an approved photo, build with `python3 scripts/build.py --input /path/to/photo-experience.json --source-image /local/photo.png --output /path/to/index.html` (the photo flag belongs to **build.py**, not the browser checker).

Optional visual QA: `python3 scripts/browser_smoke.py /path/to/index.html`. If Playwright/Chromium is unavailable, report that it was skipped.

No automatic publishing. Review factual claims, real people in photos, private details and sharing permissions before any public deployment. Read `SKILL.md` for full safeguards, art direction and publishing options. The skill works independently of repository-root files.
