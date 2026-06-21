#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate game-ready 2D art for Phaser 3 using Google's Gemini image API plus
local Pillow (PIL) image processing.

Three subcommands:

  generate  Call the Gemini image API to produce source art (a single sprite,
            an object/enemy, a uniform-frame spritesheet, or a tileset page).
            Optionally enforce a transparent background and auto-trim margins.

  sheet     Slice a uniform grid spritesheet PNG into individual frames, OR
            normalize an existing sheet (trim transparency, recolor key color
            to alpha). Emits frames AND a Phaser spritesheet frameConfig hint.

  atlas     Pack a folder of frame PNGs into a single atlas PNG plus a
            TexturePacker-style JSON Hash file that `this.load.atlas` accepts.

Pillow is required for slicing/packing/trimming. If it is missing, `generate`
still saves the raw image from Gemini and prints a clear message; `sheet` and
`atlas` exit with an actionable install hint.

Usage:
    uv run phaser_sprite_asset.py generate \
        --prompt "8-frame run cycle, side view pixel-art knight" \
        --filename assets/src/knight-run.png \
        --transparent --columns 8 --rows 1

    uv run phaser_sprite_asset.py sheet \
        --image assets/src/knight-run.png --columns 8 --rows 1 \
        --out-dir assets/frames/knight-run

    uv run phaser_sprite_asset.py atlas \
        --frames-dir assets/frames/knight-run \
        --out assets/atlas/knight --padding 2 --trim
