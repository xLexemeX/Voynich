"""Do the two leading 'meaningless text' generators reproduce ALL the Voynich statistics?
(1) Rugg-style table+grille: word = prefix + mid + suffix drawn from small weighted tables.
(2) Timm-style self-citation: copy an earlier word (mostly from the same/previous line) and mutate it.
Compare: types, hapax, word length, h2, neighbour density, same-line similarity, adjacent repeats, word-order MI."""
import collections, math, re, random, csv
random.seed(8)
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
lines=[[w for w in r['text'].split('.') if w] for r in rows if r['ltype'].startswith('P')]
voy=[w for l in lines for w in l]
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        cur=[i]
        for j,cb in enumerate(b,1): cur.append(min(prev[j]+1,cur[j-1]+1,prev[j-1]+(ca!=cb)))
        prev=cur
    return prev[-1]
def stats(name,L):
    toks=[w for l in L for w in l]; c=collections.Counter(toks); text=' '.join(toks)
    h1=H(collections.Counter(text)); h2=H(collections.Counter(text[i:i+2] for i in range(len(text)-1)))-h1
    ml=sum(map(len,toks))/len(toks); sd=(sum((len(t)-ml)**2 for t in toks)/len(toks))**.5
    ws=[w for w,v in c.items() if v>=2]; S=set(ws); alpha=set(''.join(ws)); nb=0
    for w in ws:
        for i in range(len(w)):
            if w[:i]+w[i+1:] in S: nb+=1
            for a in alpha:
                if a!=w[i] and w[:i]+a+w[i+1:] in S: nb+=1
    rep=sum(1 for l in L for a,b in zip(l,l[1:]) if a==b)/len(toks)
    LL=[l for l in L if len(l)>=3]; same=0; rnd=0
    for _ in range(2000):
        l=random.choice(LL); i=random.randrange(len(l)); same+=min(lev(l[i],o) for j,o in enumerate(l) if j!=i)
        o=random.choice(LL); rnd+=min(lev(l[i],x) for x in o[:len(l)-1])
    pairs=list(zip(toks,toks[1:])); pc=collections.Counter(pairs); a=collections.Counter(p[0] for p in pairs); b=collections.Counter(p[1] for p in pairs)
    mi=H(a)+H(b)-H(pc); sh=toks[:]; random.shuffle(sh); p2=collections.Counter(zip(sh,sh[1:])); mis=H(a)+H(b)-H(p2)
    print(f'{name:22s} types {len(c):5d} hapax {sum(v==1 for v in c.values())/len(c):.2f} len {ml:.2f}±{sd:.2f} h2 {h2:.2f} nbr {nb/len(ws):.2f} sameline {same/2000:.2f} vs rand {rnd/2000:.2f} rep {rep:.4f} xsMI {mi-mis:.2f}')
stats('VOYNICH',lines)
# (1) table+grille
pat=re.compile(r'^(qo|o|q|y|s|d|ch|sh|)?(.*?)(aiin|ain|iin|in|dy|edy|eey|ey|y|ol|al|or|ar|l|r|n|m|s|)$')
P=collections.Counter(); C=collections.Counter(); S=collections.Counter()
for w in voy:
    m=pat.match(w)
    if m and m.group(2): P[m.group(1) or '']+=1; C[m.group(2)]+=1; S[m.group(3) or '']+=1
def draw(cnt): 
    ks=list(cnt); ws=[cnt[k] for k in ks]; return random.choices(ks,ws)[0]
def grille(nlines):
    return [[draw(P)+draw(C)+draw(S) for _ in range(len(random.choice(lines)))] for _ in range(nlines)]
stats('table+grille (indep)',grille(len(lines)))
# (2) self-citation
def mutate(w):
    alpha='ochedyaiklrstnq'
    r=random.random(); i=random.randrange(len(w))
    if r<0.4 and len(w)>2: return w[:i]+w[i+1:]
    if r<0.8: return w[:i]+random.choice(alpha)+w[i+1:]
    return w[:i]+random.choice(alpha)+w[i:]
def selfcite(nlines, p_copy=0.6):
    out=[]; seed=[draw(P)+draw(C)+draw(S) for _ in range(20)]
    for k in range(nlines):
        n=len(random.choice(lines)); l=[]
        pool=(out[-1] if out else seed)+(out[-2] if len(out)>1 else [])+l
        for _ in range(n):
            src=random.choice(pool+l) if pool+l else random.choice(seed)
            w=src if random.random()<p_copy*0.15 else mutate(src)
            if random.random()<0.3: w=mutate(w)
            w=w[:12] or 'o'; l.append(w)
        out.append(l)
    return out
stats('self-citation',selfcite(len(lines)))
