"""Controlled decipherment experiment.
Hypothesis under test: Voynich glyph-units map 1:1 (or to nothing) onto Latin letters, spaces are real.
Method: simulated annealing over the mapping, objective = Latin character 4-gram log-likelihood.
Controls: (a) Latin text under a random substitution (should be recovered), (b) meaningless text from a
Voynich-like Markov generator (should NOT score like Latin). Report LM score/char and % of decoded words in Latin lexicon.
"""
import collections, csv, re, random, math, sys, numpy as np
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 0); np.random.seed(0)
target=sys.argv[1] if len(sys.argv)>1 else 'voynich'
UNITS=['cth','ckh','cph','cfh','ch','sh','iin','in','ee','q','o','a','y','d','k','t','p','f','l','r','s','n','m','g','e','i']
def tokenize(w):
    out=[]; i=0
    while i<len(w):
        for u in UNITS:
            if w.startswith(u,i): out.append(u); i+=len(u); break
        else: i+=1
    return out
import alphabet as AB
rows=[r for r in csv.DictReader(open(AB.CORPUS),delimiter='\t') if r['text']]
if AB.ALPH=='chars': tokenize=AB.rare_folder([w for r in rows for w in r['text'].split('.') if w])
def latin_words(path):
    return re.findall(r'[a-z]+', open(path,encoding='utf-8',errors='replace').read().lower().replace('v','u').replace('j','i'))
pli=[w for w in latin_words('data/ref/latin_pliny.txt') if not re.fullmatch(r'[ivxlcdm]+',w) or w in ('mi','di','dum','cum','id','ii','ille','illi')]
lm_train=pli[:40000]; lexicon=set(pli); lat_all=pli[40000:]
ALPHA='abcdefghilmnopqrstuxyz '; A=len(ALPHA); NULL=A
aid={c:i for i,c in enumerate(ALPHA)}
# 4-gram LM with add-k smoothing over letters+space
txt=' '.join(w for w in lm_train if all(c in aid for c in w)); ids=np.array([aid[c] for c in txt])
K=4; cnt=collections.Counter(tuple(ids[i:i+K]) for i in range(len(ids)-K+1)); ctx=collections.Counter(tuple(ids[i:i+K-1]) for i in range(len(ids)-K+2))
logP=np.full(A**K, math.log(0.01/(A)), dtype=np.float32)
for g,c in cnt.items():
    idx=g[0]*A**3+g[1]*A**2+g[2]*A+g[3]; logP[idx]=math.log((c+0.01)/(ctx[g[:3]]+0.01*A))
def score(seq):
    if len(seq)<K: return -1e9
    idx=seq[:-3]*A**3+seq[1:-2]*A**2+seq[2:-1]*A+seq[3:]
    return float(logP[idx].sum())
# build the target sequence of unit ids (space unit = -1)
if target=='voynich':
    words=[tokenize(w) for r in rows for w in r['text'].split('.') if w]
elif target=='markov':   # meaningless control with Voynich-like unit bigram statistics
    vw=[tokenize(w) for r in rows for w in r['text'].split('.') if w]
    trans=collections.defaultdict(list)
    for w in vw:
        s=['<']+w+['>']
        for a,b in zip(s,s[1:]): trans[a].append(b)
    words=[]
    while len(words)<len(vw):
        w=[]; cur='<'
        while True:
            cur=random.choice(trans[cur])
            if cur=='>': break
            w.append(cur)
        if w: words.append(w)
elif target=='latin':    # positive control: Latin under random substitution (units = letters)
    lw=[w for w in lat_all if all(c in aid for c in w) and not re.fullmatch(r'[ivxlcdm]+',w)][:38000]
    perm=list(ALPHA[:-1]); random.shuffle(perm); P=dict(zip(ALPHA[:-1],perm))
    words=[[P[c] for c in w] for w in lw]
units=sorted(set(u for w in words for u in w)); uid={u:i for i,u in enumerate(units)}; U=len(units)
flat=[]; 
for w in words: flat.extend(uid[u] for u in w); flat.append(-1)
flat=np.array(flat); is_space=flat==-1
def decode(M):
    out=np.where(is_space, aid[' '], M[np.where(is_space,0,flat)])
    return out[out!=NULL]
MEAN_LP=-2.45   # avg log-prob per char of real Latin under this LM; deleting a unit costs this much
MAXNULL=4
def s_of(M):
    if (M==NULL).sum()>MAXNULL: return -1e18
    d=decode(M); ndel=int((~is_space).sum())-int((d!=aid[' ']).sum())
    return score(d)+ndel*MEAN_LP
# init: most frequent units -> most frequent Latin letters
lf=collections.Counter(txt.replace(' ','')); uf=collections.Counter(flat[~is_space].tolist())
M=np.full(U, NULL); 
for (u,_),(c,_) in zip(uf.most_common(), lf.most_common()): M[u]=aid[c]
cur=s_of(M); best=cur; bestM=M.copy(); T=200.0
iters=int(sys.argv[3]) if len(sys.argv)>3 else 30000
for it in range(iters):
    M2=M.copy()
    if random.random()<0.5:
        u=random.randrange(U); M2[u]=random.choice(list(range(A-1))+[NULL]*3)
    else:
        u,v=random.sample(range(U),2); M2[u],M2[v]=M[v],M[u]
    s=s_of(M2)
    if s>cur or random.random()<math.exp((s-cur)/T):
        M,cur=M2,s
        if s>best: best,bestM=s,M.copy()
    T=max(0.5,T*0.9997)
dec=decode(bestM); s=''.join(ALPHA[i] for i in dec); dw=s.split()
inlex=sum(w in lexicon for w in dw)/len(dw); inlex4=sum(w in lexicon for w in dw if len(w)>=4)/max(1,sum(len(w)>=4 for w in dw))
print(f'[{target}] best LM score/char = {score(dec)/len(dec):.3f}; deleted units {(bestM==NULL).sum()}; decoded words {len(dw)}; in-lexicon {inlex:.1%}; in-lexicon (len>=4) {inlex4:.1%}')
print('mapping:', {units[i]:(ALPHA[bestM[i]] if bestM[i]<A else '∅') for i in range(U)})
print('sample:', s[:600])
