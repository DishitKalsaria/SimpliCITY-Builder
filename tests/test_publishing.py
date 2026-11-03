"""GitHub Pages bundle + social metadata regression checks (no network calls)."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder' / 'scripts'))
from build_portfolio import generate
from publish_portfolio import deploy, image_kind, page_url, prepare, rewrite_social

PNG = bytes.fromhex('89504e470d0a1a0a') + b'x' * 32


class PublishingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads((ROOT / 'examples' / 'space-sample.json').read_text(encoding='utf-8'))
        cls.html = generate(data)

    def test_github_pages_url(self):
        self.assertEqual(page_url('DemoUser', 'my-world'), 'https://DemoUser.github.io/my-world/')
        self.assertEqual(page_url('DemoUser', 'DemoUser.github.io'), 'https://DemoUser.github.io/')
        for user, repo in [('bad/user', 'site'), ('valid', '../oops'), ('evil&', 'site')]:
            with self.assertRaises(ValueError):
                page_url(user, repo)

    def test_replace_social_metadata_without_duplicates(self):
        initial = rewrite_social(self.html, 'https://DemoUser.github.io/my-world/',
                                 'https://DemoUser.github.io/my-world/social-preview.jpg', 'My world')
        again = rewrite_social(initial, 'https://DemoUser.github.io/my-world/',
                               'https://DemoUser.github.io/my-world/social-preview.jpg', 'My world')
        self.assertEqual(again.count('property="og:image"'), 1)
        self.assertEqual(again.count('property="og:url"'), 1)
        self.assertEqual(again.count('name="twitter:card"'), 1)
        self.assertIn('social-preview.jpg', again)
        self.assertIn('property="og:image:alt" content="My world"', again)
        self.assertNotIn('property="og:image:width"', again)  # optional source image may have different dimensions
        self.assertIn('class="scene-landmark', again)

    def test_prepare_is_offline_and_copies_only_public_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / 'generated.html'
            source.write_text(self.html, encoding='utf-8')
            original = folder / 'private-resume.txt'
            original.write_text('Sensitive private résumé text', encoding='utf-8')
            image = folder / 'preview.png'
            image.write_bytes(PNG)
            bundle = folder / 'bundle'
            url = prepare(source, 'DemoUser', 'my-world', bundle, image)
            self.assertEqual(url, 'https://DemoUser.github.io/my-world/')
            site = bundle / 'site'
            self.assertEqual(sorted(p.name for p in site.iterdir()), ['.nojekyll','index.html','social-preview.png'])
            self.assertNotIn('Sensitive private', (site / 'index.html').read_text(encoding='utf-8'))
            self.assertTrue((bundle / 'LINKEDIN_POST.txt').exists())
            self.assertTrue((bundle / 'PUBLISH_CHECKLIST.md').exists())
            self.assertIn('social-preview.png', (site / 'index.html').read_text(encoding='utf-8'))
            self.assertIn(url, (bundle / 'LINKEDIN_POST.txt').read_text(encoding='utf-8'))
            with self.assertRaisesRegex(ValueError, 'overwrite'):
                prepare(source, 'DemoUser', 'my-world', bundle, image)

    def test_publish_never_runs_without_owner_approval(self):
        with self.assertRaisesRegex(ValueError, '--approve-public'):
            deploy(Path('/nonexistent'), 'DemoUser', 'my-world', False)

    def test_image_type_checks(self):
        self.assertEqual(image_kind(PNG), 'png')
        with self.assertRaises(ValueError):
            image_kind(b'<svg onload=bad()></svg>')
        with self.assertRaises(ValueError):
            rewrite_social('<html><head></head></html>', 'https://example.com/', 'https://example.com/i.jpg', 'alt')


if __name__ == '__main__':
    unittest.main()
