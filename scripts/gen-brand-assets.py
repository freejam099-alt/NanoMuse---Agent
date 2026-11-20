#!/usr/bin/env python3
"""Generate nanoMuse brand icon assets from assets/brand/nanomuse-mark.svg.

The source paths are Hugeicons AI Brain 02, free Stroke Rounded. This script
keeps launcher/favicons and marketing copies visually aligned. It requires
Playwright with Chromium; Pillow is used only to update the existing README
cover raster and logo lockup without changing their typography or layout.
"""

from __future__ import annotations

import base64
import re
import shutil
import sys
from io import BytesIO
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets" / "brand"
START = "#015CFB"
END = "#0186FB"
BLUE = "#0078FD"
TILE = "#FFFFFF"
BORDER = "#D9D9DE"


def source_paths() -> list[str]:
    root = ET.parse(BRAND / "nanomuse-mark.svg").getroot()
    paths = [e.attrib["d"] for e in root.iter() if e.tag.endswith("path")]
    if len(paths) != 3:
        raise SystemExit(f"Expected 3 Hugeicons AI Brain 02 paths, found {len(paths)}")
    return paths


def defs(x1: float = 14, y: float = 50, x2: float = 86) -> str:
    return (
        '<defs><linearGradient id="nm-gradient" gradientUnits="userSpaceOnUse" '
        f'x1="{x1:g}" y1="{y:g}" x2="{x2:g}" y2="{y:g}">'
        f'<stop offset="0" stop-color="{START}"/><stop offset="1" stop-color="{END}"/>'
        '</linearGradient></defs>'
    )


def mark_group(paths: list[str], translate: tuple[float, float] = (6.8, 6.8), scale: float = 3.6,
               stroke: str = "url(#nm-gradient)", stroke_width: float = 1.5) -> str:
    ox, oy = translate
    body = "".join(
        f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{stroke_width:g}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        for d in paths
    )
    return f'<g transform="translate({ox:g} {oy:g}) scale({scale:g})">{body}</g>'


def svg_mark(paths: list[str]) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Generated from Hugeicons AI Brain 02 (free Stroke Rounded), see THIRD_PARTY_NOTICES.md. -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{defs()}'
        f'{mark_group(paths)}</svg>\n'
    )


def svg_brand_icon(paths: list[str], border: bool = True) -> str:
    edge = (
        f'<rect x="0.3" y="0.3" width="99.4" height="99.4" rx="27" ry="27" '
        f'fill="{TILE}" stroke="{BORDER}" stroke-width="0.6"/>'
        if border else '<rect width="100" height="100" rx="27" ry="27" fill="#FFFFFF"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Generated from Hugeicons AI Brain 02 (free Stroke Rounded), see THIRD_PARTY_NOTICES.md. -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">{defs()}{edge}'
        f'{mark_group(paths)}</svg>\n'
    )


def svg_icon_on_blue(paths: list[str]) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!-- Generated from Hugeicons AI Brain 02 (free Stroke Rounded), see THIRD_PARTY_NOTICES.md. -->\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 148 148">{defs(38, 74, 110)}'
        f'<rect width="148" height="148" fill="{BLUE}"/>'
        '<g transform="translate(24 24)"><rect width="100" height="100" rx="27" ry="27" fill="#FFFFFF"/>'
        f'{mark_group(paths)}</g></svg>\n'
    )


def render(svg: str, target: Path, size: int, *, transparent: bool = True) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("Playwright not installed; install it before generating raster assets") from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox"],
        )
        page = browser.new_page(viewport={"width": size, "height": size}, device_scale_factor=1)
        page.set_content(f'<html><body style="margin:0;padding:0">{svg}</body></html>')
        page.locator("svg").evaluate(
            "(e, s) => { e.setAttribute('width', s); e.setAttribute('height', s); }", str(size)
        )
        page.screenshot(
            path=str(target),
            omit_background=transparent,
            clip={"x": 0, "y": 0, "width": size, "height": size},
        )
        browser.close()


