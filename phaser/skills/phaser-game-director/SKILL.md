---
name: phaser-game-director
description: "Primary entrypoint for complete Phaser 3 (2D) browser game creation, premium iteration, and automatic phase orchestration. Use by default for build-a-game, upgrade, polish, premium, AAA, high-fidelity, from-scratch, platformer, top-down, arcade, action, shoot-em-up, shmup, roguelike, brick/breakout, runner, puzzle, release-ready, or showcase requests. For broad work, first load sibling public skill files for gameplay systems, AAA graphics, UI, debug/profile, and QA/release. For premium games with characters, enemies, bosses, vehicles, ships, weapons, tilesets, signature props, backgrounds, skies, decals, logos, icons, GUI art, audio/SFX/voice needs, or less-basic graphics, phaser-sprite-generator, phaser-image-generator, and/or phaser-audio-generator are optional enhancements you can reach for when generated assets would materially improve the result and the user wants them; procedural/local/hand-made assets are always a complete, fully acceptable answer. Keep skill-loading, reference, asset-sourcing, and phase-execution ledgers so users do not choose skills manually."
---

# Phaser Game Director

## Purpose

Own the end-to-end game outcome. Build the playable loop, route through the right phases, verify evidence, and do not call prototype-quality work premium.

## Claude Compatibility Rule

Claude-style skill runners may invoke only this skill when the user runs `/phaser-game-director`. Do not claim other skills were invoked unless the runner actually invoked them. For broad work, you must still try to load the sibling public `SKILL.md` files with filesystem read tools before planning or editing, then load each phase's required reference files before that phase starts. If a sibling `SKILL.md` cannot be loaded, then use `references/director-phase-os.md` as the fallback for that phase and record the failure.

## Mandatory Sibling Skill Loading

For complete, premium, AAA, polished, high-fidelity, showcase, from-scratch, upgrade, or release-ready game work, load these sibling skill files before implementation:

- `phaser-gameplay-systems/SKILL.md`
- `phaser-aaa-graphics-builder/SKILL.md`
- `phaser-game-ui-designer/SKILL.md`
- `phaser-debug-profiler/SKILL.md`
- `phaser-qa-release/SKILL.md`

For premium, AAA, high-fidelity, showcase, complete, release-ready, or "less basic" game work, this skill is an optional enhancement when the game includes or should include high-value 2D art assets: generated spritesheets, animation frame sets, texture atlases, tilesets, characters, enemies, bosses, buildings, vehicles, ships, weapons, signature props, complex pickups, or hero environment tiles. Procedural Phaser Graphics is a complete answer; optionally load this skill if you want generated art and the user is open to it:

- `phaser-sprite-generator/SKILL.md`

For premium, AAA, high-fidelity, showcase, complete, release-ready, or "less basic" game work, this skill is an optional enhancement when the game includes or should include concept/reference images, sprite-sheet sources, tileset sources, skies/backgrounds, parallax plates, logos, marks, icons, decals, GUI art, title/menu art, or 2D images that feed the sprite generator. Procedural/local art is a complete answer; optionally load this skill if you want generated images and the user is open to it:

- `phaser-image-generator/SKILL.md`

For premium, AAA, high-fidelity, showcase, complete, release-ready, or "less basic" game work, this skill is an optional enhancement when the game includes or should include SFX, ambience, UI sounds, interaction audio, vehicle/weapon/boss sounds, announcer/dialogue, scratch-performance voice conversion, or audio cleanup. Optionally load this skill if you want generated audio and the user is open to it:

- `phaser-audio-generator/SKILL.md`

Try paths in this order:

1. Sibling installed path: `../<skill-name>/SKILL.md`
2. Claude default path: `~/.claude/skills/<skill-name>/SKILL.md`
3. Codex default path: `~/.codex/skills/<skill-name>/SKILL.md`
4. General agents path: `~/.agents/skills/<skill-name>/SKILL.md`
5. Repository source path: `skills/<skill-name>/SKILL.md`

If the file-read tool requires absolute paths, expand `~` to the user's home directory before reading.

