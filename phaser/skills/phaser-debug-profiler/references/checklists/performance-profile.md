# Performance Profile Checklist

- Record target device, browser, viewport, Scale mode, zoom/DPR, and build mode (use production preview).
- Measure `this.game.loop.actualFps` and frame time (`this.game.loop.delta`) after warmup.
- Capture draw calls (batches) and confirm the renderer type (`game.renderer.type` WEBGL vs CANVAS).
- Count active game objects (`this.children.length`, group `countActive(true)`) and animated objects.
- Count physics bodies (Arcade: `this.physics.world.bodies.size` + `staticBodies.size`; Matter: `localWorld.bodies.length`) and colliders.
- Count particles (alive per emitter), active emitters, active tweens (`this.tweens.getTweens().length`), and timers.
- Identify expensive postFX/pipelines, large TileSprites, Graphics redraws, transparent overdraw, and full-screen effects.
- Check texture & atlas count, dimensions, duplicates, and mobile GPU texture limits.
- Check texture atlasing/batching opportunities, blend-mode/texture switches breaking batches, and object churn in `update`.
- Check garbage-collection pressure from per-frame allocations in `update`.
- Check resource cleanup during scene changes (timers/tweens/emitters/listeners/textures).
- Compare bundle size before and after major dependencies.
- Re-measure the same scenario after each optimization.
