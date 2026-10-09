"""Ve ao choang thu cong (procedural) -> 2 sheet: cape_back (ve TRUOC than) va cape_front (ve SAU than).
Layout giong base: 8 hang huong (S,SE,E,NE,N,NW,W,SW) x N cot, o 64x64."""
import math, numpy as np
from PIL import Image
A='assets/player/'; OUT='assets/player/cape/'
FACE=[(0,1),(.7,.7),(1,0),(.7,-.7),(0,-1),(-.7,-.7),(-1,0),(-.7,.7)]
FRONT={3,4,5}            # N, NE, NW: ao choang nam TREN than
OL=(7,1,1);BASE=(165,16,54);SH=(100,10,35);HI=(188,29,69);FOLD=(107,7,34);GOLD=(243,212,106)
CFG={'idle':dict(sway=.8,trail=5,fl=.6),'walk':dict(sway=1.6,trail=7,fl=1.0),
     'run':dict(sway=2.2,trail=11,fl=1.4),'jump':dict(sway=1.4,trail=9,fl=1.8)}
def cape(anim,d,f,n,bob,lift):
    c=CFG[anim];fx,fy=FACE[d];ph=2*math.pi*f/n
    m=np.zeros((64,64),bool);col=np.zeros((64,64,3),np.uint8)
    wf=abs(fy); ytop=28+bob; hem=ytop+(23 if d in(0,4) else 22)-lift
    wtop=6+8*wf; wbot=wtop+4+4*wf
    if d in(1,3,5,7): wtop,wbot=11,17
    cx0=32-fx*2.5; tr=c['trail']*(1.0 if wf<.9 else .35)
    cx1=cx0-fx*tr
    xs=[];
    for y in range(int(ytop),int(hem)+2):
        u=(y-ytop)/max(1,hem-ytop)
        cx=cx0+(cx1-cx0)*u**1.2+c['sway']*math.sin(ph-u*2.2)*u*(1.2 if wf>.9 else .6)
        hw=(wtop+(wbot-wtop)*u)/2
        for x in range(int(cx-hw),int(cx+hw)+1):
            if not(0<=x<64 and 0<=y<64):continue
            hy=hem+round(c['fl']*1.3*math.sin(x*.9+ph*2))
            if y<=hy:
                m[y,x]=True
                t=(x-(cx-hw))/max(1,2*hw)    # 0..1 ngang
                s=t if fx<=0 and fy>=0 or fx>0 and False else t
                k=BASE
                lead=(t if fx<0 else 1-t) if abs(fx)>.1 else abs(t-.5)*2
                if lead>.72: k=SH
                elif u<.35 and lead<.35: k=HI
                if u>.35 and abs(t-.5)<.07 and (y+x)%2==0: k=FOLD
                if y>=hy-0: k=GOLD
                col[y,x]=k
    col[int(ytop),:][m[int(ytop),:]]=GOLD
    o=np.zeros_like(m)
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):o|=np.roll(np.roll(m,dy,0),dx,1)
    o&=~m
    a=np.zeros((64,64,4),np.uint8);a[m,:3]=col[m];a[m,3]=255;a[o]=(*OL,255)
    return a
def main():
    import os;os.makedirs(OUT,exist_ok=True)
    for anim in['idle','walk','run','jump']:
        base=np.array(Image.open(A+f'base/{anim}.png'));n=base.shape[1]//64
        sb=Image.new('RGBA',(64*n,512));sf=Image.new('RGBA',(64*n,512))
        for d in range(8):
            tops=[int(np.argmax(base[d*64:d*64+64,f*64:f*64+64,3].any(1))) for f in range(n)]
            ref=tops[0]
            for f in range(n):
                bob=tops[f]-ref; lift=0
                if anim=='jump': bob=tops[f]-ref; lift=0
                im=Image.fromarray(cape(anim,d,f,n,bob,lift))
                (sf if d in FRONT else sb).paste(im,(f*64,d*64))
        sb.save(OUT+f'back_{anim}.png');sf.save(OUT+f'front_{anim}.png')
main()
