"""Is the first word of a herbal page (candidate plant name) concentrated on its own page more than other words?"""
import csv, collections, random
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P') and r['section']=='herbal']
pages=collections.OrderedDict()
for r in rows: pages.setdefault(r['folio'],[]).append(r['text'].split('.'))
G='ptkf'
def stem(w): return w[1:] if len(w)>3 and w[0] in G else w
def forms(w):
    s=stem(w); return {s}|{g+s for g in G}
tot=collections.Counter(); ptok={}
for f,ls in pages.items():
    c=collections.Counter(w for l in ls for w in l if w); ptok[f]=c; tot.update(c)
N=sum(tot.values())
def conc(f,w,skip):
    """observed vs expected occurrences of w's forms on page f, excluding the token itself"""
    F=forms(w) if skip else {w}; c=ptok[f]; n=sum(c.values())-1
    obs=sum(c[x] for x in F)-(1 if w in F else 0)
    other=sum(tot[x] for x in F)-sum(c[x] for x in F); exp=other/(N-n-1)*n
    return obs,exp
def agg(items,skip):
    O=E=0; hits=0
    for f,w in items: o,e=conc(f,w,skip); O+=o; E+=e; hits+=o>0
    return O,E,hits,len(items)
first=[(f,ls[0][0]) for f,ls in pages.items() if len(ls)>=4 and len(ls[0][0])>=3]
linefirst=[(f,l[0]) for f,ls in pages.items() if len(ls)>=4 for l in ls[1:] if len(l[0])>=3]
second=[(f,ls[0][1]) for f,ls in pages.items() if len(ls)>=4 and len(ls[0])>1 and len(ls[0][1])>=3]
anyw=[(f,w) for f,ls in pages.items() if len(ls)>=4 for l in ls for w in l[1:] if len(w)>=3]
random.seed(1)
for skip in (False,True):
    print('match', 'gallows-stripped stem, any gallows' if skip else 'exact word')
    for name,it in [('page-first word',first),('second word of page',second),('first word of later lines',linefirst),('mid-line words',anyw)]:
        O,E,h,n=agg(it,skip); print(f'  {name:28s} n={n:5d} recurs on own page {h/n:.2f}  obs/exp {O/max(E,1e-9):.2f} ({O} vs {E:.1f})')
    # null: page-first word placed on a random other page
    O,E,h,n=agg(first,skip); null=[]
    fs=[f for f,_ in first]
    for _ in range(1000):
        p=fs[:]; random.shuffle(p); o,e,hh,_=agg([(q,w) for q,(f,w) in zip(p,first)],skip); null.append(hh)
    print(f'  page-first words on own page: {h} recur; on shuffled pages mean {sum(null)/len(null):.1f}, p={sum(x>=h for x in null)/len(null):.3f}')
print('page-first words:', ' '.join(w for _,w in first))
