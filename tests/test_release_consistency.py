"""Release/documentation consistency and portable skill isolation."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder'


class ReleaseConsistencyTests(unittest.TestCase):
    def test_current_version_across_active_docs_and_ci(self):
        for name in ('README.md', 'INSTALL.md', 'AI_START_HERE.md', 'docs/maintainers/RELEASING.md',
                     'docs/maintainers/TESTING.md', 'COMPATIBILITY.md', 'docs/maintainers/RELEASE_ACCEPTANCE.md',
                     'docs/LINK_ONLY.md', 'simplicity-builder/SKILL.md',
                     '.github/workflows/test.yml'):
            with self.subTest(file=name):
                self.assertIn('v0.2.0', (ROOT / name).read_text(encoding='utf-8'))

        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        version = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', text, re.M).group(1)
        self.assertEqual(version, '0.2.0')
        self.assertIn(f'# SimpliCITY Builder v{version}', text)
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        current = re.search(r'^## v([0-9.]+)', changelog, re.M)
        self.assertIsNotNone(current)
        self.assertEqual(current.group(1), version)
        self.assertIn('--tag "$GITHUB_REF_NAME"', (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8'))

    def test_all_markdown_local_links_exist(self):
        for file in ROOT.rglob('*.md'):
            if any(x in file.parts for x in ('private', '.git', '__pycache__')):
                continue
            text = file.read_text(encoding='utf-8')
            for match in re.finditer(r'(?<!!)\[[^\]\n]+\]\(([^)]+)\)', text):
                target = match.group(1).split('#')[0].strip()
                if not target or target.startswith(('https://', 'http://', 'mailto:')):
                    continue
                with self.subTest(file=str(file), target=target):
                    self.assertTrue((file.parent / target).exists())

    def test_skill_paths_do_not_escape_installed_folder(self):
        for file in SKILL.rglob('*'):
            if not file.is_file():
                continue
            with self.subTest(file=str(file)):
                self.assertFalse(file.is_symlink())
                self.assertTrue(file.resolve().is_relative_to(SKILL.resolve()))
                if file.suffix == '.md':
                    text = file.read_text(encoding='utf-8')
                    self.assertNotIn('../', text, 'Installed skill must not refer to repo-root paths')
                    self.assertNotIn('from repo root', text)

    def test_no_obsolete_release_content(self):
        for name in ('PUBLISHING_IDEA.md', 'V014_ACCEPTANCE.md', 'tests/test_v014.py', 'scripts/browser_smoke.py'):
            self.assertFalse((ROOT / name).exists())
        self.assertTrue((SKILL / 'scripts/browser_smoke.py').exists())
        self.assertTrue((SKILL / 'scripts/build_experience.py').exists())
        self.assertTrue((SKILL / 'scripts/validate_experience.py').exists())
        self.assertTrue((SKILL / 'scripts/build.py').exists())
        self.assertTrue((SKILL / 'scripts/check.py').exists())
        self.assertNotIn('Power Rangers', (SKILL / 'SKILL.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
