#!/usr/bin/env python3
"""Opt-in GitHub Pages publishing for an already reviewed SimpliCITY HTML portfolio.

Stdlib-only package preparation. Publishing uses an already-authenticated `gh` + git,
requires an explicit owner approval flag, and refuses existing repository names.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

USER_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?\Z")
REPO_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}\Z")
META_RE = re.compile(r"<meta\s+[^>]*>", flags=re.IGNORECASE)
CANONICAL_RE = re.compile(r'<link\s+[^>]*\brel=["\']canonical["\'][^>]*>', re.IGNORECASE)


def validate_names(account: str, repo: str) -> None:
    if not USER_RE.fullmatch(account) or not REPO_RE.fullmatch(repo) or repo in {'.', '..'}:
        raise ValueError('Invalid GitHub account or repository name')


def page_url(account: str, repo: str) -> str:
    validate_names(account, repo)
    if repo.casefold() == f'{account}.github.io'.casefold():
        return f'https://{account}.github.io/'
    return f'https://{account}.github.io/{quote(repo)}/'


def image_kind(raw: bytes) -> str:
    if raw.startswith(b'\xff\xd8\xff'):
        return 'jpg'
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if raw.startswith(b'RIFF') and raw[8:12] == b'WEBP':
        return 'webp'
    raise ValueError('Preview must be JPEG, PNG or WebP')


def rewrite_social(html_source: str, url: str, image_url: str, image_alt: str) -> str:
    if '<!doctype html>' not in html_source[:120].lower() or '</head>' not in html_source.lower():
        raise ValueError('Expected a complete generated HTML document')
    if 'scene-landmark' not in html_source or 'SimpliCITY Builder' not in html_source:
        raise ValueError('Source does not look like a SimpliCITY Builder interactive site')
    if '\x00' in html_source:
        raise ValueError('Invalid HTML source')
    first, sep, rest = re.split(r'(</head>)', html_source, maxsplit=1, flags=re.IGNORECASE)
    if not sep:
        raise ValueError('No HTML head')
    # Remove old/possibly stale share meta tags; retain the existing og:title and og:description.
    keys = {'og:url','og:image','og:image:alt','og:image:width','og:image:height',
            'twitter:card','twitter:image','twitter:title','twitter:description'}
    def remove_meta(match: re.Match[str]) -> str:
        source = match.group(0)
        attr = re.search(r'(?:name|property)\s*=\s*["\']([^"\']+)["\']', source, re.I)
        return '' if attr and attr.group(1).lower() in keys else source
    first = META_RE.sub(remove_meta, first)
    first = CANONICAL_RE.sub('', first)
    if 'property="og:title"' not in first or 'property="og:description"' not in first:
        raise ValueError('Required Open Graph title/description missing')
    def escape(value: str) -> str:
        return html.escape(value, quote=True)
    title_match = re.search(r'<title>(.*?)</title>', first, flags=re.I | re.S)
    title = html.unescape(title_match.group(1)) if title_match else 'My interactive world'
    desc_match = re.search(r'<meta property="og:description" content="([^"]*)"', first, flags=re.I)
    description = html.unescape(desc_match.group(1)) if desc_match else ''
    fresh = '\n'.join([
        f'<meta property="og:url" content="{escape(url)}">',
        f'<meta property="og:image" content="{escape(image_url)}">',
        f'<meta property="og:image:alt" content="{escape(image_alt)}">',
        f'<link rel="canonical" href="{escape(url)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{escape(title)}">',
        f'<meta name="twitter:description" content="{escape(description)}">',
        f'<meta name="twitter:image" content="{escape(image_url)}">',
    ])
    return first + '\n  ' + fresh + '\n' + sep + rest


def capture_preview(html_file: Path, output: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError('Preview screenshot requires optional Playwright: pip install playwright && python -m playwright install chromium; or supply --preview YOUR_IMAGE') from exc
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
        except Exception as first_error:
            system_browser = shutil.which('chromium') or shutil.which('google-chrome')
            if not system_browser:
                raise RuntimeError('Chromium is unavailable. Run python -m playwright install chromium, or use --preview /path/to/approved.jpg') from first_error
            browser = p.chromium.launch(headless=True, executable_path=system_browser, args=['--no-sandbox'])
        try:
            page = browser.new_page(viewport={'width': 1200, 'height': 627}, device_scale_factor=1)
            page.route('http://**/*', lambda route: route.abort())
            page.route('https://**/*', lambda route: route.abort())
            page.set_content(html_file.read_text(encoding='utf-8'), wait_until='load')
            page.screenshot(path=str(output), type='jpeg', quality=87, animations='disabled')
        finally:
            browser.close()


def prepare(html_file: Path, account: str, repo: str, bundle: Path, preview: Path | None = None) -> str:
    url = page_url(account, repo)
    if not html_file.is_file():
        raise ValueError(f'HTML file not found: {html_file}')
    if bundle.exists() and any(bundle.iterdir()):
        raise ValueError('Refusing to overwrite a nonempty bundle directory. Choose a new --out path.')
    site = bundle / 'site'
    site.mkdir(parents=True)
    try:
        return _prepare_into(html_file, url, bundle, preview)
    except Exception:
        # Do not leave a half-generated bundle that prevents a clean retry.
        shutil.rmtree(bundle)
        raise


def _prepare_into(html_file: Path, url: str, bundle: Path, preview: Path | None) -> str:
    site = bundle / 'site'
    image_file = site / 'social-preview.jpg'
    if preview:
        raw = preview.read_bytes()
        if len(raw) > 5_000_000:
            raise ValueError('Preview image exceeds 5 MB')
        kind = image_kind(raw)
        image_file = site / f'social-preview.{kind}'
        image_file.write_bytes(raw)
    else:
        capture_preview(html_file, image_file)
    # Verify generated preview as well as supplied image.
    kind = image_kind(image_file.read_bytes())
    if image_file.stat().st_size > 5_000_000:
        raise ValueError('Preview image exceeds 5 MB')
    if image_file.suffix != f'.{kind}':
        raise ValueError('Preview extension does not match its bytes')
    image_url = url + image_file.name
    source = html_file.read_text(encoding='utf-8')
    rewritten = rewrite_social(source, url, image_url, 'Illustration of the interactive portfolio world')
    (site / 'index.html').write_bytes(rewritten.encode('utf-8'))
    (site / '.nojekyll').touch()
    (bundle / 'LINKEDIN_POST.txt').write_text(
        'My professional journey now has a world of its own.\n\n'
        'I turned my résumé into an interactive world where every place tells a part of my story.\n\n'
        f'Explore it: {url}\n\n'
        'Created with SimpliCITY Builder (optional credit): '\
        'https://github.com/DishitKalsaria/SimpliCITY-Builder\n\n'
        '#SimpliCITYBuilder #InteractivePortfolio\n', encoding='utf-8')
    (bundle / 'PUBLISH_CHECKLIST.md').write_text(
        '# Review before publishing\n\n'
        '- [ ] I have opened `site/index.html` and reviewed every employer, date, metric, quote, link and private detail.\n'
        '- [ ] I authorize this site to be publicly accessible and potentially searchable.\n'
        '- [ ] The social preview does not disclose private information.\n'
        '- [ ] I have tested mobile and desktop navigation.\n'
        '- [ ] I understand that LinkedIn only shows a preview; visitors click through to explore.\n\n'
        f'Expected URL: {url}\n\n'
        'Manual publication: create a public GitHub repository named as requested; upload only the **contents of `site/`** to its root; then Settings > Pages > Deploy from branch > `main` > `/(root)`.\n'
        'Optional CLI deployment: `python simplicity-builder/scripts/publish_portfolio.py deploy --bundle PATH_TO_BUNDLE --account ACCOUNT --repo REPO --approve-public`.\n', encoding='utf-8')
    return url


def run_command(args: list[str], cwd: Path | None = None, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None,
                          stderr=subprocess.PIPE if capture else None)


def deploy(bundle: Path, account: str, repo: str, approve: bool) -> str:
    url = page_url(account, repo)
    if not approve:
        raise ValueError('No publication without --approve-public after reviewing the full site and checklist')
    site = bundle / 'site'
    if not (site / 'index.html').is_file() or not (bundle / 'PUBLISH_CHECKLIST.md').is_file():
        raise ValueError('Missing prepared bundle and owner-review checklist')
    if not re.search(r'<meta property="og:url" content="' + re.escape(url) + r'"',
                     (site / 'index.html').read_text(encoding='utf-8')):
        raise ValueError('Site metadata URL does not match requested GitHub account/repository')
    if not any((site / f'social-preview.{ext}').exists() for ext in ('jpg','png','webp')):
        raise ValueError('Social preview image missing')
    if (site / '.git').exists():
        raise ValueError('Site directory already contains git history; use a fresh bundle')
    if not shutil.which('gh') or not shutil.which('git'):
        raise RuntimeError('Automatic publish requires Git and the GitHub CLI (gh); manual upload is documented in PUBLISH_CHECKLIST.md')
    actual = run_command(['gh','api','user','--jq','.login'], capture=True).stdout.strip()
    if actual.casefold() != account.casefold():
        raise ValueError(f'Authenticated GitHub account {actual!r} does not match requested account {account!r}')
    existing = subprocess.run(['gh','repo','view',f'{account}/{repo}','--json','name'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if existing.returncode == 0:
        raise ValueError('Repository already exists; refusing to overwrite existing content')
    # Only the fixed, inspected site payload is committed; no raw résumé or evidence report.
    run_command(['git','init','-b','main'], cwd=site)
    run_command(['git','add','index.html','.nojekyll'] + [p.name for p in site.glob('social-preview.*')], cwd=site)
    run_command(['git','commit','-m','Publish approved SimpliCITY world'],cwd=site)
    run_command(['gh','repo','create',f'{account}/{repo}','--public','--source','.','--remote','origin','--push'],cwd=site)
    try:
        run_command(['gh','api','-X','POST',f'repos/{account}/{repo}/pages',
                     '-f','source[branch]=main','-f','source[path]=/'],cwd=site)
    except subprocess.CalledProcessError:
        # Repository is already public; never claim Pages was enabled when the API fails.
        print('Repository created and pushed. Pages API setup was not confirmed; enable it manually in repository Settings > Pages.', file=sys.stderr)
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='command', required=True)
    prep = actions.add_parser('prepare', help='Make a reviewed site bundle and social share draft (no upload)')
    prep.add_argument('--html', required=True, type=Path)
    prep.add_argument('--account', required=True)
    prep.add_argument('--repo', required=True)
    prep.add_argument('--out', type=Path, required=True)
    prep.add_argument('--preview', type=Path, help='Original JPEG/PNG/WebP image; default: browser screenshot')
    pub = actions.add_parser('deploy', help='Explicitly publish a prepared bundle using authenticated gh CLI')
    pub.add_argument('--bundle', required=True, type=Path)
    pub.add_argument('--account', required=True)
    pub.add_argument('--repo', required=True)
    pub.add_argument('--approve-public', action='store_true', help='Owner explicitly approves public publication')
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            url = prepare(args.html, args.account, args.repo, args.out, args.preview)
            print(f'Prepared {args.out}/site for {url}\nReview {args.out}/PUBLISH_CHECKLIST.md before publishing. No upload occurred.')
        else:
            url = deploy(args.bundle, args.account, args.repo, args.approve_public)
            print(f'Repository creation and push completed. Confirm GitHub Pages deployment at {url} before sharing.')
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f'ERROR: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
