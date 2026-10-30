#!/usr/bin/env python3
"""Generate a standalone interactive world portfolio from grounded JSON (stdlib only)."""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'assets' / 'template.html'

THEMES = {
    'fairytale': {'background': '#100d20', 'background2': '#291e3e', 'accent': '#f6cd8e', 'secondary': '#c4a7f8', 'icon': '🏰', 'label': 'The enchanted realm'},
    'space': {'background': '#070c20', 'background2': '#171d46', 'accent': '#9de6ff', 'secondary': '#bf96ff', 'icon': '🪐', 'label': 'The cosmic realm'},
    'graffiti': {'background': '#16111c', 'background2': '#302034', 'accent': '#ffb073', 'secondary': '#80ebd9', 'icon': '🎨', 'label': 'The creative realm'},
    'ocean': {'background': '#061c27', 'background2': '#103b52', 'accent': '#9beade', 'secondary': '#a4caff', 'icon': '🐚', 'label': 'The underwater realm'},
    'custom': {'background': '#101522', 'background2': '#222d43', 'accent': '#f3cf9e', 'secondary': '#a7c8ef', 'icon': '🗺️', 'label': 'The imagined realm'},
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
    for field in ('name', 'headline', 'summary'):
        required(profile, field, 'profile')
    for field in ('title', 'tagline', 'theme'):
        required(world, field, 'world')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', world['theme']):
        fail('world.theme must be a lowercase hyphenated identifier (any setting is allowed)')
    for field in ('description', 'symbol', 'accent', 'accent_secondary', 'background', 'background_secondary', 'visual_name'):
        optional(world, field, 'world')
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
    return data


# Optional original hero illustration for truly open-ended prompts. SVG is parsed and
# re-serialized through a strict allowlist; scripts, links, CSS and external resources
# are not accepted. This artwork is decorative; career facts remain HTML text.
SVG_TAGS = {'svg', 'defs', 'linearGradient', 'radialGradient', 'stop',
            'g', 'circle', 'ellipse', 'rect', 'line', 'path', 'polygon', 'polyline'}
SVG_COMMON = {'transform', 'opacity', 'fill', 'stroke', 'stroke-width',
              'stroke-linecap', 'stroke-linejoin'}
SVG_GEOMETRY = {
    'svg': {'viewBox'}, 'defs': set(),
    'linearGradient': {'id', 'x1', 'y1', 'x2', 'y2'},
    'radialGradient': {'id', 'cx', 'cy', 'r', 'fx', 'fy'},
    'stop': {'offset', 'stop-color', 'stop-opacity'},
    'g': SVG_COMMON,
    'circle': {'cx', 'cy', 'r'} | SVG_COMMON,
    'ellipse': {'cx', 'cy', 'rx', 'ry'} | SVG_COMMON,
    'rect': {'x', 'y', 'width', 'height', 'rx', 'ry'} | SVG_COMMON,
    'line': {'x1', 'y1', 'x2', 'y2'} | SVG_COMMON,
    'path': {'d'} | SVG_COMMON,
    'polygon': {'points'} | SVG_COMMON,
    'polyline': {'points'} | SVG_COMMON,
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


def sanitize_scene(markup: str) -> str:
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
                if not SVG_ID.fullmatch(val) or val in gradient_ids:
                    fail(f'world.scene_svg: invalid or duplicate gradient id {val!r}')
                gradient_ids.add(val)
            if key == 'viewBox' and val != '0 0 620 520':
                fail('world.scene_svg: viewBox must be 0 0 620 520')
            if key == 'd' and not SVG_PATH.fullmatch(val):
                fail('world.scene_svg: invalid path data')
            if key == 'points' and not re.fullmatch(r'[0-9eE+.,\s-]{1,3500}', val):
                fail('world.scene_svg: invalid points')
            if key == 'transform' and not SVG_TRANSFORM.fullmatch(val):
                fail('world.scene_svg: invalid transform; use translate, rotate, scale, matrix or skewX/skewY')
            if key == 'stroke-linecap' and val not in {'round', 'square', 'butt'}:
                fail('world.scene_svg: stroke-linecap must be round, square or butt')
            if key == 'stroke-linejoin' and val not in {'round', 'bevel', 'miter'}:
                fail('world.scene_svg: stroke-linejoin must be round, bevel or miter')
            pieces.append(f' {key}="{e(val)}"')
        return f'<{tag}{"".join(pieces)}>' + ''.join(clean(child, tag) for child in node) + f'</{tag}>'

    interior = ''.join(clean(child, 'svg') for child in root)
    missing = gradient_refs - gradient_ids
    if missing:
        fail(f'world.scene_svg: paint refers to undefined gradient id(s): {", ".join(sorted(missing))}')
    return '<svg class="scene-svg" viewBox="0 0 620 520" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">' + interior + '</svg>'


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


def entry_html(entry: dict) -> str:
    tags = entry.get('tags', [])
    tags_html = ''.join(f'<span class="tag">{e(tag)}</span>' for tag in tags if tag)
    subtitle = f'<p class="entry-subtitle">{e(entry["subtitle"])}</p>' if entry.get('subtitle') else ''
    link_html = ''
    if entry.get('url'):
        href = e(safe_url(entry['url']))
        link_html = f'<a class="entry-link" href="{href}" target="_blank" rel="noopener noreferrer">Visit project <span aria-hidden="true">↗</span></a>'
    return f'''<article class="entry"><div class="entry-top"><h4>{e(entry['title'])}</h4>{subtitle}</div>
      <p>{e(entry['description'])}</p><div class="tags">{tags_html}</div>{link_html}</article>'''


def generate(data: dict) -> str:
    validate_model(data)
    profile, world, sections = data['profile'], data['world'], data['sections']
    theme_name = world['theme']
    theme = THEMES.get(theme_name, THEMES['custom'])
    accent = safe_color(world.get('accent') or '', theme['accent'])
    secondary = safe_color(world.get('accent_secondary') or '', theme['secondary'])
    symbol = world.get('symbol') or theme['icon']
    links_html = ''.join(f'<a class="social" href="{e(link["url"])}" target="_blank" rel="noopener noreferrer">{e(link["label"])} <span aria-hidden="true">↗</span></a>' for link in profile.get('links', []))
    nodes = []
    dialogs = []
    for i, section in enumerate(sections):
        sid = section['id']
        glyph = section.get('symbol') or ('✦', '✧', '✺', '◈', '◆', '✷', '⬡', '✹')[i]
        eyebrow = section.get('eyebrow') or f'Chapter {i + 1:02}'
        search_text = ' '.join([section['name'], section['intro']] + [f'{item["title"]} {item.get("subtitle", "")} {item["description"]} {" ".join(item.get("tags", []))}' for item in section['entries']])
        nodes.append(f'''<button class="landmark" type="button" data-dialog="detail-{e(sid)}" data-search="{e(search_text.casefold())}" aria-haspopup="dialog" aria-label="Explore {e(section['name'])}">
            <span class="landmark-top"><span class="landmark-number">{i+1:02}</span><span class="landmark-glyph" aria-hidden="true">{e(glyph)}</span></span>
            <span class="landmark-eyebrow">{e(eyebrow)}</span>
            <span class="landmark-name">{e(section['name'])}</span>
            <span class="landmark-description">{e(section['intro'])}</span>
            <span class="landmark-bottom"><span>{len(section['entries'])} {'story' if len(section['entries']) == 1 else 'stories'}</span><span class="view-arrow" aria-hidden="true">↗</span></span>
          </button>''')
        dialogs.append(f'''<dialog id="detail-{e(sid)}" class="detail-dialog" aria-labelledby="title-{e(sid)}">
          <div class="dialog-inner"><div class="dialog-heading"><div><p class="eyebrow">{e(eyebrow)}</p><h3 id="title-{e(sid)}">{e(glyph)} {e(section['name'])}</h3><p class="dialog-intro">{e(section['intro'])}</p></div><button type="button" class="close-dialog" aria-label="Close details">✕</button></div>
          <div class="entries">{''.join(entry_html(item) for item in section['entries'])}</div><p class="dialog-footer">Part of {e(world['title'])}</p></div></dialog>''')
    result = TEMPLATE.read_text(encoding='utf-8')
    replacements = {
        'TITLE': e(world['title']), 'TAGLINE': e(world['tagline']), 'DESCRIPTION': e(world.get('description') or world['tagline']),
        'PROFILE_NAME': e(profile['name']), 'PROFILE_HEADLINE': e(profile['headline']), 'PROFILE_SUMMARY': e(profile['summary']),
        'ACCENT': accent, 'ACCENT2': secondary, 'BG': safe_background(world.get('background') or '', theme['background']), 'BG2': safe_background(world.get('background_secondary') or '', theme['background2']),
        'THEME': e(theme_name), 'THEME_LABEL': e(world.get('visual_name') or theme['label']), 'WORLD_SYMBOL': e(symbol),
        'LINKS': links_html, 'SCENE': sanitize_scene(world['scene_svg']) if world.get('scene_svg') else scene_svg(theme_name if theme_name in THEMES else 'custom'), 'LANDMARKS': '\n'.join(nodes), 'DIALOGS': '\n'.join(dialogs),
        'SECTION_COUNT': str(len(sections)), 'ENTRY_COUNT': str(sum(len(section['entries']) for section in sections)),
    }
    # Single-pass replacement: user-provided text cannot become a template directive.
    def replace_placeholder(match):
        key = match.group(1)
        if key not in replacements:
            fail(f'Template has unresolved placeholder {key}')
        return replacements[key]
    result = re.sub(r'%%([A-Z0-9_]+)%%', replace_placeholder, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate an offline SimpliCITY Builder world portfolio.')
    parser.add_argument('--input', required=True, type=Path, help='Input JSON file with verified career content')
    parser.add_argument('--output', required=True, type=Path, help='Output HTML file')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        result = generate(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding='utf-8')
        print(f'Generated {args.output} ({len(result.encode("utf-8")):,} bytes)')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
