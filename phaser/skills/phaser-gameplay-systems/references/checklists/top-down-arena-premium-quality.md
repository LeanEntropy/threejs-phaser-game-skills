# Top-Down Arena Premium Quality Checklist

For top-down arenas, twin-stick shooters, survivor/horde games, and arena brawlers.

- Player avatar has a strong readable silhouette and clear facing/aim direction from the top-down camera.
- Player includes visible subassemblies or states such as body, weapon/aim indicator, shield/hit flash, dash trail, and reload/charge tell.
- Player collision body is tighter than the art and feels fair (no clipping or invisible-corner snags).
- Enemy families have distinct silhouettes, colors/tints, and telegraphed attacks (wind-up tween before they strike).
- At least three enemy families are present: a chaser, a ranged/shooter, and a heavy/special (charger, splitter, or elite).
- Pickups/drops are readable on a busy floor and have clear collection feedback (pop, sparkle, sound, HUD pulse).
- At least two reward/upgrade variants exist beyond one recolored pickup (e.g. health, ammo/energy, score gem, temporary power-up).
- Floor and arena edges communicate playable bounds and safe zones without becoming visual noise (camera bounds + readable wall band).
- Background, floor decals, and a subtle parallax or vignette layer create depth and focus without hiding entities.
- The arena uses reusable tile/prop kits (cover, hazards, spawners), not one stretched background image.
- Spawn telegraphs are clear: the player sees where enemies/waves appear before they can deal damage.
- Projectiles (player and enemy) are pooled, readable, color-coded by source, and never lost against the floor.
- Camera follow, zoom, deadzone, and shake support fast movement and dodging without nausea or losing the player.
- HUD prioritizes combat state: health/shield, ammo/energy/cooldown, score/combo, wave/timer, and clear fail/retry.
- HUD lives in a parallel UI scene with `setScrollFactor(0)` and is not a grid of generic debug/stat cards unless intentionally diegetic.
- Hit, kill, dash, level-up, low-health, and restart states have polished feedback (flash, hit-stop, shake, particles, audio).
- Difficulty ramps through wave/timer/density and stays readable at peak entity counts.
- Mobile layout keeps virtual stick/aim and action buttons away from the combat focal area and safe-area edges.
- Worst-case wave performance is checked with diagnostics (fps, active bodies, pooled projectile count, active tweens/particles).
- The game is playtested through ramp-up, ordinary clears, a dodge/near-death moment, failure, and restart.
