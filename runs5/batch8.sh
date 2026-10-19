#!/bin/bash
cd /home/ds/Desktop/Voynich
export TRI=1 NULLK=20
for S in A B; do for U in 60 100; do for s in 1 2; do
  SUBSET=$S timeout 14000 python3 syllabary.py voynich $s 400000 catalan 60 $U > runs5/tricatAB_${S}_${U}_$s.out 2>&1 &
done; done; done; wait
grep -h -e "train score" -e "random-key" runs5/tricatAB_*.out | cut -c1-200
