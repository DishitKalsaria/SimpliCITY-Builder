"""Strip common photographic metadata without re-encoding image pixels.

Python standard-library parsing only. Pillow is OPTIONAL for downscaling.
Reject malformed or unrecognized image structures instead of embedding them.
"""
from __future__ import annotations

import io
import struct
import warnings
import zlib
from pathlib import Path

RAW_LIMIT = 10_000_000  # base64 expands to ~13.34 MB; complete HTML capped at 16 MB
WARN_LIMIT = 4_000_000
OUTPUT_LIMIT = 16_000_000
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'


def jpeg_clean(raw: bytes) -> bytes:
    if not raw.startswith(b'\xff\xd8\xff'):
        raise ValueError('Malformed JPEG')
    result = bytearray(raw[:2])
    offset = 2
    # Retain the byte-for-byte entropy-coded scan after SOS.
    while offset < len(raw):
        if raw[offset] != 0xff:
            raise ValueError('Malformed JPEG marker')
        marker_start = offset
        while offset < len(raw) and raw[offset] == 0xff:
            offset += 1
        if offset == len(raw):
            raise ValueError('Truncated JPEG')
        marker = raw[offset]
        offset += 1
        if marker in (0xd9, 0x01) or 0xd0 <= marker <= 0xd7:
            result.extend(raw[marker_start:offset])
            if marker == 0xd9:
                if offset != len(raw):
                    raise ValueError('Unexpected data after JPEG end')
                return bytes(result)
            continue
        if offset + 2 > len(raw):
            raise ValueError('Truncated JPEG segment')
        length = int.from_bytes(raw[offset:offset + 2], 'big')
        end = offset + length
        if length < 2 or end > len(raw):
            raise ValueError('Invalid JPEG segment length')
        if marker == 0xda:
            result.extend(raw[marker_start:])
            return bytes(result)
        if marker not in (0xe1, 0xed):  # APP1 / APP13: EXIF, XMP, Photoshop/IPTC
            result.extend(raw[marker_start:end])
        offset = end
    raise ValueError('JPEG missing image scan')


def png_clean(raw: bytes) -> bytes:
    if not raw.startswith(PNG_SIGNATURE):
        raise ValueError('Malformed PNG')
    result = bytearray(PNG_SIGNATURE)
    offset = 8
    found_end = False
    # Remove location-bearing metadata; keep compressed pixels/chunks unchanged.
    excluded = {b'eXIf', b'tEXt', b'zTXt', b'iTXt'}
    while offset + 12 <= len(raw):
        size = int.from_bytes(raw[offset:offset + 4], 'big')
        end = offset + 12 + size
        if end > len(raw) or size > 80_000_000:
            raise ValueError('Corrupt PNG chunk size')
        tag = raw[offset + 4:offset + 8]
        if zlib.crc32(raw[offset+4:end-4]) & 0xffffffff != int.from_bytes(raw[end-4:end], 'big'):
            raise ValueError('Corrupt PNG checksum')
        if tag not in excluded:
            result.extend(raw[offset:end])
        offset = end
        if tag == b'IEND':
            found_end = True
            break
    if not found_end or offset != len(raw):
        raise ValueError('Malformed PNG end')
    return bytes(result)


def webp_clean(raw: bytes) -> bytes:
    if len(raw) < 20 or raw[:4] != b'RIFF' or raw[8:12] != b'WEBP':
        raise ValueError('Malformed WebP')
    if int.from_bytes(raw[4:8], 'little') + 8 != len(raw):
        raise ValueError('WebP RIFF size mismatch')
    chunks = []
    offset = 12
    while offset + 8 <= len(raw):
        tag=raw[offset:offset+4]
        size=int.from_bytes(raw[offset+4:offset+8], 'little')
        end=offset+8+size+(size&1)
        if end > len(raw):
            raise ValueError('Invalid WebP chunk size')
        payload=bytearray(raw[offset+8:offset+8+size])
        if tag == b'VP8X' and len(payload) >= 10:
            payload[0] &= ~0x0c  # EXIF 0x08, XMP 0x04 in VP8X feature flags
        if tag not in (b'EXIF', b'XMP '):
            chunks.append(tag + struct.pack('<I',size) + payload + (b'\0' if size&1 else b''))
        offset=end
    if offset != len(raw) or not chunks:
        raise ValueError('Malformed WebP chunks')
    body=b'WEBP'+b''.join(chunks)
    return b'RIFF'+struct.pack('<I',len(body))+body


def clean_image(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    if raw.startswith(PNG_SIGNATURE):
        mime='image/png'
        cleaned=png_clean(raw)
    elif raw.startswith(b'\xff\xd8\xff'):
        mime='image/jpeg'
        cleaned=jpeg_clean(raw)
    elif raw.startswith(b'RIFF') and raw[8:12] == b'WEBP':
        mime='image/webp'
        cleaned=webp_clean(raw)
    else:
        raise ValueError('Expected a valid JPEG, PNG, or WebP file')
    # Optional Pillow: downscale only when present AND > 2000px long side.
    try:
        from PIL import Image, ImageOps
    except ImportError:
        if len(cleaned) > WARN_LIMIT:
            warnings.warn('Pillow unavailable: photo is over 4 MB. Install Pillow for downscaling.', stacklevel=2)
    else:
        with Image.open(io.BytesIO(cleaned)) as image:
            if max(image.size) > 2000:
                image = ImageOps.exif_transpose(image)
                image.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
                output = io.BytesIO()
                image.save(output, {'image/jpeg':'JPEG','image/png':'PNG','image/webp':'WEBP'}[mime],
                           quality=86 if mime != 'image/png' else None, optimize=True)
                cleaned = output.getvalue()
                # Ensure no metadata reintroduced by Pillow.
                cleaned = {'image/jpeg':jpeg_clean,'image/png':png_clean,'image/webp':webp_clean}[mime](cleaned)
    if len(cleaned) > RAW_LIMIT:
        raise ValueError(f'Image exceeds {RAW_LIMIT // 1_000_000} MB after metadata removal/downscaling; reduce it before embedding (16 MB HTML limit)')
    warnings.warn('Review faces, recognizable locations and private details before sharing this photo publicly.', stacklevel=2)
    return cleaned, mime
