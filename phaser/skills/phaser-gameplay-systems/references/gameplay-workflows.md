# Gameplay Workflows

Use this reference for first playable slices, scene architecture, mechanics, entities, controls, camera, physics, audio hooks, and game-feel iteration.

## First Playable Slice

The first slice must be playable, not just rendered.

1. Inspect folder, scripts, dependencies, current scenes, game config, entrypoint, CSS, assets, and tests.
2. Define the loop in one sentence: verb, objective, pressure, reward, fail/retry.
3. Implement only the mechanics needed for that loop:
   - `Phaser.Game` config and a `Play` scene
   - camera and Scale Manager (`Phaser.Scale.FIT`, world bounds)
   - `update(time, delta)` loop
   - input intents
   - player entity (sprite + body)
   - one obstacle/enemy or challenge
   - one reward/progress path
   - collision/overlap checks
   - score/status state
   - fail/retry state (scene `restart`)
   - minimal HUD (a parallel UI scene)
   - one audio/VFX feedback hook
4. Add diagnostics when possible:
   - `window.__PHASER_GAME_DIAGNOSTICS__`
   - `this.game.loop.actualFps`
   - game state snapshot
   - input state
   - active game object / group counts
5. Verify build, browser, console/page errors, screenshot, nonblank canvas, and one real input path.

Reject a slice that cannot be controlled or restarted.

## Architecture Boundaries

Prefer simple modules once the prototype grows beyond one file:

- `main`: DOM bootstrap, `Phaser.Game` config, CSS imports.
- `scenes`: `Boot` (config/scale), `Preload` (asset loading + loading bar), `Play` (gameplay), `UI` (HUD/menus run in parallel via `this.scene.launch('UI')`).
- `game`: orchestration, state transitions, update order, scoring/objectives (often a registry or a small store).
- `entities`: player, enemies, pickups, projectiles, obstacles (extend `Phaser.GameObjects.Sprite` or `Physics.Arcade.Sprite`).
- `systems`: camera, collision/physics setup, spawning, animation, audio, UI bridge, debug.
- `assets`: texture/atlas/tilemap keys, procedural `generateTexture` factories, loaders, palette.
- `tests`: browser, visual, interaction, mobile, performance smoke checks.

Keep update order explicit:

```text
input -> physics step (Arcade/Matter) -> gameplay systems -> animation/tweens/VFX -> camera -> UI bridge -> render
```

Do not invent abstractions before the mechanics need them. Do extract duplicated entity, input, collision, and asset logic once multiple features share it.

## Scenes, Groups, And Pooling

Phaser organizes a game into scenes and a per-scene display list.

- Split startup into `Boot` (scale/input config), `Preload` (all `this.load.*` + a progress bar via `this.load.on('progress', ...)`), and `Play`.
- Run the HUD as a separate scene: `this.scene.launch('UI')` so the camera scroll never moves HUD text; HUD text uses `.setScrollFactor(0)`.
- Use Groups for collections that share behavior: `this.physics.add.group()`, `staticGroup()`, or a plain `this.add.group()`.
- Pool frequently spawned objects (bullets, particles, enemies) with a capped group and reuse instead of create/destroy:

```ts
const bullets = this.physics.add.group({ defaultKey: 'bullet', maxSize: 64 });
function fire(x: number, y: number) {
  const b = bullets.get(x, y) as Phaser.Physics.Arcade.Image | null;
  if (!b) return;                       // pool exhausted
  b.setActive(true).setVisible(true);
  (b.body as Phaser.Physics.Arcade.Body).enable = true;
  b.setVelocityY(-600);
}
// recycle on leave/hit:
function kill(b: Phaser.Physics.Arcade.Image) {
  b.setActive(false).setVisible(false);
  (b.body as Phaser.Physics.Arcade.Body).enable = false;
}
```

## Sprites, Atlases, And Animations

When gameplay uses `phaser-sprite-generator` spritesheets/atlases/tilesets:

- Load uniform sheets with `this.load.spritesheet(key, url, { frameWidth, frameHeight })`.
- Load packed atlases with `this.load.atlas(key, png, json)` (TexturePacker JSON Hash/Array).
- Keep asset loading in the `Preload` scene, not inside entity update loops.
- Wrap textures in entity classes with explicit body size/offset (`setSize`, `setOffset`), origin, depth, and state hooks.
- Build animations once in `create` and map gameplay states to anim keys:

```ts
this.anims.create({
  key: 'run',
  frames: this.anims.generateFrameNumbers('hero', { start: 0, end: 7 }),
  frameRate: 12,
  repeat: -1,
});
player.play('run');
```

- Map states to clips: idle, walk/run, jump, fall, attack/shoot, hurt, die, turn.
- For arcade games, prefer in-place animation and move the entity in code (no root motion).
- Keep collision bodies simple and independent from the visible frame.
- Add fallback placeholder textures (`graphics.generateTexture`) if an asset fails to load.
- Report sheet/atlas key, frame count, frame size, and texture/atlas memory after import.

## Input And Intent

