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

## Private repo note

Right now this companion repo is private.

That means the raw GitHub URLs shown above are not a production-safe install path for other devices unless those devices have authenticated access that Hermes can actually use for the fetch. In practical terms, while this repo stays private, treat it as clone-only.

## If this repo becomes public later

If you later make `big-herm-optional-skills` public, retest raw installs before promoting them as safe defaults.

Why: public visibility removes the private-repo 404 problem, but it does not guarantee every heavyweight pack will install cleanly from raw URL. Some packs may still fail if companion-file references inside `SKILL.md` do not resolve cleanly through Hermes' raw URL installer.

Recommended future validation pass:

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
