# Physics Engine Selection

Use this reference before adding or changing physics, collision-heavy gameplay, platforming, top-down movement, projectiles, moving platforms, ball/rolling games, sensors/overlaps, rigid-body puzzles, destructible props, character controllers, or high-speed collision.

## Current Recommendation

Default to this ladder:

1. Custom checks: arcade triggers, pickups, lanes, bullets, simple distance/rectangle overlap tests, deterministic rails, or games where authored feel matters more than simulation.
2. Arcade Physics: default robust choice for serious Phaser browser games that need AABB bodies, velocity/acceleration/gravity, world bounds, colliders, overlaps, sensors, tile collision, and fast deterministic behavior on desktop and mobile.
3. Matter.js: use when Arcade's axis-aligned model is insufficient: rotation, slopes/angled surfaces, joints/constraints, stacking, compound or polygon bodies, and realistic restitution.
4. Custom + tweens: scripted hazards and moving platforms that never need true collision response.

For most new Phaser games, choose Arcade. Reach for Matter only when a mechanic genuinely needs rotational rigid bodies or non-AABB shapes.

## Why Arcade Is The Default

Phaser is a renderer plus a game framework with two built-in physics systems. Arcade Physics is an AABB (axis-aligned bounding box) engine: every body is an upright rectangle or circle. It is extremely fast, allocation-light, and deterministic, which is exactly what platformers, top-down games, runners, shooters, brick/breakout, and most arcade games want.

Arcade supports velocity, acceleration, drag, gravity (`gravity: { x, y }`), bounce, world bounds (`setCollideWorldBounds`), immovable/static bodies, group-vs-group collision, overlaps with callbacks, separation, and tilemap collision. It runs at the game's fixed simulation rate and synchronizes the body to the Game Object automatically.

## Why And When To Use Matter

Matter.js is a full 2D rigid-body engine bundled with Phaser. Bodies can rotate, have arbitrary convex/compound shapes, stack, rest on slopes, and be linked with constraints/joints. Use it when AABB is a lie for the mechanic.

Matter is heavier and less deterministic than Arcade. Do not pick it for a platformer or top-down shooter just because it sounds more capable.

## Choose By Game Type

Use custom checks:

- Endless runners, lane dodgers, simple shooters, pickups, checkpoint gates, scripted hazards.
- Transform-driven movement where feel is custom and barriers are simple rectangles.
- Bullet-hell overlap tests using distance or `Phaser.Geom.Intersects`.

Use Arcade Physics:

- Platformers (gravity, jumping, one-way and solid tiles, moving platforms via kinematic/immovable bodies).
- Top-down arenas, twin-stick shooters, survivors, roguelikes.
- Breakout/brick, asteroids, runners, bullet groups, pickups, enemies.
- Tilemap collision (`setCollisionByProperty`, `collider(player, layer)`).
- Sensor/trigger zones via `overlap` and `body.setAllowGravity(false)`.
- High body counts where speed and determinism matter.

Use Matter.js:

- Physics puzzles, stacking crates, dominoes, rope/chain via constraints.
- Angled surfaces and slopes where bodies must rotate and slide.
- Pinball, marble/ball games with realistic bounce and spin.
- Soft pegboard / Peggle-style restitution, ragdolls, vehicles with joints.
- Anything needing compound bodies, polygon hulls, or constraints.

Avoid pixel-perfect collision:

- Use AABB rectangles/circles, simplified compound bodies, and explicit sensor zones.
- Generated sprites/atlases get separate, simplified collision bodies — never collide against the raw frame pixels.

## Arcade Setup Pattern

Configure in the game config (no install needed; bundled):

```ts
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: 0 }, debug: false },
  },
  scene: [BootScene, PreloadScene, PlayScene],
};
```

Platformer gravity lives in config (`gravity: { y: 900 }`); top-down games use `gravity: { y: 0 }`.

Create bodies and groups:

```ts
const player = this.physics.add.sprite(100, 100, 'hero').setCollideWorldBounds(true);
player.setDragX(1200);

const walls = this.physics.add.staticGroup();
const enemies = this.physics.add.group();
const bullets = this.physics.add.group({ defaultKey: 'bullet', maxSize: 64 });
```

Wire interactions in one place:

```ts
this.physics.add.collider(player, walls);
this.physics.add.collider(player, layer);                 // tilemap layer
this.physics.add.overlap(player, pickups, (p, item) => {
  (item as Phaser.GameObjects.GameObject).destroy();
});
```

Sensors / triggers (overlap, no separation):

```ts
const goal = this.physics.add.staticSprite(x, y, 'goal');
(goal.body as Phaser.Physics.Arcade.StaticBody).setSize(48, 48);
this.physics.add.overlap(player, goal, () => this.win());
```

Moving platform (kinematic feel via immovable body + tween):

