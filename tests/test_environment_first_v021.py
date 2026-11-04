"""v0.2.1 environment-first scenes: content objects, geometry and version safety."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder/scripts'))
from scene_art import build_scene, family_for, palette_for, _semantic_shape
from build_portfolio import generate, sanitize_scene
from build_experience import to_portfolio


class EnvironmentFirstTests(unittest.TestCase):
    def test_theme_matching_uses_boundaries_and_room_priority(self):
        self.assertEqual(family_for('inviting modern meeting room'), 'meeting')
        self.assertEqual(family_for('a public playground'), 'playground')
        self.assertEqual(family_for('an agricultural working farm'), 'farm')
        self.assertEqual(family_for('a smart city'), 'invented')
        self.assertNotEqual(family_for('pharmacy'), 'farm')
        self.assertEqual(family_for('volcanic citadel Guardian Command Center'), 'volcanic')
        self.assertEqual(len({palette_for(n) for n in ('meeting room','playground','farm')}), 3)

    def test_chapter_titles_define_structures_not_just_index(self):
        self.assertEqual(_semantic_shape('meeting', 'Team Laptop', 0), 'laptop')
        self.assertEqual(_semantic_shape('meeting', 'Planning Whiteboard', 0), 'whiteboard')
        self.assertEqual(_semantic_shape('playground', 'Sandbox Activities', 0), 'sandbox')
        self.assertEqual(_semantic_shape('farm', 'Farm Tractor', 0), 'tractor')
        self.assertEqual(_semantic_shape('farm', 'Irrigation Pond', 0), 'pond')
        sections = [{'id': 'item', 'name': 'Team Laptop'}]
        scene = build_scene('meeting room', sections)
        self.assertIn('fill="#c8dde0"', scene)
        self.assertNotIn('stroke="#ff6829"', scene)

    def test_one_to_eight_landmarks_in_all_environment_families(self):
        kinds = ('meeting room', 'playground', 'working farm', 'volcanic citadel',
                 'guardian academy', 'space constellation', 'ocean reef', 'toon city',
                 'nature forest', 'museum', 'technology laboratory', 'fantasy castle',
                 'music festival', 'desert oasis', 'noir city', 'invented dreamworld')
        for theme in kinds:
            for count in range(1, 9):
                sections = [{'id': f'place-{i}', 'name': f'Place {i}'} for i in range(count)]
                for mobile in (False, True):
                    with self.subTest(theme=theme, count=count, mobile=mobile):
                        artwork = build_scene(theme, sections, mobile)
                        cleaned = sanitize_scene(artwork, section_ids={s['id'] for s in sections})
                        self.assertIn('<svg class="scene-svg"', cleaned)
                        self.assertEqual(artwork.count('id="landmark-'), count)

    def test_generated_pages_keep_v021_interface_and_reachable_objects(self):
        for key in ('meeting-room', 'playground', 'farm'):
            source = ROOT / 'simplicity-builder/examples' / f'{key}-sample.json'
            data = json.loads(source.read_text(encoding='utf-8'))
            page = generate(to_portfolio(data))
            self.assertIn('data-count="4"', page)
            self.assertIn('id="mobile-scene-template"', page)
            self.assertEqual(page.count('class="scene-landmark"'), 8)  # desktop + portrait
            self.assertIn('Start guided tour', page)
            self.assertIn('id="list-dialog"', page)
            self.assertTrue((ROOT / 'docs' / f'{key}.html').is_file())

    def test_v021_version_is_unchanged(self):
        skill = (ROOT / 'simplicity-builder/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('version: "0.2.1"', skill)
        self.assertIn('# SimpliCITY Builder v0.2.1', skill)


if __name__ == '__main__':
    unittest.main()
