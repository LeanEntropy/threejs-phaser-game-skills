# Phaser Gameplay Systems Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# Gameplay System Prompt

Use `phaser-gameplay-systems` to add or modify this gameplay system:

System:
- Player-facing behavior:
- Entities affected:
- State changes:
- Collision/physics needs (Arcade vs Matter):
- Audio/visual/HUD feedback:
- Edge cases:

Constraints:
- Preserve existing controls and camera unless the task asks to change them.
- Keep update order deterministic and scenes/groups cleaned up on restart.
- Use Arcade Physics (or simple custom checks) unless the mechanics justify Matter.js.
- Pool frequently spawned objects instead of create/destroy each frame.
- Add debug controls only when they speed tuning.
- Verify through build, local browser run, console check, screenshot, canvas-pixel check, and interaction test.
