#!/usr/bin/env python3
"""Local, conservative evidence checks for non-résumé experiences.

The source-reading AI host supplies per-item excerpts (or visible observations
for photos). This code checks coverage and numeric consistency; it cannot prove
that the source was understood or that supplied excerpts are authentic. No I/O
or network traffic occurs in this module.
"""
from __future__ import annotations

import re
import unicodedata

NUMBER = re.compile(r'(?<![\w])\d[\d,]*(?:\.\d+)?\s*%?(?![\w])')


def normalize(value: str) -> str:
    text = unicodedata.normalize('NFKC', value).casefold()
    return re.sub(r'[^\w%]+', ' ', text).strip()


def numbers(value: str) -> set[str]:
    return {normalize(m.group()).replace(' ', '') for m in NUMBER.finditer(value)}


def evidence_issues(data: dict, source_text: str | None = None) -> list[str]:
    """Return source-grounding issues. Reject missing evidence, not creative titles."""
    source = data.get('source', {})
    if not isinstance(source, dict) or source.get('kind') == 'prompt':
        return []
    kind = source.get('kind')
    if kind not in {'resume', 'document', 'link', 'photo'}:
        return []  # Formal schema validation reports unknown kinds.
    issues = []
    source_normalized = normalize(source_text) if source_text is not None else None
    for i, chapter in enumerate(data.get('chapters', [])):
        if not isinstance(chapter, dict):
            continue
        chapter_evidence = []
        for j, item in enumerate(chapter.get('items', [])):
            if not isinstance(item, dict):
                continue
            path = f'chapters[{i}].items[{j}]'
            excerpt = item.get('evidence_excerpt', '')
            if not isinstance(excerpt, str) or len(normalize(excerpt)) < 15:
                issues.append(f'{path}.evidence_excerpt: provide at least 15 characters of source evidence or photo observations')
                continue
            chapter_evidence.append(excerpt)
            if source_normalized is not None and normalize(excerpt) not in source_normalized:
                issues.append(f'{path}.evidence_excerpt: excerpt not found in locally supplied source text')
            claims = ' '.join(str(item.get(field, '')) for field in ('title', 'description', 'subtitle', 'dates', 'employer'))
            claims += ' ' + ' '.join(str(h) for h in item.get('highlights', []))
            unsupported = numbers(claims) - numbers(excerpt)
            if unsupported:
                issues.append(f'{path}: numbers/dates not grounded by item evidence: {", ".join(sorted(unsupported))}')
        summary_nums = numbers(str(chapter.get('summary', '')))
        missing = summary_nums - numbers(' '.join(chapter_evidence))
        if missing:
            issues.append(f'chapters[{i}].summary: numbers/dates missing from chapter evidence: {", ".join(sorted(missing))}')
    return issues
