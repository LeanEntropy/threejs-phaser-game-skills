# Phaser AAA Graphics Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# AAA Graphics Production Pass Prompt

Use `phaser-aaa-graphics-builder` to upgrade this Phaser 3 game from basic prototype 2D visuals to premium browser-game graphics.

Current screenshot blockers:
- 

Target art direction:
- 

Required pass:
- Score current screenshots with `phaser-aaa-graphics-builder/references/visual-scorecard.md`.
- Add or improve the graphics architecture from `references/implementation-blueprint.md`.
- Build palette/material library, procedural texture/decal helpers (Graphics + generateTexture), sprite/Graphics factories, world parallax prop kit, VFX + juice system, render/postFX pipeline, and diagnostics.
- Use `phaser-sprite-generator` for high-value hero/player, character, creature, vehicle, building, weapon, pickup, boss spritesheets/atlases/tilesets when procedural Graphics is not enough.
- Use `phaser-image-generator` for 2D concepts, character turnarounds, texture/tileset references, decals, logos, icons, GUI art, skies, parallax backgrounds, or sprite-generator source images.
- Upgrade hero/player, obstacles/enemies, rewards/interactables, world/parallax kit, HUD cohesion, lighting/postFX, particle VFX + juice, and renderer metrics.

Do not count as completion:
- Recolored rectangles/circles/triangles.
- Bloom, vignette, or darkness hiding missing sprite art.
- One improved sprite while world/obstacles/UI remain placeholders.
- Stiff animation with no juice (no squash/stretch, shake, hit-stop, flash) where impacts occur.
- Idle/showroom screenshots only.
- Missing renderer diagnostics after visual density changes.

Verification:
- Capture active gameplay desktop and mobile screenshots.
- Report visual score before/after.
- Report draw calls (batches), active game objects, texture/atlas count, particle/tween counts, and FPS when available.
- Run build, browser, console/page error, nonblank canvas, interaction, and responsive checks.
- Continue until every scorecard category is at least 2, or report exactly why the target was not reached.

---

# Before/After Visual Critique Prompt

Use `phaser-aaa-graphics-builder` to critique this Phaser 3 game's current screenshots with the visual scorecard and produce a prioritized graphics plan.

Evidence to gather:
- Desktop screenshot.
- Mobile screenshot.
- Optional before/after screenshots if a pass was already completed.
- Renderer diagnostics if available.
- Notes on the game genre (platformer/top-down/shoot-em-up/roguelike/arcade), core verb, and target mood.

Critique dimensions:
- Gameplay readability.
- UI hierarchy and text fit.
- Sprite/silhouette craft and procedural Graphics fidelity.
- Palette, blend modes, Lights2D/faked lighting, color, and contrast.
- Camera composition, parallax depth, and motion/juice clarity.
- Mobile framing and touch/control readability.
- Performance risk from proposed upgrades (batches, overdraw, particles).

Output:
- Pass/fail on whether the game looks polished enough for the current milestone.
- Top five blockers ordered by player impact.
- Recommended next skill/phase: `phaser-aaa-graphics-builder`, `phaser-game-ui-designer`, `phaser-debug-profiler`, or `phaser-qa-release`.
- Concrete acceptance criteria for the next pass.

---

# Palette, Lighting, And PostFX Quality Pass Prompt

Use `phaser-aaa-graphics-builder` for scene-level render quality, palette/material libraries, sprite palettes, Graphics factories, and visual scoring.

Current problem:
- 

Target look:
- 

Work areas:
- Renderer config: pixelArt/antialias, NEAREST/linear filtering, mobile resolution cap, roundPixels.
- Lights2D ambient/key/fill/rim or faked light via gradients/additive sprites.
- Palette ramps, blend modes (ADD/MULTIPLY/SCREEN), tint, generated textures, and decals.
- Parallax background, postFX (bloom/glow/vignette/color matrix), and feedback effects only where they improve readability.
- Camera composition, zoom, deadzone, and gameplay-distance readability.

Constraints:
- Improve palette and silhouettes before adding heavy postFX.
- Keep threats, pickups, player, and objective readable during motion.
- Avoid excessive bloom, low-contrast washes, additive overdraw, and particle clutter.
- Re-measure batches/active objects if visual complexity changes.

