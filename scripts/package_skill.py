#!/usr/bin/env python3
"""Package the portable Skill with a correctly rooted top-level folder."""
import argparse
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def make_skill(output: Path) -> Path:
    skill = ROOT / 'simplicity-builder'
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(skill.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                z.write(path, path.relative_to(ROOT).as_posix())
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='v0.1.5', help='Release label (e.g. v0.1.5-rc.1)')
    args = parser.parse_args()
    if not args.label.startswith('v0.1.5'):
        parser.error('Label must match current v0.1.5 release family')
    print(make_skill(ROOT / f'SimpliCITY-Builder-Skill-{args.label}.zip'))
