# SimpliCITY Builder v0.2.0 — stable-release acceptance

**This checklist is a gate; blank items are not passing results.**

- [ ] All v0.1.5 regression tests and added v0.2.0 tests pass.
- [ ] Skill ZIP extracts and runs both legacy résumé and new experience examples without accessing the repository root.
- [ ] Versions match in SKILL metadata, H1, README, latest CHANGELOG entry and tag; no escaping skill paths.
- [ ] Installed-skill chat successfully builds from an owner-consented real résumé with no invented career claims.
- [ ] Image-capable chat accurately describes a user-approved photo and generates a working interactive scene without invented people identities.
- [ ] Document-reading chat turns a real authorized PDF/document into source-grounded chapters and an interactive exhibition.
- [ ] Retrieval-capable chat transforms an authorized link, preserving source attribution and without copying entire copyrighted content.
- [ ] Prompt-only chat makes a fictional world with imaginative art; no fiction is represented as verified information.
- [ ] New arbitrary superhero-team prompt yields recognizable, original, unbranded art and clickable named SVG objects.
- [ ] Host without image tools still produces coherent procedural SVG; limitations clearly disclosed.
- [ ] Desktop, narrow phone, landscape mobile, keyboard, search, overview, reduced-motion, and print verified; no unintended document scroll.
- [ ] Contrast and visual coherence reviewed using screenshots (no unsupported WCAG certification claim).
- [ ] GitHub Pages live gallery and all six demos checked; 404 resolved or clearly disclosed.
- [ ] Test opt-in publish preparation and ensure no remote deployment without explicit permission.
- [ ] Run or explicitly skip optional Chromium/Playwright QA and state which.
- [ ] No actual résumés/photos, secrets, private evidence or raw extracted text in repository or release assets.
- [ ] Download official release ZIP, validate checksums and perform a clean installation in the target AI host.

Record **host/version, input kind, requested world, visual review, tests actually run, result and issues** with no personal source data. Do not mark AI platforms verified simply because the local Python tests pass.

## Additional stable-release acceptance gates

- [ ] All current tests pass, including malformed-metadata and negative-browser regression cases.
- [ ] Inspect mobile/desktop image previews, with plaque placement, no visual cutoff, meaningful source anchors, guided tour, and accessible object navigation.
- [ ] Golden comparisons pass at the configured CI tolerance; approve baseline changes explicitly.
- [ ] Test private review-sheet generation, photo metadata removal and output-size limits.
- [ ] Verify real hosted docs/ gallery, external chat file delivery and optional axe-core separately. Never mark skipped checks as passed.
