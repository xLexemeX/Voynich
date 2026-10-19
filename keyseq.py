"""Do the single-glyph sequences (f57v ring 3 period, f57v ring 5 head, f66r and f49v margin columns) share an ordering?"""
import random
P='o l d r v x k m f 169 v t r 170 171 y c 172'.split()          # f57v ring 3, one period of 17 (+ 'v' after 169 joined in ZL)
seqs={'f57v ring 5 (single glyphs before the first word)':'o v l r m aiin d 170 c f s y l k x l r 171'.split(),
      'f66r margin single glyphs':'y o s sh y d o f 169 x air d sh y f f y o d s f c 172 x t o 195 l r t o x p d'.split(),
      'f49v margin column':'f o r y e 140 k s p o 192 y e 140 164 p o 192 y e 140 d y e k y'.split()}
def lcs(a,b):
    D=[[0]*(len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)):
        for j in range(len(b)): D[i+1][j+1]=D[i][j]+1 if a[i]==b[j] else max(D[i][j+1],D[i+1][j])
    return D[-1][-1]
def best(s):  # P is cyclic; allow any rotation, and up to two passes round the cycle
    return max(lcs(s,(P[r:]+P[:r])*2) for r in range(len(P)))
random.seed(0)
for name,s in seqs.items():
    o=best(s); null=[]
    for _ in range(2000): t=s[:]; random.shuffle(t); null.append(best(t))
    print(f'{name}: n={len(s)} LCS with ring-3 cycle {o}; shuffled mean {sum(null)/len(null):.2f}, p={sum(x>=o for x in null)/len(null):.4f}')
