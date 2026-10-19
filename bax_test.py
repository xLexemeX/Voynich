"""Bax (2014) plant/star names: how page-specific are the EVA words he read as names?"""
import csv, collections
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
occ=collections.defaultdict(list); first={}
for r in rows:
    for i,w in enumerate(r['text'].split('.')):
        if w: occ[w].append((r['folio'],r['section'],r['ltype'][0]))
for r in rows:
    if r['ltype'].startswith('P') and r['folio'] not in first and r['section']=='herbal': first[r['folio']]=r['text'].split('.')[0]
anchors=[('kydainy','f2r','Centaurea, KNTəIRN'),('koaiin','f3v','hellebore, KAUR'),('kooiin','f29v','Nigella, KAUR (CHAR)'),
         ('keedey','f31r','cotton, KOOTON'),('keeredal','f41v','coriander, KOORATU'),('ksor','f27r','crocus, KSAR'),('oror','f16r','juniper, ARAR')]
herbal_pages={r['folio'] for r in rows if r['section']=='herbal'}
for w,page,gloss in anchors:
    o=occ.get(w,[]); pages=collections.Counter(f for f,_,_ in o); herb=[f for f in pages if f in herbal_pages]
    asfirst=[f for f,x in first.items() if x==w]
    print(f'{w:9s} ({gloss:22s} on {page}): {len(o):3d} tokens on {len(pages):2d} folios, {len(herb):2d} herbal; own page {pages[page]}; opens herbal pages {asfirst}')
    print('           other folios:', ' '.join(sorted(f for f in pages if f!=page))[:150])
# the K: page-initial gallows. How often does a herbal page open with k, and how common is k- word-initially elsewhere?
toks=[(w,r) for r in rows if r['ltype'].startswith('P') for i,w in enumerate(r['text'].split('.')) if w]
c=collections.Counter(x[0] for x in first.values())
print('herbal page-first word initial glyph:', dict(c.most_common(6)), f'of {len(first)}')
mid=[w for r in rows if r['ltype'].startswith('P') and r['section']=='herbal' for w in r['text'].split('.')[1:] if w]
print(f'k-initial share: herbal page-first words {c["k"]/len(first):.2f}; herbal non-line-initial words {sum(w[0]=="k" for w in mid)/len(mid):.3f}')
allw=collections.Counter(w for w,_ in toks)
print('stripped of the opening gallows:')
for w,page,gloss in anchors[:6]:
    s=w[1:]; print(f'  {w:9s} -> {s:8s} {allw[s]:4d} tokens; same core after p/t/f: ' + ', '.join(f'{g+s}:{allw[g+s]}' for g in 'ptf' if allw[g+s]))
