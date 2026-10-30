# Acceptance tests — SimpliCITY Builder v0.1.2

Use fictional résumés for public screenshots. For full acceptance use a résumé you have permission to process, then **do not publish its raw content**. Never post sensitive files in GitHub Issues.

## Automated checks (local)

```bash
python3 -m unittest discover -s tests -v
python3 simplicity-builder/scripts/build_portfolio.py --input examples/clockwork-sample.json --output /tmp/clockwork.html
python3 simplicity-builder/scripts/validate.py examples/clockwork-sample.json /tmp/clockwork.html
```

## Human acceptance: installed skill

1. Install the packaged ZIP in Claude (with code execution) or copy `simplicity-builder/` into a Codex skills folder.
2. Upload a résumé. Ask: `SimpliCITY Builder, make me a floating library in the clouds.`
3. Verify `index.html` is actually downloadable and opens in a browser. The AI should not demand manual JSON entry.
4. Open two locations, verify names, organizations, dates and accomplishments against the résumé. Check mobile and keyboard navigation, search and absence of broken links.
5. Repeat with a materially different prompt (e.g., `a surreal street-food night market`) and check that the setting and *scene* differ, not merely titles/colors.

## Human acceptance: paste repository URL

Start a **new chat** in an AI app that can read GitHub, the résumé and run scripts. Upload the résumé and use the copy-paste prompt from README. Confirm the agent retrieves `AI_START_HERE.md`, the skill and the Python generator before building; it should not claim the link installed the skill. Verify the same deliverables and facts as above. A chat without retrieval/execution is an **unsupported host**, not a successful run.

## Quality gate

- [ ] Install/run tested in Claude and at least one coding agent.
- [ ] Link + prompt tested successfully in at least one capable app.
- [ ] Original off-preset themes produce visually distinct artwork and labels.
- [ ] No fabricated résumé facts, no private home address or contact information.
- [ ] Offline HTML, browser navigation and smartphone layout work.
- [ ] GitHub Actions and Agent Skills reference validator pass.
- [ ] Public README demo is real, downloadable and works.
- [ ] Another person follows the installation instructions without extra guidance.

A passing unit suite does not establish cross-app reliability. Record tested host versions, prompt, error and remediation in release notes.

## SVG and résumé regression tests (v0.1.2)

Run the unit suite and preflight custom artwork before building:

```bash
python3 -m unittest discover -s tests -v
python3 simplicity-builder/scripts/check_artwork.py examples/gradient-scene.svg
python3 simplicity-builder/scripts/extract_resume.py your-resume.docx --output private/resume-extracted.txt
```

For PDF input, install optional `pypdf`; scanned files require OCR. After generation run real Chromium tests:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
python3 scripts/browser_smoke.py index.html --screenshots private/screenshots
```

Screenshot inspection is still a **human visual-review step**: smoke tests can catch layout overflow and broken interactions but cannot decide whether the fictional world is beautiful or sufficiently distinctive. Never publish unreviewed résumé details.


## Required v0.1.2 checks

- Run `python3 -m unittest discover -s tests -v`.
- Generate all four demo HTML files and validate with `simplicity-builder/scripts/validate.py`.
- Run `python3 scripts/browser_smoke.py docs/fairytale.html docs/space.html docs/festival.html docs/clockwork.html --screenshots private/screenshots`.
- Confirm zero **document** scrolling at 1440×900, 390×844 and 360×640; internal modal scrolling is deliberate.
- Inspect screenshots for landmark label collisions, contrast, clipped text, thematic quality, and mobile finger target size. Automated checks do not grade artistry.
- With a **private, user-approved résumé**, run `verify_facts.py --strict`; manually resolve any unmatched claims. Do not commit the résumé or report.
- Before marking the release stable, test installed skill and pinned repository-link workflows in a capable AI app using varied, consenting résumés.

### Optional screenshot regression aid

After generating Chromium screenshots, compare the latest `fairytale-desktop.png` to the baseline in `docs/assets`:

```bash
python3 -m pip install Pillow
python3 scripts/compare_screenshots.py docs/assets/fairytale-desktop.png private/screenshots/fairytale-desktop.png --max-changed 0.15
```

Screenshot diffs can be sensitive to OS/font/browser versions; they are a review trigger, not an automatic measure of good art. The release gate requires someone to look at desktop and mobile screenshots. Do not treat passing geometry or screenshot comparison as proof of aesthetics.
