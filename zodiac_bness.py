import csv, re, collections, random, math, numpy as np, sys
random.seed(13)
src=sys.argv[1] if len(sys.argv)>1 else 'data/corpus.tsv'
rows=[r for r in csv.DictReader(open(src),delimiter='\t') if r['text']]
# 1. B-ness scorer from running text OUTSIDE the zodiac/astro/cosmo pages: glyph-bigram log-odds B vs A
def bigrams(w): 
    w='^'+w+'$'; return [w[i:i+2] for i in range(len(w)-1)]
cA=collections.Counter(); cB=collections.Counter()
for r in rows:
    if r['ltype'].startswith('P') and r['section'] in ('herbal','bio','stars','pharma','text'):
        for w in r['text'].split('.'):
            if w: (cA if r['lang']=='A' else cB if r['lang']=='B' else collections.Counter()).update(bigrams(w))
V=set(cA)|set(cB); nA=sum(cA.values()); nB=sum(cB.values())
lo={b:math.log((cB[b]+1)/(nB+len(V)))-math.log((cA[b]+1)/(nA+len(V))) for b in V}
def bness(w): 
    bg=bigrams(w); return sum(lo.get(b,0) for b in bg)/len(bg)
order=[('Pisces',['f70v2']),('AriesD',['f70v1']),('AriesL',['f71r']),('TaurusL',['f71v']),('TaurusD',['f72r1']),('Gemini',['f72r2']),('Cancer',['f72r3']),('Leo',['f72v3']),('Virgo',['f72v2']),('Libra',['f72v1']),('Scorpio',['f73r']),('Sagitt',['f73v'])]
def spearman(x,y):
    rx=np.argsort(np.argsort(x)); ry=np.argsort(np.argsort(y)); return np.corrcoef(rx,ry)[0,1]
def test(name, groups, nperm=5000):
    # groups: list (in sign order) of lists of scores
    means=[np.mean(g) for g in groups]; rho=spearman(range(len(groups)),means)
    allv=[x for g in groups for x in g]; sizes=[len(g) for g in groups]; null=[]
    for _ in range(nperm):
        random.shuffle(allv); k=0; mm=[]
        for n in sizes: mm.append(np.mean(allv[k:k+n])); k+=n
        null.append(spearman(range(len(groups)),mm))
    p=np.mean([abs(x)>=abs(rho) for x in null])
    print(f'  {name:34s} per-sign mean B-ness: '+' '.join(f'{m:+.2f}' for m in means)+f'   rho={rho:+.2f}  p={p:.4f}  (n={sum(sizes)})')
print(f'B-ness scorer trained on A={nA} / B={nB} bigrams; sanity: mean score of A text words {np.mean([bness(w) for r in rows if r["lang"]=="A" and r["ltype"].startswith("P") for w in r["text"].split(".") if w]):+.2f}, B text words {np.mean([bness(w) for r in rows if r["lang"]=="B" and r["ltype"].startswith("P") for w in r["text"].split(".") if w]):+.2f}')
print('signs: '+' '.join(f'{s[:5]:>5s}' for s,_ in order))
lab=[[bness(w) for f in fs for r in rows if r['folio']==f and r['ltype'].startswith('L') for w in r['text'].split('.') if w] for s,fs in order]
ring=[[bness(w) for f in fs for r in rows if r['folio']==f and not r['ltype'].startswith('L') for w in r['text'].split('.') if w] for s,fs in order]
test('LABELS (all)', lab); test('RING TEXT (all)', ring)
# first-ring-only labels: use raw file to find ring starts ('@' prefix) -- approximate via corpus order: first run of L loci per page
if src=='data/corpus.tsv':
    first=[]
    for s,fs in order:
        g=[]; 
        for f in fs:
            seen=False
            for line in open('data/ZL3b-n.txt',encoding='utf-8',errors='replace'):
                m=re.match(r'^<'+f+r'\.(\d+),([@&+=*~])L\w>\s*(?:<![^>]*>)?(.*)$',line)
                if not m: continue
                if m.group(2)=='@':
                    if seen: break
                    seen=True
                t=re.sub(r'<[^>]*>|\{[^}]*\}','',m.group(3)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t).replace(',','.').replace('?','')
                g+= [bness(w) for w in t.split('.') if w]
        first.append(g)
    test('LABELS (outer ring only)', first)
# labels vs ring text on the same page: difference per sign
print('  label minus ring mean per sign: '+' '.join(f'{np.mean(a)-np.mean(b):+.2f}' for a,b in zip(lab,ring)))
