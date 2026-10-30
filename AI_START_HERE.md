# SimpliCITY Builder — instructions for AI assistants opening this repository link

**User intent:** They have attached a résumé and asked "SimpliCITY, make me [their imaginative world]." Your job is to create an actual downloadable interactive portfolio website, with arbitrary world aesthetics and verified career facts.

1. Read [`simplicity-builder/SKILL.md`](simplicity-builder/SKILL.md) completely, then its [schema](simplicity-builder/references/portfolio-schema.md), [visual rules](simplicity-builder/references/illustration-rules.md) and [world mapping](simplicity-builder/references/world-rules.md).
2. Obtain the repo's *source files*, particularly `simplicity-builder/scripts/build_portfolio.py` and `simplicity-builder/assets/template.html` (clone/download to a filesystem you can execute). Reading a README alone is not enough to construct the site.
3. Read the attached résumé with your native tools; create truthful `portfolio.json` describing the user's **chosen world**. Do not use example résumé contents. Provide original `world.scene_svg` artwork when the theme isn't a starter scene.
4. Run `python3 simplicity-builder/scripts/build_portfolio.py --input portfolio.json --output index.html`, then `python3 simplicity-builder/scripts/validate.py portfolio.json index.html`.
5. Deliver `index.html` and optionally `portfolio.json`; state whether a browser test was performed. Do not publish the résumé or site without explicit approval.

This link-only route works only if your environment can actually retrieve the repository, read the uploaded résumé, execute Python and return files. **Never claim that pasting a link installs a skill or makes code execution possible.** If those capabilities aren't available, say what is missing.

**Publisher:** [Dishit Kalsaria](https://github.com/dishitkalsaria). Original flagship portfolio: [Simpli-City](https://dishitkalsaria.github.io/Simpli-City/).
