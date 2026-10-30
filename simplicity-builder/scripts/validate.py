#!/usr/bin/env python3
"""Verify JSON schema and presence of functional offline map UI."""
import json
import re
import sys
from pathlib import Path
from build_portfolio import validate_model


def validate(json_path: Path, html_path: Path) -> None:
    data=json.loads(json_path.read_text(encoding='utf-8'))
    validate_model(data)
    output=html_path.read_text(encoding='utf-8')
    checks={
        'HTML document':'<!doctype html>' in output.lower(),
        'one hotspot per section':output.count('class="hotspot motion-float"')==len(data['sections']),
        'accessible list fallback':output.count('class="landmark"')==len(data['sections']),
        'accessible dialogs':output.count('class="detail-dialog"')==len(data['sections']),
        'no document scroll':'height:100dvh' in output and 'overflow:hidden' in output,
        'recruiter view':'id="recruiter-dialog"' in output,
        'all narrative text substituted':not re.search(r'%%[A-Z0-9_]+%%',output),
        'no external scripts':not re.search(r'<script\b[^>]*\bsrc\s*=',output,re.I),
        'no external stylesheets':not re.search(r'<link\b[^>]*\brel\s*=\s*["\']stylesheet',output,re.I),
        'responsive viewport':'name="viewport"' in output,
    }
    for name,ok in checks.items():print(f'{"PASS" if ok else "FAIL"} {name}')
    if not all(checks.values()):raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: validate.py portfolio.json index.html')
    validate(Path(sys.argv[1]),Path(sys.argv[2]))
