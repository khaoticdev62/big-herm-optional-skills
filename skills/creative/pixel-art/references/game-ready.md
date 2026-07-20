# Game-Ready Export (p0UZ — Insignia dev)

## Atlas vs per-file
- A single giant "master atlas" of objects is convenient to DRAW in (keeps style consistent, Animal Well did this) but PAINFUL to maintain: resizing one object breaks slice indexes; space-conservative mindset hurts.
- For game OBJECTS: export per-file (or per-tag sheet). Modern engines atlas+compress for you; your economizing costs time, not bytes.
- TILESETS are the exception: keep all tiles in ONE file (the tileset editor loads it as one texture; needs internal consistency). Give tiles a 1px extra border buffer to kill transparent seams when the camera scrolls (Unity AND Godot both exhibit this float-inaccuracy seam).

## Empty space is free — leave it
- Pixels are cheap, especially transparent ones. Don't squeeze the canvas tight around a sprite.
- Leave >=1px (2px recommended) EMPTY border beyond the art. Shaders (outlines, pushes, VFX) sample the canvas; a tight canvas clips the effect or bleeds a neighbor in an atlas.
- p0UZ: his game has ~20-30k hand-drawn sprites at ~45MB of assets. Not the bottleneck.

## EVEN canvas only (critical)
- Odd width/height -> the sprite's center is on a half-pixel -> when the camera snaps to pixels, the asset STRADDLES pixels and JITTERS every half-pixel of movement.
- Fix: always export even dimensions (16x16, 32x32, 64x64). If you need a center pixel (e.g. a UI arrow), accept asymmetry or pad to even; do NOT ship odd.
- This is the #1 cause of "why does my pixel art vibrate when moving."

## Pivot points
- Pivot = where the world places the asset on its canvas rectangle.
- Grounded characters: pivot at FEET (between the feet). World position = where they stand.
- Flying/centered: chest or center-of-mass.
- Flipping/rotation pivots around this point. A wrong pivot makes a character SHIFT when it should turn in place.
- In Aseprite: set pivot on selection; in engine (Godot Sprite2D / Unity slicer): assign pivot explicitly (bottom-center is the Aseprite-importer default — good for grid chars).

## Animation speed (FPS)
- Aseprite default 100ms/frame. p0UZ prefers ~80ms ("on twos" = 12fps, the classic film/TV standard).
- NPCs walking at 6fps is fine. Players don't notice 6 vs 8 vs 10.
- Fast VFX: up to 20fps.
- Guideline: is it easy to produce, scalable, and looks good? That beats historical "purity."

## Even vs odd pixel practical test
- 16x16 diamond: snaps clean to grid, moves with terrain.
- 15x15 diamond: center off-grid, jitters against terrain. Never ship.
