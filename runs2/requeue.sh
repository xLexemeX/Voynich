#!/bin/bash
cd /home/ds/Desktop/Voynich
while pgrep -f '^python3 wordcipher2.py' >/dev/null; do sleep 15; done
run_batch() {
  for job in "$@"; do
    set -- $job
    case $1 in
      cl) timeout 7200 python3 wordcipher2.py control $2 10000000 300 1.0 latin 0.38 > runs2/control_latin_drop_$2.out 2>&1 & ;;
      ci) timeout 7200 python3 wordcipher2.py control $2 10000000 300 1.0 italian 0.38 > runs2/control_italian_drop_$2.out 2>&1 & ;;
      vi) timeout 7200 python3 wordcipher2.py voynich $2 10000000 300 1.0 italian > runs2/voynich_italian_$2.out 2>&1 & ;;
      mi) timeout 7200 python3 wordcipher2.py markov $2 10000000 300 1.0 italian > runs2/markov_italian_$2.out 2>&1 & ;;
    esac
  done
  wait
}
run_batch "ci 1" "ci 2" "cl 1" "cl 2" "vi 1" "vi 2" "mi 1" "mi 2"
run_batch "ci 3" "ci 4" "ci 5" "cl 4" "vi 3" "vi 4" "mi 3" "mi 4"
grep -h 'LM/char=' runs2/*.out | sort | cut -c1-240
