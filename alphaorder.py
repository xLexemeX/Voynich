"""Do identified herbal plants follow alphabetical order of Latin names through the folios (as in Circa instans / Tractatus de herbis)?
Spearman rank correlation between folio number and alphabetical rank of the first proposed name; per identifier; also within quires."""
import json, re, csv, random
ids=json.load(open('data/plantids.json')); shw=json.load(open('data/plantids_sherwood.json'))
quire={r['folio']:r['quire'] for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t')}
herbal={r['folio'] for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['section']=='herbal'}
def first(s,who):
    m=re.search(who+r'A?:\s*(.*?)(?=(ELVA?|THP|ThP):|$)',s,re.I)
    if not m: return None
    t=re.sub(r'\([^)]*\)','',m.group(1)); w=re.findall(r'[A-Za-z]{4,}',t)
    return w[0].lower() if w else None
def fkey(f): m=re.match(r'f(\d+)([rv])(\d?)',f); return int(m.group(1))*2+(m.group(2)=='v')
def spearman(a,b):
    ra={v:i for i,v in enumerate(sorted(set(a)))}; rb={v:i for i,v in enumerate(sorted(set(b)))}
    x=[ra[v] for v in a]; y=[rb[v] for v in b]; n=len(x); mx=sum(x)/n; my=sum(y)/n
    return sum((p-mx)*(q-my) for p,q in zip(x,y))/((sum((p-mx)**2 for p in x)*sum((q-my)**2 for q in y))**.5)
random.seed(0)
for who,src in [('ELV',ids),('ThP',ids),('Sherwood',shw)]:
    D=[(fkey(f),(first(s,who) if who!='Sherwood' else s.lower()),quire.get(f)) for f,s in src.items() if f in herbal]
    D=[d for d in D if d[1]]; D.sort()
    r=spearman([d[0] for d in D],[d[1] for d in D]); null=[]
    names=[d[1] for d in D]
    for _ in range(5000): random.shuffle(names); null.append(spearman([d[0] for d in D],names))
    # within-quire: mean of per-quire correlations (quires with >=4 pages)
    qs={}
    for d in D: qs.setdefault(d[2],[]).append(d)
    wq=[spearman([d[0] for d in v],[d[1] for d in v]) for v in qs.values() if len(v)>=4]
    print(f'{who:8s} n={len(D):3d}  folio order vs alphabetical: rho {r:+.3f} (p two-sided {sum(abs(x)>=abs(r) for x in null)/len(null):.3f}); within quires: mean rho {sum(wq)/len(wq):+.3f} over {len(wq)} quires')
