# Mobile Input Checklist

- Include `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">`.
- Set the canvas/parent `touch-action: none` only where needed to stop scroll/zoom from stealing input.
- Use Phaser pointer events (`this.input.on('pointerdown'|'pointermove'|'pointerup')`) and `setInteractive()` hit areas for per-object touch.
- Enable multi-touch with `this.input.addPointer(n)` when controls need simultaneous touches.
- Choose an appropriate Scale Manager mode (`FIT`/`RESIZE`/`ENVELOP`) with `autoCenter` so the canvas fits the device.
- Keep controls reachable with thumbs and away from safe-area edges (`env(safe-area-inset-*)` around the parent).
- Avoid tiny text or buttons below practical touch size.
- Verify portrait and landscape if both are supported, repositioning HUD via `this.scale.on('resize', ...)`.
- Cap zoom/DPR if performance suffers; ensure controls are not too small or too large after scaling.
- Test pointer up/out/cancel and `pointerupoutside` so a held virtual joystick/button releases when the finger leaves the control.
- Confirm desktop keyboard/mouse input still works after touch controls are added.
- Verify with Playwright mobile emulation and real hardware when available.
