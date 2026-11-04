"""Direct, offline checks for the SVG preflight and optional browser QA wrapper.

Browser interaction tests use a small mocked page because the 11-world Chromium
matrix runs separately in CI; these checks exercise Python error handling
without requiring a browser or modifying the public HTML.
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / 'simplicity-builder' / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))

import browser_smoke
import check_artwork

VALID_SCENE = '<svg viewBox="0 0 620 520"><circle cx="40" cy="40" r="20" fill="#aabbcc"/></svg>'


class ArtworkCliTests(unittest.TestCase):
    def test_accepted_original_artwork(self):
        with tempfile.TemporaryDirectory() as folder:
            svg = Path(folder) / 'scene.svg'
            svg.write_text(VALID_SCENE, encoding='utf-8')
            with patch.object(sys, 'argv', ['check_artwork.py', str(svg)]), \
                 contextlib.redirect_stdout(io.StringIO()) as printed:
                check_artwork.main()
            self.assertIn('PASS: SVG artwork accepted', printed.getvalue())

    def test_active_svg_event_handler_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            svg = Path(folder) / 'unsafe.svg'
            svg.write_text(VALID_SCENE.replace('<circle', '<circle onload="alert(1)"'), encoding='utf-8')
            with patch.object(sys, 'argv', ['check_artwork.py', str(svg)]), \
                 contextlib.redirect_stderr(io.StringIO()) as err:
                with self.assertRaises(SystemExit) as caught:
                    check_artwork.main()
            self.assertEqual(caught.exception.code, 1)
            self.assertIn('FAIL:', err.getvalue())
            self.assertIn('illustration-rules.md', err.getvalue())

    def test_missing_artwork_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            missing = Path(folder) / 'not-found.svg'
            with patch.object(sys, 'argv', ['check_artwork.py', str(missing)]), \
                 contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    check_artwork.main()
            self.assertEqual(caught.exception.code, 1)


class BrowserSmokeTests(unittest.TestCase):
    @staticmethod
    def page(*, counts=None, axe=None, variant='desktop', metrics=None):
        counts = counts or {}
        metrics = metrics or {'stageCoverage': 1, 'numberOfLandmarks': 1,
                              'missingPlaques': 0, 'clippedLandmarks': 0}
        page = MagicMock()

        def locator(selector):
            found = MagicMock()
            found.count.return_value = counts.get(selector, {
                '.scene-backdrop': 0,
                '#mobile-scene-template': 0,
                'button.landmark:visible': 0,
            }.get(selector, 1))
            found.first.get_attribute.return_value = 'Explore test object'
            found.get_attribute.return_value = variant
            found.first.is_visible.return_value = True
            found.is_visible.return_value = True
            found.inner_text.return_value = '2 of 2'
            return found

        page.locator.side_effect = locator

        def evaluate(script):
            if script == browser_smoke.METRICS_JS:
                return metrics
            if 'axe.run(' in script:
                return axe or []
            if 'document.activeElement?.id' in script:
                return 'landmark-test-object'
            return None

        page.evaluate.side_effect = evaluate
        return page

    def test_visual_metrics_are_measurement_based(self):
        page = self.page()
        metrics = browser_smoke.assert_visual(page, 'sample')
        self.assertEqual(metrics['numberOfLandmarks'], 1)
        self.assertEqual(page.evaluate.call_count, 2)  # Flush layout and inspect metrics.

    def test_geometry_and_missing_landmarks_fail_closed(self):
        for bad_metrics, message in (
            ({'stageCoverage': 0.90, 'numberOfLandmarks': 1}, 'stageCoverage'),
            ({'stageCoverage': 1, 'numberOfLandmarks': 0}, 'numberOfLandmarks'),
            ({'stageCoverage': 1, 'numberOfLandmarks': 1, 'clippedLandmarks': 2}, 'clippedLandmarks'),
            ({'stageCoverage': 1, 'numberOfLandmarks': 1, 'poorContrast': 1}, 'poorContrast'),
        ):
            with self.subTest(issue=message), self.assertRaisesRegex(AssertionError, message):
                browser_smoke.assert_visual(self.page(metrics=bad_metrics), 'bad')

    def test_all_viewports_execute_keyboard_tour_and_optional_axe_check(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'fixture.html'
            source.write_text('<!doctype html><title>offline fixture</title>', encoding='utf-8')
            browser = MagicMock()
            browser.new_page.side_effect = [self.page() for _ in browser_smoke.VIEWPORTS]
            axe_path = Path(folder) / 'axe.min.js'
            axe_path.write_text('// fixture; evaluated in the simulated page', encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()) as output:
                browser_smoke.check(source, browser, screenshots=Path(folder) / 'captures', axe_script=axe_path)
            self.assertEqual(browser.new_page.call_count, 5)
            self.assertEqual(output.getvalue().count('PASS fixture.html'), 5)
            for page in (call for call in browser.new_page.side_effect):
                self.assertEqual(page.close.call_count, 1)
                self.assertEqual(page.add_script_tag.call_count, 1)
                self.assertEqual(page.screenshot.call_count, 1)

    def test_mismatched_landmarks_and_keyboard_order_are_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'fixture.html'
            source.write_text('example', encoding='utf-8')
            for counts, expected in (
                ({'button.landmark': 2}, 'landmark/list mismatch'),
                ({'.scene-landmark[tabindex="0"]': 0}, 'missing keyboard Tab stops'),
            ):
                with self.subTest(expected=expected):
                    browser = MagicMock()
                    browser.new_page.return_value = self.page(counts=counts)
                    with self.assertRaisesRegex(AssertionError, expected):
                        browser_smoke.check(source, browser)

    def test_accessibility_violations_fail_and_variant_must_match(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'fixture.html'
            source.write_text('example', encoding='utf-8')
            browser = MagicMock()
            browser.new_page.return_value = self.page(axe=['color-contrast'])
            with self.assertRaisesRegex(AssertionError, 'axe violations'):
                browser_smoke.check(source, browser, axe_script=Path(folder) / 'axe.js')
            browser.new_page.return_value = self.page(
                counts={'#mobile-scene-template': 1}, variant='wrong')
            with self.assertRaisesRegex(AssertionError, 'wrong active scene'):
                browser_smoke.check(source, browser)

    def test_chromium_fallback_and_absence(self):
        runner = MagicMock()
        runner.chromium.launch.side_effect = [RuntimeError('bundled browser missing'), MagicMock()]
        with patch.object(browser_smoke.shutil, 'which', return_value='/usr/bin/chromium'):
            browser_smoke.launch(runner)
        self.assertEqual(runner.chromium.launch.call_count, 2)
        self.assertEqual(runner.chromium.launch.call_args.kwargs['executable_path'], '/usr/bin/chromium')
        runner.chromium.launch.side_effect = RuntimeError('missing')
        with patch.object(browser_smoke.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'No Chromium available'):
                browser_smoke.launch(runner)

    def test_cli_requires_axe_file_before_launching(self):
        with patch.object(sys, 'argv', ['browser_smoke.py', 'demo.html', '--axe-script', 'absent.js']), \
             contextlib.redirect_stderr(io.StringIO()) as stderr:
            with self.assertRaises(SystemExit) as caught:
                browser_smoke.main()
        self.assertEqual(caught.exception.code, 2)
        self.assertIn('supplied --axe-script missing', stderr.getvalue())

    def test_cli_routes_pages_and_closes_browser(self):
        fake_browser = MagicMock()
        fake_playwright = MagicMock()
        with patch.object(sys, 'argv', ['browser_smoke.py', 'a.html', 'b.html']), \
             patch('playwright.sync_api.sync_playwright') as start, \
             patch.object(browser_smoke, 'launch', return_value=fake_browser), \
             patch.object(browser_smoke, 'check') as check:
            start.return_value.__enter__.return_value = fake_playwright
            browser_smoke.main()
        self.assertEqual(check.call_count, 2)
        self.assertEqual([call.args[0].name for call in check.call_args_list], ['a.html', 'b.html'])
        fake_browser.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
