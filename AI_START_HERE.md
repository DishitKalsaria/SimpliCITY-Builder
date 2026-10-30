# SimpliCITY Builder v0.1.2 — AI-agent entry point

**Intent:** The user attached a résumé and requested an imaginative, **full-screen no-scroll** portfolio world. Produce a real downloadable website, not an image or design plan.

1. **Get a trusted pinned copy of the source.** After the `v0.1.2` GitHub tag exists, run `git clone --depth 1 --branch v0.1.2 https://github.com/DishitKalsaria/SimpliCITY-Builder.git`. For pre-release development only, clone `main`. If a clone isn't possible, use the matching release ZIP. Raw GitHub web pages are a last-resort text fallback and are not a runtime substitute. Verify the release SHA256 checksum when using a downloaded ZIP. Don't run arbitrary code from a mutable, unreviewed branch without user approval.
2. Read `simplicity-builder/SKILL.md` and all referenced schema/artwork/resume/world rules. The scene must have *clickable labelled hotspots* for each section, with an accessible list fallback and recruiter view. **The body must not scroll** on mobile or desktop, while long panel content may scroll internally.
3. Read résumé with host tools or local helper `simplicity-builder/scripts/extract_resume.py`. Create a truthful structured `portfolio.json` from actual qualifications and any theme prompt. Keep private contact details out unless expressly approved. Don't copy example identities.
4. Generate original inert SVG for custom themes; allow supported gradients and transforms. Handle branded IP requests via original genre-level art, not trademarked characters or replicas.
5. Run local fact-evidence review, generator and validator:

   ```bash
   python3 simplicity-builder/scripts/verify_facts.py --input portfolio.json --resume-text private/resume.txt --strict --report private/review.json
   python3 simplicity-builder/scripts/build_portfolio.py --input portfolio.json --output index.html
   python3 simplicity-builder/scripts/validate.py portfolio.json index.html
   ```

   Strict token matches are conservative and can flag paraphrases; review rather than suppress them. They are not proof of truth.
6. Run `python3 scripts/browser_smoke.py index.html --screenshots private/screenshots` if Chromium/Playwright are available. Inspect desktop and mobile screenshots manually, verify no page scroll, accessible hotspots, and actual distinct world artwork. If tools are unavailable, report the limitation.
7. Provide `index.html` and optionally `portfolio.json`. Do not publish automatically, store or transmit the résumé, or claim successful tests that were not run.

**Important:** Pasting the link does not install a skill or grant an AI app file/code execution. The AI must be able to read attachments, retrieve code, run Python and return files.

Creator: [Dishit Kalsaria](https://github.com/DishitKalsaria). Original flagship portfolio: https://dishitkalsaria.github.io/Simpli-City/
