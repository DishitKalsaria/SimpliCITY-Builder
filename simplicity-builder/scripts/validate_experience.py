#!/usr/bin/env python3
"""Independently validate source-neutral experience JSON and generated offline HTML."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from build_experience import to_portfolio
from validate import validate


def validate_experience(input_path: Path, html_path: Path) -> None:
    data = json.loads(input_path.read_text(encoding='utf-8'))
    portfolio = to_portfolio(data)
    with tempfile.TemporaryDirectory(prefix='simplicity-validation-') as folder:
        source = Path(folder) / 'validated.json'
        source.write_text(json.dumps(portfolio), encoding='utf-8')
        validate(source, html_path)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: validate_experience.py experience.json index.html')
    try:
        validate_experience(Path(sys.argv[1]), Path(sys.argv[2]))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f'Error: {error}') from error
