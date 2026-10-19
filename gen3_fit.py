"""Random search: can lexicon reuse + page topic + junction rule + line-initial avoidance match the sequence-level statistics
simultaneously? Lexicon = real word types (so word-internal statistics match by construction)."""
import random, collections, math, json, sys
from scorecard import real_pages, card
REAL=real_pages(); R=card(REAL)
W=[w for p in REAL for l in p for w in l]; cnt=collections.Counter(W)
HAPAX=[w for w,c in cnt.items() if c==1]                     # one-shot words: emitted once, never re-copied
LEX=[w for w,c in cnt.most_common() if c>1]; FR=[cnt[w] for w in LEX]
def gen(seed, p_local, topic_p, topic_n, p_q, p_unq, p_alt, p_new, p_rep=0.0, fav_min=1):
    rng=random.Random(seed); out=[]; pool=HAPAX[:]; rng.shuffle(pool); used=set()
    cum=[];s=0
    for f in FR: s+=f; cum.append(s)
    import bisect
    def glob(): return LEX[bisect.bisect(cum, rng.random()*s)]
    for p in REAL:
        fav=[];
        while len(fav)<topic_n:
            w=glob()
            if cnt[w]>=fav_min: fav.append(w)
        page=[]; prev=None
        for l in p:
            line=[]
            for j in range(len(l)):
                for t in range(4):
                    if pool and rng.random()<p_new: w=pool.pop(); used.add(w)
                    elif page and rng.random()<p_local:
                        cand=[x for x in rng.choice(page) if x not in used] or [glob()]; w=rng.choice(cand)
                    elif rng.random()<topic_p: w=rng.choice(fav)
                    else: w=glob()
                    if j>0 or prev is None or w[0]!=prev or rng.random()>p_alt: break
                if line and rng.random()<p_rep: w=line[-1]
                elif line:
                    if line[-1].endswith('y') and w.startswith('o') and rng.random()<p_q: w='q'+w
                    elif not line[-1].endswith('y') and w.startswith('qo') and rng.random()<p_unq: w=w[1:]
                line.append(w)
            prev=line[0][0] if line else prev; page.append(line)
        out.append(page)
    return out
KEYS=['types/tokens','hapax share of types','adjacent repeats','line-initial repeat ratio','page-exclusive rate (40 pages)','y|qo junction ratio']
SCALE={'types/tokens':0.02,'hapax share of types':0.03,'adjacent repeats':0.003,'line-initial repeat ratio':0.1,'page-exclusive rate (40 pages)':0.05,'y|qo junction ratio':0.4}
def dist(c): return math.sqrt(sum(((c[k]-R[k])/SCALE[k])**2 for k in KEYS))
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0); best=None
    START=json.loads(sys.argv[3]) if len(sys.argv)>3 else None
    for i in range(int(sys.argv[2]) if len(sys.argv)>2 else 40):
        if START:
            base=best[1] if best else START
            prm={k:(min(1,max(0,v+rng.gauss(0,0.06))) if k!='topic_n' else max(3,int(v+rng.gauss(0,8)))) for k,v in base.items()}
        else:
            prm=dict(p_local=rng.uniform(0,0.5),topic_p=rng.uniform(0,0.3),topic_n=rng.randint(5,80),p_q=rng.uniform(0.2,0.9),p_unq=rng.uniform(0.2,0.9),p_alt=rng.uniform(0,1),p_new=rng.uniform(0.05,0.25),p_rep=rng.uniform(0,0.01))
        c=card(gen(i,**prm)); d=dist(c)
        if best is None or d<best[0]: best=(d,prm,c); print(f'{i:3d} dist {d:6.2f} {json.dumps({k:round(v,2) for k,v in prm.items()})}', flush=True)
    print('\nbest fit vs real:'); [print(f'   {k:32s} real {R[k]:7.3f}  model {best[2][k]:7.3f}') for k in KEYS+['h2','mean word length']]
