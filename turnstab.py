#!/usr/bin/env python3
"""turnstab.py <video.mp4> — is this actually a turntable, or a wandering camera?

A product turntable has exactly one job: the object rotates and NOTHING else changes.
Eyeballing a contact sheet catches gross failures but not the slow drift that makes a
loop feel cheap, so measure it. The object sits on pure black, which makes the silhouette
trivially separable — no model needed, just a threshold.

Reports, across every frame:
  height  vertical extent of the silhouette  -> scale drift
  cy      vertical centre of that extent    -> bob
  cx      horizontal centre                 -> lateral slide

MEASURE THE BOUNDING BOX, NOT THE CENTROID. The centre of mass of an asymmetric object
moves legitimately as it turns, so a centroid-based meter reports ~20% drift on a shot
that is in fact locked — it condemns good footage. Vertical extent is the true invariant
of a vertical-axis spin; width is not (a helmet is genuinely narrower head-on).

Drift is expressed as a percentage of the object's own size, which is the only scale
that means anything. Under ~1.5% reads as locked; past ~4% the eye sees it swim.
"""
import sys, subprocess, tempfile, os, glob
from PIL import Image

SRC = sys.argv[1]
THRESH = int(sys.argv[2]) if len(sys.argv) > 2 else 26   # 0-255 luma over pure black
STEP = 4

tmp = tempfile.mkdtemp()
subprocess.run(['/opt/homebrew/bin/ffmpeg', '-v', 'error', '-i', SRC,
                '-vf', f"select='not(mod(n\\,{STEP}))',scale=240:-1",
                '-fps_mode', 'passthrough', f'{tmp}/f%04d.png'], check=True)

rows = []
for p in sorted(glob.glob(f'{tmp}/*.png')):
    im = Image.open(p).convert('L')
    w, h = im.size
    px = im.load()
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        for x in range(w):
            if px[x, y] > THRESH:
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    if x1 >= 0:
        rows.append(((x0 + x1) / 2, (y0 + y1) / 2, y1 - y0))

if len(rows) < 4:
    sys.exit('not enough frames resolved — is the background actually black?')

cx = [r[0] for r in rows]; cy = [r[1] for r in rows]; ht = [r[2] for r in rows]
size = sum(ht) / len(ht)                   # object's height in px — the invariant

def swing(v): return max(v) - min(v)

bob   = swing(cy) / size * 100
slide = swing(cx) / size * 100
zoom  = swing(ht) / size * 100

print(f'{len(rows)} frames sampled, object ~{size:.0f}px')
print(f'  bob   (vertical drift)  {bob:5.1f}%  of object size')
print(f'  slide (lateral drift)   {slide:5.1f}%')
print(f'  zoom  (height drift)    {zoom:5.1f}%')

# The loop is the other half: a turntable that does not return to its start cannot be
# scrubbed endlessly without a visible jump at the seam.
first, last = rows[0], rows[-1]
close = (abs(first[1] - last[1]) / size * 100,
         abs(first[2] - last[2]) / size * 100)
print(f'  loop close: dy {close[0]:.1f}%  dscale {close[1]:.1f}%')

worst = max(bob, slide, zoom)
print()
if worst < 1.5:   print('LOCKED — reads as a rig. Ship it.')
elif worst < 4:   print('ACCEPTABLE — slight swim, invisible at display size.')
else:             print(f'WANDERING ({worst:.1f}%) — the camera is moving. Re-prompt, do not upscale.')
