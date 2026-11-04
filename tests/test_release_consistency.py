"""Release/documentation consistency and portable skill isolation."""
from __future__ import annotations

import ast
import io
import re
import tokenize
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
                self.assertIn('v0.2.1', (ROOT / name).read_text(encoding='utf-8'))

        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        version = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', text, re.M).group(1)
        self.assertEqual(version, '0.2.1')
        self.assertIn(f'# SimpliCITY Builder v{version}', text)
        changelog = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
        current = re.search(r'^## v([0-9.]+)', changelog, re.M)
        self.assertIsNotNone(current)
        self.assertEqual(current.group(1), version)
        self.assertEqual(
            len(re.findall(r'^## v0\.2\.1\b', changelog, re.M)),
            1,
            'Document the active release under one version heading, with subheadings as needed',
        )
        release = (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8')
        self.assertIn('workflow_dispatch:', release)
        self.assertIn('python3 -m pip install -r requirements-dev.txt', release)
        self.assertIn('--tag "$RELEASE_TAG"', release)
        self.assertIn('ref: ${{ inputs.release_tag || github.ref_name }}', release)

    def test_contributor_and_browser_docs_match_supported_release(self):
        contributing = (ROOT / 'CONTRIBUTING.md').read_text(encoding='utf-8')
        self.assertIn('For v0.2.1', contributing)
        self.assertNotIn('For v0.2.0', contributing)
        testing = (ROOT / 'docs/maintainers/TESTING.md').read_text(encoding='utf-8')
        self.assertIn('11 demos', testing)
        self.assertIn('eight', testing.lower())  # Exactly eight visual baselines, not eleven.
        workflow = (ROOT / '.github/workflows/test.yml').read_text(encoding='utf-8')
        for world in ('meeting-room', 'playground', 'farm'):
            self.assertIn(f'docs/{world}.html', workflow)
        self.assertIn('scripts/check_environment_matrix.py', workflow)
        preflight = (ROOT / 'scripts/ci_preflight.py').read_text(encoding='utf-8')
        self.assertIn("'simplicity-builder/scripts/build_portfolio.py'", preflight)
        visual_execution = (ROOT / 'docs/maintainers/V021_VISUAL_EXECUTION.md').read_text(encoding='utf-8')
        self.assertIn('all 11 browser HTML worlds', visual_execution)
        self.assertNotIn('all eight browser HTML worlds', visual_execution)
        golden_notes = (ROOT / 'tests/visual-golden/README.md').read_text(encoding='utf-8')
        self.assertIn('all 11 gallery worlds', golden_notes)
        self.assertIn('eight original gallery worlds', golden_notes)
        self.assertNotIn('all eight gallery worlds', golden_notes)
        config = (ROOT / 'pyproject.toml').read_text(encoding='utf-8')
        self.assertIn('python_version = "3.11"', config)
        self.assertNotIn('python_version = "3.9"', config)
        self.assertIn("python-version: '3.11'", workflow)

    def test_scene_lint_regression_and_python39_syntax(self):
        scene = ROOT / 'simplicity-builder/scripts/scene_art.py'
        tokens = tokenize.tokenize(io.BytesIO(scene.read_bytes()).readline)
        self.assertFalse(
            [(item.start[0], item.string) for item in tokens
             if item.type == tokenize.OP and item.string == ';'],
            'Do not reintroduce multiple statements per line in scene_art.py',
        )
        for source in (ROOT / 'simplicity-builder/scripts').glob('*.py'):
            with self.subTest(file=source.name):
                ast.parse(source.read_text(encoding='utf-8'), feature_version=(3, 9))

    def test_no_inline_control_flow_or_semicolons_in_python_sources(self):
        # Prevent reintroducing the condensed statements that obscured
        # branching/exception behavior in CI, validation and browser tools.
        compound = (ast.If, ast.For, ast.While, ast.With, ast.Try,
                    ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef,
                    ast.AsyncFor, ast.AsyncWith)
        for source in ROOT.rglob('*.py'):
            if any(p in source.parts for p in ('private', '__pycache__')):
                continue
            with self.subTest(file=str(source.relative_to(ROOT))):
                raw = source.read_bytes()
                tokens = tokenize.tokenize(io.BytesIO(raw).readline)
                self.assertFalse([(tok.start[0], tok.string) for tok in tokens
                                  if tok.type == tokenize.OP and tok.string == ';'])
                tree = ast.parse(raw, filename=str(source))
                self.assertFalse([(type(node).__name__, node.lineno) for node in ast.walk(tree)
                                  if isinstance(node, compound) and node.body
                                  and node.body[0].lineno == node.lineno])

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
