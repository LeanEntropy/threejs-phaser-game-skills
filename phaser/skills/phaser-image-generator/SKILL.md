---
name: phaser-image-generator
description: "Generate and edit 2D image assets for Phaser 3 games using Google's Gemini image API. Use for concept sheets, sprite-sheet source images, tileset source images, character/enemy/prop art, backgrounds, skies, parallax layers, decals, particle textures, icons, logos, item cards, ability badges, GUI/HUD panels, title/menu art, thumbnails, marketing stills, and source images that feed phaser-sprite-generator. Triggers on build-a-2D-game, platformer, top-down, arcade, shoot-em-up, roguelike, sprite art, tileset, background plate, game logo, UI art. Also use for direct image editing when the user provides an image path."
---

# Phaser Image Generator

## Purpose

Create game-useful 2D assets and references for Phaser 3 projects. This skill is the image-generation layer for the Phaser game system: it produces concepts, sprite/tileset source art, backgrounds, parallax layers, decals, particle textures, and UI art that can be handed to `phaser-sprite-generator` for slicing into spritesheets and packing into texture atlases.

Providers: OpenAI's GPT-Image (`gpt-image-1`) and Google's Gemini image API. Select with `--provider {auto,openai,gemini}` (default `auto` = OpenAI if a key is present, else Gemini).

## When To Use

This skill is an optional enhancement, not a requirement: procedural assets (Graphics shapes + `generateTexture()`) are always a complete, fully acceptable answer. Reach for it when generated art would materially improve the result and the user wants it, for example when a Phaser game needs:

- Sprite-sheet and atlas source art for `phaser-sprite-generator`: characters, enemies, NPCs, bosses, vehicles, ships, weapons, props, pickups, projectiles, animation poses.
- Tileset source images: ground/wall/platform tiles, terrain transitions, dungeon kits, decorative tiles, autotile sheets.
- Background and environment images: skies, gradients, city horizons, nebula plates, menu/title backdrops, parallax depth layers (`tileSprite`-ready).
- VFX source art: particle textures, glow/spark/smoke/flash sprites, decals, explosion frames.
- UI art: logos, faction marks, icons, item cards, ability badges, HUD/GUI panels, buttons, title art.
- Existing-image edits, style variants, cleanup, palette alignment, or concept sheet refinements.

For premium/AAA/showcase graphics work, generating images for high-value 2D surfaces or sprite/tileset sources is one optional route to higher fidelity; procedural/local art is a complete answer, so do this only when you want generated art and the user is open to it.

## API Key

Never store API keys in skill files or browser/game code. The script resolves a key for the chosen provider in this order:

1. `--api-key` (explicit flag)
2. environment variable — `OPENAI_API_KEY` (OpenAI) or `GEMINI_API_KEY` (Gemini)
3. a config file (KEY=value lines), searched in order: `$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`

With `--provider auto` (default), OpenAI is used when `OPENAI_API_KEY` resolves, otherwise Gemini. Copy `.env.example` (repo root) to `.env` or `~/.config/game-skills/.env` to set keys via the config file.

A missing key is never a problem — procedural/local assets are a complete answer. You only need the probe if you choose to report a key as the reason generation was skipped: in that case, run the director credential probe and paste its literal SET/MISSING output so the report is accurate (it reports `OPENAI_API_KEY` and `GEMINI_API_KEY`, and also checks the config file):

```bash
bash ~/.codex/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

For Claude installs:

```bash
bash ~/.claude/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

If the probe says the provider key is `SET` but the script sees no key, run through a shell that sources the user's profile:

```bash
zsh -c 'source "$HOME/.zprofile" 2>/dev/null; source "$HOME/.zshrc" 2>/dev/null; uv run ~/.codex/skills/phaser-image-generator/scripts/generate_image.py --prompt "..." --filename assets/concepts/example.png'
```

## Tool Script

Run from the user's current project directory so output lands in the game project:

```bash
uv run ~/.codex/skills/phaser-image-generator/scripts/generate_image.py --prompt "your image description" --filename assets/concepts/output.png --resolution 2K
```

Claude install path:

```bash
uv run ~/.claude/skills/phaser-image-generator/scripts/generate_image.py --prompt "your image description" --filename assets/concepts/output.png --resolution 2K
```

Edit an existing image:

```bash
uv run ~/.codex/skills/phaser-image-generator/scripts/generate_image.py \
  --input-image assets/concepts/ship.png \
  --prompt "turn this into a battle-worn red racing livery with clearer color zones for sprite slicing" \
  --filename assets/concepts/ship-red-livery.png \
  --resolution 2K
```

