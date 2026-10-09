"""Tạo lớp skin cho sheet attack (ô 96x96) bằng cùng hàm của skins.py."""
import sys; sys.path.insert(0,'/home/claude/tools')
import numpy as np, skins
skins.CW=skins.CH=96
skins.Y,skins.X=np.mgrid[0:96,0:96]
for k,fn in skins.LAYERS.items(): skins.build(k,fn,sheets=('attack',))
print('attack skins built')
