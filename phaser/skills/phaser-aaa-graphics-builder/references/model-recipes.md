# Sprite And Procedural Graphics Art Recipes

These recipes are for scratch-built Phaser 3 art when external sprite assets are unavailable. The goal is not photorealism; it is authored, layered, readable, premium 2D browser-game art built from `Graphics`, baked textures (`generateTexture`), atlas frames, palette ramps, and (optionally) Lights2D normal maps.

## Art Principles

- Start with silhouette. A sprite should be recognizable as a flat dark shape before palette, tint, or glow.
- Combine simple bases with authored detail: layered Graphics shapes, polygons, arcs, beveled edges (two offset strokes), trim lines, decals, and tinted accent sprites.
- Use asymmetry and functional parts: fins, vents, antennae, panels, bolts, visors, exhausts, joints.
- Put detail where the camera sees it. Spend pixels and child objects on player-facing, gameplay-relevant areas.
- Create state variants through palette/tint swaps, animation frames, additive accent sprites, and VFX sockets.
- Keep a simple Arcade collision body separate from the detailed visual (size/offset the body, not the sprite).
- Use shared atlas frames / baked textures and tint for repeated bolts, panels, lights, windows, spikes, rocks, or tiles.
- Name important child objects: `cockpitGlass`, `leftEngine`, `hazardTeeth`, `pickupCore`, and size the collision body explicitly.

## Palette Ramps (the 2D "material")

A premium 2D look comes from a controlled palette, not from glow. For each role build a 3-5 step ramp (shadow -> mid -> highlight, plus accent):

- Pick a small master palette (8-16 colors) and reuse it everywhere for cohesion.
- Shade with the ramp, not with `alpha` darkening, so colors stay saturated.
- Use a single warm or cool light direction across all sprites for consistency.
- Reserve the brightest highlight and the most saturated accent for hero/reward/emissive signals.
- For Lights2D, author a matching normal map (baked from the same Graphics silhouette with a faux-bevel gradient) and `sprite.setPipeline('Light2D')`.

## Minimum Premium Asset Pass

For a game that asks for premium/AAA/showcase quality, build at least:

- One hero/player sprite with a readable silhouette, a palette ramp, and three state cues (idle, action, hit).
- Three obstacle/enemy variants with unique silhouettes and telegraphs.
- Two reward/interactable variants with idle and collect states.
- One world prop/parallax kit with at least eight reusable parts/layers.
- One palette/decal kit with trim, panel lines, hazard marks, and emissive accents.
- Collision body sizing and renderer diagnostics for the above.

## Hero Vehicle Recipe (top-down or side)

Use for runners, racers, hovercraft, spaceships, drones, or arcade vehicles.

- Core hull: an authored polygon (`graphics.fillPoints([...])`), tapered, not a plain rectangle.
- Nose/front: wedge, intake, sensor strip, or blade shape.
- Cockpit/core: a beveled ellipse or capsule with a glass-tint highlight (`SCREEN`/`ADD` accent).
- Engines: thruster nozzles with inner emissive discs (additive sprite) and trail sockets (anchor points for emitters).
- Wings/fins: triangular or curved plates with a trim line (offset darker stroke).
- Decals: panel lines, numeric marks, faction glyph, hazard ticks, small bolts (baked decal texture, reused).
- State cues: boost flare frame, shield shell sprite, damage scorch overlay, pickup glow, overheat red tint.
- Collision body: one box/circle matching the gameplay footprint, smaller than the visual.

Reject if the hero is mostly a rectangle with two dots and a glow.

## Hero Character Recipe

Use for platformers, brawlers, top-down action, or stylized adventure games.

- Body mass: head, torso, limbs as separate shapes/frames with a clear costume color-block silhouette.
- Rig illusion: distinct shoulders, hands, feet, belt, backpack, cape, or armor accents; if using a Container, group limbs as named children for procedural anim.
- Face/identity: visor, mask, hair/helmet crest, color-blocked silhouette, weapon/tool.
- Animation: build a spritesheet (idle/run/jump/hit) or tween-pose a Container; define anims with `this.anims.create({ key, frames: this.anims.generateFrameNumbers('sheet', { start, end }), frameRate, repeat: -1 })`.
- Palette zones: skin/fabric/armor/metal/glass/emissive accents from the shared ramp.
- State cues: hit-flash (`setTintFill(0xffffff)`), shield ring, attack trail socket, charge glow.
- Collision body: a box/capsule narrower than the art, with `setSize`/`setOffset`.

