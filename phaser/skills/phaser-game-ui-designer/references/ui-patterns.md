# Game UI Patterns (Phaser 3 / 2D)

Use this when designing HUDs, menus, overlays, pause/fail/win states, touch controls, typography, responsive layout, and UI/world cohesion.

## UI Principles

- Build the game interface, not a web dashboard.
- Prioritize gameplay hierarchy: survival/status, objective/progress, immediate feedback, then flavor.
- Use meters, icons, reticles, badges, alert strips, cooldown rings, inventory slots, minimaps, diegetic labels, and compact clusters before generic stat readouts.
- Keep UI outside the play path and away from threats, pickups, the player, and the next decision.
- UI should reinforce the world art direction through palette, icon shapes, tint, blend modes, and motion language (tweens, count-ups, pulses).
- Do not use visible text to explain obvious controls when an icon, affordance, or direct interaction can do the job.

## Surface Choice: UI Scene vs DOM Overlay

Decide this before building. Phaser gives you two fixed-to-screen surfaces and they have different strengths.

**Parallel UI Scene** — `this.scene.launch('UI')` from the play scene so the UI Scene runs *in parallel* over the gameplay scene, with its own camera and display list. Sleep/wake or stop it as needed.

```ts
// In PlayScene.create()
this.scene.launch('UI');           // run UI in parallel
this.scene.bringToTop('UI');       // keep UI above gameplay
// talk to it via the global registry or scene events
this.registry.set('score', 0);
this.events.emit('damage', 12);
```

Use a UI Scene when:

- The HUD should match the game's pixel art / canvas look (BitmapText, nineslice, sprites, Graphics).
- You want canvas tweens, particles, shaders/postFX, or Lights2D on UI elements.
- The UI is diegetic or animated (cooldown rings, combo pop, screen-shake-immune banners).
- You want one render path and no DOM/CSS layering concerns.

A UI Scene's objects are already fixed to its own camera, so they do not scroll with the world. Inside the *same* scene as gameplay, pin elements with `setScrollFactor(0)` and a high `setDepth(...)` instead.

**DOM overlay** — HTML/CSS positioned over the canvas parent (`<div id="game">`), or Phaser DOM Elements (`dom: { createContainer: true }` in config, then `this.add.dom(...)`).

Use a DOM overlay when:

- You need crisp, perfectly scalable text at any DPR (DOM text beats canvas text for small legible copy).
- You want easy responsive reflow with fl/grid/`clamp()` and media queries.
- You need real form controls (sliders, selects, toggles, text inputs) and accessibility/focus order.
- You need true safe-area handling via CSS `env(safe-area-inset-*)`.

Rule of thumb: in-world / juicy / pixel HUD → UI Scene; settings forms, long copy, accessibility, and edge-safe controls → DOM overlay. Mixing is fine: canvas HUD plus a DOM settings panel.

## Text: Text vs BitmapText

- `this.add.text(...)` renders TrueType/web fonts to a texture. Flexible styling (color, stroke, shadow, wordWrap, padding) but each distinct string re-rasterizes; avoid updating it every frame with `setText` for heavy strings.
- `this.add.bitmapText(...)` draws from a pre-baked glyph atlas (`this.load.bitmapFont('pixel','pixel.png','pixel.xml')`). Cheap to update every frame, pixel-perfect, ideal for scores/timers/combos and pixel-art games. Limited to the baked glyph set and style.
- Prefer BitmapText for frequently-changing numeric HUD (score, timer, ammo). Prefer Text (or DOM) for occasional, richly-styled, or localized copy.
- Load web fonts before the scene uses them (e.g. WebFontLoader in `preload`/Boot) so `Text` does not render in a fallback font.

## Containers, Nineslice, and Pinning

