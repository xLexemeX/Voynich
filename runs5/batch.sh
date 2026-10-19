#!/bin/bash
cd /home/ds/Desktop/Voynich
for s in 1 2 3; do for t in control voynich generator; do
  timeout 7200 python3 syllabary.py $t $s 400000 > runs5/syl1_${t}_$s.out 2>&1 &
done; done; wait
grep -h "score/token" runs5/syl1_*.out
