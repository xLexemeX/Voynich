"""Acrostic test: does the sequence of line-initial (or line-final) glyphs down a page carry sequential structure?"""
import csv, collections, math, random, re
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
G=re.compile(r"cth|ckh|cph|cfh|ch|sh|[a-z]")
def first(t): m=G.match(t.replace("'",'')); return m.group() if m else None
def last(t): t=t.replace("'",''); return t[-1] if t and t[-1].isalpha() else None
pages=collections.OrderedDict()
for r in rows: pages.setdefault(r['folio'],[]).append(r)
def mi(pairs):
    n=len(pairs); a=collections.Counter(x for x,_ in pairs); b=collections.Counter(y for _,y in pairs); ab=collections.Counter(pairs)
    return sum(c/n*math.log2(c*n/(a[x]*b[y])) for (x,y),c in ab.items())
def seqs(f, skip_pstart):
    out=[]
    for ls in pages.values():
        s=[f(r['text']) for r in ls if not (skip_pstart and r['pstart']=='1')]
        out.append([x for x in s if x])
    return out
random.seed(0)
for name,f in [('line-initial glyph',first),('line-final glyph',last)]:
    for skip in (False,True):
        S=seqs(f,skip); pairs=[(a,b) for s in S for a,b in zip(s,s[1:])]; o=mi(pairs); null=[]
        for _ in range(500):
            T=[random.sample(s,len(s)) for s in S]; null.append(mi([(a,b) for s in T for a,b in zip(s,s[1:])]))
        m=sum(null)/len(null); sd=(sum((x-m)**2 for x in null)/len(null))**.5
        print(f'{name:20s} {"without paragraph-first lines" if skip else "all lines":30s} pairs {len(pairs):5d}  MI {o:.4f}  within-page shuffle {m:.4f}±{sd:.4f}  excess {o-m:+.4f}  p={sum(x>=o for x in null)/len(null):.3f}')
# reference: same statistic for letters of Latin text in lines of ~40 chars
w=re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower())[:30000]
txt=' '.join(w); L=[a for a in txt]; pairs=list(zip(L,L[1:]))[:6000]
print(f'reference: adjacent letters in Latin, MI {mi(pairs):.3f} over {len(pairs)} pairs')
# what carries the excess: repeats of the same glyph, or specific transitions?
S=seqs(first,True); pairs=[(a,b) for s in S for a,b in zip(s,s[1:])]
rep=sum(a==b for a,b in pairs)/len(pairs); nr=[]
for _ in range(500):
    T=[random.sample(s,len(s)) for s in S]; tp=[(a,b) for s in T for a,b in zip(s,s[1:])]; nr.append(sum(a==b for a,b in tp)/len(tp))
print(f'same initial on consecutive lines: {rep:.3f} vs shuffle {sum(nr)/len(nr):.3f}')
off=[(a,b) for a,b in pairs if a!=b]; o=mi(off); null=[]
for _ in range(500):
    T=[random.sample(s,len(s)) for s in S]; null.append(mi([(a,b) for s in T for a,b in zip(s,s[1:]) if a!=b]))
m=sum(null)/len(null); print(f'MI over non-repeat pairs only: {o:.4f} vs shuffle {m:.4f}, excess {o-m:+.4f}, p={sum(x>=o for x in null)/len(null):.3f}')
# by section: is it page-local drift (sections differ in initials) — use sections-level shuffle already within page; report per-section repeat rates
sec=collections.defaultdict(list)
for f,ls in pages.items():
    s=[first(r['text']) for r in ls if r['pstart']!='1']; s=[x for x in s if x]; sec[ls[0]['section']].append(s)
for k,v in sec.items():
    p=[(a,b) for s in v for a,b in zip(s,s[1:])]
    if len(p)>100:
        r=sum(a==b for a,b in p)/len(p); sh=[]
        for _ in range(200):
            T=[random.sample(s,len(s)) for s in v]; tp=[(a,b) for s in T for a,b in zip(s,s[1:])]; sh.append(sum(a==b for a,b in tp)/len(tp))
        print(f'  {k:8s} pairs {len(p):4d} repeat {r:.3f} vs shuffle {sum(sh)/len(sh):.3f}')
# which transitions are over/under-represented (within-page shuffle expectation)
obs=collections.Counter(pairs); exp=collections.Counter()
R=300
for _ in range(R):
    T=[random.sample(s,len(s)) for s in S]
    for s in T:
        for a,b in zip(s,s[1:]): exp[(a,b)]+=1/R
rows_=sorted(((obs[k]+.5)/(exp[k]+.5),k) for k in set(obs)|set(exp) if exp[k]>=8)
print('most under-represented line-initial transitions (obs/exp):')
for r,k in rows_[:10]: print(f'  {k[0]:>3s} -> {k[1]:<3s} obs {obs[k]:3d} exp {exp[k]:5.1f}  {r:.2f}')
print('most over-represented:')
for r,k in rows_[-10:][::-1]: print(f'  {k[0]:>3s} -> {k[1]:<3s} obs {obs[k]:3d} exp {exp[k]:5.1f}  {r:.2f}')
