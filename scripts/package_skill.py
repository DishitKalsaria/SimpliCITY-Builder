#!/usr/bin/env python3
"""Create a skill ZIP with the correct top-level skill directory."""
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parents[1]
skill = root / 'simplicity-builder'
out = root / 'SimpliCITY-Builder-Skill-v0.1.4.zip'
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for path in sorted(skill.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            z.write(path, path.relative_to(root).as_posix())
print(f'Created {out}')
