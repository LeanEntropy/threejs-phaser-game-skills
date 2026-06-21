# Mobile Input Checklist (Phaser 3)

- Include `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">`.
- Set the canvas parent / control regions to `touch-action: none` only where needed to stop page scroll/zoom stealing input.
- Pointer events cover touch in Phaser; enable multi-touch with `this.input.addPointer(n)` so a stick and a button can be held together.
- Touch controls emit the SAME game intents as keyboard/mouse (shared logic, not a forked code path).
- Keep controls reachable with thumbs and away from safe-area edges (`env(safe-area-inset-*)` on the parent, or inset positions from `this.scale.gameSize`).
- Avoid tiny text or buttons below practical touch size; keep ~44 CSS px after canvas scaling.
- Verify portrait and landscape if both are supported; reflow pinned UI on `this.scale.on('resize', ...)`.
- Check high-DPR rendering and consider `resolution`/zoom or a perf cap if it stutters.
- Prevent page scroll/zoom gestures from stealing gameplay input.
- Test virtual joystick/button release on every exit path: `pointerup`, `pointerupoutside`, `gameout`, and browser `blur`/`visibilitychange`, so a held control never sticks.
- Verify with Playwright mobile emulation and real hardware when available.
