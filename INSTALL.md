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
