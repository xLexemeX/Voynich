"""Lossy-syllabary decipherment test. Italian -> onset+vowel signs (codas dropped, Linear-B style). Voynich glyphs BPE-merged to the
same inventory size. Search unit->sign (one-to-one when inventories are equal; many-to-one collapses, see NOTES 61) maximising an Italian sign-bigram model (with word boundaries).
Controls: Italian (held-out half) under a random relabelling of signs (positive); slot self-citation generator (negative).
usage: python3 syllabary.py voynich|control|generator seed iters"""
import sys, re, csv, math, random, collections, unicodedata
import numpy as np
target, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); random.seed(seed); rng=np.random.default_rng(seed)
t=unicodedata.normalize('NFKD',open('data/ref/italian_dante.txt',encoding='utf-8').read().lower()).encode('ascii','ignore').decode()
iw=re.findall(r'[a-z]+',t)
V='aeiou'
def signs(w):
    out=[]
    for m in re.finditer(r'([^aeiou]*)([aeiou])',w):
        on=m.group(1); on=on[-2:] if len(on)>2 else on        # keep at most a 2-consonant onset
        out.append(on+m.group(2))
    return out or None
half=len(iw)//2
A=[s for s in (signs(w) for w in iw[:half]) if s]; B=[s for s in (signs(w) for w in iw[half:]) if s]
cnt=collections.Counter(u for w in A for u in w); SIG=[u for u,_ in cnt.most_common(60)]; K=len(SIG); sid={u:i for i,u in enumerate(SIG)}
def enc(words): return [[sid[u] for u in w] for w in words if all(u in sid for u in w)]
EA=enc(A); EB=enc(B)
# bigram LM over signs + boundary (index K)
C2=np.full((K+1,K+1),0.1)
for w in EA:
    s=[K]+w+[K]
    for a,b in zip(s,s[1:]): C2[a,b]+=1
LP=np.log(C2/C2.sum(1,keepdims=True))
# input sequences of units
exec_ns={}
def bpe(words,n_units):
    words=[list(w) for w in words]
    while len({u for w in words for u in w})<n_units:
        pc=collections.Counter((a,b) for w in words for a,b in zip(w,w[1:]))
        (a,b),_=pc.most_common(1)[0]; m=a+b; nw=[]
        for w in words:
            o=[];i=0
            while i<len(w):
                if i+1<len(w) and w[i]==a and w[i+1]==b: o.append(m); i+=2
                else: o.append(w[i]); i+=1
            nw.append(o)
        words=nw
    return words
N=12000
if target=='control':
    perm=list(range(K)); random.shuffle(perm); words=[[perm[x] for x in w] for w in EB][:N]; truth={perm[x]:x for x in range(K)}; U=K
else:
    if target=='voynich':
        rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
        src=[w for r in rows for w in r['text'].split('.') if re.fullmatch(r'[a-z]+',w)]
    else:
        exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0], exec_ns); src=[w for l in exec_ns['gen'](len(exec_ns['lines'])) for w in l]
    bw=bpe(src[:N], K); units=sorted({u for w in bw for u in w}); ui={u:i for i,u in enumerate(units)}; words=[[ui[u] for u in w] for w in bw]; U=len(units); truth=None
# sequence of (prev,next) pairs as unit indices, boundary = -1
pairs=collections.Counter()
for w in words:
    s=[-1]+w+[-1]
    for a,b in zip(s,s[1:]): pairs[(a,b)]+=1
P=np.array([[a,b,c] for (a,b),c in pairs.items()])
ntok=P[:,2].sum()
def score(M):
    Mx=np.append(M,K)        # unit -> sign, boundary -> K
    return (LP[Mx[P[:,0]],Mx[P[:,1]]]*P[:,2]).sum()/ntok
# unigram-frequency init, then annealing on single reassignments
freqU=collections.Counter(u for w in words for u in w); orderU=[u for u,_ in freqU.most_common()]+[u for u in range(U) if u not in freqU]
M=np.zeros(U,dtype=np.int64)
for r,u in enumerate(orderU): M[u]=min(r,K-1)
# with equal inventories this is a bijection (rank-to-rank)
cur=score(M); best=cur; bestM=M.copy(); T0=0.05
ONE2ONE=(U==K)
for it in range(iters):
    if ONE2ONE:   # bijection: swap the signs of two units
        u,v=random.randrange(U),random.randrange(U); M[u],M[v]=M[v],M[u]; s=score(M); d=s-cur
        if d>=0 or random.random()<math.exp(d/max(1e-4,T0*(1-it/iters))): cur=s
        else: M[u],M[v]=M[v],M[u]
    else:
        u=random.randrange(U); old=M[u]; M[u]=random.randrange(K); s=score(M); d=s-cur
        if d>=0 or random.random()<math.exp(d/max(1e-4,T0*(1-it/iters))): cur=s
        else: M[u]=old
    if cur>best: best=cur; bestM=M.copy()
dec=' '.join(''.join(SIG[bestM[x]] for x in w) for w in words[:25])
ref=sum(LP[[K]+w,w+[K]].sum() for w in EB[:N])/sum(len(w)+1 for w in EB[:N])
res=f'[{target} seed={seed} units={U} signs={K}] score/token {best:.4f} (true Italian with true signs {ref:.4f})'
if truth: res+=f' | units correctly mapped {np.mean([bestM[u]==truth[u] for u in range(U)]):.2f}'
print(res); print('  sample:',dec[:200])
