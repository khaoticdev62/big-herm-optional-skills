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

For raw skill installs, use the raw GitHub URL to the pack's `SKILL.md`.

Example:

```bash
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/creative/comfyui/SKILL.md
```

Note: some skills include references, scripts, templates, tests, or workflows alongside `SKILL.md`. For those, cloning this repo locally is the safer path.

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
