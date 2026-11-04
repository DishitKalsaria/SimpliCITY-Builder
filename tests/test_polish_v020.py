"""Privacy, photo semantics and negative Chromium regressions for v0.2.0."""
from __future__ import annotations

import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'simplicity-builder/scripts'
sys.path.insert(0,str(SCRIPTS))
from build_experience import to_portfolio
from photo_privacy import jpeg_clean,png_clean,webp_clean,clean_image
from build_portfolio import embedded_image, generate
from review_sheet import make_review_sheet
from browser_smoke import assert_visual, launch


def chunk(tag:bytes,payload:bytes)->bytes:
    return struct.pack('>I',len(payload))+tag+payload+struct.pack('>I',zlib.crc32(tag+payload)&0xffffffff)


class PrivacyTests(unittest.TestCase):
    def test_jpeg_removes_exif_app13_without_touching_scan_bytes(self):
        scan=b'\xff\xda\x00\x08\x01\x01\x00\x00\x3f\x00\x11\x22\xff\xd9'
        raw=(b'\xff\xd8' + b'\xff\xe1' + struct.pack('>H',2+len(b'Exif-GPS-TEST-COORDS')) + b'Exif-GPS-TEST-COORDS' + b'\xff\xed' + struct.pack('>H',2+len(b'APP13-GPS-METADATA')) + b'APP13-GPS-METADATA' + scan)
        # Synthetic scan bytes intentionally not a real photograph; parser checks transport.
        cleaned=jpeg_clean(raw)
        self.assertNotIn(b'GPS-',cleaned)
        self.assertTrue(cleaned.endswith(scan))

    def test_png_drops_exif_and_text_but_preserves_pixels(self):
        sample=ROOT/'simplicity-builder/examples/synthetic-lakeside.png'
        raw=sample.read_bytes()
        self.assertTrue(raw.startswith(b'\x89PNG'))
        split=8+int.from_bytes(raw[8:12],'big')+12
        enhanced=raw[:split]+chunk(b'eXIf',b'fake GPS latitude 42.0')+chunk(b'tEXt',b'Location\0fake GPS longitude 71.0')+raw[split:]
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'gps.png'
            p.write_bytes(enhanced)
            cleaned,mime=clean_image(p)
        self.assertEqual(mime,'image/png')
        self.assertNotIn(b'GPS',cleaned)
        self.assertEqual(png_clean(cleaned),raw)  # unchanged IDAT and every other image byte

    def test_webp_removes_exif_xmp_and_flags(self):
        def riff(tag,data):
            return tag+struct.pack('<I',len(data))+data+(b'\0' if len(data)&1 else b'')
        body=b'WEBP'+riff(b'VP8X',bytes([0x0c])+bytes(9))+riff(b'VP8 ',b'framebytes')+riff(b'EXIF',b'GPS=42.0')+riff(b'XMP ',b'<GPS>71.0</GPS>')
        cleaned=webp_clean(b'RIFF'+struct.pack('<I',len(body))+body)
        self.assertNotIn(b'GPS',cleaned)
        self.assertNotIn(b'EXIF',cleaned)
        self.assertNotIn(b'XMP ',cleaned)
        self.assertIn(b'framebytes',cleaned)
        self.assertEqual(cleaned[20]&0x0c,0)

    def test_metadata_never_reaches_published_html(self):
        import base64
        original=(ROOT/'simplicity-builder/examples/synthetic-lakeside.png').read_bytes()
        split=8+int.from_bytes(original[8:12],'big')+12
        tainted=original[:split]+chunk(b'eXIf',b'GPS-LATITUDE-42.6 PRIVATE-ADDRESS')+original[split:]
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'photo.png'
            p.write_bytes(tainted)
            uri=embedded_image(p)
            data=json.loads((ROOT/'simplicity-builder/examples/photo-sample.json').read_text(encoding='utf-8'))
            output=generate(to_portfolio(data),uri)
        self.assertNotIn('GPS-LATITUDE',output)
        self.assertNotIn('PRIVATE-ADDRESS',output)
        encoded=output.split('data:image/png;base64,')[1].split('"')[0]
        self.assertNotIn(b'GPS-LATITUDE',base64.b64decode(encoded))
        self.assertNotIn(b'PRIVATE-ADDRESS',base64.b64decode(encoded))

    def test_optional_pillow_downscales_large_dimensions(self):
        try:
            from PIL import Image
        except ImportError:
            raise unittest.SkipTest('Optional Pillow not installed')
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'wide.png'
            Image.new('RGB',(2101,90),'white').save(p)
            cleaned,mime=clean_image(p)
            from io import BytesIO
            with Image.open(BytesIO(cleaned)) as img:
                self.assertLessEqual(max(img.size),2000)

    def test_review_sheet_private_evidence_and_warning(self):
        source=json.loads((ROOT/'simplicity-builder/examples/photo-sample.json').read_text(encoding='utf-8'))
        content=make_review_sheet(source)
        self.assertIn('PRIVATE REVIEW',content)
        self.assertIn('does NOT prove factual correctness',content)
        self.assertIn('Image anchor',content)
        self.assertIn('Evidence or observation',content)

    def test_cli_theme_override_keeps_source_copy_and_private_review(self):
        import subprocess
        fixture=ROOT/'simplicity-builder/examples/guardian-academy.json'
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'index.html'
            private=Path(td)/'private/review.md'
            process=subprocess.run([sys.executable,str(SCRIPTS/'build.py'),'--input',str(fixture),
                '--output',str(out),'--theme','noir mystery','--review-sheet',str(private)],
                capture_output=True,text=True)
            self.assertEqual(process.returncode,0,process.stderr)
            self.assertIn('data-family="noir"',out.read_text(encoding='utf-8'))
            self.assertNotIn('PRIVATE REVIEW',out.read_text(encoding='utf-8'))
            self.assertIn('PRIVATE REVIEW',private.read_text(encoding='utf-8'))
            self.assertIn('The Team Mission',out.read_text(encoding='utf-8'))

    def test_photo_rejects_extreme_and_duplicate_boxes(self):
        original=json.loads((ROOT/'simplicity-builder/examples/photo-sample.json').read_text(encoding='utf-8'))
        for anchor in ({'x':.1,'y':.1,'width':.1,'height':.3},  # 3%
                       {'x':.01,'y':.01,'width':.97,'height':.96}):
            data=json.loads(json.dumps(original))
            data['chapters'][0]['anchor']=anchor
            with self.subTest(anchor=anchor),self.assertRaisesRegex(ValueError,'4%–90%'):
                to_portfolio(data)
        data=json.loads(json.dumps(original))
        data['chapters'][1]['anchor']=dict(data['chapters'][0]['anchor'])
        with self.assertRaisesRegex(ValueError,'overlaps'):
            to_portfolio(data)


