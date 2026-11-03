#!/usr/bin/env python3
"""Run the same lint, type, and unit checks used by GitHub Actions.

Usage after `python -m pip install -r requirements-dev.txt`:
    python scripts/ci_preflight.py all

This script has no runtime dependencies; Ruff and mypy are developer tools only.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUFF_TARGETS = (
    'simplicity-builder/scripts/scene_art.py',
    'simplicity-builder/scripts/build_experience.py',
    'simplicity-builder/scripts/validate_experience.py',
    'simplicity-builder/scripts/build.py',
    'simplicity-builder/scripts/check.py',
    'simplicity-builder/scripts/verify_source.py',
    'scripts/package_skill.py',
    'scripts/ci_preflight.py',
)
MYpy_TARGETS = (
    'simplicity-builder/scripts/scene_art.py',
    'simplicity-builder/scripts/build_experience.py',
)


def source_fingerprints() -> None:
    print('Source fingerprints (compare with the files in your pushed commit):', flush=True)
    for relative in MYpy_TARGETS:
        path = ROOT / relative
        print(f'  SHA256 {hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}', flush=True)


def check_tools(names: tuple[str, ...]) -> bool:
    missing = [name for name in names if shutil.which(name) is None]
    if missing:
        print(f'Missing developer tool(s): {", ".join(missing)}', file=sys.stderr)
        print('Install them with: python -m pip install -r requirements-dev.txt', file=sys.stderr)
        return False
    return True


def run_step(command: list[str]) -> int:
    print('\n$ ' + ' '.join(command), flush=True)
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('step', choices=('all', 'lint', 'types', 'tests', 'fingerprint'),
                        nargs='?', default='all')
    args = parser.parse_args()
    source_fingerprints()
    if args.step == 'fingerprint':
        return 0
    required_tools = tuple(name for name, active in (
        ('ruff', args.step in ('all', 'lint')),
        ('mypy', args.step in ('all', 'types')),
    ) if active)
    if not check_tools(required_tools):
        return 2
    commands = {
        'lint': ['ruff', 'check', *RUFF_TARGETS, '--select', 'E4,E7,E9,F821,F822,F823'],
        'types': ['mypy', *MYpy_TARGETS, '--follow-imports=skip', '--ignore-missing-imports'],
        'tests': [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
    }
    selected = ('lint', 'types', 'tests') if args.step == 'all' else (args.step,)
    for step in selected:
        result = run_step(commands[step])
        if result:
            print(f'FAIL: {step} returned exit status {result}', file=sys.stderr)
            return result
    print('\nPASS: all selected pre-push checks passed.', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
