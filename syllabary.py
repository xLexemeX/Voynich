"""Lossy-syllabary decipherment test. Italian -> onset+vowel signs (codas dropped, Linear-B style). Voynich glyphs BPE-merged to the
same inventory size. Search unit->sign (one-to-one when inventories are equal; many-to-one collapses, see NOTES 61) maximising an Italian sign-bigram model (with word boundaries).
Controls: Italian (held-out half) under a random relabelling of signs (positive); slot self-citation generator (negative).
usage: python3 syllabary.py voynich|control|generator seed iters"""
import sys, re, csv, math, random, collections, unicodedata
import numpy as np
target, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); random.seed(seed); rng=np.random.default_rng(seed)
LANG=sys.argv[4] if len(sys.argv)>4 else 'italian'; KS=int(sys.argv[5]) if len(sys.argv)>5 else 60; NU=int(sys.argv[6]) if len(sys.argv)>6 else KS
if LANG=='italian':
    t=unicodedata.normalize('NFKD',open('data/ref/italian_dante.txt',encoding='utf-8').read().lower()).encode('ascii','ignore').decode(); iw=re.findall(r'[a-z]+',t)
else:
    t=open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower().replace('j','i').replace('v','u'); iw=[w for w in re.findall(r'[a-z]+',t) if not re.fullmatch(r'[ivxlcdm]+',w)]
V='aeiou'
def signs(w):
    out=[]
    for m in re.finditer(r'([^aeiou]*)([aeiou])',w):
        on=m.group(1); on=on[-2:] if len(on)>2 else on        # keep at most a 2-consonant onset
        out.append(on+m.group(2))
    return out or None
half=len(iw)//2
A=[s for s in (signs(w) for w in iw[:half]) if s]; B=[s for s in (signs(w) for w in iw[half:]) if s]
cnt=collections.Counter(u for w in A for u in w); SIG=[u for u,_ in cnt.most_common(KS)]; K=len(SIG); sid={u:i for i,u in enumerate(SIG)}
def enc(words): return [[sid[u] for u in w] for w in words if all(u in sid for u in w)]
EA=enc(A); EB=enc(B)
# bigram LM over signs + boundary (index K)
C2=np.full((K+1,K+1),0.1)
for w in EA:
    s=[K]+w+[K]
    for a,b in zip(s,s[1:]): C2[a,b]+=1
LP=np.log(C2/C2.sum(1,keepdims=True))
import os
TRI=os.environ.get('TRI')=='1'
if TRI:   # sign trigram over the running sequence: w1 signs, boundary, w2 signs, boundary ...
    C3=np.full((K+1,K+1,K+1),0.05); flat=[K]
    for w in EA: flat+=w+[K]
    flat=np.array(flat)
    np.add.at(C3,(flat[:-2],flat[1:-1],flat[2:]),1)
    LP3=np.log(C3/C3.sum(2,keepdims=True))
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
    # homophonic: each sign gets 1+ unit labels in proportion to frequency, NU labels in all
    fs=collections.Counter(x for w in EB for x in w); alloc={x:1 for x in range(K)}
    while sum(alloc.values())<NU: x=max(range(K),key=lambda x:fs[x]/alloc[x]); alloc[x]+=1
    labs=list(range(NU)); random.shuffle(labs); homo={}; k=0
    for x in range(K): homo[x]=labs[k:k+alloc[x]]; k+=alloc[x]
    truth={u:x for x in range(K) for u in homo[x]}
    words=[[random.choice(homo[x]) for x in w] for w in EB][:N]; U=NU
else:
    if target=='voynich':
        rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
        src=[w for r in rows for w in r['text'].split('.') if re.fullmatch(r'[a-z]+',w)]
    else:
        exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0], exec_ns); exec_ns['random'].seed(1000+seed); src=[w for l in exec_ns['gen'](len(exec_ns['lines'])) for w in l]
    bw=bpe(src[:N], NU); units=sorted({u for w in bw for u in w}); ui={u:i for i,u in enumerate(units)}; words=[[ui[u] for u in w] for w in bw]; U=len(units); truth=None
# fit on the first half of the words, keep the second half for the held-out order test
TEST=words[len(words)//2:]; words=words[:len(words)//2]
# sequence of (prev,next) pairs as unit indices, boundary = -1
pairs=collections.Counter()
for w in words:
    s=[-1]+w+[-1]
    for a,b in zip(s,s[1:]): pairs[(a,b)]+=1
P=np.array([[a,b,c] for (a,b),c in pairs.items()])
ntok=P[:,2].sum()
if TRI:
    fl=[-1]
    for w in words: fl+=w+[-1]
    tr=collections.Counter(zip(fl,fl[1:],fl[2:])); P3=np.array([[a,b,c,n] for (a,b,c),n in tr.items()]); n3=P3[:,3].sum()
def score(M):
    Mx=np.append(M,K)        # unit -> sign, boundary -> K
    if TRI: return (LP3[Mx[P3[:,0]],Mx[P3[:,1]],Mx[P3[:,2]]]*P3[:,3]).sum()/n3
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
def seqscore(M,W):
    Mx=np.append(M,K); tot=n=0
    for w in W:
        s_=[-1]+w+[-1]; a=Mx[np.array(s_[:-1])]; b=Mx[np.array(s_[1:])]; tot+=LP[a,b].sum(); n+=len(s_)-1
    return tot/n
def seqscore3(M,W):
    Mx=np.append(M,K); fl=[-1]
    for w in W: fl+=w+[-1]
    f=Mx[np.array(fl)]; return LP3[f[:-2],f[1:-1],f[2:]].mean()
def gain(M):
    if TRI:   # whole-word shuffle: changes only cross-word trigrams
        o=seqscore3(M,TEST); sh=[seqscore3(M,random.sample(TEST,len(TEST))) for _ in range(5)]
    else:
        o=seqscore(M,TEST); sh=[]
        for _ in range(5): sh.append(seqscore(M,[random.sample(w,len(w)) for w in TEST]))
    return o-sum(sh)/len(sh)
G=gain(bestM)
dec=' '.join(''.join(SIG[bestM[x]] for x in w) for w in words[:25])
ref=sum(LP[[K]+w,w+[K]].sum() for w in EB[:N])/sum(len(w)+1 for w in EB[:N])
res=f'[{target} {LANG} seed={seed} units={U} signs={K}] train score/token {best:.4f}; held-out {'cross-word' if TRI else 'within-word'} order gain {G:+.4f} (true text with true signs {ref:.4f})'
if truth: TM=np.array([truth[u] for u in range(U)]); res+=f' | units correctly mapped {np.mean([bestM[u]==truth[u] for u in range(U)]):.2f}; true key: train {score(TM):.4f}, held-out gain {gain(TM):+.4f}'
print(res); print('  sample:',dec[:200])
