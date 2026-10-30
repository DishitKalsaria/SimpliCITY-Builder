import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'simplicity-builder'/'scripts'
sys.path.insert(0,str(SCRIPT))
from build_portfolio import generate,validate_model
from verify_facts import evidence_gaps

class InteractiveWorldTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'examples'/'fairytale-sample.json').read_text())

    def test_no_page_scroll_and_hotspots(self):
        page=generate(self.data)
        self.assertIn('height:100dvh',page)
        self.assertIn('overflow:hidden;overscroll-behavior:none',page)
        self.assertEqual(page.count('class="scene-landmark"'),len(self.data['sections']))
        self.assertIn('aria-haspopup="dialog"',page)
        self.assertIn('id="recruiter-dialog"',page)
        self.assertIn('prefers-reduced-motion:reduce',page)

    def test_copy_and_labels_are_configurable(self):
        self.data['world']['copy']['list']='The enchanted atlas'
        self.data['world']['copy']['hint']='Tap glowing castles'
        page=generate(self.data)
        self.assertIn('The enchanted atlas',page)
        self.assertIn('Tap glowing castles',page)
        self.assertIn('The Quest Tower',page)
        self.assertNotIn('The journey begins here',page)

    def test_rich_content_and_quotes(self):
        page=generate(self.data)
        self.assertIn('class="highlights"',page)
        self.assertIn('class="metrics"',page)
        self.assertIn('class="entry quote-entry"',page)
        self.assertIn('Imaginary character',page)

    def test_missing_landmark_label_rejected(self):
        data=copy.deepcopy(self.data)
        data['world']['landmarks'][1]['section_id']='not-a-section'
        with self.assertRaisesRegex(ValueError,'exactly one'):validate_model(data)

    def test_scene_objects_are_real_svg_geometry(self):
        data=copy.deepcopy(self.data)
        data['world']['scene_svg']='<svg viewBox="0 0 620 520"><g id="landmark-experience"><rect x="50" y="80" width="100" height="100" fill="#aabbcc"/></g><g id="landmark-projects"><path d="M200 120 L300 150 L250 220Z" fill="#aabbcc"/></g></svg>'
        page=generate(data)
        self.assertEqual(page.count('class="scene-landmark"'), 2)
        self.assertNotIn('class="hotspot motion-float"',page)
        self.assertIn('aria-label="Explore The Castle"',page)
        self.assertIn('role="button" tabindex="0"',page)

    def test_rejects_unmapped_svg_landmark(self):
        data=copy.deepcopy(self.data)
        data['world']['scene_svg']='<svg viewBox="0 0 620 520"><g id="landmark-experience"><rect x="50" y="80" width="100" height="100" fill="#aabbcc"/></g></svg>'
        with self.assertRaisesRegex(ValueError,'each section needs exactly one'):generate(data)

    def test_rejects_duplicate_svg_landmarks_and_unsafe_ids(self):
        data=copy.deepcopy(self.data)
        data['world']['scene_svg']='<svg viewBox="0 0 620 520"><g id="landmark-experience"><circle cx="100" cy="100" r="35" fill="#aabbcc"/></g><rect id="landmark-experience" x="350" y="90" width="90" height="90" fill="#aabbcc"/><g id="landmark-projects"><rect x="150" y="250" width="90" height="90" fill="#aabbcc"/></g></svg>'
        with self.assertRaisesRegex(ValueError,'duplicate'):generate(data)

    def test_complete_open_graph_metadata_when_image_given(self):
        data=copy.deepcopy(self.data)
        data['world']['share']={'url':'https://example.com/city/','image':'https://example.com/cover.jpg','image_alt':'Fairytale scene'}
        html=generate(data)
        for frag in ('property="og:image"','property="og:url"','name="twitter:card" content="summary_large_image"','name="twitter:image"'):
            self.assertIn(frag,html)
        data['world']['share']['image']='javascript:alert(1)'
        with self.assertRaises(ValueError):generate(data)

    def test_reject_false_quote_attribution(self):
        data=copy.deepcopy(self.data)
        del data['sections'][1]['entries'][1]['attribution']
        with self.assertRaisesRegex(ValueError,'attribution'):validate_model(data)

    def test_fact_evidence_catches_unmatched_metric_and_employer(self):
        data=copy.deepcopy(self.data)
        data['sections'][0]['entries'][0]['employer']='Nonexistent Company'
        data['sections'][0]['entries'][0]['metrics'][0]['value']='97%'
        resume='Alex Rivers works as a product designer at Fictional Studio in 2023 and 2025. They work on product design, research, prototyping and prototypes.'
        gaps=evidence_gaps(data,resume)
        self.assertTrue(any(x['claim']=='97%' for x in gaps))
        self.assertTrue(any(x['claim']=='Nonexistent Company' for x in gaps))

    def test_fact_evidence_works_on_exact_claims(self):
        data={'profile':{'name':'Jordan Lee','headline':'Analyst','summary':'Improved workflows by 97%'},'sections':[{'entries':[{'title':'Project','description':'Reduced effort 97% in 2024.','employer':'Cloud Company','tags':['Python']}]}]}
        resume='Jordan Lee — Analyst at Cloud Company. Reduced effort 97% in 2024. Python automation. Improved workflows by 97%.'
        self.assertEqual(evidence_gaps(data,resume),[])

if __name__=='__main__':unittest.main()
