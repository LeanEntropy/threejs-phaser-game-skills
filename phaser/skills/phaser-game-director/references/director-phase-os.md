# Director Phase OS

Use this reference only after `phaser-game-director` has attempted to load the relevant sibling public skill files and one or more files were unavailable. This file is the fallback operating system, not a reason to skip sibling skill loading.

## Non-Negotiable Rules

- Do not claim another public skill was invoked unless its `SKILL.md` was actually loaded or the runner explicitly invoked it.
- For broad game work, try to load all five sibling public skill files before implementation: gameplay systems, AAA graphics, UI designer, debug profiler, and QA release.
- When external 2D art would help, also try to load `phaser-sprite-generator`; when 2D concepts/backgrounds/UI art would help, also try to load `phaser-image-generator`; when SFX/ambience/voice would help, also try to load `phaser-audio-generator`.
- For premium/AAA/showcase/high-fidelity/less-basic work with vehicles, ships, characters, enemies, bosses, weapons, buildings, signature props, tilesets, skies/backgrounds, decals, logos, icons, GUI art, SFX, ambience, or voice, the relevant generator skill is an optional enhancement; procedural/local assets are a complete answer, so load a generator only when you want generated assets and the user is open to it.
- The director credential probe is optional and diagnostic; a missing key simply means use procedural/local assets. If you do report a key as a blocker, paste the literal SET/MISSING output.
- Record an external asset sourcing ledger before the graphics phase.
- Record sibling skill loading paths or failure reasons in the ledger.
- Load each phase's required reference files at phase entry. Do not defer references until final judgment.
- Record every required reference path or failure reason in the reference ledger.
- A phase cannot be marked `done` if its required references were skipped.
- A broad game request is not complete after a first playable slice when the user asked for premium, AAA, polished, showcase, complete, release-ready, or "less basic".
- Keep an execution ledger with phases, evidence, skipped work, and blockers.
- Prefer a small authored vertical slice over a larger placeholder scene.
- Treat flat colored rectangles, plain Graphics shapes, untextured tile grids, generic stat-card HUDs, and glow/vignette-only detail as prototype placeholders.
- Verify through browser evidence before calling the game done.

## External Asset Sourcing Gate

For broad or premium game work, fill this before the graphics phase:

```text
External asset sourcing:
- Credential probe output:
- Hero/player:
- Enemies/vehicles/weapons:
- Signature props/pickups:
- World/sky/background/tileset:
- Materials/textures/decals:
- Logos/icons/GUI art:
- Audio/SFX/voice:
- Chosen sources per surface: procedural / phaser-image-generator / phaser-sprite-generator / phaser-audio-generator / hybrid
- Sprite generator loaded: yes/no, path or blocker:
- Image generator loaded: yes/no, path or blocker:
- Audio generator loaded: yes/no/not-needed, path or blocker:
- External assets generated: yes/no, outputs or reason:
- Audio assets generated: yes/no/not-needed, outputs or reason:
```

Procedural/local/hand-made assets are always a valid, complete final answer; reach for a generator only as an opt-in enhancement when it would materially improve the result AND the user wants it. Common reasons procedural is the right default include:

- The user explicitly requested no external AI/assets or offline-only output.
- Credential probe output shows the relevant key is `MISSING` (procedural is the natural path; the probe is optional).
- A real API/network/quota error occurs after an attempted generation command; include the command and error summary.
- The surface is a repeated low-value prop better handled by batched/procedural Graphics kits.
- A non-hero repeated/support surface is already scoring 2+ and the ledger explains why external generation would not improve the active screenshot.
- Procedural craft already meets the visual bar — quality is judged on the result, not on whether a generator was used.

`not-needed` / `procedural` is always a valid ledger entry for any surface, with no generator loaded; record which approach was chosen, but choosing procedural needs no excuse.

