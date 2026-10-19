#!/bin/bash
cd /home/ds/Desktop/Voynich
export TRI=1 NULLK=30
for t in control voynich; do for s in 1 2 3; do
  timeout 14000 python3 syllabary.py $t $s 400000 catalan 60 60 > runs5/tricat_${t}_$s.out 2>&1 &
done; done; wait
grep -h -e "train score" -e "random-key" runs5/tricat_*.out | cut -c1-260
