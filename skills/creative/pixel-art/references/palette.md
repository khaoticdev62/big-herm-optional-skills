# Palette-First Workflow (DKmrB + p0UZ)

## Don't hand-mix early
- Use a pre-made pixel-art palette (lowspec.app is the go-to; sort by color count).
- Rule of thumb: pick a palette with AT LEAST 3 shades per hue you'll need.
- In Aseprite: `Windows > Palette > Import` then `Save as Default`.
- "You don't have to learn color theory to start" — automate the palette, focus on drawing.

## 3 shades per material
- base / shadow / highlight. That's the default shading kit.
- Level up: shade with ANALOGOUS colors (neighbors on the wheel):
  - red base -> orange highlight -> purple shadow
  - green base -> yellow highlight -> blue shadow
- This reads more vivid than light/dark of the same hue.

## Reference palettes (start here)
- LowSpec: https://lospec.com/palette-list (filter "pixel art", by color count)
- Endesga / DawnBringer 32 / Sweetie 16 are community favorites for games.
- For BLACKTOP AMERICA: choose a palette with road/desert + night + UI contrast built in.

## Palette discipline (p0UZ)
- You do NOT need a minimal palette for file-size reasons. File compression is not the bottleneck.
- But DO keep <=3 shades per material for readability (too many = noise).
- Audit will flag sprite palettes >32 and tileset palettes >64 as review items.

## Anti-patterns
- Pillow shading: wrapping shadow around the outline with no light source. Looks like a inflated pillow. Fix: pick ONE light direction, keep it consistent across all sprites.
- Per-material >3 shades "just because": noisy, hard to read at game scale.
