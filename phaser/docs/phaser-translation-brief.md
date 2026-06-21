# Phaser 3 Skill Translation Brief (shared)

You are porting one skill from the **Three.js** game-skills suite to an equivalent **Phaser 3
(2D)** skill. This brief is shared by all skill-porting agents so the suite stays consistent.

## Mission

Produce a faithful Phaser 3 equivalent of an existing Three.js skill. "Faithful" means: same
purpose, same file shape, same structure and tone, same level of rigor and the same gate/ledger
discipline — but every 3D concept, API, and asset workflow is replaced by its correct **2D
Phaser 3** counterpart. The result must read like it was written by the same author, for Phaser.

## Hard rules

1. **Read your source first.** Read every file in your assigned Three.js source skill directory
   (`SKILL.md`, all of `references/`, all of `scripts/`, `agents/openai.yaml`) before writing.
   Mirror its structure file-for-file unless this brief says otherwise.
2. **Write ONLY inside your assigned destination directory.** Never edit anything under
   `threejs-game-skills/` and never write into another skill's directory.
3. **Keep the front-matter shape.** Each `SKILL.md` starts with YAML front-matter:
   ```
   ---
   name: <phaser-skill-name>
   description: "<trigger-rich description, same style/length as the source>"
   ---
   ```
   Rewrite the description for Phaser/2D triggers (build-a-2D-game, platformer, top-down,
   arcade, shoot-em-up, roguelike, sprite, tilemap, etc.). Keep it dense with trigger words like
   the source.
4. **Rename references.** Everywhere the source says Three.js / WebGLRenderer / mesh / material /
   geometry / camera-in-3D / 3D model / GLB/FBX / Tripo, replace with the correct Phaser 3 / 2D
   concept (see the translation table). Replace `threejs-` skill names with `phaser-` names.
5. **Scripts must stay runnable.** Any ported Python/Node script must pass a syntax check
   (`python3 -m py_compile` / `node --check`). Keep the same CLI shape and flags as the source
   unless the provider differs (see per-skill notes).
6. **No invented APIs.** Use only the Phaser 3 APIs in the cheat sheet below or ones you are
   certain exist in Phaser 3.60+. When unsure, prefer the documented forms here.
7. **Match length and depth.** Do not summarize the source down to a stub. If the source
   `references/` has 5 checklists, produce 5 equivalent checklists.

## Suite naming (use these exact names in cross-references)

| Three.js | Phaser |
| --- | --- |
| threejs-game-director | phaser-game-director |
| threejs-gameplay-systems | phaser-gameplay-systems |
| threejs-aaa-graphics-builder | phaser-aaa-graphics-builder |
| threejs-game-ui-designer | phaser-game-ui-designer |
| threejs-debug-profiler | phaser-debug-profiler |
| threejs-qa-release | phaser-qa-release |
| threejs-3d-generator | **phaser-sprite-generator** (spritesheets/tilesets/atlases) |
| threejs-image-generator | phaser-image-generator |
| threejs-audio-generator | phaser-audio-generator |

## 3D → 2D concept translation table

| Three.js / 3D | Phaser 3 / 2D |
| --- | --- |
| `WebGLRenderer`, render loop | `Phaser.Game` (`type: Phaser.AUTO`), Scene `update(time, delta)` |
| Scene graph, `THREE.Scene` | `Phaser.Scene` (Boot/Preload/Play/UI), display list |
| Mesh = geometry + material | Sprite / Image / Graphics / TileSprite from a texture |
| Geometry / procedural geometry | `this.add.graphics()` shapes, `generateTexture()`, tilemaps, Graphics→texture |
| Material / PBR / shaders | Tint, blend modes, custom **pipelines** (`Phaser.Renderer.WebGL.Pipelines.PostFXPipeline`), preFX/postFX |
| Lighting (3D lights) | **Lights2D** (`this.lights`, `Light2D` pipeline, normal maps) + faked light via gradients/additive sprites |
| Camera (PerspectiveCamera) | `this.cameras.main` (2D ortho): `startFollow`, `setZoom`, `setBounds`, `shake`, `flash`, `fade` |
| Post-processing (EffectComposer, bloom pass) | Camera/GameObject **postFX**: `.postFX.addBloom()`, `.addGlow()`, `.addVignette()`, custom PostFXPipeline |
| Rapier / cannon-es physics | **Arcade Physics** (default) or **Matter.js** (complex bodies) |
| Instancing / LOD / draw calls | Texture atlases, sprite batching, object pooling (Groups), `setVisible`/culling |
| GLB/FBX 3D models (Tripo) | **Spritesheets / texture atlases / tilesets** (sliced PNGs) |
| Skybox / environment map | Parallax background layers (`tileSprite`), sky gradient image |
| OrbitControls | Pointer drag / pinch-zoom / keyboard camera control |
| `dispose()` of geometries/materials/textures | Scene `shutdown`/`destroy`, `this.textures.remove`, tween/timer/emitter cleanup, group clearing |

