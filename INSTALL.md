# Install or use SimpliCITY Builder

## Link + prompt (no skill installation)

Use an AI app that can fetch GitHub files, read your attached résumé, execute Python and return downloadable files. Paste the repository URL together with the example in the [README](README.md). The AI must follow [AI_START_HERE.md](AI_START_HERE.md). Pasting a bare link into an ordinary chatbot is **not** guaranteed to execute the skill.

## Claude custom skill

Upload the **skill ZIP** published as a GitHub Release asset using Customize → Skills → Create skill → Upload a skill, where supported. Turn on code execution. Attach a résumé and ask for a theme. Claude Code can instead use `.claude/skills/simplicity-builder/`.

## OpenAI Codex

Copy the `simplicity-builder` directory (including `SKILL.md`, scripts, assets and references) into `.agents/skills/simplicity-builder/` in your project, or `~/.agents/skills/simplicity-builder/` for personal use. Invoke with `$simplicity-builder` where supported, or ask for SimpliCITY Builder by name.

## Other compatible coding agents

Use the host's documented Agent Skills folder or import option. The host must be able to read PDF/DOCX and run local Python. For other apps, the link-based instructions may work if they support the same capabilities. No universal auto-install is implied.

## Manual generator only

From the repository root run:

```bash
python3 simplicity-builder/scripts/build_portfolio.py --input examples/fairytale-sample.json --output index.html
python3 simplicity-builder/scripts/validate.py examples/fairytale-sample.json index.html
```

Open `index.html` locally. You can publish this static file to any static hosting provider after reviewing the content.

## Safety

Never publish a résumé, its extracted JSON, or a generated site without the owner's review. By default, the skill excludes phone, email, and home address. Your AI host may process private résumé data under its own policy.

## Optional local tools (v0.1.3)

- To extract TXT/DOCX résumé text: `python3 simplicity-builder/scripts/extract_resume.py resume.docx --output private/resume-extracted.txt`. For text-based PDF files, install `pypdf` first. This is extraction only; the AI must still interpret and verify facts.
- To check original SVG artwork **before** generating a website: `python3 simplicity-builder/scripts/check_artwork.py scene.svg`. Internal SVG gradients, shape transforms and line caps are supported; external URLs are blocked.
- To check HTML in Chromium: install `playwright` and its Chromium browser, then run `python3 scripts/browser_smoke.py index.html --screenshots private/screenshots`.
- If GitHub browsing is blocked, prefer a reviewed tagged `git clone` or verified release ZIP; raw-file reading is a last-resort text fallback, not an installation. See `docs/LINK_ONLY.md`.


## v0.1.3 no-scroll world contract

Once generated, a world opens full screen with **named, clickable SVG landmarks**, not overlaid pins or coordinate buttons. On mobile, long résumé content stays in internal detail/list/recruiter panels (not document scrolling). Run the browser suite at **five viewport sizes** (desktop, mobile, compact, small phone, landscape) before distributing. See [TESTING.md](TESTING.md).
