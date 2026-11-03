"""Self-contained, deterministic SVG compositions for unfamiliar themes.

No image API, network access, external SVG resources, or runtime dependencies.
An AI host should still prefer bespoke source-aware art where available.
"""
from __future__ import annotations

import hashlib
import html

PALETTES = (
    ('#f4c879', '#a7b9ff', '#11182b', '#29354e'),
    ('#a7ead9', '#f5b3dc', '#10212d', '#243e47'),
    ('#ffcb9c', '#d2b9fa', '#20142c', '#41304f'),
    ('#c5e8fd', '#ffca95', '#131b30', '#2e344c'),
    ('#daef9b', '#a1d8fb', '#152128', '#2d4145'),
    ('#ffc7db', '#96e3de', '#241929', '#413246'),
)

FAMILIES = {
    'guardian': ('ranger', 'superhero', 'guardian', 'hero', 'mecha', 'robot', 'transformer', 'power-ranger'),
    'space': ('space', 'planet', 'galaxy', 'cosmos', 'cosmic', 'observatory', 'starship', 'astronaut', 'alien'),
    'nature': ('forest', 'jungle', 'garden', 'nature', 'fairy', 'flower', 'tree', 'forest'),
    'ocean': ('ocean', 'underwater', 'sea', 'coral', 'submarine', 'aquatic'),
    'museum': ('museum', 'gallery', 'exhibit', 'history', 'archive', 'library', 'book'),
    'technology': ('technology', 'cyber', 'digital', 'network', 'future', 'science', 'lab', 'data'),
    'fantasy': ('kingdom', 'castle', 'dragon', 'magic', 'fantasy', 'medieval', 'enchanted'),
    'festival': ('music', 'festival', 'concert', 'dance', 'graffiti', 'street', 'art'),
    'desert': ('desert', 'oasis', 'dune', 'sand', 'ancient ruins', 'pyramid'),
    'noir': ('noir', 'detective', 'mystery', 'city night', 'rainy alley', 'film noir'),
}


def family_for(theme: str) -> str:
    content = theme.lower().replace('-', ' ')
    # A named exhibition takes precedence over its subject (e.g. cosmic museum).
    if any(t in content for t in ('museum', 'gallery', 'exhibit')):
        return 'museum'
    for family, terms in FAMILIES.items():
        if any(t in content for t in terms):
            return family
    return 'invented'


THEME_PACKS = {  # accent, secondary, dark background, dark surface
    'guardian': ('#b4dcff', '#ffcc8e', '#111b30', '#273750'),
    'space': ('#a5e4ff', '#c7b3ff', '#0a1128', '#242544'),
    'nature': ('#d5efac', '#a5dfca', '#122822', '#26413d'),
    'ocean': ('#a5f0e6', '#a6cfff', '#091f2c', '#17384c'),
    'museum': ('#f1d9a9', '#c6c0f2', '#1c1a2c', '#343347'),
    'technology': ('#9ce8e5', '#cfb7ff', '#111b2d', '#2a3348'),
    'fantasy': ('#f5d6a0', '#cbb7f0', '#20172e', '#3c2a49'),
    'festival': ('#ffd1a0', '#ffbfe1', '#241725', '#432a43'),
    'desert': ('#f8df9c', '#e6bd83', '#282018', '#493b2d'),
    'noir': ('#a9e8dc', '#e9b6c9', '#121c22', '#29333a'),
}


def palette_for(theme: str) -> tuple[str, str, str, str]:
    family = family_for(theme)
    if family in THEME_PACKS:
        return THEME_PACKS[family]
    checksum = hashlib.sha256(theme.encode('utf-8')).digest()[0]
    return PALETTES[checksum % len(PALETTES)]


