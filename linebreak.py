import csv, collections, random, math
random.seed(7)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
L=[[w for w in r['text'].split('.') if w] for r in rows]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def MI(pairs):
    pc=collections.Counter(pairs); a=collections.Counter(p[0] for p in pairs); b=collections.Counter(p[1] for p in pairs); return H(a)+H(b)-H(pc)
def ratio(pairs):
    y=[b for a,b in pairs if a.endswith('y')]; o=[b for a,b in pairs if not a.endswith('y')]
    if len(y)<30 or len(o)<30: return float('nan'),len(y),len(o)
    return (sum(b.startswith('qo') for b in y)/len(y))/(sum(b.startswith('qo') for b in o)/len(o)+1e-9), len(y), len(o)
def sets(idx):
    within=[(a,b) for i in idx for a,b in zip(L[i],L[i][1:])]
    across=[(L[i][-1],L[i+1][0]) for i in idx if i+1<len(L) and rows[i]['pend']=='0' and rows[i]['para']==rows[i+1]['para']]
    return within, across
print('=== y|qo ratio within line vs across line break, by section and language')
for key in ['section','lang']:
    for v in sorted(set(r[key] for r in rows)):
        idx=[i for i,r in enumerate(rows) if r[key]==v]
        w,a=sets(idx); rw=ratio(w); ra=ratio(a)
        if rw[1]>=100 and ra[1]>=30: print(f'  {key}={v:7s} within {rw[0]:.2f} (ny={rw[1]}) across {ra[0]:.2f} (ny={ra[1]})')
print('\n=== glyph-level MI between final glyph of word i and initial glyph of word i+1')
w,a=sets(range(len(rows)))
rnd=[(random.choice(w)[0], random.choice(w)[1]) for _ in range(len(w))]
# across-line control: pair each line end with the first word of a random other line in the same section
sec=[r['section'] for r in rows]
ctrl=[]
for i in range(len(L)-1):
    if rows[i]['pend']=='0':
        j=random.randrange(len(L)); ctrl.append((L[i][-1],L[j][0]))
gl=lambda P:[(x[-1],y[0]) for x,y in P]
print(f'  within-line adjacent   MI={MI(gl(w)):.4f} (n={len(w)})')
print(f'  across line break      MI={MI(gl(a)):.4f} (n={len(a)})')
print(f'  line end -> random line start (control) MI={MI(gl(ctrl)):.4f} (n={len(ctrl)})')
print(f'  random within pairs (control) MI={MI(gl(rnd)):.4f}')
print('\n=== word-level: excess MI(word_i, word_i+1) minus shuffled baseline')
def xs(P, k=5):
    m=MI(P); s=0
    for _ in range(k):
        b=[p[1] for p in P]; random.shuffle(b); s+=MI(list(zip([p[0] for p in P],b)))
    return m-s/k
# subsample within to the size of across for a fair finite-sample comparison
ws=random.sample(w,len(a))
print(f'  within-line (subsampled to n={len(a)}): {xs(ws):.3f}   across line break: {xs(a):.3f}   line end->random line start: {xs(random.sample(ctrl,len(a))):.3f}')
print('\n=== the same test on Latin and Italian with artificial lines of 8 words (dependencies should survive line breaks)')
import re
for name,path in [('latin','data/ref/latin_pliny.txt'),('italian','data/ref/italian_dante.txt')]:
    t=re.findall(r'[a-z]+',open(path,encoding='utf-8',errors='replace').read().lower())[:40000]
    LL=[t[i:i+8] for i in range(0,len(t)-8,8)]
    wi=[(a,b) for l in LL for a,b in zip(l,l[1:])]; ac=[(LL[i][-1],LL[i+1][0]) for i in range(len(LL)-1)]
    print(f'  {name}: glyph MI within {MI(gl(wi)):.4f} across {MI(gl(ac)):.4f};  word excess MI within(sub) {xs(random.sample(wi,len(ac))):.3f} across {xs(ac):.3f}')
# Dante is verse: real line breaks. Use actual Dante lines (tercets) for a true test
txt=open('data/ref/italian_dante.txt',encoding='utf-8',errors='replace').read().lower()
vl=[re.findall(r'[a-z]+',l) for l in txt.split('\n')]; vl=[l for l in vl if 5<=len(l)<=12][:6000]
wi=[(a,b) for l in vl for a,b in zip(l,l[1:])]; ac=[(vl[i][-1],vl[i+1][0]) for i in range(len(vl)-1)]
print(f'  dante REAL verse lines: glyph MI within {MI(gl(wi)):.4f} across {MI(gl(ac)):.4f}; word excess MI within(sub) {xs(random.sample(wi,len(ac))):.3f} across {xs(ac):.3f}')
