# OpenAI GPT-Image (gpt-image-1) — API notes

## Auth & keys

- Python SDK: `from openai import OpenAI; client = OpenAI(api_key=...)`.
- Key resolution (this skill's script): `--api-key`/`--openai-key` → `OPENAI_API_KEY` env →
  config file (`$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`).
- Never embed keys in browser/game code. Generate locally; ship only the output images.

## Generation

```python
result = client.images.generate(
    model="gpt-image-1",
    prompt="...",
    size="1024x1024",         # or 1536x1024 (landscape), 1024x1536 (portrait), auto
    quality="high",           # low | medium | high | auto
    background="transparent", # transparent | opaque | auto  (transparent -> PNG alpha)
    output_format="png",      # png | jpeg | webp
    n=1,
)
b64 = result.data[0].b64_json  # GPT image models ALWAYS return base64 (no url)
```

- gpt-image-1 returns **base64** in `data[i].b64_json` — decode with `base64.b64decode` and write bytes.
- `background="transparent"` requires `output_format` png or webp; ideal for icons, decals, UI marks.
- Supported sizes: `1024x1024`, `1536x1024`, `1024x1536`, `auto` (256/512 are dall-e-2 only).

## Editing (image-to-image)

```python
result = client.images.edit(
    model="gpt-image-1",
    image=open("ref.png", "rb"),   # up to 16 reference images for GPT image models
    prompt="...",
    mask=open("mask.png", "rb"),   # optional; transparent areas mark where to edit (1st image)
    input_fidelity="high",         # high | low — how closely to match the references
    size="1024x1024",
    quality="high",
)
```

- `mask` must be a PNG the same dimensions as the (first) image; fully transparent pixels mark editable areas.
- Use `input_fidelity="high"` to preserve the look of the reference (faces, logos, established style).

## Model variants

- `gpt-image-1` (default here). Override with `--model` for `gpt-image-1-mini` (faster/cheaper) or
  newer GPT image models as they become available.

## Three.js consumption

- Albedo/texture maps: `texture.colorSpace = THREE.SRGBColorSpace`. Data maps (normal/roughness): linear.
- Transparent PNGs: `new THREE.MeshBasicMaterial({ map, transparent: true })` for decals/UI sprites.
- Orthographic/concept sheets feed `threejs-3d-generator` image-to-3D.
