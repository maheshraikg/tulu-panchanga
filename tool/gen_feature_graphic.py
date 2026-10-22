# Draws docs/play/feature_graphic.png (1024x500 Google Play banner) from the
# artwork in docs/branding/banner_source.png, adding the title in Kannada
# and English on the empty red area.
# Usage: python tool/gen_feature_graphic.py <repo root>   (needs Pillow with raqm)
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

root = sys.argv[1]
W, H = 1024, 500
art = Image.open(f'{root}/docs/branding/banner_source.png').convert('RGB')
# Cover-fit: scale to fill, crop the (tiny) overflow evenly.
s = max(W / art.width, H / art.height)
art = art.resize((round(art.width * s), round(art.height * s)), Image.LANCZOS)
x0, y0 = (art.width - W) // 2, (art.height - H) // 2
img = art.crop((x0, y0, x0 + W, y0 + H))


def font(weight, size):
    return ImageFont.truetype(
        f'{root}/assets/fonts/baloo/BalooTamma2-{weight}.ttf', size,
        layout_engine=ImageFont.Layout.RAQM)


CX = 748  # centre of the empty red area on the right
lines = [
    ('ತುಳು ಪಂಚಾಂಗ', font(800, 74), (255, 255, 255), 84),
    ('Tulu Panchanga', font(700, 48), (242, 201, 76), 186),
]
# Soft dark glow behind the text so it reads on the bright sky.
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for text, f, _, y in lines:
    w = gd.textlength(text, font=f)
    gd.text((CX - w / 2, y), text, font=f, fill=(90, 0, 0, 150))
glow = glow.filter(ImageFilter.GaussianBlur(10))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img)
for text, f, fill, y in lines:
    w = d.textlength(text, font=f)
    d.text((CX - w / 2 + 2, y + 3), text, font=f, fill=(90, 10, 8))
    d.text((CX - w / 2, y), text, font=f, fill=fill)

# Tagline pill.
tag = 'ದಿನ · ಹಬ್ಬ · ಮುಹೂರ್ತ  |  Offline'
f = font(700, 30)
w = d.textlength(tag, font=f)
pill = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(pill).rounded_rectangle(
    [CX - w / 2 - 26, 286, CX + w / 2 + 26, 338], radius=26, fill=(80, 0, 0, 110))
img.paste(pill, (0, 0), pill)
d = ImageDraw.Draw(img)
d.text((CX - w / 2, 292), tag, font=f, fill=(255, 255, 255))

img.save(f'{root}/docs/play/feature_graphic.png')
print(img.size)