```ts
const plat = this.physics.add.image(x, y, 'plat').setImmovable(true);
(plat.body as Phaser.Physics.Arcade.Body).setAllowGravity(false);
this.tweens.add({ targets: plat, x: x + 200, yoyo: true, repeat: -1, duration: 2000 });
```

Fixed-step intent: Arcade already runs at a fixed simulation step. Use `update(time, delta)` for input/intents and let physics integrate; clamp any custom integration with `delta`.

## Matter Setup Pattern

Configure Matter instead of Arcade:

```ts
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  physics: {
    default: 'matter',
    matter: { gravity: { x: 0, y: 1 }, debug: false },
  },
};
```

Bodies, world bounds, and shapes:

```ts
this.matter.world.setBounds(0, 0, worldW, worldH);

const crate = this.matter.add.sprite(x, y, 'crate', undefined, {
  restitution: 0.2,
  friction: 0.6,
});
const ball = this.matter.add.sprite(x, y, 'ball', undefined, {
  shape: { type: 'circle', radius: 16 },
  restitution: 0.9,
});
```

Sensors and collision events:

```ts
const zone = this.matter.add.rectangle(x, y, 64, 64, { isSensor: true, isStatic: true });
this.matter.world.on('collisionstart', (_e, bodyA, bodyB) => {
  // identify via bodyA.gameObject / bodyB.label
});
```

## Architecture Rules

- Put physics ownership in `systems/PhysicsSetup`, `systems/CollisionSystem`, or equivalent.
- Do not create bodies or wire colliders inside render/update hot loops; set them up in `create()`.
- Keep body/group references on entities and clear them on restart (`group.clear(true, true)`).
- Update order: input intents -> physics step (engine-driven) -> game state/collision callbacks -> VFX/camera/UI -> render.
- Toggle `arcade.debug=true` (or `matter.debug=true`) for body/velocity overlays during tuning, gated from release.
- Use immovable Arcade bodies (or `setStatic`) for moving platforms and scripted obstacles.
- Use `overlap` (Arcade) or `isSensor` (Matter) for pickups, goals, holes, portals, checkpoints, triggers, and damage zones.
- Pool bullets/particles via Groups instead of creating/destroying every frame.
- Destroy bodies, tweens, timers, and emitters on scene shutdown to avoid stale simulation.

## Tuning Rules

- Tune in pixels/second and pixels/second^2 that map cleanly to scene scale.
- Clamp or use `delta` in any custom movement integration so feel is frame-rate independent.
- Tune drag, bounce, gravity, body size/offset, and collision categories explicitly.
- For platformers: tune gravity, jump velocity, coyote time, jump buffer, terminal fall speed, and one-way platform behavior.
- For top-down: tune acceleration, drag, max speed, and overlap radii rather than raw teleport movement.
- For Matter balls/pinball: tune restitution, friction, frictionAir, density, and slop.
- For arcade vehicles: combine scripted control logic with Arcade collision response; do not rely on Matter alone for car feel.
- For character controllers: prefer a tight Arcade body with a custom `setSize`/`setOffset` rather than the full sprite frame.

## Verification Requirements

For physics work, verify:

- Build/typecheck.
- Browser run with console/page error check.
- Real input changes body velocity/position.
- Collision/overlap callback path fires.
- Restart clears or resets bodies and groups.
- High-speed movement does not pass through thin walls (increase body checks or use Arcade `tileBias`/smaller steps; Matter handles this natively).
- Mobile/low-FPS frame spikes do not break simulation.
- Physics diagnostics: engine used, active body count, group sizes, gravity, debug state, sensors, collision categories, and risky overlaps.

## Common Failures

- Choosing Matter for a platformer/top-down game that Arcade handles better and faster.
- Body and sprite drift because the body size/offset never matched the art.
- Bodies/groups persist after restart.
- Thin walls let fast bodies tunnel in Arcade (no continuous collision; mitigate with `tileBias`, larger bodies, or substeps).
- Overlap zones missing `setAllowGravity(false)` and falling out of the world.
- Moving platforms tween visually but the body is not immovable, so the player shoves them.
- Debug overlay or `arcade.debug` left enabled in release.
- Creating/destroying bullets each frame instead of pooling, causing GC spikes.

## Source Basis

- Phaser 3 docs: Arcade Physics is an AABB engine for fast, lightweight collision; Matter.js is a full 2D rigid-body engine for rotation, constraints, and complex shapes.
- Phaser 3 docs: configure physics via `config.physics.default` and `arcade`/`matter` blocks; add bodies with `this.physics.add.*` / `this.matter.add.*`; wire interactions with `collider`/`overlap` (Arcade) or `collisionstart` events (Matter).
- Phaser 3 docs: tilemap layers expose `setCollisionByProperty` and integrate with Arcade colliders.
