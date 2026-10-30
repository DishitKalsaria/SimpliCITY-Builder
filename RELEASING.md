# Release checklist — SimpliCITY Builder v0.1.2

Creator and maintainer: Dishit Kalsaria. This is a **candidate** for the user's planned v0.1.2 stable release. Do not label it verified stable until the checks below are complete.

1. Sync the source to GitHub, and confirm no private résumé files, review reports, secrets, `__pycache__`, or `.git` internals were added.
2. Run `python3 -m unittest discover -s tests -v` and verify green GitHub Actions.
3. Run the four example builds and Chromium browser tests, including 320x568 mobile, 390x844 phone, and 844x390 landscape. Inspect screenshots for overlap, contrast, clipped headings and thematic quality.
4. Run at least one **real consented résumé** in a skill-installed compatible AI host and one from the pinned GitHub link. Test the actual upload → factual extraction → world-building → file download flow. Document unsupported hosts honestly. Do not commit résumé evidence.
5. On GitHub, create annotated tag `v0.1.2` **only after** the above checks:

   ```bash
   git tag -a v0.1.2 -m "SimpliCITY Builder v0.1.2"
   git push origin v0.1.2
   ```

6. Attach the packaged skill ZIP and `SHA256SUMS.txt` in **Releases → Draft a release → v0.1.2**. Compare locally: `sha256sum -c SHA256SUMS.txt` (run in the downloaded-release-assets folder). Check that zipped skill is installable in the target host. GitHub's automatic source archives are different from the skill-only ZIP.
7. Visit GitHub Pages demo gallery and verify all four interactive demos and JSON links. Mark stable only if acceptance tests pass. Otherwise use GitHub's pre-release label and include known limitations.

This file is maintainer documentation and may be removed from a minimal public root if preferred.
