# Phaser Image Generator Pairing

Use `phaser-image-generator` when a strong concept or non-sprite asset improves
`phaser-sprite-generator` output, or when the final asset is a background / icon /
logo rather than an in-game sprite. Both skills use Google's Gemini image API and
the same `GEMINI_API_KEY` — the difference is the workflow, not the provider.

## Division Of Labor

- `phaser-image-generator`: concept sheets, style sheets, backgrounds, sky and
  parallax plates, menu/title art, logos, faction marks, HUD/item/ability icons,
  decals, button skins, GUI panels — standalone 2D art that is loaded with
  `this.load.image`.
- `phaser-sprite-generator` (this skill): the in-game sprite pipeline — generate
  a sprite/animation-strip/tileset, key the background to alpha, slice the grid
  into frames, and pack frames into an atlas PNG + JSON for `this.load.atlas`.

## Concept → Sprite Sheet Source → Slice/Pack

The core pipeline this pairing enables:

1. **Concept** (`phaser-image-generator`): generate a clean reference of the
   character/enemy/object — a turnaround or a style sheet that locks palette,
   proportions, and silhouette. Save under `assets/concepts/`.
2. **Sprite sheet source** (`phaser-sprite-generator generate`): generate the
   actual uniform-grid animation strip, passing the concept as `--input-image`
   to lock style and a `--style` clause for the palette. Use `--transparent` and
   `--columns/--rows` matching the intended frame count.
3. **Slice** (`phaser-sprite-generator sheet`): cut the grid into per-frame PNGs
   with `--trim`.
4. **Pack** (`phaser-sprite-generator atlas`): pack the frames into one atlas
   PNG + JSON for `this.load.atlas`, or keep them as a uniform spritesheet.

## Concept / Style Reference Images

Generate clean references before sprite generation for:

- Characters: front/side/back turnaround, neutral pose, visible hands/feet,
  clear costume layers, color callouts.
- Enemies/creatures: side silhouette, readable limb count, attack-pose hint.
- Objects/pickups: centered item, plain background, strong outline, no baked text.
- Tilesets: a biome mood board / palette and a few example tiles to copy.
- Vehicles/props: side and three-quarter, clear material zones.

Prompt pattern (image-generator):

```text
Create a clean 2D game art reference of [asset]. Centered, plain flat background,
full subject visible, readable silhouette, [style], [palette], game-ready, no text,
no motion blur, no cropped parts.
```

For an animation-ready character reference:

```text
Create a side-view character reference for sprite animation: [character]. Neutral
standing pose, arms and legs visible, consistent palette, flat background,
game-ready proportions, [pixel-art/clean vector] style.
```

## Backgrounds, Skies, Parallax, UI (use image-generator directly)

Use `phaser-image-generator`, not the sprite pipeline, for:

- Parallax layers and sky/horizon plates loaded as `tileSprite` backgrounds.
- Menu/title/loading illustrations.
- Logos, faction marks, achievement badges.
- HUD icons, item icons, ability icons, pickup symbols, hazard signs.
- Button skins, GUI panel art, decals.

These are single images, not sliced; load with `this.load.image` (or pack a UI
icon set into an atlas with this skill's `atlas` command if there are many).

## Sprite Pipeline Handoff

After generating a concept reference:

1. Save it in the working project, usually `assets/concepts/`.
2. Run `phaser-sprite-generator generate` with `--input-image <concept>` to lock
   style, plus `--transparent`, `--columns/--rows`, and a `--style` palette clause.
3. Slice with `sheet --trim`; pack with `atlas --trim --pot` when you want one
   texture for a whole character or kit.
4. Load + animate per `phaser-integration.md`; pool spawned sprites.

## Avoid

- Crowded multi-subject concepts for a single-sprite generation.
- Cropped limbs, hidden backs, heavy perspective, motion blur, or depth of field
  on art destined to become a uniform spritesheet.
- Baked-in frame numbers, grid lines, or labels on a spritesheet generation.
- Backdrops whose color also appears in the sprite (breaks color-key alpha) —
  use a chroma magenta/green you can key cleanly.
- Using the sprite pipeline for flat single-image UI/logo/background assets —
  generate those directly with `phaser-image-generator`.
- Inconsistent palettes across a sprite family — reuse a `--style` clause and an
  `--input-image` lock.