class SourceFixtureIsolation(unittest.TestCase):
    def test_copied_examples_have_no_demo_canonical_urls(self):
        for fixture in (ROOT/'examples').glob('*-sample.json'):
            with self.subTest(name=fixture.name):
                self.assertNotIn('share',json.loads(fixture.read_text(encoding='utf-8')).get('world',{}))
        installable=ROOT/'simplicity-builder/examples/fairytale-sample.json'
        self.assertNotIn('share',json.loads(installable.read_text(encoding='utf-8'))['world'])
        for theme in ('fairytale','space','custom','clockwork'):
            demo=ROOT/f'docs/demo-inputs/{theme}-sample.json'
            self.assertIn('share',json.loads(demo.read_text(encoding='utf-8'))['world'])

    def test_manual_synthetic_mountain_box_covers_three_peak_tips(self):
        # Curated observations for THIS illustration only. A general program
        # cannot verify semantic object boundaries in arbitrary photographs.
        photo=json.loads((ROOT/'simplicity-builder/examples/photo-sample.json').read_text(encoding='utf-8'))
        region=photo['chapters'][0]['anchor']
        for x,y in ((.14,.26),(.425,.235),(.79,.38)):
            with self.subTest(peak=(x,y)):
                self.assertLessEqual(region['x'],x)
                self.assertLessEqual(x,region['x']+region['width'])
                self.assertLessEqual(region['y'],y)
                self.assertLessEqual(y,region['y']+region['height'])


