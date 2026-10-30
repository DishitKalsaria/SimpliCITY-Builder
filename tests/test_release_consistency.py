"""Keep release docs/paths consistent with the current skill package."""
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class ReleaseConsistencyTests(unittest.TestCase):
    def test_current_version_across_active_docs_and_ci(self):
        for name in ('README.md','INSTALL.md','AI_START_HERE.md','RELEASING.md',
                     'TESTING.md','COMPATIBILITY.md','RELEASE_ACCEPTANCE.md',
                     'docs/LINK_ONLY.md','simplicity-builder/SKILL.md',
                     '.github/workflows/test.yml'):
            with self.subTest(file=name):
                content=(ROOT/name).read_text(encoding='utf-8')
                self.assertIn('v0.1.5',content)
                self.assertNotIn('v0.1.4',content)
        self.assertIn('version: "0.1.5"',(ROOT/'simplicity-builder/SKILL.md').read_text())

    def test_all_markdown_local_links_exist(self):
        for file in ROOT.rglob('*.md'):
            if any(x in file.parts for x in ('private','.git','__pycache__')):
                continue
            content=file.read_text(encoding='utf-8')
            for match in re.finditer(r'(?<!!)\[[^\]\n]+\]\(([^)]+)\)',content):
                target=match.group(1).split('#')[0].strip()
                if not target or target.startswith(('https://','http://','mailto:')):
                    continue
                with self.subTest(file=str(file),target=target):
                    self.assertTrue((file.parent/target).exists())

    def test_no_obsolete_release_content(self):
        for name in ('PUBLISHING_IDEA.md','V014_ACCEPTANCE.md','tests/test_v014.py'):
            self.assertFalse((ROOT/name).exists())
        for name in ('README.md','AI_START_HERE.md','INSTALL.md'):
            text=(ROOT/name).read_text()
            self.assertNotIn('PUBLISHING_IDEA.md',text)
        self.assertTrue((ROOT/'simplicity-builder/scripts/publish_portfolio.py').exists())
        self.assertTrue((ROOT/'simplicity-builder/references/publishing.md').exists())

if __name__=='__main__': unittest.main()
