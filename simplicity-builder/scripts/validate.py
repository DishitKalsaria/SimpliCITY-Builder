#!/usr/bin/env python3
"""Verify JSON schema and presence of a functional offline world interface.

SVG landmarks are inspected as XML elements, not fragile string fragments.
This supports combined classes (including animation classes), both the desktop
and optional mobile SVG, and rejects duplicates/missing landmarks.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from build_portfolio import validate_model


def named_scene_landmarks_valid(html: str, section_ids: set[str], has_mobile_scene: bool) -> bool:
    """Require one accessible, uniquely named landmark per section in each scene."""
    scenes = re.findall(r'<svg\b[^>]*\bclass="scene-svg"[^>]*>.*?</svg>', html, flags=re.S)
    if len(scenes) != (2 if has_mobile_scene else 1):
        return False
    expected = {f'landmark-{section_id}' for section_id in section_ids}
    for markup in scenes:
        try:
            svg = ET.fromstring(markup)
        except ET.ParseError:
            return False
        landmarks = [
            element for element in svg.iter()
            if element.tag.rsplit('}', 1)[-1] == 'g'
            and element.get('id', '').startswith('landmark-')
        ]
        if len(landmarks) != len(expected):
            return False
        if {node.get('id') for node in landmarks} != expected:
            return False
        for node in landmarks:
            if ('scene-landmark' not in node.get('class', '').split()
                    or node.get('role') != 'button'
                    or node.get('tabindex') != '0'
                    or not node.get('aria-label')
                    or not node.get('data-dialog')):
                return False
    return True


def validate(json_path: Path, html_path: Path) -> None:
    data = json.loads(json_path.read_text(encoding='utf-8'))
    validate_model(data)
    output = html_path.read_text(encoding='utf-8')
    checks = {
        'HTML document': '<!doctype html>' in output.lower(),
        'one named SVG object per section': named_scene_landmarks_valid(
            output,
            {section['id'] for section in data['sections']},
            '<template id="mobile-scene-template">' in output,
        ),
        'no HTML pin overlays': 'class="hotspot' not in output and 'spot-dot' not in output,
        'accessible list fallback': output.count('class="landmark"') == len(data['sections']),
        'accessible dialogs': output.count('class="detail-dialog"') == len(data['sections']),
        'no document scroll': 'height:100dvh' in output and 'overflow:hidden' in output,
        'recruiter view': 'id="recruiter-dialog"' in output,
        'all narrative text substituted': not re.search(r'%%[A-Z0-9_]+%%', output),
        'no external scripts': not re.search(r'<script\b[^>]*\bsrc\s*=', output, re.I),
        'no external stylesheets': not re.search(r'<link\b[^>]*\brel\s*=\s*["\']stylesheet', output, re.I),
        'responsive viewport': 'name="viewport"' in output,
    }
    for name, ok in checks.items():
        print(f'{"PASS" if ok else "FAIL"} {name}')
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: validate.py portfolio.json index.html')
    validate(Path(sys.argv[1]), Path(sys.argv[2]))