class BrokenPageMustFail(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise unittest.SkipTest('Playwright not installed; Chromium negative tests skipped')
        cls.ctx=sync_playwright().start()
        try:
            cls.browser=launch(cls.ctx)
        except Exception:
            cls.ctx.stop()
            raise unittest.SkipTest('Chromium not installed; negative browser tests skipped')

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.ctx.stop()

    def broken(self,filename,css,expected,width=390,height=844):
        page=self.browser.new_page(viewport={'width':width,'height':height})
        try:
            page.set_content((ROOT/'docs'/filename).read_text(encoding='utf-8'),wait_until='load')
            page.emulate_media(reduced_motion='reduce')
            if page.locator('.scene-backdrop').count():
                page.locator('.scene-backdrop').first.evaluate('(img)=>img.decode()')
            page.add_style_tag(content=css)
            with self.assertRaisesRegex(AssertionError,expected):
                assert_visual(page,'deliberately broken')
        finally:
            page.close()

    def test_distant_but_inside_plaque_must_fail(self):
        # A label can be within the stage and not collide, yet be detached.
        self.broken('guardian.html',
                    '.scene-plaque[data-plaque-for="landmark-the-command-deck"]'
                    '{left:6px!important;top:6px!important}', 'plaqueDetached',
                    width=1440,height=900)

    def test_mobile_owner_ellipsis_must_fail(self):
        self.broken('guardian.html',
                    '.owner{white-space:nowrap!important;overflow:hidden!important;'
                    'text-overflow:ellipsis!important;max-width:75px!important}',
                    'ownerClipped')

    def test_miniature_mobile_landmarks_must_fail(self):
        self.broken('guardian.html',
                    '.scene-landmark{scale:.24!important}', 'mobileLandmarkSizes')

    def test_hidden_foreground_seam_must_fail(self):
        page=self.browser.new_page(viewport={'width':1440,'height':900})
        try:
            page.set_content((ROOT/'docs/guardian.html').read_text(encoding='utf-8'),wait_until='load')
            page.evaluate("""() => {
                const svg=document.querySelector('.scene-svg');
                const r=document.createElementNS('http://www.w3.org/2000/svg','rect');
                r.setAttribute('width','620');r.setAttribute('height','520');
                r.setAttribute('fill','#445566');svg.appendChild(r);
            }""")
            with self.assertRaisesRegex(AssertionError,'hardEdges'):
                assert_visual(page,'deliberately added scene-box seam')
        finally:
            page.close()

    def test_overlapping_plaques_must_fail(self):
        self.broken('guardian.html','.scene-plaque{left:7px!important;top:7px!important}', 'plaqueOverlap')

    def test_plaques_outside_stage_must_fail(self):
        self.broken('guardian.html','.scene-plaque{left:-400px!important}', 'plaqueOutside')

    def test_hard_stage_edges_must_fail(self):
        self.broken('guardian.html','.scene-ambience{display:none!important}', 'hardEdges')

    def test_focused_photo_plaque_tracks_next_object(self):
        page=self.browser.new_page(viewport={'width':390,'height':844})
        try:
            page.set_content((ROOT/'docs/photo.html').read_text(encoding='utf-8'),wait_until='load')
            page.locator('.scene-backdrop').first.evaluate('(img)=>img.decode()')
            assert_visual(page,'photo starting focus')
            first=page.locator('.scene-plaque.placed').all_text_contents()
            self.assertEqual(len(first),1)
            page.locator('#photo-next').click()
            assert_visual(page,'photo next focus')
            next_=page.locator('.scene-plaque.placed').all_text_contents()
            self.assertEqual(len(next_),1)
            self.assertNotEqual(first,next_)
        finally:
            page.close()

    def test_photo_coverage_below_55_percent_must_fail(self):
        page=self.browser.new_page(viewport={'width':390,'height':844})
        try:
            page.set_content((ROOT/'docs/photo.html').read_text(encoding='utf-8'),wait_until='load')
            page.locator('.scene-backdrop').first.evaluate('(img)=>img.decode()')
            page.evaluate("""() => {
                const img=document.querySelector('.scene-backdrop');
                img.style.width='150px';img.style.height='100px';
            }""")
            with self.assertRaisesRegex(AssertionError,'photoCoverageLow'):
                assert_visual(page,'deliberately tiny photo')
        finally:
            page.close()

    def test_distorted_celestial_circle_must_fail(self):
        page=self.browser.new_page(viewport={'width':1440,'height':900})
        try:
            page.set_content((ROOT/'docs/fairytale.html').read_text(encoding='utf-8'),wait_until='load')
            page.evaluate("""() => {
                for(const moon of document.querySelectorAll('.scene-ambience circle[r="42"]'))
                    moon.removeAttribute('transform');
            }""")
            with self.assertRaisesRegex(AssertionError,'distortedCircles'):
                assert_visual(page,'deliberately distorted moon')
        finally:
            page.close()

    def test_missing_procedural_scenery_must_fail(self):
        page=self.browser.new_page(viewport={'width':1440,'height':900})
        try:
            page.set_content((ROOT/'docs/guardian.html').read_text(encoding='utf-8'),wait_until='load')
            page.evaluate("""() => {
                document.querySelector('.scene-ambience').replaceChildren();
            }""")
            with self.assertRaisesRegex(AssertionError,'sceneryMissing'):
                assert_visual(page,'deliberately empty ambience')
        finally:
            page.close()

    def test_clipped_header_must_fail(self):
        self.broken('guardian.html','.intro h1{height:2px!important;overflow:hidden!important}', 'headerClipped')

    def test_low_contrast_must_fail(self):
        self.broken('guardian.html','.scene-plaque{background:#f5f5f5!important;color:#eeeeee!important}', 'poorContrast')

    def test_tiny_landmark_must_fail(self):
        self.broken('guardian.html','.scene-landmark{scale:.05!important}', 'tinyTargets')


if __name__=='__main__':
    unittest.main()
