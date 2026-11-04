"""Theme grammar should differ in geometry and material, not just a heading."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder/scripts'))
from scene_art import build_scene, family_for, palette_for
from build_portfolio import sanitize_scene


class ThemeCompositionTests(unittest.TestCase):
    def test_franchise_cue_chooses_original_toon_family(self):
        self.assertEqual(family_for('Cartoon Network-style original comic town'), 'toon')
        self.assertEqual(family_for('volcanic network citadel'), 'volcanic')
        self.assertNotEqual(family_for('network alone'), 'technology')

    def test_layout_and_backdrop_change_with_family(self):
        sections = [{'id': f'world-{i}'} for i in range(4)]
        scenes = {family: build_scene(f'{family} studio', sections)
                  for family in ('guardian','space','volcanic','ocean','toon')}
        locations = [tuple(re.findall(r'<g id="landmark-[^"]+" transform="([^"]+)"', svg))
                     for svg in scenes.values()]
        self.assertEqual(len(set(locations)),len(locations), 'Families recycled the same coordinates')
        self.assertEqual(len(set(scenes.values())),len(scenes))
        for scene in scenes.values():
            sanitize_scene(scene, section_ids={s['id'] for s in sections})
        self.assertIn('rx="62"', scenes['volcanic'])
        self.assertIn('stroke="#ffb162"', scenes['volcanic'])
        self.assertIn('stroke="#10152f"', scenes['toon'])
        self.assertIn('stroke="#9bdaf9"', scenes['space'])
        self.assertIn('stroke="#9cf4e2"', scenes['ocean'])
        for pastel in ('#9bd6ff','#ffb6d6','#b3f1c6'):
            self.assertNotIn(pastel, scenes['volcanic'])

    def test_two_variants_at_same_count_and_safe_mobile_scene(self):
        sections = [{'id': f'world-{i}'} for i in range(4)]
        variants = [build_scene(theme,sections) for theme in
                    tuple(f'volcanic district {i}' for i in range(12))]
        self.assertGreaterEqual(len(set(variants)),2)
        portrait=build_scene('toon city',sections,mobile=True)
        self.assertIn('viewBox="0 0 620 880"', portrait)
        sanitize_scene(portrait, section_ids={s['id'] for s in sections})

    def test_color_palettes_distinct(self):
        families=['guardian','space','ocean','toon','volcanic']
        self.assertEqual(len({palette_for(f) for f in families}),len(families))


if __name__=='__main__':
    unittest.main()