For narrow director-invoked work, load the directly relevant sibling skill and `phaser-qa-release`. For broad game creation or premium iteration, load all five. Do not skip sibling loading just because this director contains a summarized phase OS.

## External Asset Sourcing Gate

Do not decide "sprite generator not needed", "image generator not needed", or "audio generator not needed" before loading the relevant skill files when the trigger categories above are present.

Before claiming an API key is unavailable, run the credential probe and paste its literal output in the report:

```bash
bash <director-skill-dir>/scripts/probe_asset_credentials.sh
```

Expected output shape:

```text
GEMINI_API_KEY=SET|MISSING
OPENAI_API_KEY=SET|MISSING
ELEVENLABS_API_KEY=SET|MISSING
```

The probe sources the user's shell profiles and also checks the config file (`$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`), printing only SET/MISSING markers, never secret values. Image generation can use OpenAI (`gpt-image-1`) or Gemini, so either `OPENAI_API_KEY` or `GEMINI_API_KEY` being SET enables image/sprite generation if you opt into it. The probe is an optional diagnostic, not a gate: a missing key simply means use procedural/local assets, which is a complete answer. If you do report a key as a blocker, show this probe output so the report is accurate.

For broad or premium game work, create an asset sourcing ledger before the graphics phase:

```text
External asset sourcing:
- Credential probe output:
- Hero/player:
- Enemies/vehicles/weapons:
- Signature props/pickups:
- World/sky/background/tileset:
- Materials/textures/decals:
- Logos/icons/GUI art:
- Chosen sources per surface: procedural / phaser-image-generator / phaser-sprite-generator / hybrid
- Sprite generator loaded: yes/no, path or blocker:
- Image generator loaded: yes/no, path or blocker:
- Audio generator loaded: yes/no/not-needed, path or blocker:
- External assets generated: yes/no, outputs or reason:
- Audio assets generated: yes/no/not-needed, outputs or reason:
```

Procedural/local/hand-made assets are always a valid, complete final answer for any surface — no generator needs to be loaded or attempted to justify that choice. Reach for a generator only as an opt-in enhancement when it would materially improve the result AND the user wants it. Common reasons procedural is the right default include:

- The user explicitly requested no external AI/assets or offline-only output.
- Credential probe output shows the relevant key is `MISSING` (procedural is the natural path; the probe is optional).
- A real API/network/quota error occurs after an attempted generation command; include the command and error summary.
- The surface is a repeated low-value prop better handled by batched/procedural Graphics kits.
- A non-hero repeated/support surface is already scoring 2+ in the visual scorecard and the asset sourcing ledger explains why external generation would not improve the active screenshot.
- Procedural craft already meets the visual bar — quality is judged on the result, not on whether a generator was used.

`not-needed` / `procedural` is always a valid ledger entry, for any surface, with no generator loaded — record which approach was chosen and why, but choosing procedural needs no excuse. For premium claims, a generator is one optional route to higher fidelity; use `phaser-image-generator`, `phaser-sprite-generator`, or a documented hybrid only when you want generated art and it would improve the active screenshot.

For premium claims with hero surfaces such as player, enemy, boss, creature, vehicle, ship, weapon, building, tileset, or signature prop, procedural-only is perfectly acceptable; if the user wants higher fidelity, generating a hero/high-value asset is one optional route. When you do generate, note the evidence in the report: a generated spritesheet/atlas path, a downloaded PNG/atlas JSON path, an image generator output path, or a documented hybrid chain. For premium claims that include active gameplay, audio is informational: if omitted, note it as a possible gap, but it is never a hard requirement and procedural/silent output is acceptable.

## Mandatory Reference Gate

References are not optional enrichment. They are phase-entry gates. For broad game creation, premium/AAA/showcase/polish requests, release-ready work, or any task that claims high visual quality, load the applicable reference files before implementation in that phase.

Required phase references:

