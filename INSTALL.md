# INSTALL — BIG HERM Optional Skills

## Option 1: clone the repo locally

```bash
git clone https://github.com/khaoticdev62/big-herm-optional-skills.git
cd big-herm-optional-skills
```

This is the best option when a pack ships with supporting files such as:

- `references/`
- `scripts/`
- `templates/`
- `tests/`
- `workflows/`

## Option 2: install a single skill from GitHub raw

This is a convenience path, not the safest default for heavyweight packs.

Verified testing on Hermes Agent `v0.18.2` showed that some URL-installed skills succeed, but several heavier packs fail when their `SKILL.md` references companion paths that the raw URL installer cannot fetch cleanly.

Example:

```bash
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/comfyui/SKILL.md
```

Use raw install only when:

- you only need one pack
- the pack is relatively simple
- or you have already verified that this exact pack installs cleanly from raw URL

## Public repo note

`big-herm-optional-skills` is now public.

That fixes the earlier private-repo access problem, but it does not automatically make raw installs safe defaults for heavyweight packs. Verified retesting still showed clone-only outcomes caused by security-scan blocks, missing companion files, and raw support-reference resolution failures.

## Ongoing retest rule

Retest any pack before calling raw install supported.

Minimum retest:

```bash
hermes skills inspect <raw-skill-url>
hermes skills install <raw-skill-url> --yes
```

Then confirm the installed skill directory contains the expected `references/`, `scripts/`, `templates/`, or other companion files.

## Currently verified raw-safe examples

Verified on 2026-07-18 with Hermes Agent `v0.18.2`:

```bash
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/ascii-video/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/manim-video/SKILL.md
```

These two installed successfully from raw URL without `--force` in fresh `--no-skills` test profiles.

## Top 5 ready-to-copy install commands

```bash
# convenient, but clone-first is safer for heavyweight packs
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/comfyui/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/productivity/powerpoint/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/productivity/google-workspace/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/research/research-paper-writing/SKILL.md
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/p5js/SKILL.md
```

## Recommended first packs

If you want the easiest raw-URL smoke tests first, start with:

- `creative/ascii-video`
- `creative/manim-video`

If you want the flagship heavyweight packs, use clone-first:

- `creative/comfyui`
- `productivity/powerpoint`
- `productivity/google-workspace`
- `research/research-paper-writing`
- `creative/p5js`

## After install

List available skills:

```bash
hermes skills list
```

Load a skill in a session:

```text
/skill comfyui
```

Or start Hermes with a preload:

```bash
hermes -s comfyui
```

## External dependency note

Many optional packs need extra software, credentials, or cloud access. Read each pack's `SKILL.md` before use.

Common examples:

- ComfyUI local/runtime dependencies
- Google API credentials
- Office/PPTX tooling
- model-serving stacks
- research LaTeX toolchains

## Safety

Never copy your personal `.env`, auth files, or runtime state into this repo.
