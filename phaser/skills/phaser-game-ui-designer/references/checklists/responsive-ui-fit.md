# Responsive UI Fit Checklist (Phaser 3)

- A Scale Manager mode (FIT / RESIZE / ENVELOP) and a design resolution were chosen deliberately and match the UI strategy.
- `autoCenter` is set so the canvas centers in its parent.
- Desktop, laptop, narrow, and mobile viewports (and both orientations if supported) have been checked.
- Under RESIZE, a `this.scale.on('resize', ...)` handler repositions/resizes pinned UI, scrims, and edge controls; it is removed on `SHUTDOWN`.
- UI is anchored to screen edges/centers from `this.scale.gameSize` (or design width/height under FIT), not hard-coded device pixels.
- Safe-area padding is applied for mobile edges and notches when controls sit near edges (`env(safe-area-inset-*)` on the canvas parent / DOM overlay, plus `viewport-fit=cover`).
- No text clips, overflows, overlaps, or becomes unreadably small at any tested size.
- Long labels wrap or compress intentionally without breaking button/nineslice height.
- Controls keep stable hit targets and do not shift during score/time/state changes.
- Touch targets stay ~44 CSS px after canvas scaling (e.g. `44 / this.scale.displayScale.x` world px under FIT) and are separated enough to avoid mis-taps.
- Menu content remains on-screen and reachable without offscreen controls at every supported aspect ratio.
- Canvas resizing does not desynchronize HUD placement from gameplay framing.
- Screenshots or Playwright artifacts prove fit at the tested sizes and modes.
