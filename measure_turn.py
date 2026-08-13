"""Silhouette measurement that survives the floor reflection.

A plain threshold mask includes the helmet AND its reflection on the black floor, and the
reflection fades in and out with the angle. That moved the measured bottom edge by 198px
between adjacent frames — 20% of the object — and normalising scale against that reading
injected exactly the lurch the stabiliser exists to remove. So keep only the largest
connected blob: the helmet, never its ghost.
"""
from PIL import Image
import numpy as np
from collections import deque

def silhouette(path, thresh=18, work=360):
    im = Image.open(path).convert('L')
    W  = im.size[0]
    a  = np.asarray(im.resize((work, work), Image.BILINEAR))
    m  = a > thresh
    seen = np.zeros_like(m, bool)
    best = None; bestn = 0
    ys0, xs0 = np.where(m)
    for sy, sx in zip(ys0, xs0):
        if seen[sy, sx]: continue
        q = deque([(sy, sx)]); seen[sy, sx] = True; cells = []
        while q:
            y, x = q.popleft(); cells.append((y, x))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny, nx = y+dy, x+dx
                if 0 <= ny < work and 0 <= nx < work and m[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx] = True; q.append((ny,nx))
        if len(cells) > bestn: bestn = len(cells); best = cells
    ys = np.array([c[0] for c in best], float); xs = np.array([c[1] for c in best], float)
    k = W / work
    y0,y1 = np.percentile(ys,[0.4,99.6]); x0,x1 = np.percentile(xs,[0.4,99.6])
    return (y1-y0)*k, (x0+x1)/2*k, (y0+y1)/2*k
