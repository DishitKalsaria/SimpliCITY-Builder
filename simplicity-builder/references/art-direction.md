# Art direction — SimpliCITY Builder v0.1.4

**Do not begin by drawing disconnected SVG shapes.** Prepare a compact internal plan first, then build the interactive scene. Any user-defined world (saloon, fantasy, underwater, space, graffiti, original hybrid) is valid.

## Six-part art brief (before making artwork)

1. **Setting and visual metaphor:** one sentence describing the world's physical place and how career chapters relate.
2. **Focal hierarchy:** one unmistakable primary destination, one or two secondary landmarks, and atmospheric supporting details that do not steal clicks.
3. **Layering:** distinct far background, midground, interactive objects, foreground details. Do not paint the foreground over a landmark's click area.
4. **Palette and lighting:** 3–5 cohesive colors, an intentional light direction, softened shadow contrast, gradients for volume, accessible text outside art.
5. **Landmarks:** one original named *object* per section, each made from a recognizably different silhouette. Use grouping, depth and meaningful context; no icon pins.
6. **Desktop AND mobile:** check the 620 × 520 coordinate scene at desktop; for phones explicitly decide whether separate `world.scene_svg_mobile` is better. Mobile version must include *all* named landmarks with the same section IDs. Never hide résumé sections on mobile.

Use optional `assets/art-kit/` samples as composable primitives, not fixed themes. Layer larger coherent objects before adding highlights and tiny embellishments. Avoid excessive path/shape counts that create scattered compositions. Scenes should communicate a place, not icons sprinkled on a canvas.

## Optional image-assisted artwork

Only when the host offers image-generation or the user supplies a suitable image. Generate or use an **original** raster background with no career text embedded. Leave room for the named interactive SVG objects. The background is NOT clickable. Embed a local PNG/JPEG/WebP (4MB maximum) using `--background-image`. The generator embeds the image as a data URL, so the HTML works without network access. Keep the SVG landmarks on top, so they remain navigable, searchable, keyboard-operable, and visible at mobile sizes. Set `world.artwork_mode` to `image-assisted`; do not request this mode unless the image file is available.

For mobile, a separate mobile SVG is optional and supported, but a separate raster image is not; compose/crop any supplied image with safe central regions. Never fetch a user's private image URL or embed third-party trademarks without rights. Image provenance and publication rights must be reviewed by the owner.

## Iterative visual review

Before delivery, run the validator and browser smoke checks. Compare desktop (1440×900), mobile (390×844), 320×568 and landscape. Inspect screenshots, not just assertions. Ask: is the setting recognizable without reading the title? Are landmarks visibly distinct, reasonably sized, separated, interactive, and not competing with badge text? Is there a focal point? Does visual polish survive narrow viewports? If not, revise existing scene once deliberately rather than layering random decoration. See `visual-quality.md`.
