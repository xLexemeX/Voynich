#!/bin/bash
cd /home/ds/Desktop/Voynich
export SUBSET=B
for s in 1 2 3; do
  timeout 9000 python3 wordcipher2.py voynich $s 10000000 300 1.0 catalan > runs7/voynichB_catalan_$s.out 2>&1 &
  timeout 9000 python3 wordcipher2.py control $s 10000000 300 1.0 catalan -1 > runs7/controlB_catalan_$s.out 2>&1 &
done
wait
grep -h 'LM/char=' runs7/*.out | sort | cut -c1-240
