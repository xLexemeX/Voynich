# Voynich working folder

Start with `NOTES.md`. Scripts are Python 3 (numpy only). Regenerate everything with:

    python3 parse_ivtff.py     # data/corpus.tsv from data/ZL3b-n.txt (download from voynich.nu if missing)
    python3 stats1.py; python3 compare.py; python3 structure.py; python3 tests2.py; python3 tests3.py
    python3 tests4.py; python3 tests5.py; python3 transforms.py; python3 generators.py; python3 generators2.py
    python3 wordclasses.py; python3 linegrammar.py
    python3 decipher.py latin|voynich|markov [seed] [iters]
    python3 reading.py f1r     # annotated reading of any folio -> readings/f1r.md

Reference texts (data/ref/) and page images (pages/, hires/) are not committed; `pdftoppm -r 100 -png ../Voynich_Manuscript.pdf pages/p` rebuilds the pages.