def update_cover(svg_icon_bytes: bytes) -> None:
    """Replace the embedded square icon in the draw.io source and its PNG export."""
    cover_svg = BRAND / "nanomuse-cover.svg"
    text = cover_svg.read_text(encoding="utf-8")
    data_uri = "data:image/png;base64," + base64.b64encode(svg_icon_bytes).decode("ascii")
    changed = 0

    def replace_image(match: re.Match[str]) -> str:
        nonlocal changed
        tag = match.group(0)
        if all(re.search(rf'\b{key}="{value}"', tag) for key, value in (
            ("x", "21"), ("y", "10.83"), ("width", "63.34"), ("height", "63.34")
        )):
            tag, n = re.subn(r'((?:xlink:)?href=")[^"]*(")', rf"\g<1>{data_uri}\2", tag, count=1)
            changed += n
        return tag

    text = re.sub(r"<image\b[^>]*>", replace_image, text)
    if changed != 1:
        raise SystemExit(f"Expected to update one embedded cover icon, updated {changed}")
    cover_svg.write_text(text, encoding="utf-8")

    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow not installed; cannot update nanomuse-cover.png") from exc
    cover_png = BRAND / "nanomuse-cover.png"
    with Image.open(cover_png) as old:
        canvas = old.convert("RGBA")
    with Image.open(BytesIO(svg_icon_bytes)) as icon:
        icon = icon.convert("RGBA").resize((633, 633), Image.Resampling.LANCZOS)
    # The draw.io cover is exported at 10× its 819×85 SVG viewport.
    if canvas.size != (8190, 850):
        raise SystemExit(f"Unexpected cover raster size {canvas.size}; expected 8190×850")
    canvas.alpha_composite(icon, (210, 108))
    canvas.save(cover_png, optimize=True)


def update_combined_logo(svg_icon_bytes: bytes) -> None:
    """Replace only the old app tile in the unused transparent wordmark export."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Pillow not installed; cannot update nanoMuse-logo-and-text.png") from exc
    logo = BRAND / "nanoMuse-logo-and-text.png"
    with Image.open(logo) as old:
        canvas = old.convert("RGBA")
    if canvas.size != (4010, 780):
        raise SystemExit(f"Unexpected logo lockup size {canvas.size}; expected 4010×780")
    with Image.open(BytesIO(svg_icon_bytes)) as icon:
        icon = icon.convert("RGBA").resize((632, 634), Image.Resampling.LANCZOS)
    # Preserve the existing lockup and wordmark; the old square occupies this exact box.
    canvas.alpha_composite(icon, (0, 68))
    canvas.save(logo, optimize=True)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    print(f"  copied {target.relative_to(ROOT)}")


def main() -> int:
    if sys.argv[1:] in (["-h"], ["--help"]):
        print(__doc__.strip())
        return 0
    if sys.argv[1:]:
        print(f"usage: {sys.argv[0]}", file=sys.stderr)
        return 2
    paths = source_paths()
    print("== brand vectors")
    svg_mark_text = svg_mark(paths)
    svg_icon_text = svg_brand_icon(paths)
    svg_plain_icon_text = svg_brand_icon(paths, border=False)
    svg_blue_text = svg_icon_on_blue(paths)
    write_text(BRAND / "nanomuse-icon.svg", svg_plain_icon_text)
    write_text(BRAND / "nanomuse-icon-on-blue.svg", svg_blue_text)
    write_text(ROOT / "web/public/mark.svg", svg_mark_text)
    write_text(ROOT / "web/public/icon.svg", svg_icon_text)
    write_text(ROOT / "cloud/nanomuse_cloud/console/mark.svg", svg_mark_text)
    write_text(ROOT / "cloud/nanomuse_cloud/console/icon.svg", svg_icon_text)
    write_text(ROOT / "demo/showcase/site/page/mark.svg", svg_mark_text)
    write_text(ROOT / "website/public/nanomuse-icon.svg", svg_icon_text)

    print("== raster assets")
    render(svg_mark_text, BRAND / "nanomuse-mark-rgba-688.png", 688)
    render(svg_icon_text, ROOT / "docs/app-icon.png", 512)
    source_png = BRAND / "nanomuse-icon-source-1024.png"
    render(svg_blue_text, source_png, 1024, transparent=False)
    for size in (192, 512):
        render(svg_icon_text, ROOT / f"web/public/icon-{size}.png", size)
        copy_file(ROOT / f"web/public/icon-{size}.png", ROOT / f"nanomuse/server/static/icon-{size}.png")
    copy_file(ROOT / "web/public/icon.svg", ROOT / "nanomuse/server/static/icon.svg")
    copy_file(ROOT / "web/public/mark.svg", ROOT / "nanomuse/server/static/mark.svg")
    render(svg_icon_text, ROOT / "harness/desktop/resources/app-icon.png", 1024)
    render(svg_icon_text, ROOT / "harness/desktop/resources/logo.png", 256)
    for size in (16, 24, 32, 48, 64, 128, 256, 512):
        render(svg_icon_text, ROOT / f"harness/desktop/resources/icons/{size}x{size}.png", size)

    update_cover(source_png.read_bytes())
    update_combined_logo(source_png.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