- Gameplay systems: `phaser-gameplay-systems/references/gameplay-workflows.md`
- Physics selection, when physics/collision-heavy gameplay is in scope: `phaser-gameplay-systems/references/physics-engine-selection.md`
- New game completion checklist, when creating a game or first playable slice: `phaser-gameplay-systems/references/checklists/new-game-definition-of-done.md`
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

Prompt templates are packaged in `references/prompt-templates.md` under the director and relevant sibling skills. Load them only when the user asks for a reusable prompt or task template.

Try reference paths in this order:

1. Relative to the loaded skill path: `<loaded-skill-dir>/references/<file>.md`
2. Claude default path: `~/.claude/skills/<skill-name>/references/<file>.md`
3. Codex default path: `~/.codex/skills/<skill-name>/references/<file>.md`
4. General agents path: `~/.agents/skills/<skill-name>/references/<file>.md`
5. Repository source path: `skills/<skill-name>/references/<file>.md`

Rules:

- Load references at phase entry, not at the end.
- Track every required reference in the reference ledger with yes/no, path, and failure reason.
- A phase cannot be marked `done` until its required references are loaded or the final answer explicitly reports the reference as unavailable and the phase as blocked/fallback.
- For premium/AAA/showcase claims, the final response must include the filled 10-category visual scorecard from `visual-scorecard.md`, including average and automatic failures remaining.
- For broad work, include the phase checklist outputs from each relevant reference, not just a summary that the game works.
- Thorough mode is the default for broad, premium, AAA, showcase, complete, and release-ready requests. Economy mode is allowed only for narrow fixes that do not claim premium quality.

If Task/subagent/workflow tools are available, delegate each major phase to a focused worker with the phase `SKILL.md` plus its required references explicitly loaded. If those tools are unavailable, execute serially after the same reference files have been loaded.

## Ledgers

Track both skill loading and phase execution:

- Director: active
- Sibling skills loaded:
  - Gameplay systems: yes/no, path or reason:
  - AAA graphics: yes/no, path or reason:
  - UI: yes/no, path or reason:
  - Debug/profile: yes/no, path or reason:
  - QA/release: yes/no, path or reason:
  - Sprite generator: yes/no/not-needed, path or reason:
  - Image generator: yes/no/not-needed, path or reason:
  - Audio generator: yes/no/not-needed, path or reason:
- External asset sourcing:
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
- Required references loaded:
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
- Gameplay systems: pending/running/done/skipped, evidence:
- External asset sourcing: pending/running/done/skipped, evidence:
- AAA graphics: pending/running/done/skipped, evidence:
- UI: pending/running/done/skipped, evidence:
- Debug/profile: pending/running/done/skipped, evidence:
- QA/release: pending/running/done/skipped, evidence:

A phase is done only with implementation plus verification evidence.

## Phase Routing

- `phaser-gameplay-systems`: first playable slice, architecture, mechanics, entities, input, camera, controls, game feel.
- Physics selection: engine choice (Arcade vs Matter), fixed/semi-fixed timestep, collider/overlap strategy, sensors, body sizing, world bounds, and QA for physics-heavy games.
- External asset sourcing (optional): only if the user wants generated art — an optional credential probe, generator skill loading, and the resulting output files. Procedural/local art needs none of this; recording the asset-source decision (procedural or generated) is sufficient and is not a prerequisite for `phaser-aaa-graphics-builder`.
- `phaser-aaa-graphics-builder`: basic-looking screenshots, sprite/atlas architecture, parallax, particles/VFX, pipelines/postFX, Lights2D, juice, visual scorecard.
- `phaser-game-ui-designer`: HUDs, menus, overlays, responsive UI, icons, safe areas, UI states, parallel UI Scene.
- `phaser-debug-profiler`: blank/black canvas, scene/render/runtime bugs, loader failures, scale/resize, mobile input/render bugs, performance profiling.
- `phaser-qa-release`: browser QA, screenshots, canvas pixels, responsive checks, production build, preview, base path, release notes.
- `phaser-sprite-generator`: external AI-generated 2D art, spritesheets, animation frame sets, tilesets, texture atlases (+ JSON), sheet slicing and atlas packing.
- `phaser-image-generator`: 2D concept/reference images, sprite-sheet sources, tileset sources, backgrounds, skies, parallax plates, logos, icons, GUI elements, decals.
- `phaser-audio-generator`: generated SFX, looping ambience, UI sounds, voice/TTS, voice conversion, cleanup/isolation, and game audio runtime planning.

