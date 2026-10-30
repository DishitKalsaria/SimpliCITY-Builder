#!/usr/bin/env python3
"""Generate a standalone interactive world portfolio from grounded JSON (stdlib only)."""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'assets' / 'template.html'

THEMES = {
    'fairytale': {'background': '#100d20', 'background2': '#291e3e', 'accent': '#f6cd8e', 'secondary': '#c4a7f8', 'label': 'The enchanted realm'},
    'space': {'background': '#070c20', 'background2': '#171d46', 'accent': '#9de6ff', 'secondary': '#bf96ff', 'label': 'The cosmic realm'},
    'graffiti': {'background': '#16111c', 'background2': '#302034', 'accent': '#ffb073', 'secondary': '#80ebd9', 'label': 'The creative realm'},
    'ocean': {'background': '#061c27', 'background2': '#103b52', 'accent': '#9beade', 'secondary': '#a4caff', 'label': 'The underwater realm'},
    'custom': {'background': '#101522', 'background2': '#222d43', 'accent': '#f3cf9e', 'secondary': '#a7c8ef', 'label': 'The imagined realm'},
}


def fail(message: str) -> None:
    raise ValueError(message)


def required(obj: dict, key: str, context: str, limit: int = 3000) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f'{context}.{key}: nonempty string required')
    if len(value) > limit:
        fail(f'{context}.{key}: exceeds {limit} characters')
    return value.strip()


def optional(obj: dict, key: str, context: str, limit: int = 3000) -> str:
    value = obj.get(key, '')
    if value is None:
        return ''
    if not isinstance(value, str) or len(value) > limit:
        fail(f'{context}.{key}: expected string up to {limit} characters')
    return value.strip()


def safe_url(value: str) -> str:
    if not value:
        return ''
    parsed = urlparse(value)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc or any(c.isspace() for c in value):
        fail('Links must be absolute http(s) URLs')
    return value


def safe_color(value: str, fallback: str) -> str:
    if not value:
        return fallback
    if not re.fullmatch(r'#[A-Fa-f0-9]{3}(?:[A-Fa-f0-9]{3})?', value):
        fail('Theme accent colors must be #RGB or #RRGGBB')
    return value


def safe_background(value: str, fallback: str) -> str:
    color = safe_color(value, fallback)
    expanded = color.lstrip('#')
    if len(expanded) == 3:
        expanded = ''.join(ch * 2 for ch in expanded)
    rgb = [int(expanded[i:i+2], 16) / 255 for i in (0, 2, 4)]
    channels = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    lum = sum(c * w for c, w in zip(channels, (0.2126, 0.7152, 0.0722)))
    if lum > 0.16:
        fail('World backgrounds must be dark for readable text (luminance <= 0.16)')
    return color


def e(text: str) -> str:
    return html.escape(text, quote=True)


