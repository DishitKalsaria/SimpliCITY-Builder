# Source-neutral interactive experience JSON — v0.2.0

A coding-capable AI host reads and interprets the user's input, then writes this structured, source-grounded file. **The Python generator itself cannot understand a photo, retrieve a web link, extract arbitrary PDFs, or verify semantic claims.** Never turn missing source content into fabricated claims.

## Input contract

- `source.kind`: `resume`, `photo`, `document`, `link` or `prompt`.
- `source.title`: nonempty descriptive title. `source.summary` is optional.
- `source.reviewed_by_host: true` for non-fiction sources after the agent actually reads them. This flag records a review claim; it is **not cryptographic or semantic verification**. Every non-fiction item also requires `source_grounded: true` and an `evidence_excerpt` (at least 15 normalized characters) describing the exact source passage or an observable detail for a photograph. This excerpt is **not** embedded in the public HTML. Supply `--source-text /private/extracted.txt` to match excerpts against locally extracted document/link text. Numeric claims must appear in item evidence; the tool cannot establish semantic accuracy or the truthfulness of an agent-supplied excerpt.
- `source.url`: an absolute HTTP(S) URL for `kind: "link"`; the generator **never fetches it**.
- `source.fictional: true` is required for `kind: "prompt"`. Fictional source items must not be presented as genuine evidence.
- **Photo mode:** `source.kind: "photo"` requires the supplied original image (`--source-image /path/to/photo.png`) and one `chapter.anchor` per chapter: `{"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.25}`. These are normalized 0–1 bounding boxes of **objects actually visible in the photo**. The host must inspect the real image and locate each object before writing the JSON; no invented objects. The builder refuses photo builds without the image/anchors, uses that photo rather than procedural scenery, and aligns hotspots to the image on all viewports. On portrait phones, the real image uses a context-preserving crop that covers at least about 64% of the stage height, with blurred margins; accessible Previous / Next object and Fit photo controls navigate/zoom without page scrolling. Photo box areas must be 4%–90% of the source image and may not overlap more than 50% of the smaller region. Preserve original photography, permissions and source accuracy. Photo test images are expressly fictional synthetic fixtures, not real user photos. No automatic image-recognition model is bundled.
- `experience.title`, `experience.theme` (free-form creative direction), optional `tagline`, `mode` (`world`, `explore`, `explain`), optional safe `scene_svg` and `scene_svg_mobile`, `colors`, and `share`.
- `chapters`: 1–8 items with a `title`, `summary`, and 1–20 `items` containing `title`, `description`, and for non-fiction `evidence_excerpt`. An item may include `subtitle`, `highlights`, `tags`, `url`, `dates` or `employer` when supported by the source.
- `creator`: optional short public display name; omit private contact details by default.

## Example (all content fictional)

```json
{
  "source": {"kind": "prompt", "title": "A fictional superhero academy", "fictional": true},
  "experience": {"title": "Guardian Academy", "theme": "colorful superhero command center", "mode": "world"},
  "chapters": [
    {"title": "Training Arena", "summary": "Meet the fictional guardians.",
     "items": [{"title": "Team Training", "description": "Fictional guardians practice teamwork here."}]}
  ]
}
```

See `references/experience-sample.json` for a multi-chapter fictional document test and `examples/photo-sample.json` and `examples/link-sample.json` for **synthetic fixtures only**, not proof of live source-reading capabilities. Photo inputs need an image-capable host and **must embed** the approved source image with `--source-image`; the host must provide object anchors for each chapter. Without those inputs, building stops instead of displaying generic art. Never invent identities or context for people in photographs. A website URL requires an agent capable of retrieving the page with appropriate authorization; do not bypass access controls. Use attribution and copyright-conscious summaries rather than copying articles wholesale.

## Photo privacy and evidence

Before a photo is embedded, the stdlib sanitizer strips JPEG APP1/APP13, PNG eXIf/text and WebP EXIF/XMP metadata while preserving encoded image pixels. With optional Pillow installed, source images with a long side above 2000 pixels are downsized. Images above about 4 MB raise a warning when Pillow is unavailable; sanitized images over 10 MB, or complete HTML over 16 MB, are rejected. **Review visible faces and locations even when metadata is gone.**

For private factual review, use `--review-sheet /path/to/private/review.md` and `--source-text /path/to/private/extracted.txt` when available; never publish either private file. Passing mechanical checks does not establish factual correctness.

## Commands (inside the installed skill folder)

```bash
python3 scripts/build.py --input /path/to/experience.json --output /path/to/index.html
python3 scripts/check.py /path/to/experience.json /path/to/index.html
python3 scripts/build.py --input /path/to/experience.json --output /path/to/index.html --theme "noir mystery" --review-sheet /path/to/private/review.md
# Required for photo mode; optional for other source kinds (never fetched by the generator):
python3 scripts/build.py --input /path/to/experience.json --source-image /path/to/photo.jpg --output /path/to/index.html
```

Legacy résumé-based `profile/world/sections` JSON remains supported by the same `scripts/build.py` dispatcher. The old script names still work for existing integrations. Both produce the same offline HTML interface and safe SVG rules. Automated evidence coverage checks are part of the required build; semantic human review, image-generated illustrations, browser screenshots and publishing are separate optional passes, not prerequisites for basic HTML output.

**Photo anchor review:** Normalized rectangles can enclose unrelated sky, miss part of an object or include overlapping scenery even when they pass geometry validation. Check the intended region visually against the source photo. On cropped phone screens the focused object has the visible name plaque; use Previous/Next or the location list for the other named regions.
