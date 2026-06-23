#!/usr/bin/env bash
set -euo pipefail

# Reports SET/MISSING for the image/audio API keys, never the secret values.
# A key counts as SET if it is exported in the environment (after sourcing shell
# profiles) OR present in a config file. Config search order:
#   $GAME_SKILLS_ENV, ./.env, ~/.config/game-skills/.env, ~/.game-skills.env

PROBE='
_has() {
  local key="$1" f
  eval "local val=\${$key:-}"
  if [ -n "$val" ]; then return 0; fi
  for f in "${GAME_SKILLS_ENV:-}" "$PWD/.env" "$HOME/.config/game-skills/.env" "$HOME/.game-skills.env"; do
    [ -n "$f" ] && [ -f "$f" ] || continue
    if grep -Eq "^[[:space:]]*(export[[:space:]]+)?${key}=[^[:space:]]" "$f" 2>/dev/null; then
      return 0
    fi
  done
  return 1
}
for key in GEMINI_API_KEY OPENAI_API_KEY ELEVENLABS_API_KEY; do
  if _has "$key"; then printf "%s=SET\n" "$key"; else printf "%s=MISSING\n" "$key"; fi
done
'

if command -v zsh >/dev/null 2>&1; then
  zsh -lc 'source "$HOME/.zprofile" >/dev/null 2>&1 || true; source "$HOME/.zshrc" >/dev/null 2>&1 || true; '"$PROBE"
else
  bash -lc 'source "$HOME/.bash_profile" >/dev/null 2>&1 || true; source "$HOME/.bashrc" >/dev/null 2>&1 || true; '"$PROBE"
fi
