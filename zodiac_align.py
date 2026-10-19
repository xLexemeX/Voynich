"""Zodiac labels as 30 ordered entries per sign: best alignment over all 30 rotations x 2 directions between pairs of complete signs,
vs the same maximum after shuffling one sign's labels. Order: ring by ring (as listed), within ring by clock angle."""
import json, random, itertools
lab=json.load(open('data/zodiac_labels.json'))
def seq(s):
    L=[l for l in lab if l[0]==s]; L.sort(key=lambda l:(l[1], l[3] if l[3] is not None else l[2])); return [l[4].split('.')[0] for l in L]
def ed(a,b):
    D=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        P=D[:]; D[0]=i
        for j,y in enumerate(b,1): D[j]=min(P[j]+1,D[j-1]+1,P[j-1]+(x!=y))
    return D[-1]
def sim(a,b): return 1-ed(a,b)/max(len(a),len(b))
signs=['Pisces','Cancer','Leo','Virgo','Libra','Scorpio','Sagitt']
S={s:seq(s) for s in signs}
def best(a,b):
    n=len(a); out=0
    for d in (b,b[::-1]):
        for r in range(n): out=max(out,sum(sim(a[i],d[(i+r)%n]) for i in range(n))/n)
    return out
random.seed(0); rows=[]
for x,y in itertools.combinations(signs,2):
    o=best(S[x],S[y]); null=[best(S[x],random.sample(S[y],len(S[y]))) for _ in range(200)]
    rows.append((x,y,o,sum(null)/len(null),sum(v>=o for v in null)/len(null)))
for x,y,o,m,p in rows: print(f'{x:8s} {y:8s} best aligned similarity {o:.3f}  shuffled best {m:.3f}  p {p:.3f}')
ps=[r[4] for r in rows]; print(f'pairs with p<0.05: {sum(p<0.05 for p in ps)} of {len(ps)} (expected by chance {0.05*len(ps):.1f})')
# follow-up on the one low p: more shuffles, and the alignment itself
a,b=S['Virgo'],S['Scorpio']; o=best(a,b); null=[best(a,random.sample(b,len(b))) for _ in range(5000)]
print(f'\nVirgo-Scorpio: {o:.3f}; 5000 shuffles: p {sum(v>=o for v in null)/len(null):.4f}; Bonferroni threshold for 21 pairs 0.0024')
n=len(a); bestc=None
for dname,d in (('forward',b),('reversed',b[::-1])):
    for r in range(n):
        v=sum(sim(a[i],d[(i+r)%n]) for i in range(n))/n
        if bestc is None or v>bestc[0]: bestc=(v,dname,r,[(a[i],d[(i+r)%n]) for i in range(n)])
print(f'best alignment: {bestc[1]} shift {bestc[2]}'); print('  '+'  '.join(f'{x}/{y}' for x,y in bestc[3]))
print('  exact matches:', [(i,x) for i,(x,y) in enumerate(bestc[3]) if x==y])
