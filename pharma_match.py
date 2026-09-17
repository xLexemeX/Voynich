import re, csv, collections, random, numpy as np
random.seed(22)
pairs=[('f1v','f102r1',3,2,'sure'),('f18v','f102r2',3,1,'tent'),('f19r','f102v1',2,2,'tent'),('f23r','f102r2',3,1,'sure'),('f32v','f102r2',1,2,'tent'),
       ('f37v','f102r1',3,1,'tent'),('f39r','f95r2',None,None,'tent'),('f47v','f102r2',1,1,'sure'),('f48r','f89v2',3,4,'tent'),('f48v','f89v1',1,4,'tent'),
       ('f90v2','f100r',1,3,'tent'),('f90v1','f100r',1,3,'tent'),('f96v','f99r',4,1,'tent')]
# pharma label layout: rows = blocks of consecutive label loci separated by paragraphs
lines=open('data/ZL3b-n.txt',encoding='utf-8',errors='replace').read().split('\n')
def clean(t):
    t=re.sub(r'<[^>]*>|\{[^}]*\}','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t).replace(',','.').replace('?','')
    return [w for w in t.split('.') if w and re.fullmatch(r'[a-z]+',w)]
def layout(folio):
    rows=[]; prevP=True
    for l in lines:
        m=re.match(r'^<'+re.escape(folio)+r'\.\d+,[@+=*~&](\w)\w>\s*(.*)$',l)
        if not m: continue
        if m.group(1)=='L':
            if prevP: rows.append([])
            rows[-1].append(clean(m.group(2))); prevP=False
        else: prevP=True
    return rows
for p in sorted(set(x[1] for x in pairs)): print(p, [[ ' '.join(l) for l in r] for r in layout(p)])
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
page=collections.defaultdict(list)
for r in rows: page[r['folio']]+= [w for w in r['text'].split('.') if w]
herbal=[f for f in page if any(r['folio']==f and r['section']=='herbal' for r in rows)]
def near(w,S):
    if w in S: return True
    for i in range(len(w)):
        if w[:i]+w[i+1:] in S: return True
    return False
print('\npair | pharma label | exact in herbal page | 1-glyph variant | null rate (random herbal pages, exact / variant)')
hits_e=hits_v=exp_e=exp_v=0; n=0
for h,ph,r,c,conf in pairs:
    L=layout(ph)
    if r is None or r>len(L) or c>len(L[r-1]): print(f'{h}-{ph}[{r},{c}] {conf}: no label at that position'); continue
    labs=L[r-1][c-1]
    for w in labs:
        if len(w)<3: continue
        S=set(page[h]); e=w in S; v=near(w,S)
        null_e=np.mean([w in set(page[f]) for f in herbal if f!=h]); null_v=np.mean([near(w,set(page[f])) for f in herbal if f!=h])
        print(f'{h}-{ph}[{r},{c}] {conf}: {w:12s} exact={e} variant={v}   null {null_e:.2f} / {null_v:.2f}')
        n+=1; hits_e+=e; hits_v+=v; exp_e+=null_e; exp_v+=null_v
print(f'\nlabels tested {n}: exact hits {hits_e} (expected {exp_e:.2f}); variant hits {hits_v} (expected {exp_v:.2f})')
