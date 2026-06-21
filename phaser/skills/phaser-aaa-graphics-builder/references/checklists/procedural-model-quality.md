# Procedural Sprite/Graphics Quality Checklist

- The sprite has a recognizable silhouette from the gameplay camera.
- Primary forms read clearly before palette, tint, or postFX detail.
- Secondary detail supports the asset role: panels, trims, ridges, fins, sockets, decals, or additive emissive accents.
- Tertiary detail is visible at intended gameplay distance and does not create noise.
- Palette has purposeful value contrast via ramps, blend modes, tint, or accent color.
- Faux-bevels (offset light/dark strokes), arcs, and polygon silhouettes improve readability and form.
- Repeated props use shared atlas frames / baked textures (generateTexture), tinting, tiling, or pools when practical.
- Static composite art is baked to a single texture to reduce draw calls where it makes sense.
- Visual art and Arcade collision body are intentionally separated (body sized/offset, not the full sprite).
- The factory returns named containers/sprites with clear ownership/disposal and body-size metadata.
- Renderer diagnostics are checked when active objects, unique textures, or draw calls increase.
- Animation has juice where appropriate (squash & stretch, flash, anim frames), not a static stiff pose.
- Mobile screenshot still shows the asset as more than a primitive placeholder.
