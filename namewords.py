"""Name-like words: word forms that occur 2+ times on one page/chapter and on no other page of the same text.
Real herbal (Macer Floridus, 77 chapters) vs Voynich herbal A pages vs the copying generator laid out on the same pages."""
import json, re, csv, collections, random
exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0])   # gen()
random.seed(4)
d=json.load(open('data/ext_herbal/dvh.json')); t=list(d['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
parts=re.split(r'==\s*[IVXLC]+\.\s*([^=]+?)\s*==',t)
chap=[(parts[i].strip(' .').lower(), re.findall(r'[a-z]+',re.sub(r'\{\{[^}]*\}\}|<[^>]+>','',parts[i+1]).lower())) for i in range(1,len(parts),2)]
def stem(w): return w[:5]   # crude Latin stem: first 5 letters
def namelike(pages, key=lambda w:w):
    occ=collections.defaultdict(collections.Counter)
    for i,ws in enumerate(pages):
        for w in ws: occ[key(w)][i]+=1
    per=[0]*len(pages)
    for w,c in occ.items():
        if len(c)==1:
            (i,n),=c.items()
            if n>=2: per[i]+=1
    return per
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P') and r['section']=='herbal' and r['lang']=='A']
pg=collections.OrderedDict()
for r in rows: pg.setdefault(r['folio'],[]).extend(w for w in r['text'].split('.') if w)
V=list(pg.values()); n=sum(map(len,V))
M=[ws for _,ws in chap]
# generator text cut into pages of the Voynich page lengths
g=[w for l in gen(2*len(rows)) for w in l]; G=[]; k=0
for ws in V: G.append(g[k:k+len(ws)]); k+=len(ws)
def report(name,P,key=lambda w:w):
    per=namelike(P,key); L=[len(p) for p in P]
    print(f'{name:44s} pages {len(P):3d}, words/page {sum(L)/len(L):5.0f}; pages with >=1 name-like word {sum(x>0 for x in per)/len(P):.2f}; mean per page {sum(per)/len(P):.2f}')
report('Macer chapters, word forms',M)
report('Macer chapters, 5-letter stems',M,stem)
hits=sum(any(stem(w)==stem(re.sub('[^a-z]','',h.split()[0])) for w in ws) for h,ws in chap)
print(f'   Macer: chapter title (plant name) occurs in its own chapter: {hits}/{len(chap)}')
report('Voynich herbal A pages, word forms',V)
report('generator, same page lengths, word forms',G)
Mc=[ws[:84] for ws in M if len(ws)>=84]
report('Macer chapters cut to 84 words, word forms',Mc)
report('Macer chapters cut to 84 words, stems',Mc,stem)
# Voynich with a looser key: drop a word-initial gallows (§45) so pchol/kchol/tchol count as one form
report('Voynich herbal A, opening gallows stripped',V,lambda w:w[1:] if len(w)>3 and w[0] in 'ptkf' else w)
# Italian prose-like reference: Dante cut into 84-word pages (not a herbal; checks language effects)
import unicodedata
it=re.findall(r'[a-z]+',unicodedata.normalize('NFKD',open('data/ref/italian_dante.txt',encoding='utf-8').read().lower()).encode('ascii','ignore').decode())
report('Dante, 95 pages of 84 words',[it[i*84:(i+1)*84] for i in range(95)])
def loose(w):
    w=re.sub(r'^[qoyptkfsd]+','',w); w=re.sub(r'[ymgn]$','',w); return w if len(w)>=2 else '#'+w
report('Voynich herbal A, loose key (prefix q/o/y/s/d/gallows and final y/m/g/n removed)',V,loose)
report('generator, same loose key',G,loose)
report('Macer cut to 84, 4-letter stems',Mc,lambda w:w[:4])
from math import comb
p=0.27; n=95; k=sum(x>0 for x in namelike(V)); print(f'binomial P(<= {k} of {n} | rate {p}) = {sum(comb(n,i)*p**i*(1-p)**(n-i) for i in range(k+1)):.1e}')
def decomp(name,P):
    occ=collections.defaultdict(collections.Counter)
    for i,ws in enumerate(P):
        for w in ws: occ[w][i]+=1
    rep=excl=0
    for i,ws in enumerate(P):
        for w,c in collections.Counter(ws).items():
            if c>=2: rep+=1; excl+= len(occ[w])==1
    print(f'{name:34s} words repeated within a page: {rep/len(P):.2f} per page; of these, found on no other page: {excl/max(rep,1):.3f}')
decomp('Macer cut to 84 words',Mc); decomp('Dante, 84-word pages',[it[i*84:(i+1)*84] for i in range(95)]); decomp('Voynich herbal A',V); decomp('generator',G)
