import collections, csv, re, random, math
import numpy as np
random.seed(5)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def MI(pairs):
    pc=collections.Counter(pairs); a=collections.Counter(p[0] for p in pairs); b=collections.Counter(p[1] for p in pairs)
    return H(a)+H(b)-H(pc)

print('=== 1. A/B continuum: PCA of per-page glyph-bigram profiles')
pages=collections.OrderedDict()
meta={}
for r in rows:
    pages.setdefault(r['folio'],[]).extend(w for w in r['text'].split('.') if w); meta[r['folio']]=(r['lang'],r['section'],r['quire'])
keys=[k for k,v in pages.items() if len(v)>=80]
bg=sorted(set(w[i:i+2] for w in voy for i in range(len(w)-1)))
X=[]
for k in keys:
    cc=collections.Counter(w[i:i+2] for w in pages[k] for i in range(len(w)-1)); v=np.array([cc[b] for b in bg],float); X.append(v/v.sum())
X=np.array(X); X-=X.mean(0)
U,S,Vt=np.linalg.svd(X,full_matrices=False); pc1=U[:,0]*S[0]
print('  variance explained by PC1: %.1f%%, PC2: %.1f%%'%(100*S[0]**2/(S**2).sum(),100*S[1]**2/(S**2).sum()))
for lang in ['A','B','']:
    v=[pc1[i] for i,k in enumerate(keys) if meta[k][0]==lang]
    if v: print(f'  lang {lang or "?":2s}: n={len(v):3d} PC1 mean {np.mean(v):+.4f} sd {np.std(v):.4f} min {min(v):+.4f} max {max(v):+.4f}')
hist=np.histogram(pc1,bins=14)
print('  PC1 histogram (all pages):', hist[0].tolist())
print('  top bigrams driving PC1 (+):', [bg[i] for i in np.argsort(Vt[0])[-8:][::-1]], ' (-):', [bg[i] for i in np.argsort(Vt[0])[:8]])
print('  PC1 by section:', {s: round(float(np.mean([pc1[i] for i,k in enumerate(keys) if meta[k][1]==s])),4) for s in set(m[1] for m in meta.values())})

print('\n=== 2. Agreement between neighboring words: MI(ending_i, ending_i+1) vs shuffled')
def ending(w): 
    m=re.search(r'(iin|in|dy|ey|y|l|r|n|m|s|o|d)$',w); return m.group(1) if m else w[-1]
lines=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P')]
pairs=[(ending(a),ending(b)) for l in lines for a,b in zip(l,l[1:])]
sh=[p[1] for p in pairs]; random.shuffle(sh)
print(f'  voynich: MI = {MI(pairs):.4f}  shuffled {MI(list(zip([p[0] for p in pairs],sh))):.4f}')
lat=re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower())[:38000]
lp=[(a[-2:],b[-2:]) for a,b in zip(lat,lat[1:])]; sh=[p[1] for p in lp]; random.shuffle(sh)
print(f'  latin (last 2 letters): MI = {MI(lp):.4f}  shuffled {MI(list(zip([p[0] for p in lp],sh))):.4f}')
print(f'  voynich word-initial glyph vs previous word-final glyph MI = {MI([(a[-1],b[0]) for l in lines for a,b in zip(l,l[1:])]):.4f}')

print('\n=== 3. Do prefix / core / suffix combine independently (category code) or with dependencies (morphology)?')
pat=re.compile(r'^(qo|o|q|y|s|d|ch|sh|)?(.*?)(aiin|ain|iin|in|dy|edy|eey|ey|y|ol|al|or|ar|l|r|n|m|s|)$')
trip=[]
for w in voy:
    m=pat.match(w)
    if m and m.group(2): trip.append((m.group(1) or '-',m.group(2),m.group(3) or '-'))
print(f'  decomposed {len(trip)} tokens; distinct prefixes {len(set(t[0] for t in trip))}, cores {len(set(t[1] for t in trip))}, suffixes {len(set(t[2] for t in trip))}')
print(f'  MI(prefix,suffix) = {MI([(t[0],t[2]) for t in trip]):.3f}   MI(core,suffix) = {MI([(t[1],t[2]) for t in trip]):.3f}   MI(prefix,core) = {MI([(t[0],t[1]) for t in trip]):.3f}')
# shuffled baselines
s=[t[2] for t in trip]; random.shuffle(s)
print(f'  shuffled baselines: MI(prefix,suffix) {MI([(t[0],x) for t,x in zip(trip,s)]):.3f}  MI(core,suffix) {MI([(t[1],x) for t,x in zip(trip,s)]):.3f}')
# Latin comparison: prefix = first 2 letters, suffix = last 2, core = middle
lt=[(w[:2],w[2:-2],w[-2:]) for w in lat if len(w)>=6]
s=[t[2] for t in lt]; random.shuffle(s)
print(f'  latin: MI(prefix,suffix) {MI([(t[0],t[2]) for t in lt]):.3f}  MI(core,suffix) {MI([(t[1],t[2]) for t in lt]):.3f}  shuffled core,suffix {MI([(t[1],x) for t,x in zip(lt,s)]):.3f}')
print('  top cores:', collections.Counter(t[1] for t in trip).most_common(25))

print('\n=== 4. Zipf law of abbreviation: correlation(log freq, length) over types')
for name,t in [('voynich',voy),('latin',lat)]:
    c=collections.Counter(t); f=np.log([v for v in c.values()]); L=np.array([len(w) for w in c])
    print(f'  {name}: r = {np.corrcoef(f,L)[0,1]:.3f}')

print('\n=== 5. Fraction of -edy / qo- words by quire in manuscript order (folio order)')
order=list(pages.keys())
for k in sorted(set(m[2] for m in meta.values() if m[2]), key=lambda k:(len(k),k)):
    ws=[w for f in order if meta[f][2]==k for w in pages[f]]
    print(f'  quire {k:2s} n={len(ws):5d} -edy {sum(w.endswith("edy") for w in ws)/len(ws):.3f}  qo- {sum(w.startswith("qo") for w in ws)/len(ws):.3f}  -ol/-or {sum(w.endswith(("ol","or")) for w in ws)/len(ws):.3f}  cth/ckh {sum(("cth" in w) or ("ckh" in w) for w in ws)/len(ws):.3f}  daiin {sum(w=="daiin" for w in ws)/len(ws):.3f}')
