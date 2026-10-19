#!/bin/bash
cd /home/ds/Desktop/Voynich
for L in italian latin; do for K in 40 60 80; do for t in control voynich; do for s in 1 2; do
  [ "$L" = italian ] && [ "$K" = 60 ] && continue
  timeout 9000 python3 syllabary.py $t $s 400000 $L $K > runs5/syl2_${L}_${K}_${t}_$s.out 2>&1 &
done; done; done; done; wait
grep -h "score/token" runs5/syl2_*.out | sort
