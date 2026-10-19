"""Does a label's word form occur in the running text of its own page more often than in the running text of another page
of the same section? Null: labels reassigned to random pages of the same section (5000 draws)."""
import csv, collections, random
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
txt=collections.defaultdict(collections.Counter); labels=[]; sec={}
for r in rows:
    ws=[w for w in r['text'].split('.') if w and w.isalpha()]
    sec[r['folio']]=r['section']
    if r['ltype'][0]=='P' or r['ltype'][0] in 'CR': txt[r['folio']].update(ws)
    elif r['ltype'][0]=='L':
        for w in ws:
            if len(w)>=3: labels.append((r['folio'],w))
pages_by_sec=collections.defaultdict(list)
for f in txt:
    if sum(txt[f].values())>=20: pages_by_sec[sec[f]].append(f)
random.seed(1)
print(f'{"section":8s} {"labels":>6s} {"in own page text":>17s} {"random page":>12s} {"p":>6s}   matches')
for s,P in sorted(pages_by_sec.items()):
    L=[(f,w) for f,w in labels if sec.get(f)==s and f in txt]
    if len(L)<15 or len(P)<4: continue
    obs=sum(txt[f][w]>0 for f,w in L); null=[]
    for _ in range(5000): null.append(sum(txt[random.choice([p for p in P if p!=f] or P)][w]>0 for f,w in L))
    m=sum(null)/len(null)
    print(f'{s:8s} {len(L):6d} {obs:17d} {m:12.1f} {sum(x>=obs for x in null)/len(null):6.3f}   {", ".join(sorted({w for f,w in L if txt[f][w]>0}))[:120]}')
# baseline: same ratio for running-text words (3+ glyphs), each tested against the REST of its own page's text vs a random page
print('\nlocality baseline: text words, own page (minus the word itself) vs random page of the same section')
for s,P in sorted(pages_by_sec.items()):
    W=[(f,w) for f in P for w,c in txt[f].items() for _ in range(c) if len(w)>=3]
    if len(W)<50: continue
    random.shuffle(W); W=W[:2000]
    own=sum((txt[f][w]-1)>0 for f,w in W); rnd=sum(sum(txt[random.choice([p for p in P if p!=f])][w]>0 for f,w in W) for _ in range(20))/20
    L=[(f,w) for f,w in labels if sec.get(f)==s and f in txt]
    lo=sum(txt[f][w]>0 for f,w in L); lr=sum(sum(txt[random.choice([p for p in P if p!=f] or P)][w]>0 for f,w in L) for _ in range(200))/200
    print(f'  {s:8s} text words own/random {own/len(W):.3f}/{rnd/len(W):.3f} = {own/max(rnd,1e-9):.2f}x   labels {lo}/{lr:.1f} = {lo/max(lr,1e-9):.2f}x')
