# Illustrated landmark rules — SimpliCITY Builder v0.1.4

The illustration is the navigation. **Do not draw icon pins, badges or clickable circles over an unrelated background.** A saloon, windmill, planet, bridge, train, creature or crystal spire is itself a safe clickable SVG object.

- Root must be `<svg viewBox="0 0 620 520">`. Max 25,000 characters and 180 SVG nodes.
- Each career section `id` must have exactly one **named, painted** scene object: `<g id="landmark-experience">...</g>` or a shape with that ID. No nesting of interactive landmark IDs. The ID must match the section and must not be repeated.
- Compose each landmark as a coherent group of colored geometry. Groups can contain multiple shapes; the actual filled/stroked geometry is the clickable outline. Never create invisible overlay rectangles or percentage-coordinate pins to simulate interactions.
- Allowed geometry: `g`, `circle`, `ellipse`, `rect`, `line`, `path`, `polygon`, `polyline`, plus `defs`, `linearGradient`, `radialGradient`, `stop`. Allowed shape style attributes: `fill`, `stroke`, `stroke-width`, `stroke-linecap`, `stroke-linejoin`, `opacity`, `transform` and `class`. The `id` attribute is allowed only on landmarks and self-contained gradients. No scripts, external resources, foreignObject, SVG text, event handlers, external links or arbitrary CSS.
- Allowed paint: hex `#RGB` / `#RRGGBB`, `white`, `black`, `none`, `var(--accent)`, `var(--accent2)`, `url(#localGradient)`. Linear/radial gradient stops stay local. Only preset animation class names `motion-twinkle`, `motion-drift`, `motion-float`, `motion-pulse` may be specified; there is no arbitrary SVG/CSS animation input.
- Keep distinct object silhouettes with ample space. Aim for solid painted objects at least ~80 SVG units wide for phone usability. Use layers, muted background color, light, shadow, safe gradients, and scenery—but ensure landmarks remain readable and foreground art does not intercept taps.
- A landmark gets a title, hover glow, and keyboard focus by the generator. The label tooltip is positioned from its **real rendered bounding box**, not guessed coordinates. Keyboard Enter/Space and touch open details. Screen reader labels are generated from `world.landmarks`.
- `prefers-reduced-motion` disables decorative animation and transitions. Never animate important career text.
- Automated smoke tests cannot judge illustrative taste. Inspect desktop, mobile portrait, small mobile, and landscape screenshots before publishing.

Example minimal scene:

```xml
<svg viewBox="0 0 620 520">
  <defs><linearGradient id="towerLight"><stop stop-color="#f4daaf"/><stop offset="1" stop-color="#a790c5"/></linearGradient></defs>
  <g id="landmark-projects"><rect x="230" y="210" width="140" height="170" rx="12" fill="url(#towerLight)"/><path d="M215 210 L300 135 L385 210Z" fill="#b48fce" transform="rotate(-7 300 190)"/></g>
</svg>
```

Preflight the SVG with `scripts/check_artwork.py`, then run the full builder, validator, and browser smoke test. Preflight alone checks SVG safety; **full build** checks that every section has a matching named landmark.

## v0.1.4 interaction and mobile guidance

Landmarks may use a single permitted `motion-*` class; the generator merges this with `scene-landmark` instead of emitting a duplicate class attribute. Hollow constellations and comet trails use a bounding-box click target where supported without drawing visible pins; use the accessible location list as a universal fallback. Test hovering the landmark's geometric center and keyboard Enter to catch sparse object defects.

`world.scene_svg_mobile` is an optional complete second `<svg viewBox="0 0 620 520">` with identical landmark IDs, composed for phones rather than an automatic shrink. The inactive scene stays inside an inert HTML template, and no duplicate active landmark IDs are created. See `art-direction.md` and `visual-quality.md`.