def _motif(kind: str, x: int, y: int, i: int) -> str:
    """Shapes *are* interaction landmarks; no overlay pins or detached buttons."""
    primary = f'url(#material-{i})'
    if kind == 'guardian':
        # The stations have different silhouettes, not a row of cloned helmets.
        # Color-coded team energy is conveyed without protected logos/characters.
        if i % 4 == 0:  # Command citadel
            return (f'<path d="M{x-74} {y+67} L{x-66} {y-42} L{x-38} {y-74} L{x-12} {y-74} L{x} {y-118} L{x+12} {y-74} L{x+38} {y-74} L{x+66} {y-42} L{x+74} {y+67}Z" fill="{primary}"/>'
                    f'<path d="M{x-67} {y-24} H{x+67} V{y+9} H{x-67}Z" fill="#233654"/>'
                    f'<path d="M{x-42} {y-14} H{x+42} L{x+23} {y+9} H{x-23}Z" fill="var(--accent2)"/>'
                    f'<path d="M{x-14} {y+67} V{y+24} Q{x} {y+3} {x+14} {y+24} V{y+67}Z" fill="#172844"/>'
                    f'<path d="M{x-67} {y+30} H{x-30} M{x+30} {y+30} H{x+67}" stroke="#f5ebbf" stroke-width="8"/>')
        if i % 4 == 1:  # Training arena with tiered octagonal ring
            return (f'<path d="M{x-83} {y+13} L{x-58} {y-35} H{x+58} L{x+83} {y+13} L{x+56} {y+71} H{x-56}Z" fill="#42547d"/>'
                    f'<path d="M{x-65} {y+8} L{x-45} {y-28} H{x+45} L{x+65} {y+8} L{x+42} {y+53} H{x-42}Z" fill="{primary}"/>'
                    f'<ellipse cx="{x}" cy="{y+7}" rx="40" ry="20" fill="#192d4b" stroke="var(--accent2)" stroke-width="8"/>'
                    f'<path d="M{x} {y-93} L{x+20} {y-65} L{x} {y-35} L{x-20} {y-65}Z" fill="var(--accent)"/>'
                    f'<path d="M{x-65} {y+60} H{x+65}" stroke="#dce7fd" stroke-width="9"/>')
        if i % 4 == 2:  # Mecha hangar, angular roof and open bays
            return (f'<path d="M{x-78} {y+66} L{x-68} {y-49} L{x} {y-104} L{x+68} {y-49} L{x+78} {y+66}Z" fill="{primary}"/>'
                    f'<path d="M{x-53} {y-40} H{x+53} V{y+66} H{x-53}Z" fill="#243655"/>'
                    f'<path d="M{x-37} {y+66} V{y-21} H{x+37} V{y+66}" fill="none" stroke="var(--accent2)" stroke-width="10"/>'
                    f'<path d="M{x-24} {y+64} V{y+7} L{x} {y-16} L{x+24} {y+7} V{y+64}" fill="#a9e1ec"/>'
                    f'<circle cx="{x}" cy="{y+21}" r="12" fill="var(--accent)"/>')
        # Energy portal on a plinth, visibly distinct and circular.
        return (f'<path d="M{x-77} {y+45} L{x-56} {y+72} H{x+56} L{x+77} {y+45}Z" fill="#50617b"/>'
                f'<ellipse cx="{x}" cy="{y-8}" rx="59" ry="83" fill="#1c3455" stroke="var(--accent2)" stroke-width="18"/>'
                f'<ellipse cx="{x}" cy="{y-8}" rx="34" ry="61" fill="{primary}" opacity=".86"/>'
                f'<path d="M{x} {y-57} L{x+15} {y-9} L{x} {y+36} L{x-15} {y-9}Z" fill="#fff9dc" opacity=".76"/>')
    if kind == 'space':
        if i % 3 == 1:  # tall observatory, unlike a planet
            return (f'<path d="M{x-64} {y+62} L{x-50} {y-22} H{x+50} L{x+64} {y+62}Z" fill="{primary}"/>'
                    f'<path d="M{x-55} {y-22} Q{x} {y-130} {x+55} {y-22}Z" fill="#29476a" stroke="#bde7ff" stroke-width="8"/>'
                    f'<rect x="{x-28}" y="{y+3}" width="56" height="59" rx="8" fill="#213753"/>')
        if i % 3 == 2:  # communication array
            return (f'<path d="M{x-49} {y+62} L{x} {y-48} L{x+49} {y+62}Z" fill="{primary}"/>'
                    f'<ellipse cx="{x}" cy="{y-48}" rx="72" ry="27" transform="rotate(-20 {x} {y-48})" fill="none" stroke="#bbdfff" stroke-width="11"/>'
                    f'<circle cx="{x}" cy="{y-48}" r="18" fill="var(--accent2)"/>')
        return (f'<circle cx="{x}" cy="{y}" r="65" fill="{primary}"/>'
                f'<ellipse cx="{x}" cy="{y}" rx="80" ry="26" transform="rotate(-28 {x} {y})" fill="none" stroke="var(--accent2)" stroke-width="12"/>'
                f'<circle cx="{x-21}" cy="{y-22}" r="18" fill="#ffffff" opacity=".29"/>')
    if kind == 'nature' and i % 3 == 1:
        return (f'<path d="M{x-60} {y+62} Q{x-78} {y-11} {x} {y-80} Q{x+78} {y-11} {x+60} {y+62}Z" fill="{primary}"/>'
                f'<circle cx="{x}" cy="{y-18}" r="27" fill="#edffd2" opacity=".5"/>'
                f'<path d="M{x} {y+64} V{y-21}" fill="none" stroke="#355c4a" stroke-width="15"/>')
    if kind == 'nature' and i % 3 == 2:
        return (f'<path d="M{x} {y+64} V{y-72}" stroke="#bde8d1" stroke-width="15"/>'
                f'<ellipse cx="{x}" cy="{y-48}" rx="68" ry="41" fill="{primary}"/>'
                f'<circle cx="{x-22}" cy="{y-53}" r="21" fill="#eff9db" opacity=".45"/>')
    if kind == 'ocean' and i % 3 == 1:
        return (f'<ellipse cx="{x}" cy="{y+25}" rx="77" ry="39" fill="{primary}"/>'
                f'<path d="M{x-34} {y+18} V{y-50} Q{x} {y-116} {x+34} {y-50} V{y+18}Z" fill="#2a5973" stroke="#aeefff" stroke-width="8"/>'
                f'<circle cx="{x}" cy="{y-38}" r="18" fill="var(--accent2)"/>')
    if kind == 'ocean' and i % 3 == 2:
        return (f'<path d="M{x-65} {y+58} Q{x-45} {y-48} {x-12} {y+12} Q{x+15} {y-95} {x+41} {y+28} L{x+61} {y+58}Z" fill="{primary}"/>'
                f'<circle cx="{x-21}" cy="{y-18}" r="15" fill="#baffed" opacity=".65"/>')
    if kind == 'museum' and i % 3 == 1:
        return (f'<path d="M{x-65} {y-73} H{x+65} L{x+48} {y-55} H{x-48}Z" fill="{primary}"/>'
                f'<path d="M{x-47} {y-53} V{y+55} M{x} {y-53} V{y+55} M{x+47} {y-53} V{y+55}" stroke="#c9d0e3" stroke-width="20"/>'
                f'<rect x="{x-73}" y="{y+55}" width="146" height="17" fill="#8c85b1"/>')
    if kind == 'museum' and i % 3 == 2:
        return (f'<circle cx="{x}" cy="{y-29}" r="52" fill="{primary}"/>'
                f'<path d="M{x-56} {y+29} H{x+56} V{y+71} H{x-56}Z" fill="#5f6687"/>'
                f'<path d="M{x-29} {y-29} Q{x} {y-80} {x+29} {y-29}" fill="none" stroke="#edf3ff" stroke-width="9"/>')
    if kind == 'technology' and i % 3 == 1:
        return (f'<rect x="{x-70}" y="{y-62}" width="140" height="126" rx="18" fill="{primary}"/>'
                f'<circle cx="{x}" cy="{y}" r="43" fill="#1c3558" stroke="var(--accent2)" stroke-width="9"/>'
                f'<path d="M{x-20} {y} H{x+20} M{x} {y-20} V{y+20}" stroke="#d5faff" stroke-width="8"/>')
    if kind == 'technology' and i % 3 == 2:
        return (f'<path d="M{x-68} {y+61} L{x-48} {y-57} H{x+48} L{x+68} {y+61}Z" fill="{primary}"/>'
                f'<rect x="{x-31}" y="{y-33}" width="62" height="78" rx="8" fill="#223c5b"/>'
                f'<circle cx="{x}" cy="{y-5}" r="20" fill="var(--accent2)"/>')
    if kind == 'nature':
        return (f'<path d="M{x} {y-112} Q{x+94} {y-50} {x+54} {y+9} Q{x+87} {y+53} {x} {y+45} Q{x-86} {y+53} {x-54} {y+9} Q{x-94} {y-50} {x} {y-112}Z" fill="{primary}"/>'
                f'<path d="M{x} {y+40} V{y+84}" stroke="var(--accent2)" stroke-width="18"/>'
                f'<path d="M{x-55} {y-9} Q{x} {y-83} {x+54} {y-9}" fill="none" stroke="#e6ffe7" stroke-width="9" opacity=".55"/>')
    if kind == 'ocean':
        return (f'<path d="M{x-57} {y+69} Q{x-77} {y-8} {x-31} {y-49} Q{x} {y-87} {x+31} {y-49} Q{x+77} {y-8} {x+57} {y+69}Z" fill="{primary}"/>'
                f'<path d="M{x-42} {y+47} Q{x} {y+10} {x+42} {y+47}" fill="none" stroke="#e5fff7" stroke-width="11" opacity=".55"/>'
                f'<circle cx="{x}" cy="{y-16}" r="24" fill="#234361" stroke="var(--accent2)" stroke-width="8"/>')
    if kind == 'museum':
        return (f'<path d="M{x-71} {y-53} L{x} {y-105} L{x+71} {y-53}Z" fill="{primary}"/>'
                f'<rect x="{x-64}" y="{y-46}" width="128" height="117" rx="5" fill="#53617a"/>'
                f'<rect x="{x-46}" y="{y-29}" width="92" height="68" rx="6" fill="var(--accent2)" opacity=".69"/>'
                f'<path d="M{x-22} {y+71} V{y+39} Q{x} {y+9} {x+22} {y+39} V{y+71}Z" fill="#152332"/>')
    if kind == 'technology':
        return (f'<path d="M{x-59} {y-69} H{x+59} V{y+52} H{x-59}Z" fill="{primary}"/>'
                f'<rect x="{x-42}" y="{y-51}" width="84" height="79" rx="7" fill="#20334e"/>'
                f'<path d="M{x-24} {y-13} L{x} {y-38} L{x+24} {y-13} L{x} {y+12}Z" fill="var(--accent2)"/>'
                f'<path d="M{x-37} {y+58} H{x+37}" stroke="#c2effc" stroke-width="11"/>')
    if kind == 'fantasy':
        return (f'<rect x="{x-51}" y="{y-48}" width="102" height="113" rx="5" fill="{primary}"/>'
                f'<rect x="{x-67}" y="{y-56}" width="30" height="118" fill="#8576aa"/>'
                f'<rect x="{x+37}" y="{y-56}" width="30" height="118" fill="#8576aa"/>'
                f'<path d="M{x-74} {y-55} L{x-52} {y-108} L{x-30} {y-55}Z M{x+30} {y-55} L{x+52} {y-108} L{x+74} {y-55}Z" fill="var(--accent2)"/>'
                f'<path d="M{x-16} {y+65} V{y+21} Q{x} {y-5} {x+16} {y+21} V{y+65}Z" fill="#27314b"/>')
    if kind == 'festival':
        return (f'<path d="M{x-68} {y+69} L{x-49} {y-31} L{x+49} {y-31} L{x+68} {y+69}Z" fill="{primary}"/>'
                f'<path d="M{x-76} {y-30} L{x} {y-107} L{x+76} {y-30}Z" fill="var(--accent2)"/>'
                f'<circle cx="{x}" cy="{y+8}" r="28" fill="#27314c" stroke="#ffe8cb" stroke-width="7"/>'
                f'<circle cx="{x}" cy="{y+8}" r="10" fill="var(--accent)"/>')
    if kind == 'desert':
        if i % 3 == 0:
            return (f'<path d="M{x-80} {y+68} L{x} {y-112} L{x+80} {y+68}Z" fill="{primary}"/>'
                    f'<path d="M{x-52} {y+68} L{x} {y-52} L{x+52} {y+68}Z" fill="#ae8156"/>'
                    f'<rect x="{x-12}" y="{y+16}" width="24" height="52" fill="#2b282b"/>')
        if i % 3 == 1:
            return (f'<path d="M{x-70} {y+68} V{y-34} Q{x} {y-108} {x+70} {y-34} V{y+68}Z" fill="{primary}"/>'
                    f'<ellipse cx="{x}" cy="{y-38}" rx="59" ry="20" fill="#f7dfb0" opacity=".6"/>'
                    f'<rect x="{x-25}" y="{y+5}" width="50" height="63" rx="23" fill="#4e443a"/>')
        return (f'<path d="M{x-63} {y+67} L{x-50} {y-18} L{x+48} {y-18} L{x+65} {y+67}Z" fill="{primary}"/>'
                f'<path d="M{x-78} {y-18} L{x} {y-96} L{x+78} {y-18}Z" fill="#be9a73"/>'
                f'<circle cx="{x}" cy="{y+4}" r="22" fill="#44392f" stroke="#f6dca1" stroke-width="8"/>')
    if kind == 'noir':
        if i % 3 == 0:
            return (f'<rect x="{x-59}" y="{y-106}" width="118" height="175" fill="{primary}"/>'
                    f'<rect x="{x-43}" y="{y-75}" width="26" height="32" fill="#102d3f"/>'
                    f'<rect x="{x+10}" y="{y-75}" width="26" height="32" fill="#102d3f"/>'
                    f'<rect x="{x-14}" y="{y+14}" width="28" height="55" fill="#14232d"/>')
        if i % 3 == 1:
            return (f'<path d="M{x-64} {y+67} L{x-54} {y-43} H{x+54} L{x+64} {y+67}Z" fill="{primary}"/>'
                    f'<path d="M{x-76} {y-44} L{x} {y-103} L{x+76} {y-44}Z" fill="#6d8392"/>'
                    f'<path d="M{x-27} {y+68} V{y-14} H{x+27} V{y+68}" fill="#132630"/>')
        return (f'<rect x="{x-55}" y="{y-57}" width="110" height="126" rx="6" fill="{primary}"/>'
                f'<rect x="{x-42}" y="{y-45}" width="84" height="62" fill="#193543"/>'
                f'<path d="M{x-39} {y+34} H{x+39}" stroke="#d7f1f3" stroke-width="7"/>'
                f'<circle cx="{x}" cy="{y-17}" r="19" fill="#edd2d1" opacity=".76"/>')
    # Invented themes still get geometric pavilions whose motif choice varies per object.
    if i % 3 == 0:
        return (f'<path d="M{x} {y-102} L{x+64} {y-10} L{x+36} {y+68} L{x-36} {y+68} L{x-64} {y-10}Z" fill="{primary}"/>'
                f'<path d="M{x} {y-73} L{x+31} {y-7} L{x} {y+35} L{x-31} {y-7}Z" fill="var(--accent2)"/>')
    if i % 3 == 1:
        return (f'<circle cx="{x}" cy="{y-13}" r="75" fill="{primary}"/>'
                f'<path d="M{x-54} {y+8} Q{x} {y-125} {x+54} {y+8}" fill="none" stroke="var(--accent2)" stroke-width="12"/>')
    return (f'<rect x="{x-61}" y="{y-54}" width="122" height="122" rx="24" fill="{primary}"/>'
            f'<path d="M{x-45} {y+14} L{x} {y-80} L{x+45} {y+14} L{x} {y+50}Z" fill="var(--accent2)"/>')