- Convert keyboard, pointer, and touch (and gamepad where relevant) into game intents.
- Keyboard: `this.input.keyboard!.createCursorKeys()` and `addKeys('W,A,S,D')`; use `Phaser.Input.Keyboard.JustDown(key)` for one-shot actions.
- Pointer/touch: `this.input.on('pointerdown', p => ...)`; pointer events already cover touch.
- Keep input collection separate from simulation; read intents in `update`, apply to bodies.
- Support both desktop and mobile when the user asks for a browser game unless explicitly desktop-only; add on-screen buttons via the UI scene for touch.
- Handle pointer up/out and scene blur/pause so controls do not stick.
- Keep CSS `touch-action: none` on the canvas parent and respect safe areas with `env(safe-area-inset-*)`.
- Preserve focus and restart controls after fail/pause.

## Camera And Controls

Tune controls and camera together.

- Movement: acceleration, drag/friction, turn rate, max speed, jump velocity/gravity/boost.
- Camera: `startFollow(target, true, lerpX, lerpY)`, `setBounds`, `setZoom`, deadzone (`setDeadzone`), look-ahead via follow offset.
- Readability: next decision visible, player framed, threats not hidden by HUD.
- Feedback: hit pause (brief `this.physics.world.pause()` or timescale), `camera.shake`, `camera.flash`, `camera.fade`, zoom punch, meter pulse, audio pitch, particle burst.
- Accessibility: avoid excessive shake/strobe; gate camera shake behind a reduced-motion setting.

Add a debug GUI or key-toggled overlay for live constants when repeated tuning is likely, but gate debug UI from release.

## Collision And Physics

Choose the lightest reliable approach:

- Simple custom checks: arcade triggers, lanes, runners, pickups, bullets, distance/`Phaser.Geom.Intersects` tests.
- Arcade Physics: default robust choice for platformers, top-down, shooters, runners, breakout, tilemap collision, sensors via `overlap`, and high body counts.
- Matter.js: when rotation, slopes, joints, stacking, or compound/polygon bodies are required.

When physics is in scope, also load `references/physics-engine-selection.md` before choosing an engine.

Rules:

- Keep collision bodies simple and visible via `arcade.debug=true` / `this.physics.world.drawDebug`.
- Do not collide against raw frame pixels; use `setSize`/`setOffset` bodies.
- Arcade already fixed-steps; clamp `delta` in any custom integration.
- Reconcile body and sprite transforms in one place (Phaser does this automatically for physics sprites).
- Test high-speed movement for tunneling through thin walls and camera loss.
- Report engine choice, gravity, active body count, group sizes, sensors, collision categories, and risky overlaps.
- For Arcade, set up colliders/overlaps once in `create`, pool projectiles, and clear groups on restart.

## Gameplay Implementation Loop

For each mechanic:

1. Add state/data (often the scene registry or a store).
2. Add simulation/update.
3. Add visual representation (sprite/graphics/tween).
4. Add feedback: HUD, audio, particles, camera, animation.
5. Add diagnostics.
6. Verify with real input and one failing edge case.

Examples:

- Pickup: spawn data, `overlap` trigger, score/meter state, collect particle/audio, HUD pulse tween, recycle/cleanup.
- Hazard: telegraph tween, movement/update, body, damage/fail state, hit flash + shake, restart.
- Combo: timer event, reward multiplier, UI badge, audio ramp, reset rules.
- Weapon/action: cooldown timer, pooled projectile/hit, impact particles + flash, ammo/charge UI, target readability.

## Game Feel Pass

Run several short loops and tune one axis at a time:

- Movement speed and acceleration/drag.
- Camera zoom, follow lerp, deadzone, and look-ahead.
- Reaction windows and obstacle spacing.
- Jump/boost/attack cooldowns and coyote/buffer windows.
- Pickup magnetism and reward timing.
- Hit feedback (shake, flash, hit-stop) and restart speed.
- Difficulty ramp and pacing.

Record meaningful constants changed (keep them in one tuning module). If the game feels worse after a pass, revert or reduce the last tuning change instead of layering compensating changes.

## Audio Hooks

Use `this.load.audio` + `this.sound` or project audio utilities:

- UI click/pause/retry.
- Pickup/score.
- Damage/fail.
- Boost/speed.
- Combo/milestone.
- Ambient loop or procedural drone when appropriate.

Unlock Web Audio on first user input (Phaser handles this when `this.sound` is used after a pointer/key event). Audio should reflect state, not play random decoration. Respect mute and reduced-motion/accessibility settings when present.

## Diagnostics

Expose:

- FPS / frame time via `this.game.loop.actualFps`.
- Active game object and group counts.
- Current scene and game state.
- Player position/velocity.
- Active physics body count.
- Active tweens, timers, and particle counts.
- Input intents.
- Tunable constants when using a debug GUI.

Diagnostics should be easy to disable or gate for release.

## Verification

Minimum evidence after meaningful gameplay work:

- `npm run build` or equivalent.
- Local browser run.
- Console/page error check.
- Nonblank canvas pixel check.
- Desktop screenshot.
- Mobile screenshot when in scope.
- Main input path tested.
- Objective progression tested.
- Fail/retry tested when relevant.

## Common Failures

- Static scene instead of game.
- Multiple scenes/loops fighting (forgot to stop a scene; HUD in the play scene scrolls away).
- Camera not following, no bounds, or hides the next decision.
- Mechanic cannot be triggered from real input.
- HUD/audio/VFX do not reflect state changes.
- Faster movement breaks collision (tunneling) or camera framing.
- Restart leaves stale entities, tweens, timers, emitters, or input listeners.
- Mobile input works visually but does not emit game intents.
- Spritesheet loads but frame size/offset wrong, body unset, or no fallback texture.
