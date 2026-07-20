# The Pro Line-Art Alphabet (Stone Story method)

Each glyph has a ROLE. Pro art is the disciplined recombination of these, not the full ASCII table.

## Diagonals & structure
| Glyph | Altitude / role | Notes |
|-------|-----------------|-------|
| `/` | 45° forward diagonal | rocky vs web depending on neighbor |
| `\` | 45° back diagonal | pair with `/` for curves |
| `|` | vertical | high-angle lines are limited (see X/Y note) |
| `_` | low line w/ bulge | old-school thin line; creates black box if sprite sits above |
| `-` | straight thin line | cleaner than `_` for some materials |
| `:` | mid-altitude point | two dots = a point/hinge |
| `.` | lowest altitude | anti-alias softener |
| `,` | low + tail | anti-alias / small curve |
| `'` | high accent | pairs with `´` for very slight inclination |
| `´` | acute accent | anti-alias + depth connector (upper-right) |
| `¯` | overscore | draws BELOW line, frees cell above for background |
| `¡` | inverted bang | anti-aliasing / exclamation of form |
| `·` | middle dot | fills mid-cell points cleanly |

## Box drawing (DOS heritage — UI frames, buildings)
`│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼`
Use for HUD borders, doors, architecture. Crisp stacking.

## Sparse alphanumerics (use sparingly, deliberate)
| Glyph | Role |
|-------|------|
| `o` | head / hole / dot |
| `v V` | downward point / chin / open mouth |
| `t` | cross / stand |
| `l` | edge / wall |
| `7` | sitting/scratching leg (very useful) |
| `u` | shovel / cup (use rarely) |
| `c` | curl / open hand (edge-case) |
| `x` | fence / grate / pattern |

ALL OTHER letters/digits are IMMERSION RISKS — they pull the viewer's eye and shatter the static look. Flag them in review.

## Material "language" recipes (establish once, reuse)
- **Metal** (key, fence): thin `_`/`-` + `:` accents, high contrast, no soft fill.
- **Rock/mountain**: `\` `/` with `_ . -` bulges; chunky, irregular.
- **Spider web**: pure `/` `\`, no bulge — delicate.
- **Water**: `:` `.` `,` repeating, low altitude, never solid `|`.
- **Wood**: `-` `_` with occasional `,` grain.

The rule: same material → same recipe everywhere. The viewer learns your words.

## X/Y resolution reality (why ASCII anti-aliasing is unique)
- 1:2 cell: ~2x X-resolution of Y at the grid level, but ~4-5x internal Y-resolution of X.
- Consequence: you have MANY more low-angle horizontal choices than near-vertical ones.
- Near-vertical lines look jagged with full glyphs → solve with negative space (`.` `'` `´` `¡`), never by thickening.
- This mechanical asymmetry exists in NO other art form. Exploit it.

## Exercises (from the video)
1. Mirror a given motif: take a shape, draw its opposite. Teaches symbol pairing.
2. Stair-step drill: `_ . -` then reverse; repeat like an instrument until memorized.
3. One-material study: draw 5 objects of the SAME material using the SAME recipe.