- Group related UI into a `this.add.container(x, y, [children])` so you can move, scale, show/hide, and depth-sort a cluster as one unit.
- Use `this.add.nineslice(x, y, 'panel', frame, width, height, leftW, rightW, topH, bottomH)` for resizable panels/buttons whose borders must not stretch — the core scales, the corners/edges stay crisp. This replaces fragile single-image panels.
- Pin HUD with `setScrollFactor(0)` (same-scene) and a high `setDepth(...)` so it floats above gameplay and ignores camera scroll/zoom. A dedicated UI Scene does this implicitly.
- `setScrollFactor(0)` is per-object; remember it for every HUD child or nest them in one pinned container.

## Required States

Inventory states before designing:

- Gameplay HUD.
- Pause/resume.
- Settings or audio/accessibility controls when useful.
- Fail/retry.
- Win/milestone/level complete when relevant.
- Loading/empty/error when async assets exist (a Preload scene with a progress bar via `this.load.on('progress', ...)`).
- Mobile/touch controls when target includes mobile.
- Debug/tuning UI gated separately from player UI.

Premium games should not have only one HUD state. Model modal states as overlay Scenes (`this.scene.launch('Pause')` + `this.scene.pause('Play')`) or pinned containers, not ad-hoc visibility toggles scattered through update.

## HUD Composition

Use intentional zones (all pinned with `setScrollFactor(0)` or in the UI Scene):

- Top or top-left: objective, wave, distance, timer, route/progress.
- Top or top-right: score, currency, combo, inventory, pause button.
- Bottom left/right: virtual stick / action buttons when needed.
- Center top or near player: short event banners, combo, warnings.
- Near-world labels: diegetic prompts, target markers, offscreen indicators. These DO follow the world (scrollFactor 1) and clamp to screen edges.

Rules:

- Use fixed-width numeric layouts for score, timer, ammo, speed, health, and best values (BitmapText with a fixed character box, or right-aligned Text with a reserved width).
- Use icons plus short labels for unfamiliar resources.
- Use meter fills (a Graphics bar, a cropped sprite via `setCrop`, or a scaled nineslice) for quantities the player must read quickly.
- Use alert colors/tints consistently: danger, reward, shield, boost, objective, disabled.
- Animate state changes briefly with tweens: count-up, meter fill, pulse (`scale` yoyo), slide/fade, ring cooldown.
- Do not stack multiple large banners over the play path.

## Menus And Overlays

Pause/fail/win overlays should support quick action. Implement as overlay Scenes or pinned containers with a dim/scrim behind them:

- Primary action first: resume, retry, continue, next.
- Secondary actions: settings, quit, restart, level select.
- Dim gameplay with a semi-transparent full-screen rectangle (`this.add.rectangle(0,0,w,h,0x000000,0.6).setOrigin(0)`) and pause the play scene (`this.scene.pause('Play')`).
- Avoid marketing-page hero layouts inside a game.
- Keep menu panels stable and readable across desktop/mobile and across Scale Manager modes.
- Use icon buttons for pause, sound, restart, fullscreen (`this.scale.toggleFullscreen()`), settings when familiar.
- Provide focus/hover/pressed/disabled states (see Interactive Buttons below).
- Gate debug panels behind a dev flag or query param.

## Interactive Buttons

- Make any game object a button with `setInteractive({ useHandCursor: true })` and pointer events: `pointerover`, `pointerout`, `pointerdown`, `pointerup`.
- Provide all four visual states: idle, hover (`pointerover`), pressed (`pointerdown`, e.g. tint + slight scale down), disabled (lowered alpha + `disableInteractive()`).
- For a precise hit area on a nineslice/container, pass an explicit shape: `setInteractive(new Phaser.Geom.Rectangle(...), Phaser.Geom.Rectangle.Contains)`.
- Keyboard/gamepad focus: track a "selected index" and re-style on `cursors.up/down`, confirm on `space`/`enter` via `Phaser.Input.Keyboard.JustDown`. Canvas has no native focus ring, so draw one.
- DOM overlay buttons get focus, `:hover`, `:active`, `:disabled`, and tab order for free — another reason to use DOM for settings.

