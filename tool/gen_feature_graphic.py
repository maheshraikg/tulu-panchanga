# Draws docs/play/feature_graphic.png (1024x500 Google Play banner).
# Usage: python tool/gen_feature_graphic.py <repo root>   (needs Pillow with raqm)
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
root=sys.argv[1]
W,H=1024,500
img=Image.new('RGB',(W,H))
d=ImageDraw.Draw(img)
top=(122,28,23); mid=(179,38,30); bot=(224,100,31)
for y in range(H):
    t=y/H
    a,b,u=(top,mid,t/0.6) if t<0.6 else (mid,bot,(t-0.6)/0.4)
    d.line([(0,y),(W,y)],fill=tuple(int(a[i]+(b[i]-a[i])*u) for i in range(3)))
# sun rays
rays=Image.new('RGBA',(W,H),(0,0,0,0)); rd=ImageDraw.Draw(rays)
cx,cy=205,240
for i in range(16):
    ang=i*math.pi/8
    p=[(cx+30*math.cos(ang+math.pi/2),cy+30*math.sin(ang+math.pi/2)),(cx+900*math.cos(ang),cy+900*math.sin(ang)),(cx-30*math.cos(ang+math.pi/2),cy-30*math.sin(ang+math.pi/2))]
    rd.polygon(p,fill=(242,201,76,22))
img.paste(rays,(0,0),rays)
# bunting
d=ImageDraw.Draw(img)
n=24
for i in range(n):
    x0,x1=W*i/n,W*(i+1)/n
    y=lambda x: 6+14*math.sin(math.pi*x/W)
    d.polygon([(x0+2,y(x0)),(x1-2,y(x1)),((x0+x1)/2,y((x0+x1)/2)+22)],fill=(242,201,76) if i%2==0 else (255,255,255))
# paddy strip
d.rectangle([0,H-46,W,H],fill=(110,158,58))
for r in range(3):
    yy=H-38+r*12
    pts=[(x,yy+3*math.sin(x/20+r)) for x in range(0,W+12,12)]
    d.line(pts,fill=(160,200,110),width=2)
# icon with shadow
icon=Image.open(f'{root}/docs/icon_512.png').convert('RGBA').resize((270,270),Image.LANCZOS)
mask=Image.new("L",(270,270),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,269,269],radius=60,fill=255)
sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([70,125,340,395],radius=60,fill=(0,0,0,110))
sh=sh.filter(ImageFilter.GaussianBlur(14)); img.paste(sh,(0,0),sh)
img.paste(icon,(70,105),mask)
f=lambda w,s: ImageFont.truetype(f'{root}/assets/fonts/baloo/BalooTamma2-{w}.ttf',s,layout_engine=ImageFont.Layout.RAQM)
d=ImageDraw.Draw(img)
def text(xy,s,font,fill):
    d.text((xy[0]+2,xy[1]+3),s,font=font,fill=(60,10,8))
    d.text(xy,s,font=font,fill=fill)
text((385,95),'ತುಳು ಪಂಚಾಂಗ',f(800,80),(255,255,255))
text((389,205),'Tulu Panchanga',f(700,56),(242,201,76))
ov=Image.new('RGBA',(W,H),(0,0,0,0))
ImageDraw.Draw(ov).rounded_rectangle([385,300,955,356],radius=28,fill=(0,0,0,70))
img.paste(ov,(0,0),ov)
d=ImageDraw.Draw(img)
d.text((409,308),'ದಿನ · ಹಬ್ಬ · ಮುಹೂರ್ತ  |  Offline',font=f(700,32),fill=(255,255,255))
img.save(f'{root}/docs/play/feature_graphic.png')
print(img.size)
