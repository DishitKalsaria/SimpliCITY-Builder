# Upgrade an existing SimpliCITY Builder v0.1.5 checkout

**Do not overwrite your `.git/` folder.** This is an untagged v0.2.0 implementation for review, based on the available v0.1.5 source archive. Resolve any conflicts with your live GitHub `main` before committing; the remote state could not be verified in this environment.

1. Open your existing Git checkout in VS Code, run `git status` and commit/stash your own uncommitted work first.
2. Make a branch: `git switch -c feature/chat-first-v020`.
3. Extract the **v0.2.0 Update ZIP** over your repository root (includes hidden `.github/` and new `simplicity-builder/` files), or use the complete source ZIP and copy its content into the checkout. Do not copy its parent enclosing folder or delete `.git/`.
4. Move to the new installed-skill browser checker path and remove the obsolete root script (if tracked):

   ```bash
   git rm --ignore-unmatch scripts/browser_smoke.py
   ```

5. Run tests and inspect the diff:

   ```bash
   python3 -m unittest discover -s tests -v
   python3 scripts/package_skill.py --tag v0.2.0 --output simplicity-builder.zip
   git status --short
   git diff --check
   ```

6. Test the generated `simplicity-builder.zip` with the standalone extraction steps in [TESTING.md](TESTING.md). Do not commit generated ZIPs, real inputs or screenshots of private people.
7. Commit on the feature branch and push a **PR** for review. Do **not** tag `v0.2.0` until the external chat, artwork, privacy, Pages and release acceptance checklist is complete. Tagging triggers the automatic GitHub Release workflow.

The legacy `build_portfolio.py` and `profile/world/sections` format remain supported. Use `build.py` and `check.py` for both legacy résumés and new host-reviewed photo/document/link descriptions or fictional experiences. Existing script names remain available for integrations. AI-host source reading and external art creation remain agent capabilities, not magically added to the stdlib-only Python engine.