def validate_model(data: object) -> dict:
    if not isinstance(data, dict):
        fail('JSON root must be an object')
    profile, world, sections = data.get('profile'), data.get('world'), data.get('sections')
    if not isinstance(profile, dict) or not isinstance(world, dict):
        fail('profile and world objects required')
    for field, limit in (('name', 100), ('headline', 180), ('summary', 2000)):
        required(profile, field, 'profile', limit)
    for field, limit in (('title', 95), ('tagline', 200), ('theme', 60)):
        required(world, field, 'world', limit)
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', world['theme']):
        fail('world.theme must be a lowercase hyphenated identifier (any setting is allowed)')
    for field in ('description', 'symbol', 'accent', 'accent_secondary', 'background', 'background_secondary', 'visual_name'):
        optional(world, field, 'world')
    copy = world.get('copy', {})
    if not isinstance(copy, dict):
        fail('world.copy must be an object')
    allowed_copy = {'eyebrow', 'explore', 'hint', 'list', 'recruiter', 'about', 'close', 'search', 'empty', 'made_with', 'privacy', 'print', 'intro', 'locations', 'skip', 'open', 'view_work'}
    for key, value in copy.items():
        if key not in allowed_copy or not isinstance(value, str) or len(value) > 180:
            fail(f'world.copy.{key}: unsupported key or text longer than 180 characters')
    # v0.1.3: labels refer to real SVG objects, never coordinates or icon pins.
    # v0.1.2 hotspot records are accepted for migration; x/y are ignored.
    landmarks = world.get('landmarks', world.get('hotspots', []))
    if not isinstance(landmarks, list) or len(landmarks) > 8:
        fail('world.landmarks must be an array of up to 8 labelled objects')
    landmark_ids = set()
    for i, item in enumerate(landmarks):
        if not isinstance(item, dict):
            fail(f'world.landmarks[{i}]: expected object')
        sid = required(item, 'section_id', f'world.landmarks[{i}]', 40)
        required(item, 'label', f'world.landmarks[{i}]', 60)
        if sid in landmark_ids:
            fail('world.landmarks: section_id must be unique')
        landmark_ids.add(sid)
    mode = optional(world, 'artwork_mode', 'world', limit=20) or 'svg'
    if mode not in ('svg', 'image-assisted'):
        fail('world.artwork_mode: expected svg or image-assisted')
    mobile_artwork = optional(world, 'scene_svg_mobile', 'world', limit=25000)
    if mobile_artwork:
        sanitize_scene(mobile_artwork)
    artwork = optional(world, 'scene_svg', 'world', limit=25000)
    if artwork:
        sanitize_scene(artwork)
    theme_def = THEMES.get(world['theme'], THEMES['custom'])
    safe_color(world.get('accent') or '', theme_def['accent'])
    safe_color(world.get('accent_secondary') or '', theme_def['secondary'])
    safe_background(world.get('background') or '', theme_def['background'])
    safe_background(world.get('background_secondary') or '', theme_def['background2'])
    links = profile.get('links', [])
    if not isinstance(links, list) or len(links) > 8:
        fail('profile.links must be an array of up to 8 items')
    for i, link in enumerate(links):
        if not isinstance(link, dict):
            fail(f'profile.links[{i}] must be an object')
        required(link, 'label', f'profile.links[{i}]', 60)
        safe_url(required(link, 'url', f'profile.links[{i}]', 600))
    if not isinstance(sections, list) or not (1 <= len(sections) <= 8):
        fail('sections must contain 1–8 items')
    seen = set()
    for i, section in enumerate(sections):
        context = f'sections[{i}]'
        if not isinstance(section, dict):
            fail(f'{context} must be an object')
        sid = required(section, 'id', context, 40)
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', sid) or sid in seen:
            fail(f'{context}.id invalid or duplicate')
        seen.add(sid)
        required(section, 'name', context, 110)
        required(section, 'intro', context, 650)
        optional(section, 'symbol', context, 25)
        optional(section, 'eyebrow', context, 80)
        entries = section.get('entries')
        if not isinstance(entries, list) or not (1 <= len(entries) <= 20):
            fail(f'{context}.entries must contain 1–20 items')
        for j, entry in enumerate(entries):
            item = f'{context}.entries[{j}]'
            if not isinstance(entry, dict):
                fail(f'{item} must be an object')
            required(entry, 'title', item, 220)
            required(entry, 'description', item, 2500)
            optional(entry, 'subtitle', item, 250)
            url = optional(entry, 'url', item, 600)
            if url:
                safe_url(url)
            tags = entry.get('tags', [])
            if not isinstance(tags, list) or len(tags) > 12 or any(not isinstance(t, str) or len(t) > 55 for t in tags):
                fail(f'{item}.tags must contain up to 12 short strings')
            if entry.get('type', 'standard') not in ('standard', 'quote'):
                fail(f'{item}.type: must be standard or quote')
            if entry.get('type') == 'quote':
                required(entry, 'attribution', item, 180)
            for fld in ('employer', 'dates', 'attribution'):
                optional(entry, fld, item, 220)
            highlights = entry.get('highlights', [])
            if not isinstance(highlights, list) or len(highlights) > 12 or any(not isinstance(v, str) or not v.strip() or len(v) > 400 for v in highlights):
                fail(f'{item}.highlights: expected up to 12 nonempty short strings')
            metrics = entry.get('metrics', [])
            if not isinstance(metrics, list) or len(metrics) > 6:
                fail(f'{item}.metrics: expected up to 6 objects')
            for m in metrics:
                if not isinstance(m, dict):
                    fail(f'{item}.metrics: expected objects')
                required(m, 'value', f'{item}.metrics', 48)
                required(m, 'label', f'{item}.metrics', 85)
    if landmarks and landmark_ids != seen:
        fail('world.landmarks: provide exactly one labelled object for each section ID')
    if artwork:
        sanitize_scene(artwork, section_ids=seen)
    if mobile_artwork:
        sanitize_scene(mobile_artwork, section_ids=seen)
    review = data.get('review', {})
    if not isinstance(review, dict) or any(k not in {'approved_paraphrases'} for k in review):
        fail('review: only approved_paraphrases is supported')
    approvals = review.get('approved_paraphrases', [])
    if not isinstance(approvals, list) or len(approvals) > 30:
        fail('review.approved_paraphrases: expected up to 30 owner approvals')
    for i, approval in enumerate(approvals):
        if not isinstance(approval, dict):
            fail(f'review.approved_paraphrases[{i}]: expected object')
        for field, limit in [('field', 150), ('claim', 250), ('source_excerpt', 800)]:
            required(approval, field, f'review.approved_paraphrases[{i}]', limit)
        if approval.get('approved_by_owner') is not True:
            fail('review.approved_paraphrases: approved_by_owner must be true')
    share = world.get('share', {})
    if not isinstance(share, dict):
        fail('world.share: expected object')
    for key in share:
        if key not in {'url','image','image_alt'}:
            fail(f'world.share.{key}: unsupported field')
    for key in ('url','image'):
        value = optional(share, key, 'world.share', 600)
        if value:
            safe_url(value)
    optional(share, 'image_alt', 'world.share', 160)
    return data


# Optional original hero illustration for truly open-ended prompts. SVG is parsed and
# re-serialized through a strict allowlist; scripts, links, CSS and external resources
# are not accepted. This artwork is decorative; career facts remain HTML text.
SVG_TAGS = {'svg', 'defs', 'linearGradient', 'radialGradient', 'stop',
            'g', 'circle', 'ellipse', 'rect', 'line', 'path', 'polygon', 'polyline'}
SVG_COMMON = {'transform', 'opacity', 'fill', 'stroke', 'stroke-width', 'class',
              'stroke-linecap', 'stroke-linejoin'}
SVG_GEOMETRY = {
    'svg': {'viewBox'}, 'defs': set(),
    'linearGradient': {'id', 'x1', 'y1', 'x2', 'y2'},
    'radialGradient': {'id', 'cx', 'cy', 'r', 'fx', 'fy'},
    'stop': {'offset', 'stop-color', 'stop-opacity'},
    'g': SVG_COMMON | {'id'},
    'circle': {'cx', 'cy', 'r'} | SVG_COMMON | {'id'},
    'ellipse': {'cx', 'cy', 'rx', 'ry'} | SVG_COMMON | {'id'},
    'rect': {'x', 'y', 'width', 'height', 'rx', 'ry'} | SVG_COMMON | {'id'},
    'line': {'x1', 'y1', 'x2', 'y2'} | SVG_COMMON | {'id'},
    'path': {'d'} | SVG_COMMON | {'id'},
    'polygon': {'points'} | SVG_COMMON | {'id'},
    'polyline': {'points'} | SVG_COMMON | {'id'},
}
SVG_NUMERIC = {'cx','cy','r','rx','ry','x','y','width','height','x1','y1','x2','y2',
               'stroke-width','opacity','stop-opacity'}
SVG_GRADIENT_COORDS = {'cx','cy','r','fx','fy','x1','y1','x2','y2'}
SVG_ID = re.compile(r'[A-Za-z][A-Za-z0-9_-]{0,39}\Z')
SVG_PAINT = re.compile(r'(?:#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?|none|white|black|var\(--accent2?\)|url\(#[A-Za-z][A-Za-z0-9_-]{0,39}\))\Z')
SVG_REF = re.compile(r'url\(#([A-Za-z][A-Za-z0-9_-]{0,39})\)\Z')
SVG_PATH = re.compile(r'[MmLlHhVvCcSsQqTtAaZzEe0-9.,+\-\s]*\Z')
SVG_TRANSFORM = re.compile(r'(?:translate|rotate|scale|matrix|skewX|skewY)\([0-9eE+.,\s-]+\)(?:\s+(?:translate|rotate|scale|matrix|skewX|skewY)\([0-9eE+.,\s-]+\))*\Z')
SVG_NUMBER = re.compile(r'[+\-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+\-]?\d+)?\Z')
SVG_NS = 'http://www.w3.org/2000/svg'


