# SimpliCITY Builder v0.1.5 — compatibility

| Environment | Supported route | Acceptance status |
|---|---|---|
| Claude custom Skills | Import skill ZIP with code execution | External host acceptance pending |
| Claude Code | Install skill folder and run Python | External host acceptance pending |
| OpenAI Codex | Install skill folder and run Python | External host acceptance pending |
| Other AI chats | Repository link + prompt where retrieval and execution exist | Capability-dependent, not guaranteed |
| Local Python | Generate, validate, package approved site | Automated tests cover this route |
| GitHub Pages | Hosts the approved static `index.html` | Optional deployment; live user-account flow not end-to-end tested here |
| LinkedIn | Link preview + user-written post | Does not run the interactive HTML inside a post |

The Builder is portable, not a universal chatbot installation. Do not mark a host *verified* without recording résumé type, theme, test date, result and manual intervention in [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md).