Reject if the character reads as stacked circles/rectangles with no costume, joints, or silhouette.

## Obstacle And Enemy Families

Build distinct gameplay reads:

- Low barrier: ground-hugging slab, spikes, rails, caution panels, animated warning light.
- Gate/arch: overhead frame, side posts, pulsing pass/avoid lane, moving shutters.
- Moving hazard: rotating arm, sweeper beam, drone, crusher, sliding block, orbiting mines.
- Trap/zone: laser grid, electric puddle, collapsing tile, proximity mine.
- Enemy: body core, sensor/head, weapon, shield, locomotion/hover base, attack telegraph (windup frame + tint).

Each variant needs:

- Unique silhouette.
- Palette cue for danger (hazard ramp).
- Telegraph readable from distance (windup anim, tint pulse, or warning sprite).
- Animation or state change.
- Collision body.
- Low-cost repeated detail (shared atlas frame + tint).

Reject if all hazards are recolored rectangles/triangles.

## Reward And Interactable Recipes

Rewards should be readable and desirable during motion.

- Token: outer ring, inner core, value icon, shimmer accent (additive), collect-burst socket.
- Shard: faceted crystal polygon, metal bracket, orbiting chips, emissive seam.
- Capsule: glass shell, suspended item, end caps, rotating label.
- Power-up: icon silhouette matched to effect; color and shape differ from score pickups.
- Objective item: larger scale, unique motion, UI echo, stronger glow/VFX.

States:

- Idle: slow rotation/pulse/bob tween, or anim loop.
- Attract: tween/trail toward player.
- Collect: scale-snap + alpha out, emitter burst, score trail, HUD meter update.

Reject if rewards are plain dots or rings without state feedback.

## World Prop / Parallax Kit

Build modular props that can be reused, tinted, and tiled:

- Track/road: lane plates, seams, arrows, side rails, guard segments (TileSprite for repeat).
- Arena: boundary bands, floor tiles, spawn pads, cover blocks, goal markers.
- City/sci-fi: window strips, antennas, rooftop units, bridge trusses, pylons, billboards.
- Nature: rocks from authored polygons, cliffs, roots, crystals, grass tufts.
- Industrial: pipes, vents, cables, tanks, crates, gantries, lights, warning signs.
- Sky/space: gradient sky texture, cloud/nebula cards, distant skyline silhouette, parallax dust.

Layer the kit as parallax (see `render-recipes.md`):

- Near props create speed and scale (scroll factor > 1).
- Mid props define the playable corridor (0.4-0.7).
- Far props/sky create depth without stealing draw calls (0.1-0.3, often a single TileSprite).

Reject if the world is a flat single-color fill or one static band with no parallax.

## Procedural Graphics Techniques

- `graphics.fillPoints(points, true)`: tapered hulls, rocks, shards, wedges, crystals, custom silhouettes.
- `graphics.fillRoundedRect` / `strokeRoundedRect`: panels, cards, capsules, beveled bodies.
- `graphics.arc` / `slice` / `fillCircle`: domes, wheels, cores, rings, gauges.
- `graphics.lineBetween` / `strokePath`: panel lines, cables, trim, rails, seams.
- `graphics.generateTexture(key, w, h)`: bake any of the above into a reusable texture for sprites, particles, or tiles, then destroy the Graphics object.
- `TileSprite`: repeated ground, walls, parallax bands, scrolling backgrounds.
- Atlas frames + `setTint`: window grids, bolts, debris, grass, lights, small props at volume.
- Container of children: composite hero/boss art with named, separately-animated parts.

Use faux-bevel layering when real geometry depth is unavailable: draw a lighter top/left edge and a darker bottom/right edge as offset strokes; or stack a slightly smaller, brighter shape on top.

## Palette And Detail Rules

- Use palette-ramp contrast (value contrast), not only hue contrast.
- Use additive (`ADD`) accent sprites or postFX glow for authored signals, not entire objects.
- Use glass/`SCREEN` highlights sparingly on hero details.
- Add a dark contact-shadow ellipse under important objects.
- Use decals to imply scale and function.
- Reuse UI icon shapes as world decals for cohesion.

## Diagnostics Checklist

After an art pass, report:

- Container child counts for composite art.
- Unique texture keys / atlas frames touched.
- Baked-texture (`generateTexture`) count and sizes.
- Approximate active sprite count in the worst-case scene.
- Collision bodies sized separately from visuals.
- Pooling/tiling strategy for repeated/background props.
- Active-play screenshots, not only showroom renders.