## Touch Controls

When mobile is in scope:

- Pointer events already cover touch in Phaser; no separate touch API needed. Enable multi-touch with `this.input.addPointer(n)` so a stick and a button can be pressed at once.
- Ensure controls emit the same game intents as keyboard/mouse (set the same velocity/flags the keyboard path sets — do not fork the logic).
- Virtual stick: track `pointerdown` to set a base, `pointermove` to compute a normalized direction vector (`Phaser.Math.Angle.Between`, clamp radius), and `pointerup`/`pointerout`/`pointerupoutside` to recenter and zero input.
- Handle release on every exit path: `pointerup`, `pointerupoutside`, `gameout`, and the browser `blur`/`visibilitychange` so a held control never sticks.
- Use safe-area insets: if the canvas parent is full-bleed, pad bottom/side controls with CSS `env(safe-area-inset-*)` on the parent, or inset control positions from `this.scale.gameSize` by a margin.
- Avoid controls overlapping HUD warnings or the play path.
- Keep touch targets at least roughly 44 CSS pixels. Because the canvas may be scaled (FIT), convert: target a minimum of `44 / this.scale.displayScale.x` world pixels so the on-screen size stays ~44 CSS px.
- Separate adjacent controls enough to prevent accidental presses.
- On the canvas parent, set `touch-action: none` only on the game surface/control regions to stop the page scrolling/zooming during play.

## Responsive Constraints (Scale Manager)

Choose a Scale Manager mode and a design resolution up front, in the game config:

```ts
scale: {
  mode: Phaser.Scale.FIT,             // or RESIZE, ENVELOP
  autoCenter: Phaser.Scale.CENTER_BOTH,
  parent: 'game',
  width: 960, height: 540,            // design resolution
}
```

- **FIT**: scales the design-resolution canvas up/down to fit the parent while preserving aspect ratio, leaving letterbox bars. Simplest; layout is fixed at design resolution so text never reflows. Best default for most arcade/platform/top-down games.
- **RESIZE**: the canvas matches the parent exactly; you get the real width/height and must lay out UI yourself on every change. Best when you want edge-to-edge UI with no letterbox (e.g. responsive menus, full-bleed mobile). Requires a `resize` handler.
- **ENVELOP**: scales to cover the parent (fills both axes, may crop the design area). Use when a background must fill the screen and minor cropping of the play area is acceptable.
- `autoCenter` (`CENTER_BOTH`, `CENTER_HORIZONTALLY`) centers the scaled canvas in the parent.

Handle dynamic size when using RESIZE (or to reposition pinned UI under FIT):

```ts
this.scale.on('resize', (gameSize: Phaser.Structs.Size) => {
  const { width, height } = gameSize;
  pauseBtn.setPosition(width - 24, 24);
  scrim.setSize(width, height);
});
this.events.once(Phaser.Scenes.Events.SHUTDOWN, () =>
  this.scale.off('resize'));
```

Layout rules:

- Anchor UI to screen edges/centers from `this.scale.gameSize` (or the design `width`/`height` under FIT), not hard-coded pixels that assume one device.
- Do not let dynamic values resize their own layout: reserve width for the longest value.
- Check landscape and portrait; pick which you support and lock or adapt (`scale.lockOrientation` is not built-in — handle via CSS/UI reflow on `resize`).
- Test longest likely values: high score, long labels, multi-digit timers, localized-ish text if relevant.
- No clipped text, overlapping controls, unreadably small labels, or jumpy layout from changing values.
- Menus must remain on-screen and reachable at every supported aspect ratio.

## Safe Areas

- The canvas itself cannot read notch insets; the surrounding DOM can. Apply `padding: env(safe-area-inset-top) ...` to the canvas parent or to a DOM overlay, and add `viewport-fit=cover` to the viewport meta so `env()` reports real insets.
- For pure-canvas HUD, inset edge-anchored elements by a safe margin (e.g. 16–24 px scaled) and additionally read CSS env values via a hidden DOM probe if exact notch avoidance matters.
- Keep critical controls and warnings out of the top notch and the bottom home-indicator strip.

