#!/usr/bin/env python3
"""sheet.py - Pack frame PNGs into a horizontal sprite sheet (Aseprite one-line export).

Frames are sorted by filename. Forces even canvas per frame; warns if sheet
width exceeds --max-width (default 2048) so engines don't auto-compress.
"""
import argparse
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames_dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-width", type=int, default=2048)
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.frames_dir, "*.png")))
    if not files:
        print(f"[ERROR] no PNG frames in {args.frames_dir}", file=sys.stderr)
        sys.exit(2)
    imgs = [Image.open(f).convert("RGBA") for f in files]
    h = max(i.height for i in imgs)
    if h % 2:
        h += 1
    total_w = sum(i.width for i in imgs)
    if total_w > args.max_width:
        print(f"[YELLOW] sheet width {total_w} > {args.max_width}; split or risk engine compression.")
    sheet = Image.new("RGBA", (total_w, h), (0, 0, 0, 0))
    x = 0
    for i in imgs:
        sheet.paste(i, (x, 0))
        x += i.width
    sheet.save(args.out)
    print(f"[OK] sheet {total_w}x{h} from {len(imgs)} frames -> {args.out}")


if __name__ == "__main__":
    main()
