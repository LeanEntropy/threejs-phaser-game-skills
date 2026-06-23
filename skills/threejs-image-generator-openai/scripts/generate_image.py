#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "openai>=1.50.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate 2D game images using either OpenAI (gpt-image-1) or Google Gemini.

Provider is auto-detected from available keys (OpenAI preferred when present),
or forced with --provider. API keys are resolved from, in order:
  1. --api-key / --openai-key / --gemini-key
  2. environment (OPENAI_API_KEY / GEMINI_API_KEY)
  3. a config file (see _config_paths): GAME_SKILLS_ENV, ./.env,
     ~/.config/game-skills/.env, ~/.game-skills.env  (KEY=value lines)

Usage:
    # auto provider (OpenAI if OPENAI_API_KEY present, else Gemini)
    python3 generate_image.py -p "pixel-art knight sprite, side view" -f knight.png

    # force OpenAI gpt-image-1 with a transparent background (great for sprites)
    python3 generate_image.py -p "coin icon" -f coin.png --provider openai --background transparent

    # force Gemini at 2K
    python3 generate_image.py -p "forest parallax background" -f bg.png --provider gemini -r 2K

    # image-to-image edit
    python3 generate_image.py -p "make it night-time" -f bg_night.png -i bg.png
"""

import argparse
import base64
import os
import sys
from pathlib import Path


# --------------------------------------------------------------------------- #
# Key / config resolution
# --------------------------------------------------------------------------- #
def _config_paths() -> list[Path]:
    """Search order for a KEY=value config file holding API keys."""
    paths: list[Path] = []
    explicit = os.environ.get("GAME_SKILLS_ENV")
    if explicit:
        paths.append(Path(explicit))
    paths.append(Path.cwd() / ".env")
    home = Path.home()
    paths.append(home / ".config" / "game-skills" / ".env")
    paths.append(home / ".game-skills.env")
    return paths


_CONFIG_KEYS: dict[str, str] | None = None


def _load_config_keys() -> dict[str, str]:
    """Parse the first readable config file(s); earliest path wins per key."""
    keys: dict[str, str] = {}
    for path in _config_paths():
        try:
            if not path.is_file():
                continue
            for raw in path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("export "):
                    line = line[len("export "):]
                if "=" not in line:
                    continue
                name, value = line.split("=", 1)
                name = name.strip()
                value = value.strip().strip('"').strip("'")
                if name and name not in keys:
                    keys[name] = value
        except OSError:
            continue
    return keys


def resolve_key(name: str, provided: str | None = None) -> str | None:
    """Resolve a key: explicit arg, then env var, then config file."""
    global _CONFIG_KEYS
    if provided:
        return provided
    env_value = os.environ.get(name)
    if env_value:
        return env_value
    if _CONFIG_KEYS is None:
        _CONFIG_KEYS = _load_config_keys()
    return _CONFIG_KEYS.get(name)


def resolve_provider(requested: str, openai_key: str | None, gemini_key: str | None) -> str | None:
    """Pick a provider: explicit request, else auto (OpenAI preferred)."""
    if requested and requested != "auto":
        return requested
    if openai_key:
        return "openai"
    if gemini_key:
        return "gemini"
    return None


# --------------------------------------------------------------------------- #
# Providers
# --------------------------------------------------------------------------- #
def generate_openai(args, api_key: str, output_path: Path) -> None:
    """Generate or edit an image with OpenAI gpt-image-1 (always base64)."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    model = args.model or "gpt-image-1"
    size = args.size or "1024x1024"
    background = args.background if args.background and args.background != "auto" else "auto"

    if args.input_image:
        print(f"Editing image with {model} ({size}, quality={args.quality})...")
        with open(args.input_image, "rb") as handle:
            result = client.images.edit(
                model=model,
                image=handle,
                prompt=args.prompt,
                size=size,
                quality=args.quality,
                background=background,
                input_fidelity="high",
            )
    else:
        print(f"Generating image with {model} ({size}, quality={args.quality})...")
        result = client.images.generate(
            model=model,
            prompt=args.prompt,
            size=size,
            quality=args.quality,
            background=background,
            output_format="png",
            n=1,
        )

    data = result.data or []
    b64 = data[0].b64_json if data else None
    if not b64:
        print("Error: OpenAI returned no image data.", file=sys.stderr)
        sys.exit(1)

    output_path.write_bytes(base64.b64decode(b64))
    print(f"\nImage saved: {output_path.resolve()}")


