#!/usr/bin/env python3
"""Build a self-contained interactive experience from host-reviewed content JSON.

This stdlib-only script does not read PDFs, interpret photographs, visit URLs or
infer facts. A capable chat host supplies source-grounded chapter data.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from build_portfolio import embedded_image, fail, generate, required, safe_url
from verify_source import evidence_issues

KINDS = {'resume', 'photo', 'document', 'link', 'prompt'}
MODES = {'world', 'explore', 'explain'}


def slug(value: str) -> str:
    result = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
    return result[:40].rstrip('-') or 'chapter'


def to_portfolio(data: dict) -> dict:
    if not isinstance(data, dict):
        fail('Experience input must be a JSON object')
    source = data.get('source')
    experience = data.get('experience')
    chapters = data.get('chapters')
    if not isinstance(source, dict) or not isinstance(experience, dict):
        raise ValueError('source and experience must be objects')
    kind = required(source, 'kind', 'source', 16)
    if kind not in KINDS:
        fail(f'source.kind must be one of: {", ".join(sorted(KINDS))}')
    source_title = required(source, 'title', 'source', 100)
    if kind == 'link':
        safe_url(required(source, 'url', 'source', 600))
    if kind != 'prompt':
        # AI host must affirm content was read; the generator cannot independently
        # verify its semantic accuracy. The source stays local.
        if source.get('reviewed_by_host') is not True:
            fail('source.reviewed_by_host must be true after host source review')
    elif source.get('fictional') is not True:
        fail('Prompt-only experiences must explicitly mark source.fictional: true')
    issues = evidence_issues(data)
    if issues:
        fail("Evidence review failed:\n- " + "\n- ".join(issues))
    title = required(experience, 'title', 'experience', 95)
    theme = required(experience, 'theme', 'experience', 180)
    mode = experience.get('mode', 'world')
    if mode not in MODES:
        fail('experience.mode must be world, explore or explain')
    if not isinstance(chapters, list) or not 1 <= len(chapters) <= 8:
        raise ValueError('chapters must contain 1–8 sections')
    sections = []
    anchors = {}
    ids = set()
    anchor_rects: list[tuple[str, float, float, float, float]] = []
    for i, chapter in enumerate(chapters):
        if not isinstance(chapter, dict):
            fail(f'chapters[{i}] must be an object')
        name = required(chapter, 'title', f'chapters[{i}]', 110)
        summary = required(chapter, 'summary', f'chapters[{i}]', 650)
        section_id = slug(chapter.get('id') or name)
        if section_id in ids:
            fail(f'Duplicate chapter ID: {section_id}')
        ids.add(section_id)
        if kind == 'photo':
            anchor = chapter.get('anchor')
            if not isinstance(anchor, dict) or set(anchor) != {'x', 'y', 'width', 'height'}:
                raise ValueError(f'chapters[{i}].anchor: photo requires an observed object box (x, y, width, height), normalized 0–1')
            if not all(isinstance(anchor[k], (int, float)) and not isinstance(anchor[k], bool) for k in anchor):
                fail(f'chapters[{i}].anchor: expected numeric coordinates')
            x, y, w, h = (anchor[k] for k in ('x', 'y', 'width', 'height'))
            if not (0 <= x < 1 and 0 <= y < 1 and 0 < w <= 1-x and 0 < h <= 1-y):
                fail(f'chapters[{i}].anchor: box must lie inside the source image')
            area = w * h
            if area < .04 or area > .90:
                fail(f'chapters[{i}].anchor: image region must cover 4%–90% of the photo (got {area:.1%})')
            for prior_id, px, py, pw, ph in anchor_rects:
                intersection = max(0, min(x+w, px+pw)-max(x,px)) * max(0, min(y+h, py+ph)-max(y,py))
                if intersection / min(area, pw*ph) > .50:
                    fail(f'chapters[{i}].anchor: region overlaps {prior_id!r} by more than 50% of the smaller region')
            anchor_rects.append((section_id,x,y,w,h))
            anchors[section_id] = {k: round(float(v), 5) for k, v in anchor.items()}
        entries = chapter.get('items')
        if not isinstance(entries, list) or not 1 <= len(entries) <= 20:
            raise ValueError(f'chapters[{i}].items must contain 1–20 items')
        normalized = []
        for j, item in enumerate(entries):
            if not isinstance(item, dict):
                fail(f'chapters[{i}].items[{j}] must be an object')
            # Factual sources require attribution to the supplied source, not
            # fabricated external citations. Host review is an explicit step.
            if kind != 'prompt' and item.get('source_grounded') is not True:
                fail(f'chapters[{i}].items[{j}] must be marked source_grounded after verification')
            entry = {
                'title': required(item, 'title', f'chapters[{i}].items[{j}]', 220),
                'description': required(item, 'description', f'chapters[{i}].items[{j}]', 2500),
            }
            for key in ('subtitle', 'url', 'dates', 'employer'):
                if key in item:
                    entry[key] = item[key]
            if 'highlights' in item:
                entry['highlights'] = item['highlights']
            if 'tags' in item:
                entry['tags'] = item['tags']
            normalized.append(entry)
        sections.append({'id': section_id, 'name': name, 'intro': summary, 'entries': normalized})
    default_taglines = {
        'world': f'Discover {source_title} through an imaginative world.',
        'explore': f'Explore the stories and details of {source_title}.',
        'explain': f'Explore the ideas behind {source_title}.',
    }
    tagline = experience.get('tagline') or default_taglines[mode]
    if not isinstance(tagline, str) or not tagline.strip():
        fail('experience.tagline must be nonempty text')
    name = data.get('creator') or 'SimpliCITY Builder'
    if not isinstance(name, str) or not name.strip():
        fail('creator must be a nonempty string')
    theme_name = slug(theme)[:60].rstrip('-')
    modes = {
        'world': {'eyebrow': 'An explorable world', 'recruiter': 'Overview', 'about': 'About', 'list': 'Locations', 'locations': 'Locations', 'print': 'Print overview', 'intro': 'Discover the source behind this world'},
        'explore': {'eyebrow': 'An interactive exhibition', 'recruiter': 'Full overview', 'about': 'About', 'list': 'Exhibits', 'locations': 'Exhibits', 'print': 'Print overview', 'intro': 'Explore the content in this exhibition'},
        'explain': {'eyebrow': 'An interactive explainer', 'recruiter': 'Full explanation', 'about': 'About', 'list': 'Topics', 'locations': 'Topics', 'print': 'Print overview', 'intro': 'Read the explanation behind this experience'},
    }
    world = {'title': title, 'theme': theme_name, 'tagline': tagline,
             'visual_name': theme[:120], 'copy': modes[mode], 'content_kind': kind,
             'experience_mode': mode}
    if anchors:
        world['photo_anchors'] = anchors
    if len(sections) == 1:
        world['copy'].update(hint='Open the featured story', list='Explore the story',
                             locations='Featured story', explore='Explore the featured story')
    if 'scene_svg' in experience:
        world['scene_svg'] = experience['scene_svg']
    if 'scene_svg_mobile' in experience:
        world['scene_svg_mobile'] = experience['scene_svg_mobile']
    if 'colors' in experience:
        colors = experience['colors']
        if not isinstance(colors, dict):
            fail('experience.colors must be an object')
        for a, b in [('accent', 'accent'), ('secondary', 'accent_secondary'), ('background', 'background'), ('background_secondary', 'background_secondary')]:
            if a in colors:
                world[b] = colors[a]
    # Explicit share URLs are optional; this does not publish or fetch anything.
    if 'share' in experience:
        world['share'] = experience['share']
    return {
        'profile': {'name': name.strip(), 'headline': source_title,
                    'summary': source.get('summary') or f'An interactive interpretation of {source_title}.', 'links': []},
        'world': world,
        'sections': sections,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description='Build an interactive world/exhibition/explainer from reviewed source content')
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source-image', type=Path, help='Optional provided, locally stored PNG/JPEG/WebP image (embedded, no upload)')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        if data.get('source', {}).get('kind') == 'photo' and not args.source_image:
            fail('Photo experiences require --source-image and source-grounded anchors')
        portfolio = to_portfolio(data)
        image = embedded_image(args.source_image) if args.source_image else ''
        result = generate(portfolio, background_image=image)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(result.encode('utf-8'))
        print(f'Generated {args.output} ({len(result.encode("utf-8")):,} bytes)')
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
