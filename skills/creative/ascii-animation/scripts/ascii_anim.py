#!/usr/bin/env python3
"""ascii_anim.py - Stone Story method ASCII animation engine.

Commands:
  normalize  pad frames to equal size (anchor top/bottom)
  tween      generate honest in-betweens between two keyframe files
  compose    overlay multi-tempo layers (body + limbs at independent tempos)
  render     play to terminal / export self-contained HTML / export GIF

Frames are lists of equal-width rows. A source is either:
  - a .txt file with frames separated by a line "---"
  - a directory of sorted *.txt frame files
"""
import argparse
import glob
import os
import sys
import time


def load_frames(path):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.txt")))
        frames = []
        for f in files:
            with open(f, encoding="utf-8") as fh:
                frames.append(fh.read().split("\n"))
        return frames
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if "---" in text:
        return [blk.split("\n") for blk in text.split("---")]
    return [text.split("\n")]


def save_frames(frames, out):
    with open(out, "w", encoding="utf-8") as fh:
        for i, fr in enumerate(frames):
            if i:
                fh.write("---\n")
            fh.write("\n".join(fr))
            fh.write("\n")


def dims(frames):
    h = max(len(f) for f in frames)
    w = max((max((len(r) for r in f), default=0) for f in frames), default=0)
    return h, w


def normalize(frames, anchor="top"):
    h, w = dims(frames)
    out = []
    for f in frames:
        rows = list(f)
        rows = [r.ljust(w) for r in rows]
        pad = h - len(rows)
        if anchor == "top":
            rows = rows + [" " * w] * pad
        else:
            rows = [" " * w] * pad + rows
        out.append(rows)
    return out


def tween_pair(a, b, between):
    """Honest in-between: space fades in/out across the midpoint; differing
    glyphs hold then switch. Artist should hand-refine the output."""
    h = max(len(a), len(b))
    w = max((max((len(r) for r in a), default=0)),
            (max((len(r) for r in b), default=0)))
    a = [r.ljust(w) for r in a] + [" " * w] * (h - len(a))
    b = [r.ljust(w) for r in b] + [" " * w] * (h - len(b))
    out = []
    for step in range(1, between + 1):
        t = step / (between + 1)
        rows = []
        for r in range(h):
            line = []
            for c in range(w):
                ca, cb = a[r][c], b[r][c]
                if ca == cb:
                    line.append(ca)
                elif ca == " " and cb != " ":
                    line.append(cb if t > 0.5 else " ")
                elif cb == " " and ca != " ":
                    line.append(ca if t <= 0.5 else " ")
                else:
                    line.append(ca if t <= 0.5 else cb)
            rows.append("".join(line))
        out.append(rows)
    return out


def compose(layers, tempos, repeat_last=0):
    """Overlay layers. Each layer is a loop of frames; tempo holds each frame
    N times (so a 4-frame arm at tempo 1 vs 1-frame body => arm moves 4x)."""
    expanded = []
    names = []
    for (fr), tempo in zip(layers, tempos):
        fr = normalize(fr)
        ex = [f for f in fr for _ in range(max(1, tempo))]
        expanded.append(ex)
        names.append(fr)
    total = max(len(e) for e in expanded)
    h, w = dims(expanded)
    out = []
    for n in range(total):
        base = [" " * w for _ in range(h)]
        for e in expanded:
            layer = e[n % len(e)]
            for r in range(min(h, len(layer))):
                row = list(base[r])
                for c in range(min(w, len(layer[r]))):
                    ch = layer[r][c]
                    if ch != " ":
                        row[c] = ch
                base[r] = "".join(row)
        out.append(base)
    if repeat_last:
        out = out + [out[-1]] * repeat_last
    return out


def render_terminal(frames, fps):
    interval = 1.0 / max(1, fps)
    try:
        while True:
            for f in frames:
                sys.stdout.write("\033[2J\033[H")
                sys.stdout.write("\n".join(f) + "\n")
                sys.stdout.flush()
                time.sleep(interval)
    except KeyboardInterrupt:
        sys.stdout.write("\n[stopped]\n")


def render_html(frames, out, fps, repeat_last=0):
    if repeat_last:
        frames = frames + [frames[-1]] * repeat_last
    parts = []
    for f in frames:
        cells = ",".join('"' + r.replace("\\", "\\\\").replace('"', '\\"') + '"' for r in f)
        parts.append("[" + cells + "]")
    data = ",\n".join(parts)
    interval = int(1000.0 / max(1, fps))
    html = (
        "<!doctype html><html><head><meta charset=\"utf-8\">\n"
        "<title>ASCII Animation</title>\n"
        "<style>body{background:#0b0b0b;color:#9f9;margin:0;display:flex;justify-content:center}\n"
        "pre{font-family:'Courier New',monospace;font-size:18px;line-height:1.05;white-space:pre;"
        "letter-spacing:1px;background:#0b0b0b;padding:24px;border:1px solid #1f3f1f;"
        "border-radius:8px;margin-top:24px}</style></head><body><pre id=\"s\"></pre>\n"
        "<script>\nvar frames=[" + data + "];\n"
        "var i=0;\n"
        "function loop(){var f=frames[i%frames.length];"
        "document.getElementById('s').textContent=f.join('\\n');i++;"
        "setTimeout(loop," + str(interval) + ");}\nloop();\n</script></body></html>"
    )
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("[OK] HTML written: " + out + "  (" + str(len(frames)) +
          " frames, " + str(fps) + " fps)")


