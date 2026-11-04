"""Mocked deployment failure modes; the tests never call git, gh or the network."""
from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'simplicity-builder' / 'scripts'))

import publish_portfolio as publish
from build_portfolio import generate

PNG = bytes.fromhex('89504e470d0a1a0a') + b'x' * 32


class PublishSafetyGuardrails(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        data = json.loads((ROOT / 'examples' / 'space-sample.json').read_text(encoding='utf-8'))
        source = self.folder / 'source.html'
        source.write_text(generate(data), encoding='utf-8')
        preview = self.folder / 'preview.png'
        preview.write_bytes(PNG)
        self.bundle = self.folder / 'bundle'
        self.url = publish.prepare(source, 'DemoUser', 'my-world', self.bundle, preview)

    def test_approval_is_required_even_for_valid_prepared_site(self):
        with patch.object(publish, 'run_command') as shell:
            with self.assertRaisesRegex(ValueError, '--approve-public'):
                publish.deploy(self.bundle, 'DemoUser', 'my-world', False)
            shell.assert_not_called()

    def test_mismatched_account_or_repository_metadata_is_rejected_before_gh(self):
        with patch.object(publish, 'run_command') as shell:
            with self.assertRaisesRegex(ValueError, 'metadata URL'):
                publish.deploy(self.bundle, 'DifferentUser', 'my-world', True)
            shell.assert_not_called()

    def test_no_preview_or_review_checklist_is_rejected(self):
        site = self.bundle / 'site'
        (site / 'social-preview.png').unlink()
        with self.assertRaisesRegex(ValueError, 'Social preview'):
            publish.deploy(self.bundle, 'DemoUser', 'my-world', True)
        (self.bundle / 'PUBLISH_CHECKLIST.md').unlink()
        with self.assertRaisesRegex(ValueError, 'review checklist'):
            publish.deploy(self.bundle, 'DemoUser', 'my-world', True)

    def test_existing_git_directory_is_rejected(self):
        (self.bundle / 'site' / '.git').mkdir()
        with self.assertRaisesRegex(ValueError, 'already contains git history'):
            publish.deploy(self.bundle, 'DemoUser', 'my-world', True)

    def test_missing_git_or_gh_never_triggers_publish(self):
        with patch.object(publish.shutil, 'which', return_value=None), \
             patch.object(publish, 'run_command') as shell:
            with self.assertRaisesRegex(RuntimeError, 'Git and the GitHub CLI'):
                publish.deploy(self.bundle, 'DemoUser', 'my-world', True)
            shell.assert_not_called()

    def test_wrong_authenticated_account_is_rejected(self):
        with patch.object(publish.shutil, 'which', return_value='/bin/cli'), \
             patch.object(publish, 'run_command', return_value=Mock(stdout='SomeoneElse\n')) as shell:
            with self.assertRaisesRegex(ValueError, 'does not match'):
                publish.deploy(self.bundle, 'DemoUser', 'my-world', True)
            self.assertEqual(shell.call_count, 1)

    def test_existing_repository_is_not_modified(self):
        with patch.object(publish.shutil, 'which', return_value='/bin/cli'), \
             patch.object(publish, 'run_command', return_value=Mock(stdout='DemoUser\n')) as shell, \
             patch.object(publish.subprocess, 'run', return_value=Mock(returncode=0)):
            with self.assertRaisesRegex(ValueError, 'already exists'):
                publish.deploy(self.bundle, 'DemoUser', 'my-world', True)
            self.assertEqual(shell.call_count, 1)

    def test_new_repository_commands_include_only_reviewed_site_contents(self):
        calls = []
        def fake_run(command, cwd=None, capture=False):
            calls.append((command, cwd, capture))
            if command[:3] == ['gh', 'api', 'user']:
                return Mock(stdout='DemoUser\n')
            return Mock(stdout='')

        with patch.object(publish.shutil, 'which', return_value='/bin/cli'), \
             patch.object(publish, 'run_command', side_effect=fake_run), \
             patch.object(publish.subprocess, 'run', return_value=Mock(returncode=1)):
            self.assertEqual(publish.deploy(self.bundle, 'DemoUser', 'my-world', True), self.url)
        actions = [command for command, _, _ in calls]
        self.assertEqual(actions[1][:2], ['git', 'init'])
        self.assertEqual(actions[2], ['git', 'add', 'index.html', '.nojekyll', 'social-preview.png'])
        self.assertIn(['gh', 'repo', 'create', 'DemoUser/my-world', '--public',
                       '--source', '.', '--remote', 'origin', '--push'], actions)
        self.assertTrue(all(cwd == self.bundle / 'site' for _, cwd, _ in calls[1:]))

    def test_pages_setup_error_is_reported_not_falsely_claimed_success(self):
        def fake_run(command, cwd=None, capture=False):
            if command[:3] == ['gh', 'api', 'user']:
                return Mock(stdout='DemoUser\n')
            if command[:4] == ['gh', 'api', '-X', 'POST']:
                raise subprocess.CalledProcessError(1, command)
            return Mock(stdout='')
        with patch.object(publish.shutil, 'which', return_value='/bin/cli'), \
             patch.object(publish, 'run_command', side_effect=fake_run), \
             patch.object(publish.subprocess, 'run', return_value=Mock(returncode=1)), \
             contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(publish.deploy(self.bundle, 'DemoUser', 'my-world', True), self.url)
        self.assertIn('Pages API setup was not confirmed', stderr.getvalue())

    def test_failed_prepare_does_not_leave_half_public_bundle(self):
        invalid = self.folder / 'broken.html'
        invalid.write_text('<html>not generated</html>', encoding='utf-8')
        other_bundle = self.folder / 'broken-bundle'
        with self.assertRaisesRegex(ValueError, 'complete generated HTML'):
            publish.prepare(invalid, 'DemoUser', 'other-world', other_bundle,
                            self.folder / 'preview.png')
        self.assertFalse(other_bundle.exists())


if __name__ == '__main__':
    unittest.main()

class PublishPreparationGuardrails(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source_data = json.loads((ROOT / 'examples' / 'space-sample.json').read_text(encoding='utf-8'))
        self.source = self.root / 'source.html'
        self.source.write_text(generate(source_data), encoding='utf-8')
        self.image = self.root / 'preview.png'
        self.image.write_bytes(PNG)

    def test_missing_source_is_rejected_without_creating_bundle(self):
        bundle = self.root / 'bundle'
        with self.assertRaisesRegex(ValueError, 'not found'):
            publish.prepare(self.root / 'missing.html', 'DemoUser', 'my-world', bundle, self.image)
        self.assertFalse(bundle.exists())

    def test_preview_must_be_real_raster_format_and_under_size_limit(self):
        bundle = self.root / 'bundle'
        self.image.write_bytes(b'<svg onload="evil()"/>')
        with self.assertRaisesRegex(ValueError, 'JPEG, PNG or WebP'):
            publish.prepare(self.source, 'DemoUser', 'my-world', bundle, self.image)
        self.assertFalse(bundle.exists())
        self.image.write_bytes(PNG + b'x' * 5_000_001)
        with self.assertRaisesRegex(ValueError, '5 MB'):
            publish.prepare(self.source, 'DemoUser', 'my-world', bundle, self.image)
        self.assertFalse(bundle.exists())

    def test_preview_generated_locally_without_network_when_not_supplied(self):
        bundle = self.root / 'bundle'
        def mocked_capture(_html, output):
            output.write_bytes(b'\xff\xd8\xff' + b'fake-image')
        with patch.object(publish, 'capture_preview', side_effect=mocked_capture) as capture:
            publish.prepare(self.source, 'DemoUser', 'my-world', bundle)
        capture.assert_called_once()
        self.assertTrue((bundle / 'site' / 'social-preview.jpg').is_file())

    def test_social_metadata_rejects_invalid_html_and_null_bytes(self):
        source = self.source.read_text(encoding='utf-8')
        self.assertRaisesRegex(ValueError, 'Invalid HTML', publish.rewrite_social,
                               source + '\x00', 'https://example.org/', 'https://example.org/a.png', 'alt')
        self.assertRaisesRegex(ValueError, 'complete generated HTML', publish.rewrite_social,
                               source.replace('<!doctype html>', 'not-a-doctype', 1),
                               'https://example.org/', 'https://example.org/a.png', 'alt')
        self.assertRaisesRegex(ValueError, 'Required Open Graph', publish.rewrite_social,
                               source.replace('property="og:title"', 'property="not-og-title"'),
                               'https://example.org/', 'https://example.org/a.png', 'alt')

    def test_cli_prepare_and_rejected_deploy_share_central_guardrails(self):
        bundle = self.root / 'bundle'
        prepare_argv = ['publish_portfolio.py', 'prepare', '--html', str(self.source),
                        '--account', 'DemoUser', '--repo', 'my-world', '--out', str(bundle),
                        '--preview', str(self.image)]
        with patch.object(sys, 'argv', prepare_argv), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(publish.main(), 0)
        self.assertIn('No upload occurred', output.getvalue())
        deploy_argv = ['publish_portfolio.py', 'deploy', '--bundle', str(bundle),
                       '--account', 'DemoUser', '--repo', 'my-world']
        with patch.object(sys, 'argv', deploy_argv), contextlib.redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as caught:
                publish.main()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn('--approve-public', stderr.getvalue())

    def test_prepare_cli_rejects_invalid_account(self):
        bundle = self.root / 'bundle'
        args = ['publish_portfolio.py', 'prepare', '--html', str(self.source),
                '--account', 'Bad/Account', '--repo', 'my-world', '--out', str(bundle),
                '--preview', str(self.image)]
        with patch.object(sys, 'argv', args), contextlib.redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as caught:
                publish.main()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn('Invalid GitHub account', stderr.getvalue())
        self.assertFalse(bundle.exists())
