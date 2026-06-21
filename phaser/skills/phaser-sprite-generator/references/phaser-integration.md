# Phaser Integration

Use this after `phaser-sprite-generator` produces a spritesheet, sliced frames,
or a packed atlas. The goal: load the art, build animations, anchor origins
correctly, and pool spawned sprites.

## Preferred Outputs

- Single simple animation strip: uniform **spritesheet** PNG (no JSON).
- Whole character / object kit / UI set: packed **atlas** PNG + JSON.
- Tilemap art: a **tileset** PNG loaded via `this.load.image` then
  `map.addTilesetImage(...)` (a tilemap, not a spritesheet, owns the slicing).
- Static single sprite/icon: a trimmed transparent **image** PNG.

## Loading

Spritesheet (uniform grid — the `sheet` subcommand prints this frameConfig):

```ts
function preload(this: Phaser.Scene) {
  this.load.spritesheet('hero-run', 'assets/spritesheets/hero-run.png', {
    frameWidth: 64, frameHeight: 64,   // must match the slice cell size
    margin: 0, spacing: 0,
  });
}
```

Atlas (packed PNG + TexturePacker JSON Hash):

```ts
this.load.atlas('hero', 'assets/atlas/hero.png', 'assets/atlas/hero.json');
```

Tileset (image, sliced by the tilemap, not by frameConfig):

```ts
this.load.image('dungeon-tiles', 'assets/tilesets/dungeon-tiles.png');
// later:
const map = this.make.tilemap({ key: 'level', tileWidth: 16, tileHeight: 16 });
const tiles = map.addTilesetImage('dungeon', 'dungeon-tiles');
const ground = map.createLayer('ground', tiles!, 0, 0);
```

## Building Animations

From a spritesheet (frames by index):

```ts
this.anims.create({
  key: 'run',
  frames: this.anims.generateFrameNumbers('hero-run', { start: 0, end: 7 }),
  frameRate: 12,
  repeat: -1,
});
sprite.play('run');
```

From an atlas (frames by name — match the file names the packer wrote):

```ts
this.anims.create({
  key: 'run',
  frames: this.anims.generateFrameNames('hero', {
    prefix: 'hero_', start: 0, end: 7, zeroPad: 3, suffix: '.png',
  }),
  frameRate: 12,
  repeat: -1,
});
```

Notes:

- `repeat: -1` loops; omit (or `repeat: 0`) for one-shots (attack, hurt, death).
- Use `repeatDelay`/`yoyo` for idle breathing loops.
- Listen for completion on one-shots:
  `sprite.once(Phaser.Animations.Events.ANIMATION_COMPLETE + '-attack', cb)` or
  `sprite.on('animationcomplete', (anim) => { if (anim.key === 'attack') ... })`.
- Define animations once (a Boot/Preload step or a global anim registry); they
  live on `this.anims` (the global manager), not per-sprite.

## Origin / Pivot

- Default origin is `(0.5, 0.5)` (center). Phaser draws and rotates around it.
- Feet-anchored characters (platformers/top-down): `sprite.setOrigin(0.5, 1)` so
  the sprite "stands" on its y position and tile collisions line up at the feet.
- Projectiles/pickups: keep center origin so rotation and spin look right.
- Trimmed atlas frames keep their original frame box via `spriteSourceSize`, so
  the origin stays consistent across an animation even when individual frames
  were tightly cropped — do not re-set origin per frame.
- Arcade bodies do not auto-fit the visible art: size the body with
  `body.setSize(w, h)` / `body.setOffset(x, y)` to match the trimmed silhouette,
  not the full cell.

## Object Pooling

Never create art at runtime and never spawn unbounded sprites. Pool with Groups:

```ts
const bullets = this.physics.add.group({ defaultKey: 'bullet', maxSize: 64 });

function fire(this: Phaser.Scene, x: number, y: number) {
  const b = bullets.get(x, y) as Phaser.Physics.Arcade.Sprite | null;
  if (!b) return;                 // pool exhausted — drop, do not allocate
  b.setActive(true).setVisible(true);
  b.body!.enable = true;
  b.setVelocity(600, 0);
}

// recycle on hit / off-screen:
function kill(b: Phaser.Physics.Arcade.Sprite) {
  b.setActive(false).setVisible(false);
  b.body!.stop();
  b.body!.enable = false;
}
```

Recycled sprites reuse the same texture frame — atlases keep all those frames in
one texture, so pooled spawns of mixed art still batch into few draw calls.

## Asset Intake Checklist

Inspect before shipping:

- PNG dimensions and per-cell size (do frames divide evenly?).
- Transparent background actually keyed to alpha (no backdrop ring under tint).
- Frame count and order match the animation definition.
- Atlas JSON frame names match `generateFrameNames` prefix/pad/suffix.
- Origin/pivot correct for the game type (feet vs center).
- Arcade/Matter body size vs the trimmed silhouette.
- Palette consistency across a sprite family.
- Texture/atlas memory and total texture count (fewer, packed = better batches).
- Mobile: cell resolution vs DPR; downscale if oversized.

## Game Asset Strategy

- Use `phaser-sprite-generator` for hero characters, enemies, bosses, props,
  pickups, projectiles, and tilesets — the in-game sprite pipeline.
- Use `phaser-image-generator` for concept art, backgrounds, sky/parallax plates,
  decals, logos, HUD/item icons, title and menu art.
- Combine: concept (image-generator) → sprite sheet source (sprite-generator
  generate) → slice (`sheet`) → pack (`atlas`) → load + animate → pool.
- Build high-volume repeated detail (floor variants, debris, particles-as-sprites)
  from a small atlas plus tint/scale variation rather than many unique textures.

## Performance Discipline

- Pack related frames into one atlas to cut draw-call batches and texture count.
- Tint and blend modes are nearly free; prefer tinting one base sprite over
  generating a recolor when only color differs.
- Pool every frequently spawned sprite; cap `maxSize`.
- Cull/`setVisible(false)` off-screen sprites; let the camera bounds do the rest.
- Keep atlas PNGs reasonably sized; downscale cells for low-DPR targets.
- Clean up on scene shutdown: stop tweens/timers/emitters, and
  `this.textures.remove(key)` for art that will not be reused.

## Common Fixes

- Backdrop ring/halo under a tint: the background was not keyed — re-run with
  `--transparent --key-color ... --tolerance` (raise tolerance for anti-aliasing).
- Animation jitters/wobbles: frames are not uniform (Gemini drift) — regenerate
  the sheet demanding identical pivot/scale/cell size, or re-slice with exact
  `--frame-width/--frame-height`.
- Frames off by a pixel: sheet did not divide evenly — pass exact cell size and
  set `margin`/`spacing` to match the source.
- Atlas frames not found: animation `generateFrameNames` prefix/pad/suffix do not
  match the packed file names — check the JSON keys the `atlas` command printed.
- Sprite "floats" or sinks into the ground: wrong origin — use `setOrigin(0.5, 1)`
  for feet-anchored characters and size the body to the silhouette.
- Too much texture memory: pack separate spritesheets into atlases; downscale.

## Final Evidence

Report:

- Prompts and model used per generation.
- Output paths: source PNG, frames dir, atlas PNG + JSON.
- Grid dimensions, transparency/trim settings, resolution.
- The Phaser load snippet + frameConfig (spritesheet) or atlas keys.
- Animation definitions added (keys, frameRate, repeat).
- Files changed in the game project.
- Screenshot/canvas-pixel evidence of the sprite animating in gameplay.
