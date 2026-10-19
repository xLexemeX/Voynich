"""Best-fit rule model vs real text on the scorecard, three independent samples. (A plug-in word-pair MI check was removed: at this sparsity it is bias-dominated and gave the real text a negative excess.)"""
import random, math, collections, json, sys
from scorecard import real_pages, card
import gen3_fit as G
P=json.loads(sys.argv[1])
def mi(pages):
    pairs=[(a,b) for p in pages for l in p for a,b in zip(l,l[1:])]; n=len(pairs)
    ca=collections.Counter(a for a,_ in pairs); cb=collections.Counter(b for _,b in pairs); cab=collections.Counter(pairs)
    return sum(c/n*math.log2(c*n/(ca[a]*cb[b])) for (a,b),c in cab.items())
def excess(pages,rng):
    o=mi(pages); sh=sum(mi([[rng.sample(l,len(l)) for l in p] for p in pages]) for _ in range(5))/5; return o-sh
rng=random.Random(0)
REAL=G.REAL; M=[G.gen(s,**P) for s in (101,102,103)]
R=card(REAL)
for k in R:
    vals=[card(m)[k] for m in M]; print(f'   {k:32s} real {R[k]:8.3f}  model {min(vals):8.3f} to {max(vals):8.3f}')
