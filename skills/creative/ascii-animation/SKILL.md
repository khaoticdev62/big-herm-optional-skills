---
name: ascii-animation
description: "Professional ASCII animation engine in the Stone Story RPG (Gabriel / dino) tradition. Encodes the 10-step workflow (references -> concept -> primary keyframe -> size/composition -> plan -> keyframes -> in-betweens -> test -> polish -> engine delivery) plus a runnable engine: normalize frames to equal size, tween in-betweens between keyframes, compose multi-tempo layers (legs on one tempo, staff on another for fluidity), and render to terminal / self-contained HTML / GIF. Use for building, reviewing, or shipping hand-drawn ASCII animations."
platforms: [linux, macos, windows]
---

# ASCII Animation Engine (Stone Story method)

## When to use
- User wants to ANIMATE ASCII art: walk cycles, idle bob, attack, talk/speak loops, tilt, etc.
- User references the Stone Story animation tutorial, Auggie the skeleton NPC, Nagaraja, in-betweens, keyframes.
- User wants to render ASCII frames to terminal, HTML, or GIF for review or shipping.
- Companion to `ascii-lineart` (draw the art first, animate it here).

## The 10-step workflow (run this mentally / in plan mode)
1. **References** — gather existing art in the project + external refs (skeletons, walks).
2. **Concept** — sketch 3-5 variants; get feedback; pick the personality.
3. **Primary keyframe** — the single pose everything derives from. Draw it FIRST.
4. **Size & composition** — place next to the main character; match proportions; test scale.
5. **Plan** — list the animations (tilt-fwd, tilt-back, talk-fwd, talk-back, walk). Use short file names (for/back).
6. **Keyframes** — draw the extremes per animation; one animation at a time.
7. **In-betweens** — DON'T draw in order. Draw the midpoint first, then quarter points. Subdivide.
8. **Test** — render and watch. Loop the final frame for hold.
9. **Polish** — separate tempos per body part; add elasticity/bounce; arm arrives last.
10. **Engine delivery** — normalize (pad to equal height), import frames, assign speed, repeat final frame.

## Pro techniques encoded in the engine
- **Normalize**: all frames padded to the SAME height/width so they stack. Stone Story pads the TOP (anchor=top) so the baseline sits consistently. Width right-padded with spaces.
- **Tween (in-betweens)**: generates N intermediate frames between keyframes. Honest method: cells that are space on one end "fade in" on the later half; differing glyphs HOLD then SWITCH at the midpoint. Labeled `held-switch` so the artist knows to manually refine (the video's advice). For best results the artist overrides generated in-betweens by hand.
- **Multi-tempo layers**: the fluidity trick. Legs loop every 4 frames while the staff/arms run on a different tempo. Compose layers by overlay (upper layer non-space chars win; spaces let lower layer show through — this is the negative-space depth rule).
- **Render**: terminal (ANSI clear + delay), self-contained HTML (monospace <pre> + JS player, shareable), GIF (via Pillow if installed).

## Engine CLI (`scripts/ascii_anim.py`)
All commands accept a frames source: a `.txt` file with frames separated by a line `---`, OR a directory of `*.txt` frame files (sorted).

```bash
# Normalize (pad to equal size)
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" normalize \
  --frames frames.txt --out norm.txt --anchor top

# Tween in-betweens between keyframes (2+ keyframes, comma-separated)
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" tween \
  --keyframes kf_a.txt,kf_b.txt --between 3 --out tweened.txt

# Compose multi-tempo layers
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" compose \
  --layer body=norm.txt --layer arm=arm_loop.txt --arm-tempo 4 \
  --out composed.txt

# Render to terminal (live playback)
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" render \
  --frames norm.txt --mode terminal --fps 8

# Render to self-contained HTML (review / share)
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" render \
  --frames norm.txt --mode html --out anim.html

# Render to GIF (needs Pillow)
uv run --with pillow python "SKILL_DIR/scripts/ascii_anim.py" render \
  --frames norm.txt --mode gif --out anim.gif --fps 8
```

Flags:
- `--anchor top|bottom` (normalize): where to add padding rows.
- `--between N` (tween): in-betweens per segment.
- `--layer NAME=file` (compose): repeatable; NAME maps to optional `--NAME-tempo`.
- `--mode terminal|html|gif` (render).
- `--fps N` (render): frames per second.
- `--repeat-last N` (render/compose): hold final frame N times (the "loop the last frame" polish).

## Workflow with the engine
1. Draw keyframes as separate `.txt` files (use `ascii-lineart` rules).
2. `normalize` them so they're equal size and align.
3. `tween` to rough in the motion, then OPEN the output and hand-refine the in-betweens.
4. `compose` body + limb layers at independent tempos for fluidity.
5. `render --mode html` to review in a browser; `render --mode terminal` for the real medium; `render --mode gif` for a shareable clip.
6. Validate each frame with `ascii-lineart:validate_art.py` before shipping.

## Error handling
- Frames unequal size -> always `normalize` first (compose/render assume equal size; they'll warn).
- GIF fails (no Pillow) -> engine prints a clear install note; does NOT fake the file.
- Tween of mismatched-size keyframes -> normalize each keyframe first.
- Overlay looks like a blob -> apply negative-space depth (delete connector glyphs) per `ascii-lineart`.

## Verification
Render to HTML and watch loop; confirm: equal frame sizes, smooth-ish motion, independent limb tempo, final-frame hold. Only then call it production-ready.
