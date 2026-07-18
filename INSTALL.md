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

## Private repo note

Right now `big-herm-optional-skills` is private.

Because of that, the raw `raw.githubusercontent.com/.../SKILL.md` commands are not the primary cross-device path. While this repo stays private, treat optional-pack installs as clone-only unless you have a verified authenticated fetch path that works with Hermes.

## If this repo becomes public later

When or if you make the repo public, retest raw installs before calling them supported defaults.

Minimum retest:

```bash
hermes skills inspect <raw-skill-url>
hermes skills install <raw-skill-url> --yes
```

Then confirm the installed skill directory contains the expected `references/`, `scripts/`, `templates/`, or other companion files.

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
