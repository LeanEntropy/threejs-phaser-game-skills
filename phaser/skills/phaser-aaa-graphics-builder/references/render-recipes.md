# Render, Pipeline, Lighting, VFX, And Juice Recipes

Use this after authored forms exist. Rendering polish cannot compensate for missing sprites, props, or readable gameplay silhouettes.

## Renderer Setup

- Use `type: Phaser.AUTO` (prefers WebGL). PostFX, custom pipelines, and Lights2D require WebGL; design a graceful fallback for Canvas.
- Choose `backgroundColor` for the art direction, but never rely on a flat fill as the whole look — add parallax.
- For pixel art: `render: { pixelArt: true }` (disables antialias) and set textures to NEAREST filtering. For smooth art, leave antialias on and use linear filtering.
- Cap effective resolution on mobile through the `scale` config (`Phaser.Scale.FIT` + a sane base width/height). Profile before raising it.
- Use `roundPixels: true` to avoid sub-pixel shimmer when the camera/sprites move.
- Update layout, camera bounds/zoom, and UI on `this.scale.on('resize', ...)`.

## Camera Composition

- Keep the next decision visible. The camera should show player, immediate threat/reward, and route.
- Add depth via parallax layers: foreground speed elements, playable midground, background scale cues.
- Use `setZoom` and follow lerp (`startFollow(target, true, 0.1, 0.1)`) to communicate speed without hiding hazards.
- Use camera shake sparingly and clamp intensity: `this.cameras.main.shake(120, 0.004)`.
- Add camera impulses for hits/near misses/boosts (`shake`, brief `flash`, small zoom punch), then ease back quickly.
- Check mobile framing separately; vertical and narrow layouts often need different offsets, zoom, or `setBounds`.
- Use a deadzone (`camera.setDeadzone(w, h)`) to keep the player stable while the world parallaxes.

## Parallax And Depth (the 2D "world/sky")

Build the background as scrolling layers instead of a flat sky color:

- Far: a sky gradient texture plus a skyline/terrain silhouette `TileSprite`, scroll factor ~0.1-0.3, or driven manually: `far.tilePositionX = cam.scrollX * 0.2`.
- Mid: buildings/cliffs/clouds `TileSprite`s at 0.4-0.7.
- Play: ground/lanes at scroll factor 1.
- Near: foreground occluders/speed props above 1 for overtaking parallax.
- Drive each layer in `update`: `layer.tilePositionX = this.cameras.main.scrollX * layer.parallax;`
- Keep hazards/rewards readable against the parallax values; avoid backgrounds that swallow dark objects.

## Lighting Stack (Lights2D + faked light)

Phaser 2D lighting is either Lights2D or faked with sprites/gradients. Use a small, readable stack:

- Ambient: `this.lights.enable().setAmbientColor(0x202030)` sets the base mood.
- Key light: `this.lights.addLight(x, y, radius).setColor(0xffffff).setIntensity(2)`; sprites need a normal map and `setPipeline('Light2D')` for real shading.
- Fill: a second, dimmer, cooler light to keep gameplay objects legible.
- Rim/back separation: a bright additive accent sprite behind hero/hazards to lift them off the background.
- Practical/emissive: authored beacons, engines, pickups as `ADD`-blend sprites or postFX-glow targets.
- Contact: a dark, soft contact-shadow ellipse under important objects.

When Lights2D normal maps are not worth the cost, fake light with baked gradient textures, additive highlight sprites, and palette ramps. Avoid many full-scene additive overlays (overdraw).

## Shadows And Contact

- Add a cheap contact-shadow ellipse (dark, low-alpha, `MULTIPLY` or normal) under hero/hovering objects and major hazards.
- For drop shadows on hero/key sprites, use `sprite.preFX.addShadow(x, y, decay, power, color, samples, intensity)` sparingly.
- Scale shadow alpha/size with jump height for grounded platformer feel.
- Do not let shadows hide collision reads.

## Materials (palette + blend modes)

Phaser has no PBR. Express material through palette ramps, blend modes, tint, and alpha:

- Prefer value contrast before postFX: dark matte body vs bright trim vs additive emissive accent.
- Blend modes: `NORMAL` default; `ADD` for glow/energy/fire/light; `MULTIPLY` for shadow/grime; `SCREEN` for soft highlights/glass.
- Use tint (`setTint`, `setTintFill`) for variants, damage flash, and team colors instead of new textures.
- Match palette roles across UI and world: danger, reward, shield, boost, objective.

## PostFX And Custom Pipelines

