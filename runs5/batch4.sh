#!/bin/bash
cd /home/ds/Desktop/Voynich
export TRI=1
for U in 60 100; do for t in control voynich generator; do for s in 1 2 3; do
  timeout 14000 python3 syllabary.py $t $s 400000 italian 60 $U > runs5/tri_${U}_${t}_$s.out 2>&1 &
done; done; done; wait
grep -h "train score" runs5/tri_*.out | sort | cut -c1-260
