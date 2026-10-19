"""Montemurro & Zanette (2013) word-arrangement information I(s): how much a word's position among text parts of size s is
non-random. Voynich vs the slot self-citation generator (generators2.gen) vs Latin. Shuffle baseline per text."""
import math, random, collections, re
exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0])   # gen(), lines
random.seed(3)
def info(words, s, nsh=5):
    N=len(words)//s*s; words=words[:N]; P=N//s
    def ent(ws):
        pos=collections.defaultdict(lambda: collections.Counter())
        for i,w in enumerate(ws): pos[w][i//s]+=1
        return {w:-sum(c/sum(cc.values())*math.log2(c/sum(cc.values())) for c in cc.values()) for w,cc in pos.items()}
    cnt=collections.Counter(words); H=ent(words); Hs=collections.Counter()
    for _ in range(nsh):
        sh=words[:]; random.shuffle(sh)
        for w,h in ent(sh).items(): Hs[w]+=h/nsh
    return sum(cnt[w]/N*(Hs[w]-H[w]) for w in cnt if cnt[w]>=2)
voy=[w for l in lines for w in l]
g=[w for l in gen(len(lines)) for w in l]
lat=re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower())[:len(voy)]
print('text sizes', len(voy), len(g), len(lat))
for s in (100,500,1000,2000,4000):
    print(f's={s:5d}  Voynich {info(voy,s):.3f}  self-citation generator {info(g,s):.3f}  Latin (Pliny) {info(lat,s):.3f}  bits/word')
# within homogeneous stretches: generator retrained on the same subset (slot tables and line lengths)
import csv
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
for name,cond in [('herbal, language A',lambda r:r['section']=='herbal' and r['lang']=='A'),('language B, all sections',lambda r:r['lang']=='B')]:
    sub=[[w for w in r['text'].split('.') if w] for r in rows if cond(r)]
    lines=sub; P.clear(); C.clear(); S.clear()
    for w in (w for l in sub for w in l):
        m=pat.match(w)
        if m and m.group(2): P[m.group(1) or '']+=1; C[m.group(2)]+=1; S[m.group(3) or '']+=1
    v=[w for l in sub for w in l]; gg=[w for l in gen(len(sub)) for w in l]
    for s in (500,1000,2000):
        print(f'{name:26s} s={s:5d}  Voynich {info(v,s):.3f}  generator {info(gg,s):.3f}  ({len(v)} vs {len(gg)} words)')
