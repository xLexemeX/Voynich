#!/bin/bash
cd /home/ds/Desktop/Voynich
for t in control voynich generator; do for s in 1 2 3; do
  timeout 9000 python3 syllabary.py $t $s 400000 italian 60 100 > runs5/homo_${t}_$s.out 2>&1 &
done; done; wait
grep -h "train score" runs5/homo_*.out | sort
