---
name: phaser-sprite-generator
description: "Generate, slice, pack, trim, and download 2D game art for Phaser 3 games using the Gemini image API plus local image processing. Use for character/player/enemy/NPC sprites, object and prop sprites, pickup and item icons, uniform-frame spritesheets, animation strips (idle/walk/run/jump/attack/hurt/death cycles), tilesets and tilemap pages, and texture atlases with TexturePacker JSON for this.load.atlas. Produces transparent-background PNGs with a consistent palette for platformers, top-down, arcade, shoot-em-up, roguelike, and brick/breakout games. Pair with phaser-image-generator for concepts, backgrounds, skies, decals, logos, icons, and GUI art before sprite generation."
---

# Phaser Sprite Generator

## Purpose

Create production-oriented 2D game art, then prepare it for Phaser 3 games. This is the Phaser game system's art-generation layer; it generates the source art for character/object/enemy sprites, uniform-frame spritesheets, tilesets, and texture atlases via OpenAI's GPT-Image (`gpt-image-1`) or Google's Gemini image API (select with `--provider {auto,openai,gemini}`, default `auto`), plus local Pillow (PIL) image processing for slicing grids into frames, packing frames into an atlas PNG + TexturePacker JSON, enforcing transparent backgrounds, and trimming dead space. The slicing, packing, key-to-alpha, and trim steps are provider-agnostic — they run identically on art from either backend. There are no 3D models in 2D — the output is sliced PNG spritesheets and atlases that `this.load.spritesheet` and `this.load.atlas` consume directly.

## API Key

Never store API keys in skill files or client-side game code. The script resolves a key for the chosen provider in this order:

1. `--api-key` (explicit flag)
2. environment variable — `OPENAI_API_KEY` (OpenAI) or `GEMINI_API_KEY` (Gemini)
3. a config file (KEY=value lines), searched in order: `$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`

With `--provider auto` (default), OpenAI is used when `OPENAI_API_KEY` resolves, otherwise Gemini. Copy `.env.example` (repo root) to `.env` or `~/.config/game-skills/.env` to set keys via the config file. Source-art generation supports either provider; slicing/packing/trim is provider-agnostic.

A missing key is never a problem — procedural/local assets are a complete answer. Only if you choose to report a key as the reason generation was skipped, run this probe first so the report is accurate:

```bash
bash ~/.claude/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

For Codex installs:

```bash
bash ~/.codex/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

Paste the literal `OPENAI_API_KEY=SET|MISSING` / `GEMINI_API_KEY=SET|MISSING` output in the report when you report a key as the skip reason (the probe also checks the config file). Do not conclude the key is unavailable from a plain non-interactive shell until this probe has sourced the user's shell profiles. None of this is required when you simply choose procedural/local assets.

When the probe says SET but `phaser_sprite_asset.py` reports a missing key, the key is exported in an interactive-only profile (e.g. `~/.zshrc`). Wrap script invocations the same way the probe does:

```bash
zsh -c 'source "$HOME/.zprofile" 2>/dev/null; source "$HOME/.zshrc" 2>/dev/null; python3 .../phaser_sprite_asset.py ...'
```

Use the API only from local/server-side tooling. Image generation is a build-time step; never call OpenAI or Gemini from the shipped game client.

## Tool Script

Reference gate:

- Load `references/api-notes.md` before provider API work, model choices, response handling, transparency enforcement, or spritesheet-vs-atlas format decisions.
- Load `references/phaser-integration.md` before importing generated art into a game or advising spritesheet/atlas loading, animation, origin/pivot, or pooling.
- Load `references/image-generator-workflows.md` before pairing `phaser-image-generator` with this skill for concepts, sprite-sheet sources, tileset sources, backgrounds, UI art, logos, decals, or icons.

Track required references in a reference ledger with yes/no, path, and failure reason. Do not mark an asset pipeline complete while a required reference is skipped.

Run from the user's current project directory:

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py --help
```

If installed in Codex instead of Claude, use:

```bash
python3 ~/.codex/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py --help
```

Pillow (PIL) does the slicing/packing/trimming. If Pillow is missing, `generate` still saves the raw Gemini image (with a clear message) and `sheet`/`atlas` exit with an install hint — install with `pip install pillow` or run via `uv run` (the script header declares the dependency).

## Common Commands

Recommended premium animated character strip (generate, then slice):

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py generate \
  --prompt "8-frame side-view run cycle of a [hero], strong readable silhouette, consistent palette, identical pivot and scale per frame" \
  --filename assets/src/hero-run.png \
  --transparent --columns 8 --rows 1 --resolution 2K \
  --style "crisp pixel art, 64x64 cells"

python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py sheet \
  --image assets/src/hero-run.png --columns 8 --rows 1 \
  --out-dir assets/frames/hero-run --trim
```

Single object / prop / pickup sprite (transparent, trimmed):

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py generate \
  --prompt "single health potion pickup, centered, clean outline, game icon" \
  --filename assets/src/potion.png --transparent --trim
```

Enemy multi-row spritesheet (idle + walk + attack rows):

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py generate \
  --prompt "enemy slime spritesheet: row 1 idle (4), row 2 hop (4), row 3 attack (4), uniform cells" \
  --filename assets/src/slime.png --transparent --columns 4 --rows 3

python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py sheet \
  --image assets/src/slime.png --columns 4 --rows 3 --out-dir assets/frames/slime
```

