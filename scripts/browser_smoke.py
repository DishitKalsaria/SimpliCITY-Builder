#!/usr/bin/env python3
"""Real-browser no-scroll, hotspot, accessibility and clipping checks.

Screenshots require human visual review; basic geometry is not a design critique.
Optional: pip install playwright && python -m playwright install chromium
"""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil

VIEWPORTS=(('desktop',1440,900),('mobile',390,844),('compact',360,640),('small-phone',320,568),('landscape',844,390))


def check(path:Path,browser,screenshots:Path|None=None):
    for label,width,height in VIEWPORTS:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.set_content(path.read_text(encoding='utf-8'),wait_until='load')
        page.emulate_media(reduced_motion='reduce')
        if page.locator('.hotspot').count()<1: raise AssertionError(f'{label}: missing map hotspots')
        if page.locator('button.landmark').count()!=page.locator('.hotspot').count(): raise AssertionError(f'{label}: hotspot/list mismatch')
        metrics=page.evaluate('''() => ({
          docW:document.documentElement.scrollWidth,docH:document.documentElement.scrollHeight,
          winW:innerWidth,winH:innerHeight,bodyScroll:getComputedStyle(document.body).overflow,
          offscreen:[...document.querySelectorAll('.hotspot')].filter(e=>{const r=e.getBoundingClientRect();return r.left<0||r.right>innerWidth||r.top<0||r.bottom>innerHeight}).length,
          unnamed:[...document.querySelectorAll('button')].filter(e=>!((e.getAttribute('aria-label')||e.textContent).trim())).length,
          tiny:[...document.querySelectorAll('.hotspot')].filter(e=>{const r=e.getBoundingClientRect();return r.width<40||r.height<40}).length
        })''')
        if metrics['docW']>width+2 or metrics['docH']>height+2 or metrics['bodyScroll']!='hidden':
            raise AssertionError(f'{path.name} {label}: viewport scroll/overflow: {metrics}')
        if metrics['offscreen'] or metrics['unnamed'] or metrics['tiny']:
            raise AssertionError(f'{path.name} {label}: hotspot visibility or labels: {metrics}')
        if screenshots:
            screenshots.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(screenshots/f'{path.stem}-{label}.png'))
        page.locator('.hotspot').first.click()
        detail=page.locator('dialog.detail-dialog[open]')
        if detail.count()!=1 or detail.locator('.entry').count()<1:
            raise AssertionError(f'{path.name} {label}: hotspot failed to open details')
        page.keyboard.press('Escape')
        if page.locator('dialog[open]').count():raise AssertionError(f'{label}: Escape failed')
        page.locator('[data-dialog="list-dialog"]').last.click()
        if page.locator('#list-dialog[open]').count()!=1:raise AssertionError(f'{label}: location fallback missing')
        search=page.locator('#world-search');search.fill('thisshouldnotexist123')
        if page.locator('button.landmark:visible').count():raise AssertionError(f'{label}: search failed')
        search.fill('')
        if not page.locator('button.landmark:visible').count():raise AssertionError(f'{label}: search restore failed')
        page.keyboard.press('Escape')
        page.locator('[data-dialog="recruiter-dialog"]').first.click()
        if page.locator('#recruiter-dialog[open] .recruiter-section').count()<1:
            raise AssertionError(f'{label}: recruiter fallback missing')
        if errors:raise AssertionError(f'{label}: JavaScript errors {errors}')
        print(f'PASS {path.name} {label} — no page scroll, hotspots, labels, fallback, search, recruiter view')
        page.close()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pages',nargs='+',type=Path)
    ap.add_argument('--screenshots',type=Path)
    args=ap.parse_args()
    try:from playwright.sync_api import sync_playwright
    except ImportError:ap.exit(2,'Install Playwright and Chromium for browser checks.\n')
    with sync_playwright() as p:
        try:browser=p.chromium.launch(headless=True)
        except Exception:
            binary=shutil.which('chromium') or shutil.which('google-chrome')
            if not binary:ap.exit(2,'No Chromium available.\n')
            browser=p.chromium.launch(headless=True,executable_path=binary,args=['--no-sandbox'])
        try:
            for file in args.pages:check(file,browser,args.screenshots)
        finally:browser.close()

if __name__=='__main__':main()
