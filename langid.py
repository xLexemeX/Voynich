"""Hauer & Kondrak (2016)-style language identification of the Voynich text, run also on meaningless text.
Two of their measures: sorted letter-frequency profile, and word decomposition patterns (e.g. 'abca')."""
import re, collections, random, unicodedata, math
exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0])   # gen(), lines
random.seed(5)
def txt(path,it=False):
    t=open(path,encoding='utf-8',errors='replace').read().lower()
    t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode() if it else t
    return re.findall(r'[a-z]+',t)[:30000]
def heb(path):
    H='אבגדהוזחטיכלמנסעפצקרשת'; F={'ך':'כ','ם':'מ','ן':'נ','ף':'פ','ץ':'צ'}
    s=re.sub(r'&[a-z]+;',' ',open(path,encoding='utf-8').read())
    return [w for w in (''.join(chr(97+H.index(F.get(c,c))) for c in tok if F.get(c,c) in H) for tok in s.split()) if w]
REF={'Latin':txt('data/ref/latin_pliny.txt'),'Italian':txt('data/ref/italian_dante.txt',True),'German':txt('data/ref/german_faust.txt',True),
     'English':txt('data/ref/english_austen.txt'),'Hebrew':heb('data/ref/hebrew_genesis.txt')}
G=re.compile(r'cth|ckh|cph|cfh|ch|sh|[a-z]')
vw=[G.findall(w) for l in lines for w in l]
def markov_words(n):
    tr=collections.defaultdict(list); flat=[w for l in lines for w in l]
    for a,b in zip(flat,flat[1:]): tr[a].append(b)
    out=[random.choice(flat)]
    while len(out)<n: out.append(random.choice(tr[out[-1]]) if tr[out[-1]] else random.choice(flat))
    return out
def glyph_shuffled():  # same glyphs, randomly redistributed among words of the same lengths
    pool=[g for w in vw for g in w]; random.shuffle(pool); out=[]; i=0
    for w in vw: out.append(pool[i:i+len(w)]); i+=len(w)
    return out
TEST={'Voynich':vw,'slot self-citation (meaningless)':[G.findall(w) for l in gen(len(lines)) for w in l],
      'word Markov chain (meaningless)':[G.findall(w) for w in markov_words(len(vw))],'Voynich glyphs shuffled across words':glyph_shuffled()}
def sorted_profile(ws,k=30):
    c=collections.Counter(g for w in ws for g in w); n=sum(c.values()); v=sorted((x/n for x in c.values()),reverse=True)[:k]; return v+[0]*(k-len(v))
def patterns(ws):
    c=collections.Counter()
    for w in ws:
        m={}; c[''.join(m.setdefault(g,chr(97+len(m))) for g in w)]+=1
    n=sum(c.values()); return {k:v/n for k,v in c.items()}
def l1(a,b): return sum(abs(x-y) for x,y in zip(a,b))
def dpf(a,b): return sum(abs(a.get(k,0)-b.get(k,0)) for k in set(a)|set(b))
RP={k:(sorted_profile([list(w) for w in v]),patterns([list(w) for w in v])) for k,v in REF.items()}
for name,ws in TEST.items():
    sp,pt=sorted_profile(ws),patterns(ws)
    r1=sorted(RP,key=lambda k:l1(sp,RP[k][0])); r2=sorted(RP,key=lambda k:dpf(pt,RP[k][1]))
    print(f'{name:38s} letter-frequency profile: {" > ".join(r1[:3])} | decomposition patterns: {" > ".join(r2[:3])}')
    print('   pattern distances: '+', '.join(f'{k} {dpf(pt,RP[k][1]):.3f}' for k in r2)+f'; mean word length {sum(map(len,ws))/len(ws):.2f}; share of words with a repeated glyph {sum(len(set(w))<len(w) for w in ws)/len(ws):.2f}')
for k,v in REF.items(): print(f'reference {k:8s} mean word length {sum(map(len,v))/len(v):.2f}; share with a repeated letter {sum(len(set(w))<len(w) for w in v)/len(v):.2f}')
