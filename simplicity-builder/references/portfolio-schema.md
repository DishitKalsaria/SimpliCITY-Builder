# SimpliCITY Builder v0.1.4 — portfolio JSON contract

Provide verified `profile`, `world`, and `sections` objects. The generated HTML is offline, with no tracker or external runtime dependencies. Career information must be grounded in the résumé. Section IDs use lowercase hyphens and must be unique.

## Example (abridged)

```json
{
  "profile": {"name":"Verified person","headline":"Product Designer","summary":"Verified background", "links":[]},
  "world": {
    "theme":"clockwork-harbor", "title":"The Clockwork Harbor", "tagline":"Enter an invented landscape",
    "scene_svg":"<svg viewBox=\"0 0 620 520\"><g id=\"landmark-projects\"><rect x=\"200\" y=\"180\" width=\"180\" height=\"120\" fill=\"#aabbcc\"/></g></svg>",
    "landmarks":[{"section_id":"projects","label":"The Airship Workshop"}],
    "copy":{"hint":"Choose an illustrated location"},
    "share":{"url":"https://example.com/my-portfolio/","image":"https://example.com/my-portfolio/preview.jpg","image_alt":"Clockwork harbor illustration"}
  },
  "sections":[{"id":"projects", "name":"Projects", "intro":"Verified project overview", "entries":[{"title":"Verified project", "description":"A factual account", "highlights":["Grounded outcome"], "metrics":[{"value":"97%", "label":"Less manual effort"}]}]}]
}
```

## Limits actually enforced by the generator

| Field | Limit |
|---|---|
| `profile.name` | Required, 100 characters |
| `profile.headline` | Required, 180 characters |
| `profile.summary` | Required, 2,000 characters |
| `profile.links[]` | Maximum 8 absolute HTTP(S) URLs, label max 60, URL max 600 |
| `world.title` / `tagline` / `theme` | Required, 95 / 200 / 60 characters |
| `world.description` | Optional, 3,000 characters |
| `world.scene_svg` | Optional only if using fallback art; max 25,000 characters, 180 SVG nodes |
| `world.scene_svg_mobile` | Optional independent mobile scene, same section IDs, same SVG limits |
| `world.artwork_mode` | Optional `svg` (default) or `image-assisted` (requires `--background-image` when generating) |
| `world.landmarks[]` | Up to 8 records, `section_id` max 40, `label` max 60 characters |
| `world.copy` | Documented supported keys, up to 180 characters each |
| `world.share` | Optional `url` and `image` (max 600 each), `image_alt` max 160 |
| `sections[]` | 1–8, each with 1–20 entries |
| `sections[].id` / `name` / `intro` | 40 / 110 / 650 characters |
| Entry `title` / `description` / `subtitle` | 220 / 2,500 / 250 characters |
| Entry `highlights[]` | Max 12, each 400 characters |
| Entry `metrics[]` | Max 6 objects, value max 48, label max 85 characters |
| Entry `tags[]` | Max 12, each 55 characters |
| Entry `url` | Optional absolute HTTP(S), max 600 characters |

Each entry may use `type: "standard"` or `"quote"`; quotes require an authentic `attribution`. Entries also allow `employer` and `dates`. Do not invent testimonials, credentials, metrics or names.

## Navigation is the illustration, not an overlay

When `world.scene_svg` is supplied, **every section must own exactly one painted SVG object**, represented by a `<g id="landmark-SECTION-ID">...</g>` or a geometry element with that ID. The SVG viewBox is exactly `0 0 620 520`. Interactive IDs must match section IDs exactly and be unique. The generator attaches keyboard/pointer interaction and accessible labels to those actual objects. A label shown on hover/focus is dynamically positioned using the object's bounding box; there are **no coordinate pins**.

Use `world.landmarks` for human-readable labels (one per section). A previous `world.hotspots` array is accepted for migration but its `x/y` values are **ignored**. Do not create new `x/y` coordinates. Missing or duplicated SVG objects fail validation. If `scene_svg` is omitted, a safe illustrative fallback produces named landmarks automatically; off-preset custom worlds should always supply an original scene.

Aim for visibly separated, generously sized shapes that remain hittable on narrow phones. Avoid large opaque foreground elements covering landmark objects. Keep copy and résumé facts as HTML outside SVG. The document does not scroll; long text in a dialog may scroll. A searchable list and recruiter view are always offered.

## Social preview and privacy

`world.share.url` and `world.share.image` are optional public HTTPS/HTTP URLs; when supplied, they produce `og:url`, `og:image`, `og:image:alt`, `twitter:card`, `twitter:image`, and related metadata. An offline file without a **publicly reachable image** cannot show a social preview. Never auto-publish or upload sensitive résumé content. Source text and private extraction reports should remain outside Git.

## Custom copy and aesthetics

`world.copy` supported keys: `eyebrow`, `explore`, `hint`, `list`, `recruiter`, `about`, `close`, `search`, `empty`, `made_with`, `privacy`, `print`, `intro`, `locations`, `skip`, `open`, `view_work` (max 180 characters each). `world.theme` can be any lowercase-hyphenated setting. Color values use `#RGB` or `#RRGGBB`; world backgrounds must remain dark enough for accessible text. Refer to `illustration-rules.md` and `world-rules.md` for original artwork, motion, and IP guidelines.

## Background image and mobile scene

An agent may use `world.scene_svg_mobile` to create a second composition for phones. Both scenes must have one named `landmark-<section-id>` per section. The renderer keeps only one scene active at a time. For custom images, set `world.artwork_mode: "image-assisted"` and pass `--background-image /path/to/original.png`. Only local PNG/JPEG/WebP (max 4 MB) is accepted; it is embedded in the offline HTML. The SVG remains interactive, and neither image use nor image generation is mandatory. See `art-direction.md`.

**Quote entries:** `title` and `description` are required by the validator, and `attribution` is required when `type: "quote"`. No résumé quote or endorsement may be invented.

## Optional private review approvals

Top-level `review.approved_paraphrases` accepts at most 30 records with `field`, `claim`, `source_excerpt`, and `approved_by_owner: true`; source excerpts must be verifiably present in private extracted résumé text. These approvals only resolve nonnumeric, non-employer, non-date, non-quote discrepancies and are recorded in the private evidence report. Do not include original extracted résumé text in public Git repositories. See `resume-review.md`.

Legacy `world.symbol` and section `symbol` emoji fields are ignored for compatibility. New JSON should not use them. Consistent UI icons are inline SVG, and primary navigation is the illustrated scene itself.
