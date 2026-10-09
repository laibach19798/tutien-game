import numpy as np
from PIL import Image
exec(open('align.py').read().split("res={}")[0])
def shift(a,dx,dy):
    return np.roll(np.roll(a,dy,0),dx,1)
def score(F,bm,s,dx,dy,rows=slice(0,80)):
    return sum(((a:=shift(F[(f+s)%8],dx,dy)[rows])&(b:=bm[f][rows])).sum()/max(1,(a|b).sum()) for f in range(8))/8
back=Image.new('RGBA',(8*C,8*C));front=Image.new('RGBA',(8*C,8*C))
cap_frames=lambda r:None
log=[]
for r in range(8):
    F=frames(r);bm=[]
    for f in range(8):
        m=np.zeros((80,80),bool);m[8:72,8:72]=base[r*64:(r+1)*64,f*64:(f+1)*64,3]>0;bm.append(m)
    head=slice(0,36)   # dau + vai (it bi ao che)
    cand=[(score(F,bm,s,dx,dy,head),s,dx,dy) for s in range(8) for dx in range(-6,7) for dy in range(-6,7)]
    s0=max(c for c in cand if c[1]==0);sb=max(cand)
    pick=sb if sb[0]-s0[0]>0.04 else s0
    _,s,dx,dy=pick;log.append((r,s,dx,dy,round(s0[0],2),round(sb[0],2)))
    # cat ao theo cung pipeline ex.py
    b,cell,n=SRC[r];im=np.array(Image.open(D+b+'.png').convert('RGB')).astype(int)
    fr=list(range(1,9)) if n==9 else list(range(8));p=(80-cell)//2
    tiles=[]
    for f in fr:
        cw=cell*3;ch=cell*3+18;cx,cy=(f%3)*cw,(f//3)*ch+18
        c=im[cy:cy+cell*3,cx:cx+cw][1::3,1::3]
        bgm=(abs(c-np.array([31,37,44])).sum(2)<8);m=cape_mask(c,bgm)
        a=np.zeros((80,80,4),np.uint8);a[p:p+cell,p:p+cell,:3]=c;a[p:p+cell,p:p+cell,3]=255*m
        tiles.append(a)
    for k in range(8):
        a=shift(tiles[(k+s)%8],dx,dy)
        (front if r in FRONT else back).paste(Image.fromarray(a),(k*C,r*C))
for l in log:print(l)
back.save('cape_back_walk.png');front.save('cape_front_walk.png')
