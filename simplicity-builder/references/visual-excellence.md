# Visual Excellence — SimpliCITY Builder v0.2.1

## Primary goal

The first screen should make the owner want to share their world. Environment
coherence, recognisable clickable architecture, atmospheric depth, lighting,
legible callouts, and a purposeful phone layout come before adding more features.
A working page is not automatically a visually excellent page.

## Mode A — cinematic procedural SVG (offline fallback)

`scripts/scene_art.py` uses authored environment grammars, silhouettes,
architectural platforms, connecting routes, atmospheric lighting, and distinct
portrait placement for volcanic, guardian, space, nature, ocean, museum,
technology, fantasy, festival, desert, noir, and invented subjects. The same engine now supports interior meeting rooms, playgrounds and farms with setting-specific objects; it does not place fantasy towers inside a boardroom.

- Respect the *requested art direction* before unrelated nouns in the story.
- Let one place become the hero; keep smaller destinations distinct and readable.
- Ground structures on terrain. Avoid floating pins, generic repeated badges,
  detached plaques or empty areas on phones.
- Use strong broad forms before micro-detail. Vector illustration may still
  look flatter than a cinematic generated image; do not overstate its fidelity.

## Mode B — approved scenic image with authored interactive SVGs

Where the host supports original image generation, generate an environment-only
PNG/JPEG/WebP. It must **not** contain text, logos, UI, people, personal metrics,
or claims. Save it as a local approved asset; do not use remote image URLs.

For a source-neutral input, set `experience.scene_svg` and
`experience.scene_svg_mobile`, or for a legacy résumé input set
`world.scene_svg` and `world.scene_svg_mobile`. Both SVGs must contain real
clickable landmarks whose `id="landmark-..."` values match section/chapter IDs
and whose positions visually correspond to **actual structures in the art**.
The image is independent decorative scenery; all factual information remains
in validated HTML dialogs. The generator cannot infer suitable anchor locations
from an image or verify semantic correspondence.

Then run:

```bash
python3 scripts/build.py --input /path/to/content.json \
  --scenic-image /path/to/approved-environment.png \
  --output /path/to/index.html
python3 scripts/check.py /path/to/content.json /path/to/index.html
```

The builder fails closed when desktop or mobile SVG is missing, and refuses to
combine `--scenic-image` with `--theme` (a visual re-theme invalidates geometry)
or with `--source-image` (source photos require observed photo-object anchors).
The image is sanitized and embedded for offline use, with the environment
full-bleed rather than subjected to the source-photo pan/fit algorithm.

Do not copy bounding boxes from a reference or claim semantic image alignment
until you actually inspect the rendered image at desktop and mobile sizes. Photo
mode retains its separate, stricter `--source-image` and observed anchors path.

## Visual acceptance checks

1. **First impression:** artwork immediately communicates the requested theme.
2. **Spatial integration:** structures sit in a coherent environment rather
   than resembling pasted-on icons.
3. **Composition:** a main focal area and clear paths to secondary destinations.
4. **Alignment:** labels belong to the correct clickable objects; scenic-mode
   custom geometry is inspected against actual pixels.
5. **Responsive identity:** desktop, 390×844, 320×568, compact and landscape
   preserve recognizable art, without inaccessible or clipped landmarks.
6. **Truth and accessibility:** claims remain source-grounded; keyboard, touch,
   list and tour access work without the background illustration.

Run `scripts/browser_smoke.py` on each output when Chromium is available. Review
screenshots yourself; automatic geometry, contrast and screenshot tolerance
checks are necessary but not sufficient for visual acceptance.


See `scene-authoring.md` for the AI-first SVG contract, original family art directions and required browser review.

## Environment-first quality contract (v0.2.1)

A world is any explorable environment, not necessarily a city or landscape.
In a meeting room, clickable content belongs on furnishings (screen, table,
whiteboard, laptop). In a playground, it belongs on play equipment. On a farm,
it belongs on agricultural structures, machinery and crop zones.

Avoid falling back to cloned castles or freestanding pins merely because the
prompt is unfamiliar. The host should plan actual objects and their spatial
relationships; compose desktop and portrait art independently; align landmarks
with the depicted objects; inspect the result in Chromium; and reject scenes
with detached plaques, clipped objects, unreadable targets or off-screen areas.
The generator supplies deterministic offline object families, not semantic
understanding of every possible scene. Truly unfamiliar compositions still need
host-authored art and a visual quality review.

To test matrix layouts with 1–8 chapters run
`python3 scripts/check_environment_matrix.py` (optional Chromium/Playwright).
