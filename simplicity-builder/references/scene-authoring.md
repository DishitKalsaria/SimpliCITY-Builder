# AI-authored SVG scene specification — v0.2.1

**Preferred for visually ambitious worlds when the host can write SVG and
inspect screenshots.** The procedural builder is the standard-library fallback.
Use this document as a design prompt, not as permission to invent source facts.

## Deliverables

1. Create one original SVG 620×520 with one distinct `g id="landmark-{id}"`
   per content section. Each group should contain recognizable, materially
   integrated architecture and a visible, generous hit region.
2. Create a separately composed 620×880 mobile SVG using the *same* IDs.
   Do not simply stretch a desktop panorama.
3. Use only safe SVG shapes, gradients, paths and local paint; no `<script>`,
   `<image>`, external URLs, filters or proprietary character art. Test with
   `scripts/check_artwork.py` and the builder's SVG sanitizer.
4. Prefer a 3-depth-stage scene, coherent shadows and light, a main focal
   structure, supporting landmarks and terrain that physically grounds them.
   Keep labels out of the SVG; the HTML plaque system supplies names.
5. Run build → validate → browser render → *look* at desktop and mobile pixels
   → revise at most twice. If tools are missing, disclose incomplete QA.

## Family-specific scene directions (original work, never franchise copies)

| Family | Focal object | Spatial grammar | Lighting and architecture |
|---|---|---|---|
| Meeting room | presentation table or screen | a believable interior with walls, floor, furnishings and sightlines | balanced practical lighting, surface materials and human-scale proportions |
| Playground | slide, swing or play fort | activity zones, safe walking routes and age-appropriate scale | playful daylight, rounded shapes and bright materials |
| Farm | barn, crop fields or greenhouse | functional paths, field rows, agricultural buildings and equipment | daylight, growing terrain, wood, metal and vegetation |
| Space | station or planet | orbital rings and satellites | rim light, observatories, docking pylons |
| Volcanic | luminous crater | lava branches, cliffs, rim terraces | amber underlighting, basalt, ash, ember field |
| Ocean | illuminated reef | vertical depth bands and rising architecture | caustic beams, coral shelves, blue-green haze |
| Guardian | command citadel | heroic valley, staging grounds, towers | cool rim light, metallic facades |
| Toon | original comic city | stacked expressive neighborhoods | saturated blocks, thick ink outlines |
| Nature | great tree | glades, groves, root bridges | diffuse foliage light, organic structures |
| Fantasy | castle | terraces, ridge paths, keeps | lantern glow, spires, warm stone |
| Desert | oasis/temple | dunes, canyon tiers, desert routes | low sunset, sand gradients |
| Noir | moody high-rise | layered street depth | wet reflections, hard silhouettes |
| Technology | data center | circuit-like pathways, modular towers | crisp cool edge lights |
| Museum | exhibition hall | connected atria and galleries | focused exhibit spots, stone and glass |
| Festival | main stage | connected performance zones | spotlights, color blocking |
| Invented | one original landmark | bespoke grammar named by prompt | bespoke materials and focal light |

### Reusable AI instruction

> Produce **two safe standalone SVG strings** for the theme and section IDs.
> Aim for a cohesive original storybook-quality environment, not a flowchart.
> Show clear foreground/midground/background hierarchy, architectural variation,
> accessible hit geometry and coherent light. Compose an independent portrait
> layout. Place every real `landmark-{id}` group on visible physical terrain.
> Keep facts and lettering out of the art. Build and inspect actual screenshots
> if browser tools exist, revise specific flaws and revalidate.

A written prompt cannot guarantee cinematic fidelity. It is a quality contract
for hosts capable of generating and reviewing the artwork.
