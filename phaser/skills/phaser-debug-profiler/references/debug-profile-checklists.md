# Debug And Profile Checklists

Use this for blank/black canvases, bad framing, runtime errors, asset/audio loading issues, animation/tween/collision/input failures, Scale Manager/resize bugs, scene-lifecycle leaks, mobile/touch bugs, and performance optimization.

## Triage Order

1. Reproduce locally with the same command and URL the user used when possible.
2. Capture console, page, and network errors, plus any `this.load.on('loaderror')` payloads.
3. Confirm the app is serving the expected build, not another local server on the same port.
4. Identify the owner: game/renderer, scene lifecycle, camera, update loop, loader/assets, audio, input/touch, physics (Arcade/Matter), display list/depth, Scale Manager/CSS, build/base path, or performance.
5. Fix the root cause in the owning module/scene.
6. Retest the exact broken path.

## Blank Or Black Canvas

Check in this order:

- Canvas exists in the DOM and is inside the configured `scale.parent` element.
- Canvas CSS size is nonzero and visible; the parent element has layout (not `display:none`/zero height).
- `game.renderer` was created (`game.renderer.type` is WEBGL or CANVAS, not null). A null/failed WebGL context falls back to Canvas; if neither, the game never booted.
- Exactly one `Phaser.Game` instance exists (no double-`new Phaser.Game` from HMR or a stray import).
- The intended scene actually started: it is in the config `scene` array or was started via `this.scene.start('Play')`; `scene.isActive('Play')` is true and `create()` ran.
- No exception was thrown inside `preload`/`create` that aborted the scene before anything was added.
- Game objects were added to the display list (`this.add.*` / `this.physics.add.*`), not just constructed.
- Texture key exists: the key passed to `this.add.sprite(x, y, 'key')` is loaded (`this.textures.exists('key')`); a missing key shows the green/black `__MISSING` placeholder or nothing.
- Camera shows the content: `cameras.main` scroll/bounds include the objects, `setZoom` is not 0 or tiny, camera is visible and not faded/blacked out by a leftover `fade`/`flash`.
- Objects are visible: `setVisible(true)`, `alpha > 0`, `scale != 0`, depth not buried under a full-screen rectangle, tint not 0x000000 on a needed sprite, blend mode not erasing.
- `scene.children.length` is nonzero (the scene actually holds objects).
- Background color is not identical to the only objects (e.g. black sprites on `backgroundColor: '#000000'`).
- Scale Manager updated on resize: mode (`FIT`/`RESIZE`/`ENVELOP`) is intentional and the canvas is not collapsed to 0 width/height.
- DOM/HTML overlays or a UI Scene rectangle are not covering the game canvas.
- Render texture / camera postFX output is actually displayed and not rendering to an unused target.

## Asset Loading

Check:

- Keys and URLs, and the Vite base path (`import.meta.env.BASE_URL`) for hosted builds.
- Files are in `public/` (served at root) or imported with a bundler-resolved URL.
- Correct loader for the asset: `this.load.image`, `spritesheet` (with `frameWidth`/`frameHeight`), `atlas` (PNG + JSON), `bitmapFont` (PNG + XML), `tilemapTiledJSON`, `audio`.
- A `this.load.on('loaderror', (file) => ...)` handler exists so failures are visible, not silent.
- CORS and MIME type errors on cross-origin assets.
- Atlas/tilemap JSON matches the texture (frame names, atlas format Hash vs Array, tileset name in Tiled JSON matches `addTilesetImage`).
- Spritesheet `frameWidth`/`frameHeight`/`margin`/`spacing` exactly match the sheet, or frames will be misaligned.
- `create()` does not use a key before its load completed (build keyed objects in `create`, not in `preload`).
- Texture memory and dimensions are reasonable (very large PNGs can exceed mobile GPU texture limits, often 4096px).
- Old textures are removed when swapped (`this.textures.remove(key)`), and groups/objects from a previous run are destroyed.

