"""GIF chém (hướng nam, kiếm tím) -> sheet attack 96x96: thân người (không kiếm) + lớp kiếm/hiệu ứng riêng.
BẢN THỬ: mới có hướng nam nên 8 hàng đều là khung hướng nam."""
from PIL import Image, ImageSequence
import numpy as np
from scipy import ndimage as ndi
GIF='/root/.claude/uploads/93e4417b-5a7d-56c6-8655-10d96e9547d4/6a7411c3-image.gif'
CELL=96; AX=48; AY=76
fr=[np.array(f.convert('RGBA')) for f in ImageSequence.Iterator(Image.open(GIF))]
pal={tuple(int(v) for v in c) for c in fr[0][fr[0][...,3]>0][:,:3]}
lum=lambda a:a[...,0].astype(int)*3+a[...,1].astype(int)*6+a[...,2].astype(int)
SKIN=np.array([239,160,134,255],np.uint8)
m0=fr[0][...,3]>0; ys0,xs0=np.where(m0); top0,bot0=ys0.min(),ys0.max()+1; cx0=xs0.mean()
hip=int(top0+0.62*(bot0-top0))
body_l=[];sw_l=[]
for a in fr:
    m=a[...,3]>0
    inpal=np.array([tuple(int(v) for v in c) in pal for c in a.reshape(-1,4)[:,:3]]).reshape(m.shape)
    core=m&~inpal
    near=ndi.binary_dilation(core,structure=np.ones((3,3)))
    sword=core|(near&m&(lum(a)<10*75))
    body=m&~sword
    lab,n=ndi.label(body,structure=np.ones((3,3)))           # bỏ đốm trắng lẻ còn sót
    if n>1:
        sizes=ndi.sum(body,lab,range(1,n+1)); body=lab==(1+int(np.argmax(sizes)))
    closed=ndi.binary_closing(body,structure=np.ones((3,3)),iterations=2)
    b=a.copy(); b[~body]=0
    holes=(sword&closed&~body)
    b[holes]=SKIN
    # chân/hông bị kiếm hoặc vệt chém che: lấy từ khung đứng yên (chân gần như không đổi)
    legs=sword&m0&~body&(np.arange(a.shape[0])[:,None]>=hip)
    b[legs]=fr[0][legs]
    s=np.zeros_like(a); s[sword]=a[sword]
    body_l.append(b); sw_l.append(s)
dx=int(round(AX-cx0)); dy=AY-bot0
def sheet(L):
    S=Image.new('RGBA',(CELL*len(L),CELL*8))
    for c,a in enumerate(L):
        cell=Image.new('RGBA',(CELL,CELL)); cell.alpha_composite(Image.fromarray(a),(dx,dy))
        assert np.array(cell)[...,3].sum()==a[...,3].astype(int).sum(), ('clip',c)   # không mất pixel
        for r in range(8): S.alpha_composite(cell,(c*CELL,r*CELL))
    return S
import os
os.makedirs('/home/claude/tutien/assets/player/sword_purple',exist_ok=True)
sheet(body_l).save('/home/claude/tutien/assets/player/base/attack.png')
sheet(sw_l).save('/home/claude/tutien/assets/player/sword_purple/attack.png')
print('ok',len(fr),'frames; offset',dx,dy)