"""

import argparse
import json
import os
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# API key handling (ported from the image-generator pattern)
# ---------------------------------------------------------------------------
def get_api_key(provided_key):
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def require_api_key(provided_key):
    api_key = get_api_key(provided_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GEMINI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)
    return api_key


# ---------------------------------------------------------------------------
# Pillow availability (graceful degradation)
# ---------------------------------------------------------------------------
def try_import_pillow():
    """Return the PIL.Image module or None if Pillow is not installed."""
    try:
        from PIL import Image as PILImage  # noqa: F401
        return PILImage
    except Exception:
        return None


def require_pillow():
    PILImage = try_import_pillow()
    if PILImage is None:
        print("Error: Pillow (PIL) is required for this operation.", file=sys.stderr)
        print("Install it with one of:", file=sys.stderr)
        print("  pip install pillow", file=sys.stderr)
        print("  uv run phaser_sprite_asset.py ...  (uv resolves the dependency)", file=sys.stderr)
        sys.exit(1)
    return PILImage


# ---------------------------------------------------------------------------
# Transparency helpers
# ---------------------------------------------------------------------------
def hex_to_rgb(value):
    """Parse '#rrggbb' / 'rrggbb' into an (r, g, b) tuple."""
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Expected a 6-digit hex color, got: {value!r}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def color_key_to_alpha(image, key_rgb, tolerance, PILImage):
    """Make pixels matching key_rgb (within tolerance) fully transparent."""
    image = image.convert("RGBA")
    datas = image.getdata()
    kr, kg, kb = key_rgb
    new_data = []
    for r, g, b, a in datas:
        if abs(r - kr) <= tolerance and abs(g - kg) <= tolerance and abs(b - kb) <= tolerance:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    image.putdata(new_data)
    return image


def trim_to_content(image, PILImage):
    """Crop transparent margins. Returns (cropped_image, (left, top))."""
    image = image.convert("RGBA")
    bbox = image.getbbox()  # bbox of non-zero (non-transparent) region
    if bbox is None:
        return image, (0, 0)
    cropped = image.crop(bbox)
    return cropped, (bbox[0], bbox[1])


# ---------------------------------------------------------------------------
# Subcommand: generate
# ---------------------------------------------------------------------------
def cmd_generate(args):
    api_key = require_api_key(args.api_key)

    # Import here after the key check to avoid a slow import on error.
    from google import genai
    from google.genai import types
    from io import BytesIO

    PILImage = try_import_pillow()  # optional for generate

    client = genai.Client(api_key=api_key)

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build a sprite-aware prompt. Transparent-background and grid hints make
    # Gemini output far more usable as game art.
    prompt = args.prompt
    extra = []
    if args.transparent:
        extra.append(
            "transparent background (PNG alpha, no checkerboard, no backdrop, "
            "no ground shadow plate)"
        )
    if args.columns and args.rows and (args.columns > 1 or args.rows > 1):
        extra.append(
            f"arranged as a uniform {args.columns}x{args.rows} grid spritesheet, "
            "every frame the same cell size, identical pivot and scale per cell, "
            "evenly spaced, no gaps, no frame numbers, no labels"
        )
    extra.append(
        "game-ready 2D sprite art, clean readable silhouette, consistent palette, "
        "centered, no text, no watermark"
    )
    if args.style:
        extra.append(args.style)
    full_prompt = prompt + ". " + ", ".join(extra) + "."

    # Optional input image for edit/variation (same pattern as image-generator).
    input_image = None
    if args.input_image:
        if PILImage is None:
            print("Error: --input-image requires Pillow.", file=sys.stderr)
            sys.exit(1)
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")
        except Exception as e:
            print(f"Error loading input image: {e}", file=sys.stderr)
            sys.exit(1)

    contents = [input_image, full_prompt] if input_image is not None else full_prompt
    print(f"Generating sprite art at {args.resolution}...")

    try:
        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size=args.resolution),
            ),
        )
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)

    image_saved = False
    for part in response.parts:
        if part.text is not None:
            print(f"Model response: {part.text}")
        elif part.inline_data is not None:
            image_data = part.inline_data.data
            if isinstance(image_data, str):
                import base64
                image_data = base64.b64decode(image_data)

            if PILImage is None:
                # Degrade gracefully: write the raw bytes, skip processing.
                output_path.write_bytes(image_data)
                print(
                    "Note: Pillow is not installed. Saved the raw generated image "
                    "without alpha enforcement, trimming, or slicing.",
                    file=sys.stderr,
                )
                print("Install Pillow to enable --transparent/--trim and the "
                      "sheet/atlas subcommands: pip install pillow", file=sys.stderr)
                image_saved = True
                continue

            image = PILImage.open(BytesIO(image_data)).convert("RGBA")

            # Enforce transparent background by keying out the dominant corner
            # color when requested (Gemini often returns a near-solid backdrop).
            if args.transparent:
                key = hex_to_rgb(args.key_color) if args.key_color else image.getpixel((0, 0))[:3]
                image = color_key_to_alpha(image, key, args.tolerance, PILImage)

            if args.trim:
                image, _ = trim_to_content(image, PILImage)

            image.save(str(output_path), "PNG")
            image_saved = True

    if image_saved:
        print(f"\nImage saved: {output_path.resolve()}")
        if args.columns and args.rows and (args.columns > 1 or args.rows > 1):
            print(
                "Next: slice into frames with\n"
                f"  phaser_sprite_asset.py sheet --image {output_path} "
                f"--columns {args.columns} --rows {args.rows} "
                f"--out-dir {output_path.with_suffix('')}-frames"
            )
    else:
        print("Error: No image was generated in the response.", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Subcommand: sheet (slice a uniform grid OR normalize a sheet)
# ---------------------------------------------------------------------------
def cmd_sheet(args):
    PILImage = require_pillow()

    src = Path(args.image)
    if not src.exists():
        print(f"Error: image not found: {src}", file=sys.stderr)
        sys.exit(1)

    image = PILImage.open(src).convert("RGBA")
    w, h = image.size

    if args.key_color:
        image = color_key_to_alpha(image, hex_to_rgb(args.key_color), args.tolerance, PILImage)

    # Determine the cell size from explicit frame size or from columns/rows.
    if args.frame_width and args.frame_height:
        fw, fh = args.frame_width, args.frame_height
        cols = w // fw
        rows = h // fh
    elif args.columns and args.rows:
        cols, rows = args.columns, args.rows
        if w % cols != 0 or h % rows != 0:
            print(
                f"Warning: sheet {w}x{h} does not divide evenly into {cols}x{rows} "
                f"(cell {w / cols:.2f}x{h / rows:.2f}). Frames may be misaligned. "
                "Pass --frame-width/--frame-height for an exact cell size.",
                file=sys.stderr,
            )
        fw, fh = w // cols, h // rows
    else:
        print("Error: provide --columns and --rows, or --frame-width and --frame-height.",
              file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    margin = args.margin
    spacing = args.spacing
    name = args.name or src.stem

    count = 0
    for row in range(rows):
        for col in range(cols):
            left = margin + col * (fw + spacing)
            top = margin + row * (fh + spacing)
            frame = image.crop((left, top, left + fw, top + fh))
            if args.trim:
                frame, _ = trim_to_content(frame, PILImage)
            frame_path = out_dir / f"{name}_{count:03d}.png"
            frame.save(str(frame_path), "PNG")
            count += 1

    print(f"Sliced {count} frames ({fw}x{fh}) into {out_dir.resolve()}")
    print("\nPhaser spritesheet load (frameConfig):")
    print(f"  this.load.spritesheet('{name}', '{src.name}', {{")
    print(f"    frameWidth: {fw}, frameHeight: {fh},")
    if margin:
        print(f"    margin: {margin},")
    if spacing:
        print(f"    spacing: {spacing},")
    print(f"    endFrame: {count - 1}")
    print("  });")
    print("\nOr pack the frames into an atlas:")
    print(f"  phaser_sprite_asset.py atlas --frames-dir {out_dir} --out assets/atlas/{name}")


# ---------------------------------------------------------------------------
# Subcommand: atlas (pack frames -> PNG + TexturePacker JSON Hash)
# ---------------------------------------------------------------------------
def cmd_atlas(args):
    PILImage = require_pillow()

    frames_dir = Path(args.frames_dir)
    if not frames_dir.is_dir():
        print(f"Error: frames dir not found: {frames_dir}", file=sys.stderr)
        sys.exit(1)

    exts = {".png", ".PNG"}
    files = sorted(p for p in frames_dir.iterdir() if p.suffix in exts)
    if not files:
        print(f"Error: no PNG frames in {frames_dir}", file=sys.stderr)
        sys.exit(1)

    padding = args.padding

    # Load every frame; optionally trim, tracking the source-size offset so
    # Phaser can re-expand to the original frame box (spriteSourceSize).
    loaded = []  # (frame_name, trimmed_img, orig_w, orig_h, off_x, off_y)
    for f in files:
        img = PILImage.open(f).convert("RGBA")
        ow, oh = img.size
        if args.trim:
            trimmed, (ox, oy) = trim_to_content(img, PILImage)
        else:
            trimmed, (ox, oy) = img, (0, 0)
        loaded.append((f.name, trimmed, ow, oh, ox, oy))

    # Simple shelf packer: place frames row by row, wrapping at a target width.
    # Target width defaults to the next power-of-two near the square root of
    # total area for a reasonably square, GPU-friendly atlas.
    total_area = sum((im.size[0] + padding) * (im.size[1] + padding) for _, im, *_ in loaded)
    import math
    target_w = args.max_width or max(
        max(im.size[0] for _, im, *_ in loaded) + padding * 2,
        _next_pow2(int(math.sqrt(total_area))),
    )

    placements = []  # (name, x, y, img, ow, oh, ox, oy)
    x = padding
    y = padding
    row_h = 0
    atlas_w = 0
    for name, im, ow, oh, ox, oy in loaded:
        fw, fh = im.size
        if x + fw + padding > target_w and x > padding:
            x = padding
            y += row_h + padding
            row_h = 0
        placements.append((name, x, y, im, ow, oh, ox, oy))
        x += fw + padding
        row_h = max(row_h, fh)
        atlas_w = max(atlas_w, x)
    atlas_h = y + row_h + padding

    if args.pot:
        atlas_w = _next_pow2(atlas_w)
        atlas_h = _next_pow2(atlas_h)

    atlas = PILImage.new("RGBA", (atlas_w, atlas_h), (0, 0, 0, 0))
    frames_json = {}
    for name, px, py, im, ow, oh, ox, oy in placements:
        atlas.paste(im, (px, py))
        fw, fh = im.size
        frames_json[name] = {
            "frame": {"x": px, "y": py, "w": fw, "h": fh},
            "rotated": False,
            "trimmed": bool(args.trim and (fw != ow or fh != oh)),
            "spriteSourceSize": {"x": ox, "y": oy, "w": fw, "h": fh},
            "sourceSize": {"w": ow, "h": oh},
        }

    out_base = Path(args.out)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    png_path = out_base.with_suffix(".png")
    json_path = out_base.with_suffix(".json")

    atlas.save(str(png_path), "PNG")

    # TexturePacker "JSON (Hash)" layout — accepted by this.load.atlas.
    doc = {
        "frames": frames_json,
        "meta": {
            "app": "phaser_sprite_asset.py",
            "version": "1.0",
            "image": png_path.name,
            "format": "RGBA8888",
            "size": {"w": atlas_w, "h": atlas_h},
            "scale": "1",
        },
    }
    json_path.write_text(json.dumps(doc, indent=2))

    print(f"Packed {len(placements)} frames into {png_path.resolve()} ({atlas_w}x{atlas_h})")
    print(f"Atlas JSON (TexturePacker Hash): {json_path.resolve()}")
    print("\nPhaser atlas load:")
    print(f"  this.load.atlas('{out_base.stem}', '{png_path.name}', '{json_path.name}');")
    print("\nFrame names are the original file names, e.g.:")
    for name in list(frames_json)[:3]:
        print(f"  this.add.sprite(x, y, '{out_base.stem}', '{name}');")


def _next_pow2(n):
    p = 1
    while p < n:
        p <<= 1
    return p


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate and process 2D game art for Phaser 3 (Gemini + Pillow)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- generate ---
    g = sub.add_parser("generate", help="Generate source art with the Gemini image API")
    g.add_argument("--prompt", "-p", required=True, help="Sprite/sheet/tileset description")
    g.add_argument("--filename", "-f", required=True, help="Output PNG path")
    g.add_argument("--input-image", "-i", help="Optional input image for edit/variation")
    g.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], default="1K",
                   help="Output resolution (default 1K)")
    g.add_argument("--style", help="Extra style clause (e.g. 'crisp pixel art, 32x32')")
    g.add_argument("--columns", type=int, default=0,
                   help="Spritesheet columns (adds grid-layout instructions)")
    g.add_argument("--rows", type=int, default=0,
                   help="Spritesheet rows (adds grid-layout instructions)")
    g.add_argument("--transparent", action="store_true",
                   help="Request + enforce a transparent background (corner color keyed to alpha)")
    g.add_argument("--key-color", help="Hex bg color to make transparent (default: top-left pixel)")
    g.add_argument("--tolerance", type=int, default=24,
                   help="Color-key match tolerance per channel (default 24)")
    g.add_argument("--trim", action="store_true", help="Crop transparent margins after generation")
    g.add_argument("--api-key", "-k", help="Gemini API key (overrides GEMINI_API_KEY)")
    g.set_defaults(func=cmd_generate)

    # --- sheet ---
    s = sub.add_parser("sheet", help="Slice a uniform grid sheet into frames")
    s.add_argument("--image", "-i", required=True, help="Source spritesheet PNG")
    s.add_argument("--out-dir", "-o", required=True, help="Directory for sliced frames")
    s.add_argument("--columns", type=int, help="Number of columns in the grid")
    s.add_argument("--rows", type=int, help="Number of rows in the grid")
    s.add_argument("--frame-width", type=int, help="Exact cell width (overrides columns math)")
    s.add_argument("--frame-height", type=int, help="Exact cell height (overrides rows math)")
    s.add_argument("--margin", type=int, default=0, help="Outer margin before the first cell")
    s.add_argument("--spacing", type=int, default=0, help="Gap between cells")
    s.add_argument("--name", help="Frame base name (default: source stem)")
    s.add_argument("--key-color", help="Hex color to key to alpha before slicing")
    s.add_argument("--tolerance", type=int, default=24, help="Color-key tolerance (default 24)")
    s.add_argument("--trim", action="store_true", help="Trim each frame's transparent margins")
    s.set_defaults(func=cmd_sheet)

    # --- atlas ---
    a = sub.add_parser("atlas", help="Pack a folder of frames into an atlas PNG + JSON")
    a.add_argument("--frames-dir", required=True, help="Folder of PNG frames to pack")
    a.add_argument("--out", required=True, help="Output base path (.png + .json appended)")
    a.add_argument("--padding", type=int, default=2, help="Pixels between packed frames (default 2)")
    a.add_argument("--max-width", type=int, help="Max atlas width before wrapping a new shelf row")
    a.add_argument("--trim", action="store_true",
                   help="Trim each frame and record spriteSourceSize for Phaser re-expansion")
    a.add_argument("--pot", action="store_true", help="Round atlas dimensions up to powers of two")
    a.set_defaults(func=cmd_atlas)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
