# Publish & share an approved SimpliCITY world

**Optional, never automatic.** The interactive site runs on GitHub Pages; LinkedIn shows a link preview that visitors click to open it. There is no LinkedIn login, posting API, or required SimpliCITY Studio account.

## Prepare your site locally

First, verify the generated `index.html` in desktop and mobile browser views, review all public résumé facts and links, and remove anything private. **Do not put your source résumé, extracted text, evidence report, or private `portfolio.json` in a public repository.**

From a cloned SimpliCITY Builder repository:

```bash
python3 simplicity-builder/scripts/publish_portfolio.py prepare \
  --html /path/to/index.html \
  --account YOUR_GITHUB_USERNAME \
  --repo my-career-world \
  --out private/publish-ready
```

- Creates `private/publish-ready/site/index.html` and `.nojekyll`.
- Generates a **1200 × 627** image of the actual world for LinkedIn/Open Graph, when Playwright and Chromium are installed. If they are unavailable, use `--preview /path/to/approved.jpg` (JPEG, PNG or WebP; a 1200 × 627 image is recommended).
- Sets `og:url`, `og:image`, canonical URL, and Twitter-card metadata to the expected GitHub Pages address.
- Creates `PUBLISH_CHECKLIST.md` and `LINKEDIN_POST.txt` **outside** the public site directory.
- Makes **no network requests** unless you separately run the explicitly approved deployment command.

Install the optional preview tool if needed:

```bash
python3 -m pip install playwright
python3 -m playwright install chromium
```

Inspect the result before proceeding. The expected address is `https://YOUR_GITHUB_USERNAME.github.io/my-career-world/` for a project repository. Use a repository name and username you control.

## Publish: manual path (no GitHub CLI)

1. Create a **public** GitHub repository called `my-career-world` in your GitHub account.
2. Upload **only the contents of `private/publish-ready/site/`** to that repository's root (`index.html`, `social-preview.jpg` or equivalent, `.nojekyll`).
3. Go to repository **Settings → Pages → Deploy from a branch → main → /(root) → Save**.
4. Open the public URL and test it on a phone. Confirm the share image loads at `.../social-preview.jpg`.

GitHub Pages publishes static HTML from a branch; public Pages sites may be indexed by search engines. Check your repository and the published page carefully.

## Publish: optional GitHub CLI path

If your AI host or computer has the authenticated [`gh` CLI](https://cli.github.com/) and git, you can create and publish a **new** repository after reviewing the checklist:

```bash
python3 simplicity-builder/scripts/publish_portfolio.py deploy \
  --bundle private/publish-ready \
  --account YOUR_GITHUB_USERNAME \
  --repo my-career-world \
  --approve-public
```

This **creates a public repository and pushes the approved site files**. It refuses to overwrite an existing repo and checks the authenticated GitHub account. The GitHub Pages API may need additional permissions; if activation fails, visit **Settings → Pages** and enable it manually. The tool does not guarantee deployment is complete until you confirm the public URL.

Do not run the deploy command unless the portfolio owner has explicitly authorized publication and has checked the site. If a host cannot run git/gh, use the manual path instead.

## Share on LinkedIn

1. **Confirm** the Pages URL and preview-image URL work publicly.
2. Open LinkedIn → **Start a post**. Paste the URL to load a link preview.
3. Edit the text in `LINKEDIN_POST.txt`, remove anything you don't want to claim and choose your audience.
4. Post manually. Crediting **SimpliCITY Builder** is encouraged, not mandatory.

LinkedIn displays the image/title/description; people must click through to the website to interact. Preview images sometimes take time to refresh after website edits.

**No résumé or project code is posted directly to LinkedIn.** Sharing is an owner-controlled action.
