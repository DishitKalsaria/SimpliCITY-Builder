# Portfolio JSON schema — SimpliCITY Builder v0.1.2

The generator takes `profile`, `world`, and `sections`; text is HTML-escaped. Career facts must be grounded in the supplied résumé. See `examples/fairytale-sample.json` for an entirely fictional example.

```json
{
  "profile": {"name":"Verified person","headline":"Verified profession","summary":"Verified introduction","links":[]},
  "world": {
    "theme":"flying-library", "title":"The Floating Library", "tagline":"Explore a story among the clouds",
    "description":"Navigate landmarks to find professional chapters", "visual_name":"Floating islands",
    "accent":"#f1d498", "accent_secondary":"#b1a6fa", "background":"#101525", "background_secondary":"#242642",
    "scene_svg":"<svg viewBox=\"0 0 620 520\"><circle cx=\"300\" cy=\"250\" r=\"95\" fill=\"#b1a6fa\"/></svg>",
    "hotspots":[{"section_id":"projects","x":36,"y":56,"label":"Sky Library"}],
    "copy":{"eyebrow":"The story among the clouds","list":"Explore islands","hint":"Select a floating landmark","recruiter":"Career at a glance"}
  },
  "sections":[{"id":"projects","name":"Sky Library","intro":"Verified projects and outcomes","eyebrow":"Featured work","entries":[
    {"title":"A verified project","subtitle":"Verified team / timeframe","description":"Factual summary","highlights":["Actual task or outcome"],"metrics":[{"value":"97%","label":"Less manual effort (verified)"}],"tags":["Verified skill"]},
    {"type":"quote","title":"Endorsement","description":"Exact authorized quotation","attribution":"Verified source"}
  ]}]
}
```

## Sections and entries

- `sections`: 1–8 sections, unique lowercase-hyphen `id`, with `name`, `intro`, and 1–20 entries each. `eyebrow` optional.
- Entry required `title`, `description`. Optional `type: standard|quote` (default standard), `subtitle`, `highlights` (up to 12 bullet strings, 400 chars each), `metrics` (up to 6 `{value,label}` objects), `tags` (up to 12 strings), `employer`, `dates`, `url` (public http(s) only).
- A `quote` entry requires `attribution`, which must come from an authentic user-approved source. Never invent testimonials.
- Section names, thematic titles and descriptions may use imaginative *metaphors*; hard facts may not be fictionalized.

## Hotspots and no-scroll design

`world.hotspots` should have exactly one location for each section: `section_id`, `x` (8–92% of SVG frame), `y` (10–86%), and visible `label` (up to 42 characters). Distinct hotspots must be separated by at least 13 percentage points; avoid placing them over creature faces or important visual features. If omitted, the renderer uses stable default coordinates. Labels are accessible by keyboard and screen readers. The world scene fills the viewport without *page* scrolling; detailed panels can scroll internally. Reserve the interface header and footer **outside** the SVG area and keep landmarks visible at mobile width. For large detailed résumés, use recruiter view and internal scrolling; never truncate actual career facts to fit a scene.

## Editable UI text

`world.copy` optional keys: `eyebrow`, `explore`, `hint`, `list`, `recruiter`, `about`, `close`, `search`, `empty`, `made_with`, `privacy`, `print`, `intro`, `locations`, `skip`, `open`, `view_work`. Each is a string up to 180 characters. Fallback values are provided. Profile name/headline and map region labels remain fully data-driven. `scene_svg` is decorative; keep facts and labels in readable HTML.

## Colors and themes

`world.theme` can be **any lowercase-hyphenated string**; no theme whitelist. Starter scenes are fallback examples only. Supply a custom SVG for nonstarter themes to get genuinely distinctive imagery; otherwise a generic scene is used and the AI must disclose this. World background colors must be dark enough for the provided text palette.

## Fact checking

Run `scripts/verify_facts.py` with private extracted résumé text. It checks numbers, dates, explicit employer names, attributions and tags against source text, but **matching tokens does not prove the claim is true** and paraphrases may be flagged. Review the report; request owner confirmation before publishing.
