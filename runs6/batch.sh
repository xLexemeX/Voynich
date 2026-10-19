#!/bin/bash
cd /home/ds/Desktop/Voynich
for L in italian latin; do for t in control voynich generator; do for s in 1 2; do
  timeout 14000 python3 codebook.py $t $s 1500000 $L 300 > runs6/cb_${L}_${t}_$s.out 2>&1 &
done; done; done; wait
grep -h "score/token" runs6/cb_*.out | sort
