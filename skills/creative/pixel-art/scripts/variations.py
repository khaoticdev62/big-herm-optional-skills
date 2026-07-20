#!/usr/bin/env python3
"""variations.py - De-repetition tile variations (F4jEt copy/flip/hue trick).

From one tile PNG, emit N variants: horizontal/vertical flips + slight
hue/lightness nudge (Aseprite Ctrl+U style). Writes a contact sheet PNG
plus individual variant PNGs in <out>_vars/.
"""
import argparse
import os
import sys

try:
    from PIL import Image, ImageEnhance
except ImportError:
    print("[ERROR] Pillow missing: uv pip install --system pillow", file=sys.stderr)
    sys.exit(3)


def enhance(img, hue_deg, light):
    # Pillow has no direct hue rotate; approximate with channel shift (cheap hue nudge).
    if hue_deg:
        r, g, b, a = img.split()
        if hue_deg % 360 < 120:
            img2 = Image.merge("RGBA", (g, b, r, a))
        elif hue_deg % 360 < 240:
            img2 = Image.merge("RGBA", (b, r, g, a))
        else:
            img2 = Image.merge("RGBA", (r, b, g, a))
    else:
        img2 = img
    if light != 1.0:
        img2 = ImageEnhance.Brightness(img2).enhance(light)
    return img2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--count", type=int, default=6)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    base = Image.open(args.src).convert("RGBA")
    w, h = base.size
    variants = [base]
    flips = [("h", base.transpose(Image.FLIP_LEFT_RIGHT)),
             ("v", base.transpose(Image.FLIP_TOP_BOTTOM)),
             ("hv", base.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM))]
    for suf, f in flips:
        variants.append(f)
    nudges = [(15, 1.05), (-15, 0.95), (30, 1.0), (0, 1.1)]
    for deg, light in nudges:
        variants.append(enhance(base, deg, light))
    variants = variants[:max(1, args.count)]

    import math
    cols = math.ceil(math.sqrt(len(variants)))
    rows = math.ceil(len(variants) / cols)
    sheet = Image.new("RGBA", (w * cols, h * rows), (0, 0, 0, 0))
    for i, v in enumerate(variants):
        r, c = divmod(i, cols)
        sheet.paste(v, (c * w, r * h))
    out_dir = os.path.splitext(args.out)[0] + "_vars"
    os.makedirs(out_dir, exist_ok=True)
    for i, v in enumerate(variants):
        v.save(os.path.join(out_dir, f"var_{i:02d}.png"))
    sheet.save(args.out)
    print(f"[OK] wrote {len(variants)} variants -> {args.out} (+ {out_dir}/)")


if __name__ == "__main__":
    main()
