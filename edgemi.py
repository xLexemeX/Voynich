"""Mutual information between the last glyph of a word and the first glyph of the next word on the same line (arXiv 2608.17096
reports about 0.2 bits for Voynichese, above prose controls). Real text vs the rule model of §72 and line-shuffled real text.
Plug-in MI minus the mean over within-line word shuffles, which removes most of the small-sample bias."""
import random, math, collections, statistics, sys
from scorecard import G as GL
import gen3_fit as G3
def mi(pairs):
    n=len(pairs); a=collections.Counter(x for x,_ in pairs); b=collections.Counter(y for _,y in pairs); ab=collections.Counter(pairs)
    return sum(c/n*math.log2(c*n/(a[x]*b[y])) for (x,y),c in ab.items())
def edges(pages):
    return [(GL.findall(x)[-1],GL.findall(y)[0]) for p in pages for l in p for x,y in zip(l,l[1:])]
def report(name, pages, rng):
    o=mi(edges(pages)); sh=[mi(edges([[rng.sample(l,len(l)) for l in p] for p in pages])) for _ in range(10)]
    print(f'{name:40s} edge MI {o:.3f} bits; within-line shuffles {statistics.mean(sh):.3f}; excess {o-statistics.mean(sh):+.3f}', flush=True)
if __name__=='__main__':
    rng=random.Random(0)
    report('real', G3.REAL, rng)
    P=dict(p_local=0.0,topic_p=0.08,topic_n=26,p_q=0.92,p_unq=0.39,p_alt=0.62,p_new=0.22,p_rep=0.006)
    report('rule model (§72), junction rule on', G3.gen(7,**P), rng)
    report('rule model, junction rule off', G3.gen(7,**dict(P,p_q=0.0,p_unq=0.0)), rng)
def contrib(pages):
    E=edges(pages); n=len(E); a=collections.Counter(x for x,_ in E); b=collections.Counter(y for _,y in E); ab=collections.Counter(E)
    return {k:c/n*math.log2(c*n/(a[k[0]]*b[k[1]])) for k,c in ab.items()}, ab, a, b, n
if __name__=='__main__':
    cr,ab,a,b,n=contrib(G3.REAL); cm,abm,_,_,_=contrib(G3.gen(7,**P))
    print('\nlargest real-minus-model contributions (last glyph | first glyph): count, observed/expected in real, contribution real vs model')
    for k in sorted(set(cr)|set(cm), key=lambda k:-abs(cr.get(k,0)-cm.get(k,0)))[:16]:
        print(f'   {k[0]:>4s} | {k[1]:<4s} n={ab[k]:5d}  obs/exp {ab[k]*n/(a[k[0]]*b[k[1]]) if ab[k] else 0:5.2f}   {cr.get(k,0):+.4f} vs {cm.get(k,0):+.4f}')
def zl_edges():
    """Edges from ZL3b-n.txt paragraph lines, kept apart by separator: '.' (certain space) and ',' (uncertain space)."""
    import re
    out={'.':[],',':[]}
    for line in open('data/ZL3b-n.txt',encoding='utf-8',errors='replace'):
        m=re.match(r'<f[^,>]+,[@+=*~]P\w*>\s+(.*)',line)
        if not m: continue
        t=re.sub(r'<->','.',m.group(1)); t=re.sub(r'<[^>]*>','',t); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t); t=re.sub(r'@\d+;','?',t)
        toks=re.split(r'([.,])',t)
        for i in range(1,len(toks)-1,2):
            x,y=toks[i-1],toks[i+1]
            if re.fullmatch('[a-z]+',x) and re.fullmatch('[a-z]+',y): out[toks[i]].append((GL.findall(x)[-1],GL.findall(y)[0]))
    return out
if __name__=='__main__':
    Z=zl_edges(); allp=Z['.']+Z[',']
    print('\nby separator in ZL3b-n:')
    for name,E in [('certain spaces (.)',Z['.']),('uncertain spaces (,)',Z[',']),('both',allp)]:
        o=mi(E); sh=[]
        for s in range(10):
            r=random.Random(s); ys=[y for _,y in E]; r.shuffle(ys); sh.append(mi([(x,y) for (x,_),y in zip(E,ys)]))
        print(f'   {name:22s} n={len(E):6d}  edge MI {o:.3f}; permuted {statistics.mean(sh):.3f}; excess {o-statistics.mean(sh):+.3f}')
    for k in [('r','a'),('s','a'),('o','l'),('y','q')]:
        print(f'   {k[0]}|{k[1]}: {sum(e==k for e in Z["."])} across certain spaces, {sum(e==k for e in Z[","])} across uncertain')
