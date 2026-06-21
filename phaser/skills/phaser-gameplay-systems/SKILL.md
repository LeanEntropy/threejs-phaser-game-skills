---
name: phaser-gameplay-systems
description: "Build and iterate playable Phaser 3 game systems. Combines starter scaffold creation, architecture, gameplay implementation, and game-feel tuning. Use for first playable slices, new Vite/TypeScript/Phaser game setup, 2D platformers, top-down arenas, shoot-em-ups, runners, roguelikes, scenes, game loops, sprites/groups/pooling, input, Arcade/Matter collision, scoring, objectives, audio hooks, camera follow, tilemaps, tweens/timers, difficulty, feedback, and maintainable structure."
---

# Phaser Gameplay Systems

## Purpose

Create or evolve a playable browser game loop with clear ownership, responsive controls, deterministic update order, and verified player-facing behavior.

## Use When

Starting a new game, repairing a weak prototype, adding mechanics/entities, designing architecture, tuning camera/controls, implementing rules/objectives, or improving game feel.

## Workflow

Load `references/gameplay-workflows.md` as the first action when the task includes first playable setup, architecture, mechanics, entities, input, camera, collision/physics, scoring, objectives, feedback, or feel tuning.

Load `references/physics-engine-selection.md` before adding or changing physics, collision-heavy gameplay, platforming, top-down movement, projectiles, moving platforms, sensors/overlaps, rolling/rotating bodies, ragdolls, stacking crates, slopes, or physics QA. Track both references in a reference ledger with yes/no, path, and failure reason. Do not mark the gameplay phase complete while a required reference is skipped.

Load `references/checklists/new-game-definition-of-done.md` before claiming a new game or first playable slice is complete.

Load `references/checklists/top-down-arena-premium-quality.md` for top-down arena, twin-stick, survivor, or arena-shooter work.

Load `references/prompt-templates.md` only when the user asks for reusable prompts, starter prompts, or a task template.

Load `phaser-audio-generator` when implementing real SFX, ambience, UI sounds, voice/TTS, or audio cleanup beyond simple placeholder hooks. Gameplay code should emit audio events; the audio skill should generate or process the actual assets and define the runtime audio matrix.

1. Inspect project structure, scripts, dependencies, current scenes, loop, input, camera, entities, state, UI, and diagnostics.
2. Define the one-sentence playable loop: verb, objective, feedback, fail/retry.
3. Choose small architecture boundaries: scenes (`Boot`, `Preload`, `Play`, `UI`), `entities`, `systems`, `assets`, `config/tuning`, `tests`.
4. Implement mechanics in playable increments: input, state, entity, collision/overlap, feedback, HUD/audio hook, diagnostics.
5. Tune feel: movement, acceleration, camera follow/zoom/shake, impact, cooldowns, difficulty, restart loop.
6. Keep hot paths allocation-light (object pools, reused vectors) and update order explicit.
7. Verify with build, browser, screenshot, canvas pixels, console/page errors, and one real input path.

## Packaged Scaffold

Use the bundled scaffold when starting a new project or when the user asks for a starter game:

```bash
python3 <this-skill-dir>/scripts/create_phaser_game.py ./my-game
```

The script copies `assets/phaser-vite-game/`, rewrites the project name in `package.json` and `package-lock.json`, and keeps generated games self-contained with their own visual test and canvas-inspection script. Use `--force` only when the target directory may be overwritten.

## Library Guidance

- Use TypeScript, Vite, and Phaser 3 (`type: Phaser.AUTO`).
- Arcade Physics is the default for platformers, top-down, runners, shooters, and most arcade games (fast AABB, deterministic).
- Use `this.physics.add.collider`/`overlap` for interactions and `physics.add.group`/`staticGroup` for entity collections.
- Use Matter.js only when Arcade's AABB model is insufficient: rotation, slopes, joints, stacking, complex compound shapes.
- Use custom checks (distance, rectangle intersection) when authored arcade feel beats simulation.
- Tweens, the time/event system, and `Phaser.Math` cover most procedural feel; avoid ad-hoc math and `setTimeout`.
- Web Audio via `this.load.audio`/`this.sound` for runtime playback; `phaser-audio-generator` for generated game audio assets.

## Common Failure Modes

- Static demo instead of playable loop.
- Mechanic compiles but cannot be triggered by real input.
- Camera/controls feel delayed or hide the next decision.
- State changes do not drive UI/audio/VFX.
- Architecture abstractions appear before mechanics need them.

## Final Response

Report the reference ledger, gameplay checklist outcome, behavior, controls, changed files, architecture choices, tuned values, verification evidence, artifacts, and remaining edge cases.
