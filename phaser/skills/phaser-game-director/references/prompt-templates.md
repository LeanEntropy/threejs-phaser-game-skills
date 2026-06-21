# Phaser Game Director Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# New Phaser Game Prompt

Use `phaser-game-director` for a complete or premium Phaser 3 browser game. It should automatically route through gameplay systems, AAA graphics, UI, debug/profile, and QA/release phases.

Use `phaser-gameplay-systems` directly only when the requested output is explicitly a small first prototype or gameplay-system change.

Game idea:
- Core verb:
- Genre (platformer / top-down / arcade / shmup / roguelike / breakout / puzzle):
- Objective:
- Camera (fixed / follow / zoom):
- Visual tone:
- Target devices:
- Time budget:

Requirements:
- Use TypeScript, Vite, and Phaser 3 modules.
- Build a playable loop, not a static scene.
- Use scenes (Boot/Preload/Play/UI) and a clear `update(time, delta)` loop.
- Choose Arcade physics by default; use Matter only if rotation/slopes/joints/stacking are required.
- Keep the first version small enough to verify quickly, then continue quality passes if the target is complete/premium.
- Include desktop keyboard input and mobile touch/pointer input when target devices include mobile.
- Add HUD feedback (in a parallel UI Scene) for objective, score, health, time, or state.
- For premium requests, replace prototype HUD/Graphics shapes/world detail with designed UI, spritesheet/atlas/tileset kits, parallax, particles, and renderer diagnostics.
- Run build and visual verification before reporting done.

Final response:
- list files created or changed
- describe playable controls
- report build, browser, console, screenshot, canvas-pixel, and viewport evidence
- list remaining risks

---

# AAA Phaser Game Pass Prompt

Use `phaser-game-director` to upgrade this Phaser 3 browser game from prototype-quality to premium showcase quality.

Target:
- Genre:
- Core verb:
- Desired mood:
- Target devices:
- Performance budget:

Automatic skill flow:
- Use the director's active-play screenshot scorecard first if screenshots exist or can be captured.
- Use `phaser-aaa-graphics-builder` when screenshots still look basic or when multiple graphics surfaces are weak.
- Use `phaser-game-ui-designer` for HUD, menus, overlays, icons, text fit, and touch UI.
- Use `phaser-gameplay-systems` for speed, controls, camera, impact, difficulty, and restart loop.
- Use `phaser-debug-profiler` before and after expensive visual changes.
- Use `phaser-qa-release` before calling the pass complete.

Quality priorities:
- Prefer a smaller authored vertical slice over a larger placeholder game.
- Replace utility HUD boxes with designed, genre-specific interface states.
- Replace placeholder Graphics shapes with authored sprites, animation frames, and reusable atlas/tileset kits.
- Build a minimum premium asset set: hero/player, three obstacle/enemy variants, two reward/interactable variants, world/tileset prop kit, and a palette/material kit.
- Add depth layers, parallax, foreground/midground/background composition, and color/material contrast.
- Make rewards, threats, player state, and objectives readable during motion.
- Add feedback for movement, pickup, near miss, hit, fail, restart, streak, and milestone (tweens, particles, screen shake, hit-stop, flash).
- Keep render cost visible through renderer diagnostics.

Prototype rejection tests:
- Main world is mostly flat colored rectangles or plain Graphics shapes.
- Player/hero asset is a single static sprite or primitive with glow.
- Obstacles/pickups are one repeated silhouette.
- HUD is mostly rectangular stat cards.
- Vignette/darkness/bloom hides missing art.

Verification:
- Build and run locally.
- Capture desktop and mobile screenshots after interaction.
- Check console/page errors and nonblank canvas pixels.
- Check UI text fit, overlap, safe areas, and touch targets.
- Report draw calls (batches), active game objects, textures/atlases, particle/tween counts, and frame-time/FPS evidence when available.
- Compare against `phaser-aaa-graphics-builder/references/checklists/aaa-game-quality-gate.md`.
- Compare against `phaser-aaa-graphics-builder/references/checklists/aaa-visual-scorecard.md`.
- Do not report the task as premium-complete if any prototype rejection test still fails.

---

# Premium Platformer Pass Prompt

Use `phaser-game-director` to upgrade this platformer (or top-down/arcade game) into a premium, high-fidelity browser game.

Current blockers:
- 

Genre-specific targets:
- Player avatar silhouette and animation set (idle/run/jump/fall/land/hurt):
- Enemy families:
- Reward/readability language:
- World theme and tileset:
- Movement/impact feel (jump arc, coyote time, jump buffer, acceleration):
- HUD states:

Required upgrades:
- Replace simple stat-card HUDs with a genre-specific HUD: compact status, readable progress, health/hearts, combo/streak, fail/retry, pause/settings, in a parallel UI Scene.
- Replace placeholder rectangles and basic pickups with distinct spritesheet/atlas families that read instantly during motion.
- Build at least three enemy families, two reward variants, one detailed animated player, and one reusable tileset/world prop kit.
- Add level/tile detail, near-field props, mid-field silhouettes, far parallax (`tileSprite` layers), and motion cues that do not hide hazards.
- Improve player avatar detail: layered sprite, animation states, squash & stretch, emissive/flash signals, dust/land particles, trail, and a readable physics-body footprint.
- Add hazard telegraphing, pickup magnet/collect feedback, near-miss feedback, difficulty ramp cues, checkpoint/milestone gates, and death/retry polish (camera shake, hit-stop, flash).
- Tune camera follow lag, deadzone, zoom, shake, and effects for readability without disorientation.

Avoid:
- Large untextured tile grids as the main world detail.
- Glow/postFX as the only fidelity technique.
- HUD panels that look like debug readouts.
- Repeating the same enemy/tile silhouette too frequently.
- Effects that obscure the next platform or hazard decision.

Verification:
- Use `phaser-gameplay-systems/references/checklists/platformer-premium-quality.md`.
- Capture desktop and mobile screenshots during action, not only idle.
- Report renderer diagnostics for the worst-case visible screen (most sprites/particles).
- Play long enough to see the difficulty ramp, pickups, hazards, fail/retry, and any power/boost state.
- If the screenshot still reads as a tile grid plus rectangles plus basic pickups, continue art/world/UI passes instead of reporting done.
