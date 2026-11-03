#!/usr/bin/env python3
"""Produce a deterministic, self-contained Agent Skill archive (stdlib only)."""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder'
BLOCKED = {'private', '__pycache__', '.git', '.venv', 'dist', '.mypy_cache', '.pytest_cache'}


def declared_version() -> str:
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.search(r'^  version: ["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', text, re.M)
    if not match:
        raise ValueError('SKILL.md missing metadata.version')
    return match.group(1)


def make_skill(output: Path, tag: str | None = None) -> Path:
    version = declared_version()
    if tag and tag != 'v' + version:
        raise ValueError(f'Tag {tag!r} does not match SKILL.md v{version}')
    if not SKILL.is_dir():
        raise ValueError('Skill directory missing')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(SKILL.rglob('*')):
            if not path.is_file() or path.is_symlink() or any(part in BLOCKED for part in path.parts):
                continue
            if path.suffix in {'.pyc', '.zip'} or path.name.startswith('.env'):
                continue
            arc = path.relative_to(ROOT).as_posix()
            meta = zipfile.ZipInfo(arc, date_time=(2020, 1, 1, 0, 0, 0))
            meta.external_attr = 0o100644 << 16
            meta.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(meta, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(output) as z:
        if z.testzip() is not None or 'simplicity-builder/SKILL.md' not in z.namelist():
            raise ValueError('Skill archive failed integrity check')
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'simplicity-builder.zip')
    parser.add_argument('--tag', help='Optional exact release tag, e.g. v0.2.0')
    parser.add_argument('--label', help='Backward-compatible label, e.g. v0.2.0')
    args = parser.parse_args()
    version = args.tag or args.label
    if args.tag and args.label and args.tag != args.label:
        parser.error('--tag and --label must match')
    try:
        file = make_skill(args.output, tag=version)
        print(f'{file}: SHA256 {hashlib.sha256(file.read_bytes()).hexdigest()}')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')
