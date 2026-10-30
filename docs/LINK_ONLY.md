# Using a GitHub link in an AI chat

Link-only use requires repository retrieval, attached-résumé reading, Python execution and downloadable file output. A bare link will not activate the skill.

- **Preferred:** review and clone a pinned tag: `git clone --depth 1 --branch v0.1.5-rc.1 https://github.com/DishitKalsaria/SimpliCITY-Builder.git` (when that candidate tag exists).
- **Alternative:** download a matching source archive or release asset and verify its published checksum.
- **If no tag yet:** use an exact reviewed commit. For mutable `main`, obtain permission and inspect before executing code.
- **Last resort:** fetch raw files as reference text only; this doesn't provide runtime assets or execute scripts.

Tell the AI to read `AI_START_HERE.md` and `simplicity-builder/SKILL.md`. If execution/file retrieval is not possible, ask the user to install/upload the skill ZIP in a supported host.

To publish an approved world or make a LinkedIn draft, follow [PUBLISHING.md](../PUBLISHING.md). Sharing is optional; public deployment is never automatic.