Verification:
- Capture desktop and mobile screenshots.
- Check console/page errors and nonblank canvas pixels.
- Compare draw calls/active objects/texture count before and after when practical.
- Play the core loop and confirm effects do not hide gameplay information.

---

# Procedural Hero Asset Pass Prompt

Use `phaser-aaa-graphics-builder` to create or upgrade a high-fidelity scratch-built Phaser hero sprite.

Asset brief:
- Role:
- Silhouette:
- Scale (pixels):
- Camera/gameplay distance:
- Style references:
- Performance budget:

Requirements:
- Build a reusable factory that returns a named Container or a baked-texture Sprite plus body-size metadata.
- Establish a recognizable silhouette before adding small detail.
- Add secondary and tertiary detail through faux-bevels, trims, panels, ridges, decals, additive emissive accents, and palette-ramp contrast.
- Add visible subassemblies, not just a few shapes: shell/body, core/cockpit, trims/rails, engines/emitters, decals/surface marks, and state feedback when relevant.
- Use shared atlas frames / baked textures and tint where possible.
- Define anims (spritesheet) or tween-pose a Container; set palette, blend modes, and (optional) Lights2D intentionally.
- Keep the Arcade collision body simpler/smaller than the visual.

Avoid:
- Placeholder rectangles/circles plus tint.
- Detail visible only from a showroom view.
- Many unique texture keys, excessive children, or batch-breaking draws without gameplay value.
- Glow-only upgrades that leave the silhouette primitive.

Verification:
- Build and run locally.
- Capture gameplay-camera screenshot and one inspection screenshot if useful.
- Report draw calls/active objects before/after when available.
- Verify the asset reads clearly at desktop and mobile gameplay distances.

---

# Visual Polish Prompt

Use `phaser-aaa-graphics-builder` to improve the game's visual clarity and identity.

Use focused prompts instead when the main problem is narrower:
- Use `phaser-game-ui-designer/references/prompt-templates.md` for HUD/menu/interface quality prompts.
- Use the procedural hero asset or world prop kit sections in this file for scratch-built sprite fidelity inside the AAA graphics phase.
- Use the before/after visual critique section in this file when priorities are unclear.

Target feel:
- 

Constraints:
- Keep the game readable during motion.
- Avoid generic purple gradients, excessive bloom, additive overdraw, particle clutter, and static showroom composition.
- Prefer purposeful palette, value contrast, silhouettes, parallax depth, blend-mode variation, juice, and procedural Graphics that support gameplay.
- Hand off substantial UI craft to `phaser-game-ui-designer`; keep sprite/world/render construction under `phaser-aaa-graphics-builder`.
- Keep performance visible while polishing (batches, particles, overdraw).

Verification:
- Capture before/after screenshots where possible.
- Check desktop and mobile framing.
- Confirm the game remains interactive and no console errors were introduced.

---

# World Parallax / Prop Detail Kit Pass Prompt

Use `phaser-aaa-graphics-builder` to create a reusable procedural prop and parallax kit for this Phaser game's world.

World role:
- 

Kit requirements:
- Define 4-8 reusable prop factories with shared palette/atlas.
- Build parallax background layers (far sky/skyline, mid, play, near) with TileSprite and scroll factors.
- Include scale variants, color/tint variants, and clear placement rules.
- Use shared textures/atlas frames, tinting, and tiling for repeated detail.
- Add visual detail that supports navigation, danger, reward, or atmosphere.
- Keep the kit coherent with the existing game UI and world palette/lighting.
- For city/runner worlds, include skyline modules with setbacks/window bands/roof details, foreground speed props, track hardware, signage/cables/supports, and distant parallax layers.

Performance constraints:
- Avoid unique texture explosions; prefer atlas frames + tint and baked TileSprites.
- Keep repeated props tiled, shared, or pooled when practical.
- Track draw calls (batches), active objects, texture count, overdraw, and frame impact.

Verification:
- Capture before/after screenshots from gameplay camera.
- Check desktop and mobile readability.
- Report renderer diagnostics.
- Confirm no console/page errors and no obvious collision/occlusion issues.
- If the world is still a flat fill or one static band, continue the parallax/prop-kit pass.
