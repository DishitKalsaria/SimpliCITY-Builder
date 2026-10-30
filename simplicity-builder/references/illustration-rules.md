# Original SVG artwork — accepted syntax (v0.2.0)

Create original **decorative** SVG for the user's *arbitrary* imaginative world and store it as a JSON string in `world.scene_svg`. The generator validates and sanitizes the artwork before embedding it.

## Canvas and composition

- Root: `<svg viewBox="0 0 620 520"> ... </svg>`. The ordinary SVG `xmlns="http://www.w3.org/2000/svg"` is also accepted. No `width`/`height` needed.
- Allowed elements: `svg`, `defs`, `linearGradient`, `radialGradient`, `stop`, `g`, `circle`, `ellipse`, `rect`, `line`, `path`, `polygon`, `polyline`.
- `defs` must be directly under `svg`, can hold only gradients; gradients can hold only `stop` elements; every gradient needs a unique simple `id` (`[A-Za-z][A-Za-z0-9_-]*`, 40 characters max).
- Artwork uses a maximum of 180 elements and 25,000 characters. Keep most scenes to 12–60 elements.

## Supported attributes

- Geometry: `cx`, `cy`, `r`, `rx`, `ry`, `x`, `y`, `width`, `height`, `x1`, `y1`, `x2`, `y2`, `d`, `points` on their relevant primitive.
- Shape and group styling: `fill`, `stroke`, `stroke-width`, `opacity`, `stroke-linecap`, `stroke-linejoin`, **`transform` on shapes and groups**.
- Stroke caps: `round`, `square`, `butt`; stroke joins: `round`, `bevel`, `miter`.
- Transform: `translate(...)`, `rotate(...)`, `scale(...)`, `matrix(...)`, `skewX(...)`, `skewY(...)` with numeric arguments. For example `transform="rotate(-25 320 260)"` on an ellipse is valid.
- Paint values: `#abc`, `#aabbcc`, `none`, `white`, `black`, `var(--accent)`, `var(--accent2)`, and an **internal gradient reference** `url(#glow)` in `fill` or `stroke` when gradient `glow` exists in `<defs>`.
- Gradients: `linearGradient` (`id`, `x1`, `y1`, `x2`, `y2`), `radialGradient` (`id`, `cx`, `cy`, `r`, `fx`, `fy`), with numeric or percentage coordinates. `stop` accepts `offset` (0–1 or 0%–100%), `stop-color` (safe solid paint), `stop-opacity` (0–1).

## Safe example — glowing planet with a ring

```xml
<svg viewBox="0 0 620 520">
  <defs>
    <radialGradient id="planetGlow">
      <stop offset="0%" stop-color="#c1e9ff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#34478b" stop-opacity="0.2"/>
    </radialGradient>
  </defs>
  <circle cx="310" cy="250" r="130" fill="url(#planetGlow)"/>
  <ellipse cx="310" cy="250" rx="210" ry="50" transform="rotate(-22 310 250)" fill="none" stroke="#f8cfab" stroke-width="12" stroke-linecap="round"/>
</svg>
```

**Never use** `script`, event handlers, CSS, `style`, filters, images, foreignObject, embedded text, HTML, href/xlink, network URLs, remote fonts, animation, or unlisted SVG elements/attributes. `url(#id)` is only supported for references to gradients defined in the same artwork, never external URLs.

**Preflight SVG** before full generation: `python3 simplicity-builder/scripts/check_artwork.py your-scene.svg` (no résumé needed). If generation reports an invalid attribute, correct that exact error; do not downgrade the artwork to a generic theme without first checking the rules.

All career facts must remain regular selectable HTML text. The SVG is an optional visual narrative, not a substitute for the user's projects, dates or qualifications. The generator produces a responsive 2D/2.5D portfolio, not a bespoke 3D game.
