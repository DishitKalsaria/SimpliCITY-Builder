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
        for name in ('fairytale', 'space', 'festival', 'clockwork', 'guardian', 'photo'):
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
                    "--input", str(ROOT / f"docs/demo-inputs/{fixture}-sample.json"),
                    "--output", str(generated)
                ], check=True, capture_output=True, text=True)
                self.assertEqual(generated.read_bytes(), (DOCS / f"{name}.html").read_bytes())

    def test_general_experience_demo_is_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'guardian.html'
            result = subprocess.run([
                sys.executable, str(ROOT / 'simplicity-builder/scripts/build_experience.py'),
                '--input', str(ROOT / 'simplicity-builder/examples/guardian-academy.json'),
                '--output', str(output),
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(output.read_bytes(), (DOCS / 'guardian.html').read_bytes())
            self.assertTrue((DOCS / 'assets/guardian-preview.webp').exists())
            self.assertIn('href="guardian.html"', (DOCS / 'index.html').read_text(encoding='utf-8'))

    def test_photo_demo_is_current_and_anchored_to_synthetic_image(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'photo.html'
            process = subprocess.run([
                sys.executable, str(ROOT / 'simplicity-builder/scripts/build.py'),
                '--input', str(ROOT / 'simplicity-builder/examples/photo-sample.json'),
                '--source-image', str(ROOT / 'simplicity-builder/examples/synthetic-lakeside.png'),
                '--output', str(output),
            ], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(output.read_bytes(), (DOCS / 'photo.html').read_bytes())
            self.assertTrue((DOCS / 'assets/photo-preview.webp').exists())
            self.assertIn('href="photo.html"', (DOCS / 'index.html').read_text(encoding='utf-8'))

    def test_readme_distinguishes_live_demo_from_json(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        self.assertIn('## See it in action', readme)
        for name in ('fairytale','space','festival','clockwork'):
            self.assertIn(f'{BASE}{name}.html', readme)
        self.assertIn('Fictional data', readme)
        self.assertIn('gallery-preview.webp', readme)

if __name__ == '__main__':
    unittest.main()
