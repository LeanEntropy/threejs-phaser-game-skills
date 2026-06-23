#!/usr/bin/env bash
set -euo pipefail

# Install BOTH skill suites with the same flags:
#   - Three.js (3D) skills at the repo root (./install.sh)
#   - Phaser (2D) skills under ./phaser (./phaser/install.sh)
#
# Usage: ./install-all.sh [--codex] [--claude] [--all] [--force] [--prune-managed]

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -eq 0 ]]; then
  echo "Usage: ./install-all.sh [--codex] [--claude] [--all] [--force] [--prune-managed]" >&2
  exit 1
fi

echo "=== Installing Three.js (3D) skills ==="
(cd "$script_dir" && ./install.sh "$@")

echo "=== Installing Phaser (2D) skills ==="
(cd "$script_dir/phaser" && ./install.sh "$@")

echo "Done. Use phaser-game-director for 2D games and threejs-game-director for 3D games."