If a sibling skill file is loaded, follow its workflow for that phase. If it is unavailable, record the missing path/reason and use `references/director-phase-os.md` for that phase.

## Packaged Runtime Resources

For new projects, use the gameplay skill's packaged scaffold creator:

```bash
python3 <phaser-gameplay-systems-skill-dir>/scripts/create_phaser_game.py ./my-game
```

For canvas inspection, use the generated game's `npm run inspect:canvas` when available, or the QA skill's packaged inspector:

```bash
node <phaser-qa-release-skill-dir>/scripts/inspect-phaser-canvas.mjs --url http://127.0.0.1:5188
```

## Premium Completion Rule

For premium, AAA, polished, complete, release-ready, or showcase requests, completion requires visible quality across gameplay, hero/player, obstacles/enemies, rewards/interactables, world kit, HUD/menu states, render/pipeline/lighting, feel, performance/mobile, and QA.

If screenshots are dominated by flat colored rectangles, plain Graphics shapes, untextured tile grids, generic stat cards, sparse worlds, or glow-only detail, the task is not done.

The scorecard must use the exact categories from `phaser-aaa-graphics-builder/references/visual-scorecard.md`: Art direction, Hero/player, Obstacles/enemies, Rewards/interactables, World/environment, Materials/textures, Lighting/render, VFX/motion, UI/HUD, and Performance evidence. Do not substitute a personal rubric.

## Required Verification

- Build/typecheck.
- Local browser run.
- Console/page error check.
- Active desktop and mobile screenshots.
- Nonblank canvas pixel evidence.
- Main input/objective/fail or restart path.
- Visual scorecard for premium/AAA claims.
- External asset sourcing ledger for premium/AAA or less-basic graphics claims.
- Asset-sourcing decision recorded (procedural or generated); when generation was used, the output paths. Procedural/local art is a complete answer and needs no probe output or blocker evidence.
- Audio is optional; if omitted, it may be noted as a possible gap, never a blocker (procedural/silent output is acceptable).
- Renderer diagnostics when graphics changed.
- Final ledger with evidence and remaining blockers.

## Report Audit

When shell tools are available, draft the final evidence report to a temporary markdown file and run the director audit before finalizing broad or premium work:

```bash
python3 <director-skill-dir>/scripts/audit_reference_report.py --premium /path/to/final-report.md
```

Use `--premium` for premium, AAA, showcase, high-fidelity, polished, complete, release-ready, or "less basic" claims. Add `--physics` for physics-heavy games such as pinball, marble/physics puzzles, Matter-based stacking/ragdoll games, mini-golf, or games with many sensors/colliders. Add `--audio` when generated or integrated audio is in scope. Audio is informational, not mandatory: for premium active-gameplay claims you may note its absence as a possible gap, but silent/procedural output is acceptable and the user need not generate audio. If the audit fails, fix the missing report sections or state the exact blocker instead of claiming completion. If the script is unavailable, manually enforce the same required sections: skill-loading ledger, reference ledger, external asset/audio sourcing ledger, phase checklist, visual scorecard, physics/audio diagnostics when relevant, verification evidence, and remaining risks.

## Final Response

Report the skill-loading ledger, reference ledger, external asset sourcing ledger, phase ledger, files changed, run URL, controls, verification commands, screenshots/artifacts, renderer/performance notes, quality gates passed, skipped phases, and remaining risks. For premium/AAA/showcase claims, include the filled visual scorecard and automatic failures remaining. Be precise: "invoked" means a slash/tool skill invocation; "loaded" means the `SKILL.md` or reference file was read into context; "executed phase" means the work was performed under either loaded skill guidance or the director fallback.
