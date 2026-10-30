import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / 'simplicity-builder' / 'scripts' / 'build_portfolio.py'
spec = importlib.util.spec_from_file_location('simpli_city_build', MODULE)
builder = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = builder
spec.loader.exec_module(builder)

class BuildTests(unittest.TestCase):
    def load(self, name='fairytale'):
        return json.loads((ROOT / 'examples' / f'{name}-sample.json').read_text(encoding='utf-8'))

    def test_all_sample_themes(self):
        for theme in ('fairytale', 'space', 'custom', 'clockwork'):
            with self.subTest(theme=theme):
                result = builder.generate(self.load(theme))
                self.assertIn('<!doctype html>', result)
                self.assertIn('dialog.showModal()', result)
                self.assertEqual(result.count('class="landmark"'), len(self.load(theme)['sections']))
                self.assertNotIn('%%TITLE%%', result)
                self.assertNotIn('src="https://', result)

    def test_escapes_untrusted_text(self):
        data = self.load()
        data['profile']['name'] = '<script>alert(1)</script>'
        data['sections'][0]['entries'][0]['title'] = 'A & B <Testing>'
        result = builder.generate(data)
        self.assertNotIn('<script>alert(1)</script>', result)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', result)
        self.assertIn('A &amp; B &lt;Testing&gt;', result)

    def test_rejects_dangerous_url(self):
        data = self.load()
        data['profile']['links'] = [{'label':'bad','url':'javascript:alert(1)'}]
        with self.assertRaises(ValueError):
            builder.generate(data)

    def test_rejects_invalid_color(self):
        data = self.load()
        data['world']['accent'] = 'red;background:url(https://evil.test)'
        with self.assertRaises(ValueError):
            builder.generate(data)

    def test_rejects_duplicate_ids(self):
        data = self.load()
        data['sections'].append(dict(data['sections'][0]))
        with self.assertRaises(ValueError):
            builder.generate(data)

    def test_arbitrary_prompt_theme_is_supported(self):
        data = self.load('custom')
        self.assertEqual(data['world']['theme'], 'midnight-festival')
        page = builder.generate(data)
        self.assertIn('The nocturnal concert grounds', page)
        self.assertIn('<svg class=\"scene-svg\"', page)
        self.assertIn('path d=', page)

    def test_custom_svg_rejects_scripts_and_external_resources(self):
        for payload in (
            '<svg viewBox=\"0 0 620 520\"><script>alert(1)</script></svg>',
            '<svg viewBox=\"0 0 620 520\"><image href=\"https://evil.test/x\"/></svg>',
            '<svg viewBox=\"0 0 620 520\"><circle cx=\"10\" cy=\"10\" r=\"10\" onload=\"alert(1)\"/></svg>',
            '<svg viewBox=\"0 0 620 520\"><rect width=\"10\" height=\"10\" fill=\"url(https://evil.test/a)\"/></svg>',
        ):
            with self.subTest(svg=payload):
                data = self.load('custom')
                data['world']['scene_svg'] = payload
                with self.assertRaises(ValueError): builder.generate(data)

    def test_rejects_light_background(self):
        data = self.load()
        data['world']['background'] = '#ffffff'
        with self.assertRaises(ValueError): builder.generate(data)

    def test_custom_unknown_theme_works_without_svg(self):
        data = self.load()
        data['world']['theme'] = 'sandcastle-safari'
        result = builder.generate(data)
        self.assertIn('sandcastle-safari', result)

    def test_single_pass_template_replacement(self):
        data = self.load()
        data['profile']['summary'] = 'Research into the literal token %%LANDMARKS%%.'
        result = builder.generate(data)
        self.assertIn('%%LANDMARKS%%', result)


if __name__ == '__main__':
    unittest.main()
