# Phaser 3 (2D) Game Skills

This repository is a **fork** of
[majidmanzarpour/threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills)
that adds a parallel suite of skills for building **Phaser 3 (2D)** browser games.

**2D games → Phaser. 3D games → Three.js.**

- The original Three.js skills live at the repo root (`skills/`, `install.sh`, `README.md`) and
  are kept **pristine** so upstream updates merge cleanly.
- The Phaser suite lives entirely under [`phaser/`](phaser/) and is maintained in this fork.

## Layout

```
.
├── skills/                # Three.js (3D) skills — upstream, untouched
├── install.sh             # upstream Three.js installer
├── phaser/                # Phaser (2D) skills — added by this fork
│   ├── skills/            # the 9 phaser-* skills
│   ├── install.sh         # Phaser installer
│   ├── README.md          # Phaser suite docs
│   └── docs/              # design spec + 3D→2D translation brief
├── install-all.sh         # install BOTH suites with the same flags
└── PHASER.md              # this file
```

## Install

Both suites at once:

```bash
./install-all.sh --claude      # or --codex / --all  (add --force to overwrite)
```

Or just one:

```bash
./install.sh --claude          # Three.js (3D)
cd phaser && ./install.sh --claude   # Phaser (2D)
```

After installing, use `phaser-game-director` for 2D games and `threejs-game-director` for 3D
games. The director routes to the specialist skills automatically.

## Pulling updates from upstream (Three.js)

Because the upstream files are never modified here, updates merge cleanly:

```bash
git fetch upstream
git merge upstream/main        # or: git rebase upstream/main
```

`upstream` is the original repo; `origin` is this fork. If `upstream` is missing:

```bash
git remote add upstream https://github.com/majidmanzarpour/threejs-game-skills.git
```

## The Phaser suite (9 skills)

| Skill | Role |
| --- | --- |
| `phaser-game-director` | Primary entrypoint / orchestrator for 2D games |
| `phaser-gameplay-systems` | Playable loop, scenes, Arcade/Matter physics + Vite+TS+Phaser scaffold |
| `phaser-aaa-graphics-builder` | Parallax, particles, pipelines/postFX, Lights2D, juice, visual scorecard |
| `phaser-game-ui-designer` | HUDs, menus, Scale Manager, BitmapText, nineslice, touch UI |
| `phaser-debug-profiler` | Blank-canvas/scale/loader bugs, fps/batches/atlas-memory profiling |
| `phaser-qa-release` | Build, preview, base paths, canvas-pixel inspection, release report |
| `phaser-sprite-generator` | Spritesheets, tilesets, atlases (Gemini image API + local slice/pack) |
| `phaser-image-generator` | Concepts, backgrounds, skies, decals, icons, GUI art (Gemini) |
| `phaser-audio-generator` | SFX, ambience, UI sounds, voice (ElevenLabs) |

### Optional API keys

| Variable | Used by |
| --- | --- |
| `GEMINI_API_KEY` | `phaser-image-generator`, `phaser-sprite-generator` |
| `ELEVENLABS_API_KEY` | `phaser-audio-generator` |

The core skills work without keys and fall back to procedural/local assets. There is no Tripo /
3D key in the Phaser suite — Phaser is 2D.

## License

MIT, inherited from the upstream project. See [LICENSE](LICENSE).