def _svg_name(name: str) -> str:
    # Standard SVG xmlns is allowed, other namespaces, including xlink, are not.
    if name.startswith('{'):
        prefix, _, local = name[1:].partition('}')
        if prefix != SVG_NS:
            fail(f'world.scene_svg: forbidden XML namespace {prefix}')
        return local
    return name


def _fraction(value: str, attribute: str, percent: bool = False) -> None:
    raw = value[:-1] if percent and value.endswith('%') else value
    if not SVG_NUMBER.fullmatch(raw):
        fail(f'world.scene_svg: invalid {attribute}={value!r} (expected a number{ " or percentage" if percent else ""})')
    if attribute in ('opacity', 'stop-opacity', 'offset'):
        number = float(raw)
        if value.endswith('%'):
            number /= 100
        if not 0 <= number <= 1:
            fail(f'world.scene_svg: {attribute} must be between 0 and 1')


def sanitize_scene(markup: str, section_ids: set[str] | None = None, labels: dict[str, str] | None = None) -> str:
    """Allow inert decorative SVG and self-contained gradients, never active resources.

    This is intentionally restrictive. New SVG features must be added to the
    allowlist, documented, and covered by tests at the same time.
    """
    if len(markup) > 25000 or '<!' in markup or '<?' in markup:
        fail('world.scene_svg: illegal or oversized SVG (25,000 characters max)')
    try:
        root = ET.fromstring(markup)
    except ET.ParseError as exc:
        fail(f'world.scene_svg: malformed SVG ({exc})')
    if _svg_name(root.tag) != 'svg' or root.attrib.get('viewBox') != '0 0 620 520':
        fail('world.scene_svg: root must be <svg viewBox="0 0 620 520">')
    if set(root.attrib) != {'viewBox'}:
        fail('world.scene_svg: root attributes other than viewBox are not supported')

    count = 0
    gradient_ids: set[str] = set()
    gradient_refs: set[str] = set()
    landmark_ids: set[str] = set()

    def clean(node: ET.Element, parent: str = '') -> str:
        nonlocal count
        count += 1
        if count > 180:
            fail('world.scene_svg: exceeds 180 elements')
        tag = _svg_name(node.tag)
        if tag not in SVG_TAGS:
            fail(f'world.scene_svg: forbidden tag <{tag}>')
        if (node.text or '').strip() or (node.tail or '').strip():
            fail('world.scene_svg: text nodes are not supported')
        if tag == 'defs' and parent != 'svg':
            fail('world.scene_svg: <defs> must be a direct child of <svg>')
        if tag in {'linearGradient', 'radialGradient'} and parent != 'defs':
            fail(f'world.scene_svg: <{tag}> must be inside <defs>')
        if tag == 'stop' and parent not in {'linearGradient', 'radialGradient'}:
            fail('world.scene_svg: <stop> must be inside a gradient')
        if parent == 'defs' and tag not in {'linearGradient', 'radialGradient'}:
            fail('world.scene_svg: <defs> may only contain gradients')
        if parent in {'linearGradient', 'radialGradient'} and tag != 'stop':
            fail('world.scene_svg: gradients may only contain <stop>')
        if tag in {'linearGradient', 'radialGradient'} and not node.attrib.get('id'):
            fail('world.scene_svg: every gradient needs an id')
        pieces = []
        for raw_key, val in node.attrib.items():
            key = _svg_name(raw_key)
            if key not in SVG_GEOMETRY[tag] or len(val) > 3500:
                fail(f'world.scene_svg: <{tag}> does not allow attribute {key!r}')
            if key in SVG_NUMERIC:
                _fraction(val, key, percent=tag in ('linearGradient', 'radialGradient') or key == 'offset')
            if tag in {'linearGradient', 'radialGradient'} and key in SVG_GRADIENT_COORDS:
                _fraction(val, key, percent=True)
            if key == 'offset':
                _fraction(val, key, percent=True)
            if key in {'fill', 'stroke', 'stop-color'}:
                if not SVG_PAINT.fullmatch(val) or (key == 'stop-color' and val.startswith('url(')):
                    fail(f'world.scene_svg: invalid paint for {key}: {val!r}')
                ref = SVG_REF.fullmatch(val)
                if ref:
                    gradient_refs.add(ref.group(1))
            if key == 'id':
                if not SVG_ID.fullmatch(val):
                    fail(f'world.scene_svg: invalid ID {val!r}')
                if tag in {'linearGradient','radialGradient'}:
                    if val in gradient_ids or val in landmark_ids:
                        fail(f'world.scene_svg: duplicate ID {val!r}')
                    gradient_ids.add(val)
                else:
                    if not val.startswith('landmark-'):
                        fail(f'world.scene_svg: interactive object id must begin landmark- ({val!r})')
                    if val in landmark_ids or val in gradient_ids:
                        fail(f'world.scene_svg: duplicate landmark {val!r}')
                    if parent in {'defs','linearGradient','radialGradient'}:
                        fail('world.scene_svg: landmarks must be visible shapes, not definitions')
                    landmark_ids.add(val)
            if key == 'viewBox' and val != '0 0 620 520':
                fail('world.scene_svg: viewBox must be 0 0 620 520')
            if key == 'd' and not SVG_PATH.fullmatch(val):
                fail('world.scene_svg: invalid path data')
            if key == 'points' and not re.fullmatch(r'[0-9eE+.,\s-]{1,3500}', val):
                fail('world.scene_svg: invalid points')
            if key == 'class' and val not in {'motion-twinkle','motion-float','motion-drift','motion-pulse'}:
                fail('world.scene_svg: only predefined motion classes are permitted')
            if key == 'transform' and not SVG_TRANSFORM.fullmatch(val):
                fail('world.scene_svg: invalid transform; use translate, rotate, scale, matrix or skewX/skewY')
            if key == 'stroke-linecap' and val not in {'round', 'square', 'butt'}:
                fail('world.scene_svg: stroke-linecap must be round, square or butt')
            if key == 'stroke-linejoin' and val not in {'round', 'bevel', 'miter'}:
                fail('world.scene_svg: stroke-linejoin must be round, bevel or miter')
            # A landmark receives a single combined class attribute below.
            # Duplicate class attributes are invalid XML/HTML and break motion + clicks.
            if not (key == 'class' and node.attrib.get('id', '').startswith('landmark-')):
                pieces.append(f' {key}="{e(val)}"')
        landmark_id = node.attrib.get('id', '') if tag not in {'linearGradient','radialGradient'} else ''
        if landmark_id.startswith('landmark-'):
            section_id = landmark_id.removeprefix('landmark-')
            if section_ids is not None and section_id not in section_ids:
                fail(f'world.scene_svg: landmark {section_id!r} is not a section id')
            if any(child.attrib.get('id', '').startswith('landmark-') for child in node.iter() if child is not node):
                fail('world.scene_svg: landmarks cannot be nested')
            if labels is not None:
                human_label = labels[section_id]
                motion = node.attrib.get('class', '')
                classes = 'scene-landmark' + (f' {motion}' if motion else '')
                attrs = f' role="button" tabindex="0" aria-haspopup="dialog" aria-label="Explore {e(human_label)}" data-dialog="detail-{e(section_id)}" class="{classes}"' 
                return f'<{tag}{"".join(pieces)}{attrs}><title>{e(human_label)}</title>' + ''.join(clean(child, tag) for child in node) + f'</{tag}>'
        return f'<{tag}{"".join(pieces)}>' + ''.join(clean(child, tag) for child in node) + f'</{tag}>'

    interior = ''.join(clean(child, 'svg') for child in root)
    missing = gradient_refs - gradient_ids
    if missing:
        fail(f'world.scene_svg: paint refers to undefined gradient id(s): {", ".join(sorted(missing))}')
    if section_ids is not None:
        expected = {'landmark-' + sid for sid in section_ids}
        if landmark_ids != expected:
            fail('world.scene_svg: each section needs exactly one named SVG object (landmark-<section-id>); missing: ' + ', '.join(sorted(expected-landmark_ids)))
    return '<svg class="scene-svg" viewBox="0 0 620 520" role="group" aria-label="Explorable illustrated world" xmlns="http://www.w3.org/2000/svg">' + interior + '</svg>'


