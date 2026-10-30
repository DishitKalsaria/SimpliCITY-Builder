#!/usr/bin/env python3
"""Check an SVG scene independently before building a résumé portfolio."""
import argparse
from pathlib import Path
from build_portfolio import sanitize_scene


def main():
    parser = argparse.ArgumentParser(description='Preflight a local original SVG scene against the Builder allowlist.')
    parser.add_argument('svg', type=Path)
    args = parser.parse_args()
    try:
        rendered = sanitize_scene(args.svg.read_text(encoding='utf-8'))
        print(f'PASS: SVG artwork accepted ({len(rendered)} output characters).')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'FAIL: {exc}\nSee simplicity-builder/references/illustration-rules.md\n')


if __name__ == '__main__':
    main()
