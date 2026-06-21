# Phaser Game Skills

Self-contained Codex and Claude Code skills for building playable, polished **Phaser 3 (2D)**
browser games. Install the skills, then ask your agent to use `phaser-game-director`; the
director routes gameplay, graphics, UI, sprite/asset generation, audio, debugging, and release
verification without requiring users to choose every specialist skill manually.

The package includes the runtime materials agents need: `SKILL.md` files, references,
checklists, prompt templates, helper scripts, and a Vite + TypeScript + Phaser 3 scaffold
bundled inside the relevant skill folders.

This is the 2D companion to the Three.js game skills. **2D games → Phaser. 3D games → Three.js.**

## Install

For local development from a cloned checkout:

```bash
./install.sh --codex
./install.sh --claude
./install.sh --all
```

The local installer copies `skills/` into the selected agent skills directory. It skips
same-named skills unless you pass `--force`, and it never removes unrelated user skills unless
`--prune-managed` is explicitly requested.

```bash
./install.sh --claude --force
```

## Use The Skills

After installing, open Codex or Claude Code in an empty project folder, or in an existing
Phaser game you want to improve. Then prompt the agent with the outcome you want and name the
director skill:

```text
Use phaser-game-director to build a premium 2D action-platformer from scratch.
Automatically use the relevant gameplay, graphics, UI, sprite generation, image generation,
audio, debug, and QA skills. Build a playable loop first, then iterate until it passes
browser, mobile, visual, UI, performance, and release checks.
```

## Optional API Keys

The core Phaser skills work without paid API keys. When keys are missing, the director should
report the credential probe output, skip external generation, and fall back to procedural/local
assets. Add keys only when you want the agent to generate external sprites, images, or audio.

Never commit API keys or put them in browser-side game code.

| Provider | Skill | Environment variable | Use cases |
| --- | --- | --- | --- |
| Gemini image API | `phaser-image-generator`, `phaser-sprite-generator` | `GEMINI_API_KEY` | Concept art, sprites, spritesheets, tilesets, textures, backgrounds, skies, decals, icons, logos, GUI art. |
| ElevenLabs API | `phaser-audio-generator` | `ELEVENLABS_API_KEY` | SFX, ambience loops, UI sounds, announcer lines, dialogue TTS, voice conversion, audio cleanup. |

Set keys in your shell profile, then restart your terminal:

```bash
export GEMINI_API_KEY="..."
export ELEVENLABS_API_KEY="..."
```

The director skill includes a credential probe that sources common shell profiles before
deciding a key is missing:

```bash
bash ~/.agents/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

> Note: there is no Tripo/3D-model key here. Phaser is a 2D engine; high-value 2D assets come
> from `phaser-sprite-generator` (spritesheets, tilesets, atlases) and `phaser-image-generator`.

## Skill System

- `phaser-game-director`: main entrypoint for complete game builds and orchestration.
- `phaser-gameplay-systems`: playable loop, scenes, mechanics, entities, input, Arcade/Matter physics, camera, and feel.
- `phaser-aaa-graphics-builder`: visual scorecard, sprite/atlas architecture, parallax, particles, pipelines/shaders, Lights2D, post-FX, render polish.
- `phaser-game-ui-designer`: HUDs, menus, overlays, responsive UI, Scale Manager, icons, safe areas, touch targets.
- `phaser-debug-profiler`: scene/runtime/render bugs, mobile/scale bugs, performance profiling, draw calls, texture/atlas memory.
- `phaser-qa-release`: browser QA, screenshots, canvas pixels, responsive checks, production build, release risk report.
- `phaser-sprite-generator`: spritesheets, tilesets, atlases, character/object/tile sprites, palette consistency (Gemini art → slice/pack).
- `phaser-image-generator`: Gemini image generation for concepts, textures, backgrounds, skies, icons, logos, GUI art, and title/menu art.
- `phaser-audio-generator`: ElevenLabs-backed SFX, ambience, UI sounds, voice/TTS, voice conversion, cleanup, and Phaser audio integration.

## Packaged Resources

- `skills/`: the full public package. Each skill owns its required `SKILL.md`, `references/`, `scripts/`, and `assets/`.
- `skills/phaser-gameplay-systems/assets/phaser-vite-game/`: packaged Phaser 3 game scaffold used when starting from an empty project.
- `skills/phaser-qa-release/scripts/inspect-phaser-canvas.mjs`: packaged browser/canvas inspection helper used by QA workflows.
- `scripts/`: local validation helpers for maintainers.
- `install.sh`: local installer for working on this checkout.

## Maintainer Checks

```bash
npm install
npm run check:scripts
npm run validate:skills
```

## License

MIT. See [LICENSE](LICENSE).
