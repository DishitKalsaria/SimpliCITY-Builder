# Install SimpliCITY Builder

Choose one approach:

- **Link + prompt:** Paste the repository URL and prompt shown in [README.md](README.md) into an AI tool with GitHub retrieval, résumé reading, Python execution and file downloads. The link does not automatically install the skill. [Source trust guidance](docs/LINK_ONLY.md).
- **Claude custom Skills:** Where supported, upload the installable `SimpliCITY-Builder-Skill-v0.1.5.zip` and enable file/code execution. Claude Code can instead place `simplicity-builder/` in `.claude/skills/`.
- **OpenAI Codex:** Place `simplicity-builder/` under `.agents/skills/simplicity-builder/` or `~/.agents/skills/simplicity-builder/` where supported.
- **Other agents:** Follow the host's Agent Skills import instructions. A text-only chatbot without execution/file access cannot run the website generator.

## Manual quick test

```bash
python3 simplicity-builder/scripts/build_portfolio.py --input examples/space-sample.json --output space-demo.html
python3 simplicity-builder/scripts/validate.py examples/space-sample.json space-demo.html
```

Open `space-demo.html`. Python 3.9+ is sufficient for generation. Optional `pypdf` enables text-based PDF extraction; scanned PDFs require OCR or pasted text. Optional Playwright + Chromium enables browser tests and publishing preview screenshots.

## Publishing and privacy

The output is an offline, dependency-free interactive HTML file. **Nothing is published by default.** Optional GitHub Pages packaging and LinkedIn preview drafting are documented in [PUBLISHING.md](PUBLISHING.md). All public content requires owner review and approval. Do not commit real résumés, extracted text or private verification reports.