Use postFX as a finishing pass:

- Bloom: `this.cameras.main.postFX.addBloom(0xffffff, 1, 1, strength, steps)` — tune to lift only authored emissive elements, not the whole frame.
- Glow: `sprite.postFX.addGlow(0x66ccff, outerStrength)` on hero/emissive/reward, not everywhere.
- Vignette: `this.cameras.main.postFX.addVignette(0.5, 0.5, radius, strength)` — subtle focus, never heavy darkness.
- Color grade: `this.cameras.main.postFX.addColorMatrix().brightness/contrast/saturate/hue(...)` for a cohesive look.
- Custom signature look: subclass `Phaser.Renderer.WebGL.Pipelines.PostFXPipeline` with a fragment shader (CRT, scanlines, heat haze, chromatic aberration on impact). Register: `this.game.renderer.pipelines.addPostPipeline('CRT', CRTPipeline)`; apply: `this.cameras.main.setPostPipeline('CRT')`; access for uniform updates via `getPostPipeline`.
- Chromatic aberration / shake distortion: brief, event-driven only.

Always compare screenshots with postFX enabled/disabled and watch the draw-call/overdraw cost (postFX adds render passes).

## Background, Sky, And Depth

- A sky should be a gradient texture or parallax plate, not a single flat color when the world needs scale.
- Layer background silhouettes at varied scales and heights.
- Add slow-moving far layers for motion-heavy games.
- Keep hazards/rewards readable against background values.

## Event-Driven VFX (Phaser 3.60+ particles)

Tie effects to state. Use `this.add.particles(x, y, 'texture', config)`:

- Boost: trail emitter (`blendMode: 'ADD'`), lane streak TileSprite speedup, camera zoom punch, side streaks, audio pitch.
- Pickup: `emitter.explode(n, x, y)` shard burst, ring snap (tween scale + alpha), score line to HUD, short glow pulse.
- Hit: impact ring, debris emitter, damage flash, hit-stop, camera shake.
- Near miss/combo: edge spark emitter, badge pulse, streak counter animation.
- Shield: additive shell sprite, rim glow postFX pulse, absorbed-impact ripple.
- Spawn/despawn: anticipation pulse, telegraph, scale-snap or alpha dissolve.

Pool emitters and reuse particle textures (one small baked spark/dot texture, tinted per use). Permanent particle fields should be cheap, sparse, and short-lived.

## Juice (game feel)

Juice is mandatory for a premium 2D feel. Centralize in a `JuiceSystem`:

- Squash & stretch: `this.tweens.add({ targets, scaleX: 1.25, scaleY: 0.8, yoyo: true, duration: 90, ease: 'Quad.out' })` on jump, land, hit, and pickup. Stretch along motion, squash on impact.
- Screen shake: `this.cameras.main.shake(duration, intensity)` scaled by event weight; clamp so it never hides gameplay.
- Hit-stop: drop `this.time.timeScale` (and optionally `this.physics.world.timeScale`) to a small value for a few real-time milliseconds on big hits, then restore with `this.time.delayedCall` (delayedCall uses real time, so it still fires).
- Flash/tint: `sprite.setTintFill(0xffffff)` then `clearTint()` after ~60ms; or `this.cameras.main.flash(120, r, g, b)` for global impacts.
- Trails: short follow emitter, or fading after-images (clone sprite, tween alpha to 0, destroy).
- Knockback/recoil: brief velocity impulse + position tween, eased back fast.

Juice must clarify and reward action, never obscure collisions or readability.

## Readability Checks

During active play, confirm:

- Player orientation is clear.
- Threats differ from rewards by both shape and palette.
- Important pickups are visible before reaction time expires.
- UI feedback does not cover the play path.
- VFX/juice clarifies state instead of obscuring collisions.
- Background/parallax contrast does not swallow dark objects.
- Hit-stop and shake durations stay short enough to keep control responsive.

## Performance Checks

After render/FX changes, report:

- FPS / frame time (`this.game.loop.actualFps`).
- Draw calls (batches) and how many unique textures break batching.
- Active game objects, active particle emitters, total live particles.
- Active tweens and timers.
- PostFX passes in use and their cost (each adds a full-frame pass).
- Overdraw from large additive/alpha sprites (glow, fog, trails).
- Texture/atlas count and approximate memory; mobile resolution cap and NEAREST/pixelArt notes.

If performance drops, reduce postFX passes and overdraw first, then cull/pool/tile, then merge textures into atlases, then reduce asset density only where it is least visible.
