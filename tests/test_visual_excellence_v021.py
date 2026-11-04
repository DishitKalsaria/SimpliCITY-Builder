"""Regression checks for themed 0.2.1 scene art and strict scenic-image input."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder/scripts'))
from scene_art import build_scene, family_for, palette_for
from build_portfolio import sanitize_scene


class VisualExcellenceTests(unittest.TestCase):
    def test_volcanic_theme_wins_over_story_nouns(self):
        self.assertEqual(family_for('volcanic citadel Guardian Command Center'), 'volcanic')
        self.assertEqual(family_for('fairytale guardian academy'), 'guardian')
        self.assertNotEqual(palette_for('volcanic citadel'), palette_for('space station'))

    def test_decorative_depth_and_distinct_architecture(self):
        sections = [{'id': f'location-{i}'} for i in range(4)]
        desktop = build_scene('volcanic citadel', sections)
        portrait = build_scene('volcanic citadel', sections, mobile=True)
        self.assertIn('v21-ridge', desktop)
        self.assertIn('v21-light', desktop)
        self.assertIn('stroke="#ffb162"', desktop)
        self.assertIn('viewBox="0 0 620 880"', portrait)
        self.assertEqual(desktop, build_scene('volcanic citadel', sections))
        self.assertEqual(desktop.count('id="landmark-'), 4)
        self.assertEqual(portrait.count('id="landmark-'), 4)
        ids = {s['id'] for s in sections}
        sanitize_scene(desktop, section_ids=ids)
        sanitize_scene(portrait, section_ids=ids)

    def test_committed_volcanic_reference_is_generated_and_fictional(self):
        fixture = ROOT / 'simplicity-builder/examples/volcanic-sample.json'
        source = json.loads(fixture.read_text(encoding='utf-8'))
        self.assertEqual(source['source']['kind'], 'prompt')
        self.assertIs(source['source']['fictional'], True)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'volcanic.html'
            result = subprocess.run(
                [sys.executable, str(ROOT / 'simplicity-builder/scripts/build.py'),
                 '--input', str(fixture), '--output', str(out)],
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(out.read_bytes(), (ROOT / 'docs/volcanic.html').read_bytes())

    def test_scenic_requires_reviewable_desktop_and_mobile_anchors(self):
        original = json.loads((ROOT / 'examples/fairytale-sample.json').read_text(encoding='utf-8'))
        sections = original['sections']
        image = ROOT / 'simplicity-builder/examples/synthetic-lakeside.png'
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            inp = folder / 'input.json'
            out = folder / 'world.html'
            inp.write_text(json.dumps(original), encoding='utf-8')
            command = [sys.executable, str(ROOT / 'simplicity-builder/scripts/build.py'),
                       '--input', str(inp), '--output', str(out), '--scenic-image', str(image)]
            rejected = subprocess.run(command, text=True, capture_output=True)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('requires authored scene_svg and scene_svg_mobile', rejected.stderr)
            self.assertFalse(out.exists())
            original['world']['scene_svg'] = build_scene('volcanic citadel', sections)
            original['world']['scene_svg_mobile'] = build_scene('volcanic citadel', sections, mobile=True)
            inp.write_text(json.dumps(original), encoding='utf-8')
            accepted = subprocess.run(command, text=True, capture_output=True)
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            html = out.read_text(encoding='utf-8')
            self.assertIn('scenic-art-mode', html)
            self.assertIn('data:image/png;base64,', html)
            self.assertIn('mobile-scene-template', html)
            self.assertIn('scene-landmark', html)
            self.assertNotIn('https://fonts.', html)


if __name__ == '__main__':
    unittest.main()
