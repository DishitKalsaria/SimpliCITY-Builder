#!/usr/bin/env python3
"""Browser QA across environment types, 1–8 landmarks, and five real viewports.

Optional developer dependency: Playwright + Chromium. This does not certify art
quality, factual accuracy, or the quality of a host-generated scenic image.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder/scripts'))
from build_experience import to_portfolio
from build_portfolio import generate
from browser_smoke import VIEWPORTS, assert_visual, launch

THEMES = {
    'meeting': ('modern meeting room', ('Presentation Screen', 'Roundtable', 'Planning Whiteboard',
                  'Team Laptop', 'Knowledge Bookshelf', 'Conversation Chair', 'Vision Projector', 'Meeting Notebook')),
    'playground': ('outdoor playground', ('Slide', 'Swing', 'Sandbox', 'Climbing Frame',
                    'Balance Seesaw', 'Roundabout', 'Playhouse', 'Ball Games')),
    'farm': ('agricultural farm', ('Barn', 'Crop Fields', 'Farm Tractor', 'Greenhouse',
             'Fruit Orchard', 'Windmill', 'Silo', 'Irrigation Pond')),
    'volcanic': ('volcanic citadel', ()),
    'guardian': ('guardian academy', ()),
    'space': ('space observatory', ()),
    'ocean': ('ocean reef', ()),
    'toon': ('toon city', ()),
    'nature': ('nature forest', ()),
    'museum': ('history museum', ()),
    'technology': ('technology laboratory', ()),
    'fantasy': ('fantasy kingdom', ()),
    'festival': ('music festival', ()),
    'desert': ('desert oasis', ()),
    'noir': ('film noir', ()),
    'invented': ('unexpected new world', ()),
}


def make_world(theme: str, names: tuple[str, ...], count: int) -> str:
    titles = list(names[:count]) or [f'Chapter {i}' for i in range(count)]
    data = {
        'source': {'kind': 'prompt', 'title': 'Synthetic matrix fixture', 'fictional': True},
        'experience': {'title': f'{theme} quality check', 'theme': theme},
        'chapters': [
            {'title': title, 'summary': 'An invented place for layout verification.',
             'items': [{'title': 'Fictional object', 'description': 'Generated solely for testing.'}]}
            for title in titles
        ],
    }
    return generate(to_portfolio(data))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--new-only', action='store_true', help='Only test new settings across all 1–8 counts')
    args = parser.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Playwright is required to run the browser matrix', file=sys.stderr)
        return 2
    passed = 0
    failures = []
    with sync_playwright() as playwright:
        browser = launch(playwright)
        try:
            for family, (theme, names) in THEMES.items():
                if args.new_only and family not in ('meeting', 'playground', 'farm'):
                    continue
                for count in (range(1, 9) if family in ('meeting', 'playground', 'farm') else (4, 8)):
                    markup = make_world(theme, names, count)
                    for label, width, height in VIEWPORTS:
                        page = browser.new_page(viewport={'width': width, 'height': height},
                                                device_scale_factor=1)
                        try:
                            page.emulate_media(reduced_motion='reduce')
                            page.set_content(markup, wait_until='load')
                            assert_visual(page, f'{family} {count} {label}')
                            passed += 1
                        except Exception as exc:
                            failures.append(f'{family} {count} {label}: {exc}')
                        finally:
                            page.close()
                print(f'Checked {family}', flush=True)
        finally:
            browser.close()
    print(f'{passed} viewport checks passed; {len(failures)} failed.')
    if failures:
        for failure in failures:
            print(f'FAIL {failure}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
