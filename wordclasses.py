"""Distributional word classes: cluster frequent words by their left/right neighbour profiles.
If classes are driven by suffix/prefix (i.e. syntax == spelling), that points to a code; if classes cut across spelling, that points to grammar."""
import collections, csv, re, random, numpy as np
random.seed(9); np.random.seed(9)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
lines=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P')]
toks=[w for l in lines for w in l]; freq=collections.Counter(toks)
V=[w for w,_ in freq.most_common(300)]; vi={w:i for i,w in enumerate(V)}
C=[w for w,_ in freq.most_common(150)]; ci={w:i for i,w in enumerate(C)}
X=np.zeros((len(V),2*len(C)))
for l in lines:
    s=['<']+l+['>']
    for i in range(1,len(s)-1):
        w=s[i]
        if w in vi:
            if s[i-1] in ci: X[vi[w],ci[s[i-1]]]+=1
            if s[i+1] in ci: X[vi[w],len(C)+ci[s[i+1]]]+=1
X=X/np.maximum(X.sum(1,keepdims=True),1); X=X-X.mean(0)
# k-means
def kmeans(X,k,it=50):
    c=X[np.random.choice(len(X),k,replace=False)]
    for _ in range(it):
        d=((X[:,None,:]-c[None])**2).sum(2); a=d.argmin(1)
        c=np.array([X[a==j].mean(0) if (a==j).any() else c[j] for j in range(k)])
    return a
a=kmeans(X,8)
pat=re.compile(r'(aiin|ain|iin|in|edy|dy|eey|ey|y|ol|al|or|ar|l|r|n|m|s)$')
for j in range(8):
    ws=[V[i] for i in range(len(V)) if a[i]==j]
    suf=collections.Counter((pat.search(w).group(1) if pat.search(w) else '-') for w in ws)
    pre=collections.Counter(w[:2] if w[:2] in ('qo','ch','sh','ok','ot','da','ol','sa','so') else w[0] for w in ws)
    print(f'class {j} ({len(ws)} words): {" ".join(ws[:18])}')
    print(f'   suffixes {suf.most_common(5)}  prefixes {pre.most_common(5)}')
# how much of the class assignment is predictable from suffix alone? (mutual information)
import math
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
sufs=[(pat.search(w).group(1) if pat.search(w) else '-') for w in V]
joint=collections.Counter(zip(sufs,a.tolist()))
print(f'\nMI(class, suffix) = {H(collections.Counter(sufs))+H(collections.Counter(a.tolist()))-H(joint):.2f} bits; H(class) = {H(collections.Counter(a.tolist())):.2f}')
pres=[w[:2] if w[:2] in ('qo','ch','sh','ok','ot','da','ol','sa','so') else w[0] for w in V]
joint=collections.Counter(zip(pres,a.tolist()))
print(f'MI(class, prefix) = {H(collections.Counter(pres))+H(collections.Counter(a.tolist()))-H(joint):.2f} bits')
