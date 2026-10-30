# Changelog

## 0.2.0 — 2026-10-30 (testing candidate; not yet released)

- Align SVG documentation and sanitizer: transforms and line caps on shapes/groups; safe internal linear/radial gradients; explicit rejection of remote artwork resources.
- Add `check_artwork.py` preflight and regression tests for SVG features and malicious payloads.
- Add local TXT/DOCX and optional text-based PDF résumé extraction fallback, with evidence-review instructions; scanned PDFs still require OCR.
- Add Playwright/Chromium smoke-test script covering desktop/mobile layout, dialogs, search and JS exceptions, plus CI job.
- Document raw GitHub URL, `git clone` and ZIP fallback paths for supported AI hosts.
- Keep résumé fact mapping in the AI host and require human review before publication.

## 0.1.0 — 2026-10-30 (public beta candidate)

- Packaged the SimpliCITY Builder Agent Skill with a dependency-free HTML generator.
- Added link-first agent instructions for capable AI hosts.
- Allowed arbitrary world names and themes, with optional sanitized original SVG scenes.
- Added fictional fairytale, space, festival and clockwork museum sample inputs.
- Added unit/security tests, GitHub Actions, GitHub Pages demo and contributor documentation.
- Initial release requires real end-to-end résumé-upload testing before broad promotion.