def scene_svg(theme: str) -> str:
    start = '''<svg class="scene-svg" viewBox="0 0 620 520" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs>
      <radialGradient id="halo"><stop stop-color="var(--accent)" stop-opacity=".36"/><stop offset="1" stop-color="var(--accent)" stop-opacity="0"/></radialGradient>
      <linearGradient id="earth" x1="0" x2="0" y1="0" y2="1"><stop stop-color="var(--accent2)" stop-opacity=".8"/><stop offset="1" stop-color="var(--accent)" stop-opacity=".3"/></linearGradient>
      </defs><circle cx="315" cy="253" r="235" fill="url(#halo)"/>
      <g fill="var(--accent)" opacity=".65"><circle cx="107" cy="96" r="3"/><circle cx="500" cy="83" r="3"/><circle cx="472" cy="147" r="2"/><circle cx="160" cy="198" r="2"/><circle cx="530" cy="304" r="3"/><circle cx="78" cy="338" r="2"/><circle cx="375" cy="64" r="2"/></g>'''
    scenes = {
        'fairytale': '''<path d="M22 398 Q150 320 282 389 T607 382 L607 522 H22Z" fill="#405071" opacity=".65"/>
          <path d="M0 441 Q175 369 320 430 T620 409 V522 H0Z" fill="#244e4a"/>
          <path d="M180 397 L180 248 L227 248 L227 197 L261 175 L296 197 L296 247 L351 247 L351 170 L387 129 L425 170 L425 250 L453 250 L453 397 Z" fill="#9780b4"/>
          <path d="M205 248 L205 219 L237 187 L269 219 L269 248 M342 170 L387 103 L433 170" fill="#dfb8e8"/>
          <path d="M286 398 V320 Q318 279 348 320 V398" fill="#2c2243"/><path d="M226 286 H249 V319 H226ZM370 213 H395 V244 H370Z" fill="#ffd994"/>
          <path d="M182 403 Q322 372 460 406" fill="none" stroke="#f8d7a3" stroke-width="7" stroke-linecap="round" opacity=".6"/>
          <circle cx="457" cy="136" r="30" fill="#f9dcac" opacity=".85"/>
          <g fill="#f9dba8"><path d="M110 236 l4 13 13 4-13 4-4 13-4-13-13-4 13-4Z"/><path d="M490 284 l3 9 9 3-9 3-3 9-3-9-9-3 9-3Z"/></g>''',
        'space': '''<circle cx="322" cy="259" r="145" fill="#7c72b3"/><circle cx="289" cy="220" r="134" fill="#464c93"/>
          <circle cx="289" cy="220" r="134" fill="url(#earth)" opacity=".5"/>
          <ellipse cx="321" cy="268" rx="226" ry="64" transform="rotate(-25 321 268)" fill="none" stroke="#eac9f0" stroke-width="27" opacity=".66"/>
          <ellipse cx="321" cy="268" rx="226" ry="64" transform="rotate(-25 321 268)" fill="none" stroke="#fcdfb6" stroke-width="7" opacity=".8"/>
          <circle cx="95" cy="353" r="42" fill="#f6aa8d"/><circle cx="493" cy="105" r="30" fill="#a1d8e8"/>
          <path d="M174 178 q65-80 155-20" fill="none" stroke="#c1b4ff" stroke-width="9" opacity=".25"/>
          <g fill="var(--accent)"><path d="M520 326 l5 15 15 5-15 5-5 15-5-15-15-5 15-5Z"/><path d="M132 96 l3 11 11 3-11 3-3 11-3-11-11-3 11-3Z"/></g>''',
        'graffiti': '''<path d="M25 438 V290 H93 V336 H128 V247 H204 V320 H240 V199 H328 V303 H379 V250 H454 V340 H492 V284 H594 V438 Z" fill="#524059"/>
          <path d="M0 435 H620 V520 H0Z" fill="#30243d"/><path d="M115 330 L218 266 L305 339 L391 260 L500 332" fill="none" stroke="#ffae6f" stroke-width="28" stroke-linecap="round" opacity=".85"/>
          <path d="M137 372 Q280 280 412 366" fill="none" stroke="#8dedcf" stroke-width="23" stroke-linecap="round"/>
          <path d="M194 228 q58-81 112-12 t97 8" fill="none" stroke="#da9cff" stroke-width="15" stroke-linecap="round"/>
          <circle cx="456" cy="152" r="34" fill="#ffd17a"/><circle cx="138" cy="153" r="11" fill="#8debd4"/><circle cx="498" cy="403" r="14" fill="#fa7fa4"/>
          <g fill="#ffe7bb" opacity=".65"><rect x="275" y="236" width="14" height="28" rx="3"/><rect x="73" y="315" width="11" height="20" rx="3"/><rect x="536" y="316" width="13" height="20" rx="3"/></g>''',
        'ocean': '''<circle cx="460" cy="147" r="76" fill="#a2ddec" opacity=".26"/>
          <path d="M0 316 Q85 256 162 312 T326 308 T492 312 T620 308 V520 H0Z" fill="#348b9a" opacity=".65"/>
          <path d="M0 380 Q130 326 270 386 T620 368 V520 H0Z" fill="#13566e"/>
          <path d="M75 440 q-18-66 3-116 M75 440 q22-86 53-105 M75 440 q-42-88-72-91 M521 446 q20-92 11-155 M521 446 q-30-91-62-108 M521 446 q39-72 77-81" fill="none" stroke="#e09eb1" stroke-width="15" stroke-linecap="round"/>
          <path d="M233 424 v-135 q34-56 72 0 v135 M285 424 v-176 q52-67 103 0 v176" fill="#84c3cd" opacity=".8"/>
          <circle cx="320" cy="295" r="24" fill="#f6d19f"/><circle cx="174" cy="202" r="9" fill="none" stroke="#c2f1ef" stroke-width="3"/><circle cx="422" cy="239" r="15" fill="none" stroke="#c2f1ef" stroke-width="3"/>''',
        'custom': '''<path d="M60 365 Q160 220 300 330 T560 325" fill="none" stroke="var(--accent2)" stroke-width="75" opacity=".35"/>
          <path d="M80 426 Q220 346 354 413 T590 380" fill="none" stroke="var(--accent)" stroke-width="57" opacity=".23"/>
          <circle cx="308" cy="259" r="128" fill="none" stroke="var(--accent2)" stroke-width="9" opacity=".75"/>
          <circle cx="308" cy="259" r="96" fill="var(--accent2)" opacity=".23"/>
          <path d="M308 146 l20 76 76 20-76 20-20 76-20-76-76-20 76-20Z" fill="var(--accent)" opacity=".8"/>''',
    }
    return start + scenes[theme] + '</svg>'



