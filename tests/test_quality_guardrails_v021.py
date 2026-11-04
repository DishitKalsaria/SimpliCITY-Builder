"""Maintainability and deployment guardrails for the v0.2.1 release candidate.

These tests execute the ordinary Python entry points in process so their error
handling is visible to coverage; no network access or publication is performed.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / 'simplicity-builder' / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

import build as builder_cli
import check as checker_cli
from validate_experience import validate_experience


class CliGuardrails(unittest.TestCase):
    def test_generate_check_and_validate_experience_in_process(self):
        source = ROOT / 'simplicity-builder' / 'references' / 'experience-sample.json'
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'interactive.html'
            argv = ['build.py', '--input', str(source), '--output', str(output)]
            with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
                builder_cli.main()
            self.assertTrue(output.is_file())
            markup = output.read_text(encoding='utf-8')
            self.assertIn('scene-landmark', markup)
            with contextlib.redirect_stdout(io.StringIO()):
                checker_cli.check(source, output)
                validate_experience(source, output)
            with patch.object(sys, 'argv', ['check.py', str(source), str(output)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                checker_cli.main()

    def test_photo_build_fails_before_publishing_unobserved_scene(self):
        source = ROOT / 'simplicity-builder' / 'examples' / 'photo-sample.json'
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'should-not-exist.html'
            argv = ['build.py', '--input', str(source), '--output', str(output)]
            with patch.object(sys, 'argv', argv), contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as caught:
                    builder_cli.main()
            self.assertNotEqual(caught.exception.code, 0)
            self.assertIn('--source-image', stderr.getvalue())
            self.assertFalse(output.exists())

    def test_checker_rejects_unsupported_schema_and_does_not_swallow_error(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'input.json'
            source.write_text(json.dumps({'unrecognized': True}), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'exactly one schema'):
                checker_cli.check(source)
            with patch.object(sys, 'argv', ['check.py', str(source), 'missing.html']), \
                 contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as caught:
                    checker_cli.main()
            self.assertNotEqual(caught.exception.code, 0)
            self.assertIn('exactly one schema', stderr.getvalue())

    def test_review_sheet_cannot_overwrite_public_html(self):
        source = ROOT / 'simplicity-builder' / 'references' / 'experience-sample.json'
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'index.html'
            argv = ['build.py', '--input', str(source), '--output', str(output),
                    '--review-sheet', str(output)]
            with patch.object(sys, 'argv', argv), contextlib.redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit):
                    builder_cli.main()
            self.assertIn('distinct from public HTML', stderr.getvalue())
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
