#!/usr/bin/env python3
"""Cut a turntable from a free-running orbit clip.

The clip is generated WITHOUT an end pin, because pinning both ends makes the model go out
and come back instead of round — that produced a perfect palindrome folding on frame 19 and
is what "no gira completo / da tumbos" actually was. So the clip over-rotates past its start
and we find the true loop point here.
"""
import subprocess, tempfile, glob, os, shutil, sys, bisect
from PIL import Image, ImageChops, ImageStat

SRC = sys.argv[1] if len(sys.argv) > 1 else 'assets/spin-full.mp4'
t = tempfile.mkdtemp()
subprocess.run(['/opt/homebrew/bin/ffmpeg','-v','error','-i',SRC,
                '-fps_mode','passthrough',f'{t}/r%04d.png'], check=True)
src = sorted(glob.glob(f'{t}/r*.png'))
th  = [Image.open(f).convert('L').resize((160,160), Image.LANCZOS) for f in src]
d   = lambda a,b: ImageStat.Stat(ImageChops.difference(th[a],th[b])).mean[0]
print(f'{len(src)} cuadros crudos')

# 1. True loop point: the later frame that best matches frame 0. Search past the halfway
#    mark so we cannot pick a neighbour of the start.
lo = int(len(src)*0.55)
loop = min(range(lo, len(src)), key=lambda i: d(0, i))
print(f'punto de ciclo: cuadro {loop} (diferencia con el 0: {d(0,loop):.2f})')
th, src = th[:loop+1], src[:loop+1]

# 2. GATE. A real revolution has no twins. A fold has many, symmetric about its turning point.
n = len(th)
twins = []
for i in range(n):
    cand = [(d(i,j), j) for j in range(n) if min(abs(i-j), n-abs(i-j)) > n*0.12]
    if cand:
        dist, j = min(cand)
        if dist < 6: twins.append((i, j, dist))
print(f'cuadros con gemelo lejano: {len(twins)} de {n}')
if len(twins) > n*0.15:
    ax = sum((a+b)/2 for a,b,_ in twins)/len(twins)
    print(f'RECHAZADO: la tira se dobla en ~{ax:.0f}. No es una vuelta, es un vaivén.')
    sys.exit(1)
print('ACEPTADO: vuelta genuina, sin poses repetidas.')

# 3. Sample by cumulative motion, not by time — a model satisfies a constraint by holding
#    still, and equal-time sampling spends frames on those stalls.
cum = [0.0]
for i in range(1, n):
    cum.append(cum[-1] + ImageStat.Stat(ImageChops.difference(th[i-1], th[i])).mean[0])
def pick(k): return bisect.bisect_left(cum, cum[-1]*k)

for name, count, side in [('turn',48,1000), ('turn-m',36,640), ('turn-s',36,440)]:
    idxs = [pick(k/count) for k in range(count)]
    out = f'site/product/{name}'
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    for i, fi in enumerate(idxs):
        Image.open(src[fi]).convert('RGB').resize((side,side), Image.LANCZOS)\
             .save(f'{out}/t_{i+1:04d}.jpg', quality=90, optimize=True)
    im = [Image.open(f).convert('L').resize((200,200),Image.LANCZOS)
          for f in sorted(glob.glob(f'{out}/*.jpg'))]
    st = [ImageStat.Stat(ImageChops.difference(im[i], im[(i+1)%count])).mean[0] for i in range(count)]
    kb = sum(os.path.getsize(x) for x in glob.glob(f'{out}/*.jpg'))//1024
    print(f'  {name:8} {count}f @{side}px · {kb}KB · paso min {min(st):.2f} max {max(st):.2f} '
          f'({min(st)/max(st)*100:.0f}% uniforme)')
