import csv, numpy as np, json, os, re
from PIL import Image
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
files={f:fn for fn in os.listdir('beinecke') for f in [re.sub(r'^\d+_','',fn).replace('.jpg','')]}
# quire 20 text pages + other text-only pages
pages=['103r','103v','104r','104v','105r','105v','106r','106v','107r','107v','108r','108v','111r','111v','112r','112v','113r','113v','114r','114v','115r','115v','116r','58r','58v','85r_part','76r']
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['ltype'].startswith('P')]
out=[]
for pg in pages:
    fn=files.get(pg); folio='f'+pg.replace('_part','')
    if not fn: print('missing',pg); continue
    tr=[r for r in rows if r['folio']==folio]
    im=Image.open('beinecke/'+fn).convert('L'); a=np.asarray(im); h,w=a.shape
    dark=(a<60).mean(0)           # column fraction that is near-black: background/binding
    cols=np.where(dark<0.5)[0]     # vellum columns
    px0,px1=cols[0],cols[-1]
    rowdark=(a<60).mean(1); rws=np.where(rowdark<0.5)[0]; py0,py1=rws[0],rws[-1]
    ink=a<150; m=int(0.03*h); ink[:py0+m,:]=False; ink[py1-m:,:]=False; ink[:,:px0+40]=False; ink[:,px1-40:]=False
    x0=int(px0+0.11*(px1-px0))
    colf=uniform_filter1d(ink[int(0.15*h):int(0.85*h),:].mean(0),25)
    mid=(px0+px1)//2; xr=[x for x in range(mid,px1) if colf[x]<0.008]
    x1=xr[0] if xr else int(px1-0.02*(px1-px0))
    proj=ink[:,x0:x1].sum(1).astype(float); sm=uniform_filter1d(proj,15)
    got=None
    for dist in [40,45,35,50,30]:
        for prom in [0.5,0.3,0.2,0.15,0.1,0.7]:
            peaks,_=find_peaks(sm,distance=dist,prominence=np.percentile(sm,60)*prom)
            peaks=[p for p in peaks if sm[p]>np.percentile(sm,40)]
            if len(peaks)==len(tr): got=peaks; break
        if got is not None: break
    if got is None: print(f'{folio}: no match (lines {len(tr)})'); continue
    lefts=[];rights=[]
    for p in got:
        band=ink[max(0,p-9):p+9,:]; cols=band.sum(0).astype(float)
        dens=uniform_filter1d(cols,40)*40   # ink pixels in a 40-px window
        xs=np.where(dens[x0:x1]>=30)[0]
        lefts.append(int(x0+xs[0]) if len(xs) else -1); rights.append(int(x0+xs[-1]) if len(xs) else -1)
    # sanity: left edges should be tightly clustered for non-paragraph-initial lines
    L=np.array(lefts); med=np.median(L)
    if folio=='f104v':
        from PIL import ImageDraw
        ov=Image.open('beinecke/'+fn).convert('RGB'); dr=ImageDraw.Draw(ov)
        for p,l,rt in zip(got,lefts,rights): dr.line([(l,p),(rt,p)],fill=(255,0,0),width=4); dr.line([(l,p-20),(l,p+20)],fill=(0,0,255),width=6)
        ov.thumbnail((1400,1400)); ov.save('crops/overlay_f104v.png')
    print(f'{folio}: matched {len(tr)} lines; left median {med:.0f} sd {L.std():.1f}; right max {max(rights)}')
    for r,l,rt,p in zip(tr,lefts,rights,got): out.append(dict(folio=folio,text=r['text'],pstart=r['pstart'],pend=r['pend'],left=l,right=rt,y=int(p),w=w,left_med=float(med),right_max=max(rights)))
json.dump(out,open('data/layout.json','w'))
print('total lines measured',len(out))
