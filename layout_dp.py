import csv, numpy as np, json, os, re, collections
from PIL import Image, ImageDraw
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
files={re.sub(r'^\d+_','',fn).replace('.jpg',''):fn for fn in os.listdir('beinecke')}
pages=['103r','103v','104r','104v','105r','105v','106r','106v','107r','107v','108r','108v','111r','111v','112r','112v','113r','113v','114r','114v','115r','115v','116r']
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['ltype'].startswith('P')]
out=[]
for pg in pages:
    fn=files[pg]; folio='f'+pg
    tr=[r for r in rows if r['folio']==folio]
    a=np.asarray(Image.open('beinecke/'+fn).convert('L')); h,w=a.shape
    from scipy.ndimage import uniform_filter
    bg=uniform_filter(a.astype(float),151)
    ink=a<150
    inks=a<bg*0.70
    bgc=uniform_filter1d(((a<60).mean(0)>0.3).astype(float),121)>0; ink[:,bgc]=False; inks[:,bgc]=False
    bgr=uniform_filter1d(((a<60).mean(1)>0.3).astype(float),121)>0; ink[bgr,:]=False; inks[bgr,:]=False
    colf=uniform_filter1d(ink[int(0.15*h):int(0.85*h),:].mean(0),25)
    # text block = longest run of columns with colf>0.04
    on=colf>0.04; best=(0,0); s=None
    for x in range(w):
        if on[x] and s is None: s=x
        if (not on[x] or x==w-1) and s is not None:
            if x-s>best[1]-best[0]: best=(s,x)
            s=None
    tb0,tb1=best
    xi0,xi1=tb0+int(0.15*(tb1-tb0)), tb1-int(0.15*(tb1-tb0))   # interior for row detection
    proj=ink[:,xi0:xi1].sum(1).astype(float); sm=uniform_filter1d(proj,21)
    peaks,_=find_peaks(sm,distance=36,prominence=15)
    peaks=[int(p) for p in peaks if 0.04*h<p<0.96*h]
    gaps=np.diff(peaks); pitch=np.median(gaps[(gaps>45)&(gaps<90)]) if len(gaps) else 62
    # DP alignment: lines j=0..n-1 to peaks i (increasing). cost of assigning line j to peak i given line j-1 at peak k:
    n=len(tr); m=len(peaks); INF=1e9
    same=[j>0 and tr[j]['para']==tr[j-1]['para'] for j in range(n)]
    def gapcost(g,j):
        if same[j]: return abs(g-pitch)/pitch*10          # within paragraph: expect ~pitch
        return (max(0,pitch*0.9-g)/pitch*10) + max(0,(g-2.5*pitch))/pitch*5   # between paragraphs: >= pitch, not huge
    D=np.full((n,m),INF); B=np.full((n,m),-1,int)
    for i in range(m): D[0,i]=0
    for j in range(1,n):
        for i in range(j,m):
            for k in range(j-1,i):
                c=D[j-1,k]+gapcost(peaks[i]-peaks[k],j)
                if c<D[j,i]: D[j,i]=c; B[j,i]=k
    i=int(np.argmin(D[n-1])); tot=D[n-1,i]; assign=[0]*n
    for j in range(n-1,-1,-1): assign[j]=i; i=B[j,i]
    # measure edges
    x0=max(0,tb0-55); x1=min(w,tb1+int(0.03*(tb1-tb0)))
    res=[]
    valid=[True]*n
    for j in range(1,n):
        g=peaks[assign[j]]-peaks[assign[j-1]]
        if same[j] and abs(g-pitch)>0.25*pitch: valid[j]=False; valid[j-1]=False
        if not same[j] and (g<0.8*pitch or g>2.5*pitch): valid[j]=False
    for j,r in enumerate(tr):
        if not valid[j]: continue
        p=peaks[assign[j]]; band=inks[max(0,p-9):p+9,:]; cc=band.sum(0).astype(float); dens=uniform_filter1d(cc,40)*40
        xs=np.where(dens[x0:x1]>=30)[0]
        if not len(xs): continue
        res.append(dict(folio=folio,text=r['text'],pstart=r['pstart'],pend=r['pend'],left=int(x0+xs[0]),right=int(x0+xs[-1]),y=p,tb0=int(tb0),tb1=int(tb1)))
    c=[d['right']-d['left'] for d in res if d['pend']=='0']; f=[d['right']-d['left'] for d in res if d['pend']=='1']
    print(f'{folio}: peaks {m} lines {n} pitch {pitch:.0f} cost/line {tot/n:.2f}  width cont {np.mean(c):.0f}±{np.std(c):.0f} final {np.mean(f):.0f}±{np.std(f):.0f}  text block {tb0}-{tb1}')
    out+=res
    if folio in ('f104v','f107r'):
        ov=Image.open('beinecke/'+fn).convert('RGB'); dr=ImageDraw.Draw(ov)
        for d in res: dr.line([(d['left'],d['y']),(d['right'],d['y'])],fill=(255,0,0) if d['pend']=='0' else (0,0,255),width=5)
        ov.thumbnail((1400,1400)); ov.save(f'crops/overlay_{folio}.png')
json.dump(out,open('data/layout.json','w')); print('lines',len(out))
