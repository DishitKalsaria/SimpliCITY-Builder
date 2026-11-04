"""Ensure developers can reproduce the static checks used by GitHub Actions."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'ci_preflight.py'


class CiPreflightTests(unittest.TestCase):
    def test_github_workflow_uses_shared_lint_and_typecheck_commands(self):
        workflow = (ROOT / '.github/workflows/test.yml').read_text(encoding='utf-8')
        self.assertIn('run: python3 scripts/ci_preflight.py lint', workflow)
        self.assertIn('run: python3 scripts/ci_preflight.py types', workflow)

    def test_fingerprint_reports_exact_source_bytes(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'fingerprint'],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        for relative in ('simplicity-builder/scripts/scene_art.py',
                         'simplicity-builder/scripts/build_experience.py',
                         'simplicity-builder/scripts/build_portfolio.py'):
            digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            self.assertIn(f'SHA256 {digest}  {relative}', result.stdout)


class SourcePackageHygieneTests(unittest.TestCase):
    def test_release_source_excludes_local_quality_artifacts(self):
        sys.path.insert(0, str(ROOT / 'scripts'))
        import package_release
        with tempfile.TemporaryDirectory() as folder:
            temp = Path(folder)
            (temp / '.coverage').write_text('private run history', encoding='utf-8')
            (temp / 'normal.md').write_text('release source', encoding='utf-8')
            (temp / '.ruff_cache').mkdir()
            (temp / '.ruff_cache' / 'cache.db').write_bytes(b'data')
            (temp / 'private').mkdir()
            (temp / 'private' / 'source.txt').write_text('private text', encoding='utf-8')
            with patch.object(package_release, 'ROOT', temp):
                released = [relative for _, relative in package_release.files_to_package()]
            self.assertEqual(released, ['normal.md'])


if __name__ == '__main__':
    unittest.main()
