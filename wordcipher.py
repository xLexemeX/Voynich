"""Word-level homophonic test (Naibbe-style): each Voynich word type (top K) stands for one plaintext letter.
Annealing over the type->letter map, scored by a Latin letter 4-gram model (no spaces).
Targets: voynich | control (Latin homophonically enciphered into Voynich-like word types) | markov (meaningless)."""
import sys, re, csv, math, random, collections, numpy as np
target=sys.argv[1]; seed=int(sys.argv[2]); iters=int(sys.argv[3]); K=int(sys.argv[4]) if len(sys.argv)>4 else 300
random.seed(seed); np.random.seed(seed)
ALPHA='abcdefghilmnopqrstuxyz'; A=len(ALPHA); aid={c:i for i,c in enumerate(ALPHA)}
def latin(path): 
    s=open(path,encoding='utf-8',errors='replace').read().lower().replace('v','u').replace('j','i').replace('k','c').replace('w','u')
    return [w for w in re.findall(r'[a-z]+',s) if not re.fullmatch(r'[ivxlcdm]+',w)]
pl=latin('data/ref/latin_pliny.txt')
half=len(pl)//2; train=''.join(pl[:half]); train=[aid[c] for c in train if c in aid]
t=np.array(train); K4=A**4
t=t.astype(np.int64); cnt=np.bincount(((t[:-3]*A+t[1:-2])*A+t[2:-1])*A+t[3:],minlength=K4).astype(float)
ctx=np.bincount((t[:-3]*A+t[1:-2])*A+t[2:-1],minlength=A**3).astype(float)
logP=np.log((cnt+0.05)/(np.repeat(ctx,A)+0.05*A)).astype(np.float32)
lf=np.bincount(t,minlength=A)/len(t)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
voy=[w for r in rows for w in r['text'].split('.') if w]
vc=collections.Counter(voy); top=[w for w,_ in vc.most_common(K)]
cover=sum(vc[w] for w in top)/len(voy)
if target=='voynich':
    seq=[w for w in voy if w in set(top)]; truth=None
elif target=='markov':
    trans=collections.defaultdict(list)
    for a,b in zip(voy,voy[1:]): trans[a].append(b)
    seq=[random.choice(voy)]
    while len(seq)<len(voy): seq.append(random.choice(trans[seq[-1]]) if trans[seq[-1]] else random.choice(voy))
    seq=[w for w in seq if w in set(top)]; truth=None
elif target=='control':
    # plaintext letters -> homophones: each letter gets a number of word types proportional to its frequency
    plain=[aid[c] for c in ''.join(pl[half:]) if c in aid][:int(len(voy)*cover)]
    types=top[:]; random.shuffle(types); alloc=np.maximum(1,np.round(lf*K)).astype(int)
    while alloc.sum()>K: alloc[np.argmax(alloc)]-=1
    while alloc.sum()<K: alloc[np.argmax(lf/alloc)]+=1
    homo={}; k=0
    for i in range(A): homo[i]=types[k:k+alloc[i]]; k+=alloc[i]
    seq=[random.choice(homo[c]) for c in plain]
    truth={w:i for i in range(A) for w in homo[i]}
tid={w:i for i,w in enumerate(top)}; S=np.array([tid[w] for w in seq],dtype=np.int64); N=len(S)
def score(M):
    x=M[S]; return float(logP[((x[:-3]*A+x[1:-2])*A+x[2:-1])*A+x[3:]].sum())
# init: by frequency rank, assign letters in proportion to letter frequency (homophonic-aware)
freq=np.bincount(S,minlength=K); order=np.argsort(-freq)
alloc=np.maximum(1,np.round(lf*K)).astype(int); pool=[i for i in range(A) for _ in range(alloc[i])]
random.shuffle(pool); M=np.zeros(K,int)
for j,ti in enumerate(order): M[ti]=pool[j%len(pool)]
cur=score(M); best=cur; bestM=M.copy(); T=30.0
for it in range(iters):
    ti=random.randrange(K); old=M[ti]
    M[ti]=random.randrange(A) if random.random()<0.7 else M[random.randrange(K)]
    s=score(M)
    if s>=cur or random.random()<math.exp((s-cur)/T): cur=s
    else: M[ti]=old
    if cur>best: best,bestM=cur,M.copy()
    T=max(0.3,T*0.99988)
x=bestM[S]; txt=''.join(ALPHA[i] for i in x)
# plaintext-likeness: fraction of text covered by Latin dictionary words (greedy longest match, words >=4)
lex=set(w for w in pl if len(w)>=4)
def coverage(s):
    i=0; cov=0
    while i<len(s):
        for L in range(12,3,-1):
            if s[i:i+L] in lex: cov+=L; i+=L; break
        else: i+=1
    return cov/len(s)
res=f'[{target} seed={seed} K={K} coverage_of_tokens={cover:.2f}] LM/char={best/N:.3f} dict-coverage={coverage(txt[:6000]):.3f}'
if truth is not None:
    acc=np.mean([bestM[tid[w]]==truth[w] for w in top]); tok=np.mean([bestM[s]==truth[top[s]] for s in S])
    res+=f' type-accuracy={acc:.3f} token-accuracy={tok:.3f}'
# reference: real Latin score and coverage
ref=np.array([aid[c] for c in ''.join(pl[half:])[:N] if c in aid],dtype=np.int64)
res+=f' | real-latin LM/char={float(logP[((ref[:-3]*A+ref[1:-2])*A+ref[2:-1])*A+ref[3:]].sum())/len(ref):.3f} real-latin dict-cov={coverage(ALPHA and "".join(ALPHA[i] for i in ref[:6000])):.3f}'
print(res); print('  sample:', txt[:300])
