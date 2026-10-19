#!/bin/bash
cd /home/ds/Desktop/Voynich
export SUBSET=B HOLD=1
for s in 1 2 3; do
  for t in control voynich markov shuffled; do
    timeout 7200 python3 pairchipher.py $t $s 4000000 > runs4/hold_${t}_$s.out 2>&1 &
  done
done
wait
grep -h -e "LM/char=" -e heldout runs4/hold_*.out
