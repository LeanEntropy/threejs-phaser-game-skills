# Agent Instructions

This repo contains Codex and Claude Code workflow assets for Phaser 3 (2D) browser-game development.

## Default Technical Stack

- Prefer TypeScript, Vite, npm package imports, and Phaser 3 modules (`import Phaser from 'phaser'`).
- Default renderer is `Phaser.AUTO` (WebGL with Canvas fallback).
- Use **Arcade Physics** for axis-aligned movement, platformers, top-down, shooters, and most arcade games. It is fast and deterministic enough for the common case.
- Use **Matter.js** physics only when the game needs real rigid bodies, slopes, joints, stacking, complex collision shapes, or realistic bounce/friction.
- Load `phaser-gameplay-systems/references/physics-engine-selection.md` before adding or changing physics-heavy gameplay.
- Use the Scale Manager (`Phaser.Scale.FIT` or `RESIZE` with `autoCenter`) from the first implementation path, not as a final afterthought.
- Use Scenes for separation (Boot, Preload, Play, UI/HUD overlay, menus). Keep one responsibility per Scene.
- Use object pooling (Groups with `getFirstDead`/`recycle`) for bullets, particles, enemies, and other high-churn entities.
- Use texture atlases over loose images for production; load spritesheets for fixed-frame animation.
- Use a lightweight HUD Scene or `this.game.loop.actualFps` for frame diagnostics when performance is in scope.

## Game Quality Bar

- For broad requests to build, upgrade, polish, or finish a Phaser game, route through `phaser-game-director` first. The user should not have to name every specialist skill.
- Public Phaser skills are consolidated around the director plus specialist systems: gameplay, AAA graphics, UI, debug/profile, QA/release, sprite generation, image generation, and audio generation.
- In Claude-style skill runners, do not assume a director skill can literally invoke other skills. The director must attempt to load sibling public `SKILL.md` files first, report a skill-loading ledger, and use the bundled phase OS only for files that cannot be loaded.
- For broad/premium director work, the director must load each phase's required `references/*.md` files at phase entry and report a reference ledger. A phase is not done if its required references were skipped.
- Premium/AAA/showcase claims must include the filled visual scorecard from `phaser-aaa-graphics-builder/references/visual-scorecard.md`, including average score and automatic failures remaining. Do not substitute an improvised rubric.
- When shell tools are available, run `skills/phaser-game-director/scripts/audit_reference_report.py --premium <report.md>` against the final evidence report before claiming premium, AAA, showcase, complete, release-ready, or "less basic" success.
- Build a playable loop first. A static scene is not done.
- Do not stop at first playable slice when the user asked for premium, AAA, polished, complete, release-ready, or showcase quality.
- Keep scene setup, game loop, input, systems, entities, UI, assets, and debug tools separated once the prototype grows beyond a single simple file.
- Tune movement, camera, collisions, feedback, and HUD through short playtest loops.
- For physics-heavy games, report engine choice (Arcade vs Matter), fixed/variable step, collider strategy, sensors/overlap zones, body counts, and restart cleanup evidence.
- Avoid decorative-only UI, generic purple gradients, particle clutter, and unchecked post-processing/shaders.
- Keep mobile/touch input and resize behavior in the first implementation path, not as a final afterthought.
- Use screenshot-based art-direction critique when visual priorities are unclear.
- Use `phaser-aaa-graphics-builder` when screenshots still look basic across multiple visual surfaces (flat sprites, no parallax, no particles, no lighting, no juice). Do not split that broad graphics problem into isolated small polish tasks.
- Use focused UI passes for HUDs, menus, text fit, icon controls, and safe-area layout instead of treating interface craft as generic polish.
- Use focused art passes for sprites, tilesets, atlases, parallax layers, particle FX, and pipeline/post-FX detail.
- For premium/AAA/showcase/high-fidelity/less-basic work with characters, props, tilesets, backgrounds, skies, decals, logos, icons, GUI art, SFX, ambience, or voice, load `phaser-sprite-generator`, `phaser-image-generator`, and/or `phaser-audio-generator` before deciding procedural/generated assets are unnecessary.
- Run the director credential probe before claiming sprite/image/audio generation credentials are unavailable. A missing key is not a valid blocker unless the SET/MISSING probe output is reported.
- Report an external asset sourcing ledger for premium graphics work: procedural / phaser-image-generator / phaser-sprite-generator / hybrid per high-value surface, plus output paths or real blocker evidence.
- Treat flat untextured rectangles, single-frame sprites, and generic stat-card HUDs as prototype placeholders unless the user explicitly wants that style.
- Require active-play screenshot scoring for premium/AAA claims. A build is not premium if the visual scorecard has any category below 2.

## Verification Bar

For meaningful Phaser changes, gather evidence before claiming success:

- `npm run build`
- a local dev or preview server opened in a browser
- browser console and page error check
- Playwright screenshot
- canvas nonblank pixel check
- at least one desktop and one mobile viewport
- interaction check for the main control path
- performance snapshot when sprite counts, particles, shaders, or post-processing changed
- UI text-fit, overlap, safe-area, and touch-target evidence when interface layout changed
- external asset sourcing ledger when premium graphics include high-value sprite/tileset/background categories
- credential probe output plus real external asset outputs or blocker evidence for premium asset-category claims
- visual scorecard before/after when the user asks for premium, AAA, showcase, or "less basic" graphics

Use the scaffold's `npm run verify:visual` and `npm run inspect:canvas` when available, or `skills/phaser-qa-release/scripts/inspect-phaser-canvas.mjs` from this repo.
