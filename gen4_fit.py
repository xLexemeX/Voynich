"""Random search over the stem model (gen4.py): fit the scorecard and the §73 gradient together."""
import random, json, sys, math
import gen4 as M, gen3_fit as G
from scorecard import card
R=card(G.REAL); RM,RD=M.decomp(G.REAL)
TGT={**{k:R[k] for k in M.KEYS}, 'lines':RD[0], 'page':RD[1], 'section':RD[2], 'any-page':RM[3]}
SCALE={'types/tokens':0.01,'hapax share of types':0.02,'line-initial repeat ratio':0.05,'page-exclusive rate (40 pages)':0.04,'y|qo junction ratio':0.3,'h2':0.02,
       'lines':0.03,'page':0.03,'section':0.03,'any-page':0.08}
def score(prm, seed=7):
    P=M.gen(seed,**prm); c=card(P); m,d=M.decomp(P)
    v={**{k:c[k] for k in M.KEYS},'lines':d[0],'page':d[1],'section':d[2],'any-page':m[3]}
    return math.sqrt(sum(((v[k]-TGT[k])/SCALE[k])**2 for k in TGT)), v
if __name__=='__main__':
    rng=random.Random(int(sys.argv[1])); best=None
    print('target', json.dumps({k:round(v,3) for k,v in TGT.items()}), flush=True)
    for i in range(int(sys.argv[2])):
        prm=dict(group_lex=True, norm=rng.random()<0.5, n_sec=rng.choice([10,20,40,80]), n_page=rng.choice([3,6,10]), p_sec=rng.uniform(0.3,1),
                 p_nh=0.0, p_nl=0.0, topic_p=rng.uniform(0,0.1), k_h=rng.choice([1,3,10,20]), k_l=rng.choice([2,3,5]), p_kl=rng.uniform(0,1),
                 recent=rng.choice([0,1,2]), p_recent=rng.uniform(0,0.5), p_new=rng.uniform(0.15,0.25))
        d,v=score(prm)
        if best is None or d<best[0]:
            best=(d,prm,v); print(f'{i:3d} dist {d:6.2f} {json.dumps({k:(round(x,2) if isinstance(x,float) else x) for k,x in prm.items()})}\n     {json.dumps({k:round(x,3) for k,x in v.items()})}', flush=True)
