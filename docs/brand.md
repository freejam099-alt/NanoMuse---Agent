# nanoMuse brand

Decided 2026-09-24. The app icon and the in-app colour system are one decision: the palette
is derived from the icon so the whole app matches the tile on the home screen.

## The mark

The app mark is **AI Brain 02** from Hugeicons, using its free, non-Pro *Stroke Rounded*
variant. It was chosen from the AI category after reviewing all 16 catalog pages; 143 free
rounded options were available, and AI Brain 02 was selected from page 1. Its three paths,
rounded caps and rounded joins are preserved from the upstream glyph.

- Source of truth: `assets/brand/nanomuse-mark.svg`, the original 24 × 24 path geometry from
  `AiBrain02Icon` in `@hugeicons/core-free-icons` 4.4.0. The glyph is MIT-licensed; attribution
  and the license text are in `THIRD_PARTY_NOTICES.md`.
- `assets/brand/nanomuse-icon-source-1024.png`: the 1024 px white tile on the brand-blue
  background. It is a generated export, not the path source.
- `assets/brand/nanomuse-icon.svg`: the white squircle tile (`rx=27`) and mark. Web and desktop
  identity icons add a fine `#D9D9DE` edge so the tile stays visible on white.
- `assets/brand/nanomuse-icon-on-blue.svg`: the icon on the blue backdrop, for store and splash
  contexts. Favicons, README and ordinary app identity use the white tile without that backdrop.
- `assets/brand/nanomuse-mark-rgba-688.png`: transparent 688 px raster fallback for the mark.
- `docs/app-icon.png`: 512 px icon tile with transparent outer corners and a fine edge; the
  README cover and other app previews use this image.
- `scripts/gen-brand-assets.py`, `scripts/gen-android-icons.py` and `scripts/gen-ios-icons.py`
  regenerate the platform assets from the shared geometry.

The icon is **not** the mascot. The default face is the bundled **dragon** (`web/public/avatars/`,
the Android app's `avatar/`); the other choices are an emoji on a colour and a face made in
the avatar studio. The red panda of the early releases retired in 0.1.23. Never put the dragon
(or the old red panda) on the launcher icon, and never put the app mark in chat as a face.
Navigation/control glyphs remain UI icons, and the dragon's animations remain mascot behavior;
neither is part of the app identity mark.

## Colour

Measured from the icon.

| Token | Value | Use |
|---|---|---|
| `brand.stroke.start` | `#015CFB` | left end of the mark's gradient |
| `brand.stroke.end` | `#0186FB` | right end of the mark's gradient |
| `brand.blue` | `#0078FD` | solid backdrop behind the white tile; splash/hero washes instead use a pale tint of the stroke gradient |
| `tile` | `#FFFFFF` | icon tile |

### Light theme

| Token | Value | Contrast | Use |
|---|---|---|---|
| `primary` | `#015CFB` | 5.35 on white | links, primary buttons (white text), status line |
| `primary.container` | `#E5F0FF` | — | selected rows, chips |
| `ink` | `#000000` | 21 on white | your message pill (white text), the send button and the scroll-to-latest disc (white arrow) |
| `pill` | `#F2F2F7` |  | the agent's message pill |
| `primary.tint` | `#EEF5FF` | — | subtle highlighted surfaces |
| `bg` | `#FFFFFF` |  | the chat, the pill bar, the menus and the drawer |
| `bg.grouped` | `#F2F2F7` | — | the settings pages (unchanged from OpenMinis) |
| `surface` | `#FFFFFF` | — | cards, input |

### Dark theme

| Token | Value | Contrast | Use |
|---|---|---|---|
| `primary` | `#58A6FF` | 8.3 on `#000`, 6.7 on `#1C1C1E` | links, buttons (black text), status line |
| `primary.container` | `#1A2B4A` | — | selected rows, chips |
| `ink` | `#FFFFFF` | 21 on `#000` | your message pill (black text), the send button and the scroll-to-latest disc (black arrow) |
| `pill` | `#1C1C1E` |  | the agent's message pill |
| `bg` / `surface` / `surface.2` | `#000000` / `#1C1C1E` / `#2C2C2E` | — | unchanged from OpenMinis |

Rules: one accent hue only. Code blocks, thinking text and links that OpenMinis coloured with
iOS blue, orange and green become `primary` plus neutrals. The conversation itself stays
monochrome: message pills, the send button and the scroll-to-latest disc use `ink`; the chat
canvas remains neutral or uses the person's chosen chat background. The selected navigation
capsule is the small exception: it uses the brand gradient `#015CFB` → `#0186FB` with a white
glyph (at least 3.62:1 contrast across the gradient). Use a very pale, static blue wash only on
welcome/setup or loading surfaces; never place it behind a readable transcript. Other control
glyphs keep their existing shapes and semantic colors. The dragon's own colors stay inside the
avatar; they are not UI colors.

## Android mapping

- Adaptive icon: background layer = solid `#FFFFFF`; foreground layer = the AI Brain 02 paths
  as a `VectorDrawable` with the two-stop `strokeColor` gradient above and rounded caps/joins;
  monochrome layer = the same paths in white, which Android can tint.
- Icon skins (activity aliases kept from OpenMinis): *Auto* = white tile; *Light* = white tile;
  *Dark* = `#0F1B33` tile with the white AI Brain 02 mark.
- Notification small icon: the mark in flat white, 24 dp.
- Never ship the old OpenMinis icon, name or the letter-n drafts.

## Don'ts

- Don't recolour the mark outside the blue gradient / flat white / flat black.
- Don't rotate the mark, add an extra outline around its strokes, or add a shadow.
- Don't place the mark on the brand blue without the white tile (contrast).
- Don't use another product's mark, name or blue as an asset; the only mark is ours.
