# HUD Readability Checklist (Phaser 3)

- Player health/status is readable during normal movement and high-action moments.
- Objective/progress information is visible without competing with threats or pickups.
- Text contrast remains legible over bright, dark, and moving scene backgrounds (use stroke, shadow, or a backing nineslice/scrim).
- Critical status changes have at least two feedback channels when useful: shape, color/tint, motion (tween/pulse), particles, sound, or text.
- Meters, timers, and counters have fixed-width or stable containers (BitmapText box, reserved Text width, or scaled meter Graphics).
- HUD placement avoids the player focal area and likely spawn/threat lanes.
- HUD is pinned (`setScrollFactor(0)`) or in a parallel UI Scene so it stays put as the camera follows/zooms.
- HUD scale is appropriate at the chosen Scale Manager mode for desktop, laptop, and mobile viewports.
- Touch controls and HUD elements do not overlap each other.
- UI transitions (tweens, scene fades) do not delay input response or hide the next player decision.
- Fast-changing readouts use BitmapText (or are not re-rasterized every frame) so the HUD does not cost frame time.
- Screenshot review confirms HUD readability before and after interaction.
