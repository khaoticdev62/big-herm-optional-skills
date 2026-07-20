---
name: ascii-lineart
description: "Professional ASCII line-art studio in the Stone Story RPG (Gabriel / dino) tradition: curated symbol palette, monospace discipline, anti-aliasing via negative space, depth via negative space, material 'language' recipes, and a validator that enforces the pro rules (monospace grid, no off-grid alphanumerics, immersion-safe). Use for creating, critiquing, or teaching hand-drawn ASCII art in a 1:2 or square glyph field."
platforms: [linux, macos, windows]
---

# ASCII Line-Art Studio (Stone Story method)

## When to use
- User wants to DRAW, design, or critique ASCII art by hand (not auto-converted photos).
- User asks about ASCII/ANSI line-art style, symbol choices, material consistency, anti-aliasing, depth.
- User references Stone Story RPG, Gabriel (dino), the Nagaraja animation, or "ASCII art tutorial".
- User wants to verify a piece follows pro rules before shipping it into a game/terminal panel.

This is the PART 1 knowledge base + a validator. For animation (keyframes, in-betweens, multi-tempo layers), use the companion skill `ascii-animation`.

## Core philosophy (learn these before drawing)
1. **It's a subset language, not the whole ASCII table.** Pro line-art uses ~25 glyphs, not 95.
2. **Monospace is law.** Every glyph occupies one cell. Art that relies on proportional fonts is not ASCII art — it's text art.
3. **Glyph ratio matters.** 1:2 (tall) is old-school ASCII; square is modern roguelikes (Cogmind, Dwarf Fortress). In a 1:2 cell you have ~2x X-resolution of Y, but ~4-5x internal Y-resolution of X — this is what makes ASCII anti-aliasing unique.
4. **Anti-aliasing = negative space.** Insert empty cells / low-altitude glyphs (`. ' , ¡`) to soften near-vertical lines instead of jagged full glyphs.
5. **Depth = broken overlaps.** When two shapes overlap, delete the connecting glyph or use an accent (`´`) so the brain reads two separate objects with a shadow.
6. **Establish a "language of the art."** Pick one symbol-combination recipe per material (metal, rock, web, water) and reuse it everywhere. Consistency = the viewer learns your vocabulary.
7. **Alphanumerics break immersion.** Letters/numbers activate the language center of the brain and shatter the static look. Avoid sprinkling them. (Use only where you WANT the eye drawn — e.g., a character's eye — and call it a deliberate choice.)

## The pro line-art alphabet (reference/alphabet.md)
Load `skill_view(name='ascii-lineart', file_path='references/alphabet.md')` for the full glyph table with roles, altitude, and material pairing. Quick set:
- Diagonals: `/ \ |`
- Low-altitude softeners: `. , ' ´`  (anti-aliasing + accents)
- Extended (fit-the-style, pragmatic): `¯` overscore, `´` acute, `¡` inverted bang, `·` middle dot
- Lines/curves: `_ - :` (underscore=bulge line, hyphen=straight thin, colon=mid point)
- Useful alphanumerics (sparingly): `o v V t l 7` (7 = sitting/scratching legs, u = shovel, c = curl, x = fence/grate)
- Box drawing: `│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼` (DOS heritage; great for UI frames)

## The overscore trick (critical)
`¯` (overscore) draws in the cell BELOW the line, freeing the cell ABOVE for background to show through. When a sprite sits on top of art drawn with `_`, the underscore creates a black box obscuring the background; the overscore avoids that. Same visual line, different stacking behavior.

## Workflow for a new piece
1. Pick glyph ratio (1:2 for retro, square for modern roguelike).
2. Choose monospace font (Courier / custom). Confirm it has your extended glyphs.
3. Sketch silhouette with diagonals + box drawing.
4. Apply material recipes from the language you've established.
5. Anti-alias near-vertical/high-angle lines with negative space.
6. Break overlaps for depth.
7. Run the validator (`scripts/validate_art.py`) on the final text.
8. Fix violations, re-validate.

## Validator (enforce pro rules)
`scripts/validate_art.py` checks a text file and reports:
- **monospace_grid**: all rows equal width after strip (catches accidental drift).
- **off_grid_alphanumerics**: flags letters/digits NOT in the allowed sparse set (`o v V t l 7 u c x`), labeling them immersion risks.
- **stray_control**: tabs / non-breaking spaces that break the grid.
- **empty_rows**: suggests trimming.
Returns JSON + a human summary; exit code 1 if blocking issues found.

```bash
uv run --with pyyaml python "SKILL_DIR/scripts/validate_art.py" art.txt
uv run --with pyyaml python "SKILL_DIR/scripts/validate_art.py" art.txt --json
```

## Error handling
- If art looks "jagged": add `.`/`'`/`´` between near-vertical glyphs (anti-alias), don't thicken.
- If two shapes read as one blob: delete the connector glyph or swap to `´` (depth).
- If a sprite's underscore creates a black box over background: switch to `¯`.
- If validator flags alphanumerics: either remove them or consciously keep + note "deliberate focal point."

## Verification
After drawing, always run the validator and confirm zero blocking issues before calling the art production-ready.
