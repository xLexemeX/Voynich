"""Stem model with a variation step (gen4.py p_mut): new one-shot words are made from page stems instead of selected."""
import gen4 as M, gen3_fit as G
from scorecard import card
from pageshuffle import shuffle
import random
R=card(G.REAL); _,RD=M.decomp(G.REAL)
K=['page-exclusive rate (40 pages)','hapax share of types','types/tokens','h2','mean word length']
print('real            '+' '.join(f'{k[:14]} {R[k]:.3f}' for k in K)+f' | page {RD[1]:+.3f} section {RD[2]:+.3f}', flush=True)
base=dict(group_lex=True, norm=True, n_sec=20, n_page=6, p_sec=0.5, topic_p=0.0, p_nh=0.0, p_nl=0.0, k_h=1, k_l=1)
for pm in (0.0,0.5,1.0):
  for pn in (0.22,0.30):
    for seed in (7,8):
        P=M.gen(seed,**dict(base,p_mut=pm,p_new=pn)); c=card(P); _,d=M.decomp(P)
        print(f'p_mut {pm:.1f} p_new {pn:.2f} s{seed} '+' '.join(f'{k[:14]} {c[k]:.3f}' for k in K)+f' | page {d[1]:+.3f} section {d[2]:+.3f}', flush=True)
