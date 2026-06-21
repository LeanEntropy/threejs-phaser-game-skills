# Performance-Safe 2D Visual Detail Checklist

- Baseline renderer info (draw calls/batches, active objects, FPS) is captured when increasing fidelity.
- Draw calls (batches), active game objects, texture/atlas count, particle counts, tween counts, and frame time are reviewed after changes.
- Repeated details use shared atlas frames + tint, baked textures (generateTexture), TileSprite tiling, or pooled Groups instead of unique textures.
- Batch breaks are minimized: textures are packed into atlases so consecutive draws share one texture.
- Overdraw is controlled: large additive/alpha sprites (glow, fog, trails) are limited in count and size.
- Particle budgets are explicit: short-lived pooled bursts over permanent high-quantity fields.
- PostFX passes are justified by gameplay readability or strong art direction (each pass adds a full-frame render).
- Mobile resolution cap, pixelArt/NEAREST, and roundPixels are considered before removing detail.
- Generated textures and atlases have a disposal/reuse strategy (`this.textures.remove`, pooled emitters, group clearing).
- Off-screen props are pooled, `setVisible(false)`, or culled.
- The worst-case gameplay scene, not only idle view, is inspected.
- Visual detail remains readable at mobile resolution without excessive GPU cost (batches + overdraw).
