---
name: threejs-image-generator-openai
description: "Generate and edit 2D image assets for Three.js games using OpenAI's GPT-Image (gpt-image-1). Use for concept sheets, image-to-3D inputs, texture references, sky/background plates, decals, logos, icons, GUI art, title/menu art, thumbnails, marketing stills, and source images that feed threejs-3d-generator. This is the OpenAI/GPT-Image alternative to threejs-image-generator (which uses Gemini): same role, OpenAI provider. Supports transparent backgrounds (great for icons/decals) and image-to-image editing. Also use for direct image editing when the user provides an image path."
---

# Three.js Image Generator (OpenAI / GPT-Image)

## Purpose

Generate 2D image assets for Three.js games using OpenAI's **gpt-image-1**. This is a drop-in
alternative to the upstream `threejs-image-generator` (which uses Google Gemini) — same use
cases, OpenAI provider. Use whichever your key fits, or run both.

> **Add-on skill.** This skill is maintained in the Phaser fork and is not part of the upstream
> `majidmanzarpour/threejs-game-skills` repo. It is purely additive, so upstream updates still
> merge cleanly. It does not modify the upstream `threejs-image-generator`.

## When To Use

- Concept art and reference sheets (characters, vehicles, props, environments).
- Source images for image-to-3D in `threejs-3d-generator` (T-pose/A-pose sheets, orthographic views).
- Texture references, sky/background plates, decals, logos, icons, GUI/title/menu art.
- Direct image editing (image-to-image) when the user provides an input image path.
- Transparent-background art (icons, decals, UI marks) via `--background transparent`.

## API Key

Set an OpenAI key as `OPENAI_API_KEY`. The script resolves keys in this order:

1. `--api-key` / `--openai-key`
2. environment `OPENAI_API_KEY`
3. a config file (KEY=value lines), searched in order:
   `$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`

Before claiming the key is unavailable, run the director credential probe (it reports
`OPENAI_API_KEY=SET|MISSING`) and paste its output; do not invent a key.

## Tool Script

```bash
# Generate (square, high quality)
python3 <skill-dir>/scripts/generate_image.py \
  --provider openai \
  -p "orthographic concept sheet of a sci-fi hover bike, neutral background" \
  -f assets/concepts/hoverbike.png

# Transparent icon/decal (ideal for HUD marks and decals)
python3 <skill-dir>/scripts/generate_image.py --provider openai \
  -p "glowing energy shield emblem, centered" -f assets/ui/shield.png --background transparent

# Portrait sky/background plate
python3 <skill-dir>/scripts/generate_image.py --provider openai \
  -p "stylized dusk sky gradient with soft clouds" -f assets/sky/dusk.png --size 1024x1536

# Image-to-image edit
python3 <skill-dir>/scripts/generate_image.py --provider openai \
  -p "repaint as a snowy night scene" -f out/night.png -i refs/scene.png
```

Notes:
- `--provider auto` (default) prefers OpenAI when `OPENAI_API_KEY` is present, else Gemini.
- `--model` overrides the model id (e.g. `gpt-image-1`, `gpt-image-1-mini`).
- `--size` ∈ `1024x1024` (default) / `1536x1024` / `1024x1536` / `auto`; `--quality` low/medium/high/auto.
- `--background transparent` outputs a transparent PNG (icons, decals, UI). gpt-image-1 always
  returns PNG bytes; the script saves them directly.

## Three.js Integration

- Use generated concept/orthographic sheets as **image-to-3D inputs** for `threejs-3d-generator`.
- Use texture/sky/decal output as `THREE.TextureLoader` sources; mark UI/decal PNGs with
  `transparent: true` materials; set `colorSpace` appropriately (sRGB for albedo, linear for data maps).
- Never put API keys in browser-side game code. Generate locally; ship only the resulting images.

## Required Report

When you generate assets, report: provider used (openai), model, output file paths, and how each
asset is consumed (texture, decal, image-to-3D input, GUI art). If the key is missing, paste the
credential probe output and state the fallback (procedural/local assets).
