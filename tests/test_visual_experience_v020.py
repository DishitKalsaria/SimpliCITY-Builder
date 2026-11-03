"""Regression cases for failures that basic click/no-scroll tests previously missed."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder'
SCRIPTS = SKILL / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from build_experience import to_portfolio
from build_portfolio import generate, embedded_image
from scene_art import build_scene, family_for, palette_for


class VisualExperienceTests(unittest.TestCase):
    def photo(self):
        return json.loads((SKILL / 'examples/photo-sample.json').read_text(encoding='utf-8'))

    def cli(self, sample: Path, *extra):
        with tempfile.TemporaryDirectory() as folder:
            return subprocess.run([sys.executable, str(SCRIPTS / 'build.py'),
                                   '--input', str(sample), '--output', str(Path(folder) / 'index.html'),
                                   *map(str, extra)], capture_output=True, text=True)

    def test_photo_without_original_image_fails_closed(self):
        process = self.cli(SKILL / 'examples/photo-sample.json')
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('--source-image', process.stderr)

    def test_missing_and_invalid_photo_anchor_fails_closed(self):
        for anchor in (None, {'x': .85, 'y': .4, 'width': .4, 'height': .2},
                       {'x': -.2, 'y': .2, 'width': .2, 'height': .2}):
            with self.subTest(anchor=anchor):
                data = self.photo()
                if anchor is None:
                    data['chapters'][0].pop('anchor')
                else:
                    data['chapters'][0]['anchor'] = anchor
                with self.assertRaisesRegex(ValueError, 'anchor'):
                    to_portfolio(data)

    def test_photo_embeds_original_and_no_procedural_sky_or_ground(self):
        img = embedded_image(SKILL / 'examples/synthetic-lakeside.png')
        html = generate(to_portfolio(self.photo()), img)
        self.assertIn('class="photo-mode ', html)
        self.assertIn('id="photo-anchors"', html)
        self.assertIn('naturalWidth', html)
        self.assertIn('class="photo-ambient"', html)
        self.assertIn('class="scene-backdrop"', html)
        scene = html.split('<svg class="scene-svg"', 1)[1].split('</svg>', 1)[0]
        self.assertNotIn('<path', scene)  # no fabricated mountain silhouette or moon
        self.assertEqual(scene.count('class="scene-landmark"'), 3)
        self.assertIn('Snow-capped Mountains</span>', html)

    def test_procedural_mobile_variant_and_families(self):
        data = json.loads((SKILL / 'references/experience-sample.json').read_text(encoding='utf-8'))
        html = generate(to_portfolio(data))
        self.assertIn('<template id="mobile-scene-template">', html)
        self.assertIn('class="scene-plaque"', html)
        self.assertIn('<body data-theme="cosmic-archive-museum" data-family="museum"', html)
        self.assertNotEqual(build_scene('space travel', to_portfolio(data)['sections'], mobile=False),
                            build_scene('space travel', to_portfolio(data)['sections'], mobile=True))
        self.assertNotEqual(palette_for('underwater sea'), palette_for('colorful guardian robot'))
        self.assertEqual(family_for('cosmic observatory'), 'space')

    def test_single_exhibit_is_featured_and_copy_is_grammatical(self):
        data = json.loads((SKILL / 'examples/link-sample.json').read_text(encoding='utf-8'))
        html = generate(to_portfolio(data))
        self.assertIn('class="single-mode"', html)
        self.assertIn('class="featured-action"', html)
        self.assertIn('Open the featured story', html)
        for bad in ('1 Exhibits', 'Explore experience', 'in an interactive explain',
                    'in an interactive explore'):
            self.assertNotIn(bad, html)
        self.assertIn('ui-sans-serif,system-ui', html)

    def test_browser_smoke_checks_layout_not_only_clicks(self):
        source = (SCRIPTS / 'browser_smoke.py').read_text(encoding='utf-8')
        for check in ('missingPlaques', 'stageCoverage', 'poorContrast',
                      'headerClipped', 'clippedLandmarks', 'photoCoverageLow', 'plaqueOverlap'):
            self.assertIn(check, source)


if __name__ == '__main__':
    unittest.main()
