---
name: phaser-aaa-graphics-builder
description: "Upgrade Phaser 3 games from basic/prototype 2D visuals to premium AAA-inspired browser graphics. Combines art-direction critique, procedural Graphics/sprite art building, optional external asset sourcing decisions, phaser-sprite-generator spritesheets/atlases/tilesets, phaser-image-generator concept/texture workflows, scene visual polish, palette/material/Lights2D libraries, world parallax/prop kits, particle VFX and juice, render/postFX pipeline, and visual scorecard gates. For premium 2D games (platformer, top-down, shoot-em-up, roguelike, arcade) with characters, vehicles, ships, weapons, buildings, signature props, skies, tilesets, decals, logos, icons, or GUI art, procedural/local assets are a complete answer; the generator skills are optional enhancements to reach for when generated art would materially improve the result and the user wants it."
---

# Phaser AAA Graphics Builder

## Purpose

Own the production graphics pass for a Phaser 3 (2D) game. Convert basic screenshots into authored, high-density, performance-aware 2D visual experiences with strong silhouette craft, palette, parallax depth, particle VFX, animation juice, cohesive UI, and disciplined postFX.

## Use When

Screenshots still look basic, sprites look primitive or are flat Graphics blocks, worlds are sparse single-color backgrounds, UI/world art feels generic, animation reads stiff (no squash/stretch, shake, hit-stop, or flash), or the user asks for premium, AAA, high-fidelity, showcase, or less-basic 2D graphics.

## Required References

These references are required phase-entry gates, not optional reading:

- Load `references/visual-scorecard.md` before scoring, judging completion, or making any premium/AAA/showcase claim.
- Load `references/implementation-blueprint.md` before changing graphics architecture, palette/Lights2D, VFX, rendering/pipelines, diagnostics, or broad visual systems.
- Load `references/model-recipes.md` before building or upgrading hero/player, obstacle, enemy, pickup, world-kit, palette, or prop sprites and procedural Graphics art.
- Load `references/render-recipes.md` before changing blend modes, postFX/preFX, camera FX, Lights2D, parallax layering, or render composition.
- Load `references/checklists/aaa-game-quality-gate.md` and `references/checklists/aaa-visual-scorecard.md` before declaring a game premium, AAA, showcase, complete, release-ready, or less basic.
- Load the relevant checklist before focused work: `references/checklists/procedural-model-quality.md`, `references/checklists/material-lighting-quality.md`, or `references/checklists/performance-safe-visual-detail.md`.
- Load `references/prompt-templates.md` only when the user asks for reusable prompts, a graphics-pass prompt, or a task template.

For broad "still looks basic", premium, AAA, high-fidelity, showcase, or less-basic graphics work, load all four references as the first action in the phase. Track them in a reference ledger with yes/no, path, and failure reason. Do not mark the graphics phase complete while any required reference is skipped.

External asset sourcing (optional enhancement):

- For premium/AAA/showcase/high-fidelity/less-basic graphics with a hero/player, character, creature, boss, vehicle, ship, building, weapon, signature prop, complex pickup, or hero environment piece, `phaser-sprite-generator` is one optional route to higher fidelity; procedural Graphics/atlas art is a complete answer, so load it only when you want generated art and the user is open to it.
- For premium/AAA/showcase/high-fidelity/less-basic graphics with concept needs, texture/tileset references, decals, logos, faction marks, icons, GUI art, skies, backgrounds, parallax plates, or title/menu art, `phaser-image-generator` is an optional enhancement; procedural/local 2D art is a complete answer.
- The director credential probe is optional and diagnostic; a missing key simply means use procedural/local assets. If you do report a key as a blocker, paste the SET/MISSING output.
- Create an asset sourcing ledger for each high-value surface: procedural Graphics / phaser-image-generator / phaser-sprite-generator / hybrid, recording the chosen approach (procedural needs no excuse) plus any outputs.
- `not-needed` / `procedural` is always a valid ledger entry for any surface, with no generator loaded.
- For premium hero surfaces, procedural-only is perfectly acceptable; if the user wants higher fidelity, a generator is one optional route. When you do generate, note the output (spritesheet/atlas/tileset path + JSON, an image-generator output path, or a documented hybrid chain). Quality is judged on the result, not on whether a generator was used.

## Workflow

1. Capture or inspect active desktop/mobile screenshots.
2. Score visuals across art direction, hero/player, obstacles, rewards, world, palette/materials, lighting/postFX, particle VFX/juice, UI, and performance evidence.
3. Add missing graphics architecture: palette/material library, procedural texture/decal helpers (Graphics + `generateTexture`), sprite/atlas factories, world parallax prop kit, VFX/juice system, render/postFX pipeline, diagnostics.
4. Run the credential probe, then fill the external asset sourcing ledger per surface: procedural Phaser Graphics factory, `phaser-image-generator` 2D reference/texture, `phaser-sprite-generator` spritesheet/atlas/tileset, or a hybrid.
5. Upgrade every weak visible surface, not only one hero sprite.
6. Add palette/Lights2D/blend-mode and postFX polish after authored forms exist.
7. Add event-driven particle VFX and juice (squash & stretch, screen shake, hit-stop, flash/tint, trails) tied to gameplay state.
8. Re-score screenshots. Continue until every premium category is at least 2/3 or report exact blockers.
9. Verify renderer diagnostics, desktop/mobile screenshots, console/page errors, canvas pixels, imported asset budgets, and playability.

## Core Rule

Do not make primitives look AAA by adding bloom/glow. First build authored silhouettes, then palette/materials, then lighting/blend, then particles/juice/postFX.

## Final Response

Report the reference ledger, credential probe output, external asset sourcing ledger, score before/after, production surfaces upgraded, files changed, screenshots/artifacts, renderer diagnostics (draw calls/batches, active game objects, texture/atlas memory, particle/tween counts), imported asset diagnostics when relevant, and remaining blockers. For premium/AAA/showcase claims, include the filled visual scorecard exactly as defined in `references/visual-scorecard.md`, including average and automatic failures remaining.
