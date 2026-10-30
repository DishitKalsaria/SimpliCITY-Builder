#!/usr/bin/env python3
"""Browser smoke test generated offline portfolio HTML at desktop and mobile sizes.

Optional development dependency: pip install playwright && python -m playwright install chromium
"""
from __future__ import annotations

import argparse
from pathlib import Path
import shutil


def check(path: Path, browser, screenshots: Path | None = None) -> None:
    for label, width, height in (('desktop', 1440, 900), ('mobile', 390, 844)):
        page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
        errors: list[str] = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.set_content(path.read_text(encoding='utf-8'), wait_until='load')  # offline, no file:// permission required
        if page.locator('button.landmark').count() < 1:
            raise AssertionError(f'{path.name} {label}: missing landmarks')
        overflow = page.evaluate('document.documentElement.scrollWidth > window.innerWidth + 2')
        if overflow:
            raise AssertionError(f'{path.name} {label}: horizontal overflow')
        if screenshots:
            screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshots / f'{path.stem}-{label}.png'), full_page=True)
        first = page.locator('button.landmark').first
        first.click()
        dialog = page.locator('dialog[open]')
        if dialog.count() != 1 or dialog.locator('article.entry').count() < 1:
            raise AssertionError(f'{path.name} {label}: landmark dialog failed')
        page.keyboard.press('Escape')
        if page.locator('dialog[open]').count() != 0:
            raise AssertionError(f'{path.name} {label}: dialog did not close on Escape')
        search = page.locator('#world-search')
        search.fill('searchtermthatshouldnotexist000')
        if page.locator('button.landmark:visible').count() != 0:
            raise AssertionError(f'{path.name} {label}: search filtering failed')
        search.fill('')
        if page.locator('button.landmark:visible').count() < 1:
            raise AssertionError(f'{path.name} {label}: search reset failed')
        if errors:
            raise AssertionError(f'{path.name} {label}: JS errors: {errors}')
        print(f'PASS {path.name} {label} — no overflow, interactions and JS checks')
        page.close()


def main():
    parser = argparse.ArgumentParser(description='Test generated HTML in real Chromium and optionally save screenshots.')
    parser.add_argument('pages', nargs='+', type=Path)
    parser.add_argument('--screenshots', type=Path, help='Optional local screenshot output directory')
    args = parser.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        parser.exit(2, 'Browser test requires Playwright: python3 -m pip install playwright; python3 -m playwright install chromium\n')
    for path in args.pages:
        if not path.exists():
            parser.error(f'Missing HTML file: {path}')
    try:
        with sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except Exception:
                local_chromium = shutil.which('chromium') or shutil.which('google-chrome')
                if not local_chromium:
                    raise RuntimeError('Chromium not installed. Run python3 -m playwright install chromium')
                browser = playwright.chromium.launch(headless=True, executable_path=local_chromium, args=['--no-sandbox'])
            try:
                for path in args.pages:
                    check(path, browser, args.screenshots)
            finally:
                browser.close()
    except Exception as exc:
        parser.exit(1, f'FAIL browser test: {exc}\n')


if __name__ == '__main__':
    main()
