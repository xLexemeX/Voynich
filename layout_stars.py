import csv, numpy as np, json, os, re
from PIL import Image, ImageDraw
from scipy.ndimage import uniform_filter1d, label
from scipy.signal import find_peaks
files={re.sub(r'^\d+_','',fn).replace('.jpg',''):fn for fn in os.listdir('beinecke')}
pages=['103r','103v','104r','104v','105r','105v','106r','106v','107r','107v','108r','108v','111r','111v','112r','112v','113r','113v','114r','114v','115r','115v','116r']
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['ltype'].startswith('P')]
out=[]; report=[]
for pg in pages:
    fn=files[pg]; folio='f'+pg
    tr=[r for r in rows if r['folio']==folio]
    im=Image.open('beinecke/'+fn).convert('L'); a=np.asarray(im); h,w=a.shape
    dark=(a<60).mean(0); cols=np.where(dark<0.5)[0]; px0,px1=cols[0],cols[-1]
    rowdark=(a<60).mean(1); rws=np.where(rowdark<0.5)[0]; py0,py1=rws[0],rws[-1]
    ink=a<150; m=int(0.03*h); ink[:py0+m,:]=False; ink[py1-m:,:]=False; ink[:,:px0+40]=False; ink[:,px1-40:]=False
    W=px1-px0
    colf=uniform_filter1d(ink[int(0.15*h):int(0.85*h),:].mean(0),25)
    # text block left edge: first x from which ink is sustained for 200 px
    tl=[x for x in range(px0+40, px1-300) if colf[x:x+200].min()>0.03]
    x0=tl[0]-10 if tl else int(px0+0.11*W)
    mid=(px0+px1)//2; xr=[x for x in range(mid,px1) if colf[x]<0.008]; x1=xr[0] if xr else int(px1-0.02*W)
    # stars: blobs in the margin zone left of the text block start; text block start = first column with sustained ink
    tz=ink[:, px0+40:x0-15]
    sproj=uniform_filter1d(tz.sum(1).astype(float),9)
    speaks,_=find_peaks(sproj,distance=60,prominence=np.percentile(sproj,90)*0.3)
    speaks=[p for p in speaks if sproj[p]>8]
    # text rows
    proj=ink[:,x0:x1].sum(1).astype(float); sm=uniform_filter1d(proj,15)
    peaks,_=find_peaks(sm,distance=38,prominence=np.percentile(sm,60)*0.15); peaks=[p for p in peaks if sm[p]>np.percentile(sm,40)]
    # paragraphs in transcription
    paras=[]; cur=[]
    for r in tr:
        if r['pstart']=='1' and cur: paras.append(cur); cur=[]
        cur.append(r)
    if cur: paras.append(cur)
    ok=0
    if len(speaks)!=len(paras):
        report.append(f'{folio}: stars {len(speaks)} vs paragraphs {len(paras)} -> skip (x0={x0} px0={px0} star zone width {x0-15-px0-40})'); continue
    bounds=list(speaks)+[h]
    for k,pr in enumerate(paras):
        ya=bounds[k]-25; yb=bounds[k+1]-25
        ps=[p for p in peaks if ya<=p<yb]
        if len(ps)!=len(pr): continue
        ok+=1
        for p,r in zip(ps,pr):
            band=ink[max(0,p-9):p+9,:]; cc=band.sum(0).astype(float); dens=uniform_filter1d(cc,40)*40
            xs=np.where(dens[x0:x1]>=30)[0]
            if not len(xs): continue
            out.append(dict(folio=folio,text=r['text'],pstart=r['pstart'],pend=r['pend'],left=int(x0+xs[0]),right=int(x0+xs[-1]),y=int(p),x0=int(x0),x1=int(x1),W=int(W)))
    report.append(f'{folio}: stars {len(speaks)} paragraphs {len(paras)}; aligned {ok}/{len(paras)} paragraphs; x0={x0} px0={px0}')
    if folio=='f104v':
        ov=Image.open('beinecke/'+fn).convert('RGB'); dr=ImageDraw.Draw(ov)
        for d in out:
            if d['folio']=='f104v': dr.line([(d['left'],d['y']),(d['right'],d['y'])],fill=(255,0,0),width=5)
        for p in speaks: dr.ellipse([px0+40,p-10,x0,p+10],outline=(0,0,255),width=4)
        ov.thumbnail((1400,1400)); ov.save('crops/overlay_f104v.png')
print('\n'.join(report)); print('lines measured',len(out))
json.dump(out,open('data/layout.json','w'))
import collections
byp=collections.defaultdict(list)
for d in out: byp[d['folio']].append(d)
for f,ls in byp.items():
    c=[l['right']-l['left'] for l in ls if l['pend']=='0']; p=[l['right']-l['left'] for l in ls if l['pend']=='1']
    if c and p: print(f'  {f}: cont {np.mean(c):6.0f} (sd {np.std(c):4.0f}) n={len(c)}  final {np.mean(p):6.0f} (sd {np.std(p):4.0f}) n={len(p)}')
