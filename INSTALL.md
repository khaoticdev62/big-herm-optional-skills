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

Example:

```bash
hermes skills install https://raw.githubusercontent.com/khaoticdev62/big-herm-optional-skills/main/skills/creative/comfyui/SKILL.md
```

Use this when you only need one pack and the skill does not depend heavily on local companion files.

## Top 5 ready-to-copy install commands

```bash
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
