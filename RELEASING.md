> **v0.1.4 is a testing candidate. Do not create a `v0.1.4` tag or stable skill release until cross-agent acceptance tests pass.**

# Release checklist — SimpliCITY Builder v0.1.4

Creator and maintainer: Dishit Kalsaria. **v0.1.4 is a release candidate until the end-to-end host tests below are completed.** Do not label it stable based on local unit/browser tests alone.

1. Sync the source to GitHub, and confirm no private résumé files, review reports, secrets, `__pycache__`, or `.git` internals were added.
2. Run `python3 -m unittest discover -s tests -v` and verify green GitHub Actions.
3. Run the four example builds and Chromium browser tests, including 320x568 mobile, 390x844 phone, and 844x390 landscape. Inspect screenshots for overlap, contrast, clipped headings and thematic quality.
4. Run at least one **real consented résumé** in a skill-installed compatible AI host and one from the pinned GitHub link. Test the actual upload → factual extraction → world-building → file download flow. Document unsupported hosts honestly. Do not commit résumé evidence.
5. On GitHub, create annotated tag `v0.1.4` **only after** the above checks:

   ```bash
   git tag -a v0.1.4 -m "SimpliCITY Builder v0.1.4"
   git push origin v0.1.4
   ```

6. Attach `SimpliCITY-Builder-Skill-v0.1.4.zip` and `SHA256SUMS.txt` in **Releases → Draft a release → v0.1.4**. If you also publish the complete-source and update ZIPs, attach those too. Download the files listed in the checksum manifest into **one folder** and run `sha256sum -c SHA256SUMS.txt` (or `shasum -a 256` on macOS to compare individually). Do not claim checksum verification for a missing file. Verify the skill ZIP installs in the target host. GitHub's automatic source archives are different from the installable skill ZIP.
7. Visit GitHub Pages demo gallery and verify all four interactive demos and JSON links. Mark stable only if acceptance tests pass. Otherwise use GitHub's pre-release label and include known limitations.

This file is maintainer documentation and may remain public to make release criteria transparent.

For optional external spec validation, use the official `skills-ref validate simplicity-builder` separately if its maintained CLI is installed. Do not describe this as a CI gate unless a CI step runs it.
