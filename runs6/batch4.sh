#!/bin/bash
cd /home/ds/Desktop/Voynich
for t in control voynich; do for s in 1 2; do
  timeout 14000 python3 codebook.py $t $s 1500000 catalan 300 > runs6/cb_catalan_${t}_$s.out 2>&1 &
done; done; wait
grep -h "score/token" runs6/cb_catalan_*.out | sort
