"""§51 again, with the page spelling profile of §75 instead of shared words: are herbal pages identified as the same plant
closer in profile (17 word-feature rates, z-scored within Currier language) than matched different-plant pairs?
Same null as §51: same language, similar folio distance. Power check: adjacent folios against pairs 10+ folios apart."""
import random, statistics, collections, math
import sameplant as S
from pageprofile import F
prof={f:[sum(map(fn,c.elements()))/sum(c.values()) for fn in F.values()] for f,c in S.pw.items() if sum(S.pw[f].values())>=60}
for L in set(S.lang.values()):
    fs=[f for f in prof if S.lang[f]==L]
    if len(fs)<2: continue
    for k in range(len(F)):
        v=[prof[f][k] for f in fs]; m=statistics.mean(v); sd=statistics.pstdev(v) or 1
        for f in fs: prof[f][k]=(prof[f][k]-m)/sd
def dist(a,b): return math.dist(prof[a],prof[b])
same=[(a,b) for a,b in S.same if a in prof and b in prof]
pairs=[(a,b) for a,b in S.pairs if a in prof and b in prof]
pool=collections.defaultdict(list)
for a,b in pairs:
    if not S.genera(a)&S.genera(b): pool[(S.lang[a],min(abs(S.fnum(a)-S.fnum(b))//10,6))].append((a,b))
key=lambda a,b:(S.lang[a],min(abs(S.fnum(a)-S.fnum(b))//10,6))
obs=statistics.mean(dist(a,b) for a,b in same); rng=random.Random(0)
null=[statistics.mean(dist(*rng.choice(pool[key(a,b)])) for a,b in same) for _ in range(5000)]
print(f'{len(same)} same-genus pairs: mean profile distance {obs:.3f}; matched different-genus pairs {statistics.mean(null):.3f} (sd {statistics.pstdev(null):.3f}); p(closer by chance) = {sum(x<=obs for x in null)/len(null):.3f}')
herb=[f for f in prof]
adj=[(a,b) for a in herb for b in herb if a<b and S.lang[a]==S.lang[b] and abs(S.fnum(a)-S.fnum(b))==1]
far=[(a,b) for a in herb for b in herb if a<b and S.lang[a]==S.lang[b] and abs(S.fnum(a)-S.fnum(b))>=10]
print(f'power check: adjacent folios ({len(adj)} pairs) {statistics.mean(dist(*p) for p in adj):.3f}; 10+ folios apart ({len(far)} pairs) {statistics.mean(dist(*p) for p in far):.3f}')
