"""Does each page have its own spelling profile? For word features (start, end, glyph content), the spread of the per-page
rate across pages, against the spread when words are shuffled among the pages of their own section/language/hand group.
Ratio = real variance / mean shuffled variance (1 = no page profile beyond the group)."""
import random, collections, statistics, re, sys
import vertical2 as V
from pageshuffle import shuffle
P=[(m,L) for m,L in V.pages() if sum(map(len,L))>=60]
F={'starts qo':lambda w:w.startswith('qo'),'starts ch':lambda w:w.startswith('ch'),'starts sh':lambda w:w.startswith('sh'),'starts o':lambda w:w.startswith('o'),
   'starts d':lambda w:w.startswith('d'),'ends y':lambda w:w.endswith('y'),'ends dy':lambda w:w.endswith('dy'),'ends n':lambda w:w.endswith('n'),'ends l':lambda w:w.endswith('l'),
   'ends r':lambda w:w.endswith('r'),'has k':lambda w:'k' in w,'has t':lambda w:'t' in w,'has ee':lambda w:'ee' in w,'has a':lambda w:'a' in w,'has gallows p/f':lambda w:re.search('[pf]',w) is not None,
   'has ckh/cth':lambda w:re.search('c[kt]h',w) is not None,'length>=6':lambda w:len(w)>=6}
def var(Q,f):
    r=[statistics.mean(f(w) for l in L for w in l) for _,L in Q]; return statistics.pvariance(r)
def table(Q, label):
    S=[shuffle(Q,random.Random(s)) for s in range(20)]
    out=[]
    for n,f in F.items():
        v=var(Q,f); sv=[var(x,f) for x in S]; out.append((n, v/statistics.mean(sv), max(sv)/statistics.mean(sv)))
    print(label); [print(f'   {n:18s} ratio {r:5.2f}   (largest shuffle {mx:.2f})') for n,r,mx in out]
    return out
if __name__=='__main__':
    table(P,'Voynich, pages of 60+ words (%d pages)'%len(P))
    for path in sys.argv[1:]:
        Q=[x for x in V.layout(path,V.pages()) if sum(map(len,x[1]))>=60]
        table(Q,path)
def generic(Q):
    """Language-neutral features: the 6 commonest first letters, 6 commonest last letters, 6 commonest letters anywhere."""
    W=[w for _,L in Q for l in L for w in l]
    fi=[c for c,_ in collections.Counter(w[0] for w in W).most_common(6)]; la=[c for c,_ in collections.Counter(w[-1] for w in W).most_common(6)]
    an=[c for c,_ in collections.Counter(ch for w in W for ch in set(w)).most_common(6)]
    G={**{f'starts {c}':(lambda c:lambda w:w[0]==c)(c) for c in fi},**{f'ends {c}':(lambda c:lambda w:w[-1]==c)(c) for c in la},
       **{f'has {c}':(lambda c:lambda w:c in w)(c) for c in an}}
    S=[shuffle(Q,random.Random(s)) for s in range(20)]
    r=[var(Q,f)/statistics.mean(var(x,f) for x in S) for f in G.values()]
    return statistics.median(r), min(r), max(r)
if __name__=='__main__':
    print('\ngeneric features (median ratio, range over 18 features):')
    print('   Voynich        %.2f  (%.2f-%.2f)'%generic(P))
    for path in ['data/ref/latin_pliny.txt','data/ref/italian_dante.txt','data/ext_cat/tirant.txt','data/ref/german_faust.txt']:
        try: Q=[x for x in V.layout(path,V.pages()) if sum(map(len,x[1]))>=60]
        except AssertionError: print('   '+path+' too short for the layout'); continue
        print('   %-14s %.2f  (%.2f-%.2f)'%((path.split('/')[-1][:-4],)+generic(Q)))
