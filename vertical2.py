"""Splits the vertical-neighbor effect (gen3_vertical.py) into its parts. For a word, the minimum edit distance to the
words at positions j-1..j+1 of: (a) the line directly above; (b) a line on the same page at least 3 lines away;
(c) a line on another page of the same section, Currier language and hand; (d) a line on any other page."""
import csv, re, random, collections, statistics
from gen3_vertical import ed
def pages():
    pg=collections.OrderedDict(); meta={}
    for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t'):
        if r['text'] and r['ltype'].startswith('P'):
            ws=[w for w in r['text'].split('.') if re.fullmatch(r'[a-z]+',w)]
            if ws: pg.setdefault(r['folio'],[]).append(ws); meta[r['folio']]=(r['section'],r['lang'],r['hand'])
    return [(meta[f],L) for f,L in pg.items()]
def window(l,j): return l[max(0,j-1):j+2] or l
def run(P, rng, n=4000, target=None, near_only=False):
    """target: optional test on the word; near_only: ignore identical words, so only near forms count."""
    grp=collections.defaultdict(list)
    for i,(m,L) in enumerate(P): grp[m].append(i)
    s=[[],[],[],[]]
    cand=[(i,li) for i,(m,L) in enumerate(P) for li in range(1,len(L)) if len(L)>=6 and len(grp[m])>=2]
    while len(s[0])<n:
        i,li=rng.choice(cand); m,L=P[i]; j=rng.randrange(len(L[li])); w=L[li][j]
        if target and not target(w): continue
        far=[k for k in range(len(L)) if abs(k-li)>=3]
        if not far: continue
        o=rng.choice([k for k in grp[m] if k!=i]); a=rng.randrange(len(P))
        if a==i: continue
        ls=[L[li-1], L[rng.choice(far)], rng.choice(P[o][1]), rng.choice(P[a][1])]
        ws=[[x for x in window(l,j) if not (near_only and x==w)] for l in ls]
        if not all(ws): continue
        for t,l in enumerate(ws): s[t].append(min(ed(w,x) for x in l))
    return [statistics.mean(x) for x in s]
if __name__=='__main__':
    P=pages(); R=[run(P,random.Random(s)) for s in range(5)]
    names=['line above','same page, 3+ lines away','other page, same section/language/hand','any other page']
    for t,nm in enumerate(names):
        v=[r[t] for r in R]; print(f'{nm:42s} {statistics.mean(v):.3f}  (sd over 5 runs {statistics.stdev(v):.3f})')
    for a,b,lab in [(1,0,'vertical (b-a)'),(2,1,'page (c-b)'),(3,2,'section/language/hand (d-c)')]:
        v=[r[a]-r[b] for r in R]; print(f'{lab:42s} {statistics.mean(v):+.3f}  (sd {statistics.stdev(v):.3f})')
def position(P, rng, n=6000):
    """Line above only: window at the same position vs a 3-word window at least 3 positions away."""
    a=[];b=[]
    cand=[(i,li,j) for i,(m,L) in enumerate(P) for li in range(1,len(L)) for j in range(len(L[li])) if len(L[li-1])>=7]
    for _ in range(n):
        i,li,j=rng.choice(cand); L=P[i][1]; w=L[li][j]; up=L[li-1]
        far=[k for k in range(1,len(up)-1) if abs(k-j)>=4]
        if not far: continue
        k=rng.choice(far); a.append(min(ed(w,x) for x in window(up,j))); b.append(min(ed(w,x) for x in up[k-1:k+2]))
    return statistics.mean(a), statistics.mean(b)
if __name__=='__main__':
    R=[position(P,random.Random(s)) for s in range(5)]
    v=[r[1]-r[0] for r in R]
    print(f'line above, same position {statistics.mean(r[0] for r in R):.3f} vs 4+ positions away {statistics.mean(r[1] for r in R):.3f}: '
          f'difference {statistics.mean(v):+.3f} (sd {statistics.stdev(v):.3f})')
def layout(path, P):
    """Lay a reference text, in order, onto the Voynich page and line shapes (and their section/language/hand labels)."""
    ws=re.findall(r'[a-zà-ÿ]+', open(path, encoding='utf-8', errors='replace').read().lower()); k=0; out=[]
    for m,L in P:
        Q=[]
        for l in L: Q.append(ws[k:k+len(l)]); k+=len(l)
        out.append((m,Q))
    assert k<=len(ws), path
    return out
if __name__=='__main__' and len(__import__('sys').argv)>1:
    for path in __import__('sys').argv[1:]:
        Q=layout(path,P); R=[run(Q,random.Random(s)) for s in range(5)]
        m=[statistics.mean(r[t] for r in R) for t in range(4)]
        print(f'{path}: ' + ' | '.join(f'{x:.3f}' for x in m) + f' | vertical {m[1]-m[0]:+.3f} page {m[2]-m[1]:+.3f} section {m[3]-m[2]:+.3f}')
