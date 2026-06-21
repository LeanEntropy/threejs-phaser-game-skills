# QA And Release Checklists

Use this before calling a Phaser 3 browser game complete, premium, release-ready, or fixed.

## Browser QA Matrix

Minimum meaningful QA:

- Dependencies installed or known.
- Build/typecheck passes (`npm run build` = `tsc && vite build`).
- Dev or preview server opened at the correct URL.
- Console/page/network errors captured.
- Canvas nonblank and visually varied through pixel sampling.
- Desktop active-play screenshot.
- Mobile active-play screenshot when mobile is in scope.
- Main input path changes game state.
- Objective/progress path works.
- Fail/retry or pause/resume path works when relevant.
- Recent or risky code paths triggered.
- Physics-heavy games: engine choice (Arcade vs Matter), body/group count, collider/overlap path, high-speed tunneling check, and restart body cleanup verified.
- HUD text fit, overlap, safe areas, and touch targets checked when UI changed.
- Renderer diagnostics captured when graphics complexity changed (FPS, active game objects, draw batches, particle/tween counts).
- Imported/generated asset paths, file sizes, and runtime load behavior checked when external assets changed (spritesheets, atlases, tilesets, audio).
- Audio unlock, decode/load, loop cleanup, mute/volume, and main SFX triggers checked when audio changed.

## Interaction QA

Test what a player actually does:

- Start or resume.
- Move/aim/steer/jump/attack/dash as appropriate.
- Collect or score.
- Avoid or hit a hazard.
- Trigger a state change: combo, wave, checkpoint, damage, shield, fail, win.
- Pause and resume (`this.scene.pause` / `this.scene.resume`, or a paused UI Scene).
- Restart after fail (`this.scene.restart`).
- For physics games, verify bodies reset cleanly after restart and no stale bodies, timers, tweens, or emitters keep running.
- For audio, verify user-gesture unlock, main SFX triggers, ambience loop start/stop, pause/resume, restart cleanup, and mute/volume controls.
- Resize or rotate when responsive/mobile is in scope.

Do not rely only on screenshots for gameplay changes.

## Visual QA

For premium/AAA/showcase or "less basic" requests:

- Capture active-play screenshot before and after when possible.
- Use the visual scorecard.
- Check for automatic failures:
  - primitive-dominant active screenshot (solid-color rectangles instead of sprites)
  - flat single-color background with no parallax or sky gradient
  - generic stat-card HUD
  - one repeated obstacle/reward sprite silhouette
  - vignette/glow/darkness hiding missing art
  - no renderer diagnostics
- Confirm UI and VFX do not obscure threats, rewards, player, or next decision.
- Confirm desktop and mobile framing both show the playable path (account for Scale.FIT letterboxing).
- For generated 2D assets, confirm spritesheets/atlases have correct frame slicing, pivot/origin, transparent backgrounds, consistent palette, and that animations play in active gameplay.

## Mobile QA

- Touch controls emit game intents (pointer events / on-screen buttons in a UI Scene).
- Pointer release/cancel/blur cannot leave controls stuck (`pointerup`, `pointerupoutside`, `pointercancel`, game blur).
- Safe areas respected (`env(safe-area-inset-*)` around the canvas parent).
- Touch targets reachable and separated.
- Page scroll does not steal gameplay input (touch-action / preventDefault on the canvas parent).
- Orientation/resize preserves canvas and HUD (Scale.FIT or RESIZE handled).
- DPR/performance acceptable.
- Desktop input still works unless intentionally removed.
- UI remains readable on narrow screens.

## Performance QA

When sprite counts, atlases, particles, pipelines/postFX, Lights2D, or physics changed:

- Record `this.game.loop.actualFps` / frame time if available.
- Record active game objects, draw batches, particle counts, active tweens, and active timers.
- Record physics engine, body count, collider/overlap count, active sensors, and known expensive bodies when physics changed.
- Note DPR cap, postFX/pipeline usage, and Lights2D usage.
- Check active gameplay, not only idle view.
- Compare before/after if performance work was requested.
- Report any unmeasured risk honestly.

## Release Checks

Before release-ready:

- Production build passes (`tsc && vite build`).
- Production preview/static server tested (`npm run preview` or equivalent).
- Vite `base` and asset URLs match target host (subpath hosting like GitHub Pages needs `base: '/repo/'`).
- Arcade debug (`physics.arcade.debug`) is `false`, `this.physics.world.drawDebug` off, no Matter debug rendering, no diagnostics/FPS overlays, no verbose logs, and no scene-skip/god-mode/test shortcuts in player-facing release.
- Bundle and large assets reviewed (atlases, tilesets, audio, fonts).
- API keys are not present in client-side code, checked-in files, built assets, or browser-visible environment.
- Public assets load under static hosting assumptions (relative/base-aware paths, correct case-sensitive filenames).
- Browser support assumptions documented (WebGL vs Canvas fallback with `Phaser.AUTO`).
- Deployment command or static artifact location reported.
- Residual risks listed.

## Evidence Format

```text
QA result: pass/fail
Commands:
URL:
Controls tested:
Screenshots/artifacts:
Console/page/network errors:
Canvas pixel check:
Desktop/mobile viewports:
Renderer/performance diagnostics:
Physics diagnostics:
External asset evidence:
Audio evidence:
Issues found/fixed:
Residual risks:
```

## Bug Report Format

```text
Title:
Severity:
Reproduction steps:
Expected:
Actual:
Browser/viewport/device:
Console/page errors:
Screenshot/artifact:
Likely owner:
Suggested fix:
```

## Common Release Failures

- Testing dev server but shipping untested production build.
- Static host base path breaks assets (`base` not set for subpath hosting).
- Arcade/Matter debug graphics or diagnostics overlay visible to players.
- Mobile UI passes screenshot but touch controls do not work.
- Canvas is nonblank but wrong app is running on the port.
- Physics gameplay looks right visually but colliders, overlap sensors, or restart cleanup were not tested.
- Screenshots are title/idle views instead of active play.
- Premium claim has no visual scorecard or renderer diagnostics.
- Sprite/image/audio generation API key or generated temporary URLs accidentally exposed in client code.
- Scene `shutdown` leaks (timers, tweens, emitters, or input listeners surviving a restart).
