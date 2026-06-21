---
name: phaser-debug-profiler
description: "Debug and profile Phaser 3 (2D) browser games. Combines scene/lifecycle debugging, blank-canvas/render/runtime/loader/animation/tween/resize/Scale-Manager/mobile-touch fixes, performance profiling, actualFps, draw calls (batches), active game objects, physics body counts, particle/tween/timer counts, texture & atlas memory, overdraw, and pipeline/postFX cost. For platformer, top-down, arcade, shoot-em-up, roguelike, and sprite/tilemap games."
---

# Phaser Debug Profiler

## Purpose

Find root causes and optimize measured bottlenecks without breaking playability.

## Debug Workflow

Load `references/debug-profile-checklists.md` as the first action when debugging render/runtime/mobile issues, asset loading, audio loading/playback, animation/tween, resize/Scale-Manager, input/touch, blank or black canvas, physics/collision bugs, scene-lifecycle leaks, or profiling performance. Track it in a reference ledger with yes/no, path, and failure reason. Do not mark the debug/profile phase complete while this reference is skipped for debug or profiling work.

Load `references/checklists/scene-debugging.md` for render/runtime bug diagnosis, `references/checklists/performance-profile.md` for profiling work, and `references/checklists/mobile-input.md` for mobile render/touch issues. Load `references/prompt-templates.md` only when the user asks for reusable debug/profile prompts or a task template.

1. Reproduce locally.
2. Read console/page/network errors and `this.load.on('loaderror')` events.
3. Check canvas display size, Scale Manager mode/size, and `Phaser.Game` renderer (`game.renderer`, AUTO/WEBGL/CANVAS).
4. Check game/scene ownership: one `Phaser.Game`, scene started/active, no duplicate scene instances.
5. Check camera bounds/zoom/scroll/visibility, object depth, alpha, tint, blend mode, texture key existence, and display-list membership.
6. Check asset keys/paths/CORS/Vite base path and loader completion before `create()` uses keys.
7. Check delta units in `update(time, delta)`, physics/update order, Arcade vs Matter body ownership, input/pointer listeners, touch behavior, resize handling, and audio context unlock/decode errors when audio is involved.
8. Fix root cause in owning module/scene.
9. Verify browser screenshot, nonblank canvas, console/page errors, and broken path.

## Performance Workflow

1. Reproduce in correct build mode (production preview, not dev server).
2. Record baseline: `this.game.loop.actualFps`/frame time, draw calls (batches), active game objects, physics body count, particle/tween/timer counts, texture & atlas memory, bundle size.
3. Identify CPU/GPU/memory/network bottleneck.
4. Optimize one thing at a time: texture atlases, sprite batching, object pooling (Groups), culling/`setVisible`, DPR/zoom discipline, cheaper postFX/pipelines, particle/emitter limits, fewer dynamic bodies.
5. Re-measure same scenario and verify visuals/playability.

## Final Response

Lead with root cause or bottleneck. Report the reference ledger, checklist items used, files changed, baseline/post metrics, commands, screenshots/artifacts, broken paths retested, and residual risks.
