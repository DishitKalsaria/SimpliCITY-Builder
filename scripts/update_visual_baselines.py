#!/usr/bin/env python3
"""Explicitly refresh tracked goldens after a HUMAN has reviewed new screenshots.

Call with --accept; never updates snapshots merely because a build occurred.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NAMES=('guardian-desktop.png','guardian-mobile.png','photo-desktop.png','photo-mobile.png')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--screenshots',type=Path,required=True)
    p.add_argument('--accept',action='store_true',help='You have visually approved these generated screenshots')
    args=p.parse_args()
    if not args.accept:p.exit(2,'Refusing to update goldens without --accept (human screenshot review required).\n')
    dest=ROOT/'tests/visual-golden'
    for name in NAMES:
        source=args.screenshots/name
        if not source.is_file():p.exit(2,f'Missing screenshot: {source}\n')
    for name in NAMES:
        shutil.copyfile(args.screenshots/name,dest/name)
        print(f'Updated {dest/name}')
    print('Review the changed tracked PNGs in git diff before committing.')

if __name__=='__main__':main()
