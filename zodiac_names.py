import csv, collections, itertools, random, numpy as np
random.seed(21)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
W=[('Pisces','f70v2'),('AriesD','f70v1'),('AriesL','f71r'),('TaurusL','f71v'),('TaurusD','f72r1'),('Gemini','f72r2'),('Cancer','f72r3'),('Leo','f72v3'),('Virgo','f72v2'),('Libra','f72v1'),('Scorpio','f73r'),('Sagitt','f73v')]
def words(f,label): return [w for r in rows if r['folio']==f and (r['ltype'].startswith('L')==label) for w in r['text'].split('.') if w]
glob=collections.Counter(w for r in rows for w in r['text'].split('.') if w)
paired={frozenset(('AriesD','AriesL')),frozenset(('TaurusL','TaurusD'))}
for label,name in [(False,'ring text'),(True,'labels'),(None,'both')]:
    sets={s:set(words(f,False) if label is False else words(f,True) if label else words(f,False)+words(f,True)) for s,f in W}
    def jac(a,b): return len(sets[a]&sets[b])/len(sets[a]|sets[b])
    pairs=list(itertools.combinations([s for s,_ in W],2))
    pj=[jac(a,b) for a,b in pairs if frozenset((a,b)) in paired]; oj=[jac(a,b) for a,b in pairs if frozenset((a,b)) not in paired]
    rank=[sorted([jac(a,b) for a,b in pairs],reverse=True).index(x)+1 for x in pj]
    print(f'{name:9s}: paired-wheel Jaccard {["%.3f"%x for x in pj]} vs other pairs mean {np.mean(oj):.3f} (max {max(oj):.3f}); rank of paired among {len(pairs)} pairs: {rank}')
    # words shared by both wheels of a pair and absent from all other 10 wheels
    for pa in [('AriesD','AriesL'),('TaurusL','TaurusD')]:
        others=set().union(*[sets[s] for s,_ in W if s not in pa])
        excl=sorted(w for w in sets[pa[0]]&sets[pa[1]] if w not in others)
        print(f'   words on both {pa} and on no other wheel: {[(w,glob[w]) for w in excl]}')
    # null: how many exclusive shared words does a random non-paired pair have?
    ex=[]
    for a,b in pairs:
        if frozenset((a,b)) in paired: continue
        others=set().union(*[sets[s] for s,_ in W if s not in (a,b)])
        ex.append(len([w for w in sets[a]&sets[b] if w not in others]))
    print(f'   exclusive shared words for non-paired wheel pairs: mean {np.mean(ex):.2f}, max {max(ex)}, distribution {collections.Counter(ex)}')