def render_gif(frames, out, fps, repeat_last=0):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[ERROR] Pillow not installed. Run: uv pip install --system pillow",
              file=sys.stderr)
        sys.exit(3)
    if repeat_last:
        frames = frames + [frames[-1]] * repeat_last
    font_path = None
    for p in [
        "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/Library/Fonts/Menlo.ttc",
    ]:
        if os.path.exists(p):
            font_path = p
            break
    if font_path:
        font = ImageFont.truetype(font_path, 20)
    else:
        font = ImageFont.load_default()
    sample = max((max(f, key=len) for f in frames), key=len)
    bbox = font.getbbox("M" * len(sample))
    cw = (bbox[2] - bbox[0]) or 12
    ascent, descent = font.getmetrics()
    ch = (ascent + descent) or 20
    W = cw * len(sample) + 20
    H = ch * max(len(f) for f in frames) + 20
    imgs = []
    for f in frames:
        img = Image.new("RGB", (W, H), (11, 11, 11))
        d = ImageDraw.Draw(img)
        for r, line in enumerate(f):
            d.text((10, 10 + r * ch), line, fill=(150, 255, 150), font=font)
        imgs.append(img)
    dur = int(1000.0 / max(1, fps))
    imgs[0].save(out, save_all=True, append_images=imgs[1:],
                 duration=dur, loop=0, optimize=False)
    print("[OK] GIF written: " + out + "  (" + str(len(frames)) +
          " frames, " + str(fps) + " fps)")


def main():
    ap = argparse.ArgumentParser(description="Stone Story ASCII animation engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("normalize")
    p.add_argument("--frames", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--anchor", default="top", choices=["top", "bottom"])

    p = sub.add_parser("tween")
    p.add_argument("--keyframes", required=True, help="a.txt,b.txt")
    p.add_argument("--between", type=int, default=3)
    p.add_argument("--out", required=True)

    p = sub.add_parser("compose")
    p.add_argument("--layer", action="append", required=True, help="NAME=file")
    p.add_argument("--tempo", action="append", default=[], help="NAME=N (hold frames)")
    p.add_argument("--repeat-last", type=int, default=0)
    p.add_argument("--out", required=True)

    p = sub.add_parser("render")
    p.add_argument("--frames", required=True)
    p.add_argument("--mode", required=True, choices=["terminal", "html", "gif"])
    p.add_argument("--out", default="anim.html")
    p.add_argument("--fps", type=int, default=8)
    p.add_argument("--repeat-last", type=int, default=0)

    args = ap.parse_args()

    if args.cmd == "normalize":
        frames = normalize(load_frames(args.frames), args.anchor)
        save_frames(frames, args.out)
        print("[OK] normalized " + str(len(frames)) + " frames -> " + args.out)
    elif args.cmd == "tween":
        kf = args.keyframes.split(",")
        if len(kf) != 2:
            print("[ERROR] tween needs exactly two keyframes (a,b)", file=sys.stderr)
            sys.exit(2)
        a = normalize(load_frames(kf[0]))
        b = normalize(load_frames(kf[1]))
        mids = tween_pair(a[0], b[0], args.between)
        out = a + mids + b
        save_frames(out, args.out)
        print("[OK] tweened: " + str(len(a)) + "->" + str(len(out)) +
              "<-" + str(len(b)) + " frames -> " + args.out)
        print("     NOTE: hand-refine the generated in-betweens.")
    elif args.cmd == "compose":
        layers = []
        names = []
        for kv in args.layer:
            name, path = kv.split("=", 1)
            layers.append(load_frames(path))
            names.append(name)
        tempo_map = {}
        for kv in args.tempo:
            n, v = kv.split("=", 1)
            tempo_map[n] = int(v)
        tempos = [tempo_map.get(n, 1) for n in names]
        out = compose(layers, tempos, args.repeat_last)
        save_frames(out, args.out)
        print("[OK] composed " + str(len(out)) + " frames from " +
              str(len(layers)) + " layers -> " + args.out)
    elif args.cmd == "render":
        frames = normalize(load_frames(args.frames))
        if args.mode == "terminal":
            render_terminal(frames, args.fps)
        elif args.mode == "html":
            render_html(frames, args.out, args.fps, args.repeat_last)
        else:
            render_gif(frames, args.out, args.fps, args.repeat_last)


if __name__ == "__main__":
    main()
