"""Rule model of §72 plus stems: each section/language/hand group gets a set of stem words, each page draws its stems
from its group, and a share of words (one-shot and lexicon) is chosen among the forms close in spelling to a page stem.
Tests whether this reproduces the page and section clustering of word forms (NOTES §73) without spoiling the scorecard."""
import random, collections, bisect, statistics, sys, json
import gen3_fit as G, vertical2 as V
from scorecard import card
META=[m for m,_ in V.pages()]; assert len(META)==len(G.REAL)
def dels(w): return {w}|{w[:i]+w[i+1:] for i in range(len(w))}
def index(words):
    ix=collections.defaultdict(set)
    for w in words:
        for d in dels(w): ix[d].add(w)
    return ix
IXH=index(G.HAPAX); IXL=index(G.LEX); FREQ=dict(zip(G.LEX,G.FR))
def _big():
    from scorecard import G as GL
    c=collections.defaultdict(collections.Counter)
    for w,n in G.cnt.items():
        g=[' ']+GL.findall(w)
        for a,b in zip(g,g[1:]): c[a][b]+=n
    return {a:(list(v),list(v.values())) for a,v in c.items()}
BIG=_big()
def near(ix, s): return set().union(*(ix.get(d,()) for d in dels(s)))-{s}
def gen(seed, group_lex=False, n_sec=60, n_page=6, p_sec=0.8, p_nh=0.5, p_nl=0.2, topic_p=0.08, topic_n=26, p_q=0.92, p_unq=0.39, p_alt=0.62, p_new=0.22, p_rep=0.006, k_h=1, k_l=1, recent=0, p_kl=1.0, p_recent=1.0, norm=False, p_mut=0.0, mut='cross', n_edit=1, mut_src='stems'):
    rng=random.Random(seed); pool=G.HAPAX[:]; rng.shuffle(pool); used=set()
    cum=list(__import__('itertools').accumulate(G.FR)); tot=cum[-1]
    gl={}
    if group_lex:                                 # each group draws from its own real lexicon and its own one-shot words
        for m,p in zip(META,G.REAL):
            for l in p:
                for w in l: gl.setdefault(m,collections.Counter())[w]+=1
        gl={m:([w for w in c if G.cnt[w]>1],list(__import__('itertools').accumulate(c[w] for w in c if G.cnt[w]>1)),[w for w in c if G.cnt[w]==1]) for m,c in gl.items()}
        for m in gl: rng.shuffle(gl[m][2])
    cur=[None]
    def glob():
        if group_lex: L,C,_=gl[cur[0]]; return L[bisect.bisect(C, rng.random()*C[-1])]
        return G.LEX[bisect.bisect(cum, rng.random()*tot)]
    secstems=collections.defaultdict(list)
    def close(w,x): return V.ed(w,x)/max(len(w),len(x)) if norm else V.ed(w,x)
    def best(cands, stems): return min(cands, key=lambda w: min(close(w,x) for x in stems))
    def glyphs(w): return __import__('scorecard').G.findall(w)
    def new_hapax(stems):
        if rng.random()<p_mut:                    # variation: the head of a page stem joined to the tail of a real one-shot word
            pl=gl[cur[0]][2] if group_lex else pool
            if pl:
                if mut=='edit':                   # change n_edit glyphs of the stem, each drawn given the glyph before it
                    src=[x for l2 in cur[1] for x in l2] if mut_src=='page' else stems
                    a=glyphs(rng.choice(src or stems))
                    for _ in range(n_edit):
                        i=rng.randrange(len(a)); prev=a[i-1] if i else ' '
                        nx=BIG.get(prev)
                        if nx: a[i]=rng.choices(nx[0],weights=nx[1])[0]
                    w=''.join(a)
                    if w not in G.cnt: return w
                a=glyphs(rng.choice(stems)); b=glyphs(pl.pop())
                if len(a)>1 and len(b)>1:
                    return ''.join(a[:rng.randrange(1,len(a))]+b[rng.randrange(1,len(b)):])
        if k_h>1:                                 # best of k_h unused one-shot words, by closeness to the page stems
            pl=gl[cur[0]][2] if group_lex else pool; c=[]
            while pl and len(c)<k_h:
                w=pl.pop()
                if w not in used: c.append(w)
            if c:
                w=best(c,stems); c.remove(w); [pl.insert(rng.randrange(len(pl)+1),x) for x in c]; used.add(w); return w
        if rng.random()<p_nh:
            c=[w for w in near(IXH, rng.choice(stems)) if w not in used]
            if c: w=rng.choice(sorted(c)); used.add(w); return w
        pl=gl[cur[0]][2] if group_lex else pool
        while pl:
            w=pl.pop()
            if w not in used: used.add(w); return w
        return glob()
    def lex(stems):
        if k_l>1 and rng.random()<p_kl: return best([glob() for _ in range(k_l)], stems)
        if rng.random()<p_nl:
            c=sorted(near(IXL, rng.choice(stems)))
            if c: return rng.choices(c, weights=[FREQ[x] for x in c])[0]
        return glob()
    out=[]
    for m,p in zip(META,G.REAL):
        cur[0]=m
        if not secstems[m]: secstems[m]=[glob() for _ in range(n_sec)]
        stems=[rng.choice(secstems[m]) if rng.random()<p_sec else glob() for _ in range(n_page)]
        fav=[lex(stems) for _ in range(topic_n)]
        page=[]; prev=None; cur[1:]=[page]
        for l in p:
            line=[]
            for j in range(len(l)):
                st=stems+[x for l2 in page[-recent:] for x in l2] if recent and rng.random()<p_recent else stems
                for t in range(4):
                    if rng.random()<p_new: w=new_hapax(st)
                    elif rng.random()<topic_p: w=rng.choice(fav)
                    else: w=lex(st)
                    if j>0 or prev is None or w[0]!=prev or rng.random()>p_alt: break
                if line and rng.random()<p_rep: w=line[-1]
                elif line:
                    if line[-1].endswith('y') and w.startswith('o') and rng.random()<p_q: w='q'+w
                    elif not line[-1].endswith('y') and w.startswith('qo') and rng.random()<p_unq: w=w[1:]
                line.append(w)
            prev=line[0][0] if line else prev; page.append(line)
        out.append(page)
    return out
def decomp(pages, seeds=(0,1,2)):
    R=[V.run(list(zip(META,pages)),random.Random(s),n=3000) for s in seeds]
    m=[statistics.mean(r[t] for r in R) for t in range(4)]
    return m, (m[1]-m[0], m[2]-m[1], m[3]-m[2])
KEYS=['types/tokens','hapax share of types','line-initial repeat ratio','page-exclusive rate (40 pages)','y|qo junction ratio','h2']
if __name__=='__main__':
    R=card(G.REAL); m,d=decomp(G.REAL)
    print('real   '+' '.join(f'{k[:12]}={R[k]:.3f}' for k in KEYS)+f' | gradient lines {d[0]:+.3f} page {d[1]:+.3f} section {d[2]:+.3f} (any-page {m[3]:.2f})', flush=True)
    for cfg in map(json.loads, sys.argv[1:]):
        P=gen(7,**cfg); c=card(P); m,d=decomp(P)
        print(f'{json.dumps(cfg)}\n       '+' '.join(f'{k[:12]}={c[k]:.3f}' for k in KEYS)+f' | gradient lines {d[0]:+.3f} page {d[1]:+.3f} section {d[2]:+.3f} (any-page {m[3]:.2f})', flush=True)
