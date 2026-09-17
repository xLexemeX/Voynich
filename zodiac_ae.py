import csv, collections, random, numpy as np, sys
random.seed(14)
order=[('Pisces',['f70v2']),('AriesD',['f70v1']),('AriesL',['f71r']),('TaurusL',['f71v']),('TaurusD',['f72r1']),('Gemini',['f72r2']),('Cancer',['f72r3']),('Leo',['f72v3']),('Virgo',['f72v2']),('Libra',['f72v1']),('Scorpio',['f73r']),('Sagitt',['f73v'])]
def ae(w): 
    a=w.count('a'); e=w.count('e'); return (a-e)/(a+e) if a+e else 0.0
def spearman(x,y):
    rx=np.argsort(np.argsort(x)); ry=np.argsort(np.argsort(y)); return np.corrcoef(rx,ry)[0,1]
def perm(groups, stat, nperm=10000):
    obs=stat(groups); allv=[x for g in groups for x in g]; sizes=[len(g) for g in groups]; null=[]
    for _ in range(nperm):
        random.shuffle(allv); k=0; gg=[]
        for n in sizes: gg.append(allv[k:k+n]); k+=n
        null.append(stat(gg))
    return obs, np.mean([abs(x)>=abs(obs) for x in null])
trend=lambda groups: spearman(range(len(groups)),[np.mean(g) for g in groups])
step=lambda groups: np.mean([x for g in groups[:7] for x in g])-np.mean([x for g in groups[7:] for x in g])   # f70v-f72r (7 wheels) vs f72v-f73v (5 wheels)
for src in ['data/corpus.tsv','data/corpus_VT.tsv','data/corpus_RF.tsv']:
    rows=[r for r in csv.DictReader(open(src),delimiter='\t') if r['text']]
    lab=[[w for f in fs for r in rows if r['folio']==f and r['ltype'].startswith('L') for w in r['text'].split('.') if w] for s,fs in order]
    ring=[[w for f in fs for r in rows if r['folio']==f and not r['ltype'].startswith('L') for w in r['text'].split('.') if w] for s,fs in order]
    print(f'== {src}')
    for name,G in [('labels',lab),('ring text',ring)]:
        S=[[ae(w) for w in g] for g in G]
        o1,p1=perm(S,trend); o2,p2=perm(S,step)
        print(f'  {name:9s} a-e index per sign: '+' '.join(f'{np.mean(g):+.2f}' for g in S)+f' | trend rho={o1:+.2f} p={p1:.4f} | step (f70v-f72r minus f72v-f73v)={o2:+.2f} p={p2:.4f}')
    # length control for labels: restrict to labels of length 4-7
    S=[[ae(w) for w in g if 4<=len(w)<=7] for g in lab]; o,p=perm(S,step)
    print(f'  labels len 4-7 only: step={o:+.2f} p={p:.4f} (n={sum(len(g) for g in S)})')
    # composition table
    print('  labels: %a-only / %e-only / %both / %neither per sign')
    for (s,_),g in zip(order,lab):
        n=len(g); A=sum(1 for w in g if 'a' in w and 'e' not in w); E=sum(1 for w in g if 'e' in w and 'a' not in w); B=sum(1 for w in g if 'a' in w and 'e' in w)
        print(f'    {s:8s} n={n:2d}  a-only {A/n:.2f}  e-only {E/n:.2f}  both {B/n:.2f}  neither {(n-A-E-B)/n:.2f}')
    break
