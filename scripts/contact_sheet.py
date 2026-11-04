#!/usr/bin/env python3
"""Create a deterministic one-image review grid from real Chromium screenshots.

CI-only Pillow dependency; does not change the stdlib-only installed skill.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def make_sheet(folder: Path, output: Path, worlds: tuple[str, ...]) -> None:
    from PIL import Image, ImageDraw
    # Every named world must supply both real viewport screenshots; missing
    # worlds are a failure, never an invisible hole in the contact sheet.
    images = [(world, folder / f'{world}-desktop.png', folder / f'{world}-mobile.png')
              for world in worlds]
    missing = [str(p) for _, desktop, mobile in images for p in (desktop, mobile) if not p.is_file()]
    if missing:
        raise FileNotFoundError('Missing browser review screenshots: '+', '.join(missing))
    row_height, width = 342, 880
    canvas = Image.new('RGB', (width, row_height * len(images) + 28), '#141522')
    pen = ImageDraw.Draw(canvas)
    pen.text((19, 8), 'SimpliCITY Builder / real-browser visual review / desktop + mobile', fill='#f8d9a7')
    for i, (name, desktop, mobile) in enumerate(images):
        y = 28 + i*row_height
        pen.rectangle((8, y, width-8, y+row_height-9), outline='#565068', width=2)
        pen.text((22, y+9), name.upper(), fill='#ffffff')
        with Image.open(desktop) as original:
            art = original.convert('RGB')
            art.thumbnail((642, 292))
            canvas.paste(art, (17, y+34))
        with Image.open(mobile) as original:
            art = original.convert('RGB')
            art.thumbnail((195, 292))
            canvas.paste(art, (674, y+34))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)
    print(f'PASS contact sheet: {len(images)} worlds, {output}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--screenshots', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--worlds', nargs='+', required=True)
    args = parser.parse_args()
    make_sheet(args.screenshots, args.output, tuple(args.worlds))


if __name__ == '__main__':
    main()
