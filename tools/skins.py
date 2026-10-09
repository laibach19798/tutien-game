"""Tạo skin tối giản từ sheet base (walk.png / idle.png: 8 hàng hướng x 8 cột, ô 64x64).
Mỗi lớp là một sheet cùng bố cục, chỉ chứa pixel của món đồ, nên có thể gắn chồng lên base."""
from PIL import Image
import numpy as np
from scipy import ndimage as ndi
import os, sys

BASE = '/home/claude/tutien/assets/player/base'
OUT = '/home/claude/tutien/assets/player'
CW = CH = 64
ROWS = ['S', 'SE', 'E', 'NE', 'N', 'NW', 'W', 'SW']
# (s, view): s = +1 nhìn sang phải, -1 sang trái; view = front/side/back
FACE = {'S': (0, 'front'), 'SE': (1, 'front'), 'SW': (-1, 'front'),
        'E': (1, 'side'), 'W': (-1, 'side'),
        'N': (0, 'back'), 'NE': (1, 'back'), 'NW': (-1, 'back')}
Y, X = np.mgrid[0:CH, 0:CW]

HAIR = dict(line=(22, 16, 30), dark=(44, 36, 58), mid=(68, 58, 88), hi=(110, 98, 132), pin=(222, 184, 88))
ROBE = dict(line=(64, 60, 92), light=(240, 238, 248), shade=(198, 195, 220), belt=(52, 66, 112),
            belt_hi=(84, 102, 158), collar=(146, 142, 180))
SHOE = dict(line=(24, 22, 30), main=(58, 56, 72), hi=(92, 90, 110))


def shift(m, dx, dy):
    r = np.zeros_like(m)
    ys, xs = slice(max(dy, 0), CH + min(dy, 0)), slice(max(dx, 0), CW + min(dx, 0))
    yd, xd = slice(max(-dy, 0), CH + min(-dy, 0)), slice(max(-dx, 0), CW + min(-dx, 0))
    r[ys, xs] = m[yd, xd]
    return r


def border(mask, solid):
    """pixel của mask có hàng xóm 4 hướng không thuộc mask và cũng không thuộc 'solid' (phần đã có pixel)."""
    out = np.zeros_like(mask)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb = shift(mask, dx, dy)  # nb[p] = mask[p - d]; ta cần hàng xóm tại p+d => dùng shift ngược
        nb = shift(mask, -dx, -dy)
        out |= mask & ~nb & ~shift(solid, -dx, -dy)
    return out


def border_any(mask):
    out = np.zeros_like(mask)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        out |= mask & ~shift(mask, -dx, -dy)
    return out


def geom(base):
    a = base[..., 3] > 0
    ys, xs = np.where(a)
    top = ys.min()
    head = a[top:top + 20]
    hw = head.sum(1).max()
    cx = np.where(head)[1].mean()
    torso = a[top + 24:top + 39]
    cxb = np.where(torso)[1].mean() if torso.any() else cx
    return a, top, hw, cx, cxb


def paint(out, mask, col):
    out[mask] = (*col, 255)


# ---------------------------------------------------------------- TÓC (búi tóc + đuôi tóc)
def hair_cell(base, name):
    a, top, hw, cx, cxb = geom(base)
    s, view = FACE[name]
    out = np.zeros((CH, CW, 4), np.uint8)
    dx = X - cx
    ell = ((dx / (hw / 2 + 0.7)) ** 2 + ((Y - (top + 9.5)) / 11.0) ** 2 <= 1) & (Y <= top + 19)
    if view == 'front':
        yh = top + 6 + np.clip(np.abs(dx) * 0.55, 0, 6) + (X % 3 == 0)
        if s:
            yh = np.where(-s * dx > 1.5, top + 15, yh)
        cap = ell & (Y < yh)
    elif view == 'back':
        cap = ell.copy()
        if s:
            cap &= ~((dx * s > hw / 2 - 3.5) & (Y > top + 9))
    else:
        f = dx * s
        yh = np.interp(f, [-11, -3, 0, 3, 11], [top + 19, top + 17, top + 10, top + 6, top + 7])
        cap = ell & (Y < yh)
    # búi tóc trên đỉnh
    kx = cx - s * (2.2 if view == 'side' else 1.0)
    ky = top - 1.0
    knot = (((X - kx) / 4.6) ** 2 + ((Y - ky) / 3.6) ** 2) <= 1
    tail = np.zeros_like(cap)
    if view == 'back':
        tx = cx - s * 1.5
        for t in range(18):
            w = 2.6 - t * 0.07
            tail |= (np.abs(X - tx) <= w) & (Y == top + 17 + t)
    elif view == 'side':
        bx = cx - s * (hw / 2 - 0.5)
        for t in range(21):
            x = bx - s * (0.6 + 2.0 * np.sin(t * 0.15))
            tail |= (np.abs(X - x) <= 2.5 - t * 0.05) & (Y == top + 6 + t)
    hair = cap | knot | tail
    paint(out, hair, HAIR['dark'])
    # đường sáng chéo cho tóc
    stripe = hair & (((X - cx) + 2 * (Y - top)) % 7 == 0) & (Y < top + 12)
    paint(out, stripe, HAIR['mid'])
    paint(out, hair & (X < cx - 2) & (Y < top + 3) & (Y >= top - 2), HAIR['hi'])
    paint(out, knot & (X < kx) & (Y < ky), HAIR['mid'])
    # viền ngoài: chỉ nơi hàng xóm trống (không phải da/đồ khác)
    solid = a | hair
    ring = np.zeros_like(hair)
    for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ring |= hair & ~shift(solid, -ddx, -ddy)
    paint(out, ring, HAIR['line'])
    # trâm cài tóc
    pin_y = int(round(ky))
    pin = (Y == pin_y) & (np.abs(X - kx) <= 5.2)
    paint(out, pin & (np.abs(X - kx) > 3.2) | (pin & (np.abs(X - kx) <= 1.0)), HAIR['pin'])
    return out


