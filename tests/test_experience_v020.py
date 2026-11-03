"""Source-neutral chat experience, art, privacy and clean installation regressions."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'simplicity-builder/scripts'
sys.path.insert(0, str(SCRIPTS))
from build_experience import to_portfolio
from build_portfolio import generate
from scene_art import build_scene, family_for


class ExperienceTests(unittest.TestCase):
    def example(self):
        return json.loads((ROOT / 'simplicity-builder/references/experience-sample.json').read_text(encoding='utf-8'))

    def test_document_experience_builds_accessible_offline_html(self):
        portfolio = to_portfolio(self.example())
        html = generate(portfolio)
        self.assertIn('An interactive exhibition', html)
        self.assertIn('aria-label=', html)
        self.assertIn('id="landmark-the-observatory"', html)
        self.assertIn('overflow:hidden', html)
        self.assertNotIn('src="https://', html)

    def test_photo_and_link_require_host_source_grounding(self):
        for kind in ('photo', 'document', 'link', 'resume'):
            with self.subTest(kind=kind):
                data = self.example()
                data['source']['kind'] = kind
                if kind == 'link':
                    data['source']['url'] = 'https://example.org/fictional-guide'
                if kind == 'photo':
                    data = json.loads((ROOT / 'simplicity-builder/examples/photo-sample.json').read_text(encoding='utf-8'))
                    from build_portfolio import embedded_image
                    html = generate(to_portfolio(data), embedded_image(ROOT / 'simplicity-builder/examples/synthetic-lakeside.png'))
                else:
                    html = generate(to_portfolio(data))
                self.assertIn('<!doctype html>', html)
                del data['source']['reviewed_by_host']
                with self.assertRaises(ValueError):
                    to_portfolio(data)
        data = self.example()
        data['chapters'][0]['items'][0].pop('source_grounded')
        with self.assertRaises(ValueError):
            to_portfolio(data)

    def test_invalid_urls_fail_and_dont_trigger_retrieval(self):
        data = self.example()
        data['source'].update(kind='link', url='file:///etc/passwd')
        with self.assertRaises(ValueError):
            to_portfolio(data)

    def test_fictional_prompt_does_not_need_attached_source(self):
        data = self.example()
        data['source'] = {'kind': 'prompt', 'title': 'A fictional superhero world', 'fictional': True}
        for chapter in data['chapters']:
            for item in chapter['items']:
                item.pop('source_grounded', None)
        self.assertIn('scene-landmark', generate(to_portfolio(data)))
        data['source'].pop('fictional')
        with self.assertRaises(ValueError):
            to_portfolio(data)

    def test_families_make_visually_distinct_custom_art(self):
        sections = to_portfolio(self.example())['sections']
        scenes = {}
        for theme, expected in [('colorful superhero command center', 'guardian'), ('underwater city', 'ocean'),
                                ('fantasy forest', 'nature'), ('history museum', 'museum'),
                                ('cyber technology lab', 'technology'), ('starship planets', 'space')]:
            with self.subTest(theme=theme):
                self.assertEqual(family_for(theme), expected)
                scene = build_scene(theme, sections)
                self.assertIn('landmark-the-observatory', scene)
                scenes[theme] = scene
        self.assertEqual(len(set(scenes.values())), len(scenes))

    def test_all_modes_accept_source_neutral_content(self):
        for mode, label in [('world', 'An explorable world'), ('explore', 'An interactive exhibition'),
                            ('explain', 'An interactive explainer')]:
            data = self.example()
            data['experience']['mode'] = mode
            self.assertIn(label, generate(to_portfolio(data)))

    def test_clean_zip_can_generate_and_validate_both_formats(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            archive = directory / 'simplicity-builder.zip'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/package_skill.py'),
                                     '--output', str(archive), '--tag', 'v0.2.0'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(archive) as z:
                z.extractall(directory)
                self.assertIn('simplicity-builder/SKILL.md', z.namelist())
                self.assertNotIn('README.md', z.namelist())
            skill = directory / 'simplicity-builder'
            for source, build, validate in [
                ('examples/fairytale-sample.json', 'build_portfolio.py', 'validate.py'),
                ('references/experience-sample.json', 'build_experience.py', 'validate_experience.py')]:
                with self.subTest(source=source):
                    output = directory / 'index.html'
                    for args in [
                        [str(skill / 'scripts' / build), '--input', str(skill / source), '--output', str(output)],
                        [str(skill / 'scripts' / validate), str(skill / source), str(output)]]:
                        result = subprocess.run([sys.executable, *args], cwd=directory, capture_output=True, text=True)
                        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_unreadable_custom_accent_is_rejected(self):
        data = self.example()
        data['experience']['colors'] = {'accent': '#121212', 'secondary': '#101010'}
        with self.assertRaisesRegex(ValueError, 'contrast'):
            generate(to_portfolio(data))

    def test_wrong_tag_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            archive = Path(folder) / 'not-built.zip'
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/package_skill.py'),
                                     '--tag', 'v9.9.9', '--output', str(archive)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(archive.exists())


if __name__ == '__main__':
    unittest.main()
