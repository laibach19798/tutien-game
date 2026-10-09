"""Tạo biến thể kiếm từ sheet kiếm tím: xoay màu, giữ nguyên hình/chuyển động."""
from PIL import Image
import numpy as np, colorsys, os
SRC='/home/claude/tutien/assets/player/sword_purple/attack.png'
V={'sword_gold':(125,1.0),'sword_fire':(80,1.1),'sword_ice':(-100,0.9),'sword_jade':(-160,0.9)}
a=np.array(Image.open(SRC).convert('RGBA'))
ys,xs=np.where(a[...,3]>0)
for name,(deg,sat) in V.items():
    t=a.copy()
    for y,x in zip(ys,xs):
        r,g,b=[int(v)/255 for v in a[y,x,:3]]; h,l,s=colorsys.rgb_to_hls(r,g,b)
        if s>0.25:
            h=(h+deg/360)%1
            if name=='sword_fire': l=min(1,l*1.02)
            r,g,b=colorsys.hls_to_rgb(h,l,min(1,s*sat)); t[y,x,:3]=(round(r*255),round(g*255),round(b*255))
    os.makedirs(f'/home/claude/tutien/assets/player/{name}',exist_ok=True)
    Image.fromarray(t).save(f'/home/claude/tutien/assets/player/{name}/attack.png')
print('ok',list(V))
