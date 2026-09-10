#!/usr/bin/env python3
"""
Build the narrow copies of each photo that phones actually need.

The pages ship one file per photo at full size, so a phone showing a picture in
a 129 px column still downloads the 1200 px original. This writes a 480 px and
an 800 px copy of each photo, in WebP and JPEG, next to the source; the pages
list them in `srcset` and the browser picks the smallest one that fits.

    python make-image-variants.py            # write anything missing or stale
    python make-image-variants.py --check     # exit 1 if anything is missing

Naming is `<stem>-<width>.<ext>`, e.g. images/gallery-1-480.webp. The original
stays untouched and stays in `srcset` as the largest candidate, so nothing
breaks if a variant is ever deleted.

Re-run after adding a photo. It skips work that is already up to date, and
never upscales: a width at or above the source's own width is skipped, which is
why small images like blog-one-health.jpg produce nothing.
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"

# Every photo a page requests, with the widths worth generating for it.
# 480 covers a phone at 2-3x; 800 covers the widest slot any of these fills on
# a desktop at 2x. The source file remains the largest candidate.
SOURCES = {
    # About — the photo carousel. Shown ~326 px on a phone, ~898 px on desktop.
    "gallery-1.jpg": (480, 800),
    "gallery-2.jpg": (480, 800),
    "gallery-3.jpg": (480, 800),
    "gallery-4.jpg": (480, 800),
    "gallery-5.jpg": (480, 800),
    "gallery-6.jpg": (480, 800),
    # About — the research figures, in a two-column grid. Shown ~129 px on a
    # phone, ~420 px on desktop, and currently have no WebP at all.
    "research-01-photo-1.jpg": (480, 800),
    "research-01-photo-3.jpg": (480, 800),
    "research-02-photo-1.jpg": (480, 800),
    "research-02-photo-2.jpg": (480, 800),
    # Resources — card photos.
    "aspire-1.jpg": (480, 800),
    "ffa-1.jpg": (480, 800),
    # Homepage — the portrait beside the hero.
    "sandra-and-teddy.jpg": (480, 800),
}

WEBP_QUALITY = 82
JPEG_QUALITY = 82


def variants_for(name, widths):
    """Yield (width, output_path, format) for the widths worth writing."""
    src = IMAGES / name
    if not src.exists():
        sys.exit(f"{name}: listed in SOURCES but not found in images/")
    with Image.open(src) as im:
        source_width = im.size[0]
    stem = src.stem
    for w in widths:
        if w >= source_width:
            continue  # never upscale
        yield w, IMAGES / f"{stem}-{w}.webp", "WEBP"
        yield w, IMAGES / f"{stem}-{w}.jpg", "JPEG"


def stale(src, out):
    return not out.exists() or out.stat().st_mtime < src.stat().st_mtime


def main():
    check = "--check" in sys.argv
    if not IMAGES.is_dir():
        sys.exit("images/ not found - run this from the repository root")

    written, missing, skipped = [], [], 0
    saved_before = saved_after = 0

    for name, widths in SOURCES.items():
        src = IMAGES / name
        for width, out, fmt in variants_for(name, widths):
            if not stale(src, out):
                skipped += 1
                continue
            if check:
                missing.append(out.name)
                continue
            with Image.open(src) as im:
                im = im.convert("RGB")
                ratio = width / im.size[0]
                size = (width, max(1, round(im.size[1] * ratio)))
                resized = im.resize(size, Image.LANCZOS)
                if fmt == "WEBP":
                    resized.save(out, "WEBP", quality=WEBP_QUALITY, method=6)
                else:
                    resized.save(out, "JPEG", quality=JPEG_QUALITY,
                                 optimize=True, progressive=True)
            written.append(out.name)
            saved_before += src.stat().st_size
            saved_after += out.stat().st_size

    if check:
        if missing:
            print("Missing or stale variants (run: python make-image-variants.py):")
            for m in missing:
                print("  " + m)
            return 1
        print(f"All {skipped} image variants are up to date.")
        return 0

    if written:
        print(f"Wrote {len(written)} variants ({skipped} already up to date):")
        for w in written:
            print("  " + w)
    else:
        print(f"All {skipped} image variants already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
