#!/usr/bin/env python3
"""Make reproducible-ish public source/skill ZIPs and a SHA256 release manifest.

Run from the exact tagged revision. Excludes private data, caches and git internals.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import zipfile
from pathlib import Path
from package_skill import make_skill

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '.venv', '.pytest_cache', '__pycache__', 'private', 'dist', 'out', '.mypy_cache'}
EXCLUDED_GLOBS = ('*.pyc', '*.zip', 'SHA256SUMS.txt', '*.log', '.env', '.env.*')


def files_to_package():
    for path in sorted(ROOT.rglob('*')):
        relative = path.relative_to(ROOT)
        if not path.is_file() or any(x in EXCLUDED_DIRS for x in relative.parts):
            continue
        if relative.as_posix() in {'index.html', 'portfolio.json'} or any(relative.match(pattern) for pattern in EXCLUDED_GLOBS):
            continue
        if path.is_symlink():
            continue
        yield path, relative.as_posix()


def package(label: str):
    if not re.fullmatch(r'v0\.1\.5(?:-rc\.[1-9][0-9]*)?', label):
        raise ValueError('Expected v0.1.5 or v0.1.5-rc.N')
    skill = ROOT / f'SimpliCITY-Builder-Skill-{label}.zip'
    source = ROOT / f'SimpliCITY-Builder-Complete-Source-{label}.zip'
    make_skill(skill)
    with zipfile.ZipFile(source, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for path, arcname in files_to_package():
            z.write(path, arcname)
    hashes = ROOT / 'SHA256SUMS.txt'
    hashes.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in (skill, source)))
    for path in (skill, source):
        with zipfile.ZipFile(path) as z:
            corrupt=z.testzip()
            if corrupt:
                raise RuntimeError(f'Broken archive member: {corrupt}')
    print(f'Created {skill.name}, {source.name}, SHA256SUMS.txt')

if __name__ == '__main__':
    arg = argparse.ArgumentParser()
    arg.add_argument('--label', default='v0.1.5')
    package(arg.parse_args().label)
