"""Kober/Ventris-style grid test. Cluster syllable signs by left-context and by right-context distributions; on Maori (true CV known)
check whether either clustering recovers the consonant or the vowel classes (positive control)."""
import re, glob, unicodedata, collections, math, random
import numpy as np
mt=' '.join(open(f,encoding='utf-8').read() for f in sorted(glob.glob('data/ext_poly/mri/mri_*_read.txt')) if '_000_' not in f).lower()
mt=unicodedata.normalize('NFKD',mt).encode('ascii','ignore').decode()
mw=re.findall(r'[a-z]+',mt)[:35000]
S=[re.findall(r'(?:ng|wh|[hkmnprtw])?[aeiou]',w) for w in mw]
def ctx(words, side):
    units=sorted({u for w in words for u in w}); idx={u:i for i,u in enumerate(units)}; ctxs=sorted(units)+['#']; ci={c:i for i,c in enumerate(ctxs)}
    M=np.zeros((len(units),len(ctxs)))
    for w in words:
        s=['#']+w+['#']
        for i in range(1,len(s)-1): M[idx[s[i]],ci[s[i-1] if side=='L' else s[i+1]]]+=1
    return units,M
def kmeans(X,k,seed=0,it=100):
    rng=np.random.default_rng(seed); C=X[rng.choice(len(X),k,replace=False)]
    for _ in range(it):
        d=((X[:,None,:]-C[None])**2).sum(-1); a=d.argmin(1)
        C=np.array([X[a==j].mean(0) if (a==j).any() else C[j] for j in range(k)])
    return a
def nmi(a,b):
    n=len(a); ca=collections.Counter(a); cb=collections.Counter(b); cab=collections.Counter(zip(a,b))
    I=sum(c/n*math.log(c*n/(ca[x]*cb[y])) for (x,y),c in cab.items()); Ha=-sum(c/n*math.log(c/n) for c in ca.values()); Hb=-sum(c/n*math.log(c/n) for c in cb.values())
    return I/math.sqrt(Ha*Hb) if Ha>0 and Hb>0 else 0
def features(M):
    P=(M+0.5)/(M+0.5).sum(1,keepdims=True); return np.sqrt(P)    # Hellinger embedding
def best_nmi(units,M,truth,k):
    keep=[i for i,u in enumerate(units) if M[i].sum()>=30]; X=features(M[keep]); t=[truth(units[i]) for i in keep]
    vals=[nmi(list(kmeans(X,k,s)),t) for s in range(10)]; return max(vals), np.mean(vals), len(keep)
if __name__=='__main__':
    cons=lambda u:re.match(r'(ng|wh|[hkmnprtw])?',u).group(0) or '0'; vow=lambda u:u[-1]
    rnd=lambda u:random.Random(sum(map(ord,u))*7919).randrange(5); rnd10=lambda u:random.Random(sum(map(ord,u))*104729).randrange(10)
    for side in 'LR':
        units,M=ctx(S,side)
        for name,tr,k in [('vowel',vow,5),('consonant',cons,10),('random 5-way labels',rnd,5),('random 10-way labels',rnd10,10)]:
            b,m,n=best_nmi(units,M,tr,k); print(f'Maori, {side}-context clusters vs {name:20s}: NMI best {b:.2f} mean {m:.2f} ({n} signs)')
