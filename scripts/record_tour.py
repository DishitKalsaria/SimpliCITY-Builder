#!/usr/bin/env python3
"""Capture an actual Chromium-guided tour to a self-contained silent WebM.

Developer-only: Playwright, Chromium, and local ffmpeg (no network).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def record(source: Path, output: Path) -> None:
    from playwright.sync_api import sync_playwright
    encoder = shutil.which('ffmpeg')
    if not encoder:
        raise RuntimeError('ffmpeg required to produce guided-tour video')
    with tempfile.TemporaryDirectory() as temp:
        frames = Path(temp)
        with sync_playwright() as playwright:
            chromium = shutil.which('chromium') or shutil.which('google-chrome')
            browser = (playwright.chromium.launch(headless=True, executable_path=chromium,
                                                  args=['--no-sandbox']) if chromium else
                       playwright.chromium.launch(headless=True))
            try:
                page = browser.new_page(viewport={'width': 1280, 'height': 800})
                page.set_content(source.read_text(encoding='utf-8'), wait_until='load')
                page.emulate_media(reduced_motion='reduce')
                index = 0
                def capture(seconds: int) -> None:
                    nonlocal index
                    for _ in range(seconds * 4):
                        page.screenshot(path=str(frames / f'{index:04d}.png'))
                        index += 1
                capture(1)
                page.locator('#start-tour').click()
                capture(2)
                for _ in range(2):
                    page.locator('dialog.detail-dialog[open] [data-tour="next"]').click()
                    capture(2)
                page.locator('dialog.detail-dialog[open] [data-tour="exit"]').click()
                capture(1)
                page.close()
            finally:
                browser.close()
        output.parent.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run([encoder, '-hide_banner', '-loglevel', 'error',
                               '-y', '-framerate', '4', '-i', str(frames / '%04d.png'),
                               '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34',
                               '-pix_fmt', 'yuv420p', str(output)],
                              text=True, capture_output=True)
        if proc.returncode:
            raise RuntimeError(proc.stderr)
        print(f'PASS actual browser-guided-tour frames encoded: {output}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('html', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    record(args.html, args.output)


if __name__ == '__main__':
    main()