Tileset page (slice into individual tiles for a tilemap):

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py generate \
  --prompt "16x16 top-down dungeon tileset: floor, wall, wall-corner, door, stairs, torch, chest, rubble; orthographic, seamless edges, no perspective" \
  --filename assets/src/dungeon-tiles.png --columns 8 --rows 8

python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py sheet \
  --image assets/src/dungeon-tiles.png --frame-width 16 --frame-height 16 \
  --out-dir assets/frames/dungeon-tiles
```

Pack a folder of frames into one atlas PNG + TexturePacker JSON Hash:

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py atlas \
  --frames-dir assets/frames/hero-run --out assets/atlas/hero \
  --padding 2 --trim --pot
```

Normalize an existing sheet that has a colored background (key to alpha + trim) while slicing:

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py sheet \
  --image vendor/character.png --columns 6 --rows 1 \
  --key-color "#00ff00" --tolerance 30 --trim \
  --out-dir assets/frames/character
```

Edit/vary an existing sprite (image-to-image):

```bash
python3 ~/.claude/skills/phaser-sprite-generator/scripts/phaser_sprite_asset.py generate \
  --prompt "same character, swap blue armor for red, keep pose and pixel grid" \
  --input-image assets/src/hero-idle.png --filename assets/src/hero-idle-red.png \
  --transparent --trim
```

## Phaser Image Generator Pairing

Use `phaser-image-generator` before sprite generation when the asset benefits from a strong concept or non-sprite art:

- Character/enemy concept sheet, front/side/back reference, color callouts, a whole-family style sheet.
- Tileset look reference, biome palette, prop family reference.
- Backgrounds, sky/horizon plates, parallax layers, menu/title art.
- Logos, faction marks, item/ability/HUD icons, hazard signs, button skins, GUI panels.

`phaser-image-generator` and this skill share the same providers (OpenAI `gpt-image-1` / Gemini) and key resolution (`OPENAI_API_KEY` / `GEMINI_API_KEY`, or the config file). The division of labor: `phaser-image-generator` makes concept art, backgrounds, and standalone GUI/icon art; `phaser-sprite-generator` makes the in-game sprite/spritesheet/tileset/atlas pipeline (generate → slice → pack → transparent). Load `references/image-generator-workflows.md` for prompt patterns and the handoff before generating inputs.

## Phaser Integration

Load `references/phaser-integration.md` before importing generated art into a game. In short:

- Use `this.load.spritesheet(key, url, { frameWidth, frameHeight, margin, spacing })` for uniform grid sheets; the `sheet` subcommand prints the exact frameConfig.
- Use `this.load.atlas(key, pngUrl, jsonUrl)` for packed atlases; the `atlas` subcommand writes a TexturePacker JSON Hash that Phaser parses natively.
- Build animations with `this.anims.create({ key, frames, frameRate, repeat })` using `generateFrameNumbers` (spritesheet) or `generateFrameNames` (atlas).
- Set `origin`/pivot deliberately for feet-anchored characters and centered projectiles; trimmed atlas frames carry `spriteSourceSize` so Phaser keeps the original frame box.
- Pool frequently spawned sprites (bullets, particles-as-sprites, pickups) in Groups; never generate art at runtime.

## Spritesheet vs Atlas Decision

Load `references/api-notes.md` for the full format tables. The short rule:

- **Uniform spritesheet** (`this.load.spritesheet`) — one PNG, every frame the same cell size. Best for single animation strips and tilesets. Cheapest to author: generate a grid, slice, done. No JSON.
- **Texture atlas** (`this.load.atlas`) — one packed PNG + JSON describing arbitrary-sized, trimmed, named frames. Best for a whole character's mixed-size animations, an object/prop kit, or a UI set — fewer textures, fewer draw-call batches, smaller memory. Author by slicing/collecting frames then `atlas` to pack.
- **Aseprite** — Phaser also loads `this.load.aseprite(key, png, json)` for `.aseprite`-exported JSON with tag-based animations; use it when the source art is authored in Aseprite. This skill emits the TexturePacker Hash form, which is the most portable.

## Quality Rules

- Improve the user's prompt with palette, silhouette readability, cell-uniformity, view angle, and game-use constraints before calling the image provider (OpenAI or Gemini).
- Always request and enforce a transparent background for sprites (`--transparent`); key out the backdrop and `--trim` dead space so origins and collision boxes stay tight.
- For animation strips, demand identical pivot, scale, and cell size per frame in the prompt — provider drift between frames is the main cause of jittery animations; regenerate rather than ship a wobbling cycle.
- Keep one consistent palette across a sprite family; pass a shared `--style` clause and, when needed, an `--input-image` reference for color/style lock.
- For tilesets, request orthographic/top-down tiles with seamless edges and no baked perspective or drop shadows that bleed across cells.
- Prefer atlases over many separate spritesheets for memory and batch count; prefer one uniform sheet for a single simple animation.
- Match resolution to budget: `1K` for icons/small sprites, `2K` for hero sheets, `4K` only when a large multi-row sheet needs detail; downscale cells locally if the game runs at low DPR.
- Save generated source art under `assets/src/`, sliced frames under `assets/frames/`, and packed output under `assets/atlas/` or `assets/spritesheets/`.
- Always save/download outputs immediately; treat generation as a build step, never a runtime call.
- Report the credential probe output, reference ledger, prompts used, model, output paths (source PNG, frames dir, atlas PNG/JSON), resolution, transparency/trim settings, grid dimensions, the Phaser load + frameConfig/atlas snippet, and any missing/failed steps.
