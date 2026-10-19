"""Vertical-neighbour similarity (Timm & Schinner; NOTES §23): mean minimum edit distance from a word to the words at similar
positions in the line above/below, vs to words at the same positions on a random other page. Real text vs rule models."""
import random, json, sys
import gen3_fit as G
def ed(a,b):
    D=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        P=D[:]; D[0]=i
        for j,y in enumerate(b,1): D[j]=min(P[j]+1,D[j-1]+1,P[j-1]+(x!=y))
    return D[-1]
def vert(pages, rng, n=3000):
    near=far=0; k=0
    cand=[(pi,li) for pi,p in enumerate(pages) for li in range(1,len(p)) if p[li] and p[li-1]]
    for _ in range(n):
        pi,li=rng.choice(cand); line=pages[pi][li]; j=rng.randrange(len(line)); w=line[j]
        up=pages[pi][li-1]; nb=up[max(0,j-1):j+2] or up
        qi=rng.randrange(len(pages)); q=pages[qi]
        if qi==pi or len(q)<2: continue
        ql=rng.choice([l for l in q if l] or [['o']]); rb=ql[max(0,j-1):j+2] or ql
        near+=min(ed(w,x) for x in nb); far+=min(ed(w,x) for x in rb); k+=1
    return near/k, far/k
rng=random.Random(0)
r=vert(G.REAL,rng); print(f'real: vertical neighbours {r[0]:.2f}, same positions on another page {r[1]:.2f}, difference {r[1]-r[0]:.2f}')
for name,cfg in [('rule model, no copying',{"p_local":0.0}),('rule model, 3% copying',{"p_local":0.03}),('rule model, 15% copying',{"p_local":0.15})]:
    P=dict({"topic_p":0.08,"topic_n":26,"p_q":0.92,"p_unq":0.39,"p_alt":0.62,"p_new":0.22,"p_rep":0.006},**cfg)
    m=vert(G.gen(7,**P),rng); print(f'{name}: {m[0]:.2f} vs {m[1]:.2f}, difference {m[1]-m[0]:.2f}')
