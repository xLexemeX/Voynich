"""Starred paragraphs in quire 20: estimate the total including the lost bifolio f109-f110."""
import csv, collections, statistics as st
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text'] and r['section']=='stars' and r['ltype'].startswith('P') and not r['folio'].startswith('f58')]
p=collections.OrderedDict()
for r in rows: p.setdefault((r['folio'],r['para']),1)
fol=collections.Counter(f for f,_ in p); full=[v for f,v in fol.items() if f!='f116r']
m,sd=st.mean(full),st.stdev(full)
print(f'quire 20 paragraphs present: {len(p)} on {len(fol)} pages; per full page mean {m:.1f} sd {sd:.1f} max {max(full)}')
print(f'missing bifolio f109-f110 = 4 pages: expected {4*m:.0f} +/- {2*sd:.0f}; total {len(p)+4*m:.0f} +/- {2*sd:.0f}')
for target in (360,365): need=target-len(p); print(f'  to reach {target}: missing pages would need {need} paragraphs, {need/4:.1f} per page (observed max {max(full)})')
# visual star counts from the Beinecke scans (data/stars_visual.tsv; counted by eye from margin strips, about +/-1 per page)
V={r['folio']:int(r['stars_visual']) for r in csv.DictReader(open('data/stars_visual.tsv'),delimiter='\t')}
fullv=[v for f,v in V.items() if f!='f116r']; mv,sv=st.mean(fullv),st.stdev(fullv)
print(f'stars counted on scans: {sum(V.values())} on {len(V)} pages; per full page mean {mv:.1f} sd {sv:.1f} min {min(fullv)} max {max(fullv)}')
print(f'  lost bifolio, 4 pages: expected {4*mv:.0f} +/- {2*sv:.0f}; total {sum(V.values())+4*mv:.0f} +/- {2*sv:.0f}')
for target in (360,365): need=target-sum(V.values()); print(f'  to reach {target}: lost pages would hold {need}, {need/4:.1f} per page (observed min {min(fullv)})')
