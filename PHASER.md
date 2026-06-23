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
| `OPENAI_API_KEY` | `phaser-image-generator`, `phaser-sprite-generator` (GPT-Image `gpt-image-1`) |
| `GEMINI_API_KEY` | `phaser-image-generator`, `phaser-sprite-generator` (Gemini) |
| `ELEVENLABS_API_KEY` | `phaser-audio-generator` |

The core skills work without keys and fall back to procedural/local assets. There is no Tripo /
3D key in the Phaser suite — Phaser is 2D. See **API keys & image providers** below for the
config file, provider selection, and how upstream Three.js scripts get config-file keys.

## API keys & image providers

All generator scripts (Phaser image/sprite/audio, plus the Three.js add-on) resolve keys in
order: **explicit flag → environment variable → a config file**. The config file is searched in
this order, first match per key wins:

```
$GAME_SKILLS_ENV → ./.env → ~/.config/game-skills/.env → ~/.game-skills.env
```

Copy the repo-root `.env.example` to one of those paths (real key files are gitignored) and fill
it in:

```
# API keys for game-skills generators. Copy to .env (gitignored) or ~/.config/game-skills/.env
OPENAI_API_KEY=        # OpenAI GPT-Image (gpt-image-1) — phaser image/sprite + threejs-image-generator-openai
GEMINI_API_KEY=        # Google Gemini — phaser image/sprite + upstream threejs-image-generator
ELEVENLABS_API_KEY=    # ElevenLabs — phaser/threejs audio generators
TRIPO_API_KEY=         # Tripo — upstream threejs-3d-generator (3D only)
```

### Provider selection (image/sprite generators)

The Phaser image and sprite generators support **two providers**, chosen with
`--provider {auto,openai,gemini}` (default `auto` = OpenAI when `OPENAI_API_KEY` resolves, else
Gemini):

- **OpenAI** `gpt-image-1` — `--size {1024x1024,1536x1024,1024x1536,auto}`,
  `--quality {low,medium,high,auto}`, `--background {transparent,opaque,auto}` (transparent is
  great for sprites/icons/decals).
- **Gemini** — `--resolution {1K,2K,4K}`.

### `threejs-image-generator-openai` add-on

`skills/threejs-image-generator-openai` is a repo-fork **add-on** that gives the Three.js side
GPT-Image without touching the upstream `threejs-image-generator` (which stays Gemini-only). It
is purely additive, so upstream updates still merge cleanly.

### Bridging config-file keys to upstream Three.js scripts

The **upstream Three.js scripts read environment variables only** — they do not read the config
file. To make config-file keys visible to them (and to any shell command), source the repo-root
helper, which exports `OPENAI_API_KEY` / `GEMINI_API_KEY` / `ELEVENLABS_API_KEY` / `TRIPO_API_KEY`
from the config file into the current shell:

```bash
source ./load-keys.sh
```

## License

MIT, inherited from the upstream project. See [LICENSE](LICENSE).
