# SimpliCITY Builder v0.2.0 — capabilities and support

| Environment | Route | Verified status |
|---|---|---|
| Local Python 3.9+ | Standalone ZIP + two validators | Local automated test coverage; cross-version Python verification remains to run |
| Claude custom Skills | Import skill ZIP with code execution | External v0.2.0 acceptance pending |
| Claude Code | Install `simplicity-builder/` and run Python | External v0.2.0 acceptance pending |
| OpenAI Codex | Install skill in supported skills directory | External v0.2.0 acceptance pending |
| Other coding-enabled chats | Reviewed repository fetch + Python + file output | Host-dependent; cannot guarantee capabilities |
| Text-only chatbot | No code execution or downloadable files | Cannot run generator |
| Photo input | Host image understanding + observed normalized object boxes + approved local image | Python generator refuses a photo scene without `--source-image`; the host, not the engine, identifies objects |
| PDF/doc input | Host reader preferred; TXT/DOCX extractor bundled; text PDF optional `pypdf` | Scanned PDF requires OCR-capable host |
| Website link | Requires authorized host retrieval | Generator makes no network requests |
| Image generation | Optional host image tool, or offline procedural SVG fallback | Not built into Python runtime |
| GitHub Pages | Hosts approved static HTML | Live demo HTTP checks not verified here |
| LinkedIn | Social preview + manually authored post | Interactive site runs outside LinkedIn |

See [RELEASE_ACCEPTANCE.md](docs/maintainers/RELEASE_ACCEPTANCE.md) before marking external workflows verified. No universal automated publishing or third-party image API is implied.
