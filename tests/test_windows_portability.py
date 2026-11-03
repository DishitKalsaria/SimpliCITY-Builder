"""Generated HTML must be byte-identical across Windows and Unix hosts."""
from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder'


class WindowsPortabilityTests(unittest.TestCase):
    def test_tests_read_text_with_explicit_encoding(self):
        """Test fixtures and generated HTML must not depend on Windows cp1252."""
        for test_file in sorted((ROOT / 'tests').glob('test_*.py')):
            with self.subTest(file=test_file.name):
                tree = ast.parse(test_file.read_text(encoding='utf-8'))
                for call in ast.walk(tree):
                    if (isinstance(call, ast.Call) and
                            isinstance(call.func, ast.Attribute) and
                            call.func.attr == 'read_text'):
                        self.assertTrue(
                            any(keyword.arg == 'encoding' for keyword in call.keywords),
                            f'{test_file.name}:{call.lineno} must specify encoding for read_text()',
                        )

    def test_all_html_build_commands_preserve_lf(self):
        commands = (
            ('build_portfolio.py', ROOT / 'docs/demo-inputs/fairytale-sample.json'),
            ('build_experience.py', SKILL / 'examples/guardian-academy.json'),
            ('build.py', SKILL / 'examples/guardian-academy.json'),
        )
        with tempfile.TemporaryDirectory() as td:
            for script, source in commands:
                with self.subTest(command=script):
                    target = Path(td) / (script + '.html')
                    result = subprocess.run([
                        sys.executable, str(SKILL / 'scripts' / script),
                        '--input', str(source), '--output', str(target),
                    ], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    output = target.read_bytes()
                    self.assertTrue(output.startswith(b'<!doctype html>'))
                    self.assertIn(b'\n', output)
                    self.assertNotIn(b'\r\n', output)


if __name__ == '__main__':
    unittest.main()
