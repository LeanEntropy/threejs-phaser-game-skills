# Phaser 2D Game Skills — Design Spec

Date: 2026-06-21
Status: Approved (design), in implementation

## Goal

Produce a Phaser 3 (2D) mirror of the existing Three.js game-skills suite, delivered as a
dual repository so the upstream Three.js skills stay cleanly updatable while the new Phaser
skills live alongside. Routing intent: **2D games → Phaser, 3D games → Three.js**.

## Repository structure

The current working directory was the Three.js upstream clone. It is nested so its `.git`
(origin → `majidmanzarpour/threejs-game-skills`) stays intact and `git pull` continues to
update it.

```
prototypes/
├── threejs-game-skills/      # upstream clone, .git intact → `git pull` updates it
├── phaser-game-skills/       # NEW, ours — mirrors threejs repo layout
│   ├── skills/
│   ├── scripts/              # validate-skills.sh, check-python-syntax.py
│   ├── install.sh
│   ├── package.json
│   ├── README.md / AGENTS.md / LICENSE / .gitignore
├── docs/superpowers/specs/   # this spec
├── install-all.sh            # installs both suites to Claude/Codex
├── update-threejs.sh         # convenience: cd threejs-game-skills && git pull
└── README.md                 # explains dual layout
```

The parent stays a plain workspace (not a nested git repo) to avoid submodule complexity. If
the parent is later `git init`-ed, `threejs-game-skills/` is gitignored.

## Skill mapping (9 skills, `phaser-` prefix)

| Three.js | Phaser 3 | Translation notes |
|---|---|---|
| threejs-game-director | phaser-game-director | orchestrates Phaser siblings; probe drops Tripo, keeps Gemini + ElevenLabs |
| threejs-gameplay-systems | phaser-gameplay-systems | Scenes, Arcade vs Matter selection, input, tweens, pooling, tilemaps; owns the scaffold |
| threejs-aaa-graphics-builder | phaser-aaa-graphics-builder | parallax, particles, pipelines/shaders, Lights2D, post-FX, screen shake; 2D visual scorecard (AAA framing kept) |
| threejs-game-ui-designer | phaser-game-ui-designer | Scale Manager (FIT/RESIZE), DOM vs bitmap text, nineslice, safe areas, touch targets |
| threejs-debug-profiler | phaser-debug-profiler | arcade debug, FPS/loop, texture/atlas memory, batching/draw calls, mobile/scale bugs |
| threejs-qa-release | phaser-qa-release | vite build/preview, canvas-pixel inspection, responsive, base paths |
| threejs-3d-generator | phaser-sprite-generator | spritesheets, tilesets, atlases, palette consistency (Gemini art → slice/pack) |
| threejs-image-generator | phaser-image-generator | Gemini, reframed for sprites/tilesets/backgrounds/UI art |
| threejs-audio-generator | phaser-audio-generator | ElevenLabs, unchanged credential model |

Each skill reproduces the source shape: `SKILL.md` + `references/` (checklists, recipes,
prompt-templates, workflows as applicable) + `scripts/` where the source has them +
`agents/openai.yaml`.

## Scaffold: `phaser-vite-game`

Vite + TypeScript + Phaser 3, mirroring the Three.js scaffold structure with a first playable
loop (move + collect + HUD) running out of the box:

- `index.html`, `package.json`, `vite.config.ts`, `tsconfig.json`, `playwright.config.ts`
- `src/main.ts` — boot `Phaser.Game`
- `src/game/GameConfig.ts` — scale + physics + scene list
- `src/scenes/{Boot,Preload,Play}Scene.ts`
- `src/entities/{Player,Pickup}.ts`
- `src/systems/{InputController,CameraRig,AudioSystem,Hud,DebugTools}.ts`
- `src/utils/`, `src/styles.css`
- `tests/visual.spec.ts`, `scripts/inspect-phaser-canvas.mjs`

## Credentials

Env-var model: `GEMINI_API_KEY` (sprite + image) and `ELEVENLABS_API_KEY` (audio). No
`TRIPO_API_KEY` — there is no 3D path. Director credential probe updated to those two.

## Build approach

1. Restructure repo (done).
2. Author shared 3D→2D translation brief + current Phaser 3 conventions (verified via context7).
3. Build the `phaser-vite-game` scaffold by hand.
4. Author the director by hand; dispatch parallel subagents for the other 8 skills, each given
   its Three.js source as a template plus the shared brief.
5. Validate: scaffold typecheck/build, repo `validate:skills`.
6. Install both suites into `~/.claude/skills`.

## Non-goals

- No Phaser 2 / CE or Phaser 4 support.
- No Tripo / 3D asset generation in the Phaser suite.
- No changes to the Three.js skills' content (kept pristine for upstream updates).
