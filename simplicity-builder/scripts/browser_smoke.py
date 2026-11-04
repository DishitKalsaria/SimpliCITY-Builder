#!/usr/bin/env python3
"""Optional Chromium geometry, interaction and accessibility smoke checks.

Does NOT certify artistic quality or the truth of source interpretation.
For image comparison use repository scripts/compare_screenshots.py.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

VIEWPORTS = (('desktop', 1440, 900), ('mobile', 390, 844),
             ('compact', 360, 640), ('small-phone', 320, 568),
             ('landscape', 844, 390))

METRICS_JS = r'''() => {
  const world=document.querySelector('.scene-world');
  const frame=world.getBoundingClientRect();
  const isPhoto=document.body.classList.contains('photo-mode');
  const isPortrait=innerWidth<=680 && innerHeight>=560;
  const landmarks=[...document.querySelectorAll('.scene-landmark')];
  const plaques=[...document.querySelectorAll('.scene-plaque')];
  const visible=(e)=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);
    return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>.5};
  const intersects=(a,b,pad=0)=>a.left<b.right+pad&&a.right>b.left-pad&&a.top<b.bottom+pad&&a.bottom>b.top-pad;
  const within=(r)=>r.left>=frame.left-2&&r.right<=frame.right+2&&r.top>=frame.top-2&&r.bottom<=frame.bottom+2;
  const gapBetween=(a,b)=>Math.hypot(Math.max(0,a.left-b.right,b.left-a.right),
                                   Math.max(0,a.top-b.bottom,b.top-a.bottom));
  let plaqueOverlap=0,plaqueTargetOverlap=0,plaqueOutside=0,plaqueDetached=0;
  for(let i=0;i<plaques.length;i++){
    if(plaques[i].dataset.placement==='offscreen')continue;
    const a=plaques[i].getBoundingClientRect();
    if(!within(a))plaqueOutside++;
    const assigned=document.getElementById(plaques[i].dataset.plaqueFor);
    if(!assigned||gapBetween(a,assigned.getBoundingClientRect())>(innerWidth<=680?42:60))plaqueDetached++;
    for(let j=i+1;j<plaques.length;j++)if(plaques[j].dataset.placement!=='offscreen'&&intersects(a,plaques[j].getBoundingClientRect(),1))plaqueOverlap++;
    // Panned photo mode presents one named region at a time. Inactive wide
    // source boxes can overlap the current view without representing a visible
    // object near the active plaque; test the active region, not its siblings.
    for(const target of landmarks){
      if(isPhoto&&isPortrait&&target.id!==plaques[i].dataset.plaqueFor)continue;
      if(intersects(a,target.getBoundingClientRect(),1))plaqueTargetOverlap++;
    }
  }
  const photo=world.querySelector('.scene-backdrop');
  let imageCoverage=1,anchorMisses=0;
  if(isPhoto&&photo?.naturalWidth){
    // Image is sized explicitly with an aspect-preserving CSS width/height.
    // Measure what the user actually sees, including partial phone crops.
    const pr=photo.getBoundingClientRect();
    const visibleWidth=Math.max(0,Math.min(frame.right,pr.right)-Math.max(frame.left,pr.left));
    const visibleHeight=Math.max(0,Math.min(frame.bottom,pr.bottom)-Math.max(frame.top,pr.top));
    imageCoverage=visibleWidth*visibleHeight/(frame.width*frame.height);
    const anchors=JSON.parse(document.getElementById('photo-anchors').textContent||'{}');
    for(const [id,anchor] of Object.entries(anchors)){
      const el=document.getElementById('landmark-'+id);
      if(!el){anchorMisses++;continue;}
      const rawL=pr.left+anchor.x*pr.width,rawR=rawL+anchor.width*pr.width;
      const rawT=pr.top+anchor.y*pr.height,rawB=rawT+anchor.height*pr.height;
      if(rawR<frame.left||rawL>frame.right||rawB<frame.top||rawT>frame.bottom)continue;
      const left=Math.max(frame.left+5,rawL),right=Math.min(frame.right-5,rawR);
      const top=Math.max(frame.top+5,rawT),bottom=Math.min(frame.bottom-5,rawB);
      const r=el.getBoundingClientRect();
      const expectedX=(left+right)/2,expectedY=(top+bottom)/2;
      const actualX=(r.left+r.right)/2,actualY=(r.top+r.bottom)/2;
      if(Math.abs(actualX-expectedX)>29||Math.abs(actualY-expectedY)>29)anchorMisses++;
    }
  }
  const title=document.querySelector('.intro h1'),intro=document.querySelector('.intro');
  const owner=document.querySelector('.owner'),bar=document.querySelector('.topbar');
  const ownerStyle=getComputedStyle(owner),or=owner.getBoundingClientRect(),br=bar.getBoundingClientRect();
  const ownerClipped=or.left<br.left-2||or.right>br.right+2||or.top<br.top-2||or.bottom>br.bottom+2||
    ((owner.scrollWidth>owner.clientWidth+2||owner.scrollHeight>owner.clientHeight+2)&&
      ['hidden','clip'].includes(ownerStyle.overflowX));
  const tr=title.getBoundingClientRect(),ir=intro.getBoundingClientRect();
  const titleClipped=tr.left<ir.left-2||tr.right>ir.right+2||tr.bottom>ir.bottom+2||
    ((title.scrollHeight>title.clientHeight+2||title.scrollWidth>title.clientWidth+2)&&['hidden','clip'].includes(getComputedStyle(title).overflowY));
  const lum=c=>{const channels=(c.match(/[0-9.]+/g)||[]).slice(0,3).map(Number);
    return channels.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4})
      .reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0)};
  const contrast=plaques.map(e=>{const s=getComputedStyle(e),a=lum(s.color),b=lum(s.backgroundColor);
      return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)});
  const doc=document.documentElement;
  const ambience=world.querySelector('.scene-ambience');
  const edgeFill=isPhoto||document.body.classList.contains('scenic-art-mode')||!!(ambience&&visible(ambience)&&getComputedStyle(ambience).width===getComputedStyle(world).width);
  // Detect the previous double-projection regression: empty background clone
  // after the first call stripped scenery from the foreground.
  const sceneryMissing=!isPhoto && (!ambience||!ambience.querySelector('path,polygon,rect,ellipse'));
  const distortedCircles=!isPhoto && ambience ? [...ambience.querySelectorAll('circle')]
    .filter(el=>!el.closest('defs')&&Number(el.getAttribute('r'))>=12)
    .filter(el=>{const box=el.getBoundingClientRect();return box.width>3&&box.height>3&&Math.abs(box.width-box.height)/Math.max(box.width,box.height)>.10}).length:0;
  // A second foreground background produces a rectangular seam even when
  // full-stage ambience exists. The foreground should contain landmarks only.
  const art=world.querySelector('.scene-svg');
  const foregroundScenery=!isPhoto&&[...art.querySelectorAll('path,rect,circle,polygon,ellipse,polyline,line')]
    .some(n=>!n.closest('.scene-landmark')&&!n.closest('defs'));
  const mobileLandmarkSizes=!isPhoto&&isPortrait&&landmarks.length<=4?
    landmarks.filter(e=>{const r=e.getBoundingClientRect();return Math.min(r.width,r.height)<60}).length:0;
  const centers=landmarks.map(e=>{const r=e.getBoundingClientRect();return (r.top+r.bottom)/2});
  const portraitComposition=world.querySelector('.scene-svg')?.getAttribute('viewBox')==='0 0 620 880';
  const mobileEmptyBands=!isPhoto&&isPortrait&&portraitComposition&&landmarks.length>=3&&landmarks.length<=4&&
    (Math.max(...centers)-Math.min(...centers)<frame.height*.48);
  return {
    viewportOverflow:doc.scrollWidth>innerWidth+2||doc.scrollHeight>innerHeight+2||getComputedStyle(document.body).overflow!=='hidden',
    stageCoverage:Math.min(frame.width/document.querySelector('.stage').clientWidth,frame.height/document.querySelector('.stage').clientHeight),
    missingPlaques:plaques.filter(p=>p.dataset.placement!=='offscreen'&&(!visible(p)||!p.classList.contains('placed'))).length,
    plaqueOverlap,plaqueTargetOverlap,plaqueOutside,plaqueDetached,
    plaqueControlsOverlap:(()=>{const ctr=world.querySelector('.photo-navigation');return ctr&&getComputedStyle(ctr).display!=='none'?plaques.filter(p=>p.dataset.placement!=='offscreen'&&intersects(p.getBoundingClientRect(),ctr.getBoundingClientRect(),2)).length:0})(),
    clippedLandmarks:isPhoto&&isPortrait?0:landmarks.filter(e=>!within(e.getBoundingClientRect())).length,
    tinyTargets:landmarks.filter(e=>{const r=e.getBoundingClientRect();return r.width<43.5||r.height<43.5}).length,
    photoCoverage:imageCoverage,
    photoCoverageLow:isPhoto&&isPortrait&&imageCoverage<.55,
    anchorMisses,
    hardEdges:!edgeFill||foregroundScenery,sceneryMissing,distortedCircles,
    headerClipped:titleClipped,
    ownerClipped,
    mobileLandmarkSizes,mobileEmptyBands,
    labelsInaccessible:landmarks.filter(el=>!el.getAttribute('aria-label')||!plaques.some(p=>p.dataset.plaqueFor===el.id&&p.textContent.trim())).length,
    poorContrast:contrast.filter(x=>x<4.5).length,
    copyErrors:/\b1 Exhibits\b|Explore experience|in an interactive explore|in an interactive explain/i.test(document.body.innerText),
    isPhoto,numberOfLandmarks:landmarks.length,visibleObjects:landmarks.filter(visible).length,
  };
}'''


def visual_metrics(page) -> dict:
    # Font metrics affect plaque packing. Wait for fonts, then flush the
    # placement scheduled by document.fonts.ready and any resize effects.
    page.evaluate('''async () => {
      await document.fonts?.ready;
      await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    }''')
    return page.evaluate(METRICS_JS)


def assert_visual(page, name: str = 'page') -> dict:
    metrics = visual_metrics(page)
    failures = {k:v for k,v in metrics.items() if k in {
        'viewportOverflow','missingPlaques','plaqueOverlap','plaqueTargetOverlap','plaqueOutside',
        'plaqueControlsOverlap','plaqueDetached','clippedLandmarks','tinyTargets','mobileLandmarkSizes','mobileEmptyBands','photoCoverageLow','anchorMisses','hardEdges',
        'headerClipped','ownerClipped','labelsInaccessible','poorContrast','copyErrors',
        'sceneryMissing','distortedCircles'} and v}
    if metrics['stageCoverage'] < .95:
        failures['stageCoverage']=metrics['stageCoverage']
    if metrics['numberOfLandmarks'] < 1:
        failures['numberOfLandmarks']=0
    if failures:
        raise AssertionError(f'{name}: visual QA failed: {failures}; metrics={metrics}')
    return metrics


def check(path: Path, browser, screenshots: Path | None = None, axe_script: Path | None = None):
    for label,width,height in VIEWPORTS:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.set_content(path.read_text(encoding='utf-8'),wait_until='load')
        page.emulate_media(reduced_motion='reduce')
        page.locator('.scene-backdrop').first.evaluate('(img)=>img.decode()') if page.locator('.scene-backdrop').count() else None
        if page.locator('button.landmark').count()!=page.locator('.scene-landmark').count():
            raise AssertionError(f'{path.name} {label}: landmark/list mismatch')
        assert_visual(page, f'{path.name} {label}')
        if page.locator('#mobile-scene-template').count():
            variant=page.locator('.scene-world > .scene-svg').get_attribute('data-scene-variant')
            expected='mobile' if width<=680 else 'desktop'
            if variant!=expected:
                raise AssertionError(f'{label}: wrong active scene {variant}')
        if screenshots:
            screenshots.mkdir(parents=True,exist_ok=True)
            page.screenshot(path=str(screenshots/f'{path.stem}-{label}.png'))
        if axe_script:
            page.add_script_tag(path=str(axe_script))
            violations=page.evaluate('''async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}});return r.violations.map(v=>v.id)}''')
            if violations:
                raise AssertionError(f'{path.name} {label}: axe violations: {violations}')
        else:
            print('SKIP axe-core: no --axe-script supplied (optional accessibility checks)')
        # DOM Tab order must reach every labelled SVG object (plaques label these objects;
        # decorative plaques themselves are intentionally not separate Tab stops).
        focusable=page.locator('.scene-landmark[tabindex="0"]')
        if focusable.count()!=page.locator('.scene-landmark').count():
            raise AssertionError(f'{label}: landmarks missing keyboard Tab stops')
        # Actually traverse the Tab sequence, not merely inspect tabindex.
        page.evaluate('document.activeElement.blur()')
        reached=set()
        for _ in range(focusable.count()+12):
            page.keyboard.press('Tab')
            focus_id=page.evaluate('document.activeElement?.id')
            if focus_id and focus_id.startswith('landmark-'):
                reached.add(focus_id)
            if len(reached)==focusable.count():
                break
        if len(reached)!=focusable.count():
            raise AssertionError(f'{label}: Tab order missed named landmarks: {reached}')
        # For cropped mobile photos, focus only a visible object; other objects
        # remain reachable via the location list and guided tour panning.
        page.locator('.scene-landmark').first.hover(force=True)
        if not page.locator('#scene-tooltip').is_visible():
            raise AssertionError(f'{label}: landmark tooltip missing')
        if page.locator('.scene-landmark').first.get_attribute('aria-label') is None:
            raise AssertionError(f'{label}: unnamed landmark')
        page.locator('[data-dialog="list-dialog"]').last.click()
        page.locator('button.landmark').first.click()
        if page.locator('dialog.detail-dialog[open] .entry').count()<1:
            raise AssertionError(f'{label}: detail dialog not opened')
        page.keyboard.press('Escape')
        page.locator('.scene-landmark').first.focus()
        page.keyboard.press('Enter')
        if page.locator('dialog.detail-dialog[open]').count()!=1:
            raise AssertionError(f'{label}: keyboard Enter failed')
        page.keyboard.press('Escape')
        page.locator('#start-tour').click()
        if page.locator('dialog.detail-dialog[open] .tour-buttons:not([hidden])').count()!=1:
            raise AssertionError(f'{label}: guided tour did not start')
        if page.locator('button.landmark').count()>1:
            page.locator('dialog.detail-dialog[open] [data-tour="next"]').click()
            if '2 of ' not in page.locator('dialog.detail-dialog[open] [data-tour="status"]').inner_text():
                raise AssertionError(f'{label}: guided tour Next failed')
        page.locator('dialog.detail-dialog[open] [data-tour="exit"]').click()
        page.locator('[data-dialog="list-dialog"]').last.click()
        if page.locator('#list-dialog[open]').count()!=1:
            raise AssertionError('Accessible location list missing')
        search=page.locator('#world-search')
        search.fill('unlikely-query-123xyz')
        if page.locator('button.landmark:visible').count():
            raise AssertionError('Location search failed')
        search.fill('')
        page.keyboard.press('Escape')
        page.locator('[data-dialog="recruiter-dialog"]').first.click()
        if page.locator('#recruiter-dialog[open] .recruiter-section').count()<1:
            raise AssertionError('Overview/print view missing')
        if errors:
            raise AssertionError(f'{label}: JavaScript errors {errors}')
        print(f'PASS {path.name} {label}: geometry, contrast, labels, source alignment, tour and navigation')
        page.close()


def launch(p):
    try:
        return p.chromium.launch(headless=True)
    except Exception:
        binary=shutil.which('chromium') or shutil.which('google-chrome')
        if not binary:
            raise RuntimeError('No Chromium available; browser QA skipped')
        return p.chromium.launch(headless=True, executable_path=binary,args=['--no-sandbox'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pages',nargs='+',type=Path)
    ap.add_argument('--screenshots',type=Path)
    ap.add_argument('--axe-script',type=Path,help='Optional locally installed axe-core JS file; no CDN fetch')
    args=ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        ap.exit(2,'SKIP browser QA: Playwright unavailable. Install Playwright and Chromium.\n')
    if args.axe_script and not args.axe_script.is_file():
        ap.exit(2,'SKIP axe: supplied --axe-script missing\n')
    try:
        with sync_playwright() as p:
            browser=launch(p)
            try:
                for file in args.pages:
                    check(file,browser,args.screenshots,args.axe_script)
            finally:
                browser.close()
    except RuntimeError as err:
        ap.exit(2,str(err)+'\n')

if __name__=='__main__':
    main()
