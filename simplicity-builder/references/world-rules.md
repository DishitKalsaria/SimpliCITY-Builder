# World-building and navigation rules — v0.1.2

1. Treat the requested theme as unconstrained worldbuilding. Career facts are real; landmarks, metaphors and setting are creative.
2. Each resume section maps to one **visible clickable location inside the SVG scene**. Place hotspots near corresponding world landmarks. Provide an accurate, concise label and aria-label; use stable `section_id` references.
3. Prefer spatial storytelling: a moon represents missions, a library represents publications, a workshop represents projects. Don't place every hotspot in one cluster. Use the `world.hotspots` coordinate rules and ensure no overlap at 390px mobile.
4. No page scroll: the scene must fit inside the viewport in portrait, landscape, and desktop. Modal details and list/recruiter views may scroll internally. An accessible list is always present.
5. All narrative interface copy belongs in `world.copy` when customized. Badges, ribbon text or navigation headers must never obscure art; put these *outside* the SVG and leave each hotspot readable.
6. Built-in icons are consistent inline SVG rather than emoji. Use `references/art-components.md` to compose inert SVG artwork. Only allow predefined CSS motion classes; no untrusted CSS.
7. For requests involving Pokémon, Marvel, Star Wars or another proprietary universe, create **original** genre-level alternatives, not copies of protected characters, distinctive logos or trademark branding. Tell the user that an original interpretation was used. Do not suggest official affiliation.
8. Test screenshots at desktop, mobile, compact sizes and review visual coherence. Automated QA cannot prove artistic quality.
9. Provide recruiter view for practical hiring review, and print-friendly résumé content. The world should be playful, not block professional access.
10. Never use user-uploaded résumé examples in public galleries without informed approval; all bundled examples must be fictional.
