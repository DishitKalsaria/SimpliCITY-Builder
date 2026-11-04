# Art direction — SimpliCITY Builder v0.2.1

**Do not begin by drawing disconnected SVG shapes.** Prepare a compact internal plan first, then build the interactive scene. Any user-defined world (saloon, fantasy, underwater, space, graffiti, original hybrid) is valid.

## Six-part art brief (before making artwork)

1. **Setting and visual metaphor:** one sentence describing the world's physical place and how career chapters relate.
2. **Focal hierarchy:** one unmistakable primary destination, one or two secondary landmarks, and atmospheric supporting details that do not steal clicks.
3. **Layering:** distinct far background, midground, interactive objects, foreground details. Do not paint the foreground over a landmark's click area.
4. **Palette and lighting:** 3–5 cohesive colors, an intentional light direction, softened shadow contrast, gradients for volume, accessible text outside art.
5. **Landmarks:** one original named *object* per section, each made from a recognizably different silhouette. Use grouping, depth and meaningful context; no icon pins.
6. **Desktop AND mobile:** check the 620 × 520 desktop scene; on phones use a recomposed scene (portrait `0 0 620 880` is supported) when better suited. Mobile version must include *all* named landmarks with the same section IDs. Never hide résumé sections on mobile.

Use optional `assets/art-kit/` samples as composable primitives, not fixed themes. Layer larger coherent objects before adding highlights and tiny embellishments. Avoid excessive path/shape counts that create scattered compositions. Scenes should communicate a place, not icons sprinkled on a canvas.

## Optional image-assisted artwork

Only when the host offers image-generation or the user supplies a suitable image. Generate or use an **original** raster background with no career text embedded. Leave room for the named interactive SVG objects. The background is NOT clickable. Embed a local PNG/JPEG/WebP (4MB maximum) using `--background-image`. The generator embeds the image as a data URL, so the HTML works without network access. Keep the SVG landmarks on top, so they remain navigable, searchable, keyboard-operable, and visible at mobile sizes. Set `world.artwork_mode` to `image-assisted`; do not request this mode unless the image file is available.

For mobile, bespoke SVG can use a separate mobile composition, and procedural scenes generate one automatically. **Photo mode** preserves the original image and does not repaint it. Desktop uses containment; portrait phones use a cropped/pannable view with a Fit photo control, normalized hotspots, and a named label for the focused object. Do not paint new scenery over the photo; ask the host to identify real object boxes before generation. Never fetch a user's private image URL or embed third-party trademarks without rights. Image provenance and publication rights must be reviewed by the owner.

## Iterative visual review

Before delivery, run the validator and browser smoke checks. Compare desktop (1440×900), mobile (390×844), 320×568 and landscape. Render, inspect and deliberately revise up to two times when browser and visual-inspection tools exist. Inspect screenshots, not just assertions. Ask: is the setting recognizable without reading the title? Are landmarks visibly distinct, reasonably sized, separated, interactive, and not competing with badge text? Is there a focal point? Does visual polish survive narrow viewports? If not, revise existing scene once deliberately rather than layering random decoration. See `visual-quality.md`.

## v0.2.1 scene composition

Use the content and user theme to decide visual family, depth, focal object, spatial hierarchy, landmark metaphors and mobile framing. Prefer an original bespoke SVG scene if the host can construct one safely. The bundled `scripts/scene_art.py` creates deterministic themed SVG for recognized motifs and abstract pavilions for unfamiliar concepts; it is a fallback, **not an AI-generated image or evidence of polished visual QA**. Distinguish visible landmarks from mere decorative icons. Visual review in a real browser remains recommended when possible.

## v0.2.1 visual-excellence contract

- **Procedural mode:** theme grammar controls atmosphere, terrain, light,
  architecture, destination platforms and connecting paths. A user-requested
  art direction must take precedence over unrelated nouns in source content.
- **Scenic-art mode:** a capable host may create original scenery without
  lettering, buttons, identity claims, or UI. Use both `scene_svg` and
  `scene_svg_mobile` for the landmark layer and pass `--scenic-image` to the
  unified builder. The image is not a source photo and no arbitrary photo
  bounding boxes are inferred from it. Review geometry at actual viewports.
- **Composition:** a memorable focal landmark, distinct silhouettes, spatial
  connections, readable callouts and different portrait arrangements.
- **Quality gate:** compare scenic/illustrated output with a visual reference,
  but never claim that procedural SVG alone reproduces photorealistic imagery.
  A validated webpage may still need an artistic revision.