def share_meta(world: dict, profile: dict) -> str:
    """Optional share cards: only advertise images that have public HTTPS URLs."""
    share = world.get('share') or {}
    url = safe_url(share.get('url', ''))
    image = safe_url(share.get('image', ''))
    title = e(world['title'] + ' — ' + profile['name'])
    description = e(world.get('description') or world['tagline'])
    tags = [f'<meta name="twitter:card" content="{("summary_large_image" if image else "summary")}">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{description}">']
    if url:
        tags += [f'<meta property="og:url" content="{e(url)}">', f'<link rel="canonical" href="{e(url)}">']
    if image:
        tags += [f'<meta property="og:image" content="{e(image)}">',
                 f'<meta name="twitter:image" content="{e(image)}">',
                 f'<meta property="og:image:alt" content="{e(share.get("image_alt") or world["title"])}">']
    return '\n  '.join(tags)


def object_scene(theme: str, sections: list[dict]) -> str:
    """Fallback for when an agent doesn't supply original named art.

    The interactive shapes ARE the illustrated objects. No percentage pin positions
    or artificial overlay hit targets are generated.
    """
    n = len(sections)
    if n == 1: positions = [(310, 275)]
    elif n == 2: positions = [(186, 300), (438, 277)]
    elif n == 3: positions = [(154, 322), (463, 322), (313, 170)]
    elif n == 4: positions = [(153, 187), (455, 191), (156, 372), (456, 371)]
    else:
        positions = [(x, y) for y in (185, 365) for x in (95, 235, 385, 525)][:n]
    top = ('<svg viewBox="0 0 620 520"><defs>'
           '<radialGradient id="glow"><stop stop-color="var(--accent2)" stop-opacity=".33"/><stop offset="1" stop-color="var(--accent2)" stop-opacity="0"/></radialGradient>'
           '<linearGradient id="roof" x1="0" y1="0" x2="1" y2="1"><stop stop-color="var(--accent)"/><stop offset="1" stop-color="var(--accent2)"/></linearGradient>'
           '</defs><ellipse cx="310" cy="255" rx="285" ry="230" fill="url(#glow)"/>')
    if theme == 'space':
        top += '<path d="M0 484 Q170 455 340 487 T620 476 V520 H0Z" fill="#131e39" opacity=".6"/>'
        top += ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cbd8f7" opacity=".75"/>' for x,y,r in [(68,90,2),(470,65,3),(558,400,2),(94,425,2),(340,63,2),(540,168,2),(260,465,2)])
    elif theme == 'fairytale':
        top += '''<circle cx="490" cy="104" r="42" fill="#f4dfc1" opacity=".82"/><circle cx="490" cy="104" r="77" fill="url(#glow)"/>
          <g class="motion-twinkle" fill="#fbe3b7" opacity=".7"><circle cx="112" cy="81" r="3"/><circle cx="378" cy="105" r="3"/><circle cx="540" cy="242" r="4"/><circle cx="282" cy="56" r="2"/><circle cx="588" cy="142" r="2"/></g>
          <path d="M0 383 Q95 280 197 361 T421 357 T620 340 V520 H0Z" fill="#4b467a" opacity=".5"/>
          <path d="M0 439 Q116 375 222 412 T455 399 T620 414 V520 H0Z" fill="#315461" opacity=".85"/>
          <path d="M0 479 Q186 440 310 480 T620 457 V520 H0Z" fill="#27444d"/>
          <path d="M204 474 Q282 441 308 394 T401 354" fill="none" stroke="#eac48c" stroke-width="16" opacity=".22"/>
          <path d="M55 425 Q65 368 81 334 M74 423 Q91 379 111 356 M526 414 Q538 364 550 341 M542 419 Q566 378 585 362" fill="none" stroke="#b0a7c3" stroke-width="13" stroke-linecap="round" opacity=".65"/>'''
    elif theme == 'ocean':
        top += '<path d="M0 470 Q135 420 286 462 T620 445 V520 H0Z" fill="#34486c" opacity=".44"/>'
    elif theme in ('graffiti','custom'):
        top += '<path d="M0 456 Q180 413 310 448 T620 437 V520 H0Z" fill="#514468" opacity=".42"/>'
    parts = []
    for i,(section,(x,y)) in enumerate(zip(sections, positions)):
        sid = e(section['id'])
        if theme == 'space':
            if i % 3 == 1:
                # A spacecraft, not a circular marker.
                parts.append(f'<g id="landmark-{sid}"><path d="M{x} {y-86} Q{x+49} {y-25} {x+38} {y+52} L{x-38} {y+52} Q{x-49} {y-25} {x} {y-86}Z" fill="url(#roof)"/><path d="M{x-35} {y+20} L{x-65} {y+65} L{x-15} {y+52}Z" fill="#b2b1e3"/><path d="M{x+35} {y+20} L{x+65} {y+65} L{x+15} {y+52}Z" fill="#b2b1e3"/><circle cx="{x}" cy="{y-7}" r="19" fill="#253559" stroke="#e4effe" stroke-width="6"/><path d="M{x-20} {y+52} L{x} {y+94} L{x+20} {y+52}Z" fill="#f9c68d" opacity=".87"/></g>')
            else:
                r = 61 if n <= 4 else 40
                parts.append(f'<g id="landmark-{sid}"><circle cx="{x}" cy="{y}" r="{r}" fill="url(#roof)"/><path d="M{x-r*.77:.1f} {y+6} Q{x-8} {y-r*.5:.1f} {x+r*.60:.1f} {y+3}" fill="none" stroke="#d1dafa" stroke-width="13" opacity=".34"/><circle cx="{x-14}" cy="{y-16}" r="{r*.37:.1f}" fill="#fff8f2" opacity=".18"/><ellipse cx="{x}" cy="{y+4}" rx="{r+14}" ry="{r*.33:.1f}" transform="rotate(-23 {x} {y+4})" fill="none" stroke="var(--accent2)" stroke-width="8" opacity=".85"/></g>')
        elif theme == 'fairytale' and i % 2 == 1:
            # Windmill with painted sails and a true figure outline.
            parts.append(f'<g id="landmark-{sid}"><path d="M{x-42} {y+70} L{x-30} {y-25} L{x+30} {y-25} L{x+42} {y+70}Z" fill="#a792b1"/><path d="M{x-36} {y-25} L{x} {y-68} L{x+36} {y-25}Z" fill="url(#roof)"/><rect x="{x-9}" y="{y+18}" width="18" height="52" rx="8" fill="#342844"/><g transform="rotate(-15 {x} {y-19})"><path d="M{x-9} {y-17} L{x-25} {y-110} L{x+8} {y-110} L{x+10} {y-20}Z" fill="#edcee9"/><path d="M{x+8} {y-24} L{x+98} {y-42} L{x+105} {y-10} L{x+10} {y-11}Z" fill="#f5ce91"/><path d="M{x+10} {y-15} L{x+28} {y+82} L{x-5} {y+84} L{x-9} {y-12}Z" fill="#edcee9"/><path d="M{x-10} {y-17} L{x-98} {y+1} L{x-104} {y-29} L{x-12} {y-26}Z" fill="#f5ce91"/></g><circle cx="{x}" cy="{y-18}" r="13" fill="#4c345d" stroke="#ffe0b4" stroke-width="5"/></g>')
        elif theme == 'fairytale':
            parts.append(f'<g id="landmark-{sid}"><rect x="{x-51}" y="{y-46}" width="102" height="111" rx="4" fill="#9687b7"/><rect x="{x-74}" y="{y-70}" width="42" height="137" fill="#b4a1c5"/><rect x="{x+32}" y="{y-70}" width="42" height="137" fill="#b4a1c5"/><path d="M{x-84} {y-68} L{x-53} {y-123} L{x-22} {y-68}Z" fill="url(#roof)"/><path d="M{x+22} {y-68} L{x+53} {y-123} L{x+84} {y-68}Z" fill="url(#roof)"/><path d="M{x-25} {y-48} L{x} {y-100} L{x+25} {y-48}Z" fill="#dfbce4"/><path d="M{x-18} {y+65} V{y+10} Q{x} {y-13} {x+18} {y+10} V{y+65}Z" fill="#312944"/><rect x="{x-61}" y="{y-34}" width="15" height="25" rx="6" fill="#ffe1a5"/><rect x="{x+46}" y="{y-34}" width="15" height="25" rx="6" fill="#ffe1a5"/></g>')
        elif theme in ('custom', 'graffiti'):
            if i % 2 == 0:
                parts.append(f'<g id="landmark-{sid}"><rect x="{x-65}" y="{y-55}" width="130" height="117" rx="9" fill="#755478"/><path d="M{x-90} {y-53} L{x} {y-113} L{x+90} {y-53}Z" fill="url(#roof)"/><rect x="{x-48}" y="{y-36}" width="96" height="80" rx="5" fill="#262342"/><path d="M{x-85} {y-48} L{x-58} {y+68} M{x+85} {y-48} L{x+58} {y+68}" fill="none" stroke="#f7bb9c" stroke-width="9"/><circle cx="{x}" cy="{y-2}" r="21" fill="#a68cc3"/><rect x="{x-38}" y="{y+34}" width="76" height="13" rx="4" fill="#e7bd95"/></g>')
            else:
                parts.append(f'<g id="landmark-{sid}"><path d="M{x-77} {y+60} L{x-62} {y-39} L{x+60} {y-39} L{x+77} {y+60}Z" fill="#5c7490"/><path d="M{x-87} {y-42} Q{x} {y-138} {x+87} {y-42}Z" fill="url(#roof)"/><rect x="{x-57}" y="{y-26}" width="114" height="66" rx="8" fill="#40364f"/><circle cx="{x-28}" cy="{y+4}" r="12" fill="#e6b1ce"/><circle cx="{x+28}" cy="{y+4}" r="12" fill="#e6b1ce"/><path d="M{x-34} {y+36} Q{x} {y+6} {x+34} {y+36}" fill="none" stroke="#f9cf92" stroke-width="8"/></g>')
        elif theme == 'ocean':
            parts.append(f'<g id="landmark-{sid}"><path d="M{x-51} {y+40} Q{x-58} {y-40} {x-13} {y-49} Q{x+44} {y-65} {x+49} {y+40} Z" fill="#62aab1"/><path d="M{x-40} {y+37} Q{x-46} {y-23} {x-13} {y-29} Q{x+33} {y-40} {x+37} {y+37}Z" fill="url(#roof)" opacity=".55"/><circle cx="{x}" cy="{y-3}" r="16" fill="#1d526e"/></g>')
        else:
            parts.append(f'<g id="landmark-{sid}"><rect x="{x-42}" y="{y-43}" width="84" height="88" rx="14" fill="url(#roof)"/><path d="M{x-16} {y+42} L{x-16} {y+3} Q{x} {y-15} {x+16} {y+3} V{y+42}Z" fill="#20304a"/></g>')
    return top + ''.join(parts) + '</svg>'

