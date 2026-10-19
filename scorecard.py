"""Scorecard: the statistics any model of the Voynich text must reproduce, computed on pages -> lines -> words.
Used for the real text and for generators laid out on the real page/line structure."""
import csv, re, math, collections, random
G=re.compile(r"cth|ckh|cph|cfh|ch|sh|[a-z]")
def real_pages(section=None, lang=None):
    pg=collections.OrderedDict()
    for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t'):
        if r['text'] and r['ltype'].startswith('P') and (not section or r['section']==section) and (not lang or r['lang']==lang):
            ws=[w for w in r['text'].split('.') if re.fullmatch(r'[a-z]+',w)]
            if ws: pg.setdefault(r['folio'],[]).append(ws)
    return list(pg.values())
def h2(words):
    c1=collections.Counter(); c2=collections.Counter()
    for w in words:
        s=' '+w
        for a,b in zip(s,s[1:]+' '): c1[a]+=1; c2[(a,b)]+=1
    n=sum(c1.values()); return -sum(v/n*math.log2(v/n) for v in c2.values())+sum(v/n*math.log2(v/n) for v in c1.values())
def line_alt(pages, rng):
    S=[[G.match(l[0]).group() for l in p[1:] if l and G.match(l[0])] for p in pages]
    rep=lambda S:sum(a==b for s in S for a,b in zip(s,s[1:]))/max(1,sum(len(s)-1 for s in S))
    o=rep(S); sh=sum(rep([rng.sample(s,len(s)) for s in S]) for _ in range(30))/30; return o/sh if sh else float('nan')
def page_excl(pages, n=40, draws=100, rng=None):
    P=[[w for l in p for w in l][:84] for p in pages if sum(map(len,p))>=84]
    if len(P)<n: return float('nan')
    out=[]
    for _ in range(draws):
        S=rng.sample(P,n); occ=collections.defaultdict(set)
        for i,ws in enumerate(S):
            for w in ws: occ[w].add(i)
        out.append(sum(any(c>=2 and len(occ[w])==1 for w,c in collections.Counter(ws).items()) for ws in S)/n)
    return sum(out)/len(out)
def qo_junction(pages):
    a=b=c=d=0
    for p in pages:
        for l in p:
            for x,y in zip(l,l[1:]):
                q=y.startswith('qo')
                if x.endswith('y'): a+=q; b+=1
                else: c+=q; d+=1
    return (a/b)/(c/d) if b and d and c else float('nan')
def card(pages, rng=None):
    rng=rng or random.Random(0)
    W=[w for p in pages for l in p for w in l]; c=collections.Counter(W)
    return {'tokens':len(W),'types/tokens':len(c)/len(W),'hapax share of types':sum(v==1 for v in c.values())/len(c),
            'mean word length':sum(map(len,W))/len(W),'h2':h2(W),'adjacent repeats':sum(a==b for p in pages for l in p for a,b in zip(l,l[1:]))/len(W),
            'line-initial repeat ratio':line_alt(pages,rng),'page-exclusive rate (40 pages)':page_excl(pages,rng=rng),'y|qo junction ratio':qo_junction(pages)}
if __name__=='__main__':
    for name,P in [('all paragraph text',real_pages()),('herbal A',real_pages('herbal','A'))]:
        print(name); [print(f'   {k:32s} {v:.3f}' if isinstance(v,float) else f'   {k:32s} {v}') for k,v in card(P).items()]
