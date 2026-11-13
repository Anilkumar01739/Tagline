#!/usr/bin/env python3
"""Render TagLine launcher icons (PNG + ICO) for desktop and Android."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow: pip install pillow")

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "assets" / "icons"
ANDROID_RES = ROOT / "src" / "crates" / "tagline-android" / "res"

ANDROID_SIZES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

DESKTOP_SIZES = (16, 32, 64, 128, 256, 512)


def _load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path(r"C:\Windows\Fonts\segoeuib.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    for path in candidates:
        if path.is_file():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def render_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    radius = int(size * 0.21)
    margin = int(size * 0.047)
    draw.rounded_rectangle(
        (margin, margin, size - margin - 1, size - margin - 1),
        radius=radius,
        fill=(18, 19, 26, 255),
        outline=(46, 232, 199, 90),
        width=max(1, size // 170),
    )

    font = _load_font(int(size * 0.36))
    t_bbox = draw.textbbox((0, 0), "T", font=font)
    t_w = t_bbox[2] - t_bbox[0]
    t_h = t_bbox[3] - t_bbox[1]
    l_bbox = draw.textbbox((0, 0), "L", font=font)
    l_w = l_bbox[2] - l_bbox[0]
    gap = int(size * 0.02)
    total_w = t_w + gap + l_w
    x0 = (size - total_w) // 2
    y0 = (size - t_h) // 2 - int(size * 0.04)

    draw.text((x0, y0), "T", font=font, fill=(244, 245, 247, 255))
    draw.text((x0 + t_w + gap, y0), "L", font=font, fill=(46, 232, 199, 235))

    bar_y = y0 + t_h + int(size * 0.05)
    bar_h = max(2, size // 51)
    bar_w = int(size * 0.42)
    bar_x = (size - bar_w) // 2
    draw.rounded_rectangle(
        (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
        radius=bar_h // 2,
        fill=(46, 232, 199, 140),
    )
    return img


def main() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    icons = [render_icon(s) for s in DESKTOP_SIZES]
    for s, im in zip(DESKTOP_SIZES, icons):
        im.save(ICON_DIR / f"tagline_logo_{s}.png")
    icons[0].save(
        ICON_DIR / "tagline.ico",
        format="ICO",
        sizes=[(s, s) for s in DESKTOP_SIZES],
        append_images=icons[1:],
    )
    for folder, s in ANDROID_SIZES.items():
        out = ANDROID_RES / folder / "ic_launcher.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        render_icon(s).save(out)
    # Legacy asset used in some trees
    ui_assets = ROOT / "src" / "crates" / "concat" / "ui" / "assets"
    ui_assets.mkdir(parents=True, exist_ok=True)
    render_icon(256).save(ui_assets / "tagline-logo.png")
    print("Wrote TagLine icons to", ICON_DIR)


if __name__ == "__main__":
    main()