For premium claims with hero surfaces such as player, enemy, boss, creature, vehicle, ship, weapon, building, tileset, or signature prop, procedural-only is perfectly acceptable; if the user wants higher fidelity, generating a hero/high-value asset is one optional route. When you do generate, note the evidence: a generated spritesheet/atlas path, a downloaded PNG/atlas JSON path, an image generator output path, or a documented hybrid chain. For premium active gameplay, audio is informational: if omitted, note it as a possible gap, but it is never a hard requirement and procedural/silent output is acceptable.

## Required References

Load these files before the matching phase starts:

- Gameplay systems: `phaser-gameplay-systems/references/gameplay-workflows.md`
- Physics selection, when physics/collision-heavy gameplay is in scope: `phaser-gameplay-systems/references/physics-engine-selection.md`
- New-game checklist, when creating a game or first playable slice: `phaser-gameplay-systems/references/checklists/new-game-definition-of-done.md`
- Genre premium checklist, when building or upgrading a platformer/top-down/arcade game: `phaser-gameplay-systems/references/checklists/platformer-premium-quality.md`
- AAA graphics: `phaser-aaa-graphics-builder/references/visual-scorecard.md`
- AAA graphics: `phaser-aaa-graphics-builder/references/implementation-blueprint.md`
- AAA graphics: `phaser-aaa-graphics-builder/references/sprite-recipes.md`
- AAA graphics: `phaser-aaa-graphics-builder/references/render-recipes.md`
- AAA graphics checklists, for premium/AAA/showcase claims: `phaser-aaa-graphics-builder/references/checklists/aaa-game-quality-gate.md` and `phaser-aaa-graphics-builder/references/checklists/aaa-visual-scorecard.md`
- UI: `phaser-game-ui-designer/references/ui-patterns.md`
- UI checklists, when UI/HUD/menu/touch layout is in scope: `phaser-game-ui-designer/references/checklists/game-ui-quality.md`, `phaser-game-ui-designer/references/checklists/hud-readability.md`, and `phaser-game-ui-designer/references/checklists/responsive-ui-fit.md`
- Debug/profile: `phaser-debug-profiler/references/debug-profile-checklists.md`
- Debug/profile checklists, when debugging or profiling: `phaser-debug-profiler/references/checklists/scene-debugging.md` or `phaser-debug-profiler/references/checklists/performance-profile.md`
- QA/release: `phaser-qa-release/references/qa-release-checklists.md`
- QA/release checklists, for final verification: `phaser-qa-release/references/checklists/visual-verification.md`, `phaser-qa-release/references/checklists/playtest-qa.md`, and `phaser-qa-release/references/checklists/release.md`
- Sprite generator, when loaded by the external asset sourcing gate: `phaser-sprite-generator/references/api-notes.md`
- Sprite generator, when loaded for a game: `phaser-sprite-generator/references/phaser-integration.md`
- Sprite plus image generator, when both are loaded: `phaser-sprite-generator/references/image-generator-workflows.md`
- Audio generator, when loaded for a game: `phaser-audio-generator/references/audio-workflows.md`

Try paths relative to the loaded skill directory first, then `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`, and finally repository `skills`.

## Phase Ledger Template

