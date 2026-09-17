import csv, collections, re
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
lines=[[w for w in r['text'].split('.') if w] for r in rows]
pos=collections.defaultdict(lambda:[0,0,0])   # word -> [initial, medial, final]
for l in lines:
    for i,w in enumerate(l): pos[w][0 if i==0 else 2 if i==len(l)-1 else 1]+=1
tot=collections.Counter({w:sum(v) for w,v in pos.items()})
N=sum(tot.values()); Ninit=sum(v[0] for v in pos.values())
print(f'base rate line-initial = {Ninit/N:.3f}')
print('=== s-X vs d-X: fraction line-initial, for stems X with both forms (>=10 each)')
pairs=[]
for w in tot:
    if w.startswith('s') and not w.startswith('sh') and tot[w]>=10 and tot['d'+w[1:]]>=10:
        d='d'+w[1:]; pairs.append((w,tot[w],pos[w][0]/tot[w],d,tot[d],pos[d][0]/tot[d]))
for p in sorted(pairs,key=lambda p:-p[1])[:20]: print('  %-8s n=%4d init=%.2f   %-8s n=%4d init=%.2f'%p)
sa=sum(p[1] for p in pairs); si=sum(p[1]*p[2] for p in pairs); da=sum(p[4] for p in pairs); di=sum(p[4]*p[5] for p in pairs)
print(f'  pooled: s-forms {si/sa:.2f} line-initial (n={sa}), d-forms {di/da:.2f} (n={da})')
print('\n=== all words by initial glyph: fraction line-initial')
byg=collections.defaultdict(lambda:[0,0])
for w,v in pos.items(): g=w[:2] if w[:2] in ('sh','ch','qo','ct','ck','cp','cf') else w[0]; byg[g][0]+=v[0]; byg[g][1]+=sum(v)
for g,(i,n) in sorted(byg.items(), key=lambda x:-x[1][1]):
    if n>200: print(f'  {g:3s} n={n:6d} line-initial {i/n:.3f}')
print('\n=== y-X vs o-X vs X (bare): line-initial fraction')
for pre in ['y','o','s','d']:
    a=b=0
    for w in tot:
        if w.startswith(pre) and tot[w]>=5 and tot[w[1:]]>=5 and len(w)>2: a+=pos[w][0]; b+=tot[w]
    print(f'  {pre}+X (X also exists bare): line-initial {a/b:.3f} (n={b})')
print('\n=== do line-initial words absorb an extra glyph? compare word W at line start vs same W elsewhere: length')
# for each word type, count initial vs not — compute mean length weighted
li=[len(w) for l in lines for w in l[:1]]; lo=[len(w) for l in lines for w in l[1:]]
print(f'  mean len first word {sum(li)/len(li):.2f}, others {sum(lo)/len(lo):.2f}')
# does stripping the first glyph of a line-initial word give a word that's common elsewhere?
strip=collections.Counter(); 
for l in lines:
    w=l[0]
    if len(w)>2 and tot[w[1:]]>=20: strip[w[0]]+=1
print('  first glyph of line-initial words whose remainder is itself a frequent word:', strip.most_common(8), 'of', len(lines),'lines')