For generated/sliced sprite and atlas assets, also check file size, URL casing, Vite `public/`/import path, sheet slicing alignment (frame count and order), transparent-background preservation, atlas JSON frame names referenced by `play`/`setFrame`, animation key names, and whether generated download URLs were saved before expiring.

## Audio Loading And Playback

Check:

- Audio files exist at runtime URLs and have compatible formats (ship both `.ogg` and `.mp3`).
- The Web Audio context is unlocked from a user gesture; Phaser auto-unlocks on first input, but confirm `this.sound.unlock()` / first pointer/key happened before playback.
- `this.load.on('loaderror')` surfaces decode/load failures instead of failing silently.
- SFX triggers are event-driven and not fired every `update()` frame.
- Ambience/music loops stop on pause, restart, and scene `shutdown` (`sound.stop()` / track destroy).
- Mute/volume state controls every sound (`this.sound.mute`, per-sound volume).
- Page visibility/blur pause-resume does not stack duplicate sound instances.
- Mobile browser unlock behavior is tested when mobile is in scope.
- Audio sprites (`this.sound.addAudioSprite`) reference the correct marker names.

## Animation, Tweens, Loop, And Physics

Check:

- `update(time, delta)` uses `delta` in milliseconds; convert to seconds (`delta / 1000`) for unit-based movement, or prefer physics velocities.
- Frame-rate independence: movement scaled by delta, not assumed 60fps; Arcade velocity already integrates delta.
- Sprite animations created once (`this.anims.create`) with correct `generateFrameNumbers`/`generateFrameNames`, `frameRate`, and `repeat`; `sprite.play('key')` is called and not restarted every frame.
- Tweens have explicit `duration`/`ease`; tween targets still exist (a destroyed sprite as a tween target throws or no-ops).
- The correct physics engine is initialized in config (`physics.default: 'arcade'` or `'matter'`) before bodies are created.
- Arcade colliders/overlaps are registered (`this.physics.add.collider` / `overlap`) and bodies have bodies enabled (`setImmovable`, `setCollideWorldBounds`, world bounds set).
- Matter bodies use correct shapes/constraints and `setBounds` for the world when Matter is chosen.
- Body size/offset matches the visual sprite (`body.setSize`, `setOffset`); mismatched bodies cause phantom or missed collisions.
- High-speed tunneling and spawn overlap (use larger bodies, `setMaxVelocity`, or Matter for fast bodies).
- Overlaps/sensors have active callbacks or explicit `this.physics.overlap` checks.
- Kinematic/moving platforms update the physics body, not only the display position (`setVelocity` on a moving platform, or `moves = false` + manual body sync).
- Only one source advances the loop: no manual `requestAnimationFrame` competing with Phaser's loop; paused scenes (`this.scene.pause`) really stop `update`.
- State transitions (`this.scene.start`/`restart`) clean up entities, listeners, timers, tweens, and emitters (see Scene Lifecycle Leaks).

## Scene Lifecycle Leaks

Check on every `this.scene.start`, `restart`, `stop`, or `shutdown`:

- Timers stopped: `this.time` events are auto-cleared on shutdown, but `setInterval`/`setTimeout` or globals you created are not — clear them in a `SHUTDOWN` handler.
- Tweens: scene-owned tweens are killed on shutdown, but tweens on objects shared across scenes, or `this.tweens` referenced after destroy, leak — kill explicitly.
- Particle emitters/managers destroyed (`emitter.destroy()`), especially long-lived ambient emitters.
- Event listeners removed: `this.input.on`, `this.events.on`, `EventEmitter` subscriptions, and any DOM `window.addEventListener('resize'|'blur'|...)` you added — remove on `SHUTDOWN`.
- Global/registry listeners (`this.game.events.on`, `this.registry.events.on`, `this.scale.on('resize')`) are removed; these survive scene shutdown and accumulate per restart.
- Groups and pools cleared/destroyed so pooled objects do not pile up across restarts.
- Cached textures generated at runtime (`generateTexture`, RenderTexture) removed if regenerated each run.
- A `this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => { /* cleanup */ })` block exists for any manually-created resource.

