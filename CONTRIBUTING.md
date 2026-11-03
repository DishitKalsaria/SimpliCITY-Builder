# Contributing to SimpliCITY Builder

Thanks for considering a contribution. Please open an issue for larger features and include the intended user workflow before starting. Small bug fixes can go directly to a pull request.

1. Work on a branch and keep changes focused.
2. Before pushing, install `requirements-dev.txt` and run `python3 scripts/ci_preflight.py all` (Ruff, mypy and unit tests; must not skip missing tools).
3. Generate at least one legacy résumé demo and one new arbitrary-source experience, then check links, search and dialogs on mobile and desktop.
4. Use fictional data (no private photos, documents or résumés) in tests and screenshots. Never commit real private CVs, API keys or personal contact information.
5. Explain what changed, how it was tested, and any relevant limitations in your pull request.

Important principles: any imaginative theme; source-grounded facts or clearly fictional narratives; offline-first generated HTML; accessibility; zero forced user setup to *view* results; no surprise publishing or tracking. External images require licensing review; avoid dependencies unless they materially improve outcomes.

By contributing, you agree your contribution is provided under the repository's MIT License.

For v0.2.0, include tests for new source-neutral inputs, preserve standalone installation, and run `scripts/package_skill.py` from a clean checkout. Optional developer dependencies are in `requirements-dev.txt`; Python generator runtime remains stdlib-only.
