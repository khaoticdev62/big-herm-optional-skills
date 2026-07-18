# BIG HERM Optional Skills

`big-herm-optional-skills` is the companion repo for heavyweight, niche, or template-rich skill packs that do not need to ship in the base BIG HERM distribution.

Use this repo when you want to add advanced specialty workflows without bloating `big-herm-distribution`.

## What stays in the base repo

The base `big-herm-distribution` keeps:

- BIG HERM identity and system prompt
- crew/orchestration skills
- theme and Mission Control assets
- MCP wiring
- install docs and validation scripts
- core support skills needed for day-one use

## What lives here

This repo carries optional packs such as:

- creative media and design pipelines
- MLOps and model-operation packs
- office/document specialty packs
- research-paper authoring bundles
- external workspace integrations that are not required everywhere

## Included packs

See `MANIFEST.md` for the canonical inventory.

## Current compatibility snapshot

Verified on 2026-07-18 after switching this repo public and rerunning raw-URL tests on Hermes Agent `v0.18.2`.

| Pack | `inspect` | Raw install | Failure type | Current label | Verified reason |
|---|---|---|---|---|---|
| `creative/comfyui` | yes | blocked | scanner block (`DANGEROUS`) | clone-only | Hermes security scan returned `DANGEROUS`; install blocked |
| `productivity/powerpoint` | yes | failed | fetch/path failure | clone-only | referenced companion file `scripts/office/soffice.py` returned 404 |
| `productivity/google-workspace` | yes | blocked | scanner block (`DANGEROUS`) | clone-only | Hermes security scan returned `DANGEROUS`; install blocked |
| `research/research-paper-writing` | yes | failed | fetch/path failure | clone-only | referenced companion file `scripts/make_figure2.py` returned 404 |
| `creative/p5js` | yes | failed | fetch/path failure | clone-only | parser/fetch path hit bogus reference `references` -> 404 |

## Verified raw-safe wins

After testing every optional pack currently in this repo, I found 2 packs that installed successfully from the public raw URL path without needing `--force`:

| Pack | `inspect` | Raw install | Failure type | Current label | Verified note |
|---|---|---|---|---|---|
| `creative/ascii-video` | yes | installed | none | raw-safe | Installed `SKILL.md` plus 8 `references/*.md` companion files |
| `creative/manim-video` | yes | installed | none | raw-safe | Installed `SKILL.md`, 14 `references/*.md` files, and `scripts/setup.sh` |

I tested all currently published optional packs and did not find a third raw-safe pack in this repo state.

Issue draft for the Hermes raw URL installer behavior lives at `docs/HERMES-RAW-URL-INSTALLER-BUG-DRAFT.md`.

## Install one pack

Recommended default for heavyweight packs: clone this repo first.

Why: raw `hermes skills install https://.../SKILL.md` works for some URL-sourced skills, but verified testing on Hermes Agent `v0.18.2` showed several heavier packs fail when their `SKILL.md` references companion paths that Hermes cannot fetch cleanly from the raw URL flow.

Use raw install only as a convenience path for simpler packs or after you have personally verified that pack installs cleanly.

Example raw install:

```bash
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/comfyui/SKILL.md
```

Top 5 optional packs from this repo:

```bash
# convenient, but not guaranteed for heavyweight packs
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/comfyui/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/productivity/powerpoint/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/productivity/google-workspace/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/research/research-paper-writing/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/p5js/SKILL.md
```

Clone-first is the safer path whenever a pack includes `references/`, `scripts/`, `templates/`, tests, workflows, or other companion files.

## Public repo note

This companion repo is now public.

That removes the earlier private-repo 404 problem for raw GitHub URLs, but it still does NOT make heavyweight raw installs production-safe by default.

Verified retesting after the visibility change showed the top 5 optional packs are still clone-only for other reasons:
- some raw installs are blocked by Hermes security scanning
- some fail because referenced companion files 404
- some fail because the raw URL support-file parser/fetch path still mis-resolves references

## Ongoing retest rule

Any time a pack changes materially, retest before promoting raw install as safe.

Minimum validation pass:

```bash
hermes skills inspect <raw-skill-url>
hermes skills install <raw-skill-url> --yes
```

Then verify the installed skill directory actually contains the expected companion files.

## Clone the whole optional library

```bash
git clone https://github.com/khaoticdev62/big-herm-optional-skills.git
```

## Compatibility

Current target compatibility:

- `big-herm-distribution >= v1.3.0`

## Safety rules

Do not commit:

- `.env`
- auth tokens
- local sessions
- local memories
- generated logs
- machine-specific runtime state
- recovered secrets from third-party tooling

## Why this split exists

The goal is simple:

- keep BIG HERM fast to install on every machine
- keep optional power-user packs available when you actually need them
- stop the main distribution repo from turning into a giant junk drawer
