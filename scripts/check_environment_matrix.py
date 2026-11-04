#!/usr/bin/env python3
"""Browser QA across environment types, 1–8 landmarks, and five real viewports.

Optional developer dependency: Playwright + Chromium. This does not certify art
quality, factual accuracy, or the quality of a host-generated scenic image.
"""
from __future__ import annotations

import argparse
import json
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


# Alternate plaque metrics reproduce the previously reported failures. Keep
# these as browser checks instead of lowering the visual QA thresholds.
PLAQUE_STRESS = (
    ('meeting-7-small-phone', 'meeting', 7, 'small-phone', 10, ()),
    ('meeting-8-small-phone', 'meeting', 8, 'small-phone', 10, ()),
    ('meeting-8-larger-text', 'meeting', 8, 'small-phone', 12, ()),
    ('ocean-8-landscape', 'ocean', 8, 'landscape', 12, ()),
    ('ocean-8-long-labels', 'ocean', 8, 'landscape', 16, (
        'Coral Observatory', 'Ocean Research Library', 'Sunken Shipwreck',
        'Marine Wildlife Studies', 'Deep Sea Laboratory', 'Kelp Forest Station',
        'Tidal Energy Workshop', 'Submarine Exploration',
    )),
    # The 200px plaque cap used to wrap these labels into two lines and
    # strand two of them in the shallow ocean landscape. Preserve both cases.
    ('ocean-8-wide-text-18', 'ocean', 8, 'landscape', 18, (
        'Coral Observatory', 'Ocean Research Library', 'Sunken Shipwreck',
        'Marine Wildlife Studies', 'Deep Sea Laboratory', 'Kelp Forest Station',
        'Tidal Energy Workshop', 'Submarine Exploration',
    )),
    ('ocean-8-wide-text-24', 'ocean', 8, 'landscape', 24, (
        'Coral Observatory', 'Ocean Research Library', 'Sunken Shipwreck',
        'Marine Wildlife Studies', 'Deep Sea Laboratory', 'Kelp Forest Station',
        'Tidal Energy Workshop', 'Submarine Exploration',
    )),
    ('ocean-8-wide-text-22', 'ocean', 8, 'landscape', 22, (
        'Coral Observatory', 'Ocean Research Library', 'Sunken Shipwreck',
        'Marine Wildlife Studies', 'Deep Sea Laboratory', 'Kelp Forest Station',
        'Tidal Energy Workshop', 'Submarine Exploration',
    )),
)


# These variants reproduced Ubuntu-versus-Windows font-metric failures. The
# letter-spacing case remains useful even when a named font is unavailable.
PLAQUE_FONT_VARIANTS = (
    ('meeting-8-larger-text', 'dejavu', 'font-family:"DejaVu Sans",sans-serif !important'),
    ('meeting-8-larger-text', 'monospace', 'font-family:monospace !important'),
    ('meeting-8-larger-text', 'wide-letters', 'letter-spacing:.8px !important'),
    ('ocean-8-wide-text-24', 'dejavu', 'font-family:"DejaVu Sans",sans-serif !important'),
    ('ocean-8-wide-text-24', 'monospace', 'font-family:monospace !important'),
    ('ocean-8-wide-text-24', 'wide-letters', 'letter-spacing:.8px !important'),
    ('ocean-8-wide-text-22', 'dejavu', 'font-family:"DejaVu Sans",sans-serif !important'),
)


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


def verify_ocean_banks(page, name: str) -> None:
    # A label above/below a dense bank can strand others on different
    # Chromium/font stacks. In short landscape, each label belongs beside its
    # left or right ocean landmark bank.
    placements = page.locator('.scene-plaque').evaluate_all(
        '(nodes) => nodes.map(node => node.dataset.placement)'
    )
    if len(placements) != 8 or any(value not in ('left', 'right') for value in placements):
        raise AssertionError(f'{name}: ocean bank layout not engaged: {placements}')


def save_failure_diagnostics(page, name: str) -> None:
    # GitHub Actions uploads private/screenshots even when a browser step fails.
    # Record geometry and font details to distinguish CI font metrics, different
    # SVG bounds, and a failed placement attempt from version mismatches.
    destination = ROOT / 'private/screenshots/matrix-failures'
    destination.mkdir(parents=True, exist_ok=True)
    label = name.replace(' ', '-').replace('/', '-')
    try:
        details = page.evaluate('''() => {
          const box=e=>{const r=e.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height}};
          return {viewport:{width:innerWidth,height:innerHeight},frame:box(document.querySelector('.scene-world')),
            fonts:document.fonts?.status,readyState:document.readyState,
            plaques:[...document.querySelectorAll('.scene-plaque')].map(p=>({
              text:p.textContent.trim(),for:p.dataset.plaqueFor,
              placement:p.dataset.placement,rect:box(p),font:getComputedStyle(p).font})),
            targets:[...document.querySelectorAll('.scene-landmark')].map(p=>({id:p.id,rect:box(p)}))};
        }''')
        (destination / f'{label}.json').write_text(json.dumps(details, indent=2), encoding='utf-8')
        page.screenshot(path=str(destination / f'{label}.png'))
        print(f'Diagnostics saved under {destination / label}', file=sys.stderr)
    except Exception as error:
        print(f'Diagnostics for {name} could not be saved: {error}', file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--new-only', action='store_true', help='Only test new settings across all 1–8 counts')
    mode.add_argument('--plaque-stress', action='store_true', help='Recheck dense labels using alternate text metrics')
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
            if args.plaque_stress:
                viewport_by_name = {label: (width, height) for label, width, height in VIEWPORTS}
                cases = [(*case, '') for case in PLAQUE_STRESS]
                by_name = {case[0]: case for case in PLAQUE_STRESS}
                for base_name, variant, css in PLAQUE_FONT_VARIANTS:
                    _, *parameters = by_name[base_name]
                    cases.append((f'{base_name}-{variant}', *parameters, css))
                for name, family, count, viewport, font_px, titles, extra_css in cases:
                    width, height = viewport_by_name[viewport]
                    theme, default_titles = THEMES[family]
                    markup = make_world(theme, titles or default_titles, count)
                    page = browser.new_page(viewport={'width': width, 'height': height},
                                            device_scale_factor=1)
                    try:
                        page.emulate_media(reduced_motion='reduce')
                        page.set_content(markup, wait_until='load')
                        page.add_style_tag(content=f'body .scene-plaque {{font-size:{font_px}px !important; {extra_css}}}')
                        page.evaluate("window.dispatchEvent(new Event('resize'))")
                        assert_visual(page, name)
                        if family == 'ocean' and count == 8:
                            verify_ocean_banks(page, name)
                        passed += 1
                    except Exception as exc:
                        failures.append(f'{name}: {exc}')
                        save_failure_diagnostics(page, name)
                    finally:
                        page.close()
                    print(f'Checked {name}', flush=True)
            else:
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
                                if family == 'ocean' and count == 8 and label == 'landscape':
                                    verify_ocean_banks(page, f'{family} {count} {label}')
                                passed += 1
                            except Exception as exc:
                                failures.append(f'{family} {count} {label}: {exc}')
                                save_failure_diagnostics(page, f'{family} {count} {label}')
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
