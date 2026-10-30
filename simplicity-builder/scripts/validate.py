#!/usr/bin/env python3
"""Check the grounded portfolio JSON and basic output integrity."""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from build_portfolio import validate_model


def validate(json_path: Path, html_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding='utf-8'))
    validate_model(data)
    rendered = html_path.read_text(encoding='utf-8')
    checks = {
        'HTML document': '<!doctype html>' in rendered.lower(),
        'all landmarks': rendered.count('class="landmark"') == len(data['sections']),
        'all accessible dialogs': rendered.count('class="detail-dialog"') == len(data['sections']),
        'interactive script': 'dialog.showModal()' in rendered,
        'no unresolved placeholders': not bool(re.search(r'%%[A-Z0-9_]+%%', rendered)),
        'no external scripts': not bool(re.search(r'<script\b[^>]*\bsrc\s*=', rendered, re.I)),
        'no external stylesheets': not bool(re.search(r'<link\b[^>]*\brel\s*=\s*["\']stylesheet', rendered, re.I)),
        'responsive viewport': 'name="viewport"' in rendered,
    }
    for label, result in checks.items():
        print(f'{"PASS" if result else "FAIL"} {label}')
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python3 scripts/validate.py portfolio.json index.html')
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
