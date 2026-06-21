# Release Checklist

- `npm run build` passes (`tsc && vite build`).
- `npm run preview` or equivalent static server runs the built files.
- Asset URLs work with the intended Vite `base` path (subpath hosting like GitHub Pages needs `base: '/repo/'`).
- No local-only files, debug panels, physics debug graphics (`arcade.debug` / `drawDebug`), or diagnostics/FPS overlays are visible unless intentionally gated.
- No scene-skip, god-mode, or test shortcuts reachable in player-facing release.
- Console is clean in production preview.
- Desktop and mobile visual checks pass.
- Main interaction works in production preview.
- Bundle size and large assets are reviewed (atlases, tilesets, audio, fonts).
- License/source notes for third-party assets are present.
- Final report includes commands, screenshots/artifacts, known risks, and deployment notes.
