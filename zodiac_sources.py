import csv, collections, random, numpy as np
random.seed(17)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
early_f=['f70v2','f70v1','f71r','f71v','f72r1','f72r2','f72r3']; late_f=['f72v3','f72v2','f72v1','f73r','f73v']
E=[w for r in rows if r['folio'] in early_f and r['ltype'].startswith('L') for w in r['text'].split('.') if w]
L=[w for r in rows if r['folio'] in late_f and r['ltype'].startswith('L') for w in r['text'].split('.') if w]
zod=set(early_f+late_f)
def corpus(pred): return collections.Counter(w for r in rows if r['folio'] not in zod and pred(r) for w in r['text'].split('.') if w)
targets={
 'herbal text (A)':corpus(lambda r:r['section']=='herbal' and r['lang']=='A' and r['ltype'].startswith('P')),
 'herbal text (B)':corpus(lambda r:r['section']=='herbal' and r['lang']=='B' and r['ltype'].startswith('P')),
 'bio text':corpus(lambda r:r['section']=='bio' and r['ltype'].startswith('P')),
 'stars text':corpus(lambda r:r['section']=='stars' and r['ltype'].startswith('P')),
 'pharma text':corpus(lambda r:r['section']=='pharma' and r['ltype'].startswith('P')),
 'astro+cosmo text':corpus(lambda r:r['section'] in('astro','cosmo') and not r['ltype'].startswith('L')),
 'astro+cosmo labels':corpus(lambda r:r['section'] in('astro','cosmo') and r['ltype'].startswith('L')),
 'bio labels':corpus(lambda r:r['section']=='bio' and r['ltype'].startswith('L')),
 'pharma labels':corpus(lambda r:r['section']=='pharma' and r['ltype'].startswith('L')),
}
def hit(ws,C): return np.mean([w in C for w in ws])
print(f'early labels n={len(E)}, late labels n={len(L)}')
print(f'{"target":22s} {"early hit":>9s} {"late hit":>9s} {"diff":>6s}  perm p')
allz=E+L
for name,C in targets.items():
    he,hl=hit(E,C),hit(L,C); d=he-hl; null=[]
    for _ in range(4000):
        random.shuffle(allz); null.append(hit(allz[:len(E)],C)-hit(allz[len(E):],C))
    p=np.mean([abs(x)>=abs(d) for x in null])
    print(f'{name:22s} {he:9.3f} {hl:9.3f} {d:+6.3f}  {p:.4f}')
# near-matches: edit distance 1 to any word in the target (type level)
def lev1(w,S):
    if w in S: return True
    for i in range(len(w)):
        if w[:i]+w[i+1:] in S: return True
    return False
print('\nwith edit-distance-1 matching (deletion only):')
for name,C in targets.items():
    S=set(C); print(f'  {name:22s} early {np.mean([lev1(w,S) for w in E]):.3f} late {np.mean([lev1(w,S) for w in L]):.3f}')
