# Visual quality acceptance rubric — v0.2.1

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
- Missing or overlapping name plaques → keep concise **always-visible** accessible labels near their SVG objects, reposition them for mobile and review overlap; hover is never the only label.
- Constellation paths work with mouse only at line intersections → test bounding-box hit target and keyboard fallback.
- Dark subject disappears on an image layer → redesign contrast or adjust image opacity, do not hide object.
- Mobile merely shrinks desktop → use a separate `scene_svg_mobile` composition. The procedural engine now builds one for unfamiliar themes.

## Render → look → revise (when Chromium and image inspection are available)

After the HTML validator passes, run `python3 scripts/browser_smoke.py index.html --screenshots /private/screenshots` on desktop, phone, compact phone and landscape. Examine the **actual screenshots**, score theme recognition, composition, recognizable silhouettes, visible plaques, source fidelity, contrast and copy. Fix specific defects; rerender and inspect. Allow **up to two deliberate revision rounds**. Do not keep adding generic shapes blindly. If the host cannot inspect screenshots or lacks Chromium/Playwright, say what was skipped. Automated geometry checks cannot establish that photo anchors correspond semantically to real objects.

For a supplied photo, the original must be visibly present, no synthetic hills/moons may be superimposed, and each anchored region must correspond to an object actually visible in the photo. Check the coordinates after responsive image fitting. For one-item content, require a featured-story control instead of an empty exploration prompt.

## Contrast and visual truthfulness

Use legible interface copy, with ordinary text meeting at least 4.5:1 and large text 3:1 where measured against its actual rendered background. Review translucent overlays and custom accents with real screenshots. A default SVG composition is an accessibility-oriented fallback, not guaranteed artistic polish for every invented theme. Never claim visual WCAG certification from structural tests alone.

## Automatic checks in v0.2.1

The optional Chromium runner fails on overlapping plaques, plaques outside stage, plaques crossing landmarks/photo navigation, unfilled stage edges, clipped titles, undersized targets, inadequate foreground contrast, and mobile photo coverage below 55%. In photo crop mode, objects outside the current viewport remain available through the photo object navigator and accessible location list. A manual screenshot quality review still decides whether the visual style is compelling. Keep the render → inspect → revise cycle to no more than two revisions when tools permit.

**Last-touch QA:** A plaque must be within 42 CSS px of its landmark on phones (60 px elsewhere), not just inside the stage. Check the right-hand mobile owner/headline for clipping. A foreground scene must not redraw an aspect-fitted rectangular backdrop over edge-to-edge ambience. For panned photographs, the current object receives the visible plaque while other objects are available through Previous/Next and the accessible list. Photo-anchor correctness still requires a person or image-capable agent to inspect the actual photo: geometry checks cannot establish semantic truth.
