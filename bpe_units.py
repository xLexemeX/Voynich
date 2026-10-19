"""Byte-pair merging of glyphs within words: at each inventory size K, unigram entropy h1 and conditional entropy h2 (next unit
given current, word boundary as a unit), and mean word length in units. Voynich (EVA) vs Latin letters, same procedure."""
import csv, re, math, collections
def H(words):
    c1=collections.Counter(); c2=collections.Counter()
    for w in words:
        s=['#']+w
        for a,b in zip(s,s[1:]+['#']): c2[(a,b)]+=1; c1[a]+=1
    n=sum(c1.values()); h1=-sum(v/n*math.log2(v/n) for v in c1.values())
    h12=-sum(v/n*math.log2(v/n) for v in c2.values()); return h1, h12-h1
def bpe(words, steps, report):
    words=[list(w) for w in words]; out=[]
    for k in range(steps+1):
        inv=len({u for w in words for u in w})
        if inv in report or k==steps:
            h1,h2=H(words); out.append((inv,h1,h2,sum(map(len,words))/len(words)))
            report=[r for r in report if r!=inv]
        pc=collections.Counter((a,b) for w in words for a,b in zip(w,w[1:]))
        if not pc: break
        (a,b),_=pc.most_common(1)[0]; m=a+b
        nw=[]
        for w in words:
            o=[];i=0
            while i<len(w):
                if i+1<len(w) and w[i]==a and w[i+1]==b: o.append(m); i+=2
                else: o.append(w[i]); i+=1
            nw.append(o)
        words=nw
        if k in (5,10,20,40): print('   merges so far:',m, flush=True) if False else None
    return out,words
import alphabet as AB
rows=[r for r in csv.DictReader(open(AB.CORPUS),delimiter='\t') if r['text'] and r['ltype'].startswith('P')]
voy=[w for r in rows for w in r['text'].split('.') if AB.ok(w)]
lat=[w for w in re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower().replace('j','i').replace('v','u')) if not re.fullmatch(r'[ivxlcdm]+',w)][:len(voy)]
for name,W in [('Voynich',voy),('Latin',lat)]:
    res,final=bpe(W,120,list(range(15,200)))
    print(name)
    for inv,h1,h2,L in res:
        if inv in (20,22,24,26,28,30,35,40,50,60,80,100) or inv==res[0][0]: print(f'   units {inv:3d}: h1 {h1:.2f}  h2 {h2:.2f}  units/word {L:.2f}')
# reference: Latin split into rough syllables (onset consonants + vowel nucleus (+diphthong) ; trailing consonants attach to last syllable)
V='aeiouy'
def syl(w):
    parts=re.findall(r'[^aeiouy]*(?:ae|oe|au|[aeiouy])',w); 
    if not parts: return [w]
    rest=w[len(''.join(parts)):]; parts[-1]+=rest
    # move one consonant of a cluster to the coda of the previous syllable (VC.CV)
    out=[parts[0]]
    for p in parts[1:]:
        m=re.match(r'([^aeiouy]+)([^aeiouy].*)',p)
        if m and len(m.group(1))>=1 and not re.match(r'(qu|[bcdfgpt][rl])',p[len(m.group(1))-0:]): out[-1]+=m.group(1); out.append(m.group(2))
        else: out.append(p)
    return out
ls=[syl(w) for w in lat]
h1,h2=H(ls); inv=len({u for w in ls for u in w}); c=collections.Counter(u for w in ls for u in w); top=sum(v for _,v in c.most_common(60))/sum(c.values())
print(f'Latin syllables: inventory {inv}, top-60 cover {top:.2f} of tokens; h1 {h1:.2f} h2 {h2:.2f}; syllables/word {sum(map(len,ls))/len(ls):.2f}')
# reference: Maori (NT, ebible.org mri) split into its (C)V syllables
import glob, unicodedata
mt=' '.join(open(f,encoding='utf-8').read() for f in sorted(glob.glob('data/ext_poly/mri/mri_*_read.txt')) if '_000_' not in f).lower()
mt=unicodedata.normalize('NFKD',mt).encode('ascii','ignore').decode()
mw=[w for w in re.findall(r'[a-z]+',mt)][:len(voy)]
def msyl(w): return re.findall(r'(?:ng|wh|[hkmnprtw])?[aeiou]',w) if re.fullmatch(r'(?:(?:ng|wh|[hkmnprtw])?[aeiou])+',w) else None
ms=[s for s in (msyl(w) for w in mw) if s]
h1,h2=H(ms); c=collections.Counter(u for w in ms for u in w)
print(f'Maori syllables ({len(ms)} of {len(mw)} words parse as CV): inventory {len(c)}; h1 {h1:.2f} h2 {h2:.2f}; syllables/word {sum(map(len,ms))/len(ms):.2f}')
h1,h2=H([list(w) for w in mw]); print(f'Maori letters: h1 {h1:.2f} h2 {h2:.2f}; letters/word {sum(map(len,mw))/len(mw):.2f}')
