# Draft GitHub Issue — Hermes raw URL skill installer behavior

## Title
Raw `hermes skills install https://.../SKILL.md` aborts whole URL install when one referenced companion path 404s or when prose references are over-matched

## Summary
Hermes Agent v0.18.2 can successfully inspect a raw `SKILL.md` URL, but URL-based install may fail for heavier skills because the installer attempts to fetch every detected support-file reference and aborts the entire install if any one reference fails.

## Verified environment
- Hermes Agent: `v0.18.2 (2026.7.7.2)`
- Install method: git
- Python: `3.11.15`
- Host: Windows 10
- Shell backend: git-bash / MSYS via Hermes terminal tool

## What works
- `hermes skills inspect https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/creative/p5js/SKILL.md`
- direct HTTP fetch of the same URL returns `200 OK`
- URL install can succeed for simpler skills with clean support references, for example `dogfood`

## What fails
A heavier skill like `p5js` or other support-file-heavy skills may fail with:

```text
Error: Could not fetch 'https://raw.githubusercontent.com/.../SKILL.md' from any source.
```

Even though:
- the main `SKILL.md` URL itself is reachable
- `inspect` succeeds
- many referenced support files are reachable

## Repro examples
### Succeeds
```bash
hermes -p raw-skill-dogfood-verify skills install https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/dogfood/SKILL.md --yes
```

### Fails
```bash
hermes -p raw-skill-public-verify skills install https://raw.githubusercontent.com/NousResearch/hermes-agent/main/skills/creative/p5js/SKILL.md --yes
```

## Root cause analysis
From source inspection:
- `UrlSource.inspect()` only fetches `SKILL.md`
- `UrlSource.fetch()` fetches `SKILL.md` plus all detected support references
- if any support reference returns `None`, the whole fetch returns `None`
- CLI then reports `Could not fetch '<url>' from any source`

Relevant code paths:
- `hermes_cli/skills_hub.py:126` `_resolve_source_meta_and_bundle`
- `hermes_cli/skills_hub.py:502` `do_install`
- `tools/skills_hub.py:155-179` `_referenced_support_paths`
- `tools/skills_hub.py:1488-1532` `UrlSource.fetch`

## Observed bad reference patterns
The support-path extractor appears to over-match some prose or placeholder paths, and the installer is strict enough that one bad path kills the whole install.

Examples observed during testing:
- `creative/p5js` -> bogus support path `references`
- `creative/baoyu-infographic` -> `references/layouts`, `references/styles`
- `software-development/hermes-agent-skill-authoring` -> `references/*.md`, `references/templates/scripts/assets`

Additional failures were observed where referenced script paths 404 from the raw URL path even though the base `SKILL.md` is valid.

## Expected behavior
Prefer one of these behaviors:
1. Only fetch explicitly valid file references, not directory-like or wildcard-like prose mentions
2. Warn and skip missing support files instead of aborting the entire install
3. Surface which exact referenced path failed so the error is actionable

## Actual behavior
One failing support-file fetch causes the whole URL install to fail with a generic top-level fetch error.

## Suggested fixes
- tighten `_referenced_support_paths()` so it does not accept directory-like, wildcard-like, or placeholder prose references
- in `UrlSource.fetch()`, collect and report individual missing support paths
- optionally continue install with warnings when missing companion files are non-critical

## Extra note from BIG HERM testing
A private GitHub repo adds a separate limitation: raw `raw.githubusercontent.com/...` URLs may 404 for unauthenticated fetches. That is distinct from this installer bug. After switching the companion repo public, retest raw installs separately from the private-repo access problem.
