"""Held-out test of Bax's page-initial K: does the opening gallows of a herbal page predict the initial of the plant's proposed name?
Names: voynich.nu tentative identifications (ELV = E. Velinska, ThP = Th. Petersen), data/plantids.json."""
import csv, json, re, random, collections
ids=json.load(open('data/plantids.json'))
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P') and r['section']=='herbal']
first={}
for r in rows: first.setdefault(r['folio'],r['text'].split('.')[0])
def names(s,who):
    m=re.search(who+r'A?:\s*(.*?)(?=(ELVA?|THP|ThP):|$)',s,re.I)
    if not m: return []
    return [w.lower() for w in re.findall(r'[A-Za-zäöü]{4,}',m.group(1)) if w.lower() not in {'some','kind','leaves','species','like','nearly','allied','plant','roots','indian','water','fern','left','right','good','king','henry','with'}]
def kclass(n):  # Bax-style /k/: k, q, c not before e/i (so ca co cu cy cr cl ch)
    return n[0] in 'kq' or (n[0]=='c' and n[1] not in 'ei')
random.seed(0)
import os; EXCL=set(os.environ.get('EXCL','').split(','))
for who in ('ELV','ThP'):
    D=[(f,first[f][0],names(ids[f],who)[0]) for f in ids if f in first and f not in EXCL and names(ids[f],who) and first[f][0] in 'ptkf']
    g=collections.Counter(x[1] for x in D)
    k_rate=lambda D,gal: (sum(kclass(n) for f,x,n in D if x==gal), sum(1 for f,x,n in D if x==gal))
    a,na=k_rate(D,'k'); b=sum(kclass(n) for f,x,n in D if x!='k'); nb=len(D)-na
    obs=a/na-b/nb; null=[]
    N=[n for _,_,n in D]
    for _ in range(10000):
        random.shuffle(N); E=[(f,x,n) for (f,x,_),n in zip(D,N)]; aa,_=k_rate(E,'k'); bb=sum(kclass(n) for f,x,n in E if x!='k'); null.append(aa/na-bb/nb)
    print(f'{who}: {len(D)} herbal pages with a name and a gallows opening {dict(g)}')
    print(f'   C/K-initial names: k-opened pages {a}/{na} = {a/na:.2f}; p/t/f-opened pages {b}/{nb} = {b/nb:.2f}; permutation p = {sum(x>=obs for x in null)/len(null):.3f}')
    print('   k-opened pages:', '; '.join(f'{f} {first[f]} = {n}' for f,x,n in D if x=='k'))
    match=sum((x=='k' and kclass(n)) or (x!='k' and n[0]==x) for f,x,n in D); null=[]
    for _ in range(10000):
        random.shuffle(N); null.append(sum((x=='k' and kclass(n)) or (x!='k' and n[0]==x) for (f,x,_),n in zip(D,N)))
    print(f'   opening gallows matches name initial (k~C/K, p~P, t~T, f~F): {match} vs shuffled {sum(null)/len(null):.1f}, p = {sum(x>=match for x in null)/len(null):.3f}')
