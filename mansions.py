"""If f69v (28 radial entries) and f68r1 (29 star labels) both list the 28 lunar mansions, they should share words.
Compare with overlap between f69v and every other label/ring set of 15+ words (exact and edit distance 1)."""
import csv, collections
rows=[r for r in csv.DictReader(open('data/corpus.tsv'),delimiter='\t') if r['text']]
sets=collections.defaultdict(set)
for r in rows:
    if r['ltype'][0] in 'LR': sets[(r['folio'],r['ltype'])].update(w for w in r['text'].split('.') if w and w.isalpha())
def ed1(a,b):
    if a==b: return True
    if abs(len(a)-len(b))>1: return False
    if len(a)==len(b): return sum(x!=y for x,y in zip(a,b))==1
    s,l=(a,b) if len(a)<len(b) else (b,a)
    return any(l[:i]+l[i+1:]==s for i in range(len(l)))
A=sets[('f69v','Ri')]
print('f69v radial words:', ' '.join(sorted(A)))
res=[]
for k,B in sets.items():
    if k[0]=='f69v' or len(B)<15: continue
    ex=len(A&B); near=sum(any(ed1(a,b) for b in B) for a in A)
    res.append((near/len(A),ex,len(B),k))
res.sort(reverse=True)
for i,(n,e,l,k) in enumerate(res):
    if i<8 or k[0].startswith('f68r1'): print(f'{i+1:3d}. {k[0]:7s} {k[1]} size {l:3d}: exact shared {e}, f69v words within 1 edit {n:.2f}')
print('sets compared:',len(res))
