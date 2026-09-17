import collections, csv, re, random, math
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
c=collections.Counter(voy)
print('=== 1. Sukhotin vowel/consonant algorithm on EVA glyphs (and on merged glyphs)')
def sukhotin(words):
    alpha=sorted(set(''.join(words)))
    idx={a:i for i,a in enumerate(alpha)}; n=len(alpha)
    M=[[0]*n for _ in alpha]
    for w in words:
        for a,b in zip(w,w[1:]):
            if a!=b: M[idx[a]][idx[b]]+=1; M[idx[b]][idx[a]]+=1
    rows_=[sum(M[i]) for i in range(n)]; vowels=[]; cons=set(range(n))
    while True:
        best=max(cons,key=lambda i:rows_[i])
        if rows_[best]<=0: break
        vowels.append(best); cons.remove(best)
        for i in cons: rows_[i]-=2*M[i][best]
    return [alpha[i] for i in vowels]
print('  EVA vowels found:', sukhotin([w for w in voy if re.fullmatch(r'[a-z]+',w)]))
def retok(w):
    for a,b in [('cth','C'),('ckh','K'),('cph','P'),('cfh','F'),('ch','H'),('sh','S'),('iin','N'),('in','M'),('ee','E')]:
        w=w.replace(a,b)
    return w
print('  merged-glyph vowels found:', sukhotin([retok(w) for w in voy if re.fullmatch(r'[a-z]+',w)]))
lat=re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower())[:38000]
print('  Latin control vowels found:', sukhotin(lat))

print('\n=== 2. Line-final -m: is it a positional variant of -n / -in / -iin?')
# compare stems: for words ending in "am"/"om", strip the m and see which endings the same stem takes elsewhere
ends=collections.defaultdict(collections.Counter)
for w in voy:
    m=re.match(r'^(.*?)(a|o)(m|n|in|iin|iiin|r|l|y)$',w)
    if m: ends[m.group(1)+m.group(2)][m.group(3)]+=1
mstems=[s for s,e in ends.items() if e['m']>=3]
tot=collections.Counter()
for s in mstems: tot.update({k:v for k,v in ends[s].items() if k!='m'})
print('  stems that take -m at least 3x; their other endings summed:', tot.most_common())
print('  examples:', [(s,dict(ends[s])) for s in mstems[:8]])

print('\n=== 3. Tally-like runs: distribution of i-runs and e-runs')
print('  i-runs:', collections.Counter(len(m) for w in voy for m in re.findall(r'i+',w)))
print('  e-runs:', collections.Counter(len(m) for w in voy for m in re.findall(r'e+',w)))
print('  what precedes i-runs:', collections.Counter(m.group(1) for w in voy for m in re.finditer(r'(.)i+',w)).most_common(5))
print('  what follows i-runs:', collections.Counter(m.group(1) for w in voy for m in re.finditer(r'i+(.|$)',w)).most_common(6))

print('\n=== 4. Section-by-section: does the word "language" drift smoothly (quire order) or jump? cosine similarity of glyph-bigram profiles per quire')
import numpy as np
q=collections.defaultdict(list)
for r in rows:
    if r['quire']: q[r['quire']]+= [w for w in r['text'].split('.') if w]
keys=sorted(q, key=lambda k:(len(k),k))
bg=sorted(set(w[i:i+2] for w in voy for i in range(len(w)-1)))
def prof(ws):
    cc=collections.Counter(w[i:i+2] for w in ws for i in range(len(w)-1)); v=np.array([cc[b] for b in bg],float); return v/np.linalg.norm(v)
P={k:prof(q[k]) for k in keys}
print('  quire: tokens, lang mix, similarity to quire A(1)')
langs={k:collections.Counter(r['lang'] for r in rows if r['quire']==k) for k in keys}
for k in keys: print(f'   {k:3s} {len(q[k]):6d} {dict(langs[k])} sim={P[k]@P[keys[0]]:.3f}')
