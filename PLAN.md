# What would it take to decode it? A plan after NOTES.md §1–71

## Where the evidence points

**Excluded, with controls that recover a hidden key under the same conditions:**
- **Glyph-for-letter substitution, simple or homophonic:** Latin, Italian (§9, §16).
- **One word for one letter:** Latin, Italian, Catalan (§30–32, §70).
- **One word for a letter or letter pair (Naibbe form), held-out word-order test:** Latin, Italian, German, Hebrew, Catalan, Currier A and B (§37–39, §43, §68).
- **Small syllabary of onset+vowel signs:** Italian, Latin and Catalan, 40–80 signs, one-to-one (§61, §67). Homophonic for Italian and Catalan (§65, §71). Currier A and B separately (§71).
- **Word-for-word codebook:** Italian, Catalan (§62, §69).
- **Published sign tables:** Bax 2014, Cheshire 2017 (§45–49).

**Not excluded, because no control could be made to work:**
- Latin codebook (§62)
- Latin syllabary by cross-word gain (§65)
- homophonic syllabaries in languages other than Catalan and Italian
- any scheme whose units are not the frequency-based merges used here

**Facts any solution must explain:**
- the slot grammar of words, with prefix and suffix independent (§5, §8)
- line-position glyph variants, and the alternation of line-initial glyphs (§2, §23, §44)
- the `y | qo` junction (§20)
- low glyph entropy, matched by a small CV syllabary and by Polynesian languages, not by any European alphabet (§58–59)
- the a→e label switch at f72 (§24–26)
- 30 labels per zodiac sign with no shared sequence (§22, §63)
- labels that never reappear in the nearby text (§28, §56)
- herbal pages that keep no repeated page-specific name (§55)

## What could still move it forward

1. **An external anchor.** Every successful decipherment in history started from one: a bilingual, a known name, a cribbed phrase. The Voynich has none confirmed. Candidates:
   - The **f116v marginalia** and the **zodiac month names** are in Latin script. Determine by palaeography whether any Voynich-script glyphs inside them are glossed.
   - **Multispectral imaging** of erased or faded marginalia, the Beinecke's 2014 imaging and anything newer. It could reveal an owner's gloss or key.
   - **Plant identifications made blind to the text by botanists,** for the 20–30 most recognizable plants, to test §46-style hypotheses properly.
2. **Better language models for the codebook and syllable tests.** The word-level searches (§62, §69) were underpowered because word-bigram models are sparse. A class-based or small neural model of 15th-century Latin, Italian and Catalan would sharpen them. So would lemmatized Latin.
3. **Unit discovery not driven by frequency.** All syllabary tests used BPE merges chosen by frequency. A joint search over unit segmentation and key, with a held-out cross-word criterion, would test the syllabary family properly. It is computationally heavy, but feasible on a GPU.
4. **More reference texts of the right kind.** A Latin *prose* herbal (*Circa instans*, *Tractatus de herbis*) for §54–55. Occitan prose of the 15th century, which was not obtainable here. Medieval Hebrew and Judaeo-Romance.
5. **A generator that passes every statistic.** If a copy-and-vary procedure can reproduce all the facts above, including the junction rule, line alternation and the page-exclusive repetition rate (§55: current generator 0.96 vs real 0.06), the meaningless-text hypothesis becomes concrete and testable. No generator so far does.

## Honest expectation

Within the families tested, there is no plaintext to find: every control-calibrated search ends at the level of gibberish. A decoding, if one exists, will come from an external anchor or from a scheme outside these families. It will not come from more searches of the same kind.
