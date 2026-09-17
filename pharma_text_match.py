import re, csv, collections, random, numpy as np
random.seed(23)
pairs=[('f1v','f102r1',3),('f18v','f102r2',3),('f19r','f102v1',2),('f23r','f102r2',3),('f32v','f102r2',1),('f37v','f102r1',3),
       ('f47v','f102r2',1),('f48r','f89v2',3),('f48v','f89v1',1),('f90v2','f100r',1),('f90v1','f100r',1),('f96v','f99r',4)]
lines=open('data/ZL3b-n.txt',encoding='utf-8',errors='replace').read().split('\n')
def clean(t):
    t=re.sub(r'<[^>]*>|\{[^}]*\}','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t).replace(',','.').replace('?','')
    return [w for w in t.split('.') if w and re.fullmatch(r'[a-z]+',w)]
def rowparas(folio):
    rows=[]; prevP=True; cur=None
    for l in lines:
        m=re.match(r'^<'+re.escape(folio)+r'\.\d+,[@+=*~&](\w)\w>\s*(.*)$',l)
        if not m: continue
        if m.group(1)=='L':
            if prevP: rows.append([]); 
            prevP=False
        else:
            if not rows: rows.append([])
            rows[-1]+=clean(m.group(2)); prevP=True
    return rows
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
page=collections.defaultdict(list)
for r in rows: page[r['folio']]+= [w for w in r['text'].split('.') if w]
herbal=sorted({r['folio'] for r in rows if r['section']=='herbal'})
pharma_pages=sorted({r['folio'] for r in rows if r['section']=='pharma'})
allrows=[(p,i,rp) for p in pharma_pages for i,rp in enumerate(rowparas(p),1) if len(rp)>=10]
glob=collections.Counter(w for r in rows for w in r['text'].split('.') if w)
N=sum(glob.values())
def sim(a,b):   # IDF-weighted overlap of word sets (rare shared words count more)
    A=set(a); B=set(b); sh=A&B
    return sum(np.log(N/glob[w]) for w in sh)/np.sqrt(len(A)*len(B))
obs=[]; nulls=[]
for h,ph,r in pairs:
    rp=rowparas(ph)
    if r>len(rp) or len(rp[r-1])<5: print('skip',h,ph,r); continue
    s=sim(page[h],rp[r-1])
    others=[sim(page[h],x) for p,i,x in allrows if not (p==ph and i==r)]
    rank=1+sum(o>=s for o in others)
    obs.append(s); nulls.append(np.mean(others))
    print(f'{h:6s} vs {ph}[row {r}]: sim {s:.3f}; mean vs all other pharma paragraphs {np.mean(others):.3f}; rank {rank} of {len(others)+1}; shared {sorted(set(page[h])&set(rp[r-1]))[:12]}')
print(f'\nmean matched {np.mean(obs):.3f} vs mean unmatched {np.mean(nulls):.3f}')
# permutation: shuffle which pharma paragraph each herbal page is paired with
valid=[(h,ph,r) for h,ph,r in pairs if r<=len(rowparas(ph)) and len(rowparas(ph)[r-1])>=5]
stat=np.mean(obs); null=[]
for _ in range(5000):
    null.append(np.mean([sim(page[h],random.choice(allrows)[2]) for h,ph,r in valid]))
print(f'permutation p (random pharma paragraph per herbal page) = {np.mean([x>=stat for x in null]):.4f}')