## Physics selection rule (used by gameplay + director + debug)

- **Arcade** = AABB only, very fast, deterministic. Use for platformers, top-down, runners,
  shooters, brick/breakout, most arcade games. Bodies: `this.physics.add.sprite/group/staticGroup`;
  interactions: `this.physics.add.collider(a, b)` and `this.physics.add.overlap(a, b, cb)`.
- **Matter** = full rigid-body (rotation, slopes, joints, stacking, complex shapes). Use only
  when Arcade's AABB model is insufficient. Bodies: `this.matter.add.sprite(...)`, constraints,
  `setBounds`.
- Config: `physics: { default: 'arcade', arcade: { gravity: { y: 0|N }, debug: false } }`.

## Phaser 3 API cheat sheet (verified, safe to use)

```ts
import Phaser from 'phaser';

// Game config
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  backgroundColor: '#0b0e14',
  scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH,
           parent: 'game', width: 960, height: 540 },
  physics: { default: 'arcade', arcade: { gravity: { x: 0, y: 0 }, debug: false } },
  scene: [BootScene, PreloadScene, PlayScene],
};
new Phaser.Game(config);

// Scene lifecycle
class PlayScene extends Phaser.Scene {
  constructor() { super('Play'); }
  preload() { this.load.image('hero', 'hero.png');
              this.load.spritesheet('run', 'run.png', { frameWidth: 32, frameHeight: 32 }); }
  create() { /* build world */ }
  update(time: number, delta: number) { /* per-frame */ }
}

// Input
const cursors = this.input.keyboard!.createCursorKeys();
const keys = this.input.keyboard!.addKeys('W,A,S,D') as Record<string, Phaser.Input.Keyboard.Key>;
if (Phaser.Input.Keyboard.JustDown(cursors.space)) { /* once per press */ }
this.input.on('pointerdown', (p: Phaser.Input.Pointer) => { /* tap/click */ });

// Arcade physics
const player = this.physics.add.sprite(100, 100, 'hero').setCollideWorldBounds(true);
player.setVelocity(0, 0);
this.physics.add.collider(player, walls);
this.physics.add.overlap(player, pickups, (p, item) => (item as Phaser.GameObjects.GameObject).destroy());

// Camera
this.cameras.main.startFollow(player, true, 0.1, 0.1);
this.cameras.main.setBounds(0, 0, worldW, worldH);
this.cameras.main.shake(120, 0.004);

// Tweens & timers
this.tweens.add({ targets: player, scale: 1.2, yoyo: true, duration: 120, ease: 'Quad.out' });
this.time.addEvent({ delay: 1000, loop: true, callback: () => {} });
this.time.delayedCall(500, () => {});

// Particles (Phaser 3.60+ API)
const emitter = this.add.particles(x, y, 'spark', {
  speed: { min: 60, max: 180 }, lifespan: 500, quantity: 8, scale: { start: 1, end: 0 },
  blendMode: 'ADD',
});
emitter.explode(20, x, y);

// Post FX / FX (WebGL)
player.postFX.addGlow(0x66ccff, 4);
this.cameras.main.postFX.addBloom(0xffffff, 1, 1, 1.2, 1.1);
this.cameras.main.postFX.addVignette(0.5, 0.5, 0.9, 0.4);

// Lights2D
this.lights.enable().setAmbientColor(0x202030);
const light = this.lights.addLight(x, y, 200).setColor(0xffffff).setIntensity(2);
sprite.setPipeline('Light2D'); // sprite must have a normal map for full effect

// Text & HUD (use a separate UI Scene that runs in parallel via this.scene.launch('UI'))
this.add.text(16, 16, 'Score: 0', { fontFamily: 'monospace', fontSize: '20px', color: '#fff' })
    .setScrollFactor(0).setDepth(1000);
this.add.bitmapText(16, 16, 'pixel', 'Score: 0', 24);

// Tilemap
const map = this.make.tilemap({ key: 'level', tileWidth: 16, tileHeight: 16 });
const tiles = map.addTilesetImage('tiles', 'tiles');
const layer = map.createLayer('ground', tiles!, 0, 0);
layer!.setCollisionByProperty({ collides: true });
this.physics.add.collider(player, layer!);

// Asset loading
this.load.atlas('sheet', 'sheet.png', 'sheet.json'); // TexturePacker JSON Hash/Array
this.load.bitmapFont('pixel', 'pixel.png', 'pixel.xml');
this.load.audio('sfx', ['sfx.ogg', 'sfx.mp3']);

// Object pooling
const bullets = this.physics.add.group({ defaultKey: 'bullet', maxSize: 64 });
const b = bullets.get(x, y); if (b) { b.setActive(true).setVisible(true); }

// Cleanup on scene shutdown
this.events.once(Phaser.Scenes.Events.SHUTDOWN, () => { emitter.destroy(); });
```

