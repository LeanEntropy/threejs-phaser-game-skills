#!/usr/bin/env bash
# Load API keys from a config file into the current shell environment.
#
#   source ./load-keys.sh
#
# After sourcing, ALL skill scripts can see the keys — including the upstream
# Three.js scripts (Gemini / ElevenLabs / Tripo) that only read environment
# variables and which this fork deliberately does not modify.
#
# Config search order (first match per key wins; values already set in the
# environment are left untouched):
#   $GAME_SKILLS_ENV → ./.env → ~/.config/game-skills/.env → ~/.game-skills.env
#
# File format: KEY=value lines (optional `export ` prefix and quotes), e.g.
#   OPENAI_API_KEY=sk-...
#   GEMINI_API_KEY="..."
#   ELEVENLABS_API_KEY=...
#   TRIPO_API_KEY=...

_gs_load_keys() {
  local key f line val
  for key in OPENAI_API_KEY GEMINI_API_KEY ELEVENLABS_API_KEY TRIPO_API_KEY; do
    eval "val=\${$key:-}"
    [ -n "$val" ] && continue
    for f in "${GAME_SKILLS_ENV:-}" "$PWD/.env" "$HOME/.config/game-skills/.env" "$HOME/.game-skills.env"; do
      [ -n "$f" ] && [ -f "$f" ] || continue
      line="$(grep -E "^[[:space:]]*(export[[:space:]]+)?${key}=" "$f" 2>/dev/null | tail -n1 || true)"
      [ -n "$line" ] || continue
      val="${line#*=}"
      val="${val%\"}"; val="${val#\"}"
      val="${val%\'}"; val="${val#\'}"
      export "$key=$val"
      break
    done
  done
}

_gs_load_keys
unset -f _gs_load_keys
