"""Regression tests for the exact v0.1.4 sample-generation CI path."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder' / 'scripts'))
from build_portfolio import generate
from validate import named_scene_landmarks_valid, validate


class SceneValidationTests(unittest.TestCase):
    def test_ci_examples_generate_and_validate(self):
        """Exercise the same four examples that GitHub Actions builds."""
        with tempfile.TemporaryDirectory() as tempdir:
            for theme in ('fairytale', 'space', 'custom', 'clockwork'):
                with self.subTest(theme=theme):
                    source = ROOT / 'examples' / f'{theme}-sample.json'
                    data = json.loads(source.read_text(encoding='utf-8'))
                    target = Path(tempdir) / f'{theme}.html'
                    target.write_text(generate(data), encoding='utf-8')
                    with contextlib.redirect_stdout(io.StringIO()):
                        validate(source, target)

    def test_animated_landmarks_and_mobile_scene(self):
        data = json.loads((ROOT / 'examples/space-sample.json').read_text(encoding='utf-8'))
        html = generate(data)
        self.assertIn('class="scene-landmark motion-float"', html)
        self.assertTrue(named_scene_landmarks_valid(
            html, {section['id'] for section in data['sections']}, True))
        self.assertFalse(named_scene_landmarks_valid(
            html.replace('scene-landmark motion-float', 'motion-float', 1),
            {section['id'] for section in data['sections']}, True))


if __name__ == '__main__':
    unittest.main()
