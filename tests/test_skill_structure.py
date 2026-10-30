import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'simplicity-builder' / 'SKILL.md'

class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter_and_name(self):
        text = SKILL.read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        front = text.split('---', 2)[1]
        fields = dict(re.findall(r'^(name|description|license|compatibility):\s*(.+)$', front, re.M))
        self.assertEqual(fields['name'], SKILL.parent.name)
        self.assertRegex(fields['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertLessEqual(len(fields['name']), 64)
        self.assertLessEqual(len(fields['description']), 1024)
        self.assertIn('license', fields)
        self.assertTrue((ROOT / 'LICENSE').exists())

    def test_skill_package_files(self):
        for path in ['SKILL.md','assets/template.html','scripts/build_portfolio.py','scripts/validate.py',
                     'references/portfolio-schema.md','references/illustration-rules.md','references/world-rules.md']:
            self.assertTrue((SKILL.parent / path).is_file(), path)

if __name__ == '__main__':
    unittest.main()
