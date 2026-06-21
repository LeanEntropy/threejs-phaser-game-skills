# New Game Definition Of Done

- The project installs with `npm install`.
- `npm run dev` starts a local Vite server.
- `npm run build` completes.
- The first scene is the game (Boot/Preload land on Play), not a landing page.
- The player can interact within 5 seconds.
- There is a clear objective, score, timer, health, level target, or fail condition.
- Keyboard/mouse input works on desktop.
- Touch or pointer input works if mobile is in scope.
- The camera frames the playable area at desktop and mobile sizes (Scale Manager configured).
- HUD text (a parallel UI scene with `setScrollFactor(0)`) is readable and does not cover critical gameplay.
- Browser console has no blocking errors.
- A screenshot proves the canvas rendered.
- A canvas-pixel check proves the canvas is not blank.
- Restart cleans up entities, tweens, timers, and emitters with no stale state.
- Final report names controls, verification evidence, and remaining risks.
