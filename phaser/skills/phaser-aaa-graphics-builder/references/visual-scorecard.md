# Visual Scorecard

Score active-play screenshots, not idle title screens or isolated showroom sprites. Use desktop and mobile screenshots when mobile is in scope.

## Scoring Scale

- 0: Placeholder. Default Graphics blocks, flat single-color background, unreadable state, debug UI, or no evidence.
- 1: Basic styled. Playable and themed, but still obvious prototype art, flat composition, one repeated silhouette, or generic UI.
- 2: Premium stylized. Authored silhouettes, palette/material systems, parallax depth, readable state, cohesive UI/world, measured performance.
- 3: Showcase. Strong art direction, memorable hero and world, dense authored detail, excellent readability, polished VFX/juice and postFX, and diagnostics.

## Categories

1. Art direction.
   - 0: No clear theme.
   - 1: Theme is mostly colors/tint.
   - 2: Theme affects silhouettes, palette, UI, world, and feedback.
   - 3: Distinct identity visible in every surface.
2. Hero/player (silhouette/sprite craft).
   - 0: Default Graphics rectangle/circle.
   - 1: Basic sprite with tint or simple attachment.
   - 2: Authored silhouette, palette ramp/trim, state cues, collision proxy.
   - 3: Memorable sprite/atlas with layered construction and expressive animation.
3. Obstacles/enemies.
   - 0: Rectangles/circles/triangles.
   - 1: Recolored repeated silhouette.
   - 2: Three readable variants with telegraphs and palette cues.
   - 3: Varied family with animation, anticipation, and gameplay clarity.
4. Rewards/interactables.
   - 0: Plain dot/coin/box.
   - 1: Repeated object with simple glow tint.
   - 2: Two authored forms with idle/collect states and UI feedback.
   - 3: Desirable, animated, and clearly valued during motion.
5. World/environment (parallax/depth).
   - 0: Flat single-color fill, empty arena, one solid band.
   - 1: Themed but sparse, single static background.
   - 2: Layered parallax with foreground/midground/background and scale cues.
   - 3: Dense authored world with parallax that supports gameplay readability.
6. Palette/materials/textures.
   - 0: Flat raw colors.
   - 1: Basic tint or one blend mode.
   - 2: Shared palette roles, procedural decals/trim/panel-line textures, normal maps for Lights2D where used.
   - 3: Rich cohesive palette/material language with measured texture/atlas use.
7. Lighting/postFX.
   - 0: No lighting intent or unreadable darkness.
   - 1: Bloom/vignette used as the main style.
   - 2: Intentional Lights2D or faked light (gradients/additive sprites), key/fill/rim feel, contact shadow, depth.
   - 3: Cinematic but readable composition with disciplined postFX (bloom/glow/vignette restraint).
8. Particle VFX/juice/motion.
   - 0: None or random particles.
   - 1: Generic particles/trails.
   - 2: Event-driven VFX plus juice (squash & stretch, screen shake, hit-stop, flash/tint) for boost, pickup, hit, fail, combo, shield, or spawn.
   - 3: High-impact effects and juice that clarify gameplay and remain performant.
9. UI/HUD (cohesion).
   - 0: Debug text or missing UI.
   - 1: Generic stat-card dashboard.
   - 2: Genre-specific HUD states, meters/icons, responsive text fit, UI Scene separation.
   - 3: Cohesive game interface with strong hierarchy and polished transitions.
10. Performance evidence.
   - 0: No metrics after visual changes.
   - 1: Informal "seems fine".
   - 2: Draw-call/batch counts, active game-object counts, build/browser QA, desktop/mobile screenshots.
   - 3: Baseline/post metrics, bottleneck notes, batch/particle/texture-memory budgets, and optimized atlas strategy.

## Thresholds

Premium:

- Every category at least 2.
- Average at least 2.3.
- Desktop and mobile active-play screenshots captured when mobile is in scope.
- Renderer diagnostics reported after graphics changes.

Showcase:

- At least six categories score 3.
- No category below 2.
- Average at least 2.7.
- Performance evidence includes before/after or budget-aware notes.

## Automatic Failures

Any of these prevents a premium/AAA/showcase claim. Any single category below 2 means the game is not premium:

- Active screenshot is Graphics-primitive-dominant (raw rectangles/circles).
- Main world is a flat single-color fill, one static band, or a sparse empty arena with no parallax.
- Hero asset is mostly a default Graphics shape plus tint/glow.
- Obstacles or rewards are one repeated silhouette.
- HUD is mostly rectangular stat/debug cards.
- Bloom, vignette, darkness, or particles hide missing authored sprite art.
- Animation is stiff with no juice (no squash/stretch, shake, hit-stop, flash) where impacts occur.
- UI overlaps the play path, clips text, or fails mobile safe areas.
- The game is not playable through real input.
- No active-play screenshot was captured.
- No renderer diagnostics were collected after major graphics work.

## Report Format

```text
Visual scorecard:
- Art direction: before X / after Y - evidence:
- Hero/player (silhouette/sprite craft): before X / after Y - evidence:
- Obstacles/enemies: before X / after Y - evidence:
- Rewards/interactables: before X / after Y - evidence:
- World/environment (parallax/depth): before X / after Y - evidence:
- Palette/materials/textures: before X / after Y - evidence:
- Lighting/postFX: before X / after Y - evidence:
- Particle VFX/juice/motion: before X / after Y - evidence:
- UI/HUD (cohesion): before X / after Y - evidence:
- Performance evidence: before X / after Y - evidence:
Average:
Automatic failures remaining:
```

If any category remains below threshold, state the exact next pass instead of declaring completion.
