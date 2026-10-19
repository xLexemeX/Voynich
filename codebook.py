"""One-to-one codebook test: top-K Voynich word types -> top-K plaintext word types (bijection), all other words = OOV.
Score: plaintext word-bigram model (top-K + OOV + line/sentence boundary ignored), trained on first half of the reference.
Controls: held-out half of the reference with its top-K types randomly relabelled (positive); generator text (negative).
usage: python3 codebook.py control|voynich|generator seed iters [italian|latin] [K]"""
import sys, re, csv, math, random, collections, unicodedata
import numpy as np
target, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); LANG=sys.argv[4] if len(sys.argv)>4 else 'italian'; K=int(sys.argv[5]) if len(sys.argv)>5 else 300
random.seed(seed)
if LANG=='italian':
    t=unicodedata.normalize('NFKD',open('data/ref/italian_dante.txt',encoding='utf-8').read().lower()).encode('ascii','ignore').decode(); W=re.findall(r'[a-z]+',t)
else:
    t=open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower(); W=[w for w in re.findall(r'[a-z]+',t) if not re.fullmatch(r'[ivxlcdm]+',w)]
half=len(W)//2; A,B=W[:half],W[half:]
top=[w for w,_ in collections.Counter(A).most_common(K)]; ti={w:i for i,w in enumerate(top)}; O=K   # OOV index
def ids(ws): return [ti.get(w,O) for w in ws]
C=np.full((K+1,K+1),0.05); a=ids(A)
for x,y in zip(a,a[1:]): C[x,y]+=1
LP=np.log(C/C.sum(1,keepdims=True))
N=22000
if target=='control':
    perm=list(range(K)); random.shuffle(perm); seq=[perm[i] if i<O else O for i in ids(B)][:N]; truth={perm[i]:i for i in range(K)}
else:
    if target=='voynich':
        rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
        src=[w for r in rows for w in r['text'].split('.') if w]
    else:
        ns={}; exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0],ns); src=[w for l in ns['gen'](len(ns['lines'])) for w in l]
    vt=[w for w,_ in collections.Counter(src).most_common(K)]; vi={w:i for i,w in enumerate(vt)}
    seq=[vi.get(w,O) for w in src][:N]; truth=None
pairs=collections.Counter(zip(seq,seq[1:])); P=np.array([[x,y,c] for (x,y),c in pairs.items()]); nt=P[:,2].sum()
def score(M): Mx=np.append(M,O); return (LP[Mx[P[:,0]],Mx[P[:,1]]]*P[:,2]).sum()/nt
# init: frequency rank to frequency rank
fq=collections.Counter(x for x in seq if x<O); order=[u for u,_ in fq.most_common()]+[u for u in range(K) if u not in fq]
M=np.zeros(K,dtype=np.int64)
for r,u in enumerate(order): M[u]=r
cur=score(M); best=cur; bestM=M.copy(); T0=0.02
for it in range(iters):
    u,v=random.randrange(K),random.randrange(K); M[u],M[v]=M[v],M[u]; s=score(M); d=s-cur
    if d>=0 or random.random()<math.exp(d/max(1e-5,T0*(1-it/iters))): cur=s
    else: M[u],M[v]=M[v],M[u]
    if cur>best: best=cur; bestM=M.copy()
ref=None
b=ids(B)[:N]; pb=collections.Counter(zip(b,b[1:])); ref=sum(LP[x,y]*c for (x,y),c in pb.items())/sum(pb.values())
oov=sum(x==O for x in seq)/len(seq)
res=f'[{target} {LANG} K={K} seed={seed}] score/token {best:.4f} (true held-out text {ref:.4f}); OOV share {oov:.2f}'
if truth: res+=f' | top-50 types correct {np.mean([bestM[u]==truth[u] for u in range(50)]):.2f}, all {np.mean([bestM[u]==truth[u] for u in range(K)]):.2f}'
print(res)
inv={i:w for w,i in ti.items()}
if target!='control': print('  sample:',' '.join(inv[bestM[x]] if x<O else '_' for x in seq[:40]))
