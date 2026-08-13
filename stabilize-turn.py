#!/usr/bin/env python3
"""stabilize-turn.py <video.mp4> <out-dir> — turn a wandering orbit into a rig shot.

Video models will not hold a locked-off turntable: the object drifts and breathes in
scale even when the prompt forbids both. That defect is GEOMETRIC and global, which is
exactly the kind a post pass can fix — unlike a generated artefact sitting in the middle
of the action, which only a regeneration cures. Do not confuse the two cases.

Method: the object sits on pure black, so its silhouette is separable with a threshold.
Normalise every frame so the silhouette has the same VERTICAL EXTENT and the same centre.

Height, never width: a helmet rotating about a vertical axis is genuinely narrower head-on
than in profile, so normalising width would fight the rotation itself and squash the object
on every quarter turn. Height is the invariant of a vertical-axis spin.
"""
import sys, os, glob, subprocess, tempfile, statistics
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
THRESH = int(sys.argv[3]) if len(sys.argv) > 3 else 26
FF = '/opt/homebrew/bin/ffmpeg'

tmp = tempfile.mkdtemp()
subprocess.run([FF, '-v', 'error', '-i', SRC, '-fps_mode', 'passthrough',
                f'{tmp}/r%04d.png'], check=True)
files = sorted(glob.glob(f'{tmp}/r*.png'))
if not files: sys.exit('no frames extracted')

def bbox(im):
    g = im.convert('L'); w, h = g.size; px = g.load()
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(0, h, 2):                       # every other row is plenty
        for x in range(0, w, 2):
            if px[x, y] > THRESH:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    return None if x1 < 0 else (x0, y0, x1, y1)

boxes = []
for f in files:
    b = bbox(Image.open(f))
    boxes.append(b)
    if b is None: print('  warn: empty frame', os.path.basename(f))

good = [b for b in boxes if b]
tgtH  = statistics.median(b[3] - b[1] for b in good)
tgtCX = statistics.median((b[0] + b[2]) / 2 for b in good)
tgtCY = statistics.median((b[1] + b[3]) / 2 for b in good)
print(f'{len(files)} frames · target height {tgtH:.0f}px, centre ({tgtCX:.0f},{tgtCY:.0f})')

os.makedirs(OUT, exist_ok=True)
for i, (f, b) in enumerate(zip(files, boxes)):
    im = Image.open(f).convert('RGB'); W, H = im.size
    if b:
        s  = tgtH / max(1, (b[3] - b[1]))
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        # scale about the object's own centre, then move that centre to the target
        nw, nh = int(round(W * s)), int(round(H * s))
        im = im.resize((nw, nh), Image.LANCZOS)
        ox = int(round(tgtCX - cx * s)); oy = int(round(tgtCY - cy * s))
        canvas = Image.new('RGB', (W, H), (0, 0, 0))
        canvas.paste(im, (ox, oy))
        im = canvas
    im.save(f'{OUT}/t_{i+1:04d}.jpg', quality=92, optimize=True)

print(f'wrote {len(files)} frames to {OUT}')
