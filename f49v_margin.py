"""f49v: does the margin glyph beside each line relate to that line's text?"""
import csv, random
R=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['folio']=='f49v']
pairs=[]; m=None
for r in R:
    if r['ltype'].startswith('L'): m=r['text']
    elif m is not None: pairs.append((m,r['text'])); m=None
tests={'first glyph of line':lambda g,t:t.startswith(g),
       'first glyph of any word':lambda g,t:any(w.startswith(g) for w in t.split('.')),
       'last glyph of line':lambda g,t:t.endswith(g),
       'glyph occurs in line':lambda g,t:g in t.replace('.','')}
random.seed(0); n=len(pairs); print('pairs',n,'margin column:',' '.join(g for g,_ in pairs))
for name,f in tests.items():
    obs=sum(f(g,t) for g,t in pairs); G=[g for g,_ in pairs]; null=[]
    for _ in range(10000): random.shuffle(G); null.append(sum(f(g,t) for g,(_,t) in zip(G,pairs)))
    print(f'  {name:26s} obs {obs:2d}/{n}  shuffled mean {sum(null)/len(null):.1f}  p={sum(x>=obs for x in null)/len(null):.3f}')
