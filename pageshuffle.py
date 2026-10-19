"""Model-free check of §73: shuffle the real words among the pages of their own section/language/hand group (page and line
shapes kept). Compares the real text with these shuffles on page-exclusive repetition (exact repeats confined to one page)
and on the page part of the word-form gradient (near forms)."""
import random, collections, statistics
import vertical2 as V
from scorecard import page_excl
P=V.pages()
def shuffle(P, rng):
    g=collections.defaultdict(list)
    for m,L in P: g[m]+= [w for l in L for w in l]
    for m in g: rng.shuffle(g[m])
    out=[]
    for m,L in P: out.append((m,[[g[m].pop() for _ in l] for l in L]))
    return out
def stats(Q, seed):
    pe=page_excl([L for _,L in Q], rng=random.Random(seed))
    R=[V.run(Q,random.Random(seed*10+s),n=3000) for s in range(3)]; m=[statistics.mean(r[t] for r in R) for t in range(4)]
    Rn=[V.run(Q,random.Random(seed*10+s),n=3000,near_only=True) for s in range(3)]; mn=[statistics.mean(r[t] for r in Rn) for t in range(4)]
    return pe, m[2]-m[1], mn[2]-mn[1]
r=stats(P,1); print(f'real: page-exclusive {r[0]:.3f}, page part {r[1]:+.3f}, page part with identical words ignored {r[2]:+.3f}', flush=True)
S=[stats(shuffle(P,random.Random(s)),s) for s in range(1,7)]
for t,lab in enumerate(['page-exclusive','page part','page part with identical words ignored']):
    v=[x[t] for x in S]; print(f'within-group shuffles (6): {lab} mean {statistics.mean(v):+.3f}, range {min(v):+.3f} to {max(v):+.3f}')
