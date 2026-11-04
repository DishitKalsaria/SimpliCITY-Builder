"""Self-contained, deterministic SVG compositions for unfamiliar themes.

No image API, network access, external SVG resources, or runtime dependencies.
An AI host should still prefer bespoke source-aware art where available.
"""
from __future__ import annotations

import hashlib
import html
import re
from typing import Sequence

PALETTES = (
    ('#f4c879', '#a7b9ff', '#11182b', '#29354e'),
    ('#a7ead9', '#f5b3dc', '#10212d', '#243e47'),
    ('#ffcb9c', '#d2b9fa', '#20142c', '#41304f'),
    ('#c5e8fd', '#ffca95', '#131b30', '#2e344c'),
    ('#daef9b', '#a1d8fb', '#152128', '#2d4145'),
    ('#ffc7db', '#96e3de', '#241929', '#413246'),
)

FAMILIES = {
    'meeting': ('meeting room', 'conference room', 'boardroom', 'meeting space', 'collaboration room', 'conference table'),
    'playground': ('playground', 'play park', 'play area', 'recreation ground', 'play space'),
    'farm': ('farm', 'farmhouse', 'farmland', 'agriculture', 'agricultural', 'orchard', 'homestead', 'ranch'),
    'guardian': ('ranger', 'superhero', 'guardian', 'hero', 'mecha', 'robot', 'transformer', 'power-ranger'),
    'toon': ('toon', 'cartoon', 'comic', 'animation', 'animated', 'cel shaded', 'cel-shaded'),
    'space': ('space', 'planet', 'galaxy', 'cosmos', 'cosmic', 'observatory', 'starship', 'astronaut', 'alien'),
    'nature': ('forest', 'jungle', 'garden', 'nature', 'fairy', 'flower', 'tree', 'forest'),
    'ocean': ('ocean', 'underwater', 'sea', 'coral', 'submarine', 'aquatic'),
    'museum': ('museum', 'gallery', 'exhibit', 'history', 'archive', 'library', 'book'),
    'technology': ('technology', 'cyber', 'digital', 'future', 'science', 'lab', 'data'),
    'fantasy': ('kingdom', 'castle', 'dragon', 'magic', 'fantasy', 'medieval', 'enchanted'),
    'festival': ('music', 'festival', 'concert', 'dance', 'graffiti', 'street', 'art'),
    'desert': ('desert', 'oasis', 'dune', 'sand', 'ancient ruins', 'pyramid'),
    'noir': ('noir', 'detective', 'mystery', 'city night', 'rainy alley', 'film noir'),
    'volcanic': ('volcano', 'volcanic', 'magma', 'lava', 'caldera', 'eruption'),
}


def _has_term(text: str, term: str) -> bool:
    # Avoid partial matches: "smart" is not "art" and "farm" is not "pharmacy".
    return re.search(r'(?<![a-z0-9])' + re.escape(term).replace(r'\ ', r'[\s-]+')
                     + r'(?![a-z0-9])', text) is not None


def family_for(theme: str) -> str:
    content = theme.lower().replace('_', ' ')
    # Explicit art direction wins when it starts the prompt. Distinct room,
    # playground and farm settings win over generic story/style keywords.
    for kind in ('volcanic', 'toon'):
        if any(_has_term(content.split(' ', 1)[0], term) for term in FAMILIES[kind]):
            return kind
    for kind in ('meeting', 'playground', 'farm'):
        if any(_has_term(content, term) for term in FAMILIES[kind]):
            return kind
    if any(_has_term(content, term) for term in ('museum', 'gallery', 'exhibit')):
        return 'museum'
    for family, terms in FAMILIES.items():
        if any(_has_term(content, term) for term in terms):
            return family
    return 'invented'


THEME_PACKS = {  # accent, secondary, dark background, dark surface
    'meeting': ('#b6e6eb', '#fad8a7', '#142238', '#293e52'),
    'playground': ('#ffe494', '#97ebce', '#16283d', '#284b55'),
    'farm': ('#e7e7a8', '#9bd4ab', '#1d2b28', '#385144'),
    'guardian': ('#b4dcff', '#ffcc8e', '#111b30', '#273750'),
    'toon': ('#ffe04f', '#fff0a4', '#172b63', '#283f86'),
    'space': ('#a5e4ff', '#c7b3ff', '#0a1128', '#242544'),
    'nature': ('#d5efac', '#a5dfca', '#122822', '#26413d'),
    'ocean': ('#a5f0e6', '#a6cfff', '#091f2c', '#17384c'),
    'museum': ('#f1d9a9', '#c6c0f2', '#1c1a2c', '#343347'),
    'technology': ('#9ce8e5', '#cfb7ff', '#111b2d', '#2a3348'),
    'fantasy': ('#f5d6a0', '#cbb7f0', '#20172e', '#3c2a49'),
    'festival': ('#ffd1a0', '#ffbfe1', '#241725', '#432a43'),
    'desert': ('#f8df9c', '#e6bd83', '#282018', '#493b2d'),
    'noir': ('#a9e8dc', '#e9b6c9', '#121c22', '#29333a'),
    'volcanic': ('#ffce9a', '#ffdfb7', '#211720', '#503039'),
}


def palette_for(theme: str) -> tuple[str, str, str, str]:
    family = family_for(theme)
    if family in THEME_PACKS:
        return THEME_PACKS[family]
    checksum = hashlib.sha256(theme.encode('utf-8')).digest()[0]
    return PALETTES[checksum % len(PALETTES)]