```text
Director: active
Sibling skill files loaded:
- Gameplay systems: yes/no, path or reason:
- AAA graphics: yes/no, path or reason:
- UI: yes/no, path or reason:
- Debug/profile: yes/no, path or reason:
- QA/release: yes/no, path or reason:
- Sprite generator: yes/no/not-needed, path or reason:
- Image generator: yes/no/not-needed, path or reason:
- Audio generator: yes/no/not-needed, path or reason:
External asset sourcing:
- Credential probe output:
- Hero/player source:
- Enemies/vehicles/weapons source:
- Signature props/pickups source:
- World/sky/background/tileset source:
- Materials/textures/decals source:
- Logos/icons/GUI art source:
- Audio/SFX/voice source:
- External assets generated or skip reason:
- Audio assets generated or skip reason:
Required references loaded:
- Gameplay workflows: yes/no/not-needed, path or reason:
- Physics engine selection: yes/no/not-needed, path or reason:
- Gameplay/new-game checklists: yes/no/not-needed, path or reason:
- Visual scorecard: yes/no/not-needed, path or reason:
- Graphics implementation blueprint: yes/no/not-needed, path or reason:
- Sprite recipes: yes/no/not-needed, path or reason:
- Render recipes: yes/no/not-needed, path or reason:
- Graphics checklists: yes/no/not-needed, path or reason:
- UI patterns: yes/no/not-needed, path or reason:
- UI checklists: yes/no/not-needed, path or reason:
- Debug/profile checklists: yes/no/not-needed, path or reason:
- QA/release checklists: yes/no/not-needed, path or reason:
- Sprite generator API notes: yes/no/not-needed, path or reason:
- Sprite generator Phaser integration: yes/no/not-needed, path or reason:
- Sprite/image generator workflows: yes/no/not-needed, path or reason:
- Audio workflows: yes/no/not-needed, path or reason:
Gameplay systems: pending/running/done/skipped - evidence:
External asset sourcing: pending/running/done/skipped - evidence:
AAA graphics: pending/running/done/skipped - evidence:
UI: pending/running/done/skipped - evidence:
Debug/profile: pending/running/done/skipped - evidence:
QA/release: pending/running/done/skipped - evidence:
```

Mark a phase `done` only after implementation plus verification. If a phase is skipped, state why it is out of scope or blocked.

## Phase 1: Discovery And Playable Contract

- Inspect package scripts, dependencies, app structure, `Phaser.Game` config, scene list (Boot/Preload/Play/UI), loop ownership (`update(time, delta)`), input, camera, UI, diagnostics, and existing screenshots.
- Define the one-sentence loop: player verb, objective, pressure, reward, fail state, restart.
- Define target devices and performance budget. If absent, assume desktop plus mobile browser, `Phaser.AUTO` (WebGL with Canvas fallback), `Scale.FIT` with capped resolution, and pointer-covers-touch input.
- Identify the highest-risk surfaces: blank/black canvas, no playable loop, weak controls, basic graphics, unreadable UI, or unverified release.

Exit evidence:

- Current scripts/dependencies known.
- Playable loop stated.
- Phase ledger initialized.

For a new project, use the gameplay skill's packaged scaffold creator:

```bash
python3 <phaser-gameplay-systems-skill-dir>/scripts/create_phaser_game.py ./my-game
```

## Phase 2: Gameplay Systems (Playable Loop)

Build or repair the playable loop before visual depth.

- Add `Phaser.Game` config, scenes, cameras, scale/resize handling, `update` loop, input intents, scene state machine, entities, collision or physics, scoring/progression, fail/retry, HUD state, audio/VFX hooks, and diagnostics.
- If the game is physics-heavy, load the physics selection reference and choose an engine explicitly: prefer **Arcade** (AABB, fast, deterministic) for platformers, top-down, runners, shooters, brick/breakout, and most arcade games; use **Matter** only when rotation, slopes, joints, stacking, or complex bodies are required.
- Keep ownership boundaries clear: `core`, `scenes`, `entities`, `systems`, `assets`, `ui`, `tests`.
- Tune movement, camera follow (`startFollow`, lerp, deadzone), zoom, acceleration, cooldowns, difficulty, and restart through short play loops.
- Keep physics bodies simpler than sprite art (size/offset the body, not the texture).
- Avoid multiple update sources, duplicated state, and per-frame allocations in hot paths; pool bullets/enemies/particles via Groups.

Exit evidence:

- Build/typecheck passes.
- Browser opens with nonblank canvas.
- Main control path changes state.
- Objective or score progresses.
- Fail/retry path exists when relevant.
- Physics engine choice, timestep/world settings, body/collider strategy, and `arcade.debug`/`matter.debug` diagnostics are reported when physics is in scope.
- New-game checklist outcome is reported for new games or first playable slices.

