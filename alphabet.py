"""Corpus and glyph-alphabet switch for the decipherment scripts (NOTES §80).
CORPUS: path of the corpus TSV (default data/corpus.tsv, ZL in EVA).
ALPH:   'eva' (words must be [a-z]+; EVA units as in each script) or 'chars' (any non-empty word; one character = one glyph,
        as in the v101 transliteration, data/corpus_GC.tsv)."""
import os, re, collections, csv
CORPUS=os.environ.get('CORPUS','data/corpus.tsv')
ALPH=os.environ.get('ALPH','eva')
def ok(w): return bool(re.fullmatch(r'[a-z]+',w)) if ALPH=='eva' else bool(w) and '.' not in w
def rare_folder(words, keep=25):
    """For ALPH=chars in the 1:1 letter-substitution tests: keep the `keep` commonest glyphs, fold the rest into one unit '¤'."""
    c=collections.Counter(ch for w in words for ch in w); top={ch for ch,_ in c.most_common(keep)}
    return lambda w: [ch if ch in top else '¤' for ch in w]
