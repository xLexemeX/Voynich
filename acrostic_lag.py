"""Line-initial glyph repeats at lag 1..4 within page, against within-page shuffle; also by Currier language and with paragraph boundaries respected."""
import csv, collections, random, re
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
G=re.compile(r"cth|ckh|cph|cfh|ch|sh|[a-z]")
def first(t): m=G.match(t.replace("'",'')); return m.group() if m else None
random.seed(0)
def unitseqs(key, lang=None):
    d=collections.OrderedDict()
    for r in rows:
        if r['pstart']=='1' or (lang and r['lang']!=lang): continue
        x=first(r['text'])
        if x: d.setdefault(key(r),[]).append(x)
    return list(d.values())
def rep(S,lag): p=[(s[i],s[i+lag]) for s in S for i in range(len(s)-lag)]; return sum(a==b for a,b in p)/max(1,len(p)), len(p)
for label,key,lang in [('within page',lambda r:r['folio'],None),('within paragraph',lambda r:(r['folio'],r['para']),None),
                       ('within paragraph, language A',lambda r:(r['folio'],r['para']),'A'),('within paragraph, language B',lambda r:(r['folio'],r['para']),'B')]:
    S=unitseqs(key,lang); out=[]
    for lag in (1,2,3,4):
        o,n=rep(S,lag); null=[rep([random.sample(s,len(s)) for s in S],lag)[0] for _ in range(300)]
        m=sum(null)/len(null); out.append(f'lag{lag} {o:.3f}/{m:.3f} p_low={sum(x<=o for x in null)/len(null):.3f}')
    print(f'{label:30s}', '  '.join(out))
# initial q: does it depend on the previous line's last glyph (cross-line junction)?
prev=None; c=collections.Counter()
for r in rows:
    if r['pstart']=='1': prev=None
    t=r['text'].replace("'",''); f=first(t)
    if prev is not None and f: c[(prev=='y', f=='q')]+=1
    prev=t[-1] if t else None
a=c[(True,True)]/(c[(True,True)]+c[(True,False)]); b=c[(False,True)]/(c[(False,True)]+c[(False,False)])
print(f'P(line starts q | previous line ends y) {a:.3f}  vs otherwise {b:.3f}')
# controls: Latin and Italian prose broken into lines of 9 words, "paragraphs" of 10 lines; first letter of each line
for nm,path in [('Latin (Pliny)','data/ref/latin_pliny.txt'),('Italian (Dante, verse lines as is)','data/ref/italian_dante.txt')]:
    txt=open(path,encoding='utf-8',errors='replace').read().lower()
    if 'dante' in path:
        L=[re.sub(r'[^a-z]','',l.split()[0]) for l in txt.splitlines() if l.strip() and l.split()[0][0].isalpha()][:4000]
    else:
        w=re.findall(r'[a-z]+',txt)[:40000]; L=[w[i] for i in range(0,len(w),9)]
    S=[[x[0] for x in L[i:i+10] if x] for i in range(0,len(L),10)]
    out=[]
    for lag in (1,2):
        o,n=rep(S,lag); null=[rep([random.sample(s,len(s)) for s in S],lag)[0] for _ in range(300)]
        m=sum(null)/len(null); out.append(f'lag{lag} {o:.3f}/{m:.3f} p_low={sum(x<=o for x in null)/len(null):.3f}')
    print(f'control {nm:34s}', '  '.join(out))