## Phase 3: External Asset Sourcing

Run before the premium graphics pass when trigger surfaces exist.

- Run the credential probe from the director skill scripts and paste output.
- Load `phaser-sprite-generator`, `phaser-image-generator`, and/or `phaser-audio-generator` when their trigger surfaces exist.
- Load sprite generator API notes, Phaser integration, image-generator workflow, and audio workflow references when relevant.
- Decide source per high-value surface: procedural / phaser-image-generator / phaser-sprite-generator / phaser-audio-generator / hybrid. Procedural is a complete, fully acceptable choice.
- Optionally generate high-value external outputs for premium hero surfaces when generated art would improve the result and the user wants it; procedural hero surfaces are acceptable.
- Record the chosen approach per surface, plus any generated spritesheet/atlas/tileset paths, atlas JSON paths, image generator output paths, or audio output paths when generation was used.

Exit evidence:

- Credential probe output.
- Skill/reference loading ledger for generator skills (only when generation is used).
- Asset sourcing ledger (records the choice: procedural or generated).
- When generation was used, the external output paths. Procedural/local art needs none.

## Phase 4: AAA Graphics / Art

Use when screenshots look basic or the user asks for premium quality.

- Score active-play screenshot across art direction, hero/player, obstacles/enemies, rewards/interactables, world/environment, materials/textures, lighting/render, VFX/motion, UI/HUD, and performance evidence.
- Add production graphics architecture: texture-atlas/spritesheet plan, generated-texture (Graphics → `generateTexture`) library, decals, sprite factories, parallax background layers (`tileSprite`), particle/VFX system, pipeline/postFX and Lights2D plan, diagnostics.
- Upgrade all visible surfaces, not only the player: hero, hazards, rewards, ground/tiles/arena, foreground props, parallax background layers, interactable telegraphs, palette/material variation, and state VFX.
- Use `phaser-image-generator` for concept/reference images, background/sky plates, parallax layers, logos, icons, decals, and source frames for the sprite generator when 2D source art would improve quality.
- Use `phaser-sprite-generator` for high-value 2D art such as characters, enemies, bosses, vehicles, buildings, weapons, hero props, pickups, tilesets, spritesheets, and texture atlases when procedural Graphics code is not enough.
- Use `phaser-audio-generator` for SFX, ambience loops, UI sounds, voice, conversion, and cleanup when generated audio would improve the playable loop.
- If trigger surfaces exist, record the asset-sourcing choice per surface; procedural code is a complete answer, and a generator is an optional enhancement when the user wants higher fidelity.
- Build authored forms: layered sprites, animation frames (squash & stretch, anticipation), tint/blend variation, trim/panel detail, decals, parallax depth, particle emitters, and physics-body footprints that stay simple.
- Add pipelines/postFX (`addBloom`, `addGlow`, `addVignette`, custom `PostFXPipeline`), Lights2D + normal maps, color grading, and screen-space juice only after the authored forms exist.

Exit evidence:

- Before/after scorecard.
- Filled categories from `visual-scorecard.md`: Art direction, Hero/player, Obstacles/enemies, Rewards/interactables, World/environment, Materials/textures, Lighting/render, VFX/motion, UI/HUD, Performance evidence.
- Average score and automatic failures remaining.
- Active desktop and mobile screenshots.
- Renderer diagnostics: draw calls (batches), active game objects, textures/atlases, particle count, active tweens, and `actualFps` when possible.
- Imported asset diagnostics when generated art was used: spritesheet/atlas/tileset paths, file size, frame dimensions/count, animation keys, and texture/atlas memory when possible.
- No scorecard category below 2 for premium claims.

## Phase 5: UI

Use when HUD/menu/interface craft affects quality or readability.