def _semantic_shape(kind: str, title: str, i: int) -> str:
    """Choose an environment object from chapter meaning, not arbitrary index."""
    options = {
        'meeting': ('screen', 'table', 'whiteboard', 'laptop', 'bookshelf', 'chair', 'projector', 'notebook'),
        'playground': ('slide', 'swing', 'sandbox', 'climber', 'seesaw', 'roundabout', 'playhouse', 'ball'),
        'farm': ('barn', 'crops', 'tractor', 'greenhouse', 'orchard', 'windmill', 'silo', 'pond'),
    }
    words = {
        'meeting': (('screen', 'presentation', 'display', 'mission'), ('table', 'roundtable', 'discussion'),
                    ('whiteboard', 'board', 'planning', 'strategy'), ('laptop', 'computer', 'digital'),
                    ('bookshelf', 'library', 'knowledge'), ('chair', 'seat', 'conversation'),
                    ('projector', 'vision', 'ideas'), ('notebook', 'notes', 'minutes')),
        'playground': (('slide', 'adventure'), ('swing',), ('sandbox', 'sand'),
                       ('climber', 'climbing', 'rope'), ('seesaw', 'balance'),
                       ('roundabout', 'carousel'), ('playhouse', 'fort', 'house'), ('ball', 'games')),
        'farm': (('barn', 'stable', 'livestock', 'animals'), ('crop', 'field', 'harvest', 'plant'),
                 ('tractor', 'equipment', 'machine'), ('greenhouse', 'seedling', 'nursery'),
                 ('orchard', 'fruit', 'tree'), ('windmill', 'wind', 'energy'),
                 ('silo', 'grain', 'storage'), ('pond', 'water', 'irrigation')),
    }
    matches = words[kind]
    for j, synonyms in enumerate(matches):
        if any(_has_term(title.lower(), w) for w in synonyms):
            return options[kind][j]
    return options[kind][i % len(options[kind])]


