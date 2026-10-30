# World-building and navigation rules — v0.1.4

1. Treat the requested theme as unconstrained worldbuilding. Career facts are real; landmarks, metaphors and setting are creative.
2. Each resume section maps to one **visible clickable location inside the SVG scene**. Put the exact ID `landmark-<section_id>` on a painted SVG group/shape. Specify its human-readable label through `world.landmarks`; do not guess percentages or add icon pins.
3. Prefer spatial storytelling: a moon represents missions, a library represents publications, a workshop represents projects. Keep object silhouettes separated and legible at 390px mobile. Their *actual outlines* are clickable; there are no coordinate rules.
4. No page scroll: the scene must fit inside the viewport in portrait, landscape, and desktop. Modal details and list/recruiter views may scroll internally. An accessible list is always present.
5. All narrative interface copy belongs in `world.copy` when customized. Badges, ribbon text or navigation headers must never obscure art; put these *outside* the SVG and leave each illustrated object clear.
6. Built-in icons are consistent inline SVG rather than emoji. Use `references/art-components.md` to compose inert SVG artwork. Only allow predefined CSS motion classes; no untrusted CSS.
7. For requests involving Pokémon, Marvel, Star Wars or another proprietary universe, create **original** genre-level alternatives, not copies of protected characters, distinctive logos or trademark branding. Tell the user that an original interpretation was used. Do not suggest official affiliation.
8. Test screenshots at desktop, mobile, compact sizes and review visual coherence. Automated QA cannot prove artistic quality.
9. Provide recruiter view for practical hiring review, and print-friendly résumé content. The world should be playful, not block professional access.
10. Never use user-uploaded résumé examples in public galleries without informed approval; all bundled examples must be fictional.


## Landmark-first world design (v0.1.4)

Use actual **named** illustrated objects in `scene_svg`, such as `landmark-projects` on a train SVG group. For each section, define an SVG ID `landmark-<section_id>` and add a matching `world.landmarks` label. The user must explore the *object itself*, not an icon or floating HTML pin. Vary the forms, silhouettes, and environments to match any custom theme. Reserve contrast around key objects and test mobile views.