def generate_gemini(args, api_key: str, output_path: Path) -> None:
    """Generate or edit an image with Google's Gemini image model."""
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = genai.Client(api_key=api_key)

    input_image = None
    output_resolution = args.resolution
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")
            if args.resolution == "1K":  # default — auto-detect from input size
                width, height = input_image.size
                max_dim = max(width, height)
                if max_dim >= 3000:
                    output_resolution = "4K"
                elif max_dim >= 1500:
                    output_resolution = "2K"
                else:
                    output_resolution = "1K"
                print(f"Auto-detected resolution: {output_resolution} (from input {width}x{height})")
        except Exception as exc:
            print(f"Error loading input image: {exc}", file=sys.stderr)
            sys.exit(1)

    if input_image:
        contents = [input_image, args.prompt]
        print(f"Editing image with resolution {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    response = client.models.generate_content(
        model=args.model or "gemini-3-pro-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size=output_resolution),
        ),
    )

    from io import BytesIO

    image_saved = False
    for part in response.parts:
        if part.text is not None:
            print(f"Model response: {part.text}")
        elif part.inline_data is not None:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data)
            image = PILImage.open(BytesIO(image_data))
            if image.mode == "RGBA":
                rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                rgb_image.save(str(output_path), "PNG")
            elif image.mode == "RGB":
                image.save(str(output_path), "PNG")
            else:
                image.convert("RGB").save(str(output_path), "PNG")
            image_saved = True

    if image_saved:
        print(f"\nImage saved: {output_path.resolve()}")
    else:
        print("Error: No image was generated in the response.", file=sys.stderr)
        sys.exit(1)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate 2D game images with OpenAI (gpt-image-1) or Gemini."
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image description/prompt")
    parser.add_argument("--filename", "-f", required=True, help="Output filename (e.g., knight.png)")
    parser.add_argument("--input-image", "-i", help="Optional input image path for editing")
    parser.add_argument(
        "--provider",
        choices=["auto", "openai", "gemini"],
        default="auto",
        help="Image provider. 'auto' (default) prefers OpenAI when a key is present.",
    )
    parser.add_argument("--model", help="Override the model id (e.g. gpt-image-1, gpt-image-1-mini).")
    # OpenAI options
    parser.add_argument(
        "--size",
        choices=["1024x1024", "1536x1024", "1024x1536", "auto"],
        default="1024x1024",
        help="[OpenAI] Output size (square/landscape/portrait/auto).",
    )
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high", "auto"],
        default="high",
        help="[OpenAI] Render quality.",
    )
    parser.add_argument(
        "--background",
        choices=["transparent", "opaque", "auto"],
        default="auto",
        help="[OpenAI] Background; 'transparent' is ideal for sprites/icons.",
    )
    # Gemini options
    parser.add_argument(
        "--resolution",
        "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="[Gemini] Output resolution.",
    )
    # Keys
    parser.add_argument("--api-key", "-k", help="API key for the selected provider (overrides env/config).")
    parser.add_argument("--openai-key", help="OpenAI API key override.")
    parser.add_argument("--gemini-key", help="Gemini API key override.")

    args = parser.parse_args()

    openai_key = resolve_key("OPENAI_API_KEY", args.openai_key)
    gemini_key = resolve_key("GEMINI_API_KEY", args.gemini_key)

    provider = resolve_provider(args.provider, openai_key, gemini_key)
    if provider is None:
        print("Error: No image API key found.", file=sys.stderr)
        print("Provide one of:", file=sys.stderr)
        print("  - --api-key / --openai-key / --gemini-key", file=sys.stderr)
        print("  - env OPENAI_API_KEY or GEMINI_API_KEY", file=sys.stderr)
        print("  - a config file: ./.env, ~/.config/game-skills/.env, ~/.game-skills.env,", file=sys.stderr)
        print("    or the path in $GAME_SKILLS_ENV (KEY=value lines)", file=sys.stderr)
        sys.exit(1)

    if provider == "openai":
        key = args.api_key or openai_key
        if not key:
            print("Error: provider 'openai' selected but no OPENAI_API_KEY found.", file=sys.stderr)
            sys.exit(1)
    else:
        key = args.api_key or gemini_key
        if not key:
            print("Error: provider 'gemini' selected but no GEMINI_API_KEY found.", file=sys.stderr)
            sys.exit(1)

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if provider == "openai":
            generate_openai(args, key, output_path)
        else:
            generate_gemini(args, key, output_path)
    except Exception as exc:
        print(f"Error generating image ({provider}): {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