## Visual Style

- Match the genre: arcade/runners need speed/status readability; platformers need health/lives/coins clarity; shoot-em-ups need health/score/power hierarchy; roguelikes need inventory/objective/log clarity.
- Prefer restrained panels (nineslice with meaningful borders, ticks, glow accents) over nested cards.
- Use a limited status palette plus neutral surfaces; apply with tint and consistent blend modes.
- Avoid one-note purple/blue gradient UI unless it is strongly justified by the game world.
- Connect UI motifs to world tilesets, decals, faction marks, pickups, or hazards.
- Use camera/postFX sparingly on UI: a subtle `postFX.addGlow` on an active button or `addBloom` on a win banner reads as premium; do not bloom the whole HUD.

## 2D Asset Generation

Use `phaser-image-generator` for interface art when hand-drawn `Graphics`/styled DOM is not enough:

- Faction logos, team crests, title marks.
- Pickup, ability, weapon, inventory, achievement, and objective icons.
- Hazard signs, decals, lane glyphs, item badges.
- Menu/loading/background plates, illustrated map panels, world-style UI textures.
- Nineslice panel skins: glass panels, metal frames, holographic strips, paper/parchment, tactical screens (export with consistent corner margins so the slice geometry is clean).

Use `phaser-sprite-generator` only when the UI needs animated frames: an icon spritesheet, animated badge, or button-state sheet packed as an atlas with JSON, loaded via `this.load.atlas`/`this.load.spritesheet` and driven by `this.anims`.

## State Wiring

- UI reads game state from a single source of truth — the global `this.registry` (`this.registry.set/get`, `this.registry.events.on('changedata-score', ...)`) or a small store the play scene owns.
- UI events dispatch game intents (emit a scene/registry event, set a flag the play scene reads); they should not mutate unrelated simulation internals directly.
- A parallel UI Scene listens to the play scene: `this.scene.get('Play').events.on('damage', ...)`.
- UI should update on pause, restart, resize, orientation change, mute, fail/win, score, health, boost, combo, inventory, and accessibility settings.
- Avoid stale values after restart: reset registry/UI state in `create`, and unbind listeners on `SHUTDOWN` to prevent duplicate handlers when the scene restarts.

## Verification

Capture evidence:

- Gameplay HUD desktop screenshot.
- Gameplay HUD mobile screenshot when in scope.
- Pause/fail/retry state screenshot if changed.
- Text-fit and overlap check with high values.
- Touch target and safe-area check when mobile is in scope.
- Interaction test for UI buttons and touch controls (confirm the intent fires, not just the visual).
- Console/page error check after UI events and after scene restart.
- Resize check across the chosen Scale Manager mode (and across modes if unsure which to ship).
- Generated 2D asset path and prompt when `phaser-image-generator` was used.
- Loaded spritesheet/atlas key and anim keys when `phaser-sprite-generator` was used.

## Common Failures

- Generic stat-readout HUD with no hierarchy.
- HUD not pinned (`setScrollFactor(0)` missing) or not in a UI Scene, so it scrolls/zooms with the camera.
- Nested cards and oversized decorative panels.
- UI covers threats, pickups, player, or next decision.
- Text explains obvious controls instead of designing affordances.
- Wrong Scale Manager mode: FIT chosen when edge-to-edge UI was needed, or RESIZE chosen with no `resize` handler so UI piles in a corner.
- `Text` updated with `setText` every frame for heavy strings, tanking perf, where BitmapText belonged.
- Mobile safe areas ignored; controls under the notch or home indicator.
- Touch controls look correct but do not emit intents, or stick because a release path was unhandled.
- Values change width and shift layout during play.
- Listeners not unbound on `SHUTDOWN`, causing double-fires and stale values after restart.
- Debug UI ships as player UI.
