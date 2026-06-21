---
name: phaser-qa-release
description: "Verify and release Phaser 3 (2D) browser games. Combines playtest QA, mobile/responsive checks, production builds (tsc && vite build), preview verification, static-hosting base paths, debug gating (arcade.debug off, no debug overlays), bundle review, screenshots, packaged canvas-pixel inspection, console/page-error checks, and release risk reports."
---

# Phaser QA Release

## Purpose

Prove the 2D game works as a player encounters it, then prepare a shippable browser build with known risks.

## QA Workflow

Load `references/qa-release-checklists.md` as the first action before broad QA, mobile verification, bug reporting, production preview, static-hosting checks, or release preparation. Track it in a reference ledger with yes/no, path, and failure reason. Do not mark QA/release complete while this reference is skipped for QA or release work.

Load `references/checklists/visual-verification.md` for screenshot/canvas verification, `references/checklists/playtest-qa.md` for player-loop QA, and `references/checklists/release.md` for production release checks. Load `references/prompt-templates.md` only when the user asks for reusable QA/release prompts or a task template.

1. Install dependencies if needed.
2. Run build/typecheck (`npm run build` = `tsc && vite build`, or `npm run typecheck`).
3. Start dev or preview server.
4. Open browser target.
5. Capture console/page/network errors.
6. Verify nonblank canvas pixels.
7. Capture desktop and mobile screenshots.
8. Trigger main input, objective progression, fail/retry, and recent risky paths.
9. Check HUD text fit, safe areas, touch targets, responsive layout (Scale.FIT/RESIZE behavior).
10. If audio changed, verify user-gesture unlock, SFX triggers, ambience loop start/stop, pause/restart cleanup, mute/volume behavior, and decode/load errors.
11. Record artifacts and issues.

## Packaged Canvas Inspector

Use the bundled inspector when the target project does not already include one:

```bash
node <this-skill-dir>/scripts/inspect-phaser-canvas.mjs --url http://127.0.0.1:5188
```

For mobile emulation, add `--mobile`. Generated games from the packaged scaffold also include their own `scripts/inspect-phaser-canvas.mjs` and `npm run inspect:canvas`.

## Release Workflow

1. Inspect package scripts, Vite config, `base` path, public/assets.
2. Gate debug UI/logging/test helpers (confirm `arcade.debug` is `false`, `physics.world.drawDebug` off, no FPS/diagnostics overlays, no scene-skip or god-mode shortcuts).
3. Run production build and preview/static server.
4. Verify built output desktop/mobile.
5. Review bundle and large assets (atlases, audio, tilesets).
6. Document deploy command, host assumptions, and residual risks.

## Final Response

Lead with pass/fail. Include the reference ledger, QA matrix/checklist result, commands, URL, controls, screenshots/artifacts, issues found/fixed, deployment notes, and risks.