## Input And Mobile Bugs

Check:

- Keyboard input guarded for null in strict TS (`this.input.keyboard!` or a guard); `JustDown`/`JustUp` used for single-fire actions.
- Pointer listeners on the correct target: `this.input.on('pointerdown'|'pointerup'|'pointermove')` vs per-object `sprite.setInteractive().on('pointerdown')`.
- `setInteractive()` called (with a correct hit area) before per-object pointer events fire; interactive objects re-added after scene restart.
- Pointer up/out/cancel handled so a held virtual control releases when the finger leaves it (`pointerout`, `pointerupoutside`).
- `touch-action: none` on the canvas/parent only where needed; viewport meta present.
- Page scroll/zoom gestures not stealing gameplay input (prevent default on the parent, or `touch-action`).
- Multi-touch enabled when needed (`this.input.addPointer(n)`); default is one active pointer beyond mouse.
- Scale Manager mode appropriate for device; canvas not tiny/huge after rotation; DPR/zoom not making controls unusable.
- Safe-area insets respected for HUD/controls (`env(safe-area-inset-*)` in CSS around the parent).
- Orientation/resize handled: `this.scale.on('resize', ...)` repositions HUD and recomputes layout.
- Desktop input still works after on-screen/touch controls are added.
- On-screen UI buttons emit game intents (events) and do not directly duplicate simulation rules.

## Performance Profiling Order

Measure in production preview when user-facing performance matters.

1. Establish scenario: viewport, Scale mode, zoom/DPR, scene, gameplay state, camera view, mobile/desktop.
2. Baseline:
   - `this.game.loop.actualFps` and frame time (`this.game.loop.delta`).
   - Draw calls (batches) — WebGL pipeline flushes; reduce by atlasing and consistent textures/blend modes.
   - Active game objects (`this.children.length`, group `countActive(true)`).
   - Physics body count (`this.physics.world.bodies.size` + `staticBodies.size` for Arcade; `this.matter.world.localWorld.bodies.length` for Matter).
   - Particle counts (alive particles per emitter) and active emitters.
   - Active tweens (`this.tweens.getTweens().length`) and active timers (`this.time` events).
   - Texture & atlas memory: count and dimensions of loaded textures (`this.textures.list`), large/duplicate atlases.
   - Bundle and large assets when relevant.
   - For physics-changed work: collider/overlap count, sensors, and step cost.
3. Classify bottleneck:
   - CPU: game logic, per-frame allocations, pathfinding, physics step, tween/timer churn, UI/text layout.
   - GPU draw: too many draw calls (batches) from mixed textures, blend-mode switches, many unique textures, Graphics redraws.
   - GPU fragment: overdraw from stacked transparent sprites, large particle clouds, full-screen postFX, big TileSprites, high zoom/DPR.
   - GPU vertex: rarely dominant in 2D, but huge TileSprite/Graphics meshes and many rope/mesh objects add up.
   - Memory: oversized textures, duplicate atlases, RenderTextures, undisposed runtime textures.
   - Network/bundle: large dependencies or assets.
4. Apply one optimization.
5. Re-measure the same scenario.
6. Check visual/playability regression.

## Preferred Optimizations

