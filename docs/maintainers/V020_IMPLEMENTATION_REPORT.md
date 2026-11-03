# SimpliCITY Builder v0.2.0 — implementation review

## Basis and release status

Implemented from the local `SimpliCITY-Builder-Complete-Source-v0.1.5-rc.1.zip` snapshot. Its baseline was **52/52 Python tests passing**. The live GitHub `main`, published `v0.1.5` tag, release assets and GitHub Pages availability **could not be independently retrieved** from this environment. Review the changes against your live checkout before merging. **This is an implementation candidate, not a published stable v0.2.0 release.**

## Changes mapped to the agreed scope

| Requirement | Implementation |
|---|---|
| 1. Version consistency | v0.2.0 metadata, H1, latest changelog and active docs; automated agreement test. Historical changelog entries retained. |
| 2. Portable skill | Browser checker moved inside skill; fixture bundled; no repository-root script dependency; path-isolation tests. |
| 3. Release ZIP | Deterministic `scripts/package_skill.py`, tag-checked `.github/workflows/release.yml`, clean-install build/validate in CI. |
| 4. Demo gallery | Gallery has a new fictional guardian example, actual screenshot and revised multi-input copy; local pages rebuilt. Live Pages setup is user-controlled and unverified. |
| 5. Chat fast path | Direct host attachment reading, reviewed JSON, build, independent validate, optional quality pass. |
| 6. Bootstrap | Git clone and codeload curl/unzip commands in `AI_START_HERE.md`, with source review and capability caveats. |
| 7. Theme question | Single short question only when theme absent, explicitly any world allowed. Agent-specified behavior, not a Python interrogation loop. |
| 8. Chat delivery | Actual index.html, host-specific file output (including `/mnt/user-data/outputs` where available), approval before publishing. |
| 9. Requirement note | One-line chat capability requirement in README and INSTALL. |
| 10. Short prompts | Installed skill prompt and two-line repo bootstrap in README; long prompt in `docs/LINK_ONLY.md`. |
| 11. Installation | ZIP import and supported manual skill paths; unverified npx command deliberately omitted. |
| 12. Discoverability | Proposed GitHub topics are in `GITHUB_SETUP.md`; no settings modified. |
| Expanded source support | The unified `build.py` and `check.py` dispatch to backward-compatible modules, which accept host-reviewed photo/document/link/résumé descriptions and fictional prompt experiences. Existing legacy generator preserved. |
| Art direction | Theme-aware offline SVG art components plus host-guided bespoke SVG/image-assisted path, new superhero-themed demonstrator and screenshots. |
| Accessibility | Improved hint/footer legibility, reject unreadable custom accent colors, retained keyboard, list, dialog, reduced motion and offline HTML. |
| Optional tooling | `pyproject.toml`, `requirements-dev.txt`, CI Ruff/mypy/coverage steps without runtime pip requirements. |

## Local verification performed

- The inherited baseline passed 52 unit tests before modifications.
- **Current local verification:** 100 automated tests passed in three separately completed groups (32 + 44 + 24); 30 Chromium viewport checks passed across six demos. The initial implementation milestone of 69 passing tests is historical, not a current count. Re-run `python3 -m unittest discover -s tests -v` on your machine and confirm green GitHub Actions before release.
- A fictional guardian experience built and passed `check.py`; photo and link fixtures are synthetic and do not represent actual photo understanding or web retrieval.
- A single user-facing build/validate command pair now supports both schemas, while legacy CLI entrypoints remain for compatibility. Non-fiction experiences require item-level excerpts/observations; unsupported numeric claims fail, and a private `--source-text` input can confirm excerpt presence. This is conservative evidence coverage, not semantic fact verification.
- The tag-release workflow now tests résumé, document, fictional prompt, synthetic photo and synthetic link examples from a freshly extracted skill ZIP. Six maintainer-only Markdown files moved under `docs/maintainers/`, with links/tests updated; public skill metadata no longer names a commercial entertainment franchise.
- Actual Chromium tested the new guardian experience across desktop, mobile, compact, small-phone and landscape (5/5 viewport runs). Screenshots were manually inspected; the fallback art is an acceptable functional baseline but less sophisticated than AI-directed illustration.
- Clean ZIP archive checks and release artifact checks should be rerun after merging the final reviewed code.
- This correction was made to the local v0.2.0 candidate, not live GitHub; CI lint/type checks remain to be verified remotely.

## Not verified here

- Live repository `main` vs the available archive, existing GitHub `v0.1.5` tag, GitHub Pages HTTP status or the actual published skill asset.
- A real external AI chat reading a new résumé, photo, PDF or remote link and returning a generated file; supported host tools differ.
- Optional external image-generation integrations, real GitHub CLI publishing, LinkedIn card retrieval, `npx skills add`, or cross-version Python 3.9 runtime behavior.
- Execution of Ruff/mypy on a fully provisioned GitHub Actions runner; CI configuration is included but has not run on GitHub.
- Formal independent WCAG audit or proof of artistic quality for arbitrary unknown prompts.

The user-owned `v0.2.0` Git tag and GitHub Release should be created **only after** these external gates have passed. See [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md).

## Final pre-commit visual correction

- Corrected a double-initialization bug that stripped out the ambient SVG scenery. Environmental depth and moon/stars are preserved on desktop and mobile.
- Non-uniformly stretched terrain now keeps celestial circles round in screen space. The browser test checks this explicitly and includes negative regressions.
- Mobile photo framing shows more of the approved source image, with image-anchored rectangles remaining aligned. `Fit photo` and Previous/Next are still available; image semantics require human inspection.
- Corrected stale acceptance-demo count, changelog heading formatting, and the quickstart photo-build command explanation.
- These local improvements do not verify live GitHub CI, external host installation, or the deployed gallery.