def _place_object(kind: str, role: str, x: int, y: float, fill: str) -> str:
    """Original scenery-specific silhouettes; every shape remains clickable SVG."""
    if kind == 'meeting':
        if role == 'screen':
            return (f'<rect x="{x-75}" y="{y-96}" width="150" height="112" rx="8" fill="#172d42" stroke="#9ce5ed" stroke-width="8"/>'
                    f'<rect x="{x-60}" y="{y-79}" width="120" height="79" rx="4" fill="{fill}"/>'
                    f'<path d="M{x-45} {y-33} H{x-5} L{x+11} {y-49} L{x+44} {y-16}" stroke="#fff4ce" stroke-width="7" fill="none"/>'
                    f'<path d="M{x} {y+17} V{y+67} M{x-39} {y+67} H{x+39}" stroke="#a2c6cf" stroke-width="13"/>')
        if role == 'table':
            return (f'<ellipse cx="{x}" cy="{y+10}" rx="83" ry="44" fill="{fill}" stroke="#f1e6c8" stroke-width="7"/>'
                    f'<ellipse cx="{x}" cy="{y+1}" rx="58" ry="25" fill="#41697b" opacity=".75"/>'
                    f'<path d="M{x-48} {y+38} V{y+77} M{x+48} {y+38} V{y+77}" stroke="#8ab9c8" stroke-width="13"/>')
        if role == 'whiteboard':
            return (f'<rect x="{x-76}" y="{y-84}" width="152" height="116" rx="7" fill="#eef9ed" stroke="#7b9eaa" stroke-width="10"/>'
                    f'<path d="M{x-55} {y-49} H{x+12} M{x-55} {y-25} H{x+47} M{x-55} {y+1} H{x+26}" stroke="#368b93" stroke-width="8" opacity=".8"/>'
                    f'<path d="M{x-54} {y+37} L{x-63} {y+73} M{x+54} {y+37} L{x+63} {y+73}" stroke="#90a9b5" stroke-width="10"/>')
        if role == 'laptop':
            return (f'<path d="M{x-60} {y+25} L{x-54} {y-74} H{x+56} L{x+64} {y+25}Z" fill="#273c5b" stroke="#a9dae0" stroke-width="7"/>'
                    f'<rect x="{x-43}" y="{y-57}" width="87" height="66" rx="5" fill="{fill}"/>'
                    f'<path d="M{x-64} {y+26} H{x+64} L{x+83} {y+49} H{x-83}Z" fill="#c8dde0"/>')
        if role == 'bookshelf':
            books=''.join(f'<rect x="{x-55+j*22}" y="{y-55}" width="16" height="{40+(j%3)*9}" fill="{c}"/>'
                          for j,c in enumerate(('#f7d4a4','#84c5c7','#cfa6c5','#bedcae','#e5c186')))
            return (f'<rect x="{x-72}" y="{y-90}" width="144" height="156" rx="5" fill="#526b74" stroke="#c9d9ce" stroke-width="7"/>'
                    f'{books}<path d="M{x-66} {y+13} H{x+66}" stroke="#e6cfac" stroke-width="9"/>')
        if role == 'chair':
            return (f'<rect x="{x-52}" y="{y-77}" width="104" height="105" rx="28" fill="{fill}" stroke="#a8d5d0" stroke-width="8"/>'
                    f'<path d="M{x-70} {y+8} Q{x} {y+75} {x+70} {y+8} M{x} {y+54} V{y+86}" fill="none" stroke="#c8dddb" stroke-width="12"/>')
        if role == 'projector':
            return (f'<rect x="{x-69}" y="{y-40}" width="138" height="70" rx="18" fill="#c1d3d3" stroke="#6c99a9" stroke-width="8"/>'
                    f'<circle cx="{x+30}" cy="{y-4}" r="24" fill="#365a75" stroke="#85ddf1" stroke-width="8"/>'
                    f'<path d="M{x-43} {y+31} V{y+62} M{x+43} {y+31} V{y+62}" stroke="#9bcbcf" stroke-width="11"/>')
        return (f'<path d="M{x-73} {y-50} L{x+42} {y-71} L{x+73} {y+52} L{x-43} {y+67}Z" fill="#f5e8cb" stroke="#839ea7" stroke-width="7"/>'
                f'<path d="M{x-42} {y-15} L{x+22} {y-27} M{x-35} {y+7} L{x+34} {y-6} M{x-27} {y+30} L{x+40} {y+17}" stroke="#73a1a6" stroke-width="6"/>')
    if kind == 'playground':
        if role == 'slide':
            return (f'<path d="M{x-59} {y+70} L{x-19} {y-97} H{x+45} L{x+80} {y+70}Z" fill="{fill}" stroke="#ffeab2" stroke-width="8"/>'
                    f'<path d="M{x+15} {y-77} L{x+73} {y+70}" stroke="#fda35f" stroke-width="29"/>'
                    f'<path d="M{x-57} {y+61} L{x-19} {y-85}" stroke="#e5eac9" stroke-width="10"/>')
        if role == 'swing':
            return (f'<path d="M{x-71} {y+67} L{x-48} {y-85} H{x+48} L{x+71} {y+67}" fill="none" stroke="#f3e3bb" stroke-width="15"/>'
                    f'<path d="M{x-25} {y-77} V{y+23} M{x+25} {y-77} V{y+23}" stroke="#9bcfd2" stroke-width="5"/>'
                    f'<path d="M{x-36} {y+24} H{x+36}" stroke="#ffbb68" stroke-width="14"/>')
        if role == 'sandbox':
            return (f'<path d="M{x-79} {y+15} L{x+11} {y-39} L{x+85} {y+15} L{x-10} {y+70}Z" fill="#f2d292" stroke="#ab8b6a" stroke-width="11"/>'
                    f'<path d="M{x-32} {y+11} Q{x} {y-8} {x+30} {y+17}" fill="none" stroke="#fff0bc" stroke-width="8"/>'
                    f'<path d="M{x+29} {y+19} L{x+35} {y-35} M{x+14} {y-37} H{x+54}" stroke="#ed795f" stroke-width="8"/>')
        if role == 'climber':
            return (f'<path d="M{x-74} {y+71} L{x} {y-107} L{x+74} {y+71}Z" fill="none" stroke="#e1c08b" stroke-width="13"/>'
                    f'<path d="M{x-52} {y+35} H{x+52} M{x-37} {y+5} H{x+37} M{x-23} {y-27} H{x+23} M{x} {y-88} V{y+55}" stroke="#94e5cb" stroke-width="7"/>')
        if role == 'seesaw':
            return (f'<path d="M{x} {y-4} L{x-37} {y+67} H{x+37}Z" fill="#f3ca8a"/>'
                    f'<path d="M{x-86} {y+6} L{x+87} {y-62}" stroke="{fill}" stroke-width="18"/>'
                    f'<circle cx="{x-72}" cy="{y+2}" r="12" fill="#fff0b5"/><circle cx="{x+73}" cy="{y-55}" r="12" fill="#fff0b5"/>')
        if role == 'roundabout':
            return (f'<ellipse cx="{x}" cy="{y+38}" rx="80" ry="38" fill="{fill}" stroke="#ffe6aa" stroke-width="9"/>'
                    f'<path d="M{x} {y-80} V{y+38} M{x-54} {y+15} L{x} {y-80} L{x+54} {y+15}" fill="none" stroke="#f4dfbc" stroke-width="10"/>')
        if role == 'playhouse':
            return (f'<path d="M{x-69} {y-20} L{x} {y-97} L{x+69} {y-20}Z" fill="#f3bb85"/>'
                    f'<rect x="{x-60}" y="{y-22}" width="120" height="93" rx="6" fill="{fill}"/>'
                    f'<path d="M{x-18} {y+70} V{y+5} H{x+18} V{y+70}" fill="#2f6577"/><circle cx="{x+40}" cy="{y+8}" r="12" fill="#d9f3bb"/>')
        return (f'<circle cx="{x}" cy="{y-5}" r="65" fill="{fill}" stroke="#fff0b7" stroke-width="8"/>'
                f'<path d="M{x-55} {y+2} Q{x} {y-58} {x+55} {y+2} M{x} {y-68} V{y+60}" stroke="#ec7c71" stroke-width="11" fill="none"/>')
    # Farm objects tell an agricultural story without a fantasy-building template.
    if role == 'barn':
        return (f'<path d="M{x-77} {y-18} L{x} {y-101} L{x+77} {y-18}Z" fill="#d88c74" stroke="#f6e3c2" stroke-width="7"/>'
                f'<rect x="{x-63}" y="{y-18}" width="126" height="88" fill="{fill}"/>'
                f'<path d="M{x-31} {y+69} V{y+5} H{x+31} V{y+69} M{x-31} {y+5} L{x+31} {y+69} M{x+31} {y+5} L{x-31} {y+69}" fill="none" stroke="#e9d3aa" stroke-width="8"/>')
    if role == 'crops':
        crops=''.join(f'<path d="M{x+dx} {y+67} V{y-17} M{x+dx} {y+3} Q{x+dx-20} {y-27} {x+dx-30} {y-5} M{x+dx} {y-12} Q{x+dx+18} {y-44} {x+dx+27} {y-17}" stroke="#9ed29a" stroke-width="9" fill="none"/>' for dx in (-45,0,45))
        return f'<path d="M{x-87} {y+70} L{x-60} {y-35} H{x+63} L{x+87} {y+70}Z" fill="#644d37"/>'+crops
    if role == 'tractor':
        return (f'<rect x="{x-60}" y="{y-48}" width="86" height="88" rx="8" fill="{fill}"/>'
                f'<rect x="{x-43}" y="{y-77}" width="54" height="48" rx="4" fill="#a9d6d1"/>'
                f'<path d="M{x+26} {y-3} H{x+83} V{y+45} H{x-60}" fill="#dfbd6d"/>'
                f'<circle cx="{x-40}" cy="{y+49}" r="28" fill="#283e38" stroke="#d5dcc0" stroke-width="8"/>'
                f'<circle cx="{x+63}" cy="{y+52}" r="19" fill="#283e38" stroke="#d5dcc0" stroke-width="7"/>')
    if role == 'greenhouse':
        return (f'<path d="M{x-74} {y+69} V{y-22} L{x} {y-96} L{x+74} {y-22} V{y+69}Z" fill="{fill}" stroke="#d4e8cf" stroke-width="8"/>'
                f'<path d="M{x} {y-93} V{y+67} M{x-70} {y-19} H{x+70} M{x-35} {y-59} V{y+69} M{x+35} {y-59} V{y+69}" stroke="#e9f3de" stroke-width="6"/>'
                f'<path d="M{x-53} {y+58} Q{x-47} {y+4} {x-20} {y+20} M{x+15} {y+58} Q{x+36} {y+0} {x+50} {y+37}" stroke="#3e8a59" stroke-width="11" fill="none"/>')
    if role == 'orchard':
        return (f'<path d="M{x} {y+71} V{y-15} M{x-55} {y+65} L{x-28} {y+3}" stroke="#83604a" stroke-width="17"/>'
                f'<circle cx="{x}" cy="{y-55}" r="59" fill="{fill}"/><circle cx="{x-49}" cy="{y-22}" r="36" fill="{fill}"/>'
                f'<circle cx="{x+18}" cy="{y-55}" r="9" fill="#f0a679"/><circle cx="{x-24}" cy="{y-33}" r="9" fill="#f0a679"/>')
    if role == 'windmill':
        return (f'<path d="M{x-38} {y+72} L{x-15} {y-62} H{x+15} L{x+38} {y+72}Z" fill="#e8d7b0"/>'
                f'<circle cx="{x}" cy="{y-65}" r="18" fill="#a67f63"/>'
                f'<path d="M{x} {y-65} L{x-24} {y-126} L{x+8} {y-107}Z M{x} {y-65} L{x+77} {y-88} L{x+64} {y-52}Z M{x} {y-65} L{x+34} {y+10} L{x-4} {y}Z M{x} {y-65} L{x-73} {y-33} L{x-61} {y-71}Z" fill="{fill}"/>')
    if role == 'silo':
        return (f'<rect x="{x-49}" y="{y-73}" width="98" height="142" fill="{fill}"/>'
                f'<ellipse cx="{x}" cy="{y-73}" rx="49" ry="20" fill="#d4d9af"/>'
                f'<path d="M{x-46} {y-30} H{x+46} M{x-46} {y+11} H{x+46} M{x-46} {y+47} H{x+46}" stroke="#f1e3bd" stroke-width="6" opacity=".65"/>')
    return (f'<ellipse cx="{x}" cy="{y+21}" rx="88" ry="45" fill="#5aabac" stroke="#c3e3bb" stroke-width="9"/>'
            f'<path d="M{x-56} {y+10} Q{x} {y-5} {x+54} {y+13}" fill="none" stroke="#b2e3d5" stroke-width="5"/>')