- Inventory gameplay, pause, settings, fail/retry, milestone/win, loading/error, and touch states.
- Run the HUD in a parallel UI Scene (`this.scene.launch('UI')`) with `setScrollFactor(0)` so it does not move with the camera.
- Replace utility stat-card grids with game-specific meters, compact clusters, icons, badges, alerts, cooldown rings, reticles, diegetic labels, and stateful overlays.
- Use stable dimensions, safe-area padding (`env(safe-area-inset-*)` around the canvas parent), fixed-width numeric fields, text fit, and responsive constraints across `Scale.FIT`.
- Wire UI to game state via scene events/registry. Avoid duplicated game rules inside UI code.
- Ensure UI never blocks the player, threats, pickups, next decision, or critical on-screen touch controls.

Exit evidence:

- Desktop and mobile screenshots for relevant states.
- Text-fit and overlap check.
- Touch target and safe-area check when mobile is in scope.
- UI checklist outcomes are reported.

## Phase 6: Debug And Profile

Use whenever the canvas is blank/black, interaction fails, mobile behavior breaks, or visual changes add cost.

- Reproduce locally and read console/page/network errors.
- Check canvas CSS size and drawing-buffer size, `Phaser.Game` type/context, scene list and `update` ownership, camera bounds/zoom/scroll, `Scale` mode, loader keys/paths (404s), texture/atlas/tilemap keys, depth/visibility, and resize behavior.
- For performance, measure production preview where possible: FPS/frame time (`game.loop.actualFps`), draw calls (batches), active game objects, textures/atlases, particle/tween counts, physics body count, memory, and bundle size.
- Optimize one bottleneck at a time using atlases/batching, object pooling (Groups), culling/`setVisible`, capped particle counts, capped resolution/DPR, cheaper postFX, and explicit cleanup (`scene.shutdown`/`destroy`, `textures.remove`, emitter/tween/timer teardown).
- Use the Arcade debug graphic (`arcade.debug = true`) or `this.physics.world.drawDebug` / Matter debug to inspect bodies.

Exit evidence:

- Root cause or measured bottleneck stated.
- Baseline/post metrics when optimizing.
- Broken path retested.

## Phase 7: QA And Release

Use before calling broad work complete.

- Run build/typecheck.
- Start dev or preview server and open the correct URL.
- Check console/page/network errors.
- Capture active desktop and mobile screenshots.
- Sample canvas pixels for nonblank and varied output.
- Use the generated game's `npm run inspect:canvas` when available, or the QA skill's packaged inspector:

```bash
node <phaser-qa-release-skill-dir>/scripts/inspect-phaser-canvas.mjs --url http://127.0.0.1:5188
```

- Trigger main input, objective progression, fail/retry, and recent risky paths.
- Verify HUD text fit, safe areas, touch targets, resize/`Scale.FIT`, and mobile input (pointer/touch unlock of audio on first input).
- For release, verify production preview, base path (`vite base`), static assets/atlas/tilemap paths, debug gating (`arcade.debug` off), bundle/large assets, and deployment assumptions.

Exit evidence:

- Commands run and pass/fail.
- URL used.
- Screenshots/artifact paths.
- Issues fixed or listed with likely owners.
- Residual risks.

## Completion Gate

For premium/AAA/showcase claims, all of these must be true:

- Skill-loading ledger and reference ledger are present.
- External asset sourcing ledger is present for premium/AAA/showcase graphics work.
- The asset-sourcing decision (procedural or generated) is recorded; generated surfaces include their output paths. Procedural/local art is fully acceptable and needs no probe output or blocker evidence.
- Playable loop works through real input.
- Active-play screenshots exist for desktop and mobile.
- Visual scorecard has no category below 2 and average is at least 2.3.
- Visual scorecard uses the authored rubric, not an improvised rubric.
- HUD/menu states are readable and responsive.
- Renderer diagnostics exist after graphics changes.
- Build and browser QA passed or blockers are clearly reported.
- Physics-heavy games include engine choice, world/timestep settings, body/collider strategy, sensors/overlaps, and body/collider diagnostics.

If any gate fails, continue iterating or report the exact blocker instead of calling the game premium.
