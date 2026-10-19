"""Do herbal pages identified as the same plant (voynich.nu ELV/ThP, Sherwood) share vocabulary more than other page pairs?
Controls: same Currier language, and folio distance (nearby pages share vocabulary through drift)."""
import csv, json, re, math, random, collections, itertools
ids=json.load(open('data/plantids.json')); shw=json.load(open('data/plantids_sherwood.json'))
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P') and r['section']=='herbal']
pw=collections.defaultdict(collections.Counter); lang={}
for r in rows: pw[r['folio']].update(w for w in r['text'].split('.') if w); lang[r['folio']]=r['lang']
df=collections.Counter(w for c in pw.values() for w in c); N=len(pw)
def vec(f): return {w:(1+math.log(c))*math.log(N/df[w]) for w,c in pw[f].items()}
V={f:vec(f) for f in pw}
def cos(a,b):
    s=sum(v*b.get(w,0) for w,v in a.items()); return s/math.sqrt(sum(v*v for v in a.values())*sum(v*v for v in b.values()))
STOP={'thistle','other','plant','some','umbellifera','compositae','leaves','roots','water','flower','herba','harba','species','allied','nearly','related','relative','kind','burdoch','burweed','illegible','alpenveilchen','ehrenpreis','schuppenwurz','rosenmüntz','herzkraut','gemswurz','hauswurz','steinbrech','creutzwurz','wermuth','wermut','ringelblume','baldrian','pfeilkraut','some','kind','like','plant','leaves','roots','indian','water','fam','species','nearly','allied','left','right','good','king','henry','kind','with','fern','moss'}
def genera(f):
    g=set(); s=ids.get(f,'')
    if re.search(r'(ELV|ThP|THP)A?:',s):
        s=re.sub(r'\([^)]*\)','',s); s=re.sub(r'(ELVA?|ThP|THP):','',s)
        for w in re.findall(r'[A-Za-zäöü]{5,}',s):
            w=w.lower()
            if w not in STOP: g.add(w[:6])
    if f in shw: g.add(shw[f].lower()[:6])
    return g
def fnum(f): return int(re.match(r'f(\d+)',f).group(1))
F=[f for f in pw if genera(f)]
pairs=[(a,b) for a,b in itertools.combinations(F,2) if lang[a]==lang[b]]
same=[(a,b) for a,b in pairs if genera(a)&genera(b) and abs(fnum(a)-fnum(b))>1]
print(f'{len(F)} herbal pages with an identification; {len(pairs)} same-language pairs; {len(same)} share a proposed genus (non-adjacent folios):')
for a,b in same: print(f'   {a:6s} {b:6s} {sorted(genera(a)&genera(b))}  cos {cos(V[a],V[b]):.3f}')
# null: for each same pair, compare with pairs of the same language and similar folio distance (+-10)
obs=sum(cos(V[a],V[b]) for a,b in same)/len(same)
pool=collections.defaultdict(list)
for a,b in pairs:
    if not genera(a)&genera(b): pool[(lang[a],min(abs(fnum(a)-fnum(b))//10,6))].append((a,b))
random.seed(0); null=[]
for _ in range(5000):
    null.append(sum(cos(V[x],V[y]) for x,y in (random.choice(pool[(lang[a],min(abs(fnum(a)-fnum(b))//10,6))]) for a,b in same))/len(same))
print(f'mean cosine, same-genus pairs {obs:.4f}; matched different-genus pairs {sum(null)/len(null):.4f}; p = {sum(x>=obs for x in null)/len(null):.3f}')
