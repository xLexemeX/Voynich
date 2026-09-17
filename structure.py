import collections, csv, re, random, itertools, math
random.seed(2)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
types=collections.Counter(voy)
print('=== 1. Stolfi-style word paradigm coverage')
# crust-mantle-core approximated by regex (my own build, refined iteratively)
pat = re.compile(r'^(q?o|q?)?(k|t|p|f|ck|ct|cp|cf|cth|ckh|cph|cfh|ch|sh|d|s|l|r|y)?(e{0,3}|o|a)?(k|t|p|f|cth|ckh|cph|cfh|ch|sh|d|s|l|r)?(e{0,3}|o|a|ai|aii|aiii|oi|oii)?(n|m|l|r|y|dy|d|s|g|in|iin)?$')
cov=sum(c for w,c in types.items() if pat.match(w)); print(f'tokens matched by simple slot regex: {cov/len(voy):.1%}; types: {sum(1 for w in types if pat.match(w))/len(types):.1%}')
print('unmatched frequent words:', [w for w,c in types.most_common(400) if not pat.match(w)][:40])

print('\n=== 2. Glyph position profile (fraction of occurrences at word start / middle / end)')
pos=collections.defaultdict(lambda:[0,0,0])
for w in voy:
    for i,ch in enumerate(w):
        pos[ch][0 if i==0 else 2 if i==len(w)-1 else 1]+=1
for ch,(a,b,c) in sorted(pos.items(), key=lambda x:-sum(x[1])):
    n=a+b+c
    if n>50: print(f'  {ch}: n={n:5d} start {a/n:.2f} mid {b/n:.2f} end {c/n:.2f}')

print('\n=== 3. Within-word bigram determinism: for each glyph, prob of most likely next glyph')
nxt=collections.defaultdict(collections.Counter)
for w in voy:
    for a,b in zip(w,w[1:]+'#'): nxt[a][b]+=1
for a,c in sorted(nxt.items(), key=lambda x:-sum(x[1].values())):
    n=sum(c.values())
    if n>200: print(f'  {a}-> {" ".join(f"{b}:{v/n:.2f}" for b,v in c.most_common(4))}')

print('\n=== 4. Edit-distance-1 neighbourhood density (types with freq>=2)')
def neigh(wordset):
    ws=set(wordset); cnt=0; tot=0
    alpha=set(''.join(ws))
    for w in ws:
        tot+=1; found=0
        for i in range(len(w)):
            if w[:i]+w[i+1:] in ws: found+=1
            for a in alpha:
                if a!=w[i] and w[:i]+a+w[i+1:] in ws: found+=1
        for i in range(len(w)+1):
            for a in alpha:
                if w[:i]+a+w[i:] in ws: found+=1
        cnt+=found
    return cnt/tot
def clean(path):
    s=open(path,encoding='utf-8',errors='replace').read().lower(); return re.findall(r'[a-z]+',s)
for name,toks in [('voynich',voy),('latin',clean('data/ref/latin_pliny.txt')[:38000]),('italian',clean('data/ref/italian_dante.txt')[:38000]),('german',clean('data/ref/german_faust.txt')[:38000])]:
    c=collections.Counter(toks); ws=[w for w,v in c.items() if v>=2]
    print(f'  {name:8s} types(f>=2)={len(ws):5d} mean #neighbours at edit-dist 1 = {neigh(ws):.2f}')

print('\n=== 5. Timm self-citation test: similarity of a word to words on the SAME line vs a random line')
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1): cur.append(min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
lines=[[w for w in r['text'].split('.') if w] for r in rows]; lines=[l for l in lines if len(l)>=3]
def mean_min_dist(pairs_fn, n=3000):
    tot=0; k=0
    for _ in range(n):
        w,others=pairs_fn()
        if not others: continue
        tot+=min(lev(w,o) for o in others); k+=1
    return tot/k
def same():
    l=random.choice(lines); i=random.randrange(len(l)); return l[i],[o for j,o in enumerate(l) if j!=i]
def rand():
    l=random.choice(lines); i=random.randrange(len(l)); o=random.choice(lines); return l[i],o[:len(l)-1]
print(f'  voynich: mean min edit distance to same-line words {mean_min_dist(same):.2f}  vs random-line words {mean_min_dist(rand):.2f}')
for name,path in [('latin','data/ref/latin_pliny.txt'),('italian','data/ref/italian_dante.txt')]:
    toks=clean(path)[:38000]; L=[toks[i:i+8] for i in range(0,len(toks),8)]
    lines_bak=lines; lines=L
    print(f'  {name:8s}: same-line {mean_min_dist(same):.2f} vs random-line {mean_min_dist(rand):.2f}')
    lines=lines_bak
