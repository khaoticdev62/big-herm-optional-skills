#!/usr/bin/env python3
"""validate_art.py - Enforce the Stone Story pro line-art rules on a text file.

Checks:
  - monospace_grid: every row equal width (after strip) -> no accidental drift
  - stray_control: tabs / non-breaking spaces that break the grid
  - off_grid_alphanumerics: letters/digits NOT in the allowed sparse set
  - empty_rows: fully blank lines (usually trim)

Exit code 0 = no blocking issues. Exit code 1 = blocking issues found.
"""
import argparse
import json
import sys

# Sparse alphanumerics that are allowed in pro line-art (deliberate use).
ALLOWED_ALNUM = set("ovVtl7ucxOVTL7UCX")

# Glyphs considered part of the pro line-art palette (any of these is "on-style").
PALETTE = set(
    "/\\|_.:,`'\""  # core
    "´¯¡·"         # extended fit-the-style
    "│─┌┐└┘├┤┬┴┼"  # box drawing
    " "
) | ALLOWED_ALNUM

def classify(text):
    lines = text.split("\n")
    issues = {
        "monospace_grid": [],
        "stray_control": [],
        "off_grid_alphanumerics": [],
        "empty_rows": [],
    }
    # Widths are only meaningful for real art rows, not frame separators or blanks.
    def _is_sep(ln):
        return set(ln) == {"-"} and len(ln) >= 3
    widths = [len(ln) for ln in lines]
    art_widths = [w for ln, w in zip(lines, widths) if ln.strip() != "" and not _is_sep(ln)]
    if len(set(art_widths)) > 1:
        from collections import Counter
        modal = Counter(art_widths).most_common(1)[0][0]
        for i, w in enumerate(widths, 1):
            if w != modal:
                issues["monospace_grid"].append({"line": i, "width": w, "expected": modal})

    for i, ln in enumerate(lines, 1):
        # Skip frame separators used by ascii_animation (lines of "---").
        if set(ln) == {"-"} and len(ln) >= 3:
            continue
        if "\t" in ln or " " in ln:
            issues["stray_control"].append({"line": i, "note": "tab or non-breaking space present"})
        if ln.strip() == "":
            issues["empty_rows"].append(i)
        for ch in ln:
            if ch.isalnum() and ch not in ALLOWED_ALNUM:
                issues["off_grid_alphanumerics"].append({"line": i, "char": ch})

    blocking = bool(issues["monospace_grid"] or issues["stray_control"])
    return issues, blocking

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="text art file to validate")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()

    try:
        with open(args.path, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        sys.exit(2)

    issues, blocking = classify(text)

    if args.json:
        print(json.dumps({"issues": issues, "blocking": blocking}, indent=2))
        sys.exit(1 if blocking else 0)

    print(f"== ASCII Line-Art Validator: {args.path} ==")
    any_issue = False
    if issues["monospace_grid"]:
        any_issue = True
        print("\n[RED] MONOSPACE GRID DRIFT (blocking):")
        for r in issues["monospace_grid"]:
            print(f"   line {r['line']}: width {r['width']} (expected {r['expected']})")
    if issues["stray_control"]:
        any_issue = True
        print("\n[RED] STRAY CONTROL CHARS (blocking):")
        for r in issues["stray_control"]:
            print(f"   line {r['line']}: {r['note']}")
    if issues["off_grid_alphanumerics"]:
        print("\n[YELLOW] OFF-GRID ALPHANUMERICS (immersion risk):")
        seen = {}
        for r in issues["off_grid_alphanumerics"]:
            seen[r["char"]] = seen.get(r["char"], 0) + 1
        for ch, n in sorted(seen.items()):
            print(f"   '{ch}' x{n}  -> activates language center, breaks static look")
    if issues["empty_rows"]:
        print(f"\n[BLUE] EMPTY ROWS: {len(issues['empty_rows'])} (usually trim)")
    if not any_issue and not issues["off_grid_alphanumerics"] and not issues["empty_rows"]:
        print("\n[GREEN] CLEAN. Production-ready line-art.")
    elif not blocking:
        print("\n[YELLOW] No blocking issues, but review immersion warnings above.")
    sys.exit(1 if blocking else 0)

if __name__ == "__main__":
    main()
