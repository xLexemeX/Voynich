import collections, csv, re, random, math
random.seed(4)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
def clean(path):
    s=open(path,encoding='utf-8',errors='replace').read().lower(); return re.findall(r'[a-z]+',s)
lat=clean('data/ref/latin_pliny.txt')[:38000]; ita=clean('data/ref/italian_dante.txt')[:38000]; eng=clean('data/ref/english_austen.txt')[:38000]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
print('=== 1. Word-order syntax: H(word) and conditional H(next|current), restricted to words with freq>=20 as context')
def wordH(toks):
    c=collections.Counter(toks); h1=H(c)
    pairs=collections.Counter(zip(toks,toks[1:])); ctx=collections.Counter(toks[:-1])
    hc=sum(v/len(toks)*-math.log2(v/ctx[a]) for (a,b),v in pairs.items())
    # MI between adjacent words
    return h1, hc, h1-hc
for name,t in [('voynich',voy),('latin',lat),('italian',ita),('english',eng)]:
    h1,hc,mi=wordH(t); sh=t[:]; random.shuffle(sh); _,hcs,mis=wordH(sh)
    print(f'  {name:8s} H(word)={h1:.2f}  H(next|cur)={hc:.2f}  MI={mi:.2f}   shuffled MI (finite-sample floor)={mis:.2f}   excess MI={mi-mis:.2f}')

print('\n=== 2. Similarity decay with line distance (mean Jaccard of word sets, lines i and i+k, same folio)')
byf=collections.defaultdict(list)
for r in rows:
    if r['ltype'].startswith('P'): byf[r['folio']].append(set(w for w in r['text'].split('.') if w))
def decay(folios, K=10):
    out=[]
    for k in range(1,K+1):
        s=0;n=0
        for ls in folios:
            for i in range(len(ls)-k):
                a,b=ls[i],ls[i+k]
                if a and b: s+=len(a&b)/len(a|b); n+=1
        out.append(s/n if n else 0)
    return out
print('  voynich :', ' '.join(f'{x:.3f}' for x in decay(list(byf.values()))))
for name,t in [('latin',lat),('italian',ita)]:
    L=[[set(t[j:j+8]) for j in range(i,i+160,8)] for i in range(0,len(t)-160,160)]
    print(f'  {name:8s}:', ' '.join(f'{x:.3f}' for x in decay(L)))

print('\n=== 3. Zipf exponent (log-log slope, ranks 10-1000)')
import numpy as np
for name,t in [('voynich',voy),('latin',lat),('italian',ita),('english',eng)]:
    f=np.array(sorted(collections.Counter(t).values(),reverse=True)); r=np.arange(1,len(f)+1)
    sl=np.polyfit(np.log(r[9:1000]),np.log(f[9:1000]),1)[0]
    print(f'  {name:8s} zipf slope {sl:.2f}')

print('\n=== 4. Are the top-50 words near-variants of each other? (# pairs at edit distance 1)')
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1): cur.append(min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
for name,t in [('voynich',voy),('latin',lat),('italian',ita),('english',eng)]:
    top=[w for w,_ in collections.Counter(t).most_common(50)]
    n=sum(1 for i in range(50) for j in range(i+1,50) if lev(top[i],top[j])==1)
    print(f'  {name:8s} {n} of 1225 pairs')

print('\n=== 5. Currier A vs B on the SAME section (herbal): top words')
for lang in 'AB':
    t=[w for r in rows if r['section']=='herbal' and r['lang']==lang for w in r['text'].split('.') if w]
    print(f'  herbal-{lang} ({len(t)} tokens):', ' '.join(w for w,_ in collections.Counter(t).most_common(15)))