def _motif(kind: str, x: int, y: float, i: int) -> str:
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
    if kind == 'volcanic':
        # Silhouettes are actual selectable structures: citadel, forge,
        # observatory and refinery, rather than identical map markers.
        if i % 4 == 0:
            return (f'<path d="M{x-78} {y+66} L{x-64} {y-32} L{x-30} {y-52} L{x} {y-108} '
                    f'L{x+30} {y-52} L{x+64} {y-32} L{x+78} {y+66}Z" fill="{primary}"/>'
                    f'<path d="M{x-25} {y+65} V{y-4} L{x} {y-39} L{x+25} {y-4} V{y+65}Z" fill="#271825"/>'
                    f'<path d="M{x} {y-96} V{y-45} M{x-53} {y-4} H{x+53}" stroke="#ffd4a2" stroke-width="8"/>')
        if i % 4 == 1:
            return (f'<path d="M{x-72} {y+65} V{y-20} L{x} {y-72} L{x+72} {y-20} V{y+65}Z" fill="{primary}"/>'
                    f'<path d="M{x-45} {y+65} V{y+2} Q{x} {y-48} {x+45} {y+2} V{y+65}Z" fill="#211622"/>'
                    f'<path d="M{x-23} {y+65} V{y+10} Q{x} {y-18} {x+23} {y+10} V{y+65}Z" fill="#ffb86f"/>'
                    f'<path d="M{x-59} {y-16} V{y-75} M{x+57} {y-16} V{y-87}" stroke="#9d7880" stroke-width="13"/>')
        if i % 4 == 2:
            return (f'<path d="M{x-68} {y+65} L{x-56} {y-52} H{x+56} L{x+68} {y+65}Z" fill="{primary}"/>'
                    f'<ellipse cx="{x}" cy="{y-52}" rx="56" ry="25" fill="#42313d" stroke="#ffc28b" stroke-width="7"/>'
                    f'<path d="M{x-30} {y+44} V{y-13} M{x} {y+44} V{y-26} M{x+30} {y+44} V{y-13}" stroke="#ffcc91" stroke-width="12"/>')
        return (f'<path d="M{x-76} {y+66} V{y-19} L{x-45} {y-51} H{x+45} L{x+76} {y-19} V{y+66}Z" fill="{primary}"/>'
                f'<path d="M{x-60} {y-20} H{x+60}" stroke="#ffa768" stroke-width="10"/>'
                f'<path d="M{x-34} {y+17} H{x+34} M{x-34} {y+39} H{x+34}" stroke="#32222b" stroke-width="14"/>'
                f'<path d="M{x+47} {y-51} V{y-111} H{x+62} V{y-51}" fill="#71535a"/>')
    if kind == 'toon':
        # Original cartoon-city vocabulary: bold ink, flat primary colors and
        # squash-and-stretch silhouettes, not protected characters/logos.
        if i % 3 == 0:
            return (f'<path d="M{x-68} {y+65} L{x-58} {y-35} L{x-20} {y-35} L{x} {y-110} '
                    f'L{x+24} {y-35} L{x+60} {y-35} L{x+68} {y+65}Z" '
                    f'fill="{primary}" stroke="#10152f" stroke-width="12" stroke-linejoin="round"/>'
                    f'<circle cx="{x}" cy="{y-39}" r="22" fill="#ffe04f" stroke="#10152f" stroke-width="8"/>'
                    f'<path d="M{x-33} {y+65} V{y+9} H{x+33} V{y+65}" fill="#ff6b69" stroke="#10152f" stroke-width="8"/>')
        if i % 3 == 1:
            return (f'<path d="M{x-77} {y+60} Q{x-93} {y-12} {x-35} {y-73} '
                    f'Q{x} {y-128} {x+35} {y-73} Q{x+93} {y-12} {x+77} {y+60}Z" '
                    f'fill="{primary}" stroke="#10152f" stroke-width="12"/>'
                    f'<path d="M{x-42} {y+38} H{x+42} V{y+61} H{x-42}Z" fill="#ffe04f" stroke="#10152f" stroke-width="7"/>')
        return (f'<rect x="{x-66}" y="{y-68}" width="132" height="130" rx="19" '
                f'fill="{primary}" stroke="#10152f" stroke-width="12"/>'
                f'<path d="M{x-63} {y-69} L{x} {y-120} L{x+63} {y-69}Z" '
                f'fill="#ff6b69" stroke="#10152f" stroke-width="9"/>'
                f'<circle cx="{x}" cy="{y-16}" r="23" fill="#ffe04f" stroke="#10152f" stroke-width="8"/>')
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