ICON_PATHS = {
    'briefcase': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    'sparkles': '<path d="m12 3 1.9 6.1L20 11l-6.1 1.9L12 19l-1.9-6.1L4 11l6.1-1.9L12 3ZM19 18l.7 1.3L21 20l-1.3.7L19 22l-.7-1.3L17 20l1.3-.7L19 18Z"/>',
    'rocket': '<path d="M4 16c0-5 6-11 14-12l2 2c-1 8-7 14-12 14l-4-4Z"/><path d="m9 15-4 4M5 10H2l2-4 5-2M14 19v3l4-2 2-5"/><circle cx="15" cy="9" r="2"/>',
    'star': '<path d="m12 2 3 7 7 .5-5.5 4.6 1.7 7-6.2-3.8-6.2 3.8 1.7-7L2 9.5 9 9Z"/>',
    'book': '<path d="M12 6c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1Zm0 0v15"/>',
    'compass': '<circle cx="12" cy="12" r="9"/><path d="m15 9-2 5-5 2 2-5 5-2Z"/>',
    'quotes': '<path d="M4 11h6v9H3v-9c0-4 2-6 6-7M14 11h6v9h-7v-9c0-4 2-6 6-7"/>',
    'heart': '<path d="M20 5c-3-3-6-2-8 1-2-3-5-4-8-1-4 4 0 9 8 16 8-7 12-12 8-16Z"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-5 5-5 13 0 18M12 3c5 5 5 13 0 18"/>',
    'map': '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Zm6-3v15m6-12v15"/>',
    'list': '<path d="M9 6h12M9 12h12M9 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
    'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-5 3-8 8-8s8 3 8 8"/>',
    'close': '<path d="M5 5 19 19M19 5 5 19"/>',
    'print': '<path d="M7 8V3h10v5M7 17H4V9h16v8h-3M7 14h10v7H7v-7Z"/>',
}