- Texture atlases so sprites batch into one draw call.
- Shared textures/atlases and consistent blend modes to avoid batch breaks.
- Object pools (Groups with `maxSize`) for bullets, effects, pickups, enemies, and debris instead of create/destroy churn.
- Culling: `setVisible(false)` or `setActive(false)` for off-screen objects; cap on-screen counts; use camera `cull` for tilemap layers.
- Cap zoom/DPR or use adaptive quality on low-end devices.
- Limit postFX/pipeline passes; reuse a single PostFXPipeline rather than many.
- Bound particle emitters: cap `quantity`, `maxParticles`, lifespan, and number of simultaneous emitters; prefer `explode` bursts over endless flows.
- Reduce physics cost: simpler Arcade AABB bodies, fewer dynamic bodies, body sleeping/disable when idle, collision via groups, pooled bodies, and narrower overlap checks before removing gameplay.
- Avoid per-frame allocations and object/array creation in `update`; reuse `Phaser.Math.Vector2` and `Phaser.Geom` instances.
- Redraw `Graphics` only when it changes; bake static Graphics to a texture with `generateTexture` once.
- Use `tileSprite`/parallax layers and tilemap culling instead of thousands of individual sprites.
- Destroy/remove textures, RenderTextures, emitters, tweens, timers, listeners, and audio on scene shutdown.
- Use `phaser-sprite-generator` to produce tighter atlases, fewer/smaller frames, lower-resolution variants, or merged sheets before deleting important hero readability.

## Diagnostics Snippet

When possible, expose a diagnostic object from the active scene:

```ts
// In a scene's create(), capture `this` as `scene`:
const scene = this;
window.__PHASER_GAME_DIAGNOSTICS__ = {
  get fps() { return scene.game.loop.actualFps; },
  get delta() { return scene.game.loop.delta; },
  get renderer() { return scene.game.renderer.type; }, // WEBGL or CANVAS
  get objects() { return scene.children.length; },
  get tweens() { return scene.tweens.getTweens().length; },
  get textures() { return Object.keys(scene.textures.list).length; },
  get arcadeBodies() {
    const w = scene.physics && scene.physics.world;
    return w ? w.bodies.size + w.staticBodies.size : null;
  },
};
```

Useful fields and accessors: `this.game.loop.actualFps`, `this.game.loop.delta`, `this.children.length`, `group.countActive(true)`, `this.tweens.getTweens().length`, `this.textures.list` (texture count/dimensions), `this.physics.world.bodies.size`, and `this.game.renderer.type` (WEBGL/CANVAS).

For physics-heavy games, also surface:

```ts
physics: {
  engine: 'arcade', // or 'matter'
  bodies: this.physics.world.bodies.size,
  staticBodies: this.physics.world.staticBodies.size,
  colliders: this.physics.world.colliders.length,
}
```

## Visual Physics Debug

Enable the Arcade debug graphic to see bodies, velocities, and blocked faces:

```ts
// Config
physics: { default: 'arcade', arcade: { debug: true } }
// Or toggle at runtime:
this.physics.world.drawDebug = true;
this.physics.world.createDebugGraphic(); // creates world.debugGraphic if missing
// Off:
this.physics.world.drawDebug = false;
this.physics.world.debugGraphic?.clear();
```

For Matter, use `matter: { debug: true }` in config to render bodies, constraints, and contacts.

## Bug Report Format

```text
Issue:
Reproduction:
Expected:
Actual:
Root cause:
Fix:
Verification:
Residual risk:
```

## Common Mistakes

- Guessing without reproducing.
- Optimizing dev-server performance instead of production preview.
- Removing visual detail before checking atlasing, batches, particle limits, pooling, postFX, or culling.
- Fixing symptoms in CSS when the Scale Manager mode/parent sizing or camera bounds are wrong.
- Adding touch controls without testing pointer out/cancel/up-outside and safe areas.
- Ignoring console/page errors or `loaderror` because the canvas appears nonblank.
- Forgetting scene-shutdown cleanup, so timers, tweens, emitters, and global/registry listeners leak across restarts.
- Using a texture key before its load completed, or assuming a missing key throws instead of showing the placeholder.
- Shipping a large atlas/spritesheet without checking texture dimensions, frame alignment, memory, or mobile GPU limits.
