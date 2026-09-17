"""Word-level homophonic decipherment with incremental scoring. Each of the top-K Voynich word types = one plaintext letter."""
import sys, re, csv, math, random, collections, numpy as np
target=sys.argv[1]; seed=int(sys.argv[2]); iters=int(sys.argv[3]); K=int(sys.argv[4]) if len(sys.argv)>4 else 300
random.seed(seed); np.random.seed(seed)
ALPHA='abcdefghilmnopqrstuxyz'; A=len(ALPHA); aid={c:i for i,c in enumerate(ALPHA)}
def latin(path):
    s=open(path,encoding='utf-8',errors='replace').read().lower().replace('v','u').replace('j','i').replace('k','c').replace('w','u')
    return [w for w in re.findall(r'[a-z]+',s) if not re.fullmatch(r'[ivxlcdm]+',w)]
pl=latin('data/ref/latin_pliny.txt'); half=len(pl)//2
t=np.array([aid[c] for c in ''.join(pl[:half]) if c in aid],dtype=np.int64)
cnt=np.bincount(((t[:-3]*A+t[1:-2])*A+t[2:-1])*A+t[3:],minlength=A**4).astype(float)
# interpolated 4-gram / 3-gram / 2-gram / 1-gram for sharper scores on unseen contexts
c3=np.bincount((t[:-2]*A+t[1:-1])*A+t[2:],minlength=A**3).astype(float); c2=np.bincount(t[:-1]*A+t[1:],minlength=A**2).astype(float); c1=np.bincount(t,minlength=A).astype(float)
p1=(c1+1)/(c1.sum()+A); p2=(c2+0.1)/(np.repeat(c1,A)+0.1*A); p3=(c3+0.1)/(np.repeat(c2,A)+0.1*A); p4=(cnt+0.1)/(np.repeat(c3,A)+0.1*A)
lp=np.log(0.6*p4+0.25*np.tile(p3,A)+0.1*np.tile(p2,A**2)+0.05*np.tile(p1,A**3)).astype(np.float64)
lf=c1/c1.sum()
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
voy=[w for r in rows for w in r['text'].split('.') if w]
vc=collections.Counter(voy); top=[w for w,_ in vc.most_common(K)]; topset=set(top)
cover=sum(vc[w] for w in top)/len(voy)
truth=None
if target=='voynich': seq=[w for w in voy if w in topset]
elif target=='markov':
    trans=collections.defaultdict(list)
    for a,b in zip(voy,voy[1:]): trans[a].append(b)
    seq=[random.choice(voy)]
    while len(seq)<len(voy): seq.append(random.choice(trans[seq[-1]]) if trans[seq[-1]] else random.choice(voy))
    seq=[w for w in seq if w in topset]
elif target=='control':
    plain=[aid[c] for c in ''.join(pl[half:]) if c in aid][:int(len(voy)*cover)]
    types=top[:]; random.shuffle(types); alloc=np.maximum(1,np.round(lf*K)).astype(int)
    while alloc.sum()>K: alloc[np.argmax(alloc)]-=1
    while alloc.sum()<K: alloc[np.argmax(lf/alloc)]+=1
    homo={}; k=0
    for i in range(A): homo[i]=types[k:k+alloc[i]]; k+=alloc[i]
    seq=[random.choice(homo[c]) for c in plain]; truth={w:i for i in range(A) for w in homo[i]}
tid={w:i for i,w in enumerate(top)}; S=np.array([tid[w] for w in seq],dtype=np.int64); N=len(S)
pos=collections.defaultdict(list)
for i,s in enumerate(S): pos[s].append(i)
pos={k:np.array(v) for k,v in pos.items()}
def full(M):
    x=M[S]; return lp[((x[:-3]*A+x[1:-2])*A+x[2:-1])*A+x[3:]].sum()
def local(M,ti):
    # sum of 4-gram scores for all 4-grams touching positions of type ti (start indices p-3..p), deduplicated
    P=pos[ti]; starts=np.unique(np.clip((P[:,None]-np.arange(4)[None,:]).ravel(),0,N-4))
    x=M[S]
    return lp[((x[starts]*A+x[starts+1])*A+x[starts+2])*A+x[starts+3]].sum(), starts
M=np.zeros(K,dtype=np.int64)
freq=np.bincount(S,minlength=K); order=np.argsort(-freq)
alloc=np.maximum(1,np.round(lf*K)).astype(int); pool=[i for i in range(A) for _ in range(alloc[i])]; random.shuffle(pool)
for j,ti in enumerate(order): M[ti]=pool[j%len(pool)]
if truth is not None:
    TM=np.array([truth[w] for w in top]); print(f'  true-mapping LM/char {full(TM)/N:.3f}; init LM/char {full(M)/N:.3f}')
LAM=float(sys.argv[5]) if len(sys.argv)>5 else 1.0
lc=np.bincount(M[S],minlength=A).astype(float)
def kl(lc): q=lc/lc.sum(); m=q>0; return float((q[m]*np.log(q[m]/lf[m])).sum())
cur=full(M)-LAM*N*kl(lc); best=cur; bestM=M.copy(); T0=8.0; T=T0
active=[k for k in range(K) if k in pos]
for it in range(iters):
    ti=random.choice(active); old=M[ti]; new=random.randrange(A)
    if new==old: continue
    a,_=local(M,ti); k0=kl(lc); n=len(pos[ti]); lc[old]-=n; lc[new]+=n; M[ti]=new; b,_=local(M,ti); d=(b-a)-LAM*N*(kl(lc)-k0)
    if d>=0 or random.random()<math.exp(d/T): cur+=d
    else: M[ti]=old; lc[new]-=n; lc[old]+=n
    if cur>best: best=cur; bestM=M.copy()
    T=max(0.05,T0*(1-it/iters))
x=bestM[S]; txt=''.join(ALPHA[i] for i in x)
lex=set(w for w in pl if len(w)>=4)
def coverage(s):
    i=0; cov=0
    while i<len(s):
        for L in range(12,3,-1):
            if s[i:i+L] in lex: cov+=L; i+=L; break
        else: i+=1
    return cov/len(s)
ref=np.array([aid[c] for c in ''.join(pl[half:]) if c in aid][:N],dtype=np.int64)
res=f'[{target} seed={seed} K={K} tokcov={cover:.2f} N={N}] LM/char={full(bestM)/N:.3f} dict-cov={coverage(txt[:8000]):.3f} | real latin LM/char={lp[((ref[:-3]*A+ref[1:-2])*A+ref[2:-1])*A+ref[3:]].sum()/len(ref):.3f} dict-cov={coverage("".join(ALPHA[i] for i in ref[:8000])):.3f}'
if truth is not None:
    res+=f' | type-acc={np.mean([bestM[tid[w]]==truth[w] for w in top]):.3f} token-acc={np.mean([bestM[s]==truth[top[s]] for s in S]):.3f}'
print(res); print('  sample:', txt[:260])
