# Reusable safe SVG composition pieces

Place these snippets **inside** `<svg viewBox="0 0 620 520">` and adapt their numeric geometry and fill colors. A full final scene should be meaningful for the user's exact prompt. Everything below is inert and accepted by the sanitizer. Do not use CSS, foreign images, scripts, text elements, external URLs, or filter nodes.

## Star / beacon

```svg
<path d="M100 45 L108 67 130 75 108 83 100 105 92 83 70 75 92 67Z" fill="#f2d6ad"/>
```

## Floating island

```svg
<path d="M120 300 Q240 265 360 300 L334 342 278 365 190 355Z" fill="#49756c"/>
<ellipse cx="240" cy="300" rx="120" ry="22" fill="#94bb9c"/>
```

## Mountain chain

```svg
<path d="M20 375 L160 185 280 376 410 215 610 390 610 520 20 520Z" fill="#49557c"/>
```

## Tower / castle

```svg
<rect x="270" y="220" width="80" height="172" fill="#a893c5"/>
<path d="M255 220 L310 145 365 220Z" fill="#e9caee"/>
```

## Orb / planet (safe gradient)

```svg
<defs><radialGradient id="planetHalo"><stop stop-color="#9ac9f6" stop-opacity=".95"/><stop offset="1" stop-color="#273e75"/></radialGradient></defs>
<circle cx="310" cy="235" r="125" fill="url(#planetHalo)"/>
```

## Ocean creature silhouette (original)

```svg
<path d="M170 300 Q240 230 310 280 Q350 330 410 260 Q390 355 345 365 Q260 395 170 300Z" fill="#79c7bf"/>
<circle cx="233" cy="298" r="6" fill="#132e4d"/>
```

Use only sanitized SVG tags and attributes documented in `illustration-rules.md`; run `scripts/check_artwork.py` on the full scene. Use gradients for depth, readable contrasts for UI, and a coherent visual focal point. Do not add motion elements in SVG. Motion is provided by the host CSS `motion-float`, `motion-twinkle`, `motion-drift`, `motion-pulse` with reduced-motion support.
