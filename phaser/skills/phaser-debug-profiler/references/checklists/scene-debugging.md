# Scene Debugging Checklist

- Reproduce the issue locally before editing.
- Read the first console error, page error, and any `this.load.on('loaderror')` payload before changing code.
- Confirm exactly one `Phaser.Game` instance exists and the update loop runs once and continues.
- Confirm `game.renderer` was created (type WEBGL or CANVAS, not null) and is attached to the expected canvas inside `scale.parent`.
- Confirm the intended scene actually started and is active (`this.scene.isActive`, `create()` ran without throwing).
- Check canvas CSS size, Scale Manager mode/size, zoom, and device pixel ratio.
- Check camera bounds, scroll, zoom, visibility, and leftover `fade`/`flash` that could black out the view.
- Check the scene holds visible objects (`this.children.length`) added to the display list, with `visible`, `alpha > 0`, sane scale, depth, tint, and blend mode.
- Check texture keys exist (`this.textures.exists`) for every sprite/image; watch for the `__MISSING` placeholder.
- Check asset keys/URLs, Vite base path, async load completion before use, CORS, and failed network requests.
- Check `update(time, delta)` delta units, frame-rate independence, and physics/update ordering.
- Check Arcade/Matter body size/offset, colliders/overlaps registered, and collision layers if gameplay appears broken.
- Check scene-shutdown cleanup for timers, tweens, emitters, and global/registry/`this.scale` listeners.
- Verify the fix with screenshot, pixel sample, and interaction.