Resolution mapping (Gemini, `--resolution`):

- `1K`: quick concepts, icons, draft sheets, single small sprites.
- `2K`: default production reference for sprite/tileset sources, backgrounds, UI panels.
- `4K`: hero splash/title art, high-detail tileset sheets, large sky/background and parallax plates.

### Provider selection and OpenAI options

`--provider {auto,openai,gemini}` picks the backend (default `auto`). Gemini uses `--resolution {1K,2K,4K}`. OpenAI (`gpt-image-1`) uses its own flags:

- `--model` (default `gpt-image-1`)
- `--size {1024x1024,1536x1024,1024x1536,auto}`
- `--quality {low,medium,high,auto}`
- `--background {transparent,opaque,auto}` — `transparent` is ideal for sprites, icons, and decals.

Generate with OpenAI, transparent background (great for an icon/decal/sprite source):

```bash
uv run ~/.codex/skills/phaser-image-generator/scripts/generate_image.py \
  --provider openai --background transparent \
  --prompt "crisp game UI ability badge for a lightning dash, centered, high contrast" \
  --filename assets/ui/dash-badge.png --size 1024x1024 --quality high
```

Generate a wide OpenAI background plate:

```bash
uv run ~/.codex/skills/phaser-image-generator/scripts/generate_image.py \
  --provider openai \
  --prompt "wide parallax city skyline at dusk, layered depth, no foreground subject" \
  --filename assets/backgrounds/city-dusk.png --size 1536x1024 --quality high
```

## Prompt Patterns

Sprite / sprite-sheet source (single object, ready to slice):

```text
Create a clean 2D game sprite of [asset]. Centered single object, full object visible, transparent or flat plain background, crisp readable silhouette, consistent flat lighting, [pixel-art/hand-painted/vector/genre style], no motion blur, no cropped parts, no text, no drop shadow baked onto the ground.
```

Character/enemy pose sheet (feeds phaser-sprite-generator for animation frames):

```text
Create a uniform sprite pose sheet for [character]: a grid of [N] frames showing [idle/walk/run/jump/attack], all frames same size and aligned, consistent silhouette and palette across frames, transparent background, side-view orthographic, no overlap between frames, no text labels.
```

Tileset source:

```text
Create a seamless 2D game tileset reference for [theme]. Top-down/side-view orthographic, uniform tile grid, edges that tile cleanly, clear material variation, flat readable lighting, no perspective, no baked strong shadows, [pixel/painted style], no text.
```

Logo/icon/UI art:

```text
Create a crisp game UI [logo/icon/badge/panel/button] for [faction/item/ability]. Transparent-friendly silhouette, high contrast at small size, [genre styling], no tiny unreadable text.
```

Background / sky / parallax layer:

```text
Create a wide 2D game background plate of [environment]. Layered depth for parallax, readable horizon, [time/weather/style], suitable behind a real-time Phaser scene, tileable horizontally if possible, no foreground subject.
```

## Phaser Integration Rules

- Save concepts and sprite/tileset sources under `assets/concepts/`.
- Save backgrounds, decals, particle textures, icons, and GUI source images under `assets/backgrounds/`, `assets/decals/`, `assets/vfx/`, or `assets/ui/`.
- For spritesheets/atlases, hand the saved image path to `phaser-sprite-generator` to slice into uniform frames or pack into an atlas + JSON, and record the chain in the external asset ledger.
- Do not call the image API from client-side game code.
- Load results deliberately: `this.load.image` for single sprites/backgrounds, `this.load.spritesheet(key, png, { frameWidth, frameHeight })` for sliced sheets, `this.load.atlas(key, png, json)` for packed atlases; build animations with `this.anims.create({ frames: this.anims.generateFrameNumbers(...) })`.
- Keep PNG with alpha for sprites/UI/particles; use JPG/WebP for large opaque backgrounds where the project pipeline supports it.
- Verify how the image appears in game (correct scale, transparent background, clean tiling/parallax), not only that the file exists.

## Required Report

Report:

- Credential probe output or command blocker.
- Prompt and purpose.
- Output path.
- Resolution.
- Whether the image was used directly, edited further, or handed to `phaser-sprite-generator`.
- Any remaining integration work such as background transparency cleanup, slicing into frames, atlas packing, palette alignment, or seamless-tiling fixes.

Do not mark a premium graphics phase complete if the needed image outputs are missing and the only justification is "procedural is enough" for high-value UI, background, sky, tileset, decal, logo, or sprite-source surfaces.
