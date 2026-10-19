#!/bin/bash
# NOTES §80: v101 syllabary runs (A) and joined-uncertain-space runs of the word-level tests (B-E). Voynich targets only:
# the positive controls and generator baselines do not read the Voynich corpus and are those of the original runs.
cd /home/ds/Desktop/Voynich
for s in 1 2; do
  for U in 60 100; do
    CORPUS=data/corpus_GC.tsv ALPH=chars TRI=1 NULLK=30 timeout 14000 python3 syllabary.py voynich $s 400000 italian 60 $U > runs9/gc_tri_italian_${U}_$s.out 2>&1 &
    CORPUS=data/corpus_GC.tsv ALPH=chars TRI=1 NULLK=30 timeout 14000 python3 syllabary.py voynich $s 400000 catalan 60 $U > runs9/gc_tri_catalan_${U}_$s.out 2>&1 &
  done
  CORPUS=data/corpus_ZLjoin.tsv TRI=1 NULLK=30 timeout 14000 python3 syllabary.py voynich $s 400000 italian 60 60 > runs9/join_tri_italian_60_$s.out 2>&1 &
  CORPUS=data/corpus_ZLjoin.tsv TRI=1 NULLK=30 timeout 14000 python3 syllabary.py voynich $s 400000 catalan 60 100 > runs9/join_tri_catalan_100_$s.out 2>&1 &
  for L in latin italian catalan; do
    CORPUS=data/corpus_ZLjoin.tsv SUBSET=B timeout 9000 python3 wordcipher2.py voynich $s 10000000 300 1.0 $L > runs9/join_wc_${L}_$s.out 2>&1 &
  done
  for L in italian catalan; do
    CORPUS=data/corpus_ZLjoin.tsv timeout 14000 python3 codebook.py voynich $s 1500000 $L 300 > runs9/join_cb_${L}_$s.out 2>&1 &
  done
done
for s in 1 2 3; do for L in latin italian; do
  CORPUS=data/corpus_ZLjoin.tsv SUBSET=B HOLD=1 timeout 7200 python3 pairchipher.py voynich $s 4000000 $L > runs9/join_hold_${L}_$s.out 2>&1 &
done; done
wait
