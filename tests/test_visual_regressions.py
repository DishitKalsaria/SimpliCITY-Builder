"""Visual regressions: animations, sparse objects, optional mobile SVG and image layer."""
import copy
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'simplicity-builder/scripts'))
from build_portfolio import generate, validate_model, embedded_image, sanitize_scene

class VisualRegressionTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'examples/space-sample.json').read_text(encoding='utf-8'))

    def test_animated_landmark_has_one_class_attribute(self):
        output=generate(self.data)
        self.assertIn('class="scene-landmark motion-float"',output)
        self.assertIn('class="scene-landmark motion-twinkle"',output)
        # XML itself must parse; duplicate class attrs would fail here.
        import re
        scenes=re.findall(r'<svg class="scene-svg".*?</svg>',output,re.S)
        self.assertEqual(len(scenes),2)  # mobile SVG exists inside inert template

    def test_animated_landmark_source_xml_sanitized(self):
        data=self.data
        source=data['world']['scene_svg']
        result=sanitize_scene(source, section_ids={s['id'] for s in data['sections']},labels={s['id']:s['name'] for s in data['sections']})
        ET.fromstring(result)
        self.assertNotIn('class="motion-float" class="scene-landmark"',result)
        self.assertEqual(result.count('class="scene-landmark'),len(data['sections']))

    def test_sparse_constellation_real_group_and_bounding_box_pointer(self):
        page=generate(self.data)
        self.assertIn('pointer-events:bounding-box',page)
        self.assertIn('id="landmark-skills"',page)
        self.assertIn('stroke-width="4"',page)

    def test_optional_mobile_scene_in_inert_template(self):
        page=generate(self.data)
        self.assertIn('id="mobile-scene-template"',page)
        self.assertIn('matchMedia',page)
        self.assertIn('active.replaceWith(next)',page)
        self.assertIn("world?.addEventListener('keydown'",page)
        self.assertEqual(page.count('<template id="mobile-scene-template">'),1)
        # Both art sources remain present, but only one becomes active when JS executes.
        self.assertEqual(page.count('id="landmark-skills"'),2)

    def test_mobile_landmark_missing_rejected(self):
        data=copy.deepcopy(self.data)
        data['world']['scene_svg_mobile']=data['world']['scene_svg_mobile'].replace('id="landmark-skills"','id="not-a-landmark"')
        with self.assertRaises(ValueError):
            validate_model(data)

    def test_image_assisted_requires_image(self):
        data=copy.deepcopy(self.data)
        data['world']['artwork_mode']='image-assisted'
        with self.assertRaisesRegex(ValueError,'requires --background-image'):
            generate(data)

    def test_embedded_original_raster_is_offline_only(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            image=Path(td)/'image.png'
            image.write_bytes((ROOT / 'simplicity-builder/examples/synthetic-lakeside.png').read_bytes())
            encoded=embedded_image(image)
            self.assertTrue(encoded.startswith('data:image/png;base64,'))
            data=copy.deepcopy(self.data)
            data['world']['artwork_mode']='image-assisted'
            generated=generate(data,encoded)
            self.assertIn('class="scene-backdrop"',generated)
            self.assertIn(encoded,generated)
            self.assertIn('id="landmark-experience"',generated)

    def test_background_rejects_html_or_svg(self):
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            img=Path(td)/'fake.png'
            img.write_text('<svg><script>bad()</script></svg>')
            with self.assertRaisesRegex(ValueError,'JPEG, PNG, or WebP'):
                embedded_image(img)
            img.write_bytes(b'\x89PNG\r\n\x1a\n'+b'Z'*4_000_010)
            with self.assertRaisesRegex(ValueError,'PNG chunk size|Malformed PNG|Corrupt PNG'):
                embedded_image(img)

    def test_owner_approved_paraphrase_requires_real_resume_excerpt(self):
        from verify_facts import evidence_gaps
        data={'profile':{'name':'Jordan Lee','headline':'Engineer','summary':'Summary'},
              'sections':[{'entries':[{'title':'Engineer','description':'A software role', 'tags':['Manufacturing analytics']}]}],
              'review':{'approved_paraphrases':[{'field':'sections[0].entries[0].tags[0]','claim':'Manufacturing analytics',
                      'source_excerpt':'production performance reporting','approved_by_owner':True}]}}
        resume='Jordan Lee, Engineer. Created production performance reporting for factory planning.'
        self.assertEqual(evidence_gaps(data,resume),[])
        data['review']['approved_paraphrases'][0]['source_excerpt']='not present anywhere'
        self.assertTrue(evidence_gaps(data,resume))

if __name__=='__main__':
    unittest.main()

