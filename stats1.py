import collections, math, csv
rows = list(csv.DictReader(open('data/corpus.tsv'), delimiter='\t'))
rows = [r for r in rows if r['text']]
def words(rs): 
    for r in rs:
        for w in r['text'].split('.'):
            if w: yield w
allw = list(words(rows))
print('tokens', len(allw), 'types', len(set(allw)))
wf = collections.Counter(allw)
print('\nTop 40 words:'); print(' '.join(f'{w}:{c}' for w,c in wf.most_common(40)))
hapax = sum(1 for w,c in wf.items() if c==1)
print('hapax legomena', hapax, f'({hapax/len(wf):.1%} of types)')
# word length
L = collections.Counter(len(w) for w in allw)
print('\nword length dist:', ' '.join(f'{k}:{L[k]}' for k in sorted(L)))
print('mean len', sum(len(w) for w in allw)/len(allw))
# char freq
cf = collections.Counter(''.join(allw))
N = sum(cf.values())
print('\nchar freq:', ' '.join(f'{c}:{n/N:.3f}' for c,n in cf.most_common()))
def H(counter):
    n=sum(counter.values()); return -sum(c/n*math.log2(c/n) for c in counter.values())
text = ' '.join(allw)
h1 = H(collections.Counter(text))
bg = collections.Counter(text[i:i+2] for i in range(len(text)-1))
h2 = H(bg) - h1
print(f'\nchar entropy h1={h1:.3f}  conditional h2={h2:.3f}  (incl. space)')
# per language
for lang in 'AB':
    ws = list(words([r for r in rows if r['lang']==lang]))
    c = collections.Counter(ws)
    print(f'\nLang {lang}: tokens {len(ws)} types {len(c)}; top20:', ' '.join(f'{w}:{n}' for w,n in c.most_common(20)))
# line-initial / final
first = collections.Counter(r['text'].split('.')[0] for r in rows)
last = collections.Counter(r['text'].split('.')[-1] for r in rows)
print('\nline-initial words:', first.most_common(15))
print('line-final words:', last.most_common(15))
fc = collections.Counter(r['text'][0] for r in rows)
print('line-initial chars:', fc.most_common(10))
lc = collections.Counter(r['text'][-1] for r in rows)
print('line-final chars:', lc.most_common(10))
# word-initial/final chars
wi = collections.Counter(w[0] for w in allw); wl = collections.Counter(w[-1] for w in allw)
print('word-initial chars:', ' '.join(f'{c}:{n/len(allw):.3f}' for c,n in wi.most_common(12)))
print('word-final chars:', ' '.join(f'{c}:{n/len(allw):.3f}' for c,n in wl.most_common(12)))
# repeated adjacent words
rep = sum(1 for r in rows for a,b in zip(r['text'].split('.'), r['text'].split('.')[1:]) if a==b)
print('\nadjacent identical word pairs:', rep)
# per section vocab overlap
secs = collections.defaultdict(list)
for r in rows: secs[r['section']].append(r)
sv = {s: collections.Counter(words(rs)) for s,rs in secs.items()}
print('\nsection tokens/types:', {s:(sum(c.values()),len(c)) for s,c in sv.items()})