def icon(name: str) -> str:
    return f'<svg class="ui-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS.get(name, ICON_PATHS["compass"])}</svg>'


DEFAULT_POINTS = [(28, 57), (70, 43), (50, 24), (49, 77), (17, 30), (82, 72), (82, 20), (17, 78)]


def entry_html(entry: dict, work_label: str = 'View project') -> str:
    title = e(entry['title'])
    subtitle = e(entry.get('subtitle') or '')
    desc = e(entry['description'])
    if entry.get('type') == 'quote':
        return f'<figure class="entry quote-entry">{icon("quotes")}<blockquote>{desc}</blockquote><figcaption>— {e(entry["attribution"])}</figcaption></figure>'
    highlights = ''.join(f'<li>{e(text)}</li>' for text in entry.get('highlights', []))
    highlights_html = f'<ul class="highlights">{highlights}</ul>' if highlights else ''
    metrics = ''.join(f'<div class="metric"><strong>{e(m["value"])}</strong><span>{e(m["label"])}</span></div>' for m in entry.get('metrics', []))
    metrics_html = f'<div class="metrics">{metrics}</div>' if metrics else ''
    tags = ''.join(f'<span class="tag">{e(t)}</span>' for t in entry.get('tags', []) if t)
    tags_html = f'<div class="tags">{tags}</div>' if tags else ''
    link_html = f'<a class="entry-link" href="{e(safe_url(entry["url"]))}" target="_blank" rel="noopener noreferrer">{e(work_label)} ↗</a>' if entry.get('url') else ''
    return f'<article class="entry"><h3>{title}</h3>{f"<p class=entry-subtitle>{subtitle}</p>" if subtitle else ""}<p class="entry-description">{desc}</p>{highlights_html}{metrics_html}{tags_html}{link_html}</article>'


def embedded_image(path: Path) -> str:
    """Embed a local raster image without network requests or extra dependencies."""
    raw = path.read_bytes()
    if len(raw) > 4_000_000:
        fail('Background image exceeds 4 MB; compress it before embedding')
    if raw.startswith(b'\x89PNG\r\n\x1a\n'):
        mime = 'image/png'
    elif raw.startswith(b'\xff\xd8\xff'):
        mime = 'image/jpeg'
    elif raw.startswith(b'RIFF') and raw[8:12] == b'WEBP':
        mime = 'image/webp'
    else:
        fail('Background image must be a valid PNG, JPEG or WebP file')
    return f'data:{mime};base64,' + base64.b64encode(raw).decode('ascii')


