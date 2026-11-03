#!/usr/bin/env python3
"""Detect input schema and independently validate the generated HTML and claims."""
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from build_portfolio import validate_model
from build_experience import to_portfolio
from validate import validate
from verify_source import evidence_issues
from verify_facts import evidence_gaps


def detect_schema(data: dict) -> str:
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    experience = {'source', 'experience', 'chapters'} <= data.keys()
    resume = {'profile', 'world', 'sections'} <= data.keys()
    if experience == resume:
        raise ValueError('Expected exactly one schema: source/experience/chapters OR profile/world/sections')
    return 'experience' if experience else 'resume'


def check(input_path: Path, html_path: Path | None = None, source_text: Path | None = None) -> None:
    data = json.loads(input_path.read_text(encoding='utf-8'))
    schema = detect_schema(data)
    text = source_text.read_text(encoding='utf-8') if source_text else None
    if schema == 'experience':
        portfolio = to_portfolio(data)
        issues = evidence_issues(data, text)
    else:
        validate_model(data)
        portfolio = data
        issues = []
        if text is not None:
            # Matching numbers and names is conservative, not semantic verification.
            for gap in evidence_gaps(data, text):
                if gap['kind'] in ('number or date', 'named claim'):
                    issues.append(f'{gap["field"]}: unsupported {gap["kind"]} {gap["claim"]!r}')
    if issues:
        raise ValueError('Evidence review failed:\n- ' + '\n- '.join(issues))
    if text is None and schema == 'experience' and data['source']['kind'] != 'prompt':
        print('NOTICE Evidence excerpts checked for coverage and numbers; actual source comparison unavailable without --source-text. Human review required.')
    if html_path is not None:
        if schema == 'resume':
            validate(input_path, html_path)
        else:
            with tempfile.TemporaryDirectory(prefix='simpli-check-') as temp:
                adapted = Path(temp) / 'legacy.json'
                adapted.write_text(json.dumps(portfolio), encoding='utf-8')
                validate(adapted, html_path)
    print(f'PASS {schema} schema, available evidence, and HTML checks')


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate either schema and generated HTML')
    parser.add_argument('input', type=Path)
    parser.add_argument('html', type=Path)
    parser.add_argument('--source-text', type=Path, help='Private text extracted by the host, never bundled in HTML')
    args = parser.parse_args()
    try:
        check(args.input, args.html, args.source_text)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
