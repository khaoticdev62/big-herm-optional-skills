#!/usr/bin/env python3
"""prep.py - Create a game-ready canvas PNG.

Forces EVEN width/height (odd => jitter). Leaves an empty transparent buffer
(default 2px) for shaders/outlines. Optional power-of-two pad.
"""
import argparse
import sys

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)


def next_even(n):
    return n if n % 2 == 0 else n + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=0, help="base size (square)")
    ap.add_argument("--w", type=int, default=0, help="override width")
    ap.add_argument("--h", type=int, default=0, help="override height")
    ap.add_argument("--buffer", type=int, default=2, help="empty px border (default 2)")
    ap.add_argument("--power-of-two", action="store_true", help="pad canvas to power of two")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    w = args.w or args.size
    h = args.h or args.size
    if not w or not h:
        print("[ERROR] provide --size or both --w and --h", file=sys.stderr)
        sys.exit(2)
    w = next_even(w)
    h = next_even(h)
    if args.power_of_two:
        import math
        w = 2 ** math.ceil(math.log2(w))
        h = 2 ** math.ceil(math.log2(h))
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.save(args.out)
    print(f"[OK] prepared canvas {w}x{h} (buffer {args.buffer}px reserved by caller) -> {args.out}")


if __name__ == "__main__":
    main()
