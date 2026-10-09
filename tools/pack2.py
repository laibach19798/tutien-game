"""Ghép zip PixelLab (nhiều animation) -> sheet 8 hàng hướng. Offset/scale cố định mỗi hướng, lấy từ Walking, áp cho mọi animation."""
from PIL import Image
import numpy as np, glob, os, statistics, sys
SRC='/home/claude/pl4/Idle'; OUT='/home/claude/tutien/assets/player/base'
ORDER=['south','south-east','east','north-east','north','north-west','west','south-west']
CW=CH=64; AX=32; GROUND=60
SHEETS={'walk':'Walking','idle':'Breathing_Idle','run':'Running','jump':'Jumping'}
def bbox(im):
    a=np.array(im)[...,3]; ys,xs=np.where(a>0); w=a[ys,xs].astype(float)
    return xs.min(),ys.min(),xs.max()+1,ys.max()+1,float((xs*w).sum()/w.sum())
def load(anim,d): return [Image.open(f).convert('RGBA') for f in sorted(glob.glob(f'{SRC}/animations/{anim}/{d}/*.png'))]
walkf={d:load('Walking',d) for d in ORDER}
H={d:statistics.mean(bbox(f)[3]-bbox(f)[1] for f in walkf[d]) for d in ORDER}
T=statistics.median(H.values())
SCALE={d:(T/H[d] if T/H[d]>1.04 else 1.0) for d in ORDER}
OFF={}
for d in ORDER:
    bbs=[bbox(f) for f in walkf[d]]
    OFF[d]=(round(AX-statistics.mean(b[4] for b in bbs)),round(GROUND-statistics.median(b[3] for b in bbs)))
print('H',{d:round(h,1) for d,h in H.items()},'scale',{d:round(v,3) for d,v in SCALE.items()},'off',OFF)
def put(sheet,im,c,r,d,ex=0):
    dx,dy=OFF[d]; dy+=ex; s=SCALE[d]; cell=Image.new('RGBA',(CW,CH)); cell.paste(im,(dx,dy))
    if s!=1.0:
        n=round(CW*s); g=cell.resize((n,n),Image.NEAREST); cell=Image.new('RGBA',(CW,CH))
        cell.paste(g,(round(AX-AX*n/CW),round(GROUND-GROUND*n/CH)))
    sheet.alpha_composite(cell,(c*CW,r*CH))
os.makedirs(OUT,exist_ok=True)
for f in glob.glob(OUT+'/*'): os.remove(f)
meta={}
for name,anim in SHEETS.items():
    fr={d:load(anim,d) for d in ORDER}; n={len(v) for v in fr.values()}; assert len(n)==1,(anim,n); n=n.pop()
    sh=Image.new('RGBA',(CW*n,CH*8))
    for r,d in enumerate(ORDER):
        # nếu animation (vd. nhảy) tụt khỏi ô 64px: dịch cả hướng lên/xuống 1 lượng cố định để không mất pixel
        lo=min(bbox(f)[1]+OFF[d][1] for f in fr[d]); hi=max(bbox(f)[3]+OFF[d][1] for f in fr[d])
        ex=-(hi-CH) if hi>CH else (-lo if lo<0 else 0)
        if ex: print('shift',name,d,ex)
        for c,im in enumerate(fr[d]): put(sh,im,c,r,d,ex)
    a=np.array(sh)[...,3]
    for r,d in enumerate(ORDER):
        for c in range(n):   # không mất pixel nào khi cắt về ô 64x64 (scale=1 nên so số pixel gốc)
            src=int((np.array(fr[d][c])[...,3]>0).sum()); got=int((a[r*CH:(r+1)*CH,c*CW:(c+1)*CW]>0).sum())
            assert SCALE[d]!=1.0 or src==got,('clip',name,d,c,src,got)
    sh.save(f'{OUT}/{name}.png'); meta[name]=n; print(name,anim,n,'frames ok')
print(meta)