Notes:
- `this.input.keyboard` / `this.input.gamepad` can be null in strict TS — use `!` or guard.
- Prefer `Phaser.Math` (`Phaser.Math.Between`, `Clamp`, `Linear`, `Vector2`) over ad-hoc math.
- Animations: `this.anims.create({ key, frames: this.anims.generateFrameNumbers('run', {start:0,end:7}), frameRate: 12, repeat: -1 })`.
- Mobile: pointer events already cover touch; add on-screen buttons via a UI Scene; respect safe areas with `env(safe-area-inset-*)` in CSS around the canvas parent.

## Verification vocabulary (replace 3D terms)

- "draw calls / triangles / texture memory" → "draw calls (batches) / active sprites / texture
  & atlas memory".
- "canvas nonblank pixel check" stays — the QA canvas inspector is renderer-agnostic.
- "performance snapshot" → `this.game.loop.actualFps`, active game objects, particle counts,
  active tweens, physics body count.

## Per-skill notes

- **phaser-gameplay-systems**: owns the scaffold. The scaffold itself (`assets/phaser-vite-game/`)
  is provided SEPARATELY — **do not create `assets/`**. Write `scripts/create_phaser_game.py`
  (port of `create_threejs_game.py`) that copies `../assets/phaser-vite-game` to a target dir.
  Include `references/physics-engine-selection.md` (Arcade vs Matter) and a "new-game definition
  of done" + a premium genre checklist (e.g. platformer or top-down instead of endless-runner —
  keep one concrete premium genre checklist).
- **phaser-aaa-graphics-builder**: keep the AAA framing and the visual-scorecard gate. Replace
  model-recipes/render-recipes/material-lighting with 2D equivalents: sprite/atlas architecture,
  parallax recipes, particle/VFX recipes, pipeline/postFX recipes, Lights2D, juice (squash &
  stretch, screen shake, hit-stop, flash). Keep the same checklist filenames' intent.
- **phaser-debug-profiler**: scene/runtime/loader bugs, black canvas, scale/resize bugs, mobile
  input, performance (fps, batches, active objects, texture/atlas memory, particle/tween counts),
  arcade debug graphic (`arcade.debug=true`), `this.physics.world.drawDebug`.
- **phaser-qa-release**: port `inspect-threejs-canvas.mjs` → `inspect-phaser-canvas.mjs`
  (the logic is renderer-agnostic; just rename and update messages/usage text). Keep build/preview/
  base-path/responsive/canvas-pixel checklists.
- **phaser-sprite-generator** (was 3d-generator): this is the biggest re-think. NO Tripo, NO 3D.
  It generates **2D game art**: character/object sprites, spritesheets (uniform frames),
  tilesets, and texture atlases — using the Gemini image API as the generator plus local image
  processing (slicing a sheet into frames, packing frames into an atlas + JSON, enforcing
  transparent backgrounds and a consistent palette). Env var: `GEMINI_API_KEY`. Write
  `scripts/phaser_sprite_asset.py` (Gemini call + Pillow-based slice/pack; degrade gracefully if
  Pillow is missing). references: `api-notes.md` (Gemini + sheet/atlas formats), 
  `phaser-integration.md` (how to load spritesheet/atlas and build anims), and
  `image-generator-workflows.md` (how it pairs with phaser-image-generator). Keep the
  `agents/openai.yaml` shape.
- **phaser-image-generator**: port `generate_image.py` nearly verbatim (Gemini) — same
  `GEMINI_API_KEY`, same CLI. Reframe the SKILL/description for 2D game art: concepts, sprite
  sheets sources, tileset sources, backgrounds, skies, decals, icons, logos, GUI art.
- **phaser-audio-generator**: port `threejs_audio_asset.py` → `phaser_audio_asset.py` nearly
  verbatim (ElevenLabs, `ELEVENLABS_API_KEY`). Reframe SKILL for Phaser audio integration
  (`this.load.audio`, `this.sound.add`, web audio unlock on first input, sprite audio).
- **phaser-game-director**: authored separately by the lead — porting agents do NOT write it.

## Output

Write the complete skill directory at the destination path you are given. When done, report:
the files you created, anything you deliberately changed from the source structure, and any
Phaser API you used that is outside this cheat sheet (so it can be verified).
