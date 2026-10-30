# Résumé extraction and factual review

**Important:** Text extraction is not résumé *understanding*. The agent must still structure and verify the facts. Never invent job titles, employers, degrees, dates, metrics, projects or links.

## Obtain source text

- If the host can read attached PDF or DOCX files, use its native extraction first and verify no pages were missed.
- If the host cannot extract reliably but has file execution, use the bundled local tool:

```bash
python3 simplicity-builder/scripts/extract_resume.py resume.docx --output private/resume-extracted.txt
python3 -m pip install pypdf  # only if you need to extract a text-based PDF
python3 simplicity-builder/scripts/extract_resume.py resume.pdf --output private/resume-extracted.txt
```

- `.txt`, `.md`, and `.docx` extraction is Python-standard-library only. PDF needs optional `pypdf`. Scanned/image-only PDFs require OCR or pasted text; do not pretend they were parsed.
- Do not output the extracted full résumé to logs or commit it. `private/` is gitignored. The original file and extracted text stay local unless the user intentionally shares them with an AI host.

## Evidence-first field mapping

1. Build a private fact inventory: identity, verified headline, professional summary, role/employer/date pairs, projects/outcomes, skills, education/certifications, user-approved links. Preserve dates and employer names exactly when possible.
2. Identify missing or contradictory facts. Mark as **needs review** privately; never fabricate to fill empty sections.
3. Create 1–8 coherent *portfolio sections* from the evidence. If there are more than eight content categories, combine related categories instead of discarding verified work. Split dense roles into multiple entries when useful. Each section can have up to 20 entries, and each description up to 2,500 characters.
4. Thematic names are fiction; descriptions must preserve real-world meaning. Example: a castle could represent a verified role, but never invent a company, promotion or quantified result.
5. Keep address, phone, personal email and unapproved links off the generated public HTML. If the résumé includes them, omit them from the website unless the user explicitly chooses to publish them.
6. Before returning the generated portfolio, compare every career claim and link with the extracted résumé. Provide a brief **private review note** with omitted/uncertain fields and ask the user to approve before public deployment.
7. Validate schema, artwork and generated HTML, and do a browser check where available. If you could not test visually, disclose that limitation.

The generator intentionally does not call an LLM or run résumé-to-JSON extraction automatically: evidence interpretation happens in the chosen AI host and requires factual verification.

## Owner-approved paraphrases (v0.1.4)

An exact-token check can reject a safe paraphrase even when it is accurately supported. For carefully reviewed *nonnumeric, non-employer, non-date, non-attribution* wording, optional `review.approved_paraphrases` can record an explicit owner decision with source evidence. Each record has `field` (e.g. `sections[0].entries[0].tags[0]`), `claim` (exact text), `source_excerpt` (verbatim excerpt found in résumé text), and `approved_by_owner: true`. The verifier accepts the record only when the supporting excerpt exists. It will never override unmatched numbers, dates, employer names or testimonial attributions. This is an audit trail, not semantic proof. Keep the review JSON and extracted résumé private.
