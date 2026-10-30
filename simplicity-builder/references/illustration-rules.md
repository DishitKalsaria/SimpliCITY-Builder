# Original artwork for any world

For a genuinely user-defined theme, design an original **decorative SVG scene** matching their prompt, not a renamed default scene. Store it in `world.scene_svg` as a JSON string. Use a fixed `<svg viewBox="0 0 620 520">...</svg>` root with *no `xmlns` or namespaces*; the generator wraps the safe content with an accessible SVG shell.

Allowed elements: `svg`, `g`, `circle`, `ellipse`, `rect`, `line`, `path`, `polygon`, `polyline`. Avoid `<text>`; all meaningful content lives in HTML. Use geometric primitives to suggest silhouettes, locations, atmosphere and a visual focal point. Recommended 12–45 primitives, maximum 160. Your illustrations should remain legible at mobile sizes.

Allowed paints: hex RGB, hex RRGGBB, `white`, `black`, `none`, `var(--accent)`, `var(--accent2)`. Allowed attributes: ordinary geometry, `fill`, `stroke`, `stroke-width`, `opacity`, `stroke-linecap`, `stroke-linejoin`, and basic `transform`. Scripts, event handlers, images, href, external resources, CSS, filters, foreignObject, embedded text and gradients are **not** accepted by the generator.

No photographic claims: the world is decorative narrative art. Professional facts must be expressed as actual readable HTML. If a requested theme needs a very unusual aesthetic, create a theme-specific 2D composition with matching colors, section metaphors, and symbols rather than promising fully rendered 3D environments. Validate and revise the SVG if the generator rejects it.

No need to ask the user to choose between fairytale/space/graffiti—interpret their creative prompt directly. Example themes: steampunk carnival, floating library, space station, cricket stadium, cyberpunk subway, underwater reef, music festival, and anything else.
