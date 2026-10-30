import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'simplicity-builder' / 'scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

builder = load('build_portfolio')
resume = load('extract_resume')


class SvgContractTests(unittest.TestCase):
    def test_gradients_transforms_and_caps(self):
        scene = '''<svg viewBox="0 0 620 520"><defs>
          <radialGradient id="halo" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#abcdef" stop-opacity=".8"/>
            <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
          </radialGradient>
          <linearGradient id="sky"><stop offset="0" stop-color="#aabbcc"/>
            <stop offset="1" stop-color="#112233"/></linearGradient>
          </defs><g transform="translate(10 12)" stroke-linecap="round">
          <ellipse cx="310" cy="260" rx="180" ry="35" transform="rotate(-25 310 260)"
             stroke="url(#sky)" fill="none" stroke-width="7" stroke-linecap="round"/>
          <circle cx="310" cy="250" r="110" fill="url(#halo)"/>
          </g></svg>'''
        result = builder.sanitize_scene(scene)
        self.assertIn('<radialGradient', result)
        self.assertIn('fill="url(#halo)"', result)
        self.assertIn('transform="rotate(-25 310 260)"', result)
        self.assertIn('stroke-linecap="round"', result)

    def test_documentation_svg_example_is_executable(self):
        rules = (ROOT / 'simplicity-builder' / 'references' / 'illustration-rules.md').read_text(encoding='utf-8')
        sample = rules.split('```xml\n', 1)[1].split('\n```', 1)[0]
        result = builder.sanitize_scene(sample)
        self.assertIn('url(#planetGlow)', result)
        self.assertIn('transform="rotate(', result)

    def test_svg_default_namespace_is_accepted(self):
        scene = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 520"><circle cx="40" cy="40" r="20" fill="#aabbcc"/></svg>'
        self.assertIn('<circle', builder.sanitize_scene(scene))

    def test_rejects_malicious_or_invalid_svg(self):
        malicious = [
            '<svg viewBox="0 0 620 520"><defs><linearGradient id="g"><stop offset="0" stop-color="#fff"/></linearGradient></defs><rect width="10" height="10" fill="url(https://evil.test/a)"/></svg>',
            '<svg viewBox="0 0 620 520"><rect width="10" height="10" fill="url(#missing)"/></svg>',
            '<svg viewBox="0 0 620 520"><script>alert(1)</script></svg>',
            '<svg viewBox="0 0 620 520"><circle r="5" fill="#fff" onload="alert(1)"/></svg>',
            '<svg viewBox="0 0 620 520"><filter id="bad"/></svg>',
            '<svg viewBox="0 0 620 520"><defs><linearGradient id="x"><stop offset="1.5" stop-color="#fff"/></linearGradient></defs></svg>',
            '<svg viewBox="0 0 620 520"><defs><linearGradient id="x"><stop offset="0" stop-color="#fff"/></linearGradient><linearGradient id="x"/></defs></svg>',
            '<svg viewBox="0 0 620 520"><path d="M0 0" stroke="#fff" stroke-linecap="miter"/></svg>',
        ]
        for text in malicious:
            with self.subTest(text=text), self.assertRaises(ValueError):
                builder.sanitize_scene(text)


class ResumeExtractTests(unittest.TestCase):
    def test_extract_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'resume.txt'
            f.write_text('Casey Example\nProfessional Experience\nResearch analyst at Example Company from 2022 to 2025.', encoding='utf-8')
            self.assertIn('Example Company', resume.extract_text(f))

    def test_extract_docx(self):
        xml = '''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Jamie Example - Data Scientist</w:t></w:r></w:p><w:p><w:r><w:t>Built evidence-driven projects from 2020 through 2026.</w:t></w:r></w:p></w:body></w:document>'''
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'resume.docx'
            with zipfile.ZipFile(f, 'w') as z:
                z.writestr('word/document.xml', xml)
            self.assertIn('Built evidence-driven projects', resume.extract_text(f))

    def test_short_or_scanned_resume_fails_helpfully(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / 'resume.txt'
            f.write_text('Almost empty', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Too little selectable text'):
                resume.extract_text(f)


if __name__ == '__main__':
    unittest.main()
