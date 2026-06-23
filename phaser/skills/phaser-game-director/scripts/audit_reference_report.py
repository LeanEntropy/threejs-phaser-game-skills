#!/usr/bin/env python3
"""Audit a Phaser 3 game director final report for required skill evidence."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


BASE_REQUIRED = [
    "skill-loading ledger",
    "reference ledger",
    "phase ledger",
    "gameplay systems",
    "aaa graphics",
    "ui",
    "debug/profile",
    "qa/release",
]

PHYSICS_MARKERS = [
    "physics engine",
    "timestep",
    "collider",
]

PREMIUM_SCORECARD = [
    "art direction",
    "hero/player",
    "obstacles/enemies",
    "rewards/interactables",
    "world/environment",
    "materials/textures",
    "lighting/render",
    "vfx/motion",
    "ui/hud",
    "performance evidence",
    "average",
    "automatic failures",
]

# Only require that an asset-sourcing DECISION is recorded. Procedural/local art is
# a complete answer; external generators are optional, so we never require credential
# probes, generator-skill mentions, or generated-output evidence here.
PREMIUM_ASSET_SOURCING = [
    "external asset sourcing",
    "chosen sources",
]

PREMIUM_AUDIO = [
    "audio",
]

EXTERNAL_OUTPUT_PATTERNS = [
    re.compile(r"\b[\w./-]*assets/(sprites|spritesheets|atlases|tilesets|concepts|textures|ui|images|audio)/[\w./-]+\.(png|jpg|jpeg|webp|json|xml|mp3|wav|ogg|m4a)\b"),
    re.compile(r"\b[\w./-]+\.(png|jpg|jpeg|webp)\b.*\b[\w./-]+\.json\b"),
    re.compile(r"\b[\w./-]+\.(atlas\.json|sheet\.png|atlas\.png)\b"),
]

AUDIO_OUTPUT_PATTERNS = [
    re.compile(r"\b[\w./-]*assets/audio/[\w./-]+\.(mp3|wav|ogg|m4a)\b"),
]

NON_CREDENTIAL_BLOCKER_MARKERS = [
    "api error",
    "network error",
    "quota",
    "offline-only",
    "offline only",
    "user requested no external",
    "no external ai",
    "no external assets",
]

VERIFICATION_MARKERS = [
    "build",
    "console",
    "page error",
    "desktop",
    "mobile",
    "screenshot",
    "canvas",
    "pixel",
]


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("skill loading ledger", "skill-loading ledger")
    text = text.replace("skill loaded ledger", "skill-loading ledger")
    text = text.replace("reference loading ledger", "reference ledger")
    text = text.replace("asset sourcing ledger", "external asset sourcing")
    text = text.replace("external asset ledger", "external asset sourcing")
    text = text.replace("phaser-sprite-generator", "sprite generator")
    text = text.replace("phaser-image-generator", "image generator")
    text = text.replace("phaser-audio-generator", "audio generator")
    text = text.replace("spritesheet generation", "sprite generator")
    text = text.replace("spritesheet assets", "sprite generator")
    text = text.replace("sprite sheet generator", "sprite generator")
    text = text.replace("atlas generator", "sprite generator")
    text = text.replace("tileset generator", "sprite generator")
    text = text.replace("nano banana pro", "image generator")
    text = text.replace("nano banana", "image generator")
    text = text.replace("nanobanana", "image generator")
    text = text.replace("nano-banana", "image generator")
    text = text.replace("phase-execution ledger", "phase ledger")
    text = text.replace("phase execution ledger", "phase ledger")
    text = text.replace("debug and profile", "debug/profile")
    text = text.replace("debug profile", "debug/profile")
    text = text.replace("qa and release", "qa/release")
    text = text.replace("qa release", "qa/release")
    text = text.replace("page errors", "page error")
    return re.sub(r"\s+", " ", text)


def missing_markers(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def has_external_output_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in EXTERNAL_OUTPUT_PATTERNS)


def has_audio_output_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in AUDIO_OUTPUT_PATTERNS)


def has_external_blocker(text: str) -> bool:
    credential_missing = "gemini_api_key=missing" in text
    non_credential_blocker = any(marker in text for marker in NON_CREDENTIAL_BLOCKER_MARKERS)
    return credential_missing or non_credential_blocker


def has_audio_blocker(text: str) -> bool:
    return "elevenlabs_api_key=missing" in text or any(marker in text for marker in NON_CREDENTIAL_BLOCKER_MARKERS)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check that a Phaser 3 director final report includes required ledgers, scorecard, and verification evidence."
    )
    parser.add_argument("report", help="Path to the markdown/text final report draft.")
    parser.add_argument(
        "--premium",
        action="store_true",
        help="Require the premium/AAA visual scorecard and full verification evidence.",
    )
    parser.add_argument(
        "--physics",
        action="store_true",
        help="Require physics engine choice and diagnostics evidence.",
    )
    parser.add_argument(
        "--audio",
        action="store_true",
        help="Check the audio decision is addressed (generated, blocked, or explicitly omitted).",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Missing report file: {report_path}", file=sys.stderr)
        return 1

    text = normalize(report_path.read_text(encoding="utf-8"))
    missing = missing_markers(text, BASE_REQUIRED)

    if args.premium:
        missing.extend(missing_markers(text, PREMIUM_SCORECARD))
        missing.extend(missing_markers(text, PREMIUM_ASSET_SOURCING))
        missing.extend(missing_markers(text, VERIFICATION_MARKERS))
        # Procedural/local art is fully acceptable: no external/generated evidence required.

    if args.physics:
        missing.extend(missing_markers(text, PHYSICS_MARKERS))

    if args.audio:
        missing.extend(missing_markers(text, PREMIUM_AUDIO))
        # Audio is optional. Pass if it was generated, blocked, or explicitly omitted.
        audio_ok = (
            has_audio_output_evidence(text)
            or has_audio_blocker(text)
            or any(m in text for m in ("no audio", "silent", "procedural audio", "audio omitted", "without audio"))
        )
        if not audio_ok:
            missing.append("audio decision addressed (generated, blocked, or explicitly omitted)")

    if missing:
        print("Director report audit failed. Missing required markers:")
        for marker in missing:
            print(f"- {marker}")
        return 1

    print("Director report audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
