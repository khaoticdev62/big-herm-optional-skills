#!/usr/bin/env python3
"""audit.py - Game-ready audit of a pixel-art PNG.

Reports (real, measured):
  - dimensions + ODD width/height flag (jitter risk)
  - transparent buffer (min empty px border)
  - unique color count (palette size) with thresholds
  - aspect ratio
Exit 1 if blocking defects (odd dimension or zero buffer with content).
"""
import argparse
import sys
from collections import Counter

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)


def audit(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    # transparent buffer: min empty rows/cols from each edge
    top = left = right = bottom = 0
    for y in range(h):
        if all(px[x, y][3] == 0 for x in range(w)):
            top += 1
        else:
            break
    for y in range(h - 1, -1, -1):
        if all(px[x, y][3] == 0 for x in range(w)):
            bottom += 1
        else:
            break
    for x in range(w):
        if all(px[x, y][3] == 0 for y in range(h)):
            left += 1
        else:
            break
    for x in range(w - 1, -1, -1):
        if all(px[x, y][3] == 0 for y in range(h)):
            right += 1
        else:
            break
    buf = min(top, bottom, left, right)
    colors = Counter()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 0:
                colors[(r, g, b)] += 1
    ncolors = len(colors)
    odd = (w % 2 != 0) or (h % 2 != 0)
    return {
        "path": path, "w": w, "h": h, "odd": odd,
        "buffer": buf, "colors": ncolors,
        "aspect": round(w / h, 3) if h else 0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--tileset", action="store_true", help="use tileset thresholds")
    args = ap.parse_args()
    try:
        r = audit(args.path)
    except FileNotFoundError:
        print(f"[ERROR] not found: {args.path}", file=sys.stderr)
        sys.exit(2)

    print(f"== Pixel-Art Audit: {r['path']} ==")
    print(f"  size:     {r['w']} x {r['h']}  aspect {r['aspect']}")
    if r["odd"]:
        print("  [RED] ODD CANVAS (blocking): causes sub-pixel jitter when camera-snapped. Use even dims.")
    else:
        print("  [GREEN] even canvas")
    print(f"  buffer:   {r['buffer']}px empty border")
    if r["buffer"] == 0:
        print("  [RED] ZERO BUFFER (blocking): shaders/outlines clip. Leave >=1px (2px recommended).")
    elif r["buffer"] < 2:
        print("  [YELLOW] thin buffer: 2px recommended for shader/outline headroom.")
    else:
        print("  [GREEN] buffer OK for shaders")
    print(f"  palette:  {r['colors']} unique colors")
    limit = 64 if args.tileset else 32
    if r["colors"] > limit:
        print(f"  [YELLOW] palette > {limit}: likely >3 shades/material noise. Review.")
    else:
        print(f"  [GREEN] palette within {limit} limit")
    blocking = r["odd"] or r["buffer"] == 0
    print("  => BLOCKING DEFECTS" if blocking else "  => no blocking defects")
    sys.exit(1 if blocking else 0)


if __name__ == "__main__":
    main()
