"""Cheshire (2017/2019) sign values applied mechanically; Romance dictionary coverage vs the same values randomly reassigned.
Values read from Cheshire 2017 (lingbuzz 003737) Figs 1-27, mapped to EVA."""
import csv, re, random, collections, unicodedata
MAP={'ckh':'ele','cth':'eme','cph':'epe','cfh':'eque','ch':'e','sh':'ae','ii':'u',
     'o':'o','a':'a','y':'a','q':'d','e':'e','i':'i','n':'s','m':'s','k':'l','t':'m','p':'p','f':'qu','d':'n','l':'r','r':'s','s':'t'}
UNITS=sorted(MAP,key=len,reverse=True); RX=re.compile('|'.join(UNITS))
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
words=[w for r in rows for w in r['text'].split('.') if w and re.fullmatch(r'[a-z]+',w)]
seg={w:RX.findall(w) for w in set(words)}
seg={w:s for w,s in seg.items() if ''.join(s)==w}            # only words fully covered by the table
toks=[w for w in words if w in seg]
def norm(s):  # Cheshire: e/i interchangeable, no double consonants
    s=s.replace('e','i').replace('j','i').replace('v','u').replace('y','i'); return re.sub(r'(.)\1+',r'\1',s)
def lex(path,it=False):
    t=open(path,encoding='utf-8',errors='replace').read().lower()
    if it: t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
    return {norm(w) for w in re.findall(r'[a-z]+',t) if len(w)>=3}
LEX={'Latin':lex('data/ref/latin_pliny.txt'),'Italian':lex('data/ref/italian_dante.txt',True)}
LEX['either']=LEX['Latin']|LEX['Italian']
def cover(M,L):
    hit=n=0; ht=nt=0
    for w,c in tf.items():
        d=norm(''.join(M[u] for u in seg[w]))
        if len(d)>=3: n+=c; nt+=1; h=d in L; hit+=c*h; ht+=h
    return hit/n, ht/nt
tf=collections.Counter(toks)
print(f'{len(toks)} of {len(words)} paragraph tokens fully covered by the table; {len(tf)} types')
ex=[w for w,_ in tf.most_common(25)]
print('commonest words as read:', ', '.join(f"{w}={''.join(MAP[u] for u in seg[w])}" for w in ex))
random.seed(0); keys=list(MAP); vals=[MAP[k] for k in keys]
for name,L in LEX.items():
    o=cover(MAP,L); null=[]
    for _ in range(300):
        v=vals[:]; random.shuffle(v); null.append(cover(dict(zip(keys,v)),L))
    nt=[x[0] for x in null]; ny=[x[1] for x in null]
    print(f'{name:8s} tokens in dictionary {o[0]:.3f} (random reassignment {sum(nt)/len(nt):.3f}, max {max(nt):.3f}, p={sum(x>=o[0] for x in nt)/len(nt):.3f}); types {o[1]:.3f} (random {sum(ny)/len(ny):.3f}, p={sum(x>=o[1] for x in ny)/len(ny):.3f})')
# class-preserving null: shuffle vowel values among vowel-valued glyphs and consonant values among consonant-valued glyphs; composites fixed
V=[k for k in keys if MAP[k] in ('o','a','e','i','u','ae')]; C=[k for k in keys if k not in V and len(MAP[k])<=2 and k not in ('ckh','cth','cph','cfh')]
print('vowel class', V, 'consonant class', C)
for name,L in LEX.items():
    o=cover(MAP,L); null=[]
    for _ in range(300):
        M=dict(MAP); vv=[MAP[k] for k in V]; cc=[MAP[k] for k in C]; random.shuffle(vv); random.shuffle(cc)
        M.update(zip(V,vv)); M.update(zip(C,cc)); null.append(cover(M,L))
    nt=[x[0] for x in null]; ny=[x[1] for x in null]
    print(f'{name:8s} class-preserving null: tokens {sum(nt)/len(nt):.3f} max {max(nt):.3f} p={sum(x>=o[0] for x in nt)/len(nt):.3f}; types {sum(ny)/len(ny):.3f} max {max(ny):.3f} p={sum(x>=o[1] for x in ny)/len(ny):.3f}')
