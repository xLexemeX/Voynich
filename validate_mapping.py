"""Check a proposed EVA-unit -> letters table against controls.
usage: python3 validate_mapping.py mappings/X.json [n_null]
1. dictionary hits (words>=3 letters, e/i merged, doubles collapsed) vs tables reshuffled within vowel / consonant values
2. held-out word-order gain: Latin letter 4-gram score of decoded text in real word order minus shuffled word order, vs the same for reshuffled tables
Only words fully covered by the table are used."""
import sys, json, re, csv, random, collections, unicodedata, numpy as np
cfg=json.load(open(sys.argv[1])); NN=int(sys.argv[2]) if len(sys.argv)>2 else 200; MAP=cfg['map']
RX=re.compile('|'.join(sorted(map(re.escape,MAP),key=len,reverse=True)))
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
lines=[[w for w in r['text'].split('.') if re.fullmatch(r'[a-z]+',w)] for r in rows]
seg={}
for l in lines:
    for w in l:
        if w not in seg: s=RX.findall(w); seg[w]=s if ''.join(s)==w else None
lines=[[w for w in l if seg[w]] for l in lines]; toks=[w for l in lines for w in l]
allt=sum(len([w for w in r['text'].split('.') if w]) for r in rows)
def norm(s): s=s.replace('e','i').replace('j','i').replace('v','u').replace('y','i').replace('k','c'); return re.sub(r'(.)\1+',r'\1',s)
def words(path,it=False):
    t=open(path,encoding='utf-8',errors='replace').read().lower()
    if it: t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode()
    return re.findall(r'[a-z]+',t)
lat=words('data/ref/latin_pliny.txt')+words('data/ref/latin_vulgate.txt'); ita=words('data/ref/italian_dante.txt',True)
LEX={'Latin':{norm(w) for w in lat if len(w)>=3},'Italian':{norm(w) for w in ita if len(w)>=3}}
# letter 4-gram LM on normalised Latin (Pliny), alphabet after norm
A='abcdfghilmnopqrstuxz'; aid={c:i for i,c in enumerate(A)}; K=len(A)
t=np.array([aid[c] for c in norm(' '.join(lat[:200000])) if c in aid])
c4=np.bincount(((t[:-3]*K+t[1:-2])*K+t[2:-1])*K+t[3:],minlength=K**4)+.1; c3=np.bincount((t[:-2]*K+t[1:-1])*K+t[2:],minlength=K**3)+.1*K
LP=np.log(c4/np.repeat(c3,K))
def dec(M,w): return norm(''.join(M[u] for u in seg[w]))
def lmscore(M,seq):
    s=np.array([aid[c] for c in ''.join(dec(M,w) for w in seq) if c in aid]); 
    return LP[((s[:-3]*K+s[1:-2])*K+s[2:-1])*K+s[3:]].mean()
tf=collections.Counter(toks); half=toks[len(toks)//2:]; rng=random.Random(0)
def evaluate(M):
    r={}
    for k,L in LEX.items():
        h=n=0
        for w,c in tf.items():
            d=dec(M,w)
            if len(d)>=3: n+=c; h+=c*(d in L)
        r[k]=h/n
    sh=half[:]; g=[]
    for _ in range(5): rng.shuffle(sh); g.append(lmscore(M,sh))
    r['order gain']=lmscore(M,half)-sum(g)/len(g); return r
VOW=set('aeiouy')
keys=list(MAP); V=[k for k in keys if all(ch in VOW for ch in MAP[k])]; C=[k for k in keys if all(ch not in VOW for ch in MAP[k])]
o=evaluate(MAP); null=[]
for _ in range(NN):
    M=dict(MAP); vv=[MAP[k] for k in V]; cc=[MAP[k] for k in C]; rng.shuffle(vv); rng.shuffle(cc); M.update(zip(V,vv)); M.update(zip(C,cc)); null.append(evaluate(M))
print(f"{cfg['source']}\n  tokens fully covered by the table: {len(toks)} of {allt} ({len(toks)/allt:.1%}); reshuffled within {len(V)} vowel-valued and {len(C)} consonant-valued units; {NN} draws")
print('  sample:', ' '.join(dec(MAP,w) for w in toks[:20]))
for k in o:
    x=[n[k] for n in null]; print(f'  {k:11s} proposed {o[k]:+.4f} | reshuffled mean {np.mean(x):+.4f} max {max(x):+.4f} | p = {sum(v>=o[k] for v in x)/len(x):.3f}')
