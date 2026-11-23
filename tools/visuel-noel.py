from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math
random.seed(7)
W,H=1080,1350
img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img)
top=(8,14,38); bot=(48,18,40)
for y in range(H):
    k=y/H; d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*k) for i in range(3)))
# warm bokeh lights
bk=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(bk)
cols=[(255,190,90),(255,120,70),(255,230,160),(220,60,60),(120,200,140)]
for _ in range(70):
    x=random.randint(0,W); y=random.randint(0,H); r=random.randint(10,46); c=random.choice(cols)
    bd.ellipse([x-r,y-r,x+r,y+r],fill=c+(random.randint(40,110),))
bk=bk.filter(ImageFilter.GaussianBlur(8))
img=Image.alpha_composite(img.convert("RGBA"),bk)
# string lights garland
gl=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(gl)
pts=[(x,70+int(40*math.sin(x/W*math.pi))) for x in range(0,W+1,6)]
gd.line(pts,fill=(30,30,30,255),width=3)
for i,x in enumerate(range(30,W,70)):
    y=70+int(40*math.sin(x/W*math.pi))+14; c=cols[i%4]
    gd.ellipse([x-26,y-26,x+26,y+26],fill=c+(90,))
gl=gl.filter(ImageFilter.GaussianBlur(6))
img=Image.alpha_composite(img,gl); d=ImageDraw.Draw(img)
for i,x in enumerate(range(30,W,70)):
    y=70+int(40*math.sin(x/W*math.pi))+14; c=cols[i%4]
    d.ellipse([x-8,y-11,x+8,y+11],fill=c)
# snow
for _ in range(260):
    x=random.randint(0,W); y=random.randint(0,H); r=random.choice([1,2,2,3,4])
    d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,random.randint(120,230)))
img=img.convert("RGB"); d=ImageDraw.Draw(img)
F="/usr/share/fonts/opentype/inter/"
fb=ImageFont.truetype(F+"InterDisplay-Bold.otf",96)
fm=ImageFont.truetype(F+"InterDisplay-Medium.otf",44)
fs=ImageFont.truetype(F+"Inter-Bold.otf",30)
fl=ImageFont.truetype(F+"Inter-Bold.otf",26)
def ctext(y,t,f,fill,sh=(180,40,40)):
    w=d.textlength(t,font=f); x=(W-w)/2
    d.text((x+4,y+4),t,font=f,fill=sh); d.text((x,y),t,font=f,fill=fill)
ctext(160,"CHRISTMAS SONGS",fb,(255,255,255))
ctext(265,"ARE BACK.",fb,(255,215,140))
ctext(385,"Make yours sound like a hit.",fm,(240,235,230),(60,20,30))
def card(path,box,pos,size,label,accent):
    im=Image.open(path).convert("RGB").crop(box).resize(size)
    x,y=pos
    g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).rounded_rectangle([x-12,y-12,x+size[0]+12,y+size[1]+12],26,fill=accent+(170,))
    g=g.filter(ImageFilter.GaussianBlur(18))
    base=Image.alpha_composite(img.convert("RGBA"),g).convert("RGB")
    m=Image.new("L",size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,*size],18,fill=255)
    base.paste(im,(x,y),m)
    dd=ImageDraw.Draw(base); dd.rounded_rectangle([x,y,x+size[0],y+size[1]],18,outline=accent,width=3)
    tw=dd.textlength(label,font=fl)
    dd.rounded_rectangle([x+18,y-22,x+18+tw+28,y+20],20,fill=accent)
    dd.text((x+32,y-15),label,font=fl,fill=(20,10,10))
    return base
img=card("/mnt/project-files/site-sunrise/revolution.png",(130,596,1310,1100),(70,520),(700,300),"REVOLUTION · WRITE IT",(255,170,80))
img=card("/mnt/project-files/site-sunrise/mixpilot.png",(650,162,1337,668),(430,870),(580,327),"MIXPILOT · FREE · MIX IT",(120,210,160))
d=ImageDraw.Draw(img)
d.text((60,1230),"REMS PLUGINS",font=fs,fill=(255,255,255))
t="remsplugins.com"; d.text((W-60-d.textlength(t,font=fs),1230),t,font=fs,fill=(255,190,110))
d.text((60,1275),"Revolution: 7-day free trial",font=fl,fill=(220,215,210))
img.save("/mnt/project-files/posts/2026-11-24-noel/post-noel.png")
img.resize((540,675)).save("prev2.png")
