#!/usr/bin/env python3
"""Generate the nanoMuse iOS app icons and brand-mark image sets from assets/brand/.

The source is Hugeicons AI Brain 02, free Stroke Rounded; see THIRD_PARTY_NOTICES.md.
App-icon tiles stay full-square because iOS applies its own corner mask.
Requires Playwright with Chromium (`pip install playwright && playwright install chromium`).
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IOS = ROOT / "android" / "src" / "ios"
ICONSET = IOS / "Assets.xcassets" / "AppIcon.appiconset"
BRANDSET = IOS / "Assets.xcassets" / "NanoMuseBrandMark.imageset"
LAUNCHSET = IOS / "Assets.xcassets" / "NanoMuseLaunchMark.imageset"
LEGACY_LAUNCHSET = IOS / "NanoMuse" / "NanoMuseLaunch.xcassets" / "NanoMuseLaunchMark.imageset"
ALTERNATE = IOS / "Resources" / "AlternateIcons"
START = "#015CFB"
END = "#0186FB"
DARK = "#0F1B33"
WHITE = "#FFFFFF"
BORDER = "#D9D9DE"


def android_icons():  # noqa: ANN201  (module name has a hyphen)
    spec = importlib.util.spec_from_file_location(
        "gen_android_icons", ROOT / "scripts" / "gen-android-icons.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mark(paths: list[str], *, start: str = START, end: str | None = END) -> str:
    grad = (
        '<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="14" y1="50" x2="86" y2="50">'
        f'<stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/></linearGradient>'
        if end else ""
    )
    color = "url(#g)" if end else start
    vectors = "".join(
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5.4" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        for d in paths
    )
    return f"<defs>{grad}</defs>{vectors}"


def app_tile(paths: list[str], background: str, start: str = START, end: str | None = END) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<rect width="100" height="100" fill="{background}"/>'
        f'{mark(paths, start=start, end=end)}</svg>'
    )


def brand_tile(paths: list[str]) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="14" y1="50" x2="86" y2="50">'
        f'<stop offset="0" stop-color="{START}"/><stop offset="1" stop-color="{END}"/></linearGradient></defs>'
        f'<rect x="0.3" y="0.3" width="99.4" height="99.4" rx="27" ry="27" fill="#FFFFFF" stroke="{BORDER}" stroke-width="0.6"/>'
        f'{mark(paths)}</svg>'
    )


def save_png(page, target: Path, svg: str, size: int, transparent: bool = False) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    page.set_viewport_size({"width": size, "height": size})
    page.set_content(f'<html><body style="margin:0;padding:0">{svg}</body></html>')
    page.locator("svg").evaluate(
        "(e, s) => { e.setAttribute('width', s); e.setAttribute('height', s); }", str(size)
    )
    page.screenshot(
        path=str(target),
        omit_background=transparent,
        clip={"x": 0, "y": 0, "width": size, "height": size},
    )
    print(f"  wrote {target.relative_to(ROOT)} ({size}×{size})")


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args in (["-h"], ["--help"]):
        print(__doc__.strip())
        return 0
    if args:
        print(f"usage: {sys.argv[0]}  (takes no arguments; unknown: {' '.join(args)})", file=sys.stderr)
        return 2
    if not ICONSET.is_dir():
        sys.exit(f"{ICONSET} not found (restore the iOS tree first)")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("playwright not installed: pip install playwright && playwright install chromium")

    icons = android_icons()
    source = icons.mark_paths()
    paths = icons._brand_paths(source)
    jobs = {
        ICONSET / "Icon-1024.png": (app_tile(paths, WHITE), 1024, False),
        ICONSET / "Icon-1024-Dark.png": (app_tile(paths, DARK), 1024, False),
        ALTERNATE / "AppIcon-Light.png": (app_tile(paths, WHITE), 1024, False),
        ALTERNATE / "AppIcon-Dark.png": (app_tile(paths, DARK), 1024, False),
        ALTERNATE / "AppIcon-LegacyLight.png": (app_tile(paths, WHITE, START, None), 1024, False),
        ALTERNATE / "AppIcon-LegacyDark.png": (app_tile(paths, DARK, WHITE, None), 1024, False),
    }
    brand_svg = brand_tile(paths)
    write_json(BRANDSET / "Contents.json", {
        "images": [
            {"filename": "NanoMuseBrandMark.png", "idiom": "universal", "scale": "1x"},
            {"filename": "NanoMuseBrandMark@2x.png", "idiom": "universal", "scale": "2x"},
            {"filename": "NanoMuseBrandMark@3x.png", "idiom": "universal", "scale": "3x"},
        ],
        "info": {"author": "xcode", "version": 1},
    })
    for filename, size in (("NanoMuseBrandMark.png", 96), ("NanoMuseBrandMark@2x.png", 192),
                           ("NanoMuseBrandMark@3x.png", 288)):
        jobs[BRANDSET / filename] = (brand_svg, size, True)

    launch_svg = brand_svg
    write_json(LAUNCHSET / "Contents.json", {
        "images": [
            {"filename": "mark.png", "idiom": "universal", "scale": "1x"},
            {"filename": "mark@2x.png", "idiom": "universal", "scale": "2x"},
            {"filename": "mark@3x.png", "idiom": "universal", "scale": "3x"},
        ],
        "info": {"author": "xcode", "version": 1},
    })
    for folder in (LAUNCHSET, LEGACY_LAUNCHSET):
        for filename, size in (("mark.png", 120), ("mark@2x.png", 240), ("mark@3x.png", 360)):
            jobs[folder / filename] = (launch_svg, size, True)
        if folder == LEGACY_LAUNCHSET:
            # Keep the original image-set manifest in sync with the extra 1x file.
            write_json(folder / "Contents.json", {
                "images": [
                    {"filename": "mark.png", "idiom": "universal", "scale": "1x"},
                    {"filename": "mark@2x.png", "idiom": "universal", "scale": "2x"},
                    {"filename": "mark@3x.png", "idiom": "universal", "scale": "3x"},
                ],
                "info": {"author": "xcode", "version": 1},
            })

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
        page = browser.new_page(device_scale_factor=1)
        for target, (svg, size, transparent) in jobs.items():
            save_png(page, target, svg, size, transparent)
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
