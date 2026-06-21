# AAA Graphics Implementation Blueprint

Use this when a Phaser 3 game reads as basic even after it is playable. The goal is a production 2D graphics architecture that can be iterated, scored, profiled, and reused.

## Recommended Ownership

```text
src/art/PaletteLibrary.ts
src/art/ProceduralTextures.ts        // Graphics + generateTexture() helpers
src/art/DecalShapes.ts
src/art/ArtDiagnostics.ts
src/art/AtlasRegistry.ts             // loaded spritesheets/atlases/tilesets + frame names
src/art/factories/HeroFactory.ts
src/art/factories/ObstacleFactory.ts
src/art/factories/RewardFactory.ts
src/art/factories/WorldPropKit.ts
src/systems/LightingRig.ts           // Lights2D + faked light sprites
src/systems/RenderPipeline.ts        // postFX/preFX, custom PostFXPipeline registration
src/systems/VfxSystem.ts             // particle emitters + juice helpers
src/systems/JuiceSystem.ts           // squash & stretch, shake, hit-stop, flash, trails
src/systems/WorldArtDirector.ts      // parallax layers
src/systems/QualityDiagnostics.ts
```

Keep these boundaries lightweight. In small projects, a single file can contain multiple factories, but the concepts must remain separate: palette, authored textures, sprite/Graphics art, repeated props, particle effects, juice, render/postFX settings, and diagnostics.

## Hybrid AI Asset Pipeline

Choose the asset path per surface:

- Procedural Phaser Graphics (`this.add.graphics()` + `generateTexture(key, w, h)`): repeated detail, simple props, tiles, decals, collision proxies, particle textures, debug-friendly shapes, palette ramps.
- `phaser-image-generator`: concept sheets, character turnaround references, texture/tileset references, trim sheets, decals, icons, logos, skies, parallax background plates, UI art.
- `phaser-sprite-generator`: hero/player, characters, creatures, vehicles, buildings, weapons, signature props, pickups, bosses, full spritesheets (uniform frames), texture atlases (JSON), and tilesets.
- Hybrid: image-generator concept/reference -> sprite-generator spritesheet/atlas slice+pack -> Phaser load -> procedural collision/particle/prop kit -> visual scorecard.

For premium/AAA/showcase/high-fidelity/less-basic games, do not decide `phaser-sprite-generator` or `phaser-image-generator` is unnecessary before loading the relevant skill when the game includes characters, creatures, vehicles, ships, weapons, buildings, signature props, hero pickups, skies, tilesets, decals, logos, icons, or GUI art. Load first, run the credential probe, then document the tradeoff.

Use `phaser-sprite-generator` when generated sprite/atlas fidelity will materially improve the active screenshot. Do not generate a unique sheet for every repeated small prop; use shared atlases, tinting, and Graphics-baked textures for volume.

For premium hero surfaces, procedural-only is not a valid final choice unless a real blocker is recorded: missing key from the credential probe, API/network/quota error after an attempted command, user requested no external assets, or offline-only constraint. Repeated low-value props can stay procedural.

Asset sourcing ledger:

```text
External asset sourcing:
- Credential probe output:
- Hero/player:
- Enemies/vehicles/weapons:
- Signature props/pickups:
- World/sky/parallax background:
- Palette/textures/tilesets/decals:
- Logos/icons/GUI art:
- Chosen sources per surface: procedural / phaser-image-generator / phaser-sprite-generator / hybrid
- External assets generated: yes/no, output paths (sheet+JSON / image) or allowed skip reason:
```

## Production Surfaces

A premium pass must touch every weak visible surface:

- Hero/player: authored silhouette, state feedback, palette ramp/trim, readable from gameplay distance, animation frames, collision proxy (Arcade body size/offset).
- Hazards/enemies: at least three distinct silhouettes with telegraphs and palette cues.
- Rewards/interactables: at least two forms with collection states and VFX/juice hooks.
- World kit: parallax background, midground props, playable lane/arena, foreground occluders used carefully, set dressing, scale cues.
- Palette/textures: shared palette role library, procedural panel-line/noise/trim textures via Graphics, normal maps for Lights2D where used, emissive/additive accent sprites.
- Lighting/postFX: ambient color, Lights2D or faked light, contact shadow, parallax depth, postFX discipline (bloom/glow/vignette).
- Particle VFX/juice/motion: event-driven emitter bursts, trails, impact rings, speed lines, shield/boost states, pickup/fail feedback, squash & stretch, screen shake, hit-stop, flash/tint.
- UI/world cohesion: UI colors, icons, alerts, and meters echo gameplay palette and status colors; UI runs in a parallel Scene.
- Diagnostics: draw calls (batches), active game-object counts, texture/atlas count and memory, particle/tween counts, screenshots, scorecard.

