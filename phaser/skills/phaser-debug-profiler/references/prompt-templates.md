# Phaser Debug/Profile Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# Mobile Input Prompt

Use `phaser-debug-profiler` for mobile render/touch bugs, or `phaser-game-ui-designer` when the main issue is touch-control/HUD layout.

Target devices:
- 

Current issue:
- 

Requirements:
- Use pointer/touch handling that does not fight page scrolling (`touch-action`, multi-touch via `this.input.addPointer`).
- Keep HUD and on-screen controls inside safe areas.
- Verify portrait and landscape if both are supported, including `this.scale.on('resize', ...)` repositioning.
- Check canvas sizing, Scale Manager mode, zoom/DPR, hit target sizes, `setInteractive` hit areas, and virtual controls.
- Verify pointer up/out/cancel release paths so held controls let go when the finger leaves.
- Use Playwright mobile emulation and, when available, a real device smoke test.

---

# Performance Pass Prompt

Use `phaser-debug-profiler` to profile and improve this game.

Target device or budget:
- FPS/frame-time target:
- Target viewport:
- Known bottleneck:

Measure:
- `this.game.loop.actualFps` and frame time
- draw calls (batches)
- active game objects and group active counts
- physics body count (Arcade or Matter)
- particle counts and active emitters
- active tweens and timers
- texture & atlas count, dimensions, and memory
- bundle size
- resource cleanup behavior during scene transitions (timers/tweens/emitters/listeners)

Implement only changes justified by measurements, then rerun the same checks.

---

# Scene Debug Prompt

Use `phaser-debug-profiler` to diagnose this Phaser 3 issue:

Symptom:
- Blank/black canvas, frozen frame, bad resize, asset/loader failure, bad animation/tween timing, collision issue, scene-lifecycle leak, or mobile touch problem:

Recent changes:
- 

Expected behavior:
- 

Debugging requirements:
- Reproduce locally.
- Inspect console, page errors, and `this.load.on('loaderror')` events.
- Check canvas size, Scale Manager mode/parent, `game.renderer` creation, scene started/active, camera bounds/zoom, texture key existence, object depth/alpha/visibility, asset paths, async load completion before use, and that exactly one update loop runs.
- Check scene-shutdown cleanup for timers, tweens, emitters, and global/registry listeners.
- Make the smallest fix that addresses the root cause.
- Verify with a browser screenshot and canvas-pixel sample.
