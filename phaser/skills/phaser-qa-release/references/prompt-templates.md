# Phaser QA/Release Prompt Templates

Reusable prompt templates packaged with this skill. Use only templates relevant to the current request, and adapt placeholders to the game/project context.

---

# Release Pass Prompt

Use `phaser-qa-release` to prepare this Phaser 3 game for release.

Release target:
- static host, GitHub Pages, Netlify, Vercel, itch.io, or other:

Requirements:
- Run production build (`tsc && vite build`) and preview.
- Verify asset paths under the intended Vite `base` path (subpath hosting needs `base: '/repo/'`).
- Check bundle size and large assets (atlases, tilesets, audio).
- Run desktop and mobile visual QA.
- Confirm no debug-only UI leaks: `arcade.debug` off, no physics debug graphic, no diagnostics/FPS overlay, no scene-skip/god-mode shortcuts, unless intentionally enabled.
- Produce final report with commands, artifacts, screenshots, and residual risks.
