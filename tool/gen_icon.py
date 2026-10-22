"""Builds every app icon from docs/branding/icon_source.png (the artwork:
lamp, calendar and sun on Tulu red).

Writes:
  docs/icon_512.png                                   Google Play icon
  android/app/src/main/res/mipmap-*/ic_launcher.png   legacy launcher icon
  android/app/src/main/res/mipmap-*/ic_launcher_foreground.png
                                                      adaptive icon layer
Usage: python tool/gen_icon.py <repo root>    (pip install pillow)
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

root = sys.argv[1]
art = Image.open(f'{root}/docs/branding/icon_source.png').convert('RGB')
RES = f'{root}/android/app/src/main/res'
LEGACY = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}


def padded(n, scale):
    """[art] shrunk to [scale] of an n×n square; the margin is a blurred,
    enlarged copy of the art so the red glow continues to the edges."""
    bg = art.resize((n, n), Image.LANCZOS).filter(
        ImageFilter.GaussianBlur(n / 12))
    k = round(n * scale)
    off = (n - k) // 2
    feather = Image.new('L', (k, k), 0)
    ImageDraw.Draw(feather).rounded_rectangle(
        [0, 0, k - 1, k - 1], radius=k // 6, fill=255)
    feather = feather.filter(ImageFilter.GaussianBlur(k / 40))
    bg.paste(art.resize((k, k), Image.LANCZOS), (off, off), feather)
    return bg


# Google Play: full artwork; Play applies its own rounded mask.
art.resize((512, 512), Image.LANCZOS).save(f'{root}/docs/icon_512.png')

for dpi, n in LEGACY.items():
    # Legacy (pre-Android 8) icon: rounded square, art slightly inset.
    im = padded(n * 4, 0.92).convert('RGBA')
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, im.width - 1, im.height - 1], radius=im.width * 0.22, fill=255)
    im.putalpha(mask)
    im.resize((n, n), Image.LANCZOS).save(f'{RES}/mipmap-{dpi}/ic_launcher.png')
    # Adaptive foreground: 108dp canvas; launchers show the middle 72dp
    # and may cut it to a circle, so the whole art fits inside that circle.
    fg = padded(n * 108 // 48 * 4, 0.62)
    fg.resize((n * 108 // 48,) * 2, Image.LANCZOS).save(
        f'{RES}/mipmap-{dpi}/ic_launcher_foreground.png')
print('icons written')
