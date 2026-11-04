#!/usr/bin/env python3
"""One chat-first CLI for both supported JSON formats (stdlib only)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_experience import to_portfolio
from build_portfolio import embedded_image, generate, validate_model
from check import detect_schema, check
from review_sheet import save_private_sheet


def main() -> None:
    parser = argparse.ArgumentParser(description='Build and validate a standalone interactive HTML experience')
    parser.add_argument('--input', required=True, type=Path, help='Legacy résumé or source-neutral experience JSON')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--scenic-image', type=Path, help='Optional approved AI scenic image; requires authored desktop and mobile landmark SVGs')
    parser.add_argument('--source-image', '--background-image', dest='image', type=Path,
                        help='Optional approved local PNG/JPEG/WebP to embed offline')
    parser.add_argument('--source-text', type=Path, help='Optional private extracted source text for evidence cross-checking')
    parser.add_argument('--review-sheet', type=Path, help='Write private factual review checklist outside the public HTML')
    parser.add_argument('--theme', help='Re-render with another visual theme; does not alter verified source content')
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        schema = detect_schema(data)
        if schema == 'experience':
            if data.get('source', {}).get('kind') == 'photo' and not args.image:
                raise ValueError('Photo experiences require --source-image and an observed anchor on each chapter; cannot invent image objects')
            portfolio = to_portfolio(data)
        else:
            validate_model(data)
            portfolio = data
        if args.scenic_image:
            if args.image:
                raise ValueError('Choose --scenic-image or --source-image, not both')
            if portfolio['world'].get('content_kind') == 'photo':
                raise ValueError('Photo source images must use --source-image and observed anchors')
            if not portfolio['world'].get('scene_svg') or not portfolio['world'].get('scene_svg_mobile'):
                raise ValueError('--scenic-image requires authored scene_svg and scene_svg_mobile, aligned to the approved image')
            portfolio['world']['artwork_mode'] = 'image-assisted'
        if args.theme and args.scenic_image:
            raise ValueError('--theme cannot override authored scenic-image landmarks; re-author aligned SVGs first')
        if args.theme:
            import re
            new_theme = re.sub(r'[^a-z0-9]+', '-', args.theme.lower()).strip('-')[:60].rstrip('-')
            if not new_theme:
                raise ValueError('--theme must name an art direction')
            portfolio['world']['theme'] = new_theme
            portfolio['world']['visual_name'] = args.theme[:120]
            for key in ('accent', 'accent_secondary','background','background_secondary','scene_svg','scene_svg_mobile'):
                portfolio['world'].pop(key,None)
            # An explicit theme override recomposes the art, never changes factual items.
        # Read and check private evidence *before* writing the public HTML.
        check(args.input, source_text=args.source_text)
        if args.review_sheet:
            if args.review_sheet.resolve() == args.output.resolve():
                raise ValueError('--review-sheet must be distinct from public HTML')
            if 'docs' in args.review_sheet.parts or args.review_sheet.name == 'index.html':
                raise ValueError('Keep --review-sheet in a private folder, not a public docs/ directory')
            source_text_content = args.source_text.read_text(encoding='utf-8') if args.source_text else None
            save_private_sheet(args.review_sheet, data, source_text_content)
        image_path = args.scenic_image or args.image
        image = embedded_image(image_path) if image_path else ''
        html = generate(portfolio, background_image=image)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(html.encode('utf-8'))
        check(args.input, args.output, args.source_text)
        print(f'PASS Built and validated {schema} HTML: {args.output}')
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
