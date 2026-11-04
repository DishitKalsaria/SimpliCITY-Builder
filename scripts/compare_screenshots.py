#!/usr/bin/env python3
"""Optional pixel-difference QA aid. Review output manually; changes aren't always defects.

Requires Pillow (NOT required to generate a portfolio): pip install Pillow
"""
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description='Compare browser screenshots with a manual-review baseline.')
    p.add_argument('baseline',type=Path)
    p.add_argument('current',type=Path)
    p.add_argument('--max-changed',type=float,default=0.15)
    a=p.parse_args()
    try:
        from PIL import Image,ImageChops
    except ImportError:
        p.exit(2,'Install Pillow for optional image difference test.\n')
    prior=Image.open(a.baseline).convert('RGB')
    new=Image.open(a.current).convert('RGB')
    if prior.size != new.size:
        p.exit(1,f'FAIL: viewport size changed {prior.size} vs {new.size}\n')
    diff=ImageChops.difference(prior,new)
    hist=diff.convert('L').histogram()
    total=prior.width*prior.height
    changed=sum(hist[8:])/total
    print(f'Changed pixels (difference > 8/255): {changed:.2%} at {prior.width}x{prior.height}')
    if changed>a.max_changed:
        p.exit(1,'Screenshot changed substantially: inspect visual output and approve a new baseline if intentional.\n')
if __name__=='__main__':
    main()
