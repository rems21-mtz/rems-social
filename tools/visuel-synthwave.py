from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
W,H=1080,1350
img=Image.new("RGB",(W,H))
d=ImageDraw.Draw(img)
# synthwave sky gradient
top=(20,6,48); mid=(160,30,120); bot=(255,120,60)
for y in range(H):
    t=y/H
    if t<0.55:
        k=t/0.55; c=tuple(int(top[i]+(mid[i]-top[i])*k) for i in range(3))
    else:
        k=(t-0.55)/0.45; c=tuple(int(mid[i]+(bot[i]-mid[i])*k*0.6) for i in range(3))
    d.line([(0,y),(W,y)],fill=c)
# sun with stripes
sun=Image.new("L",(W,H),0); sd=ImageDraw.Draw(sun)
cx,cy,r=W//2,560,300
sd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
for i in range(7):
    y=cy+40+i*36; h=6+i*3
    sd.rectangle([0,y,W,y+h],fill=0)
sunc=Image.new("RGB",(W,H))
sdc=ImageDraw.Draw(sunc)
for y in range(cy-r,cy+r):
    k=(y-(cy-r))/(2*r); sdc.line([(0,y),(W,y)],fill=(255,int(220-150*k),int(90+40*k)))
img.paste(sunc,(0,0),sun)
# horizon grid
hy=760
d.rectangle([0,hy,W,H],fill=(18,4,40))
for i in range(-20,21):
    d.line([(cx+i*30,hy),(cx+i*260,H)],fill=(255,60,200),width=2)
y=hy; step=8
while y<H:
    d.line([(0,y),(W,y)],fill=(255,60,200),width=2); step*=1.35; y+=int(step)
# palm silhouettes
def palm(x,base,s):
    for k in range(40):
        t=k/40; px=x+int(math.sin(t*1.2)*30*s); py=base-int(t*380*s)
        d.ellipse([px-9*s,py-9*s,px+9*s,py+9*s],fill=(10,2,25))
    tx,ty=x+int(math.sin(1.2)*30*s),base-int(380*s)
    for a in range(0,360,40):
        for j in range(30):
            rr=j*5*s; ang=math.radians(a); droop=(j/30)**2*60*s
            d.ellipse([tx+rr*math.cos(ang)-6*s,ty+rr*math.sin(ang)*0.4+droop-4*s,tx+rr*math.cos(ang)+6*s,ty+rr*math.sin(ang)*0.4+droop+4*s],fill=(10,2,25))
palm(110,hy+10,1.0); palm(980,hy+10,0.85)
# plugin screenshot card
shot=Image.open("/mnt/project-files/site-sunrise/revolution.png").convert("RGB")
crop=shot.crop((130,596,1310,1100)).resize((900,385))
card_x,card_y=90,840
glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
gd.rounded_rectangle([card_x-14,card_y-14,card_x+914,card_y+399],30,fill=(255,60,200,200))
glow=glow.filter(ImageFilter.GaussianBlur(22))
img=Image.alpha_composite(img.convert("RGBA"),glow).convert("RGB")
mask=Image.new("L",crop.size,0); ImageDraw.Draw(mask).rounded_rectangle([0,0,*crop.size],22,fill=255)
img.paste(crop,(card_x,card_y),mask)
d=ImageDraw.Draw(img)
d.rounded_rectangle([card_x,card_y,card_x+900,card_y+385],22,outline=(255,140,220),width=3)
F="/usr/share/fonts/opentype/inter/"
fb=ImageFont.truetype(F+"InterDisplay-Bold.otf",112)
fm=ImageFont.truetype(F+"InterDisplay-Medium.otf",40)
fs=ImageFont.truetype(F+"Inter-Bold.otf",30)
def ctext(y,t,f,fill,shadow=(255,40,180)):
    w=d.textlength(t,font=f); x=(W-w)/2
    for o in (6,3):
        d.text((x+o,y+o),t,font=f,fill=shadow)
    d.text((x,y),t,font=f,fill=fill)
d.text((60,60),"REMS PLUGINS",font=fs,fill=(255,255,255))
d.text((W-60-d.textlength("NEW SYNTH",font=fs),60),"NEW SYNTH",font=fs,fill=(255,200,120))
ctext(150,"BACK TO",fm,(255,230,250),(120,20,120))
ctext(200,"VICE-ERA",fb,(255,255,255))
ctext(320,"NIGHTS",fb,(255,255,255))
d=ImageDraw.Draw(img)
# bottom band
d.rectangle([0,H-110,W,H],fill=(10,2,25))
t="Neon pads & leads in REVOLUTION · try it free 7 days"
d.text(((W-d.textlength(t,font=fs))/2,H-88),t,font=fs,fill=(255,255,255))
t2="remsplugins.com"
d.text(((W-d.textlength(t2,font=fs))/2,H-50),t2,font=fs,fill=(255,140,90))
img.save("/mnt/project-files/posts/2026-11-23-gta6/post-gta6.png")
img.resize((540,675)).save("preview.png")
