"""Can any plausible transform of Latin reproduce the Voynich statistics? Try abbreviation-like transforms."""
import collections, math, re, random
random.seed(7)
def H(c):
    n=sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())
def stats(name,toks):
    toks=[t for t in toks if t][:38000]; c=collections.Counter(toks); text=' '.join(toks)
    h1=H(collections.Counter(text)); h2=H(collections.Counter(text[i:i+2] for i in range(len(text)-1)))-h1
    ml=sum(map(len,toks))/len(toks); sd=(sum((len(t)-ml)**2 for t in toks)/len(toks))**.5
    ws=[w for w,v in c.items() if v>=2]; S=set(ws); alpha=set(''.join(ws))
    nb=0
    for w in ws:
        for i in range(len(w)):
            if w[:i]+w[i+1:] in S: nb+=1
            for a in alpha:
                if a!=w[i] and w[:i]+a+w[i+1:] in S: nb+=1
    print(f'{name:38s} types {len(c):5d} hapax {sum(v==1 for v in c.values())/len(c):.2f} len {ml:.2f}±{sd:.2f} h2 {h2:.2f} nbr {nb/len(ws):.2f}')
lat=re.findall(r'[a-z]+',open('data/ref/latin_pliny.txt',encoding='utf-8',errors='replace').read().lower())
lat=[w for w in lat if not re.fullmatch(r'[ivxlcdm]+',w)]
V='aeiou'
stats('latin plain',lat)
stats('latin, vowels removed (not initial)',[w[0]+re.sub('[aeiou]','',w[1:]) for w in lat])
stats('latin, truncated to 5 letters',[w[:5] for w in lat])
stats('latin, truncated to 4',[w[:4] for w in lat])
stats('latin, first2+last2',[w if len(w)<=4 else w[:2]+w[-2:] for w in lat])
stats('latin, suspension (stem+last letter)',[w if len(w)<=3 else w[:3]+w[-1] for w in lat])
stats('latin, consonant skeleton + final vowel',[re.sub('[aeiou](?!$)','',w) for w in lat])
# syllable-as-word: split Latin into CV-ish syllables and treat each as a "word"
syl=[s for w in lat for s in re.findall(r'[^aeiou]*[aeiou]+[^aeiou]*?(?=[^aeiou][aeiou]|$)',w) if s]
stats('latin syllables as words',syl)
# digits: Latin with each letter -> 2-glyph code from a 6-symbol alphabet (verbose cipher, 36 codes)
sym='abcdef'; codes=[a+b for a in sym for b in sym]; random.shuffle(codes); cm={c:codes[i] for i,c in enumerate('abcdefghijklmnopqrstuvwxyz')}
stats('latin, verbose 2-glyph cipher (6 symbols)',[''.join(cm[c] for c in w) for w in lat])
print('--- reference: voynich  types 7829 hapax 0.69 len 4.97±1.83 h2 2.14 nbr 8.90')
