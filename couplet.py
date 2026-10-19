"""Is the line-initial alternation phase-locked to the paragraph start (couplets), or a free-running no-repeat rule?"""
import csv, collections, random, re
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
G=re.compile(r"cth|ckh|cph|cfh|ch|sh|[a-z]")
def first(t): m=G.match(t.replace("'",'')); return m.group() if m else None
paras=collections.OrderedDict()
for r in rows: paras.setdefault((r['folio'],r['para']),[]).append(r)
S=[[first(r['text']) for r in ls] for ls in paras.values() if len(ls)>=5]   # index 0 = paragraph-first line
random.seed(0)
def stats(S):
    d=collections.Counter(); n=collections.Counter()
    for s in S:
        for i in range(1,len(s)-1):
            if s[i] and s[i+1]: n[i%2]+=1; d[i%2]+=s[i]==s[i+1]
    return {k:d[k]/n[k] for k in n}, n
o,n=stats(S)
null=[stats([[s[0]]+random.sample(s[1:],len(s)-1) for s in S])[0] for _ in range(500)]
for k,lab in [(1,'lines 2->3, 4->5, ... (odd->even index)'),(0,'lines 3->4, 5->6, ... ')]:
    m=sum(x[k] for x in null)/len(null); print(f'{lab:42s} pairs {n[k]:4d} same-initial {o[k]:.3f} vs shuffle {m:.3f}')
# word-level: within a line, do consecutive word initials avoid repeats too?
W=[[first(w) for w in r['text'].split('.') if w] for r in rows]
def rep(S,lag=1): p=[(s[i],s[i+lag]) for s in S for i in range(len(s)-lag)]; return sum(a==b for a,b in p)/len(p)
nw=[rep([random.sample(s,len(s)) for s in W]) for _ in range(100)]
print(f'consecutive word initials within a line: same {rep(W):.3f} vs within-line shuffle {sum(nw)/len(nw):.3f}; lag2 {rep(W,2):.3f}')
