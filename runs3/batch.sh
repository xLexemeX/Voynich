#!/bin/bash
cd /home/ds/Desktop/Voynich
export SUBSET=B
for s in 1 2; do
  timeout 7200 python3 wordcipher2.py voynich $s 10000000 300 1.0 latin > runs3/voynichB_latin_$s.out 2>&1 &
  timeout 7200 python3 wordcipher2.py voynich $s 10000000 300 1.0 italian > runs3/voynichB_italian_$s.out 2>&1 &
  timeout 7200 python3 wordcipher2.py control $s 10000000 300 1.0 latin -1 > runs3/controlB_latin_$s.out 2>&1 &
  timeout 7200 python3 wordcipher2.py control $s 10000000 300 1.0 italian -1 > runs3/controlB_italian_$s.out 2>&1 &
done
wait
grep -h 'LM/char=' runs3/*.out | sort | cut -c1-230
