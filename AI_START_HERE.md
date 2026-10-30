# SimpliCITY Builder v0.1.5 — AI agent entry point

**Goal:** From the user's attached résumé and original theme prompt, produce an actual downloadable, responsive, fully interactive portfolio. Never return just a picture or design plan.

**Source trust:** Prefer a reviewed, tagged release (`v0.1.5-rc.1` for external testing; `v0.1.5` once approved). Before the tag exists, use an exact reviewed commit or obtain permission to inspect and run mutable `main`. Git clone is preferred. A GitHub URL alone does not install the skill or grant execution rights.

Read `simplicity-builder/SKILL.md`, schema, art-direction, illustration and résumé-review references. Follow the skill's full build, facts, browser and quality checks. The illustrated SVG landmarks themselves are clickable; there are no overlay pins, and the document must not scroll (long panels may).

Build and deliver the private site first. Never assume publishing is requested.

If the user **explicitly requests public hosting**, review the facts and content with them and consult [PUBLISHING.md](PUBLISHING.md). Use `simplicity-builder/scripts/publish_portfolio.py prepare` to make a GitHub Pages-ready folder; this step does not upload. Deploy only after the owner approves and has authorized GitHub write access. Do not publish or post to LinkedIn on the owner's behalf without a separate explicit authorization.

For a LinkedIn share, deliver a public-site link, accessible social image and editable `LINKEDIN_POST.txt`. The interactive world runs on the hosted website, not inside a LinkedIn post. Never claim a URL is live until it has been checked.

**Unsupported host:** If you cannot retrieve files, read the résumé, execute Python or produce downloadable files, explain the limitation; do not claim success.

Creator: [Dishit Kalsaria](https://github.com/DishitKalsaria).