For imported generated sprite assets, also require the downloaded spritesheet/atlas + JSON, load wrappers with frame keys and anim definitions, simple collision body sizing, and frame-count/atlas-size/file-size diagnostics.

## Palette And Material Library

Create named palette/material roles instead of one-off colors. Each role is a base color plus a small ramp (shadow / mid / highlight) and a blend/tint intent:

- `bodyPrimary`: dominant player/world shell.
- `bodySecondary`: panel/accent contrast.
- `trim`: edges, borders, rim highlights.
- `hazard`: danger surfaces, damage cues, warning stripes.
- `reward`: collectible surfaces with readable value.
- `glass`: cockpit, shield, lens (semi-transparent + additive highlight).
- `emissiveSignal`: authored glow strips, status lights, beacon cores (rendered as `ADD` blend sprites or postFX glow targets).
- `groundContact`: dark contact shadow ellipses under important objects.
- `decalDark` and `decalLight`: panel lines, scratches, numbers, icons.

Phaser has no PBR materials. Express "material" through palette ramps, blend modes (`NORMAL`, `ADD`, `MULTIPLY`, `SCREEN`), tint, alpha, and optional Lights2D with normal maps. Share textures/atlas frames across repeated objects and tint per-instance rather than baking unique textures.

## Procedural Texture And Decal Kit

Use `this.add.graphics()` drawn into an offscreen texture with `generateTexture(key, w, h)`, plus `TileSprite`, for detail that would otherwise require external assets:

- Panel lines and access hatches.
- Trim sheets and edge bands.
- Window strips, city light grids, arena markings.
- Hazard stripes, arrows, target indicators, lane glyphs.
- Scratches, wear, noise, dirt, scorch marks (low-alpha overlay textures).
- UI/world icon motifs reused in HUD and diegetic markers.
- Palette ramps and gradient swatches baked once and reused.

Set texture filtering intentionally: `this.textures.get(key).setFilter(Phaser.Textures.FilterMode.NEAREST)` for crisp pixel art, linear for smooth art. Avoid generating unique full-size textures for tiny repeated marks; bake once, reuse the key, tint per instance.

Use `phaser-image-generator` for high-value 2D source art: terrain/rock/grass/snow texture references, sci-fi trim sheets, signs, hazard stripes, decals, sky/parallax plates, menu/loading art, faction logos, pickup icons, ability icons, and GUI glyphs. Use the resulting images either as actual 2D assets/tilesets or as references for `phaser-sprite-generator`.

## Sprite/Graphics Factories

Factories should return a structured object plus metadata. Build art as a `Container` of child Graphics/Sprites, or bake a single texture and return a Sprite:

```ts
type ArtFactoryResult = {
  root: Phaser.GameObjects.Container | Phaser.GameObjects.Sprite;
  textureKey?: string;            // when baked via generateTexture
  bodySize?: { w: number; h: number; ox: number; oy: number }; // Arcade collision proxy
  diagnostics?: {
    children: number;             // container child count
    textures: number;             // unique texture keys touched
    frames?: number;              // anim frames if a sheet
  };
};
```

Use named children for readable debugging (`container.getByName('cockpitGlass')`). Separate visual detail from the Arcade collision body (`sprite.body.setSize(w, h).setOffset(ox, oy)`). Bake static composites to a single texture with `generateTexture` to reduce draw calls.

For imported generated sprites, create an `AtlasRegistry` or loader wrapper that returns similar metadata: texture key, frame names, anim keys, body size, and diagnostics. Never put image/sprite/audio generation API calls in browser runtime code.

## World Art Director (Parallax)

Build the world as parallax layers, far to near, using `TileSprite` and `setScrollFactor`:

- Far layer: sky gradient, skyline/terrain silhouette, nebula/cloud cards. Low scroll factor (0.1-0.3) or `tilePositionX += camera.scrollX * k`.
- Mid layer: buildings, cliffs, hangars, pillars, platforms. Scroll factor 0.4-0.7.
- Play layer: ground, lanes, rails, objective path, hazards, pickups. Scroll factor 1.
- Near layer: speed props, signs, arches, foreground occluders. Scroll factor > 1 for overtaking parallax.
- Motion layer: speed lines, particles, trails, dust, sparks, screen-space UI feedback (UI Scene, scroll factor 0).

Every layer should support gameplay readability. Do not obscure threats or the next decision. Drive parallax in `update` via `tileSprite.tilePositionX = this.cameras.main.scrollX * factor`.

