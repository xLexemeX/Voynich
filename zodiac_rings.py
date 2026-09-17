import re, collections, math, random
random.seed(1)
signs=[('Pisces',['f70v2']),('AriesD',['f70v1']),('AriesL',['f71r']),('TaurusL',['f71v']),('TaurusD',['f72r1']),('Gemini',['f72r2']),('Cancer',['f72r3']),('Leo',['f72v3']),('Virgo',['f72v2']),('Libra',['f72v1']),('Scorpio',['f73r']),('Sagitt',['f73v'])]
lab=[]  # (sign, ring, idx, clock, label)
for s,fs in signs:
    ring=-1; idx=0
    for line in open('data/ZL3b-n.txt',encoding='utf-8',errors='replace'):
        m=re.match(r'^<(f\w+)\.(\d+),([@&+=*~])L\w>\s*(?:<!(\d+):(\d+)>)?(.*)$',line.rstrip())
        if not m or m.group(1) not in fs: continue
        if m.group(3)=='@': ring+=1; idx=0
        t=re.sub(r'<[^>]*>|\{[^}]*\}','',m.group(6)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t).replace(',','.').strip('.').replace('?','')
        clock=(int(m.group(4))%12)*60+int(m.group(5)) if m.group(4) else None
        lab.append((s,ring,idx,clock,t)); idx+=1
print(len(lab),'labels')
# ring sizes
for s,_ in signs:
    print(f'  {s:8s}', [sum(1 for l in lab if l[0]==s and l[1]==r) for r in range(4) if any(l[0]==s and l[1]==r for l in lab)])
def feat(w):
    return dict(gal=('t' if 't' in w[:3] else 'k' if 'k' in w[:3] else 'p' if 'p' in w[:3] else 'f' if 'f' in w[:3] else '-'),
                init=w[:2], end=(re.search(r'(aiin|ain|iin|in|dy|ey|y|ol|al|or|ar|l|r|n|m|s|g)$',w) or [None,'-'])[1] if re.search(r'(aiin|ain|iin|in|dy|ey|y|ol|al|or|ar|l|r|n|m|s|g)$',w) else '-',
                ee=('ee' in w), a=('a' in w), L=len(w))
print('\n=== by ring (0=outer/first listed) pooled over signs')
byr=collections.defaultdict(list)
for l in lab: byr[l[1]].append(l[4].split('.')[0])
for r,ws in sorted(byr.items()):
    F=[feat(w) for w in ws]
    print(f'  ring {r}: n={len(ws):3d} gallows t {sum(f["gal"]=="t" for f in F)/len(F):.2f} k {sum(f["gal"]=="k" for f in F)/len(F):.2f}  ee {sum(f["ee"] for f in F):.0f}  has-a {sum(f["a"] for f in F)/len(F):.2f}  mean len {sum(f["L"] for f in F)/len(F):.2f}  endings {collections.Counter(f["end"] for f in F).most_common(4)}')
print('\n=== first label of each ring vs others')
first=[feat(l[4].split('.')[0]) for l in lab if l[2]==0]; rest=[feat(l[4].split('.')[0]) for l in lab if l[2]>0]
for name,F in [('first',first),('rest',rest)]:
    print(f'  {name:5s} n={len(F):3d} t {sum(f["gal"]=="t" for f in F)/len(F):.2f} k {sum(f["gal"]=="k" for f in F)/len(F):.2f} init', collections.Counter(f['init'] for f in F).most_common(4), 'end', collections.Counter(f['end'] for f in F).most_common(4))
print('\n=== gallows t/k alternation along a ring: P(next same gallows) vs shuffled')
def alt(seqs):
    same=tot=0
    for s in seqs:
        g=[feat(w)['gal'] for w in s if feat(w)['gal'] in 'tk']
        for a,b in zip(g,g[1:]): tot+=1; same+=(a==b)
    return same/tot if tot else 0
seqs=[]
for s,_ in signs:
    for r in range(4):
        ws=[l[4].split('.')[0] for l in lab if l[0]==s and l[1]==r]
        if ws: seqs.append(ws)
obs=alt(seqs); sh=[]
for _ in range(500):
    ss=[random.sample(x,len(x)) for x in seqs]; sh.append(alt(ss))
print(f'  observed P(same)={obs:.3f}; shuffled mean {sum(sh)/len(sh):.3f} sd {(sum((x-sum(sh)/len(sh))**2 for x in sh)/len(sh))**.5:.3f}')
print('\n=== Aries/Taurus dark vs light halves')
for a,b in [('AriesD','AriesL'),('TaurusD','TaurusL')]:
    for s in (a,b):
        ws=[l[4].split('.')[0] for l in lab if l[0]==s]; F=[feat(w) for w in ws]
        print(f'  {s:8s} n={len(ws)} t {sum(f["gal"]=="t" for f in F)/len(F):.2f} k {sum(f["gal"]=="k" for f in F)/len(F):.2f} init {collections.Counter(f["init"] for f in F).most_common(3)} end {collections.Counter(f["end"] for f in F).most_common(3)}')
print('\n=== angular position: features vs clock sector (4 quadrants), pooled')
quad=collections.defaultdict(list)
for l in lab:
    if l[3] is not None: quad[(l[3]//180)].append(feat(l[4].split('.')[0]))
for q,F in sorted(quad.items()):
    print(f'  quadrant {q} (from {q*3} o\'clock): n={len(F):3d} t {sum(f["gal"]=="t" for f in F)/len(F):.2f} k {sum(f["gal"]=="k" for f in F)/len(F):.2f} -y {sum(f["end"]=="y" for f in F)/len(F):.2f} -dy {sum(f["end"]=="dy" for f in F)/len(F):.2f} -al/ar {sum(f["end"] in ("al","ar") for f in F)/len(F):.2f}')
import json; json.dump(lab,open('data/zodiac_labels.json','w'))
