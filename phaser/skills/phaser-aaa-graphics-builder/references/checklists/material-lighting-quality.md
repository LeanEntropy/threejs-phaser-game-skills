# Palette and Lighting Quality Checklist

- Renderer config is intentional: pixelArt/antialias, NEAREST vs linear filtering, roundPixels, and mobile resolution cap.
- A controlled master palette with per-role ramps (shadow/mid/highlight/accent) is reused across sprites for cohesion.
- Lighting clarifies depth and gameplay roles via Lights2D (ambient/key/fill/rim with normal maps) or faked light (gradients/additive sprites).
- Sprites avoid flat default looks through palette-ramp value contrast, blend modes (ADD/MULTIPLY/SCREEN), tint, and emissive accents.
- Important objects have readable silhouettes against background, parallax, and effects.
- Contact-shadow ellipses or preFX shadows ground assets without obscuring navigation or collision boundaries.
- Parallax, bloom, glow, particles, vignette, and postFX support readability instead of hiding it; additive overdraw is controlled.
- Procedural (generateTexture) textures and decals are scaled, stable, and not visually noisy during movement.
- Textures/atlas frames are reused (shared keys + tint) where possible and removed when obsolete (`this.textures.remove`).
- Desktop and mobile screenshots are checked after lighting/palette changes.
- Draw-call/batch counts, active-object counts, or frame-time evidence is gathered when render cost changes.
