"""Stem model (gen4.py): how page-exclusive repetition rises as the page-level clustering of word forms is pushed toward
the real value. One parameter varied (p_kl, the share of lexicon draws pulled toward the page stems), two seeds each."""
import sys, json
import gen4 as M, gen3_fit as G
from scorecard import card
R=card(G.REAL); _,RD=M.decomp(G.REAL)
print(f"real: page part {RD[1]:+.3f}, section part {RD[2]:+.3f}, page-exclusive {R['page-exclusive rate (40 pages)']:.3f}, hapax share {R['hapax share of types']:.3f}", flush=True)
base=dict(group_lex=True, norm=True, n_sec=20, n_page=6, p_sec=0.5, topic_p=0.0, p_nh=0.0, p_nl=0.0, k_h=10, k_l=3, recent=0)
for k_l,p in [(3,0.0),(3,0.25),(3,0.5),(3,0.75),(3,1.0),(5,1.0)]:
    for seed in (7,8):
        P=M.gen(seed,**dict(base,k_l=k_l,p_kl=p)); c=card(P); _,d=M.decomp(P)
        print(f"k_l={k_l} p_kl={p:.2f} seed {seed}: page part {d[1]:+.3f}, section part {d[2]:+.3f}, page-exclusive {c['page-exclusive rate (40 pages)']:.3f}, hapax share {c['hapax share of types']:.3f}, h2 {c['h2']:.3f}", flush=True)
