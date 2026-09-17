import csv, collections, random, numpy as np
random.seed(16)
order=[('Pisces','f70v2'),('AriesD','f70v1'),('AriesL','f71r'),('TaurusL','f71v'),('TaurusD','f72r1'),('Gemini','f72r2'),('Cancer','f72r3'),('Leo','f72v3'),('Virgo','f72v2'),('Libra','f72v1'),('Scorpio','f73r'),('Sagitt','f73v')]
def ae(w):
    a=w.count('a'); e=w.count('e'); return (a-e)/(a+e) if a+e else 0.0
for src in ['data/corpus.tsv','data/corpus_VT.tsv','data/corpus_RF.tsv']:
    rows=[r for r in csv.DictReader(open(src),delimiter='\t') if r['text']]
    G=[[w for r in rows if r['folio']==f and r['ltype'].startswith('L') for w in r['text'].split('.') if w] for s,f in order]
    S=[[ae(w) for w in g] for g in G]
    print('==',src)
    # 1. change point: best split k maximising between-group separation (t-like)
    def sep(S,k):
        a=[x for g in S[:k] for x in g]; b=[x for g in S[k:] for x in g]
        return (np.mean(a)-np.mean(b))/np.sqrt(np.var(a)/len(a)+np.var(b)/len(b))
    scores=[(k,sep(S,k)) for k in range(1,12)]
    best=max(scores,key=lambda x:abs(x[1]))
    print('  split after wheel k: '+' '.join(f'{k}:{t:+.1f}' for k,t in scores)+f'  -> best k={best[0]} ({order[best[0]-1][0]}|{order[best[0]][0]})')
    # permutation null for the MAX split statistic (accounts for choosing the split)
    allv=[x for g in S for x in g]; sizes=[len(g) for g in S]; null=[]
    for _ in range(3000):
        random.shuffle(allv); k=0; gg=[]
        for n in sizes: gg.append(allv[k:k+n]); k+=n
        null.append(max(abs(sep(gg,j)) for j in range(1,12)))
    print(f'  max-split statistic {abs(best[1]):.1f}; null 99.9th pct {np.percentile(null,99.9):.1f}; p={np.mean([x>=abs(best[1]) for x in null]):.4f}')
    # 2. leave-one-wheel-out step
    loo=[]
    for i in range(12):
        a=[x for j,g in enumerate(S[:7]) if j!=i for x in g]; b=[x for j,g in enumerate(S[7:],7) if j!=i for x in g]
        loo.append(np.mean(a)-np.mean(b))
    print('  leave-one-wheel-out step: min %.2f max %.2f'%(min(loo),max(loo)))
    # 3. type-level (count each distinct label once per half) to remove repeated-label inflation
    ea=set(w for g in G[:7] for w in g); la=set(w for g in G[7:] for w in g)
    print(f'  distinct label types: early {len(ea)} mean a/e {np.mean([ae(w) for w in ea]):+.2f}; late {len(la)} mean {np.mean([ae(w) for w in la]):+.2f}; shared types {len(ea&la)}')
    # 4. bootstrap CI of the step, resampling labels within halves
    bs=[]
    a=[x for g in S[:7] for x in g]; b=[x for g in S[7:] for x in g]
    for _ in range(5000): bs.append(np.mean(random.choices(a,k=len(a)))-np.mean(random.choices(b,k=len(b))))
    print('  bootstrap 95%% CI for step: [%.2f, %.2f]'%tuple(np.percentile(bs,[2.5,97.5])))
    # 5. labels that contain neither a nor e excluded
    Sx=[[ae(w) for w in g if ('a' in w or 'e' in w)] for g in G]
    print('  excluding labels with no a/e: early %.2f late %.2f'%(np.mean([x for g in Sx[:7] for x in g]),np.mean([x for g in Sx[7:] for x in g])))
