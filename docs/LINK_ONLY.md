# What does “paste the link and prompt” mean?

SimpliCITY Builder aims to support a one-instruction experience. Installation is the most reliable path, but a **link-first** interaction can work in an AI app that has all required capabilities.

The assistant must be able to (1) fetch the repository's actual files, (2) read the attached résumé, (3) create `portfolio.json`, (4) execute Python 3.9+, and (5) return an HTML file. It must follow `AI_START_HERE.md` and `simplicity-builder/SKILL.md`, not just browse the README.

A plain chat without file creation or tool execution may be able to explain how to use the repo but cannot automatically build the portfolio. Some apps may require a workspace, authorization, or a repo download. **Do not promise that a bare GitHub URL installs an Agent Skill.**

### Minimal prompt

```text
Read https://github.com/dishitkalsaria/SimpliCITY-Builder and follow AI_START_HERE.md. Attached is my resume. SimpliCITY Builder, create a floating archipelago as my interactive professional portfolio. Download the repository's script and template, generate grounded portfolio.json, run and validate the builder, and give me index.html. Include no private contact details.
```

Before publishing a generated site, review career facts, links, and privacy. Share any failed installation or generation scenarios as a GitHub Issue (without uploading private résumé data).
