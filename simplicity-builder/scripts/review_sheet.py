"""Generate an explicitly private, source-aware review checklist (never in HTML)."""
from __future__ import annotations

import json
from pathlib import Path

from verify_source import evidence_issues, numbers
from verify_facts import evidence_gaps


def make_review_sheet(data: dict, source_text: str | None = None) -> str:
    lines = [
        '# PRIVATE REVIEW — DO NOT PUBLISH',
        '',
        'Passing automated checks does NOT prove factual correctness.',
        'Inspect source attribution, dates, numbers, identity, faces, locations and personal information.',
        'Keep this review sheet and extracted source text outside public site folders.',
        '',
    ]
    if 'chapters' in data:
        lines.append('## Source-neutral experience')
        lines.append(f'Source: {data.get("source", {}).get("title", "Unknown")}')
        for idx, chapter in enumerate(data['chapters']):
            lines.extend(['', f'### Chapter {idx+1}: {chapter.get("title", "Untitled")}',
                          f'Summary: {chapter.get("summary", "")}'])
            if chapter.get('anchor'):
                lines.append(f'Image anchor (normalized): {json.dumps(chapter["anchor"], sort_keys=True)}')
            for j, item in enumerate(chapter.get('items', [])):
                claim=' '.join(str(item.get(k,'')) for k in ('title','description','dates','subtitle','employer'))
                evidence=item.get('evidence_excerpt', '(missing)')
                lines.extend([f'- Item {j+1}: {item.get("title", "Untitled")}',
                              f'  Claim: {claim}', f'  Evidence or observation: {evidence}',
                              f'  Claim numbers/dates: {", ".join(sorted(numbers(claim))) or "none"}',
                              f'  Evidence numbers/dates: {", ".join(sorted(numbers(str(evidence)))) or "none"}',
                              '  Open questions: [ ] Verify semantic accuracy and consent'])
        issues=evidence_issues(data, source_text)
    else:
        lines.append('## Résumé portfolio')
        lines.append(f'Profile: {data.get("profile",{}).get("name", "Unknown")}')
        for section in data.get('sections', []):
            lines.extend(['', f'### Section: {section.get("name", "Untitled")}', f'Summary: {section.get("intro","")}'])
            for item in section.get('entries', []):
                claim=' '.join(str(item.get(k,'')) for k in ('title','description','dates','employer','subtitle'))
                lines.extend([f'- Item: {item.get("title", "Untitled")}',f'  Claim: {claim}',
                              f'  Numbers/dates: {", ".join(sorted(numbers(claim))) or "none"}',
                              '  Evidence: compare against private résumé text',
                              '  Open questions: [ ] Check employment, dates, credentials and personal details'])
        issues = [str(x) for x in evidence_gaps(data,source_text)] if source_text is not None else []
    lines.extend(['', '## Automated evidence flags'])
    lines.extend([f'- {issue}' for issue in issues] or ['- No mechanical issues found. This is NOT a truth certificate.'])
    lines.extend(['', '## Owner review', '- [ ] Every claim independently reviewed',
                  '- [ ] Photo faces/locations/metadata reviewed',
                  '- [ ] Contact details and public links approved',
                  '- [ ] Publication explicitly approved (not implied)', ''])
    return '\n'.join(lines)


def save_private_sheet(path: Path, data: dict, source_text: str | None = None) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(make_review_sheet(data, source_text), encoding='utf-8')
    try:
        path.chmod(0o600)
    except OSError:
        pass
