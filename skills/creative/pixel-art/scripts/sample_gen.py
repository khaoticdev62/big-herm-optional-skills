#!/usr/bin/env python3
"""sample_gen.py - Generate a verifiable sample sprite.

A 16x16 shaded cube on a 20x20 (even) canvas with 2px empty buffer, using a
3-shade ramp (base/shadow/highlight) + analogous-style outline. Lets the skill
prove its pipeline end-to-end without external art.
"""
import argparse
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=16)
    ap.add_argument("--buffer", type=int, default=2)
    args = ap.parse_args()

    s = args.size
    buf = args.buffer
    canvas = s + buf * 2
    if canvas % 2:
        canvas += 1
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    base = (90, 170, 80, 255)
    shadow = (40, 90, 120, 255)
    highlight = (220, 220, 120, 255)
    outline = (30, 70, 40, 255)
    x0, y0 = buf, buf
    x1, y1 = buf + s, buf + s
    d.rectangle([x0, y0, x1 - 1, y0 + 3], fill=highlight)
    d.rectangle([x0, y0 + 4, x1 - 1, y1 - 1], fill=base)
    d.rectangle([x0, y1 - 4, x1 - 1, y1 - 1], fill=shadow)
    d.rectangle([x1 - 3, y0, x1 - 1, y1 - 1], fill=shadow)
    d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=outline, width=1)
    img.save(args.out)
    print(f"[OK] sample sprite {canvas}x{canvas} (buffer {buf}) -> {args.out}")


if __name__ == "__main__":
    main()
