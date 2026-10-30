# Visual quality acceptance rubric — v0.1.5

Qualitative, not a mathematically objective score. Evaluate each 1–5; revise any dimension below 4 before presenting as polished.

- **Theme recognition:** Would an unfamiliar visitor recognize the requested world without reading labels?
- **Composition:** Does one focal destination lead the eye, with coherent lighting, atmospheric depth, and spacing?
- **Illustration:** Are landmarks recognizable objects, not primitive placeholders or repetitive buildings?
- **Interaction:** Does hovering, keyboard focus, touch/click and a sparse stroked landmark work? Is a first-visit instruction available?
- **Responsive integrity:** Are all locations visible and tappable on small phones and mobile landscape, with no document scroll or clipped copy?
- **Accessibility:** Are location names meaningful, user interface legible, reduced motion honored, and a location list/recruiter view provided?

## Automated vs human

Chromium checks can verify geometry, no page scrolling, interactive focus/click, dialog behavior, console exceptions and screen captures. They **cannot** guarantee taste, faithful art direction, logo licensing, image provenance, or semantic factual correctness. Review screenshots manually with the owner.

## Typical failures

- Empty center with dispersed icons → redesign around one dominant landmark and secondary destinations.
- Floating badge obscures landmark → keep labels in hover tooltip outside art, not permanent overlay.
- Constellation paths work with mouse only at line intersections → test bounding-box hit target and keyboard fallback.
- Dark subject disappears on an image layer → redesign contrast or adjust image opacity, do not hide object.
- Mobile merely shrinks desktop → provide `scene_svg_mobile` with a better composition.
