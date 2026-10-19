"""Generators laid out on the real page/line structure, scored with scorecard.card()."""
import random, re, collections, sys
from scorecard import real_pages, card
ns={}; exec(open('generators2.py').read().rsplit("stats('VOYNICH',lines)",1)[0], ns)   # gen(), P,C,S, split, draw
REAL=real_pages()
def layout(lines):
    out=[]; k=0
    for p in REAL:
        out.append([]); 
        for l in p: out[-1].append(lines[k][:len(l)] if k<len(lines) else []); k+=1
    return out
def g2(seed):
    ns['random'].seed(seed); L=ns['gen'](sum(len(p) for p in REAL)); return layout(L)
if __name__=='__main__':
    real=card(REAL); gen=card(g2(1))
    print(f'{"statistic":32s} {"real":>8s} {"gen2":>8s}')
    for k in real: print(f'{k:32s} {real[k]:8.3f} {gen[k]:8.3f}')

def g3(seed, NLEX=9000, zipf=1.05, p_local=0.35, topic=60, p_q=0.65, p_unq=0.7, alt_tries=3):
    """Lexicon + page topic + two scribal rules. No new forms are invented while writing."""
    rng=random.Random(seed); P,C,S=ns['P'],ns['C'],ns['S']
    def draw(cnt): ks=list(cnt); return rng.choices(ks,[cnt[k] for k in ks])[0]
    lex=[]; seen=set()
    while len(lex)<NLEX:
        w=(draw(P)+draw(C)+draw(S)) or 'o'
        if w not in seen: seen.add(w); lex.append(w)
    wt=[1/(i+1)**zipf for i in range(NLEX)]
    out=[]
    for p in REAL:
        page=[]; fav=rng.sample(range(NLEX),topic)                     # page topic: a few lexicon items favored on this page
        prev_init=None
        for l in p:
            line=[]
            for j in range(len(l)):
                for _ in range(alt_tries if j==0 else 1):
                    if page and rng.random()<p_local: w=rng.choice([x for ll in page for x in ll]+line or [lex[0]])
                    elif rng.random()<0.15: w=lex[rng.choice(fav)]
                    else: w=lex[rng.choices(range(NLEX),wt)[0]]
                    if j>0 or prev_init is None or w[0]!=prev_init: break
                if line:                                                 # junction rule
                    if line[-1].endswith('y') and w.startswith('o') and rng.random()<p_q: w='q'+w
                    elif not line[-1].endswith('y') and w.startswith('qo') and rng.random()<p_unq: w=w[1:]
                line.append(w)
            prev_init=line[0][0] if line else prev_init
            page.append(line)
        out.append(page)
    return out
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='g3':
    real=card(REAL); r3=card(g3(1))
    print(f'{"statistic":32s} {"real":>8s} {"gen3":>8s}')
    for k in real: print(f'{k:32s} {real[k]:8.3f} {r3[k]:8.3f}')
