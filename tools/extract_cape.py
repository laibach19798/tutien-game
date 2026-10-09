import numpy as np, json
from PIL import Image
D='/root/.claude/projects/-home-claude-tutien-game/93e4417b-5a7d-56c6-8655-10d96e9547d4/tool-results/mcp-PixelLab-blob-'
# (blob, cell, nframes)  thu tu hang: S,SE,E,NE,N,NW,W,SW
SRC=[('1791518615901-lfulj9',64,8),('1791518618697-b3dsgy',64,8),('1791518620587-vy58va',64,8),
     ('1791518959560-ekb1q9',76,9),('1791518955012-jtlq8n',76,9),('1791518961174-3x7en2',76,9),
     ('1791518963163-txw23h',80,9),('1791518970774-s9tbfv',80,9)]
FRONT={3,4,5}; C=80
def cape_mask(c,bg):
    R,G,B=[c[...,i].astype(float) for i in range(3)]
    red=(G<0.55*R)&(R>60)
    gold=((R-B)>=100)&(G>=160)&(R>200)
    m=(red|gold)&~bg
    from scipy import ndimage as ndi
    lab,nl=ndi.label(m,structure=np.ones((3,3)))
    if nl:
        sz=ndi.sum(m,lab,range(1,nl+1))
        keep=[i+1 for i,v in enumerate(sz) if v>=max(8,0.12*sz.max())]
        m=np.isin(lab,keep)
    dark=(c.sum(2)<110)&~bg
    near=np.zeros_like(m)
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)): near|=np.roll(np.roll(m,dy,0),dx,1)
    return m|(dark&near)
back=Image.new('RGBA',(8*C,8*C));front=Image.new('RGBA',(8*C,8*C))
for r,(b,cell,n) in enumerate(SRC):
    im=np.array(Image.open(D+b+'.png').convert('RGB')).astype(int)
    S=3;cw=cell*S;ch=cell*S+18
    pad=(C-cell)//2
    fr=range(1,9) if n==9 else range(8)
    for k,f in enumerate(fr):
        cx,cy=(f%3)*cw,(f//3)*ch+18
        c=im[cy:cy+cell*S,cx:cx+cw][1::3,1::3]
        bg=(abs(c-np.array([31,37,44])).sum(2)<8)
        m=cape_mask(c,bg)
        a=np.zeros((cell,cell,4),np.uint8);a[...,:3]=c;a[m,3]=255
        t=Image.fromarray(a)
        (front if r in FRONT else back).alpha_composite(t,(k*C+pad,r*C+pad)) if False else (front if r in FRONT else back).paste(t,(k*C+pad,r*C+pad))
back.save('cape_back_walk.png');front.save('cape_front_walk.png')
