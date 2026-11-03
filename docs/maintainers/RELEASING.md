# Release SimpliCITY Builder v0.2.0

This is the **target stable minor release**, upgrading the released v0.1.5 baseline. **Do not tag `v0.2.0` until external chat and visual acceptance is complete.** An implementation ZIP for review is not an official GitHub Release.

## Pre-tag gates

1. Review the full diff against the latest published `v0.1.5` commit. The source ZIP here was based on the last available v0.1.5 archive because the live repository could not be fetched in the development environment; resolve any live-branch differences before merging.
2. Run `python3 -m unittest discover -s tests -v` and confirm all CI jobs pass, including optional browser automation and the self-contained package smoke test.
3. Confirm new photo, document, link, prompt and résumé chat workflows in at least one real supported agent; verify facts and private-data handling.
4. Inspect custom superhero-team, arbitrary-theme, and source-neutral scenes on phone and desktop. Fix poor contrast, overlap and generic presentation before calling the art quality approved.
5. Check the Pages gallery at `https://dishitkalsaria.github.io/SimpliCITY-Builder/`, or enable **Settings → Pages → Deploy from branch → `main` → `/docs`**. Verify actual HTTP links for all worlds.
6. Verify [RELEASE_ACCEPTANCE.md](RELEASE_ACCEPTANCE.md), [COMPATIBILITY.md](../../COMPATIBILITY.md), [SECURITY.md](../../SECURITY.md), license and no private data in the commit.

## Build and verify the installable ZIP

From the **clean commit to be tagged**:

```bash
python3 scripts/package_skill.py --tag v0.2.0 --output simplicity-builder.zip
python3 -m zipfile -t simplicity-builder.zip
python3 scripts/package_release.py --label v0.2.0
```

The GitHub release workflow builds the same skill-folder-root ZIP, verifies the tag matches `SKILL.md`, runs tests, extracts it into an empty directory, builds and validates a résumé, fictional prompt, document, synthetic photo, and synthetic link experience (no external source retrieval), and creates/uploads the release asset (`simplicity-builder.zip` plus SHA256SUMS). Do not attach an asset built from a different commit.

## Publish after passing acceptance

```bash
git status --short
git add -A
git diff --cached --check
git commit -m "Release SimpliCITY Builder v0.2.0"
git push origin main
# Check latest Actions run before tagging.
git tag -a v0.2.0 -m "SimpliCITY Builder v0.2.0"
git push origin v0.2.0
```

**Do not move a published tag.** `release.yml` runs on `v*` tag pushes and publishes the GitHub Release automatically after verifying tests and ZIP portability. Inspect release notes, assets and checksums and perform a fresh external install. If an existing release already exists, the workflow uploads/replaces matching named assets; retain immutable tags and ensure this is intentional.

If defects remain, keep working on an untagged branch. Optional `npx` skill installation is not documented as verified; do not claim it works without testing the actual repository in a supported environment.