def build_scene(theme: str, sections: list[dict], mobile: bool = False) -> str:
    """Compose safe multi-depth SVG art; the same landmarks receive a separate mobile layout."""
    kind = family_for(theme)
    n = len(sections)
    if mobile:
        # True portrait layout: four landmarks cover most of the vertical stage.
        if n == 1:
            points = [(310, 445)]
        elif n == 2:
            points = [(220, 310), (407, 645)]
        elif n == 3:
            points = [(178, 188), (432, 435), (225, 714)]
        elif n == 4:
            points = [(170, 172), (440, 297), (180, 580), (430, 728)]
        else:
            rows = (n + 1) // 2
            points = [(170 if i % 2 == 0 else 445,
                       155 + (i // 2) * (590 / max(1, rows-1)) + (55 if i % 2 else 0))
                      for i in range(n)]
        scales = [1.08 if n <= 2 else .97 if n <= 4 else .79 if n <= 6 else .65 for _ in range(n)]
    elif n == 1:
        points, scales = [(310, 266)], [1.2]
    elif n == 2:
        points, scales = [(200, 290), (420, 290)], [1.05, .93]
    elif n == 3:
        points, scales = [(158, 342), (462, 342), (310, 190)], [.9, .88, 1.04]
    elif n == 4:
        points, scales = [(170, 192), (452, 192), (170, 341), (452, 341)], [.77, .74, .77, .74]
    else:
        points = [(x, y) for y in (190, 358) for x in (105, 240, 382, 516)][:n]
        scales = [.59 if i == 0 else .52 for i in range(n)]
    colors = ('#9bd6ff', '#ffcc87', '#b3f1c6', '#ffb6d6', '#cbb8ff', '#fbdb9c', '#a2eded', '#e1c3ff')
    svg = [f'<svg viewBox="0 0 620 {880 if mobile else 520}"><defs>']
    for i in range(n):
        svg.append(f'<linearGradient id="material-{i}" x1="0" y1="0" x2="1" y2="1">'
                   f'<stop stop-color="{colors[i]}"/><stop offset="1" stop-color="var(--accent2)"/></linearGradient>')
    svg.append('<radialGradient id="aura"><stop stop-color="var(--accent2)" stop-opacity=".22"/>'
               '<stop offset="1" stop-color="var(--accent2)" stop-opacity="0"/></radialGradient></defs>')
    # Separate world-scale terrain. In portrait, the depth bands are distributed
    # across the entire 880-unit tall composition rather than across 520 units.
    if mobile:
        svg.extend([
          '<ellipse cx="310" cy="430" rx="375" ry="445" fill="url(#aura)"/>',
          '<path d="M-80 500 L65 365 L135 427 L245 300 L355 436 L470 342 L700 492 V960 H-80Z" fill="#7298b4" opacity=".23"/>',
          '<path d="M-80 625 Q60 510 150 575 T325 535 T530 585 T700 550 V960 H-80Z" fill="#8ed0ce" opacity=".25"/>',
          '<path d="M-80 745 Q65 670 185 708 T430 692 T700 705 V960 H-80Z" fill="var(--accent2)" opacity=".24"/>',
          '<path d="M-80 830 Q155 755 302 790 T700 780 V960 H-80Z" fill="var(--accent)" opacity=".24"/>',
          '<circle cx="511" cy="92" r="36" fill="#e1f4ff" opacity=".17"/>',
          '<g class="motion-twinkle" fill="#f4f9ff" opacity=".65"><circle cx="82" cy="73" r="3"/>'
          '<circle cx="245" cy="91" r="2"/><circle cx="438" cy="59" r="2"/></g>',
        ])
    else:
        svg.extend([
          '<ellipse cx="310" cy="270" rx="345" ry="255" fill="url(#aura)"/>',
          '<path d="M-80 333 L65 240 L135 275 L245 194 L355 281 L470 213 L700 329 V570 H-80Z" fill="#7298b4" opacity=".23"/>',
          '<path d="M-80 397 Q60 310 150 374 T325 354 T530 366 T700 350 V580 H-80Z" fill="#8ed0ce" opacity=".25"/>',
          '<path d="M-80 460 Q65 401 185 440 T430 438 T700 421 V590 H-80Z" fill="var(--accent2)" opacity=".24"/>',
          '<path d="M-80 505 Q155 455 302 490 T700 474 V590 H-80Z" fill="var(--accent)" opacity=".24"/>',
          '<circle cx="511" cy="87" r="36" fill="#e1f4ff" opacity=".17"/>',
          '<g class="motion-twinkle" fill="#f4f9ff" opacity=".65"><circle cx="82" cy="73" r="3"/>'
          '<circle cx="245" cy="91" r="2"/><circle cx="438" cy="59" r="2"/></g>',
        ])
    if kind == 'guardian':
        svg.append('<path d="M-80 370 L67 316 L151 353 L273 296 L404 351 L533 305 L700 366" '
                   'fill="none" stroke="#9edbfa" stroke-width="7" opacity=".19"/>')
    elif kind == 'ocean':
        svg.append('<path d="M-80 235 Q95 206 233 234 T465 224 T700 235" '
                   'fill="none" stroke="#9dece9" stroke-width="6" opacity=".19"/>')
    elif kind == 'desert':
        svg.append('<path d="M-80 405 Q90 310 270 403 T700 380 V590 H-80Z" fill="#f9ce8d" opacity=".16"/>')
    elif kind == 'noir':
        svg.append('<path d="M-80 200 L10 200 V108 H68 V240 H120 V141 H175 V258 H252 V164 H307 V260 H700 V590 H-80Z" fill="#678b9a" opacity=".15"/>')
    elif kind == 'museum':
        svg.append('<path d="M15 131 H604 M15 444 H604" fill="none" stroke="#e6d0af" '
                   'stroke-width="12" opacity=".16"/>')
    for i,(section,(x,y)) in enumerate(zip(sections,points)):
        sid=html.escape(section['id'],quote=True)
        sc=scales[i]
        svg.append(f'<g id="landmark-{sid}" transform="translate({x} {y}) scale({sc}) translate({-x} {-y})">')
        # Contact shadow and accessible min-hit-region while keeping painted SVG as navigation.
        svg.append(f'<ellipse cx="{x}" cy="{y+75}" rx="80" ry="14" fill="#071321" opacity=".37"/>')
        svg.append(f'<rect x="{x-84}" y="{y-105}" width="168" height="186" rx="12" fill="#ffffff" opacity=".001"/>')
        svg.append(_motif(kind,x,y,i))
        svg.append(f'<path d="M{x-44} {y-46} L{x-23} {y-73}" fill="none" stroke="#e7faff" stroke-width="6" opacity=".27"/>')
        svg.append('</g>')
    svg.append('</svg>')
    result=''.join(svg)
    if len(result)>25000:
        raise ValueError('Procedural scene exceeded SVG size limit')
    return result
