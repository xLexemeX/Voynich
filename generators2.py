"""Tuned generator: self-citation constrained to the slot grammar. Each new word copies a word from the
previous 1-2 lines (or current line) and replaces ONE slot (prefix/core/suffix) with a draw from the slot tables."""
import collections, math, re, random, csv
random.seed(11)
exec(open('generators.py').read().split("stats('VOYNICH',lines)")[0])   # reuse stats() and data
pat=re.compile(r'^(qo|o|q|y|s|d|ch|sh|)?(.*?)(aiin|ain|iin|in|dy|edy|eey|ey|y|ol|al|or|ar|l|r|n|m|s|)$')
P=collections.Counter(); C=collections.Counter(); S=collections.Counter()
for w in voy:
    m=pat.match(w)
    if m and m.group(2): P[m.group(1) or '']+=1; C[m.group(2)]+=1; S[m.group(3) or '']+=1
def draw(cnt):
    ks=list(cnt); ws=[cnt[k] for k in ks]; return random.choices(ks,ws)[0]
def split(w):
    m=pat.match(w); return [m.group(1) or '', m.group(2), m.group(3) or ''] if m and m.group(2) else [draw(P),draw(C),draw(S)]
def gen(nlines, p_copy=0.12, p_local=0.85):
    out=[]
    for k in range(nlines):
        n=len(random.choice(lines)); l=[]
        for _ in range(n):
            pool=(l+ (out[-1] if out else []) + (out[-2] if len(out)>1 else [])) if random.random()<p_local else (random.choice(out) if out else [])
            if pool and random.random()>0.1:
                src=random.choice(pool)
                if random.random()<p_copy: l.append(src); continue
                s=split(src); i=random.choice([0,1,1,2,2]); s[i]=[draw(P),draw(C),draw(S)][i]
                l.append(''.join(s) or 'o')
            else: l.append(draw(P)+draw(C)+draw(S))
        out.append(l)
    return out
stats('VOYNICH',lines)
stats('slot-self-citation',gen(len(lines)))
