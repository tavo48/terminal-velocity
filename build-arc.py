from PIL import Image, ImageChops, ImageStat, ImageDraw
import numpy as np, glob, os, shutil
fs=sorted(glob.glob('/tmp/b2/f_*.png'))[:240]
S=np.load('/tmp/b2/S.npy'); c=S.max()/S; W=Image.open(fs[0]).size[0]
FRONT=223                       # picked by eye off the contact sheet; every automatic metric
                                # I tried disagreed with the others and two of them were wrong
def stab(m,size=None):
    s=c[m]
    im=Image.open(fs[m]).convert('RGB').transform((W,W),Image.AFFINE,
        (1/s,0,(W/2)*(1-1/s), 0,1/s,(W/2)*(1-1/s)),Image.BICUBIC)
    return im.resize((size,size),Image.LANCZOS) if size else im
small=[stab(m,400) for m in range(240)]
def corner(im):
    L=np.asarray(im.convert('L'),float)
    v=[L[0:28,0:28].mean(),L[0:28,-28:].mean(),L[-28:,0:28].mean(),L[-28:,-28:].mean()]
    return max(v)-min(v)
co=np.array([corner(im) for im in small])
th=[im.convert('L').resize((160,160),Image.LANCZOS) for im in small]

k=0
while k<60 and all(co[(FRONT+d)%240] < 3.0 for d in range(-(k+1),k+2)): k+=1
idxs=[(FRONT-k+i)%240 for i in range(2*k+1)]
print(f'frente máster {FRONT} · arco +/-{k} = {2*k/240*360:.0f}° · esquinas máx {co[idxs].max():.1f}')

cum=np.concatenate([[0.0],np.cumsum([ImageStat.Stat(ImageChops.difference(th[idxs[i-1]],th[idxs[i]])).mean[0]
                                     for i in range(1,len(idxs))])])
N=36
pick=list(np.searchsorted(cum,np.linspace(0,cum[-1],N)).clip(0,len(idxs)-1))
for j in range(1,N):
    if pick[j]<=pick[j-1]: pick[j]=min(pick[j-1]+1,len(idxs)-1)
out=[stab(idxs[p]) for p in pick]
for name,side in [('turn',1000),('turn-lo',300),('turn-m',640),('turn-s',440)]:
    d=f'site/product/{name}'; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    for j,im in enumerate(out): im.resize((side,side),Image.LANCZOS).save(f'{d}/t_{j+1:04d}.jpg',quality=90,optimize=True)
gl=sorted(glob.glob('site/product/turn/t_*.jpg'))
g=[Image.open(f).convert('L').resize((200,200),Image.LANCZOS) for f in gl]
st=[ImageStat.Stat(ImageChops.difference(g[i],g[i+1])).mean[0] for i in range(N-1)]
med=sorted(st)[len(st)//2]
CO=[corner(Image.open(f)) for f in gl]
print(f'paso mín {min(st):.2f} · mediana {med:.2f} · máx {max(st):.2f} · saltos {sum(1 for s in st if s>med*1.8)} · congelados {sum(1 for s in st if s<med*0.4)}')
print(f'grados/paso {2*k/240*360/(N-1):.1f}° · borde máx {max(CO):.1f} · el frente debe caer en t_{N//2+1:02d}')
s=300; sh=Image.new('RGB',(6*s,2*s),(0,0,0)); dr=ImageDraw.Draw(sh)
for kk,i in enumerate(range(0,36,3)):
    sh.paste(Image.open(gl[i]).resize((s,s),Image.LANCZOS),((kk%6)*s,(kk//6)*s))
    dr.line([(kk%6)*s,(kk//6)*s+int(s*0.20),(kk%6)*s+s,(kk//6)*s+int(s*0.20)],fill=(0,220,130))
    dr.text(((kk%6)*s+8,(kk//6)*s+6),f't_{i+1:02d}',fill=(255,190,60))
sh.save('/tmp/arc4.jpg',quality=90)
