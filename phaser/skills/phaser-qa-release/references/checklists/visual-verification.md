# Visual Verification Checklist

- Open the local dev or preview URL in a browser.
- Check browser console errors and page errors.
- Confirm the canvas has nonzero display size and nonzero drawing-buffer size.
- Capture a screenshot.
- Sample canvas pixels for nonblank output and color variance.
- Test at desktop, laptop, and mobile viewport sizes.
- Confirm the Scale Manager reflows correctly after resize (Scale.FIT letterboxing or RESIZE relayout, camera/world still framed).
- Confirm UI/HUD text does not overlap or clip (scroll-factor-0 HUD, depth ordering, UI Scene).
- Interact for at least one core action and observe visible state change.
- If using snapshots, make dynamic effects deterministic or mask them (seed RNG, pause tweens/particles).
- If HUD/menu layout changed, also use `phaser-game-ui-designer/references/checklists/game-ui-quality.md`, `phaser-game-ui-designer/references/checklists/hud-readability.md`, and `phaser-game-ui-designer/references/checklists/responsive-ui-fit.md`.
- If sprites/atlases/pipelines/postFX changed, also use `phaser-aaa-graphics-builder/references/checklists/procedural-model-quality.md`, `phaser-aaa-graphics-builder/references/checklists/material-lighting-quality.md`, and `phaser-aaa-graphics-builder/references/checklists/performance-safe-visual-detail.md`.
- If the target is premium, AAA, complete, release-ready, or showcase quality, also use `phaser-aaa-graphics-builder/references/checklists/aaa-game-quality-gate.md`.
- If screenshots still look basic, also use `phaser-aaa-graphics-builder/references/checklists/aaa-visual-scorecard.md`.
- If the game is a platformer or top-down arcade game, also use `phaser-gameplay-systems/references/checklists/platformer-premium-quality.md`.
