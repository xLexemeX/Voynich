import re, collections, random, numpy as np
random.seed(18)
sect={}; cur=None; items=collections.defaultdict(list)   # folio -> ordered list of ('L'|'P', words)
for line in open('data/ZL3b-n.txt',encoding='utf-8',errors='replace'):
    m=re.match(r'^<(f\w+)>\s*<!(.*?)>',line)
    if m: cur=m.group(1); sect[cur]=dict(re.findall(r'\$(\w)=(\w+)',m.group(2))).get('I',''); continue
    m=re.match(r'^<(f\w+)\.(\d+),([@+=*~&])(\w)(\w)>\s*(?:<![^>]*>)?(.*)$',line.rstrip())
    if not m: continue
    t=re.sub(r'<[^>]*>|\{[^}]*\}','',m.group(6)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t).replace(',','.').replace('?','')
    ws=[w for w in t.split('.') if w and not re.search(r'[^a-z]',w)]
    kind=m.group(4)
    if kind=='P':
        if m.group(3)=='@' or not items[m.group(1)] or items[m.group(1)][-1][0]!='P': items[m.group(1)].append(['P',ws])
        else: items[m.group(1)][-1][1]+=ws
    elif kind=='L': items[m.group(1)].append(['L',ws])
def test(secs, name, minlen=3):
    hits_next=hits_other=n=0; rows=[]
    for f,it in items.items():
        if sect.get(f) not in secs: continue
        paras=[i for i,(k,_) in enumerate(it) if k=='P']
        if len(paras)<2: continue
        for i,(k,ws) in enumerate(it):
            if k!='L': continue
            nxt=[p for p in paras if p>i]
            if not nxt: continue
            j=nxt[0]; others=[p for p in paras if p!=j]
            for w in ws:
                if len(w)<minlen: continue
                n+=1; a=w in it[j][1]; b=np.mean([w in it[p][1] for p in others])
                hits_next+=a; hits_other+=b; rows.append((f,w,a,b))
    if n==0: return
    obs=hits_next/n; exp=hits_other/n
    # permutation: for each label, pick a random paragraph of its page as "next"
    null=[]
    by=collections.defaultdict(list)
    for f,w,a,b in rows: by[f].append(w)
    for _ in range(3000):
        h=0
        for f,ws in by.items():
            paras=[x[1] for x in items[f] if x[0]=='P']
            for w in ws: h+= w in random.choice(paras)
        null.append(h/n)
    p=np.mean([x>=obs for x in null])
    print(f'{name:22s} labels(len>={minlen}) n={n:4d}  in paragraph directly after: {obs:.3f}   in other paragraphs of same page (mean): {exp:.3f}   random-paragraph null mean {np.mean(null):.3f}  p={p:.4f}')
    return rows
r=test({'P'},'pharma')
test({'B'},'bio (nymph labels)')
test({'H'},'herbal')
test({'A','C','Z','S'},'astro/cosmo/zodiac')
print('\npharma label hits in the paragraph right after them:')
print(sorted(set((f,w) for f,w,a,b in r if a)))
