---
name: pixel-art
description: "Professional pixel-art studio synthesized from five pro tutorials (general method, toolchain, top-down tilesets, small-character design, game-ready export) plus Godot 4.5 / BLACKTOP AMERICA targeting. Combines the artistic rules AND a runnable Pillow toolkit: audit a sprite/tileset for game-ready defects (odd canvas, empty buffer, palette size, outline contrast), prep a canvas (even size, power-of-two-safe, empty buffer for shaders), generate de-repetition variations (flip/hue/shift), build atlas/sprite sheets from tags, generate a Bayer dither map, and produce a verifiable sample sprite. Use for creating, critiquing, auditing, or shipping pixel-art assets."
platforms: [linux, macos, windows]
---

# Pixel-Art Studio (Professional Method)

## When to use
- User wants to DRAW, critique, audit, or ship pixel art (sprites, tilesets, characters).
- User references any of: palette-first workflow, Aseprite/LibreSprite/Piskel, top-down tilesets, small-character silhouettes, game-ready export (atlas, pivot, FPS, jitter).
- User is producing assets for Godot 4.5 / Steam Deck / BLACKTOP AMERICA.
- User wants automated checks before an asset enters the engine.

## The five sources, condensed
1. **General method (DKmrB):** palette-first (don't hand-mix early); flow = outline -> base fill -> shade (base/shadow/highlight = 3 shades per material). Toggle pixel-perfect to kill "doubles". Smooth curves by counting + symmetric segment lengths. Shade with ANALOGOUS colors (base red -> highlight orange -> shadow purple), judged from a fixed light source. Avoid "pillow shading" (wrapping shadow on the outline). Use dithering for texture/3rd-color illusion. Recolor outlines (darker version of the object, or bright accent like Omori's purple) to guide the eye — outlines are a focus tool, not always black. Tip: zoom out constantly; max 3 shades/material; use references; boldness > realism.
2. **Toolchain (GameFromScratch):** Aseprite ($20, build-free alt = LibreSprite) is the indie standard; free intro = Piskel (browser); Krita/PixiEditor also viable. Escalation path MakeCode Arcade -> Python/GDScript. Audio: LMMS (retro chips) / Reaper (DAW). For BLACKTOP we target Aseprite-style PNG export + Godot import.
3. **Top-down tilesets (F4jEt):** block out 16px base tiles + 32px variants; add a 1px highlight rim + 5px "under" lip fading to abyss; separate deco layer; wall shadows = 9x9 corner mask at low opacity; de-repetition via flip/hue-shift/shift-copy + hand cracks. Don't over-plan tile lists — make, then add.
4. **Small characters (sx665):** silhouette-first (strong readable shape), add a shadow layer immediately, branch ideas fast (big-head/small-body etc.), then shade, then final details. Split every animated part (head/arm/robe/daggers) onto its OWN layer for rigging. Client loop: 20 silhouettes -> pick 5-8 -> rough shade -> client picks -> final detail.
5. **Game-ready export (p0UZ):** per-file sprites beat giant master atlases (atlas = bleed/resize pain; tiles excepted). LEAVE EMPTY SPACE around sprites (pixels are cheap; shaders need a 1px+ buffer to draw outlines). EVEN canvas size only (odd height = sub-pixel jitter when camera-snapped). Pivot = where the world places the asset (feet for grounded chars, chest for flying). FPS: 6-12 for NPCs is fine; 80ms/frame ("on twos") is the sweet spot; 20 for fast VFX. Palettes need not be minimal — file size is not the bottleneck.

## Godot 4.5 / BLACKTOP AMERICA notes
- Import discipline: `Project Settings > Rendering > Textures > Default Texture Filter = Nearest`. This is non-negotiable for crisp pixel art (matches the Route 17 "no blur/jitter" rule in project memory).
- CanvasItemTexture / Sprite2D: set texture filter to Nearest per-sprite too if project default is missed.
- Camera: snap to pixel grid (use a 2D snap or a `camera.position` rounded to integer pixels) to avoid the odd-canvas jitter p0UZ warns about.
- AnimatedSprite2D / AnimationPlayer: drive frames at the FPS above; keep pivot at feet for grounded NPCs.
- TileMaps: use a TileSet with a 1px autotile/peering buffer to kill the transparent-seam p0UZ documents in Unity (same bug exists in Godot scrolling).

## Runnable toolkit (scripts/)
All commands use `uv run --with pillow python "SKILL_DIR/scripts/<cmd>.py"`. Every command prints evidence and writes a real file; nothing is faked.

- `audit.py` — inspect a PNG sprite/tileset; report: dimensions (flag ODD width/height), transparency buffer (px of empty border), palette size (# unique colors, warn >32 for a sprite, >64 for a tileset), nearest-filter guess, aspect. Exit 1 if blocking defects.
- `prep.py` — create a prepared canvas PNG: forces EVEN width/height (rounds up), leaves an `--buffer N` px empty border (default 2), optional `--power-of-two` pad. Output is a transparent PNG ready to draw/import.
- `variations.py` — from a tile PNG, emit N de-repetition variants: horizontal/vertical flip + slight hue/lightness shift (control-U style). Writes a sheet + individual files. This operationalizes F4jEt's "copy/flip/hue" trick.
- `sheet.py` — pack a folder of frame PNGs into a horizontal sprite sheet (Aseprite "one line" export). Used for AnimatedSprite2D. Honors even canvas + buffer.
- `dither.py` — generate a Bayer 4x4 ordered-dither threshold map PNG (the classic 2-color checker). Use as a reference/stamp for dithering by hand or as a mask.
- `sample_gen.py` — generate a verifiable sample sprite (a shaded 16x16 cube with base/shadow/highlight + 2px buffer + even canvas) so the skill is testable without external art.

## Commands (copy/paste)
```bash
SK="C:/Users/thecr/AppData/Local/hermes/profiles/big-herm/skills/pixel-art"
# Audit an asset
uv run --with pillow python "$SK/scripts/audit.py" my_sprite.png
# Prep a clean canvas (even, 2px buffer)
uv run --with pillow python "$SK/scripts/prep.py" --size 32 --buffer 2 --out canvas.png
# De-repetition variations
uv run --with pillow python "$SK/scripts/variations.py" tile.png --count 6 --out variants.png
# Build a sprite sheet from a frames folder
uv run --with pillow python "$SK/scripts/sheet.py" frames_dir --out hero_sheet.png
# Dither reference map
uv run --with pillow python "$SK/scripts/dither.py" --out bayer.png
# Generate a verifiable sample
uv run --with pillow python "$SK/scripts/sample_gen.py" --out sample.png
```

## Workflow (artist + automation)
1. `prep.py` a canvas (even, buffered) OR `audit.py` an existing file and fix blockers first.
2. Draw outline -> base -> shade (3 shades/material) per general method.
3. Split animated parts to layers (sx665) before export.
4. `variations.py` for tilesets; `sheet.py` for character frames.
5. `audit.py` again before import; confirm zero blocking defects.
6. Import to Godot with Nearest filter + foot pivot + pixel-snap camera.

## Error handling
- Odd canvas -> `prep.py` or resize to even; engine import will otherwise jitter.
- No buffer -> `prep.py --buffer 2`; shaders will clip outlines without it.
- Huge palette -> reduce to <=3 shades/material; audit flags it.
- Sheet too wide (>2048) -> split into rows; warn in `sheet.py`.

## Verification
The skill ships `sample_gen.py`; run it and `audit.py` on the result to prove the pipeline produces a game-ready asset. Always audit real assets before declaring production-ready.