# Family scenes use different spatial grammar and lighting, not a shared
# mountain silhouette recolored for different subjects. The variants remain
# deterministic across machines and do not require an image-generation API.
FAMILY_LAYOUTS = {
    'meeting': (((165, 207), (451, 217), (164, 341), (455, 340)),
                ((178, 191), (436, 223), (171, 346), (456, 333))),
    'playground': (((160, 207), (446, 201), (154, 338), (452, 339)),
                   ((162, 189), (457, 215), (175, 327), (439, 346))),
    'farm': (((160, 196), (456, 208), (164, 343), (450, 340)),
             ((172, 206), (446, 185), (157, 334), (460, 347))),
    'volcanic': (((139, 224), (466, 212), (165, 325), (458, 312)),
                 ((165, 188), (465, 249), (141, 322), (474, 315))),
    'guardian': (((167, 198), (451, 190), (159, 323), (453, 317)),
                 ((155, 178), (469, 210), (167, 320), (452, 322))),
    'space': (((144, 198), (465, 177), (192, 321), (455, 317)),
              ((169, 177), (455, 206), (165, 321), (468, 312))),
    'ocean': (((161, 171), (466, 216), (145, 321), (469, 320)),
              ((157, 207), (470, 184), (181, 317), (448, 304))),
    'toon': (((152, 195), (453, 191), (171, 315), (464, 314)),
             ((166, 214), (458, 178), (157, 317), (444, 309))),
}


