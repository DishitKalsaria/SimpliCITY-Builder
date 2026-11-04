"""Chat-first dispatcher, evidence and clean package regressions."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder'


def run(*args, cwd=None):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, cwd=cwd)


class UnifiedCliTests(unittest.TestCase):
    def test_both_schemas_use_same_cli(self):
        with tempfile.TemporaryDirectory() as folder:
            for sample in ['examples/fairytale-sample.json', 'references/experience-sample.json', 'examples/guardian-academy.json', 'examples/photo-sample.json', 'examples/link-sample.json']:
                with self.subTest(sample=sample):
                    output = Path(folder) / 'index.html'
                    result = run(SKILL / 'scripts/build.py', '--input', SKILL / sample, '--output', output,
                                 *(['--source-image', SKILL / 'examples/synthetic-lakeside.png'] if sample.endswith('photo-sample.json') else []))
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertTrue(output.exists())
                    result = run(SKILL / 'scripts/check.py', SKILL / sample, output)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_nonfiction_requires_item_evidence(self):
        sample = json.loads((SKILL / 'references/experience-sample.json').read_text(encoding='utf-8'))
        sample['chapters'][0]['items'][0].pop('evidence_excerpt')
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.json'
            source.write_text(json.dumps(sample))
            result = run(SKILL / 'scripts/build.py', '--input', source, '--output', Path(folder) / 'index.html')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('evidence_excerpt', result.stderr)

    def test_fabricated_numeric_claim_fails(self):
        sample = json.loads((SKILL / 'references/experience-sample.json').read_text(encoding='utf-8'))
        sample['chapters'][0]['items'][0]['description'] += ' It had 999 visitors.'
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.json'
            source.write_text(json.dumps(sample))
            result = run(SKILL / 'scripts/build.py', '--input', source, '--output', Path(folder) / 'index.html')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('999', result.stderr)

    def test_optional_source_text_checks_quotes(self):
        sample = json.loads((SKILL / 'references/experience-sample.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as folder:
            src = Path(folder) / 'experience.json'
            src.write_text(json.dumps(sample))
            text = Path(folder) / 'private-source.txt'
            text.write_text('Nothing about space, museums, stars or engines.')
            result = run(SKILL / 'scripts/build.py', '--input', src,
                         '--source-text', text, '--output', Path(folder) / 'index.html')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('not found in locally supplied source text', result.stderr)
            text.write_text(' '.join(item['evidence_excerpt'] for chapter in sample['chapters'] for item in chapter['items']))
            result = run(SKILL / 'scripts/build.py', '--input', src,
                         '--source-text', text, '--output', Path(folder) / 'index.html')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ambiguous_schema_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'bad.json'
            source.write_text('{"source": {}, "experience": {}, "chapters": [], "profile": {}, "world": {}, "sections": []}')
            result = run(SKILL / 'scripts/build.py', '--input', source, '--output', Path(folder) / 'index.html')
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('exactly one schema', result.stderr)

    def test_portable_zip_uses_unified_cli_for_both_formats(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            archive = base / 'skill.zip'
            result = run(ROOT / 'scripts/package_skill.py', '--tag', 'v0.2.1', '--output', archive)
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(archive) as z:
                z.extractall(base)
            for sample in ['examples/fairytale-sample.json', 'references/experience-sample.json', 'examples/guardian-academy.json', 'examples/photo-sample.json', 'examples/link-sample.json']:
                with self.subTest(sample=sample):
                    output = base / 'index.html'
                    result = run(base / 'simplicity-builder/scripts/build.py', '--input',
                                 base / 'simplicity-builder' / sample, '--output', output,
                                 *(['--source-image', base / 'simplicity-builder/examples/synthetic-lakeside.png'] if sample.endswith('photo-sample.json') else []), cwd=base)
                    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                    result = run(base / 'simplicity-builder/scripts/check.py',
                                 base / 'simplicity-builder' / sample, output, cwd=base)
                    self.assertEqual(result.returncode, 0, result.stderr + result.stdout)


if __name__ == '__main__':
    unittest.main()
