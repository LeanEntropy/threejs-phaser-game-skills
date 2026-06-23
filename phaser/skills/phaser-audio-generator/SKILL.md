---
name: phaser-audio-generator
description: "Generate, convert, clean, and prepare audio assets for Phaser 3 (2D) browser games using ElevenLabs. Use for sound effects, looping ambience, UI sounds, jump/coin/hit/explosion/laser/powerup audio, platformer and top-down and shoot-em-up and arcade and roguelike SFX, boss stingers, announcer/dialogue TTS, scratch-performance voice conversion, voice cleanup/isolation, audio sprites, audio manifests, and game-ready Phaser sound integration."
---

# Phaser Audio Generator

## Purpose

Create game-ready audio assets for Phaser 3 projects. This skill consolidates game sound generation, voice generation/conversion, audio cleanup, credential probing, and runtime integration into one Phaser-focused production workflow.

Provider: ElevenLabs.

## When To Use

Use this skill for:

- SFX: jumps, hits, weapons, lasers, explosions, coins, pickups, collisions, brick/breakout bounces, UI clicks, confirms, errors.
- Ambience: wind, rain, city bed, engine hum, portal loop, dungeon room tone, arena beds for platformers, top-down, and arcade scenes.
- Voice: announcer barks, boss lines, tutorial prompts, menu narration, generated placeholder dialogue.
- Voice conversion: convert a scratch performance into a target character voice while preserving timing and emotion.
- Cleanup: isolate or denoise dialogue before voice conversion, TTS replacement, or transcription.
- Phaser integration: `this.load.audio` / `this.load.audioSprite` loading, `this.sound.add`/`play`, looping, audio sprite/manifest mapping, music vs SFX buses, Web Audio unlock on first input, pause/resume, volume/mute.

For premium/AAA/showcase game work, audio is not cosmetic. Generate or integrate at least a minimal interaction audio set for the main loop unless the user explicitly requests mute/offline-only output or credentials/API attempts are blocked.

## API Key

Never store API keys in skill files or browser/game code. The script resolves the key in this order:

1. `--api-key` (explicit flag)
2. `ELEVENLABS_API_KEY` environment variable
3. a config file (KEY=value lines), searched in order: `$GAME_SKILLS_ENV` → `./.env` → `~/.config/game-skills/.env` → `~/.game-skills.env`

Copy `.env.example` (repo root) to `.env` or `~/.config/game-skills/.env` to set `ELEVENLABS_API_KEY` via the config file instead of (or alongside) an env var.

Before declaring the key unavailable in a `phaser-game-director` workflow, run the director credential probe and paste its literal SET/MISSING output (it also checks the config file):

```bash
bash ~/.codex/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

For Claude installs:

```bash
bash ~/.claude/skills/phaser-game-director/scripts/probe_asset_credentials.sh
```

If the probe says `ELEVENLABS_API_KEY=SET` but the script sees no key, run through a shell that sources the user's profile:

```bash
zsh -c 'source "$HOME/.zprofile" 2>/dev/null; source "$HOME/.zshrc" 2>/dev/null; python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py probe'
```

## Required Reference

Load `references/audio-workflows.md` before building a game audio plan, generating multiple assets, wiring runtime audio, cleaning/converting voices, or claiming premium game audio.

Track it in the reference ledger. Do not mark the audio phase complete while this reference is skipped.

## Tool Script

Run from the user's current game project directory:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py --help
```

Claude install path:

```bash
python3 ~/.claude/skills/phaser-audio-generator/scripts/phaser_audio_asset.py --help
```

Probe:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py probe
```

Generate SFX:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py sfx \
  --prompt "tight arcade coin pickup, bright transient, short sparkling tail, 2D platformer" \
  --duration 1.2 \
  --prompt-influence 0.65 \
  --out public/assets/audio/sfx/coin-pickup.mp3
```

Generate looping ambience:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py sfx \
  --prompt "seamless overworld ambience for top-down adventure, soft wind, distant birds, gentle stream bed" \
  --duration 12 \
  --loop \
  --prompt-influence 0.45 \
  --out public/assets/audio/ambience/overworld-loop.mp3
```

Generate TTS/announcer line:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py tts \
  --text "New high score!" \
  --voice-id JBFqnCBsd6RMkjVDRZzb \
  --out public/assets/audio/voice/new-high-score.mp3
```

Clean dialogue:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py isolate \
  --input public/assets/audio/source/noisy-boss-line.wav \
  --out public/assets/audio/voice/boss-line-clean.mp3
```

Convert a scratch performance to a target voice:

```bash
python3 ~/.codex/skills/phaser-audio-generator/scripts/phaser_audio_asset.py voice-change \
  --input public/assets/audio/source/scratch-boss-line.wav \
  --voice-id JBFqnCBsd6RMkjVDRZzb \
  --remove-background-noise \
  --out public/assets/audio/voice/boss-line-final.mp3
```

## Game Audio Defaults

- SFX: `mp3_44100_128`, 0.5-2.5s, prompt influence `0.55-0.8`.
- UI: 0.15-0.8s, high prompt influence, keep transients clear.
- Ambience loops: 8-30s, `--loop`, prompt influence `0.3-0.55`.
- Voice: TTS for clean generated lines; voice-change when timing/acting from a scratch performance matters.
- Cleanup: isolate noisy speech before voice-change or final dialogue use.
- Output formats: ship web-friendly audio. The script emits MP3; provide an `.ogg` sibling when possible and load both so Phaser picks a supported codec: `this.load.audio('coin', ['coin.ogg', 'coin.mp3'])`.
- Runtime: generate locally, place files under `public/assets/audio/...` (or your Vite static dir), and load them via `this.load.audio` / `this.load.audioSprite`. Never put API keys in browser code.

## Required Report

Report:

- Credential probe output or real blocker.
- Reference ledger.
- Generated/processed file paths.
- Prompts/text/input files, voice IDs, durations, loop flags, and output formats (ogg + mp3 fallback).
- Runtime integration notes: load keys, sound buses (music vs SFX), trigger events, loop behavior, Web Audio unlock gesture, pause/resume, volume/mute controls, audio sprite mapping.
- Remaining audio gaps and any licensing/plan assumptions tied to the user's ElevenLabs account.
