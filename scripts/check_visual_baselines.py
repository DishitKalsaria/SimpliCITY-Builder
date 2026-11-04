#!/usr/bin/env python3
"""Fail CI when approved golden screenshots drift beyond a documented tolerance.

Optional developer dependency: Pillow. Only fixed viewport/dataset screenshots
are compared. Pixel matching cannot replace manual composition review.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINES = ('guardian-desktop.png','guardian-mobile.png',
             'photo-desktop.png','photo-mobile.png',
             'volcanic-desktop.png','volcanic-mobile.png',
             'toon-desktop.png','toon-mobile.png')


def changed_fraction(old: Path,new: Path,pixel_threshold: int=8) -> float:
    try:
        from PIL import Image,ImageChops
    except ImportError as exc:
        raise RuntimeError('Pillow required for golden CI checks') from exc
    with Image.open(old) as a,Image.open(new) as b:
        a=a.convert('RGB')
        b=b.convert('RGB')
        if a.size!=b.size:
            raise ValueError(f'Image dimensions differ: {old.name} {a.size} vs {b.size}')
        diff=ImageChops.difference(a,b).convert('L')
        histogram=diff.histogram()
        return sum(histogram[pixel_threshold+1:])/(a.width*a.height)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--screenshots',type=Path,required=True)
    ap.add_argument('--tolerance',type=float,default=.25,help='Maximum fraction of changed pixels (default 25%%)')
    args=ap.parse_args()
    if not 0<=args.tolerance<=1:
        ap.error('Tolerance must lie between 0 and 1')
    failures=[]
    for name in BASELINES:
        old=ROOT/'tests/visual-golden'/name
        new=args.screenshots/name
        if not old.is_file() or not new.is_file():
            failures.append(f'{name}: missing golden or current screenshot')
            continue
        try:
            fraction=changed_fraction(old,new)
        except (OSError,ValueError,RuntimeError) as err:
            failures.append(f'{name}: {err}')
            continue
        print(f'{name}: {fraction:.2%} changed (limit {args.tolerance:.0%})')
        if fraction>args.tolerance:
            failures.append(f'{name}: visual drift over tolerance')
    if failures:
        ap.exit(1,'FAIL golden screenshot checks:\n- '+'\n- '.join(failures)+'\n')
    print('PASS checked-in golden screenshot tolerance gate. Human visual approval is separate.')

if __name__=='__main__':
    main()
