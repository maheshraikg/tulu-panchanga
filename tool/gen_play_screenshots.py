# Makes Google Play phone screenshots (1080x1920, 9:16) from docs/screenshots.
# Play rejects screenshots taller than 2:1; the raw captures are 2.15:1.
# Usage: python tool/gen_play_screenshots.py <repo root>   (Pillow with raqm)
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

root = sys.argv[1]
W, H = 1080, 1920
SHOTS = [
    ('kn_1_today.png', 'ಇಂದಿನ ಪಂಚಾಂಗ', 'Today: tithi, nakshatra, Rahu kaala'),
    ('kn_3_festivals.png', 'ತುಳುನಾಡಿನ ಹಬ್ಬಗಳು', 'Every Tulunadu festival'),
    ('kn_2_calendar.png', 'ತಿಂಗಳ ಕ್ಯಾಲೆಂಡರ್', 'Gregorian and Tulu months'),
    ('kn_4_muhurta.png', 'ಮುಹೂರ್ತ ಸಹಾಯಕ', 'Find good times'),
    ('kn_0b_language_sheet.png', '7 ಭಾಷೆಗಳು', 'Kannada, Tulu, English and more'),
    ('tcy_7_today_lipi.png', 'ತುಳು ಲಿಪಿ', 'Read in Tulu script'),
]


def font(weight, size):
    return ImageFont.truetype(
        f'{root}/assets/fonts/baloo/BalooTamma2-{weight}.ttf', size,
        layout_engine=ImageFont.Layout.RAQM)


def background():
    img = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(img)
    top, bot = (122, 28, 23), (200, 70, 30)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)],
               fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    n = 18  # bunting
    for i in range(n):
        x0, x1 = W * i / n, W * (i + 1) / n
        d.polygon([(x0 + 2, 0), (x1 - 2, 0), ((x0 + x1) / 2, 30)],
                  fill=(242, 201, 76) if i % 2 == 0 else (255, 255, 255))
    return img


def centred(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2 + 2, y + 3), text, font=f, fill=(60, 10, 8))
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


for i, (name, kn, en) in enumerate(SHOTS, 1):
    img = background()
    d = ImageDraw.Draw(img)
    centred(d, 70, kn, font(800, 84), (255, 255, 255))
    centred(d, 200, en, font(600, 46), (242, 201, 76))
    shot = Image.open(f'{root}/docs/screenshots/{name}').convert('RGB')
    sh_h = 1560
    sh_w = round(shot.width * sh_h / shot.height)
    shot = shot.resize((sh_w, sh_h), Image.LANCZOS)
    x, y = (W - sh_w) // 2, 300
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [x - 6, y + 10, x + sh_w + 6, y + sh_h + 20], radius=48, fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.paste(shadow, (0, 0), shadow)
    mask = Image.new('L', (sh_w, sh_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sh_w - 1, sh_h - 1], radius=40, fill=255)
    img.paste(shot, (x, y), mask)
    out = f'{root}/docs/play/screenshots/{i}_{name}'
    img.save(out)
    print(out, img.size)
