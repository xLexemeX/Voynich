"""§55 extended: page-exclusive repeated words by section and Currier language, pages cut to 84 words (pages shorter are skipped)."""
import csv, collections
exec(open('namewords.py').read().split("rows=[r for r in csv.DictReader")[0])   # namelike(), Macer chapters, gen
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
groups=collections.defaultdict(lambda: collections.OrderedDict())
for r in rows: groups[(r['section'],r['lang'])].setdefault(r['folio'],[]).extend(w for w in r['text'].split('.') if w)
def rate(P):
    per=namelike(P); return sum(x>0 for x in per)/len(P)
def excl(P):
    occ=collections.defaultdict(set)
    for i,ws in enumerate(P):
        for w in ws: occ[w].add(i)
    rep=ex=0
    for i,ws in enumerate(P):
        for w,c in collections.Counter(ws).items():
            if c>=2: rep+=1; ex+=len(occ[w])==1
    return ex/max(rep,1)
for k,pg in sorted(groups.items()):
    P=[ws[:84] for ws in pg.values() if len(ws)>=84]
    if len(P)>=8: print(f'{k[0]:7s} {k[1]}: {len(P):3d} pages; pages with a name-like word {rate(P):.2f}; repeated words found on no other page {excl(P):.3f}')
M=[ws for _,ws in chap]; Mc=[ws[:84] for ws in M if len(ws)>=84]
print(f'Macer reference: {len(Mc)} chapters; {rate(Mc):.2f}; {excl(Mc):.3f}')
print('--- every group subsampled to 15 pages (500 draws): mean share of pages with a name-like word, and of repeats that are page-exclusive')
random.seed(9)
allg=[(f'{k[0]} {k[1]}',[ws[:84] for ws in pg.values() if len(ws)>=84]) for k,pg in sorted(groups.items())]+[('Macer',Mc)]
for name,P in allg:
    if len(P)<15: continue
    r=[];e=[]
    for _ in range(500): S=random.sample(P,15); r.append(rate(S)); e.append(excl(S))
    print(f'  {name:9s} {sum(r)/len(r):.2f}  {sum(e)/len(e):.3f}')
print('--- equal page counts and lengths (84 words): herbal A vs Macer, 300 draws each')
HA=dict(allg)['herbal A']; HB=dict(allg)['herbal B']
for n in (10,20,30,45):
    out=[]
    for name,P in [('herbal A',HA),('Macer',Mc),('herbal B',HB)]:
        if len(P)<n: out.append(f'{name} -'); continue
        r=[];e=[]
        for _ in range(300): S=random.sample(P,n); r.append(rate(S)); e.append(excl(S))
        out.append(f'{name} {sum(r)/len(r):.2f}/{sum(e)/len(e):.3f}')
    print(f'  n={n:2d}: '+'   '.join(out))
ra=[rate(random.sample(HA,45)) for _ in range(300)]; rm=[rate(random.sample(Mc,45)) for _ in range(300)]
ra.sort(); rm.sort()
print(f'  n=45 spread: herbal A 5-95% {ra[15]:.2f}-{ra[284]:.2f}; Macer 5-95% {rm[15]:.2f}-{rm[284]:.2f}; herbal A full 49 pages {rate(HA):.2f}')
