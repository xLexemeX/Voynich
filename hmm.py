"""Unsupervised HMM over glyph units (Baum-Welch), K states. Compare Voynich vs Latin: how deterministic are the
learned states (entropy of transition rows) and do states correspond to slot positions?"""
import collections, csv, re, sys, numpy as np
np.random.seed(12)
UNITS=['cth','ckh','cph','cfh','ch','sh','iin','in','q','o','a','y','d','k','t','p','f','l','r','s','n','m','g','e','i']
def tok(w):
    out=[]; i=0
    while i<len(w):
        for u in UNITS:
            if w.startswith(u,i): out.append(u); i+=len(u); break
        else: i+=1
    return out
def run(name, words, K=5, iters=40):
    words=words[:15000]
    alpha=sorted(set(u for w in words for u in w)); ai={a:i for i,a in enumerate(alpha)}; V=len(alpha)
    seqs=[np.array([ai[u] for u in w]) for w in words if w]
    A=np.random.dirichlet(np.ones(K)*2,K); B=np.random.dirichlet(np.ones(V),K); pi=np.ones(K)/K
    for it in range(iters):
        An=np.zeros((K,K))+1e-3; Bn=np.zeros((K,V))+1e-3; pin=np.zeros(K)+1e-3; ll=0
        for s in seqs:
            T=len(s); al=np.zeros((T,K)); be=np.zeros((T,K)); c=np.zeros(T)
            al[0]=pi*B[:,s[0]]; c[0]=al[0].sum(); al[0]/=c[0]
            for t in range(1,T): al[t]=(al[t-1]@A)*B[:,s[t]]; c[t]=al[t].sum(); al[t]/=c[t]
            be[-1]=1
            for t in range(T-2,-1,-1): be[t]=(A@(B[:,s[t+1]]*be[t+1]))/c[t+1]
            g=al*be; g/=g.sum(1,keepdims=True); pin+=g[0]; ll+=np.log(c).sum()
            for t in range(T): Bn[:,s[t]]+=g[t]
            for t in range(T-1):
                xi=al[t][:,None]*A*(B[:,s[t+1]]*be[t+1])[None]; An+=xi/xi.sum()
        A=An/An.sum(1,keepdims=True); B=Bn/Bn.sum(1,keepdims=True); pi=pin/pin.sum()
    n=sum(len(s) for s in seqs)
    Ht=-(A*np.log2(A)).sum(1); He=-(B*np.log2(B)).sum(1)
    print(f'{name}: K={K} log-lik/glyph={ll/n:.3f}  mean transition entropy {Ht.mean():.2f} bits  mean emission entropy {He.mean():.2f} bits')
    for k in np.argsort(-pi):
        top=[alpha[i] for i in np.argsort(-B[k])[:6]]; nxt=[f'{np.argmax(A[k])}({A[k].max():.2f})']
        print(f'   state {k}: start {pi[k]:.2f} emits {top} -> most likely next state {nxt[0]}')
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[tok(w) for r in rows for w in r['text'].split('.') if w]
lat=[list(w) for w in re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower()) if not re.fullmatch(r'[ivxlcdm]+',w)]
run('VOYNICH',voy); run('LATIN',lat)
