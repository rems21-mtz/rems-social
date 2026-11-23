from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math
random.seed(11)
W,H=1080,1350
img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img)
top=(38,14,10); bot=(120,48,18)
for y in range(H):
    k=y/H; d.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*k) for i in range(3)))
bk=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(bk)
cols=[(255,170,60),(230,100,30),(255,210,120),(180,60,20)]
for _ in range(60):
    x=random.randint(0,W); y=random.randint(0,H); r=random.randint(12,50); c=random.choice(cols)
    bd.ellipse([x-r,y-r,x+r,y+r],fill=c+(random.randint(35,90),))
bk=bk.filter(ImageFilter.GaussianBlur(9))
img=Image.alpha_composite(img.convert("RGBA"),bk).convert("RGB"); d=ImageDraw.Draw(img)
# falling leaves
lc=[(230,110,30),(200,70,20),(250,170,50),(160,50,20)]
for _ in range(34):
    x=random.randint(0,W); y=random.randint(0,1170); s=random.randint(14,30); c=random.choice(lc)
    ang=random.random()*math.pi
    pts=[(x+s*math.cos(ang),y+s*math.sin(ang)),(x+s*0.5*math.cos(ang+1.6),y+s*0.5*math.sin(ang+1.6)),(x-s*math.cos(ang),y-s*math.sin(ang)),(x+s*0.5*math.cos(ang-1.6),y+s*0.5*math.sin(ang-1.6))]
    d.polygon(pts,fill=c)
F="/usr/share/fonts/opentype/inter/"
fb=ImageFont.truetype(F+"InterDisplay-Bold.otf",96)
fm=ImageFont.truetype(F+"InterDisplay-Medium.otf",44)
fs=ImageFont.truetype(F+"Inter-Bold.otf",30)
fl=ImageFont.truetype(F+"Inter-Bold.otf",26)
def ctext(y,t,f,fill,sh=(90,30,10)):
    w=d.textlength(t,font=f); x=(W-w)/2
    d.text((x+4,y+4),t,font=f,fill=sh); d.text((x,y),t,font=f,fill=fill)
ctext(150,"THANKSGIVING WEEK",fb,(255,255,255))
ctext(255,"GOOD BEATS.",fb,(255,200,110))
ctext(375,"Warm pads, lucky grooves.",fm,(245,232,220),(70,25,10))
def card(path,box,pos,size,label,accent):
    global img
    im=Image.open(path).convert("RGB").crop(box).resize(size,Image.LANCZOS)
    x,y=pos
    g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).rounded_rectangle([x-12,y-12,x+size[0]+12,y+size[1]+12],26,fill=accent+(170,))
    g=g.filter(ImageFilter.GaussianBlur(18))
    base=Image.alpha_composite(img.convert("RGBA"),g).convert("RGB")
    m=Image.new("L",size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,*size],18,fill=255)
    base.paste(im,(x,y),m)
    dd=ImageDraw.Draw(base); dd.rounded_rectangle([x,y,x+size[0],y+size[1]],18,outline=accent,width=3)
    tw=dd.textlength(label,font=fl)
    ly=y+size[1]-20
    dd.rounded_rectangle([x+18,ly,x+18+tw+28,ly+42],20,fill=accent)
    dd.text((x+32,ly+7),label,font=fl,fill=(30,12,6))
    img=base
card("/mnt/project-files/site-sunrise/revolution.png",(130,596,1310,1100),(70,520),(700,300),"REVOLUTION · THE SOUND",(255,170,80))
card("/mnt/project-files/site-sunrise/catalogue.png",(697,870,1003,1062),(520,880),(480,301),"LUCKY BEATS · FREE · THE GROOVE",(255,120,70))
d=ImageDraw.Draw(img)
d.text((60,1230),"REMS PLUGINS",font=fs,fill=(255,255,255))
t="remsplugins.com"; d.text((W-60-d.textlength(t,font=fs),1230),t,font=fs,fill=(255,190,110))
d.text((60,1275),"Revolution: 7-day free trial",font=fl,fill=(230,215,200))
img.save("/mnt/project-files/posts/2026-11-25-thanksgiving/post-thanksgiving.png")
img.resize((540,675)).save("prev3.png")