def _layout(kind: str, count: int, mobile: bool, theme: str) -> tuple[list[tuple[int, float]], list[float]]:
    """Depth-aware, family-specific positions with two stable variants/count."""
    seed = hashlib.sha256(theme.lower().encode('utf-8')).digest()[1] % 2
    family = FAMILY_LAYOUTS.get(kind)
    # Subtle family offsets apply at every landmark count, while the four-site
    # hero layout uses more explicitly authored slopes/orbits/depth bands.
    family_shift = {'volcanic': -15, 'guardian': 9, 'space': 18,
                    'ocean': -6, 'toon': 15, 'meeting': 2, 'playground': -6, 'farm': 8}.get(kind, 0)
    points: Sequence[tuple[int, float]]
    if mobile:
        # Preserve generous vertical separation and safe touch targets.
        basics = ((170, 172), (445, 304), (172, 568), (438, 727))
        if kind == 'ocean':
            basics = ((188, 177), (428, 346), (168, 547), (433, 742))
        elif kind == 'space':
            basics = ((166, 208), (445, 302), (186, 555), (428, 715))
        elif kind == 'volcanic':
            basics = ((176, 188), (444, 336), (159, 566), (437, 739))
        if count == 1:
            points = [(310, 445)]
        elif count == 2:
            points = [(216, 317), (414, 639)]
        elif count == 3:
            points = [(175, 207), (440, 429), (213, 702)]
        elif count == 4:
            points = list(basics)
        else:
            rows = (count + 1)//2
            # Four deliberate depth bands. Preserve margins for motifs and
            # room for readable callouts at compact phone sizes.
            row_y = {3: (160, 429, 714), 4: (147, 343, 538, 738)}[rows]
            points = [(168 if i%2 == 0 else 446,
                       row_y[i//2]+(9 if i%2 else 0)) for i in range(count)]
        delta = -11 if seed == 0 else 11
        if count >= 3:
            points = [(int(x+(delta if i%2 == 0 else -delta)), y) for i,(x,y) in enumerate(points)]
        elif count <= 2:
            points = [(int(x + (family_shift if i%2 == 0 else -family_shift)), y)
                      for i,(x,y) in enumerate(points)]
        scale = 1.08 if count <= 2 else .93 if count <= 4 else .75 if count <= 6 else .62
        return list(points), [scale for _ in points]
    if count == 1:
        return [(310 + family_shift + (12 if seed else -12), 267)], [1.19]
    if count == 2:
        base = [(199, 290), (422, 286)] if seed else [(210, 272), (416, 306)]
        return [(x+(family_shift if i%2 == 0 else -family_shift),y) for i,(x,y) in enumerate(base)], [1.04, .91]
    if count == 3:
        base = [(156, 331), (465, 338), (315, 178)] if seed else [(169, 340), (448, 317), (311, 193)]
        return [(x+(family_shift if i%2 == 0 else -family_shift),y) for i,(x,y) in enumerate(base)], [.87, .85, 1.02]
    if count == 4:
        positions = family[seed] if family else ((155, 194), (459, 196), (159, 320), (461, 315))
        return list(positions), [.87, .75, .74, .69]
    # A dense view retains two generous banks of objects and an unobstructed
    # center path. Four columns at 1440px made targets and plaques too small.
    rows = (count + 1)//2
    row_y = {3: (132, 275, 416), 4: (103, 210, 319, 428)}[rows]
    points = [(166 if i%2 == 0 else 455, row_y[i//2]) for i in range(count)]
    shift = 9 if seed else -9
    return [(x+(shift if i%2==0 else -shift), y) for i,(x,y) in enumerate(points)], [0.62 if count<=6 else .56]*count


def _environment(kind: str, mobile: bool) -> str:
    h = 880 if mobile else 520
    horizon = int(h*.59)
    ridge = int(h*.77)
    sky = ('#1c1624' if kind == 'volcanic' else '#09182b' if kind == 'ocean'
           else '#0b1133' if kind == 'space' else '#254881' if kind == 'toon'
           else '#1c2746')
    art = [
        '<defs><linearGradient id="v21-horizon" x1="0" y1="0" x2="0" y2="1">'
        f'<stop stop-color="{sky}" stop-opacity=".96"/>'
        '<stop offset="1" stop-color="var(--accent2)" stop-opacity=".13"/></linearGradient>'
        '<linearGradient id="v21-ridge" x1="0" y1="0" x2="0" y2="1">'
        '<stop stop-color="var(--accent2)" stop-opacity=".38"/>'
        '<stop offset="1" stop-color="var(--accent)" stop-opacity=".08"/></linearGradient>'
        '<radialGradient id="v21-light"><stop stop-color="var(--accent2)" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="var(--accent2)" stop-opacity="0"/></radialGradient></defs>',
        f'<rect x="0" y="0" width="620" height="{h}" fill="url(#v21-horizon)"/>',
    ]
    if kind == 'meeting':
        # An interior with vanishing lines, wall lights, window and floor.
        wall = int(h*.56)
        art.extend([
            f'<path d="M0 0 H620 V{wall} L310 {int(h*.68)} L0 {wall}Z" fill="#263e55"/>',
            f'<path d="M0 0 L110 {int(h*.09)} V{wall-8} L0 {wall+50}Z" fill="#192d43"/>',
            f'<path d="M620 0 L510 {int(h*.09)} V{wall-8} L620 {wall+50}Z" fill="#1b3148"/>',
            f'<path d="M0 {wall+50} L310 {int(h*.68)} L620 {wall+50} V{h} H0Z" fill="#52646a"/>',
            f'<path d="M0 {wall+50} L310 {int(h*.68)} L620 {wall+50} M310 {int(h*.68)} V{h} M0 {int(h*.88)} H620" stroke="#a4abb0" stroke-width="3" opacity=".34" fill="none"/>',
            f'<rect x="225" y="{int(h*.09)}" width="170" height="{int(h*.27)}" rx="5" fill="#7bb1c6" stroke="#a1bdc4" stroke-width="13"/>',
            f'<path d="M310 {int(h*.09)} V{int(h*.36)} M225 {int(h*.23)} H395" stroke="#d3e5e3" stroke-width="7"/>',
            f'<path d="M247 {int(h*.29)} Q296 {int(h*.22)} 348 {int(h*.30)} T396 {int(h*.27)}" fill="none" stroke="#ecddc8" stroke-width="5" opacity=".45"/>',
            f'<path d="M310 {int(h*.01)} V{int(h*.12)}" stroke="#d2d9c9" stroke-width="9"/>',
            f'<ellipse cx="310" cy="{int(h*.15)}" rx="103" ry="19" fill="#f4dcb7" opacity=".22"/>',
            f'<ellipse cx="310" cy="{int(h*.52)}" rx="252" ry="{int(h*.29)}" fill="url(#v21-light)" opacity=".45"/>',
        ])
    elif kind == 'playground':
        field = int(h*.52)
        art.extend([
            f'<rect x="0" y="0" width="620" height="{field}" fill="#4c8fa9"/>',
            f'<circle cx="503" cy="{int(h*.14)}" r="45" fill="#ffe7a6"/>',
            f'<path d="M0 {field} Q155 {field-73} 310 {field-12} T620 {field-32} V{h} H0Z" fill="#52917c"/>',
            f'<path d="M0 {int(h*.72)} Q150 {int(h*.65)} 320 {int(h*.75)} T620 {int(h*.68)} V{h} H0Z" fill="#3e7a67"/>',
            f'<path d="M310 {h} Q150 {int(h*.74)} 320 {int(h*.55)} T305 {int(h*.35)}" fill="none" stroke="#e9d5ac" stroke-width="45" opacity=".5"/>',
            f'<path d="M0 {field-22} H620" stroke="#e6d9b6" stroke-width="8"/>',
            f'<path d="M41 {field-5} V{field+64} M86 {field-8} V{field+61} M540 {field-8} V{field+62} M584 {field-8} V{field+64}" stroke="#e9d7b0" stroke-width="10"/>',
            f'<circle cx="65" cy="{int(h*.35)}" r="40" fill="#6eb697" opacity=".65"/>',
            f'<circle cx="566" cy="{int(h*.42)}" r="35" fill="#84c69d" opacity=".6"/>',
        ])
    elif kind == 'farm':
        hill = int(h*.48)
        art.extend([
            f'<rect width="620" height="{hill}" fill="#799d9a"/>',
            f'<circle cx="505" cy="{int(h*.13)}" r="51" fill="#f5ddb1" opacity=".85"/>',
            f'<path d="M0 {hill} Q140 {hill-97} 294 {hill-18} T620 {hill-82} V{h} H0Z" fill="#65866a"/>',
            f'<path d="M0 {int(h*.66)} Q160 {int(h*.55)} 306 {int(h*.69)} T620 {int(h*.61)} V{h} H0Z" fill="#8ca16a"/>',
            f'<path d="M0 {int(h*.82)} Q188 {int(h*.72)} 340 {int(h*.86)} T620 {int(h*.74)} V{h} H0Z" fill="#536d4e"/>',
            f'<path d="M-20 {h} Q120 {int(h*.80)} 302 {int(h*.65)} T650 {int(h*.55)}" fill="none" stroke="#dfc69b" stroke-width="32" opacity=".57"/>',
        ])
        for j in range(7):
            yline = int(h*.57)+j*int(h*.065)
            art.append(f'<path d="M-10 {yline} Q155 {yline-35} 310 {yline+8} T630 {yline-25}" fill="none" stroke="#c5c887" stroke-width="4" opacity=".35"/>')
    if kind == 'volcanic':
        crater = int(h*.27)
        art.extend([
            f'<ellipse cx="316" cy="{crater}" rx="225" ry="{int(h*.26)}" fill="url(#v21-light)"/>',
            f'<path d="M-40 {horizon+50} L142 {horizon-52} L221 {crater+72} L275 {crater-37} '
            f'L302 {crater-11} L340 {crater-11} L373 {crater-37} L421 {crater+69} '
            f'L660 {horizon+47} V{h+20} H-40Z" fill="#291b25" stroke="#a35f46" stroke-width="5"/>',
            f'<ellipse cx="321" cy="{crater-10}" rx="62" ry="16" fill="#ffb366" stroke="#ff6829" stroke-width="10"/>',
            f'<path d="M310 {crater-7} Q264 {crater+80} 287 {horizon+15} '
            f'T187 {h-18} M335 {crater-8} Q399 {crater+75} 379 {horizon+15} T493 {h-12}" '
            'fill="none" stroke="#d44d28" stroke-width="19" opacity=".75"/>',
            f'<path d="M310 {crater-7} Q264 {crater+80} 287 {horizon+15} '
            f'T187 {h-18} M335 {crater-8} Q399 {crater+75} 379 {horizon+15} T493 {h-12}" '
            'fill="none" stroke="#ffb162" stroke-width="6" opacity=".93"/>',
            f'<path d="M-30 {ridge} Q90 {ridge-57} 188 {ridge-18} T400 {ridge-22} T670 {ridge-36} '
            f'V{h+30} H-30Z" fill="#261924" opacity=".73"/>',
            f'<g class="motion-drift" fill="#a27c81" opacity=".3"><ellipse cx="304" cy="{crater-80}" rx="80" ry="25"/>'
            f'<ellipse cx="351" cy="{crater-129}" rx="101" ry="23"/></g>',
        ])
        for i in range(20):
            x = 45 + (i * 137) % 545
            y = 30 + (i * 83) % max(100, int(h * .56))
            art.append(f'<circle class="motion-twinkle" cx="{x}" cy="{y}" r="{1+i%3}" fill="#ffb162" opacity=".58"/>')
    elif kind == 'space':
        art.extend([
            f'<ellipse cx="311" cy="{int(h*.44)}" rx="273" ry="{int(h*.30)}" '
            'fill="none" stroke="#9bdaf9" stroke-width="7" opacity=".38"/>',
            f'<ellipse cx="311" cy="{int(h*.44)}" rx="193" ry="{int(h*.20)}" '
            'fill="none" stroke="#d0adff" stroke-width="4" opacity=".52"/>',
            f'<circle cx="310" cy="{int(h*.44)}" r="84" fill="#333c88" opacity=".48"/>',
            f'<circle cx="465" cy="{int(h*.13)}" r="44" fill="#a3b8e7" opacity=".35"/>',
            f'<ellipse cx="310" cy="{int(h*.47)}" rx="238" ry="{int(h*.18)}" '
            'fill="url(#v21-light)" opacity=".46"/>',
        ])
        for i in range(29):
            x = 19 + (i * 173) % 581
            y = 17 + (i * 97) % (h - 34)
            art.append(f'<circle class="motion-twinkle" cx="{x}" cy="{y}" r="{1+i%3}" fill="#deecff" opacity=".7"/>')
    elif kind == 'ocean':
        art.extend([
            f'<path d="M0 {int(h*.17)} Q148 {int(h*.12)} 311 {int(h*.18)} '
            f'T620 {int(h*.16)}" fill="none" stroke="#b4f4ee" stroke-width="12" opacity=".32"/>',
            f'<path d="M-30 {horizon} Q130 {horizon-96} 241 {horizon-12} '
            f'T490 {horizon-47} T650 {horizon} V{h+20} H-30Z" fill="#114259" opacity=".6"/>',
            f'<path d="M-30 {ridge} Q110 {ridge-97} 255 {ridge-19} '
            f'T500 {ridge-54} T660 {ridge+9} V{h+20} H-30Z" fill="#143c51" opacity=".72"/>',
            f'<path d="M63 {h-30} Q35 {h-130} 97 {h-186} M510 {h-20} '
            f'Q472 {h-167} 551 {h-213}" fill="none" stroke="#7bbcb3" stroke-width="16" opacity=".48"/>',
        ])
        for i in range(15):
            x = 29 + (i * 133) % 558
            y = 26 + (i * 101) % (h - 60)
            art.append(f'<circle cx="{x}" cy="{y}" r="{3+i%4}" fill="none" stroke="#9cf4e2" stroke-width="2" opacity=".38"/>')
    elif kind == 'toon':
        art.extend([
            f'<circle cx="498" cy="{int(h*.18)}" r="60" fill="#ffe04f" stroke="#10152f" stroke-width="9"/>',
            f'<path d="M-25 {horizon+13} L96 {horizon-124} L190 {horizon-36} '
            f'L321 {horizon-173} L455 {horizon-54} L626 {horizon-128} L655 {h+20} H-25Z" '
            'fill="#6dc2eb" stroke="#10152f" stroke-width="9" stroke-linejoin="round"/>',
            f'<path d="M-25 {ridge} Q95 {ridge-76} 199 {ridge-24} '
            f'T460 {ridge-50} T660 {ridge-12} V{h+20} H-25Z" '
            'fill="#388abf" stroke="#10152f" stroke-width="8"/>',
            f'<path d="M-20 {h-33} Q140 {h-97} 306 {h-49} '
            f'T650 {h-58}" fill="none" stroke="#ffe04f" stroke-width="19" opacity=".73"/>',
        ])
    else:
        art.extend([
            f'<ellipse cx="389" cy="{int(h*.26)}" rx="230" ry="{int(h*.3)}" fill="url(#v21-light)"/>',
            f'<path d="M-40 {horizon+4} L74 {horizon-121} L147 {horizon-55} '
            f'L235 {horizon-159} L344 {horizon-39} L435 {horizon-143} '
            f'L549 {horizon-59} L650 {horizon-116} V{h+30} H-40Z" '
            'fill="url(#v21-ridge)" opacity=".63"/>',
            f'<path d="M-30 {ridge} Q110 {ridge-103} 225 {ridge-36} '
            f'T470 {ridge-34} T650 {ridge-53} V{h+30} H-30Z" '
            'fill="#26344d" opacity=".42"/>',
        ])
        if kind == 'guardian':
            art.append(f'<path d="M80 {horizon+32} L80 {horizon-75} L123 {horizon-116} '
                       f'L165 {horizon-75} L165 {horizon+32} M450 {horizon+17} '
                       f'L450 {horizon-67} L491 {horizon-106} L534 {horizon-67} L534 {horizon+17}" '
                       'fill="none" stroke="#b4dcff" stroke-width="12" opacity=".18"/>')
    return ''.join(art)


def _site(x: int, y: float, i: int, kind: str) -> str:
    """Terrain foundations replace floating generic shadow ellipses."""
    if kind in {'meeting', 'playground', 'farm'}:
        base = '#385463' if kind == 'meeting' else '#4b8a72' if kind == 'playground' else '#60764f'
        rim = '#e8ddc3' if kind == 'meeting' else '#d9d99c'
        return (f'<ellipse cx="{x}" cy="{y+57}" rx="92" ry="28" fill="{base}" stroke="{rim}" '
                'stroke-width="5" opacity=".72"/>')
    if kind == 'volcanic':
        return (f'<path d="M{x-101} {y+54} L{x-67} {y+34} H{x+59} L{x+100} {y+56} '
                f'L{x+74} {y+85} L{x+12} {y+95} L{x-69} {y+83}Z" '
                'fill="#35232b" stroke="#b76b4d" stroke-width="4"/>'
                f'<path d="M{x-66} {y+84} L{x-35} {y+75} L{x-8} {y+92} '
                f'M{x+23} {y+85} L{x+52} {y+68}" fill="none" '
                'stroke="#ff9b51" stroke-width="5" opacity=".8"/>')
    if kind == 'space':
        return (f'<path d="M{x-94} {y+59} Q{x-91} {y+36} {x-61} {y+39} '
                f'Q{x} {y+24} {x+61} {y+38} Q{x+105} {y+42} {x+93} {y+68} '
                f'Q{x} {y+102} {x-94} {y+59}Z" fill="#25335c" '
                'stroke="#a5e4ff" stroke-width="4" opacity=".82"/>')
    if kind == 'ocean':
        return (f'<path d="M{x-99} {y+59} Q{x-61} {y+12} {x-24} {y+41} '
                f'Q{x+11} {y+4} {x+53} {y+40} Q{x+105} {y+50} {x+93} {y+81} '
                f'Q{x} {y+108} {x-99} {y+59}Z" fill="#1c6172" '
                'stroke="#8bdfce" stroke-width="4" opacity=".85"/>')
    if kind == 'toon':
        return (f'<path d="M{x-102} {y+57} L{x-68} {y+33} H{x+69} '
                f'L{x+102} {y+57} L{x+68} {y+84} H{x-67}Z" '
                'fill="#ffe04f" stroke="#10152f" stroke-width="9" stroke-linejoin="round"/>')
    return (f'<path d="M{x-99} {y+63} L{x-59} {y+34} H{x+64} L{x+99} {y+62} '
            f'L{x+63} {y+86} H{x-72}Z" fill="#23334a" '
            'stroke="var(--accent2)" stroke-width="4" opacity=".8"/>')


def build_scene(theme: str, sections: list[dict], mobile: bool = False) -> str:
    """Compose safe multi-depth SVG art; the same landmarks receive a separate mobile layout."""
    kind = family_for(theme)
    n = len(sections)
    points, scales = _layout(kind, n, mobile, theme)
    # Material hues are local to each family; no pastel rainbow in volcanic
    # geology. Each facet has controlled variety without palette drift.
    colors_by_family = {
        'volcanic': ('#9b5d4b', '#d68b58', '#6f4651', '#b86f4c', '#f2a064'),
        'guardian': ('#8bb8df', '#7199c0', '#bfd9ed', '#8398c8'),
        'space': ('#677bc0', '#8992d5', '#617faf', '#a0a6e2'),
        'ocean': ('#37a5a8', '#61c1b7', '#3d8eac', '#86c9bf'),
        'toon': ('#ff6b69', '#6dc2eb', '#ffe04f', '#ff8a54'),
        'meeting': ('#8cbaca', '#b7d6c3', '#e6d0ac', '#83c2d5'),
        'playground': ('#f6a963', '#8ed2c4', '#f5cc82', '#9cc6e9'),
        'farm': ('#ba7158', '#83ad77', '#d5bc70', '#89cbb2'),
    }
    colors = colors_by_family.get(kind, ('#9bd6ff','#ffcc87','#b3f1c6','#ffb6d6'))
    svg = [f'<svg viewBox="0 0 620 {880 if mobile else 520}"><defs>']
    for i in range(n):
        svg.append(f'<linearGradient id="material-{i}" x1="0" y1="0" x2="1" y2="1">'
                   f'<stop stop-color="{colors[i%len(colors)]}"/><stop offset="1" stop-color="var(--accent2)"/></linearGradient>')
    svg.append('<radialGradient id="aura"><stop stop-color="var(--accent2)" stop-opacity=".22"/>'
               '<stop offset="1" stop-color="var(--accent2)" stop-opacity="0"/></radialGradient></defs>')
    # Separate world-scale terrain. In portrait, the depth bands are distributed
    # across the entire 880-unit tall composition rather than across 520 units.
    # Every theme family now authors its own environment and depth grammar.
    # No shared mountain/sun/stars backdrop survives to recolor another world.
    svg.append(f'<ellipse cx="310" cy="{450 if mobile else 270}" rx="345" '
               f'ry="{440 if mobile else 252}" fill="url(#aura)" opacity=".22"/>')
    svg.append(_environment(kind, mobile))
    # Landmarks form one explorable place: faint terrain paths lead between
    # nearby destinations, but remain decorative and non-interactive.
    for (ax, ay), (bx, by) in zip(points, points[1:]) if kind not in {'meeting', 'playground', 'farm'} else []:
        cx = (ax + bx) / 2
        cy = (ay + by) / 2 + (21 if mobile else 29)
        svg.append(f'<path d="M{ax} {ay+74} Q{cx:.1f} {cy+88:.1f} {bx} {by+74}" '
                   'fill="none" stroke="var(--accent2)" stroke-width="4" '
                   'opacity=".23" />')
    for i,(section,(x,y)) in enumerate(zip(sections,points)):
        sid=html.escape(section['id'],quote=True)
        sc=scales[i]
        svg.append(f'<g id="landmark-{sid}" transform="translate({x} {y}) scale({sc}) translate({-x} {-y})">')
        # Contact shadow and accessible min-hit-region while keeping painted SVG as navigation.
        if i == 0 and not mobile:
            svg.append(f'<ellipse cx="{x}" cy="{y-25}" rx="118" ry="137" fill="url(#aura)" opacity=".48"/>')
        svg.append(_site(x, y, i, kind))
        svg.append(f'<rect x="{x-84}" y="{y-105}" width="168" height="186" rx="12" fill="#ffffff" opacity=".001"/>')
        if kind in {'meeting', 'playground', 'farm'}:
            title = str(section.get('name') or section.get('title') or '')
            svg.append(_place_object(kind, _semantic_shape(kind, title, i), x, y, f'url(#material-{i})'))
        else:
            svg.append(_motif(kind,x,y,i))
        svg.append(f'<path d="M{x-44} {y-46} L{x-23} {y-73}" fill="none" stroke="#e7faff" stroke-width="6" opacity=".27"/>')
        svg.append('</g>')
    svg.append('</svg>')
    result=''.join(svg)
    if len(result)>25000:
        raise ValueError('Procedural scene exceeded SVG size limit')
    return result
