#!/usr/bin/env python3
"""Extract local TXT/DOCX/PDF résumé text for review; no AI inference or uploads.

Text and DOCX use only Python's standard library. PDF text extraction requires the
optional pypdf package; scanned PDFs require OCR or host document tools.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

MAX_INPUT_BYTES = 10 * 1024 * 1024
MAX_OUTPUT_CHARS = 160_000
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def extract_text(path: Path) -> str:
    if not path.is_file():
        raise ValueError('Resume not found. Supply a local .txt, .md, .docx, or .pdf file.')
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError('Resume exceeds 10 MB. Provide a smaller document.')
    suffix = path.suffix.lower()
    if suffix in ('.txt', '.md'):
        text = path.read_text(encoding='utf-8-sig')
    elif suffix == '.docx':
        try:
            with zipfile.ZipFile(path) as bundle:
                if sum(member.file_size for member in bundle.infolist()) > 40_000_000:
                    raise ValueError('DOCX contents are unexpectedly large')
                content = bundle.read('word/document.xml')
            if b'<!DOCTYPE' in content or b'<!ENTITY' in content:
                raise ValueError('DOCX contains unsupported XML declarations')
            root = ET.fromstring(content)
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
            raise ValueError(f'Cannot read DOCX content: {exc}') from exc
        paragraphs = []
        for p in root.iter(f'{{{W_NS}}}p'):
            parts = [n.text or '' for n in p.iter(f'{{{W_NS}}}t')]
            if ''.join(parts).strip():
                paragraphs.append(''.join(parts))
        text = '\n'.join(paragraphs)
    elif suffix == '.pdf':
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError('PDF extraction requires pypdf. Run: python3 -m pip install pypdf') from exc
        try:
            reader = PdfReader(str(path))
            if reader.is_encrypted:
                raise ValueError('Encrypted PDF: provide an unlocked copy or paste résumé text')
            if len(reader.pages) > 25:
                raise ValueError('PDF is longer than 25 pages; supply a shorter résumé')
            text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError(f'PDF text extraction failed: {exc}') from exc
    else:
        raise ValueError('Unsupported résumé format. Use .txt, .md, .docx, or .pdf')
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'\n{4,}', '\n\n\n', text).strip()
    if len(text) > MAX_OUTPUT_CHARS:
        raise ValueError('Extracted résumé exceeds 160,000 characters; trim it first')
    if len(text) < 50:
        raise ValueError('Too little selectable text found. A scanned PDF may need OCR, or paste résumé text into a .txt file.')
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract local résumé text without uploads or AI hallucination.')
    parser.add_argument('resume', type=Path)
    parser.add_argument('--output', type=Path, default=Path('private/resume-extracted.txt'))
    args = parser.parse_args()
    try:
        if args.output.resolve() == args.resume.resolve():
            raise ValueError('Output must differ from input')
        text = extract_text(args.resume)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
        print(f'Extracted {len(text)} characters to {args.output}.')
        print('PRIVATE: Review locally. Do not commit, publish, or paste private contact details into public issues.')
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
