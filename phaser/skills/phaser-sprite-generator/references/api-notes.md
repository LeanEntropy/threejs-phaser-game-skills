# Gemini Image API + Phaser Sprite Format Notes

These notes summarize the Gemini image API usage this skill relies on, plus the
spritesheet and atlas formats Phaser 3 loads. The script combines a Gemini
generation call with local Pillow processing (slice / pack / key-to-alpha / trim).

## Gemini Image API

- SDK: `google-genai` (`from google import genai; from google.genai import types`).
- Auth: `genai.Client(api_key=...)`. Key resolution order: `--api-key`, then the
  `GEMINI_API_KEY` environment variable. Never embed the key in skill files or
  the shipped game client.
- Model: `gemini-3-pro-image-preview`.
- Call: `client.models.generate_content(model=..., contents=..., config=...)`.
- `contents` is either the prompt string (text-to-image) or `[input_image, prompt]`
  for image-to-image edits/variations (the input image goes first).
- `config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"],
  image_config=types.ImageConfig(image_size="1K"|"2K"|"4K"))`.
- Response: iterate `response.parts`; each part has either `.text` (model notes)
  or `.inline_data` (the image). `inline_data.data` is raw bytes (occasionally a
  base64 string — decode if so), opened with `PIL.Image.open(BytesIO(data))`.

Treat a response with no image part as a generation error. Generation is a
build-time step; outputs are saved to disk and committed/copied into the game's
`assets/`, never fetched live by the client.

## Output Modes (what this skill generates)

- `single sprite`: one centered object/character/prop/icon, transparent bg.
- `spritesheet (uniform grid)`: one animation strip or a set of frames laid out
  as an N×M grid of identical cells. Prompt MUST request uniform cell size,
  identical pivot/scale per cell, even spacing, and no frame numbers/labels.
- `tileset page`: a grid of orthographic/top-down tiles (floor, wall, door, …)
  with seamless edges and no baked perspective/shadow bleed.
- `atlas source`: a folder of individual frame PNGs (from `sheet` slicing or
  separate generations) that the `atlas` subcommand packs.

## Transparency Enforcement (local)

Gemini often returns a near-solid backdrop instead of true alpha. The script
enforces transparency locally with Pillow:

- `--transparent` adds a "transparent background" clause to the prompt AND keys
  the chosen background color to alpha after generation.
- `--key-color "#rrggbb"` sets the color to remove; default is the top-left
  corner pixel. `--tolerance N` widens the per-channel match (default 24) for
  anti-aliased or noisy backdrops.
- `--trim` crops fully transparent margins via the image bounding box, tightening
  the frame around the art (keeps origins and collision boxes honest).

Pick a backdrop color that does not appear in the sprite (a chroma-key magenta
`#ff00ff` or green `#00ff00` is safest), or generate against a flat color you can
key cleanly.

## Slicing a Uniform Grid (`sheet`)

- Cell size comes from `--frame-width/--frame-height` (exact) OR from
  `--columns/--rows` (the script divides the sheet). Prefer explicit frame size
  when the sheet may not divide evenly; the script warns on a non-even split.
- `--margin` is the outer border before the first cell; `--spacing` is the gap
  between cells. These map 1:1 to Phaser's `frameConfig.margin`/`spacing`.
- Frames are emitted as `name_000.png`, `name_001.png`, … in row-major order
  (left-to-right, top-to-bottom) — the same order Phaser indexes frames.
- The command prints the exact `this.load.spritesheet(...)` `frameConfig`.

## Packing an Atlas (`atlas`)

- Input: a folder of PNG frames. Output: `<out>.png` + `<out>.json`.
- Layout: a simple shelf/row packer; frames wrap to a new shelf at a target
  width (default a near-square power-of-two by total area; override with
  `--max-width`). `--padding` (default 2) prevents bleeding between frames.
- `--pot` rounds the atlas dimensions up to powers of two (some GPUs/mipmaps
  prefer this; Phaser does not require it).
- `--trim` crops each frame and records the original frame box so Phaser can
  re-expand it (see the JSON fields below). Without `--trim`, frames keep their
  full size and `spriteSourceSize == sourceSize`.

## Phaser Texture Formats

### Uniform spritesheet — `this.load.spritesheet`

```ts
this.load.spritesheet('hero-run', 'hero-run.png', {
  frameWidth: 64, frameHeight: 64,
  margin: 0, spacing: 0,   // match the slice margins/spacing
  startFrame: 0, endFrame: 7,
});
```

Frames are referenced by integer index (`generateFrameNumbers`).

### Texture atlas — `this.load.atlas` (TexturePacker JSON Hash)

This skill emits the **JSON Hash** form: `frames` is an object keyed by frame
name (the original PNG file name). Phaser also accepts the **JSON Array** form
(`frames` as an array, each with a `filename`); both load with `this.load.atlas`.
Per-frame schema this script writes:

```json
{
  "frames": {
    "hero_000.png": {
      "frame":            { "x": 0, "y": 0, "w": 48, "h": 60 },
      "rotated":          false,
      "trimmed":          true,
      "spriteSourceSize": { "x": 8, "y": 4, "w": 48, "h": 60 },
      "sourceSize":       { "w": 64, "h": 64 }
    }
  },
  "meta": { "image": "hero.png", "format": "RGBA8888",
            "size": { "w": 256, "h": 256 }, "scale": "1" }
}
```

- `frame`: the rect inside the atlas PNG.
- `trimmed` + `spriteSourceSize` + `sourceSize`: when trimmed, Phaser offsets the
  drawn frame so the sprite still occupies the original cell box (origins stay
  consistent across an animation even when individual frames were trimmed).
- `rotated` is always `false` here (the packer does not rotate frames).

Frames are referenced by name (`generateFrameNames`).

### Aseprite — `this.load.aseprite`

Phaser loads `.aseprite`-exported JSON with `this.load.aseprite(key, png, json)`
and builds tag-based animations via `this.anims.createFromAseprite(key)`. Use it
when art is authored in Aseprite; this skill emits the more portable
TexturePacker Hash instead.

### Bitmap fonts — `this.load.bitmapFont`

Not produced by this skill, but related: glyph "sprite sheets" load via
`this.load.bitmapFont(key, png, xml)` (BMFont/XML). Generate font glyph art with
`phaser-image-generator` if needed.

## Game Defaults

- Always `--transparent` for in-game sprites; `--trim` for atlas frames.
- Prefer a uniform spritesheet for a single simple animation strip; prefer an
  atlas for a whole character (mixed-size clips), a prop kit, or a UI set.
- Use `1K` for icons/small sprites, `2K` for hero sheets, `4K` only for large
  multi-row sheets that need the detail; downscale cells locally for low-DPR runs.
- Keep one palette per family; reuse a `--style` clause and `--input-image` lock.
- For tilesets, generate orthographic/top-down tiles with seamless edges and no
  perspective/shadow bleed, then slice with exact `--frame-width/--frame-height`.
- Pin cell size in the prompt (e.g. "32×32 cells") so frames divide evenly.
