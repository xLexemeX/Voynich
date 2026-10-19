"""Word types -> plaintext chunk (a letter OR a letter pair), Naibbe-style. Incremental vectorised 4-gram scoring."""
import sys, re, csv, math, random, collections, os, time, numpy as np
target, seed, iters = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
LANG = sys.argv[4] if len(sys.argv)>4 else 'latin'; SUBSET=os.environ.get('SUBSET','B'); K=300; NB=60; PBI=0.4
random.seed(seed); np.random.seed(seed)
ALPHA='abcdefghilmnopqrstuxyz'; A=len(ALPHA); aid={c:i for i,c in enumerate(ALPHA)}
def words(path, italian=False):
    s=open(path,encoding='utf-8',errors='replace').read()
    if italian:
        import unicodedata; s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    s=s.lower().replace('v','u').replace('j','i').replace('k','c').replace('w','u')
    return [w for w in re.findall(r'[a-z]+',s) if not re.fullmatch(r'[ivxlcdm]+',w)]
pl=words('data/ref/latin_pliny.txt') if LANG=='latin' else words('data/ref/italian_dante.txt',True)
half=len(pl)//2
t=np.array([aid[c] for c in ''.join(pl[:half]) if c in aid],dtype=np.int64)
c1=np.bincount(t,minlength=A).astype(float); c2=np.bincount(t[:-1]*A+t[1:],minlength=A*A).astype(float)
c3=np.bincount((t[:-2]*A+t[1:-1])*A+t[2:],minlength=A**3).astype(float); c4=np.bincount(((t[:-3]*A+t[1:-2])*A+t[2:-1])*A+t[3:],minlength=A**4).astype(float)
p1=(c1+1)/(c1.sum()+A); p2=(c2+.1)/(np.repeat(c1,A)+.1*A); p3=(c3+.1)/(np.repeat(c2,A)+.1*A); p4=(c4+.1)/(np.repeat(c3,A)+.1*A)
lp=np.log(.6*p4+.25*np.tile(p3,A)+.1*np.tile(p2,A*A)+.05*np.tile(p1,A**3))
lf=c1/c1.sum()
# chunk inventory: letters + top NB bigrams
bg=np.argsort(-c2)[:NB]; CH=[(i,-1) for i in range(A)]+[(b//A,b%A) for b in bg]; C=len(CH); CHA=np.array(CH,dtype=np.int64)
chid={ch:i for i,ch in enumerate(CH)}
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P') and (not SUBSET or r['lang']==SUBSET)]
voy=[w for r in rows for w in r['text'].split('.') if w]
vc=collections.Counter(voy); top=[w for w,_ in vc.most_common(K)]; ts=set(top); cover=sum(vc[w] for w in top)/len(voy); DROP=1-cover
truth=None
if target=='voynich':
    seq=[w for w in voy if w in ts]
elif target=='shuffled':
    seq=[w for w in voy if w in ts]; random.shuffle(seq)
elif target=='markov':
    trans=collections.defaultdict(list)
    for a,b in zip(voy,voy[1:]): trans[a].append(b)
    seq=[random.choice(voy)]
    while len(seq)<len(voy): seq.append(random.choice(trans[seq[-1]]) if trans[seq[-1]] else random.choice(voy))
    seq=[w for w in seq if w in ts]
elif target=='control':
    # plaintext -> chunks
    P=[aid[c] for c in ''.join(pl[half:]) if c in aid]; chunks=[]; i=0; bset=set(bg.tolist())
    while i<len(P) and len(chunks)<int(len(voy)*cover/(1-DROP)):
        if i+1<len(P) and P[i]*A+P[i+1] in bset and random.random()<PBI: chunks.append(chid[(P[i],P[i+1])]); i+=2
        else: chunks.append(chid[(P[i],-1)]); i+=1
    cf=np.bincount(chunks,minlength=C).astype(float); alloc=np.maximum(1,np.floor(cf/cf.sum()*(K-C))).astype(int)
    while alloc.sum()<K: alloc[np.argmax(cf/alloc)]+=1
    while alloc.sum()>K: alloc[np.argmax(alloc)]-=1
    types=top[:]; random.shuffle(types); homo={}; k=0
    for c in range(C): homo[c]=types[k:k+alloc[c]]; k+=alloc[c]
    seq=[random.choice(homo[c]) for c in chunks]; seq=[w for w in seq if random.random()>=DROP]
    truth={w:c for c in range(C) for w in homo[c]}
tid={w:i for i,w in enumerate(top)}; S=np.array([tid[w] for w in seq],dtype=np.int64)
HOLD=os.environ.get('HOLD')=='1'
if HOLD: SH=S[len(S)//2:]; S=S[:len(S)//2]
N=len(S)
pos=collections.defaultdict(list)
for i,s in enumerate(S): pos[s].append(i)
pos={k:np.array(v) for k,v in pos.items()}; active=list(pos)
def full(M):
    E=CHA[M[S]].ravel(); E=E[E>=0]; return lp[((E[:-3]*A+E[1:-2])*A+E[2:-1])*A+E[3:]].sum(), np.bincount(E,minlength=A)
def local(M, js):
    js=js[(js>=3)]
    idx=js[:,None]+np.arange(-3,1)[None,:]            # tokens j-3..j
    L=CHA[M[S[idx]]].reshape(len(js),8)              # 8 letter slots
    valid=L>=0; order=np.argsort(valid,axis=1,kind='stable')   # nulls first, valid right-aligned in order
    R=np.take_along_axis(L,order,axis=1)
    last=R[:,7]; s=lp[((R[:,4]*A+R[:,5])*A+R[:,6])*A+last].sum()
    two=CHA[M[S[js]],1]>=0
    if two.any(): r=R[two]; s+=lp[((r[:,3]*A+r[:,4])*A+r[:,5])*A+r[:,6]].sum()
    return s
def affected(ti):
    P=pos[ti]; js=np.unique((P[:,None]+np.arange(4)[None,:]).ravel()); return js[js<N]
LAM=1.0
def kl(cnt): q=cnt/cnt.sum(); m=q>0; return float((q[m]*np.log(q[m]/lf[m])).sum())
# init: every type -> a random letter weighted by frequency
M=np.array([np.random.choice(A,p=lf) for _ in range(K)],dtype=np.int64)
cur_lm,cnt=full(M); cnt=cnt.astype(float)
def total(lm,cnt): return N*(lm/cnt.sum())-LAM*N*kl(cnt)
cur=total(cur_lm,cnt); best=cur; bestM=M.copy(); T0=8.0; t0=time.time()
if truth is not None:
    TM=np.array([truth[w] for w in top]); tl,tc=full(TM); print(f'  true key: LM/char {tl/tc.sum():.3f} total {total(tl,tc.astype(float)):.0f}; init total {cur:.0f}', flush=True)
for it in range(iters):
    ti=random.choice(active); old=M[ti]; new=random.randrange(C) if random.random()<0.5 else random.randrange(A)
    if new==old: continue
    js=affected(ti); a=local(M,js)
    n=len(pos[ti]); oc=CHA[old]; nc=CHA[new]; d_cnt=np.zeros(A)
    for x in oc:
        if x>=0: d_cnt[x]-=n
    for x in nc:
        if x>=0: d_cnt[x]+=n
    M[ti]=new; b=local(M,js); cnt2=cnt+d_cnt; lm2=cur_lm+(b-a)
    new_total=total(lm2,cnt2); d=new_total-cur
    if d>=0 or random.random()<math.exp(d/max(0.05,T0*(1-it/iters))): cur=new_total; cnt=cnt2; cur_lm=lm2
    else: M[ti]=old
    if cur>best: best=cur; bestM=M.copy()
    if it and it%500000==0: print(f'  progress {it/1e6:.1f}M/{iters/1e6:.1f}M best {best:.0f} ({time.time()-t0:.0f}s)', flush=True)
bl,bc=full(bestM); dec=CHA[bestM[S]].ravel(); dec=''.join(ALPHA[x] for x in dec if x>=0)
res=f'[{target} subset={SUBSET} lang={LANG} seed={seed} N={N} drop={DROP:.3f}] LM/char={bl/bc.sum():.3f} total={total(bl,bc.astype(float)):.0f} bigram-share={np.mean(CHA[bestM[S],1]>=0):.2f}'
if truth is not None:
    res+=f' | token-acc={np.mean([bestM[s]==truth[top[s]] for s in S]):.3f} decoded-letter-match={sum(1 for a,b in zip(dec, "".join(ALPHA[x] for x in CHA[TM[S]].ravel() if x>=0)) if a==b)/max(1,len(dec)):.3f}'
print(res, flush=True); print('  sample:', dec[:240])
if HOLD:
    def lmc(M,X):
        E=CHA[M[X]].ravel(); E=E[E>=0]; return lp[((E[:-3]*A+E[1:-2])*A+E[2:-1])*A+E[3:]].sum()/len(E)
    rng=np.random.default_rng(seed); keys=[('fitted',bestM)]+([('true',TM)] if truth is not None else [])
    for name,KM in keys:
        o=lmc(KM,SH); sh=[lmc(KM,rng.permutation(SH)) for _ in range(20)]
        print(f'  heldout {name} key: in-order {o:.4f} shuffled {np.mean(sh):.4f} sd {np.std(sh):.4f} gain {o-np.mean(sh):+.4f} z {(o-np.mean(sh))/np.std(sh):.1f}', flush=True)
