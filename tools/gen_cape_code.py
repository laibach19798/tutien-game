import numpy as np, math
from PIL import Image
from scipy import ndimage as ndi
D='/root/.claude/projects/-home-claude-tutien-game/93e4417b-5a7d-56c6-8655-10d96e9547d4/tool-results/mcp-PixelLab-blob-'
ROT=['1791518201673-ivhcog','1791522058116-pu85zj','1791518200112-7j1xrc','1791518198295-0eoqm5','1791518196588-kz5p4u','1791522063431-0r3cnk','1791522060973-j2y3yt','1791522059351-fb9qv0']
FACE=[(0,1),(.7,.7),(1,0),(.7,-.7),(0,-1),(-.7,-.7),(-1,0),(-.7,.7)]
BASE={a:np.array(Image.open(f'/home/claude/web2/base_{a}.png').convert('RGBA')) for a in('idle','walk','run')}
NF={'idle':4,'walk':8,'run':8}
CFG={'idle':dict(A=0.9,T=0.0,K=2.4),'walk':dict(A=1.7,T=1.5,K=2.8),'run':dict(A=2.3,T=4.0,K=3.2)}
def cape_mask(c,bg):
    R,G,B=[c[...,i].astype(float) for i in range(3)]
    m=(((G<0.55*R)&(R>60))|(((R-B)>=100)&(G>=160)&(R>200)))&~bg
    lab,nl=ndi.label(m,structure=np.ones((3,3)))
    if nl:
        sz=ndi.sum(m,lab,range(1,nl+1));m=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>=max(8,.12*sz.max())])
    dark=(c.sum(2)<110)&~bg;near=np.zeros_like(m)
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):near|=np.roll(np.roll(m,dy,0),dx,1)
    return m|(dark&near)
tiles=[]
for d,b in enumerate(ROT):
    im=np.array(Image.open(D+b+'.png').convert('RGB')).astype(int)[18:274,0:256][2::4,2::4]
    bg=(abs(im-np.array([31,37,44])).sum(2)<8);m=cape_mask(im,bg);sk=(~bg)&(~m)
    # can chinh voi than goc (idle khung 0)
    bm=BASE['idle'][d*64:(d+1)*64,0:64,3]>0
    best=max(((((np.roll(np.roll(sk,dy,0),dx,1)&bm)[:36].sum()/max(1,(np.roll(np.roll(sk,dy,0),dx,1)|bm)[:36].sum())),dx,dy) for dx in range(-6,7) for dy in range(-6,7)))
    _,dx,dy=best;print(d,'offset',dx,dy,round(best[0],2))
    sh=lambda a:np.roll(np.roll(a,dy,0),dx,1)
    m,sk,im=sh(m),sh(sk),sh(im)
    front=np.zeros((64,64,4),np.uint8);front[...,:3]=im;front[m,3]=255
    fill=np.zeros((64,64,4),np.uint8)
    for y in range(64):
        xs=np.where(m[y])[0]
        if len(xs)<2:continue
        for x in range(xs.min(),xs.max()+1):
            if sk[y,x]:
                j=xs[np.argmin(abs(xs-x))];fill[y,x,:3]=(im[y,j]*.72).astype(np.uint8);fill[y,x,3]=255
    tiles.append((front,fill,m))
def anim(tile,d,anim_,f):
    front,fill,m=tile;fx,fy=FACE[d];c=CFG[anim_];n=NF[anim_];ph=2*math.pi*f/n
    rows=np.where(m.any(1))[0];y0,y1=rows.min(),rows.max()
    base=BASE[anim_];top=lambda ff:int(np.argmax(base[d*64:(d+1)*64,ff*64:(ff+1)*64,3].any(1)))
    def hx(a,ff):
        t=a[d*64:(d+1)*64,ff*64:(ff+1)*64,3]>0;r=int(np.argmax(t.any(1)));ys,xs=np.where(t[r:r+14]);return r,xs.mean()
    r0,x0=hx(BASE['idle'],0);r1,x1=hx(base,f)
    bob=r1-r0;bx=int(round(x1-x0))
    out=[]
    for src in(front,fill):
        o=np.zeros((80,80,4),np.uint8)
        for y in range(64):
            if not src[y,:,3].any():continue
            u=min(1,max(0,(y-y0)/max(1,y1-y0)))
            lat=c['A']*u**1.3*math.sin(ph-c['K']*u)*(1.0 if abs(fx)<.5 else .6)
            tr=-fx*c['T']*u
            dx=int(round(lat+tr))+bx;yy=y+8+bob
            if 0<=yy<80:
                row=np.roll(src[y],dx,0);
                # khong de pixel tran qua mep
                o[yy,8:72]=row
        out.append(o)
    return out
for a in('idle','walk','run'):
    n=NF[a];F=Image.new('RGBA',(n*80,640));B=Image.new('RGBA',(n*80,640))
    for d in range(8):
        for f in range(n):
            fr,fl=anim(tiles[d],d,a,f)
            F.paste(Image.fromarray(fr),(f*80,d*80));B.paste(Image.fromarray(fl),(f*80,d*80))
    F.save(f'/home/claude/web2/code/cape_front_{a}.png');B.save(f'/home/claude/web2/code/cape_back_{a}.png')
