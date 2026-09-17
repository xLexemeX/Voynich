"""Macro-class sequence grammar along lines: classes by ending. Observed/expected class bigrams and positional distribution."""
import collections, csv, re, random
random.seed(10)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
lines=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P') and len(r['text'].split('.'))>=5]
def cls(w):
    if re.search(r'(edy|eey|ey|dy)$',w): return 'EDY'
    if w.endswith('y'): return 'Y'
    if re.search(r'(aiin|ain|iin|in|n|m)$',w): return 'N'
    if re.search(r'(ol|al|l)$',w): return 'L'
    if re.search(r'(or|ar|r)$',w): return 'R'
    return 'X'
seq=[[cls(w) for w in l] for l in lines]
pairs=[(a,b) for s in seq for a,b in zip(s,s[1:])]
pc=collections.Counter(pairs); fa=collections.Counter(p[0] for p in pairs); fb=collections.Counter(p[1] for p in pairs); N=len(pairs)
K=['EDY','Y','N','L','R','X']
print('class frequencies:', {k:round(fa[k]/N,3) for k in K})
print('observed/expected for (class_i -> class_i+1):')
print('        '+' '.join(f'{k:>6s}' for k in K))
for a in K: print(f'{a:>6s}  '+' '.join(f'{pc[(a,b)]/(fa[a]*fb[b]/N):6.2f}' for b in K))
print('\nshuffled-within-line control (should be ~1.00 everywhere):')
sh=[]
for s in seq: t=s[:]; random.shuffle(t); sh.append(t)
pairs2=[(a,b) for s in sh for a,b in zip(s,s[1:])]; pc2=collections.Counter(pairs2)
for a in K: print(f'{a:>6s}  '+' '.join(f'{pc2[(a,b)]/(fa[a]*fb[b]/N):6.2f}' for b in K))
print('\nclass share by relative position in line (5 bins):')
bins=[collections.Counter() for _ in range(5)]
for s in seq:
    for i,c in enumerate(s): bins[min(4,int(5*i/len(s)))][c]+=1
for i,b in enumerate(bins):
    n=sum(b.values()); print(f'  bin {i}: '+' '.join(f'{k}:{b[k]/n:.2f}' for k in K))
print('\nrun lengths of same class (observed vs shuffled):')
def runs(S):
    c=collections.Counter()
    for s in S:
        r=1
        for a,b in zip(s,s[1:]):
            if a==b: r+=1
            else: c[r]+=1; r=1
        c[r]+=1
    return c
ro=runs(seq); rs=runs(sh); tot=sum(ro.values())
print('  len:', ' '.join(f'{k}:{ro[k]/tot:.3f}/{rs[k]/sum(rs.values()):.3f}' for k in range(1,7)))
