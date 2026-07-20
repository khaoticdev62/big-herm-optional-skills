# Tilesets + Characters (F4jEt + sx665)

## Top-down tileset (F4jEt)
1. Block out base FLOOR tiles — start 16x16, bulk is 32x32 variants.
2. Add an "under" lip (~5px) fading to a darker shade (abyss feel).
3. 1px HIGHLIGHT rim on top edge so tiles "pop" and read as separate slabs.
4. Deco layer (grass, cracks, vines, glow particles) — kept SEPARATE so it overlays any base tile = instant variation.
5. Wall shadows: a 9x9 corner mask in a dark color at LOW opacity; plus inside-edge masks on corners. This is what makes walls read as walls.
6. De-repetition (the key to "not boring"):
   - copy + flip (H/V)
   - shift the tile a few px within its cell
   - slight hue/lightness nudge (Aseprite Ctrl+U) to make an "odd" tile
   - hand-add cracks/chips/gouges
7. Don't over-plan the tile list. Make bases -> add deco -> add walls/shadows -> stop when the area reads. Sellable packs grow via user feedback ("missing this connector").

## Small characters (sx665)
1. SILHOUETTE first. A strong, readable shape beats detail. Branch fast: big-head/small-body, small-head/big-legs, etc.
2. Add a SHADOW layer immediately (gives volume before any shading).
3. Keep iterating silhouettes; pick the "killer" one.
4. Shade (base/shadow/highlight) per general method.
5. FINAL details (wires, masks, cracks, damage) last — slowly manipulate.
6. SPLIT every animated part to its own layer: head, armor, robe, arms, prop (daggers/orbs). This is what makes rigging/animation feasible.
7. Client/feedback loop: 20 silhouettes -> pick 5-8 -> rough shade -> stakeholder picks -> final detail. Keep rejects; they become NPCs/merchants later.

## Layer discipline (both)
- Separate: line, base, shadow, highlight, deco, shadow-cast, per-limb.
- Export each animated part on its own layer/tag so the engine can transform it independently.

## Godot import notes
- Nearest filter (project + per-sprite).
- TileSet: bake a 1px autotile/peering buffer to avoid seams.
- Character: AnimatedSprite2D frames from `sheet.py`; pivot at feet.
- Keep deco tiles as overlay tiles, not baked into every base (variation for free).
