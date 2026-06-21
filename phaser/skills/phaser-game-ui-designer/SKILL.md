---
name: phaser-game-ui-designer
description: "Design premium Phaser 3 (2D) game UI. Use for HUDs, menus, overlays, pause/win/lose screens, settings, icon buttons, virtual sticks, touch controls, BitmapText vs Text, nineslice panels, containers, UI Scenes, Scale Manager responsiveness, safe areas, text fit, and UI/world cohesion for platformers, top-down, arcade, shoot-em-up, and roguelike games."
---

# Phaser Game UI Designer

## Purpose

Make 2D game UI intentional, readable, responsive, and genre-specific in Phaser 3.

## Workflow

Load `references/ui-patterns.md` as the first action when designing HUDs, menus, overlays, pause/win/lose screens, settings, touch controls, typography, responsive layout, safe areas, text fit, icons, or UI/world cohesion. Track it in a reference ledger with yes/no, path, and failure reason. Do not mark the UI phase complete while this reference is skipped for interface work.

Load `references/checklists/game-ui-quality.md`, `references/checklists/hud-readability.md`, and `references/checklists/responsive-ui-fit.md` before claiming UI/HUD/menu work is complete. Load `references/checklists/mobile-input.md` when touch controls or mobile safe areas are in scope.

Load `references/prompt-templates.md` only when the user asks for reusable prompts, a UI pass prompt, or a task template.

Decide the rendering surface first: a dedicated **UI Scene** drawn in the canvas (`this.scene.launch('UI')`) versus a **DOM overlay** layered over the canvas. Use the UI Scene for diegetic, world-matched, animated, in-canvas HUD/controls; use a DOM overlay when you need crisp scalable text, easy reflow, real form controls, accessibility, and `env(safe-area-inset-*)`. `references/ui-patterns.md` carries the full decision rule.

Load `phaser-image-generator` when logos, icons, GUI art, faction marks, menu backgrounds, decals, nineslice panel skins, or HUD art would improve quality. Use `phaser-sprite-generator` only for animated UI spritesheets/atlases (icon sheets, animated badges, button states packed as frames), not for elements better drawn with `Graphics` or styled DOM.

1. Capture/inspect desktop and mobile screenshots.
2. Inventory UI states: gameplay, pause, settings, fail/retry, win/milestone, loading, touch controls.
3. Define hierarchy: survival/status, objective, feedback, flavor.
4. Replace utility stat readouts with authored clusters, meters, badges, icons, alerts, and modal overlay Scenes.
5. Use stable dimensions, safe-area padding, text-fit constraints, hover/pressed/focus/disabled states, `setScrollFactor(0)` for HUD.
6. Wire UI to game state via events/registry, not duplicated rules.
7. Verify text fit, overlap, safe areas, touch targets, responsive screenshots across Scale Manager modes, and real state changes.

## Common Failure Modes

- Generic stat-readout HUD with no hierarchy.
- HUD parented to the world camera so it scrolls/zooms with gameplay (missing `setScrollFactor(0)` or a separate UI Scene).
- Text shifts/clips on resize because the Scale Manager mode or design resolution was never chosen.
- Decorative panels reduce readability.
- Touch buttons look right but never emit input intents.

## Final Response

Report the reference ledger, UI state checklist, surface choice (UI Scene vs DOM overlay) with reason, Scale Manager mode and design resolution, UI intent, states covered, files changed, screenshots, text-fit/overlap checks, safe-area/touch-target evidence, controls, and remaining risks.