# ---------------------------------------------------------------- ĐẠO BÀO
def robe_cell(base, name):
    a, top, hw, cx, cxb = geom(base)
    s, view = FACE[name]
    out = np.zeros((CH, CW, 4), np.uint8)
    y0, y1 = top + 21, min(top + 44, CH - 1)
    m = np.zeros_like(a)
    m[y0:y1 + 1] = a[y0:y1 + 1]

    def dil(mk, k):
        r = mk.copy()
        for i in range(1, k + 1):
            r |= shift(mk, i, 0) | shift(mk, -i, 0)
        return r
    rows = np.arange(CH)[:, None] * np.ones((1, CW), int)
    mm = m.copy()
    sl = (rows >= top + 24) & (rows <= y1)
    mm = np.where(sl, dil(m, 1), mm)
    hh = (rows >= top + 42) & (rows <= y1)
    mm = np.where(hh, dil(m, 2), mm)
    # đai giữa thân: bịt kín khe giữa hai chân trong vạt áo
    for yy in range(top + 40, min(y1, CH - 1) + 1):
        xs = np.where(mm[yy])[0]
        if len(xs) and view != 'side':
            mm[yy, xs.min():xs.max() + 1] = True
    lum = base[..., 0] * .3 + base[..., 1] * .59 + base[..., 2] * .11
    med = np.median(lum[m & a]) if (m & a).any() else 200
    shade = (lum < med - 7) & a
    paint(out, mm, ROBE['light'])
    paint(out, mm & shade, ROBE['shade'])
    # nếp vạt dưới: sọc đứng mờ
    paint(out, mm & (rows > top + 35) & ((X - int(cxb)) % 5 == 0), ROBE['shade'])
    # đai lưng
    b0 = top + 31
    for yy, col in ((b0, ROBE['belt_hi']), (b0 + 1, ROBE['belt'])):
        row = mm[yy]
        xs = np.where(row)[0]
        if len(xs):
            paint(out, (Y == yy) & mm, col)
    xs = np.where(mm[b0])[0]
    if len(xs):
        if view == 'side':
            kx = xs.min() + 1 if s > 0 else xs.max() - 1
        else:
            kx = int(round(cxb + (s * 1)))
        blk = (np.abs(X - kx) <= 1) & (Y >= b0 - 1) & (Y <= b0 + 3)
        paint(out, blk, ROBE['belt'])
        tail = (np.abs(X - (kx - (s if view == 'side' else 0))) <= 0) & (Y >= b0 + 3) & (Y <= b0 + 6)
        paint(out, tail & mm, ROBE['belt'])
    # cổ áo
    cxx = int(round(cxb + s))
    col = ROBE['collar']
    if view == 'front':
        for i in range(7):
            for xx in (cxx - 5 + i, cxx + 5 - i):
                if 0 <= xx < CW and mm[top + 21 + i, xx]:
                    out[top + 21 + i, xx] = (*col, 255)
    elif view == 'back':
        paint(out, (Y == top + 21) & (np.abs(X - cxx) <= 4) & mm, col)
        paint(out, (Y == top + 22) & (np.abs(X - cxx) <= 2) & mm, col)
    else:
        for i in range(5):
            xx = cxx + s * (1 + i)
            if 0 <= xx < CW and mm[top + 21 + i, xx]:
                out[top + 21 + i, xx] = (*col, 255)
    # viền
    ring = border_any(mm)
    paint(out, ring, ROBE['line'])
    return out


# ---------------------------------------------------------------- GIÀY VẢI
def shoes_cell(base, name):
    a, top, hw, cx, cxb = geom(base)
    out = np.zeros((CH, CW, 4), np.uint8)
    legs = a & (Y >= top + 45)
    split = int(round(cxb))
    sh = np.zeros_like(a)
    for half in (X < split, X >= split):
        h = legs & half
        if h.any():
            ym = np.where(h)[0].max()
            sh |= h & (Y > ym - 5)
    paint(out, sh, SHOE['main'])
    paint(out, sh & (Y == sh.any(1).argmax()), SHOE['hi'])
    # mép trên ủng sáng hơn
    top_edge = sh & ~shift(sh, 0, 1)
    paint(out, top_edge, SHOE['hi'])
    ring = np.zeros_like(sh)
    for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ring |= sh & ~shift(a | sh, -ddx, -ddy)
    paint(out, ring, SHOE['line'])
    return out


LAYERS = {'hair_topknot': hair_cell, 'robe_dao_bao': robe_cell, 'shoes_cloth': shoes_cell}


def build(layer, fn, sheets=('walk', 'idle', 'run', 'jump')):
    d = f'{OUT}/{layer}'
    os.makedirs(d, exist_ok=True)
    for sheet in sheets:
        src = np.array(Image.open(f'{BASE}/{sheet}.png').convert('RGBA'))
        res = np.zeros_like(src)
        for r, name in enumerate(ROWS):
            for c in range(src.shape[1] // CW):
                cell = src[r * CH:(r + 1) * CH, c * CW:(c + 1) * CW]
                if (cell[..., 3] > 0).any():
                    res[r * CH:(r + 1) * CH, c * CW:(c + 1) * CW] = fn(cell, name)
        Image.fromarray(res).save(f'{d}/{sheet}.png')


if __name__ == '__main__':
    for k, fn in LAYERS.items():
        build(k, fn)
    print('built', list(LAYERS))
