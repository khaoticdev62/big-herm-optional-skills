#!/usr/bin/env python3
"""dither.py - Generate a Bayer 4x4 ordered-dither threshold map PNG.

The classic 2-color checker reference used for hand dithering (DKmrB) or as a
mask. White = full threshold, black = zero. Use as a stamp or overlay guide.
"""
import argparse
import sys

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)

BAYER4 = [
    [0, 8, 2, 10],
    [12, 4, 14, 6],
    [3, 11, 1, 9],
    [15, 7, 13, 5],
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=int, default=1, help="pixel size per cell")
    args = ap.parse_args()
    s = args.scale
    img = Image.new("L", (4 * s, 4 * s), 0)
    px = img.load()
    for y in range(4):
        for x in range(4):
            v = int(255 * BAYER4[y][x] / 16)
            for dy in range(s):
                for dx in range(s):
                    px[x * s + dx, y * s + dy] = v
    img.save(args.out)
    print(f"[OK] Bayer 4x4 dither map ({4*s}x{4*s}) -> {args.out}")


if __name__ == "__main__":
    main()
