# Game UI Quality Checklist (Phaser 3)

- The first screen is the playable game or a deliberate modal/menu scene, not a landing page.
- HUD hierarchy matches gameplay priority: survival/status, objective, feedback, secondary flavor.
- UI visual language matches the game's genre, tilesets, palette, tint, and motion (tweens/particles).
- The rendering surface was chosen deliberately: parallel UI Scene for in-canvas/juicy HUD, DOM overlay for crisp text / forms / accessibility / safe areas.
- Menus include expected states: pause, resume, restart, settings, win/lose when relevant, modeled as overlay Scenes or pinned containers.
- Buttons and controls have stable dimensions plus idle, hover, pressed, focus, and disabled states (`setInteractive` + pointer events, or DOM states).
- Icons are used for compact tools/actions when recognizable; ambiguous icons have labels or tooltips.
- UI does not use nested cards, marketing-page layout, or generic dashboard styling.
- HUD is pinned with `setScrollFactor(0)` (or lives in a UI Scene) so it does not scroll or zoom with the world camera.
- UI does not block player, threats, goals, interactables, or near-future path unless intentionally modal.
- Dynamic values such as score, time, health, combo, and ammo do not shift layout (reserved width / BitmapText box).
- BitmapText is used for fast-changing numbers; Text/DOM for richly styled or localized copy; web fonts are loaded before use.
- Reduced-motion and flash risk is considered for intense UI animation, bloom/glow, or damage feedback.
- UI state is driven by the registry/event model and does not duplicate simulation rules.
- Listeners are unbound on `SHUTDOWN` and state is reset in `create`, so values are correct after restart.
- Desktop and mobile screenshots show coherent composition and no clipped or overlapping controls.
