#!/bin/bash
cd /home/ds/Desktop/Voynich
export SUBSET=B HOLD=1
for s in 1 2 3; do
  for L in italian german; do
    for t in control voynich; do
      timeout 7200 python3 pairchipher.py $t $s 4000000 $L > runs4/hold_${L}_${t}_$s.out 2>&1 &
    done
  done
done
wait
grep -h -e "LM/char=" -e heldout runs4/hold_italian_*.out runs4/hold_german_*.out
