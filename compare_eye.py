"""NOTES §80: compare the f8r first paragraph read by eye (data/eye/f8r_p1.txt) with ZL, and ZL with Takahashi (VT), on the
same lines. Glyph-level comparison uses EVA units (ch, sh, cth, ckh, cph, cfh as single glyphs); word breaks count as a symbol."""
import csv, re, collections, difflib
G=re.compile(r"cth|ckh|cph|cfh|ch|sh|[a-z?]")
def eye():
    L={}; R={}
    for l in open('data/eye/f8r_p1.txt'):
        if l.startswith('#') or not l.strip(): continue
        n,rest=l.split(' ',1); parts=[p.strip() for p in rest.split('|')]
        L[int(n)]=parts[0]; R[int(n)]=parts[1] if len(parts)>1 else ''
    # ZL line n = left part of eye line n + right part of eye line n+1 (the right column sits one line higher than I paired it)
    return {n:'.'.join(x for x in (L[n], R.get(n+1,'')) if x) for n in L}
def corpus(path):
    return {int(r['line']):r['text'] for r in csv.DictReader(open(path),delimiter='\t') if r['folio']=='f8r' and r['line'].isdigit() and int(r['line'])<=7}
def seq(t): return [g for w in t.split('.') for g in G.findall(w)+['.']][:-1]
def ed_ops(a,b):
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False); ops=collections.Counter(); d=0
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal': continue
        d+=max(i2-i1,j2-j1); ops[(''.join(a[i1:i2]) or '∅', ''.join(b[j1:j2]) or '∅')]+=1
    return d, ops
def compare(A,B,name):
    words=same=0; d=n=0; ops=collections.Counter(); brk=0
    for k in sorted(A):
        a,b=A[k],B.get(k,'')
        wa,wb=a.split('.'),b.split('.'); words+=len(wb)
        same+=sum(x.size for x in difflib.SequenceMatcher(None,wa,wb,autojunk=False).get_matching_blocks())
        sa,sb=seq(a),seq(b); dd,o=ed_ops(sa,sb); d+=dd; n+=len(sb); ops+=o
        brk+=abs(len(wa)-len(wb))
    print(f'{name}: words identical {same}/{words} ({same/words:.0%}); glyph+break edit distance {d}/{n} = {d/n:.0%}; difference in word count {brk}')
    print('   differences (first reading -> second), most common:', ', '.join(f'{x}->{y}' + (f' x{c}' if c>1 else '') for (x,y),c in ops.most_common(25)))
if __name__=='__main__':
    E=eye(); ZL=corpus('data/corpus.tsv'); VT=corpus('data/corpus_VT.tsv'); RF=corpus('data/corpus_RF.tsv')
    for k in sorted(E): print(f'{k}  eye {E[k]}\n   ZL  {ZL[k]}\n   VT  {VT[k]}')
    compare(E,ZL,'eye vs ZL'); compare(VT,ZL,'Takahashi (VT) vs ZL'); compare(RF,ZL,'RF vs ZL')
    # my 'l' and 'r' were a convention swap (EVA r is the tall hooked glyph, l the low one): score again with the two exchanged
    S={k:v.translate(str.maketrans('lr','rl')) for k,v in E.items()}
    compare(S,ZL,'eye with r/l exchanged vs ZL')
