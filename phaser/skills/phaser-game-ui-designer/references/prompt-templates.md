# Phaser Game UI Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# Premium HUD/UI Pass Prompt

Use `phaser-game-ui-designer` to make this Phaser 3 game's HUD and in-game UI feel premium, readable, and genre-specific.

Context to gather:
- Current screenshots at desktop and mobile sizes.
- Game genre, core verb, target mood, and player decisions the HUD must support.
- Current HUD/menu code, scene structure, game state sources (registry/events), input model, and touch controls.
- Current Scale Manager mode and design resolution.

Design goals:
- Keep the playable game as the first screen.
- Make survival/status/objective information readable during motion, pinned with `setScrollFactor(0)` or in a parallel UI Scene.
- Use stable dimensions for counters, buttons, meters, and labels.
- Use BitmapText for fast-changing numbers and Text/DOM for richly styled or localized copy.
- Use icons where they reduce clutter, with labels where meaning is ambiguous.
- Match the game's tilesets, palette, tint language, typography, and feedback (tweens/particles).

Constraints:
- Do not add marketing-page hero sections or explanatory feature copy.
- Do not nest cards inside cards.
- Do not let UI cover critical gameplay at desktop or mobile sizes.
- Do not parent HUD to the world camera (no scroll/zoom drift).
- Avoid text overflow, clipped controls, layout shift, and generic dashboard styling.

Verification:
- Build and run locally.
- Capture desktop and mobile screenshots.
- Check console/page errors after UI events and after scene restart.
- Verify text fit, no overlap, no clipped controls, and at least one UI state change from real input (the intent fires, not just the visual).

---

# Responsive Game Menu Pass Prompt

Use `phaser-game-ui-designer` to design or improve this Phaser 3 game's pause, start, settings, win, lose, or restart menus.

Menu states needed:
- 

Target devices/orientations:
- 

Surface and scaling decisions to make first:
- UI Scene (in-canvas) vs DOM overlay for each menu (settings forms usually favor DOM).
- Scale Manager mode (FIT / RESIZE / ENVELOP) and design resolution, plus a `this.scale.on('resize', ...)` handler for RESIZE.

Requirements:
- Menus must feel like part of the game, not a website overlay.
- Modal menus should pause or dim gameplay (`this.scene.pause('Play')` + a scrim rectangle), not look like marketing cards.
- Buttons need clear idle, hover, pressed, focus, disabled, and touch states (`setInteractive` + pointer events, or DOM `:hover/:active/:disabled`).
- Settings must use appropriate controls: toggles, sliders, segmented controls, icon buttons, and selects (DOM overlay is usually best for forms).
- Layout must respect safe-area insets (`env(safe-area-inset-*)` on the canvas parent / DOM overlay) and remain usable on mobile.

Implementation notes:
- Prefer overlay Scenes (`this.scene.launch('Pause')`) or pinned containers for modal states.
- Keep UI state driven by the registry/event model; reset it in `create` and unbind listeners on `SHUTDOWN`.
- Keep dimensions stable so labels and counters do not shift layout.
- Use nineslice panels so borders stay crisp when a panel resizes.

Verification:
- Test every menu state.
- Capture desktop and mobile screenshots.
- Check keyboard/gamepad and touch paths when supported.
- Confirm no text overflow, overlap, clipping, or offscreen/unreachable controls at every supported aspect ratio.
