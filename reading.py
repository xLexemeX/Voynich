"""Produce an annotated 'reading' of a folio: for each word, its corpus frequency, Currier A/B split,
structural decomposition, where else it occurs, and nearest neighbors. Usage: python3 reading.py f1r"""
import collections, csv, re, sys
folio=sys.argv[1]
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
allw=[(w,r) for r in rows for w in r['text'].split('.') if w]
freq=collections.Counter(w for w,_ in allw)
byl=collections.defaultdict(collections.Counter)
for w,r in allw: byl[w][r['lang'] or '?']+=1
sec=collections.defaultdict(collections.Counter)
for w,r in allw: sec[w][r['section']]+=1
pat=re.compile(r'^(qo|o|q|y|s|d|ch|sh|)?(.*?)(aiin|ain|iin|in|dy|edy|eey|ey|y|ol|al|or|ar|l|r|n|m|s|)$')
types=set(freq)
def neigh(w):
    out=set(); alpha='abcdefghiklmnopqrstyz'
    for i in range(len(w)):
        if w[:i]+w[i+1:] in types: out.add(w[:i]+w[i+1:])
        for a in alpha:
            x=w[:i]+a+w[i+1:]
            if x!=w and x in types: out.add(x)
    return sorted(out,key=lambda x:-freq[x])[:6]
out=[f'# Annotated reading of folio {folio}\n',
     'Columns: word · total count in manuscript · A/B counts · sections it appears in · slot decomposition (prefix|core|suffix) · closest spelling variants (by frequency).',
     'A count of 1 means the word appears nowhere else in the manuscript.\n']
for r in rows:
    if r['folio']!=folio: continue
    ws=[w for w in r['text'].split('.') if w]
    out.append(f'\n## line {r["line"]} ({r["ltype"]})\n`{" ".join(ws)}`\n')
    out.append('| word | n | A/B | sections | slots | variants |\n|---|---|---|---|---|---|')
    for w in ws:
        m=pat.match(w); slots=f'{m.group(1) or "-"}|{m.group(2)}|{m.group(3) or "-"}' if m else '?'
        ab=' '.join(f'{k}{v}' for k,v in sorted(byl[w].items()))
        ss=' '.join(f'{k[:3]}{v}' for k,v in sec[w].most_common(4))
        out.append(f'| {w} | {freq[w]} | {ab} | {ss} | {slots} | {" ".join(neigh(w))} |')
import os; os.makedirs('readings',exist_ok=True)
open(f'readings/{folio}.md','w').write('\n'.join(out)); print('wrote readings/%s.md'%folio)