def generate(data: dict, background_image: str = '') -> str:
    validate_model(data)
    if data['world'].get('artwork_mode') == 'image-assisted' and not background_image:
        fail('Image-assisted world requires --background-image with a local PNG/JPEG/WebP')
    profile, world, sections = data['profile'], data['world'], data['sections']
    theme_name = world['theme']
    theme = THEMES.get(theme_name, THEMES['custom'])
    accent = safe_color(world.get('accent') or '', theme['accent'])
    secondary = safe_color(world.get('accent_secondary') or '', theme['secondary'])
    copy = world.get('copy') or {}
    def c(key: str, default: str) -> str:
        return e(copy.get(key) or default)

    list_items, dialogs, recruiter_items = [], [], []
    for index, section in enumerate(sections):
        sid = section['id']
        name = e(section['name'])
        eyebrow = e(section.get('eyebrow') or f'Chapter {index + 1:02}')
        section_icon = icon(('briefcase','sparkles','rocket','star','book','compass','globe','heart')[index])
        search_text = ' '.join([section['name'],section['intro']]+[f'{item["title"]} {item.get("description", "")} {" ".join(item.get("highlights", []))} {" ".join(item.get("tags", []))}' for item in section['entries']])
        list_items.append(f'<button type="button" class="landmark" data-dialog="detail-{e(sid)}" data-search="{e(search_text.casefold())}" aria-haspopup="dialog" aria-label="{c("open", "Explore")} {name}"><span class="landmark-icon">{section_icon}</span><span class="landmark-text"><strong>{name}</strong><small>{e(section["intro"])}</small></span><span class="landmark-arrow" aria-hidden="true">↗</span></button>')
        details = ''.join(entry_html(item, copy.get('view_work') or 'View project') for item in section['entries'])
        dialogs.append(f'<dialog class="detail-dialog" id="detail-{e(sid)}" aria-labelledby="label-{e(sid)}"><div class="dialog-inner"><header class="dialog-heading"><div><p class="eyebrow">{eyebrow}</p><h2 id="label-{e(sid)}">{name}</h2><p>{e(section["intro"])}</p></div><button type="button" class="close-dialog" aria-label="{c("close", "Close details")}">{icon("close")}</button></header><div class="entries">{details}</div></div></dialog>')
        recruiter_items.append(f'<section class="recruiter-section"><h3>{name}</h3>{details}</section>')
    links = ''.join(f'<a href="{e(safe_url(link["url"]))}" target="_blank" rel="noopener noreferrer">{e(link["label"])} ↗</a>' for link in profile.get('links', []))
    scene_source = world.get('scene_svg') or object_scene(theme_name, sections)
    label_map = {section['id']: next((p['label'] for p in world.get('landmarks', world.get('hotspots', [])) if p['section_id'] == section['id']), section['name']) for section in sections}
    scene = sanitize_scene(scene_source, section_ids=set(label_map), labels=label_map)
    scene_mobile = ''
    if world.get('scene_svg_mobile'):
        # Rendered only in a <template> until selected at runtime, ensuring
        # exactly one active scene and no duplicate landmark ids in the DOM.
        scene_mobile = '<template id="mobile-scene-template">' + sanitize_scene(world['scene_svg_mobile'], section_ids=set(label_map), labels=label_map) + '</template>'
    background = f'<img class="scene-backdrop" src="{e(background_image)}" alt="" aria-hidden="true" draggable="false">' if background_image else ''
    result = TEMPLATE.read_text(encoding='utf-8')
    replacements = {
        'TITLE':e(world['title']), 'TAGLINE':e(world['tagline']), 'DESCRIPTION':e(world.get('description') or world['tagline']),
        'SHARE_META': share_meta(world, profile),
        'PROFILE_NAME':e(profile['name']), 'PROFILE_HEADLINE':e(profile['headline']), 'PROFILE_SUMMARY':e(profile['summary']),
        'ACCENT':accent, 'ACCENT2':secondary,
        'BG':safe_background(world.get('background') or '', theme['background']),
        'BG2':safe_background(world.get('background_secondary') or '', theme['background2']),
        'THEME':e(theme_name), 'THEME_LABEL':e(world.get('visual_name') or theme['label']),
        'SCENE':scene, 'SCENE_MOBILE':scene_mobile, 'SCENE_BACKDROP':background, 'LANDMARKS':'\n'.join(list_items),
        'DIALOGS':'\n'.join(dialogs), 'RECRUITER_ENTRIES':'\n'.join(recruiter_items),
        'LINKS':links, 'COUNT':str(len(sections)), 'ENTRY_COUNT':str(sum(len(s['entries']) for s in sections)),
        'ICON_MAP':icon('map'), 'ICON_LIST':icon('list'), 'ICON_USER':icon('user'), 'ICON_PRINT':icon('print'), 'ICON_CLOSE':icon('close'),
        'COPY_EYEBROW':c('eyebrow', 'An explorable career world'),
        'COPY_EXPLORE':c('explore', 'Explore the world'), 'COPY_HINT':c('hint', 'Select a landmark to discover its story'),
        'COPY_LIST':c('list', 'All locations'), 'COPY_RECRUITER':c('recruiter', 'Recruiter view'),
        'COPY_ABOUT':c('about', 'About the creator'), 'COPY_CLOSE':c('close', 'Close'),
        'COPY_SEARCH':c('search', 'Search locations'), 'COPY_EMPTY':c('empty', 'No matching locations'),
        'COPY_MADE_WITH':c('made_with', 'Made with SimpliCITY Builder'),
        'COPY_PRIVACY':c('privacy', 'Review facts and privacy before sharing'),
        'COPY_PRINT':c('print', 'Print résumé'),
        'COPY_INTRO':c('intro', 'Discover the person behind the world'),
        'COPY_LOCATIONS':c('locations', 'Locations'),
        'COPY_SKIP':c('skip', 'Skip to locations'),
    }
    def replace(match):
        key=match.group(1)
        if key not in replacements:
            fail(f'Template has unresolved placeholder {key}')
        return replacements[key]
    return re.sub(r'%%([A-Z0-9_]+)%%', replace, result)


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate an offline SimpliCITY Builder world portfolio.')
    parser.add_argument('--input', required=True, type=Path, help='Input JSON file with verified career content')
    parser.add_argument('--output', required=True, type=Path, help='Output HTML file')
    parser.add_argument('--background-image', type=Path, help='Optional locally supplied PNG/JPEG/WebP art layer; embed offline, never fetched remotely')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        image = embedded_image(args.background_image) if args.background_image else ''
        result = generate(data, background_image=image)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
        print(f'Generated {args.output} ({len(result.encode("utf-8")):,} bytes)')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
