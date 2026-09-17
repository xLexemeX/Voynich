import collections, math, csv, re, random, unicodedata
random.seed(1)
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def stats(name, toks, N=38000):
    toks = toks[:N] if len(toks)>=N else toks
    types=collections.Counter(toks)
    text=' '.join(toks)
    h1=H(collections.Counter(text)); h2=H(collections.Counter(text[i:i+2] for i in range(len(text)-1)))-h1
    # h2 without spaces
    t2=''.join(toks); h1n=H(collections.Counter(t2)); h2n=H(collections.Counter(t2[i:i+2] for i in range(len(t2)-1)))-h1n
    hap=sum(1 for v in types.values() if v==1)/len(types)
    ml=sum(map(len,toks))/len(toks); sd=(sum((len(t)-ml)**2 for t in toks)/len(toks))**.5
    rep=sum(1 for a,b in zip(toks,toks[1:]) if a==b)/len(toks)
    top=types.most_common(1)[0][1]/len(toks)
    print(f'{name:22s} tok {len(toks):6d} types {len(types):5d} TTR {len(types)/len(toks):.3f} hapax {hap:.2f} len {ml:.2f}±{sd:.2f} h1 {h1:.2f} h2 {h2:.2f} h2(nospace) {h2n:.2f} rep {rep:.4f} top1 {top:.3f} alpha {len(collections.Counter(t2))}')
def clean(path, keep):
    s=open(path,encoding='utf-8',errors='replace').read().lower()
    s=unicodedata.normalize('NFKD',s)
    return re.findall(keep, s)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
stats('voynich EVA', voy)
stats('voynich A', [w for r in rows if r['lang']=='A' for w in r['text'].split('.') if w])
stats('voynich B', [w for r in rows if r['lang']=='B' for w in r['text'].split('.') if w])
# alternative tokenizations: merge common digraphs into single symbols
def retok(w):
    for a,b in [('cth','C'),('ckh','K'),('cph','P'),('cfh','F'),('ch','H'),('sh','S'),('qo','Q'),('iin','N'),('in','M'),('ee','E'),('ai','A')]:
        w=w.replace(a,b)
    return w
stats('voynich merged-glyph', [retok(w) for w in voy])
stats('latin pliny', clean('data/ref/latin_pliny.txt', r'[a-z]+'))
stats('italian dante', clean('data/ref/italian_dante.txt', r'[a-z]+'))
stats('german faust', clean('data/ref/german_faust.txt', r'[a-z]+'))
stats('english austen', clean('data/ref/english_austen.txt', r'[a-z]+'))
stats('hebrew genesis', re.findall(r'[א-ת]+', open('data/ref/hebrew_genesis.txt').read()))
# scrambled control: shuffle voynich words
sh=voy[:]; random.shuffle(sh); stats('voynich shuffled words', sh)
