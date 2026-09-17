import collections, csv, re, random, math, itertools
random.seed(3)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
voy=[w for r in rows for w in r['text'].split('.') if w]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def h2(toks):
    t=' '.join(toks); h1=H(collections.Counter(t)); return H(collections.Counter(t[i:i+2] for i in range(len(t)-1)))-h1, h1

print('=== A. Verbose-cipher ceiling: greedily merge most frequent bigrams into single symbols, track h2')
toks=voy[:]; 
for step in range(12):
    hh,h1=h2(toks); 
    bg=collections.Counter(); 
    for w in toks:
        for i in range(len(w)-1): bg[w[i:i+2]]+=1
    best=max(bg, key=lambda b: bg[b])  # most frequent
    sym=chr(0x100+step)
    print(f'  step {step:2d}: h2={hh:.3f} h1={h1:.3f} alphabet={len(set("".join(toks)))} mean wordlen={sum(map(len,toks))/len(toks):.2f}  -> merging "{best}" ({bg[best]})')
    toks=[w.replace(best,sym) for w in toks]

print('\n=== B. Labels vs running text')
lab=[w for r in rows if r['ltype'].startswith('L') for w in r['text'].split('.') if w]
para=[w for r in rows if r['ltype'].startswith('P') for w in r['text'].split('.') if w]
labc=collections.Counter(lab); parac=collections.Counter(para)
print(f'  label tokens {len(lab)}, types {len(labc)}, hapax {sum(1 for v in labc.values() if v==1)/len(labc):.2f}, mean len {sum(map(len,lab))/len(lab):.2f}')
print(f'  labels also appearing in paragraph text: {sum(1 for w in labc if w in parac)/len(labc):.1%} of label types')
print('  label-initial chars:', collections.Counter(w[0] for w in lab).most_common(8))
print('  para-initial chars :', collections.Counter(w[0] for w in para).most_common(8))
print('  top labels:', labc.most_common(15))
print('  labels starting with q:', sum(1 for w in lab if w[0]=="q")/len(lab), ' text words starting with q:', sum(1 for w in para if w[0]=="q")/len(para))

print('\n=== C. Position within line: word length and glyph usage by position (paragraph lines with >=6 words)')
L=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P')]
L=[l for l in L if len(l)>=6]
for name,sel in [('1st',lambda l:l[0]),('2nd',lambda l:l[1]),('mid',lambda l:l[len(l)//2]),('2nd-last',lambda l:l[-2]),('last',lambda l:l[-1])]:
    ws=[sel(l) for l in L]
    print(f'  {name:8s} mean len {sum(map(len,ws))/len(ws):.2f}  q-initial {sum(w[0]=="q" for w in ws)/len(ws):.3f}  ends-y {sum(w[-1]=="y" for w in ws)/len(ws):.3f}  ends-m/g {sum(w[-1] in "mg" for w in ws)/len(ws):.3f}  starts-gallows(t/p/k/f) {sum(w[0] in "tpkf" for w in ws)/len(ws):.3f}')
# paragraph-initial (ltype P and locus prefix '@' = first line of paragraph); we lost prefix; approximate with line number 1 or lines whose first word starts with gallows
first_lines=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P') and r['line']=='1']
print('  first-line-of-page first char:', collections.Counter(l[0][0] for l in first_lines if l).most_common(6))

print('\n=== D. Topic test: vocabulary shared within a page vs across pages')
pages=collections.defaultdict(list)
for r in rows: pages[r['folio']]+= [w for w in r['text'].split('.') if w]
pg=[v for v in pages.values() if len(v)>=60]
def jacc(a,b):
    a=set(a); b=set(b); return len(a&b)/len(a|b)
def test(pg, n=2000):
    within=0; across=0
    for _ in range(n):
        p=random.choice(pg); h=len(p)//2
        within+=jacc(p[:h],p[h:])
        q=random.choice(pg); across+=jacc(p[:h],q[len(q)//2:])
    return within/n, across/n
print('  voynich within-page vs across-page Jaccard: %.3f vs %.3f'%test(pg))
def clean(path):
    s=open(path,encoding='utf-8',errors='replace').read().lower(); return re.findall(r'[a-z]+',s)
for name,path in [('latin','data/ref/latin_pliny.txt'),('italian','data/ref/italian_dante.txt')]:
    t=clean(path)[:38000]; P=[t[i:i+170] for i in range(0,len(t),170)]
    print(f'  {name} within vs across: %.3f vs %.3f'%test(P))
print('  voynich, same test but within Currier language only (B pages):')
pgB=[[w for w in v] for k,v in pages.items() if len(v)>=60 and any(r['folio']==k and r['lang']=='B' for r in rows[:1])]
