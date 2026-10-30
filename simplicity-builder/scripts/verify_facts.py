#!/usr/bin/env python3
"""Conservative local résumé evidence checks. Never claims semantic verification.

No network. Reports unmatched numeric values, employer names, dates, quoted
attributions and tool/skill tags; matches are evidence hints, not proof.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import unicodedata

NUMBER = re.compile(r'(?<![\w])\d[\d,]*(?:\.\d+)?\s*%?(?![\w])')


def norm(text: str) -> str:
    text = unicodedata.normalize('NFKC', text).casefold()
    return re.sub(r'[^\w%]+', ' ', text).strip()


def numeric_tokens(text: str) -> list[str]:
    return [norm(m.group()).replace(' ', '') for m in NUMBER.finditer(text)]


def evidence_gaps(data: dict, resume: str) -> list[dict]:
    evidence = norm(resume)
    evidence_nums = set(numeric_tokens(resume))
    gaps = []

    def inspect(path: str, value: str, *, exact: bool = False):
        if not isinstance(value, str) or not value.strip():
            return
        if exact and norm(value) not in evidence:
            gaps.append({'field': path, 'kind': 'named claim', 'claim': value})
        for number in numeric_tokens(value):
            # A percentage must also be a percentage in the résumé; numbers cannot
            # validate context (97% reduction vs 97% satisfaction).
            if number not in evidence_nums:
                gaps.append({'field': path, 'kind': 'number or date', 'claim': number})

    profile = data.get('profile') or {}
    for key in ('name','headline','summary'):
        inspect(f'profile.{key}',profile.get(key,''),exact=(key=='name'))
    for i, section in enumerate(data.get('sections',[])):
        # Fictional world names/landmark copy are not résumé claims.
        for j, item in enumerate(section.get('entries',[])):
            prefix=f'sections[{i}].entries[{j}]'
            for key in ('title','subtitle','description','dates'):
                inspect(f'{prefix}.{key}',item.get(key,''))
            for key in ('employer','attribution'):
                inspect(f'{prefix}.{key}',item.get(key,''),exact=True)
            for k, highlight in enumerate(item.get('highlights',[])):
                inspect(f'{prefix}.highlights[{k}]',highlight)
            for k, metric in enumerate(item.get('metrics',[])):
                inspect(f'{prefix}.metrics[{k}]',metric.get('value',''))
            for k, tag in enumerate(item.get('tags',[])):
                # Can include creative prose; flagged as a possible unsupported skill.
                if norm(tag) not in evidence:
                    gaps.append({'field':f'{prefix}.tags[{k}]','kind':'skill or tag for review','claim':tag})
    approvals = (data.get('review') or {}).get('approved_paraphrases', [])
    allowed = {(v['field'],norm(v['claim'])):v for v in approvals if isinstance(v,dict) and v.get('approved_by_owner') is True and all(k in v for k in ('field','claim','source_excerpt'))}
    unresolved = []
    for gap in gaps:
        candidate = allowed.get((gap['field'], norm(gap['claim'])))
        # No approval override for numbers, employers, dates or quote attribution.
        forbidden = gap['kind'] == 'number or date' or gap['field'].endswith(('.employer','.attribution','.dates'))
        if not forbidden and candidate and len(norm(candidate['source_excerpt'])) >= 12 and norm(candidate['source_excerpt']) in evidence:
            continue
        unresolved.append(gap)
    return unresolved


def main():
    ap=argparse.ArgumentParser(description='Check portfolio claims against extracted résumé text. Not semantic fact verification.')
    ap.add_argument('--input',required=True,type=Path)
    ap.add_argument('--resume-text',required=True,type=Path,help='Extracted résumé text, kept local/private')
    ap.add_argument('--report',type=Path,help='Optional local JSON report; do not commit')
    ap.add_argument('--strict',action='store_true',help='Fail for unmatched evidence (review false positives)')
    args=ap.parse_args()
    data=json.loads(args.input.read_text(encoding='utf-8'))
    from build_portfolio import validate_model
    validate_model(data)
    resume=args.resume_text.read_text(encoding='utf-8')
    if len(resume.strip())<60:
        ap.exit(2,'Résumé text is too short; PDF may be scanned. Request OCR or pasted text.\n')
    gaps=evidence_gaps(data,resume)
    report={'status':'review_required' if gaps else 'no_unmatched_tokens','unmatched':gaps,
            'owner_approved_paraphrases':(data.get('review') or {}).get('approved_paraphrases', []),
            'notice':'Token matching is not semantic proof. Human review is always required.'}
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    for gap in gaps:
        print(f'REVIEW {gap["field"]}: {gap["kind"]} {gap["claim"]!r}')
    print(f'{len(gaps)} claim(s) require review. Matching text does not prove accuracy.')
    if args.strict and gaps:
        ap.exit(1,'Strict mode failed: unmatched claims. Correct or document them before public release.\n')

if __name__=='__main__': main()