## Render / PostFX Pipeline

Own renderer/FX setup in one place:

- `type: Phaser.AUTO` (prefers WebGL; postFX/Lights2D need WebGL — degrade gracefully on Canvas).
- Choose a `backgroundColor` that supports the art direction; do not rely on a flat fill as the whole look.
- Cap effective resolution on mobile via `scale` config and `render: { pixelArt: true }` for crisp pixel art (also disables antialias).
- Camera FX: `this.cameras.main.postFX.addBloom(...)`, `.addVignette(...)`, `.addColorMatrix()` for grading; use sparingly.
- GameObject FX: `sprite.postFX.addGlow(color, outerStrength)` and `sprite.preFX.addShadow(...)` only on authored emissive/hero elements.
- Custom `Phaser.Renderer.WebGL.Pipelines.PostFXPipeline` subclass for signature looks (CRT, heat haze, chromatic on impact). Register with `game.renderer.pipelines.addPostPipeline('Name', NameClass)` and apply via `camera.setPostPipeline('Name')`.
- Resize handling: `this.scale.on('resize', ...)`, reposition UI, keep camera bounds/zoom correct.

## VFX + Juice System

Effects should be event-driven, pooled, and readable. Use the Phaser 3.60+ particle API and juice helpers:

- Pickup: emitter `explode()` shard burst, ring contraction (tween scale up + alpha out), score trail, brief HUD echo.
- Hit/fail: impact flash (white tint for ~60ms then clear), debris emitter, camera `shake`, hit-stop via `this.time.timeScale = 0.05` for a few frames then restore, brief slow.
- Boost/speed: trail emitter (`ADD` blend), lane streak TileSprite speedup, camera slight zoom, audio pitch.
- Near miss/combo: side spark emitter, badge pulse tween, streak counter animation.
- Shield/invulnerable: rim glow postFX, pulse tween, additive shell sprite, absorbed-impact ripple.
- Spawn/despawn: anticipation pulse, telegraph, scale-snap or alpha dissolve.

Juice helpers to centralize in `JuiceSystem`:

- Squash & stretch: `this.tweens.add({ targets, scaleX: 1.2, scaleY: 0.8, yoyo: true, duration: 90, ease: 'Quad.out' })` on jump/land/hit.
- Screen shake: `this.cameras.main.shake(duration, intensity)` (clamp intensity, scale by event weight).
- Hit-stop: set `this.time.timeScale` (and/or `this.physics.world.timeScale`) low, restore with a `delayedCall` measured in real time.
- Flash/tint: `sprite.setTintFill(0xffffff)` then `clearTint()`; or `this.cameras.main.flash(120, r, g, b)` for global hits.
- Trails: low-quantity follow emitter, or a fading after-image via repeated faded copies.

Avoid permanent particle clutter. Effects and juice must clarify state, never hide collisions.

## Diagnostics

Expose or log:

- Draw calls / batches (`game.renderer` draw count) and frame rate (`this.game.loop.actualFps`).
- Active game-object count, active physics body count, active tweens, active particle emitters and particle counts.
- Texture/atlas count and approximate texture memory; unique texture keys in use.
- Approximate visible prop counts by parallax layer.
- Screenshot paths and visual scorecard.
- Performance notes after postFX, Lights2D, or many repeated props/particles.

## Browser Game Budgets

Budgets vary by game and device, but start with explicit targets:

- Keep draw calls (batches) low by sharing atlases and tinting instead of unique textures, and by baking static composites with `generateTexture`.
- Prefer atlas frames + tint over many unique texture keys (each unique texture can break batching).
- Cap particle budgets: prefer short-lived bursts and pooled emitters over permanent high-quantity fields.
- Watch overdraw: large additive/alpha sprites stacked (glow, fog, trails) are the main 2D cost; limit count and size.
- Cap mobile resolution and use `pixelArt`/NEAREST before removing all detail.
- Use object pooling (Groups) and `setVisible(false)`/culling for off-screen props.
- Measure after every major graphics pass.

## Implementation Order

1. Score active screenshots and identify the weakest three categories.
2. Add palette and diagnostic foundations.
3. Decide which weak surfaces need procedural, `phaser-image-generator`, `phaser-sprite-generator`, or hybrid treatment.
4. Build/import hero/player and one complete obstacle/reward family with anims.
5. Add world parallax prop kit and layered composition.
6. Add palette/Lights2D/blend and postFX polish.
7. Add event-driven particle VFX and juice (squash & stretch, shake, hit-stop, flash, trails).
8. Re-score desktop/mobile active screenshots.
9. Optimize measured bottlenecks (batches, overdraw, particle/texture budgets).
