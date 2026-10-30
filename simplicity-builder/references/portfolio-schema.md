# Verified portfolio model

Create UTF-8 `portfolio.json` with `profile`, `world`, and `sections`. See `references/sample.json` for shape only and `examples/clockwork-sample.json` in the repository for original theme artwork. **Never reuse sample profile facts.**

```json
{
  "profile": {"name": "Verified person", "headline": "Grounded professional title", "summary": "Grounded narrative summary", "links": []},
  "world": {
    "title": "The Clockwork Museum",
    "tagline": "Original invitation to explore",
    "description": "What visitors discover",
    "theme": "clockwork-museum",
    "visual_name": "Gallery of mechanical inventions",
    "symbol": "⚙️",
    "accent": "#f0d38e",
    "accent_secondary": "#9ddbbf",
    "background": "#0d2025",
    "background_secondary": "#243a39",
    "scene_svg": "<svg viewBox=\"0 0 620 520\"><circle cx=\"310\" cy=\"250\" r=\"100\" fill=\"#9ddbbf\"/></svg>"
  },
  "sections": [{
    "id": "experience",
    "name": "The Clockmaker's Workshops",
    "intro": "Career roles and responsibilities",
    "symbol": "🔧",
    "eyebrow": "Professional experience",
    "entries": [{"title": "Grounded role", "subtitle": "Employer and dates when verified", "description": "Verifiable résumé facts", "tags": ["Verified skill"]}]
  }]
}
```

The `world.theme` field may be **any lowercase, hyphenated identifier** (`a-z`, digits, hyphen). There are starter visual scenes for fairytale, space, graffiti, ocean and custom; other names fall back to a generic scene **unless** you supply `scene_svg`, which is recommended for truly custom worlds. This is deliberately not a preset-only theme system. `visual_name`, `accent`, `accent_secondary`, `background`, `background_secondary`, and `scene_svg` are optional. Dark backgrounds required to maintain readable text.

The hero SVG must follow `illustration-rules.md`; it is strictly sanitized. Sections: 1–8. Each section: unique lowercase-hyphenated id; name, intro, 1–20 entries. Entry: title, description, optional subtitle, tags, verified public http(s) URL. No email/phone/address are output by default. Public profile links only when user-approved.

Static content will be HTML escaped. Do not put raw HTML, JavaScript, or markup in text fields. If an unusual career fact is unclear or conflicting, omit it and flag for review.
