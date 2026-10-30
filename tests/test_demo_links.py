import unittest
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'https://dishitkalsaria.github.io/SimpliCITY-Builder/'

class DemoLinksTests(unittest.TestCase):
    def test_gallery_points_to_generated_websites(self):
        gallery = (DOCS / 'index.html').read_text(encoding='utf-8')
        for name in ('fairytale', 'space', 'festival', 'clockwork'):
            with self.subTest(name=name):
                self.assertIn(f'href="{name}.html"', gallery)
                self.assertIn(f'src="assets/{name}-preview.webp"', gallery)
                page = (DOCS / f'{name}.html').read_text(encoding='utf-8')
                self.assertIn('<!doctype html>', page)
                self.assertIn('class="landmark"', page)
                self.assertIn('dialog.showModal()', page)
                self.assertTrue((DOCS / 'assets' / f'{name}-preview.webp').is_file())

    def test_committed_demo_outputs_are_current(self):
        for fixture, name in (("fairytale", "fairytale"), ("space", "space"),
                              ("custom", "festival"), ("clockwork", "clockwork")):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                generated = Path(tmp) / f"{name}.html"
                subprocess.run([
                    sys.executable, str(ROOT / "simplicity-builder/scripts/build_portfolio.py"),
                    "--input", str(ROOT / f"examples/{fixture}-sample.json"),
                    "--output", str(generated)
                ], check=True, capture_output=True, text=True)
                self.assertEqual(generated.read_bytes(), (DOCS / f"{name}.html").read_bytes())

    def test_readme_distinguishes_live_demo_from_json(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('## See what it builds', readme)
        for name in ('fairytale','space','festival','clockwork'):
            self.assertIn(f'{BASE}{name}.html', readme)
        self.assertIn('Generator input (for developers)', readme)
        self.assertIn('gallery-preview.webp', readme)

if __name__ == '__main__':
    unittest.main()
