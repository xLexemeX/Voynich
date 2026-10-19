# Voynich Manuscript — working notes

Working folder: `~/Desktop/Voynich/`. Source: `~/Desktop/Voynich_Manuscript.pdf` (209 page scans, Beinecke MS 408, no text layer).

Every claim below is either (a) something I computed and you can re-run with the script named, or (b) marked as background knowledge from the literature. I am not going to invent a translation. I am going to try to pin down what the writing system *is*, because that is the step every past "translation" skipped, and every one of them failed for exactly that reason.

## 0. Honest framing

- Nobody has translated this text. Claimed decipherments (Bax, Cheshire, Gibbs, Ardic, Hauer & Kondrak's "Hebrew", Yale's "Latin abbreviation" ideas) do not survive testing: they only work on cherry-picked words and cannot be applied consistently across the whole text.
- What *is* solid is a body of statistical facts about the text. Those facts constrain what it can be. My plan is to reproduce those facts myself, then use them to test concrete hypotheses one by one, and write down what survives.
- I will keep a scoreboard in section 9 of hypotheses with the evidence for and against.

## 1. Materials

| File | What |
|---|---|
| `pages/p-NNN.png` | page scans extracted from the PDF at 100 dpi (`pdftoppm`) |
| `data/ZL3b-n.txt` | Zandbergen–Landini EVA transliteration v3b (May 2025), IVTFF format, from voynich.nu |
| `data/RF1b-e.txt`, `data/VT0e-n.txt`, `data/LSI_ivtff_0d.txt` | other transliterations (Rene Zandbergen RF, Takahashi VT, Landini-Stolfi interlinear) for cross-checking |
| `data/corpus.tsv` | cleaned one-line-per-row corpus with folio, line, quire, Currier language (A/B), hand, section |
| `parse_ivtff.py` | builds corpus.tsv |
| `stats1.py` | baseline statistics (output in `data/stats1.out`) |

EVA ("European Voynich Alphabet") is a *transliteration*, not a decipherment: each Voynich glyph gets an ASCII letter so we can compute on it. `daiin` in EVA means the glyph sequence d-a-i-i-n; it does not mean the sound "daiin".

Sections (Zandbergen's codes): herbal, astro, zodiac, bio (the bathing women / "balneological"), cosmo, pharma, stars (the dense text-only "recipes" section), text.

## 2. Baseline facts (computed, `stats1.py`)

- 38,575 word tokens, 7,890 distinct word types. 68.7% of word types appear exactly once.
- Word length: mean 4.96 glyphs, tight peak at 4–6, very few words over 9. Natural languages have a much wider spread (long words exist).
- Most common words: `daiin` 844, `ol` 564, `aiin` 508, `chedy` 507, `shedy` 435, `ar` 400, `chol` 397, `or` 393.
- Character entropy (with spaces): h1 = 3.89 bits, conditional h2 = 2.14 bits. Latin/English are typically h2 ≈ 3.0–3.5 in the same alphabet-size range. Voynichese is far more *predictable* glyph-to-glyph than any known plain language. This is the single most important constraint on any theory.
- Currier A vs B are real: top words in A (`daiin chol chor shol cthy`) vs B (`chedy shedy qokeedy qokedy qokain`) barely overlap. The `ed`/`edy` and `qok-` words are almost entirely B.
- Line effects are strong:
  - line-initial word is disproportionately `daiin`, `y`, `saiin`, `sol`, `sar`, `sor`; first *character* of a line is `o d s y q t p` — `p`/`t` (the tall "gallows") are heavily line-initial (actually paragraph-initial).
  - line-final characters: `y` (40% of all words end in y anyway) then `m`, `n`, `l`, `r`, `g`. `m` and `g` are almost exclusively line-final. So the *same word* is written differently depending on where it sits in the line. That is a scribal/positional feature, not a linguistic one.
- Word-initial chars: `o` 22%, `c(h)` 18%, `q` 14%, `s` 12%, `d` 10%. `q` is essentially always followed by `o`.
- Word-final chars: `y` 40%, `n` 16%, `l` 15%, `r` 15%. Four endings cover 86% of all words.
- 302 places where the same word is written twice in a row (e.g. `daiin daiin`). Natural prose almost never does this; it happens ~0.8% of word pairs here.

## 3. Work log
(most recent at bottom)

- Extracted pages, downloaded ZL/RF/VT/LSI transliterations, wrote parser, ran baseline stats.

## 4. Cross-language comparison (`compare.py`, output `data/compare.out`)

All texts truncated to 38,000 tokens so the numbers are comparable. h2 = conditional character entropy (how unpredictable the next glyph is given the current one).

| text | types | hapax | word len (mean±sd) | h2 with spaces | h2 no spaces | adjacent repeats |
|---|---|---|---|---|---|---|
| Voynich (EVA) | 7,829 | 0.69 | 4.97 ± 1.83 | **2.14** | 2.36 | 0.81% |
| Voynich, common digraphs merged | 7,829 | 0.69 | 3.90 ± 1.41 | 2.46 | 2.81 | 0.81% |
| Latin (Pliny) | 10,599 | 0.70 | 5.48 ± 2.58 | 3.22 | 3.36 | ~0 |
| Italian (Dante) | 6,886 | 0.61 | 3.91 ± 2.22 | 3.12 | 3.39 | 0.05% |
| German (Faust) | 6,583 | 0.59 | 4.47 ± 2.44 | 3.26 | 3.49 | 0.17% |
| English (Austen) | 4,186 | 0.49 | 4.39 ± 2.45 | 3.31 | 3.60 | 0.06% |
| Hebrew (Genesis, consonantal) | 3,931 | 0.66 | 4.37 ± 1.36 | 3.52 | 3.85 | 0.14% |

What this means:
- Vocabulary size and hapax rate look like a *real, inflected* language (close to Latin). Zipf slope is −1.08, normal.
- But glyph predictability is far outside the natural range. A **simple substitution cipher cannot produce this** (substitution preserves entropy exactly). So "Voynich = language X with letters swapped" is dead on arrival, whatever X is. This kills the majority of published "solutions" in one line.
- Word length spread (sd 1.8) is much narrower than any language (sd 2.2–2.6). There are no long words. Real language has "et" and "circumstantibus" in the same text; Voynichese does not.
- Adjacent identical words are 10–15× more common than in prose.

## 5. Word structure (`structure.py`, output `data/structure.out`)

- **Glyphs have fixed positions.** `q` is word-initial 99% of the time (and followed by `o` 98%). `n`, `m` are word-final 95–99%. `e`, `h`, `i` are never initial or final. `y` is final 86%. This is nothing like an alphabet used for a language, where most letters can appear anywhere; it looks like a *slot system*.
- A hand-written slot regex `(q)(o)(gallows/ch/sh/d/s/l/r)(e/o/a)(gallows/ch/sh/d/s)(e/ai/aii/o)(n/m/l/r/y/dy/s/g)` matches 86% of all tokens. Stolfi's "crust–mantle–core" paradigm is essentially this.
- Within a word, the next glyph is highly predictable: `c`→`h` 84%, `q`→`o` 98%, `n`→end 99%, `i`→`n`/`i` 91%, `d`→`y` 53%.
- **Neighborhood density.** Among word types seen at least twice, a Voynich word has on average **8.9** other words at edit distance 1. Latin: 1.3. Italian: 3.3. German: 3.5. The Voynich lexicon is a dense cloud of near-identical strings (`chedy/shedy/chey/shey/qokedy/qokeedy/okedy...`).
- **Self-citation (Timm & Schinner).** Minimum edit distance from a word to the other words on its own line is 2.57, versus 3.16 to words on a random line. Latin shows a much smaller effect (4.17 vs 4.54), Italian none. Words on a line look like variations of each other. Reproduced.

## 6. More tests (`tests2.py`, `tests3.py`)

- **Verbose cipher ceiling.** If each plaintext letter were written as 2 glyphs, merging glyph pairs should restore natural-language entropy. Greedy merging of the 12 most frequent bigrams (ch, dy, ai, ok, ol, ee, sh, in, …) only raises h2 from 2.14 to 2.75, still below every natural language, while cutting mean word length to 3.35. A verbose cipher alone does not explain the text. (Not a proof: the merge search is greedy and only 12 steps. Noted as partial.)
- **Labels** (single words beside plants, stars, nymphs): 781 tokens, 86% hapax, only 48% ever occur in running text. Labels almost never begin with `q` (1.4% vs 15% in text). So whatever `q` is, it is a *running-text-only* thing, not part of a name. 52% of labels start with `o`.
- **Position in line changes the word.** First word of a line: longer (5.42 vs ~4.9), 25% start with a gallows letter (vs 5–6% elsewhere). Last word: shorter (4.64), 19.5% end in `m`/`g` (vs ≤1.8% elsewhere), and `q`-initial drops to 9%. Page-initial words start with `p`/`t`/`k`/`f` in 158 of 173 pages. The line is a functional unit and the glyph shapes are decorated by position.
- **Page topicality.** Two halves of the same page share 10.1% of vocabulary (Jaccard); two random pages share 5.1%. Latin: 6.0% vs 2.9%. Italian: 11.9% vs 10.7%. Voynich pages are at least as "topical" as Latin prose. Consistent with either meaningful text or with local copying.
- **Word-order syntax.** Excess mutual information between adjacent words (above the shuffled baseline): Voynich 0.18 bits, Latin 0.31, Italian 0.46, English 0.72. There is *some* word-order structure, but the weakest of the set. Latin (free word order) is the nearest.
- Similarity between line i and line i+k is flat with k in Voynich (0.031 → 0.026), similar to Latin. Not decisive.

## 7. Where this leaves the hypotheses (scoreboard)

| Hypothesis | Status | Evidence |
|---|---|---|
| H1 Natural language, simple substitution | **dead** | h2 2.1 vs ≥3.1; positional glyph rules; neighborhood density |
| H2 Natural language, verbose cipher (1 letter → 2+ glyphs) | weak | merging bigrams doesn't reach natural entropy; word length too uniform |
| H3 Abbreviated / shorthand Latin | open | hapax & Zipf are Latin-like; but a shorthand should show long-word tails |
| H4 Meaningless text from a generative procedure (Rugg grille / Timm self-citation) | fits all stats | but "fits" ≠ "proven"; a real language passed through an unusual encoding could also fit |
| H5 Codebook / nomenclator (words = code numbers) | poor | 69% hapax is far too many code entries |
| H6 Constructed / a priori language (Cathar, philosophical language) | open | slot structure is what a category system would look like |

## 8. Further structure tests (`tests4.py`, `tests5.py`, `tests6.out`)

- **Vowel/consonant separation (Sukhotin's algorithm).** On Latin it correctly finds i e a u o. On Voynichese it picks `o a y` (and `e` once ch/sh are merged). So the script *does* have a vowel-like class, which is what you'd expect of an alphabet or a syllabary, and not what a pure random-table generator produces unless designed to.
- **Line-final `m`.** Stems that take `-am` at line end take `-al`, `-aiin`, `-ar`, `-ain` elsewhere in roughly equal measure. So `m` is a line-end allograph for the whole ending class, not for one specific ending. (Reproduces the "line as functional unit" observation.)
- **`i` runs are not tallies.** Counts: one `i` 2,499, two 4,365, three 180, four 1. A tally system would be geometric; this looks like three distinct glyphs (`in`, `iin`, `iiin`) with `iin` the default. The runs are preceded by `a` 95% of the time and followed by `n` 80%.
- **A/B is a gradient, not a switch.** Per-page glyph-bigram profiles projected on their first principal component: A pages mean −0.057, B pages +0.051, but the ranges overlap (A up to +0.017, B down to +0.002) and the histogram has mass all along the axis. In quire order, the share of `-edy` words goes 0% (quires A–C) → 7–11% (D–F) → 25% (quire M, the bio section) → 15% (quire T, stars). `daiin` falls from 5% to 1% across the same span. This looks like a system that drifted as it was written (or one scribe's habits changing), not two languages.
- **No agreement between neighbors.** In Latin, the ending of a word predicts the ending of the next (adjective–noun agreement): excess MI 0.40 bits. In Voynichese: 0.04 bits. There is no inflectional agreement.
- **But the word boundary is not neutral.** A word ending in `y` is followed by a `q`-word 1.8× more often than chance and by an `a`-word 6× *less* often; `r|a` 3×; `o|r` 6×; `s|a` 5×. Whatever produces the text "sees across" the space.
- **Prefix and suffix are independent.** Decomposing 29.5k tokens into prefix (`qo/o/q/y/s/d/ch/sh`) + core + suffix (`aiin/ain/dy/edy/ey/y/ol/al/or/ar/…`): MI(prefix, suffix) = 0.08 bits (shuffled baseline 0.003) versus Latin 1.17. The core does constrain the suffix (excess MI ≈ 0.96 bits, Latin ≈ 1.4). Prefix and suffix are chosen essentially independently of each other, which is how a *combinatorial code* behaves and not how morphology behaves.
- Zipf's law of abbreviation (frequent words are short) holds: r = −0.32 (Latin −0.29).
- **Labels reused across sections:** `okol`, `otedy`, `otol`, `okain`, `otchdy`, `okaiin`, `otaly`, `okary` … each on 4–6 different folios spanning zodiac, bio, pharma, cosmo. Almost every multi-folio label has the shape `o + gallows(k/t) + ending`. Labels are a restricted sub-vocabulary.

## 9. Controlled decipherment experiment (`decipher.py`, `data/decipher.out`)

Question: if Voynich glyph-units (26 units: `ch sh cth ckh cph cfh iin in ee` plus single glyphs) map onto Latin letters, with up to 4 units allowed to be nulls and many-to-one allowed, can a search find the mapping? Objective = Latin character 4-gram log-likelihood (trained on Pliny, Roman numerals removed), optimized by simulated annealing (25k steps). Judge by % of decoded words found in a Latin dictionary.

| input | LM score / char | decoded words in Latin dictionary (≥4 letters) |
|---|---|---|
| Latin text under a random substitution (positive control) | −1.98 | **93.7%** (text recovered, readable) |
| Voynich text | −2.76 | 15.0% |
| Meaningless text from a Voynich-like Markov generator (negative control) | −2.96 | 15.0% |

The method works when there is Latin to find. On the Voynich text it returns the same junk (`uis iis sis uisa…`) it returns on meaningless text. First attempt (before I fixed the objective) it "found" a solution by deleting every glyph and reading the leftovers as `i i ii`: that is exactly the failure mode of the published "solutions", and it is why any claimed decipherment must be run with controls.

**Conclusion:** substitution or homophonic-substitution into Latin is excluded at this scale. I can run the same experiment against other target languages (Italian, German, Hebrew) but the entropy argument in §4 already covers all of them: a substitution cannot lower h2 from 3.1+ to 2.1.

## 10. Word-length argument against a verbose cipher with real spaces

If each plaintext letter were written as k glyphs, word length sd would be k × (plaintext sd). Latin sd = 2.6 letters. Voynich sd = 1.8 glyphs. So k would have to be < 0.7, i.e. *compression*, not verbosity. The only escapes are (a) spaces are not word boundaries, or (b) the plaintext is not a normal language (abbreviations, a list, numbers). Against (a): glyph position rules at word edges are extremely sharp (`q` 99% initial, `n` 99% final), so spaces are structurally real even if not linguistically real.

## 11. Can any abbreviation of Latin look like this? (`transforms.py`)

Took real Latin (Pliny) and applied scribal-abbreviation-style transforms, then measured the same statistics.

| transform of Latin | types | hapax | word len | h2 | edit-1 neighbors |
|---|---|---|---|---|---|
| plain | 13,684 | 0.71 | 6.07 ± 2.71 | 3.40 | 0.9 |
| vowels removed (except initial) | 9,567 | 0.62 | 3.60 ± 1.63 | 3.30 | 8.5 |
| truncated to 5 letters | 7,502 | 0.49 | 4.37 ± 1.09 | 3.47 | 2.8 |
| first 2 + last 2 letters | 5,355 | 0.37 | 3.67 ± 0.71 | 3.28 | 13.9 |
| consonant skeleton + final vowel | 10,556 | 0.63 | 3.75 ± 1.71 | 3.27 | 8.0 |
| syllables treated as words | 2,157 | 0.40 | 2.54 ± 0.82 | 2.98 | 13.6 |
| verbose 2-glyph cipher, 6-symbol alphabet | 13,684 | 0.71 | 12.1 ± 5.4 | 2.48 | 0.1 |
| **Voynich** | 7,829 | 0.69 | 4.97 ± 1.83 | **2.14** | 8.9 |

Abbreviation can reproduce the short, regular words and the dense neighborhoods, but *never* the low glyph entropy: every abbreviated Latin stays at h2 ≥ 3.27. The only transform that lowers h2 is a verbose cipher, which blows up word length. No single transform reproduces the whole profile. Whatever Voynichese is, it has *both* a small effective alphabet with rigid ordering *and* a vocabulary with Latin-like richness.

## 12. Do the "meaningless text" generators reproduce everything? (`generators.py`)

| | types | hapax | word len | h2 | nbrs | same-line vs random dist | adjacent repeats | word-order MI |
|---|---|---|---|---|---|---|---|---|
| Voynich (paragraph text) | 6,983 | 0.68 | 4.97±1.80 | 2.11 | 6.8 | 2.52 vs 3.16 | 0.82% | 0.18 |
| table-and-grille (independent slots, my implementation) | 13,290 | 0.69 | 5.53±1.96 | 2.48 | 8.9 | 3.42 vs 3.53 | 0.05% | 0.00 |
| self-citation (copy-and-mutate, my implementation) | 11,072 | 0.68 | 2.99±1.34 | 3.61 | 24.0 | 1.65 vs 2.43 | 0.72% | 0.02 |

A naive grille gets the entropy nearly right but produces no line-locality, no repeats, and no word-order dependence. A naive self-citation gets the line-locality and repeats but wrecks the glyph statistics. The real text has all of these at once. That doesn't rescue "it's a language", but it does mean the popular "it's a Rugg grille / it's a Timm copy-machine" explanations are, in their simple forms, *also* insufficient. Anyone claiming a generator explains it should have to pass this whole table. (A tuned generator that mutates only within the slot grammar and copies from nearby lines might; that is a future experiment.)

## 13. What is actually readable on the pages

- The zodiac wheels (PDF pages ~124–131; f70v2 Pisces, f71r Aries, …) carry month names in a *later* hand in Latin script (`mars`, `abril`, `may`, `yony`, `jollet`, `augst`, `septembre`, `octembre`, `novembre`, `decembre`), in a Franco-Occitan spelling. This is literature knowledge; in this PDF the foldouts are shrunk to ~770 px and the names are not legible. They tell us an early owner labeled the signs, and nothing about the Voynich script.
- f1r right margin: a later hand wrote `a b c d e f g h i k … o p q r` beside the first lines, as if trying a key (noted in the ZL transcription's comments). It doesn't align with the text and is not a key.
- Last page f116v has the "michiton oladabas" line in Latin letters mixed with Voynich glyphs. Unsolved; probably a charm.
- I generated annotated per-word readings for sample folios in `readings/` (`f1r`, `f2r`, `f26r`, `f78r`, `f103r`, `f70v2`, `f67r1`). Each word is shown with its manuscript-wide count, A/B split, sections, slot decomposition and nearest spelling variants. Run `python3 reading.py <folio>` for any other page.

## 14. Word classes from context (`wordclasses.py`)

Clustering the 300 most frequent words by what appears to their left and right (k-means, 8 classes) gives classes that line up with *spelling*:
- a class of `qo-…-edy/-eey/-dy` words (`qokeedy qokeey qokedy qokal okeey …`)
- a class of `ch/sh-…-edy/-y` words (`chedy shedy chey shey cheey …`)
- a class of `…-aiin/-ar/-al/-ain` words (`ol dar qokaiin dal okaiin okal otar …`)
- a class of very short `-r/-s` words (`or ar s r sar sor tar lor …`)
- a big residual class of A-language words (`daiin chol chor shol cthy …`)

Mutual information between class and suffix is 0.75 bits of the 2.25 bits of class entropy; with prefix 0.48 bits. So a word's *behavior in context* is largely readable off its ending. In an inflected language that is partly true too (case endings signal role), so this is consistent with both a language and a code, but it says the endings are functional, not decorative.

## 15. Is there syntax between ending-classes along a line? (`linegrammar.py`)

Words grouped into 6 classes by ending (EDY, Y, N, L, R, other). Observed/expected ratios for class *i* → class *i+1* are almost identical to the ratios obtained after shuffling the words *within each line*. Example: EDY→EDY 1.31 observed vs 1.16 shuffled; R→R 1.30 vs 1.29; Y→Y 1.34 vs 1.32. Run lengths of same-class words match the shuffle too. So the "same class follows same class" tendency comes from *lines* having different mixes (some lines are full of -edy words), not from any word-to-word rule. Within a line, the order of ending-classes is statistically random, apart from the last position (N-class words rise from 17% to 28% at line end; EDY drops from 30% to 23%).

This is a strong negative result for "sentence grammar": in a language, adjectives and nouns and verbs are not shuffled freely within a line.

## 16. Decipherment experiment repeated with Italian as target (`decipher_it.py`)

Italian positive control (Dante under random substitution): 100% dictionary words after search, text readable. Voynich → Italian: 20.5% dictionary words at ≥4 letters, output like `tan ame e de se sea tein a me sera`. Same verdict as Latin.

## 17. A tuned generator gets close, but one thing is left over (`generators2.py`)

Self-citation constrained to the slot grammar (copy a word from the current or previous two lines, replace one slot with a table draw; 12% verbatim copies):

| | types | hapax | word len | h2 | nbrs | same-line vs random | repeats | word-order MI |
|---|---|---|---|---|---|---|---|---|
| Voynich | 6,983 | 0.68 | 4.97±1.80 | 2.11 | 6.8 | 2.52 vs 3.16 | 0.82% | **0.18** |
| slot-constrained self-citation | 11,191 | 0.58 | 5.54±1.93 | 2.46 | 7.4 | 2.75 vs 3.57 | 0.86% | **0.01** |

Everything is now in the right neighborhood except the excess adjacent-word mutual information. The real text has a specific *sequential* preference that copying cannot produce.

## 18. What the sequential preference is (`data/pmi.out`)

The most over-represented adjacent pairs fall into two groups:
1. **Split words.** `o l` (PMI 5.0), `s aiin` (4.0), `r aiin`, `or aiin`, `ar al`, `s ar`. These are almost certainly single words (`ol`, `saiin`, `raiin`, `oraiin`, `aral`, `sar`) that the scribe or the transcriber broke with a space. `saiin` is itself the third most common line-initial word.
2. **`-edy` → `qo-`.** `shedy qokedy`, `shey qokain`, `chedy qokain`, `chedy qokeey`, `shedy qokaiin`, `qol chedy`, `ol shedy`. A `ch/sh…y` word is followed by a `qo…` word far more than chance, and `qo…` words are almost never labels (§6). The chain `ol → chedy/shedy → qokedy/qokain` looks like a fixed phrase skeleton in language B. It is the best candidate I have for a "grammatical" pattern, and it needs to be explained by any theory. It's also compatible with `qo` being a prefix that attaches to what follows a `-y` word (a linking particle, or a space that isn't a real boundary).

Removing identical-word pairs does not change the MI (5.55 → 5.59), so repeats aren't the source.

## 19. Where things stand, and what to do next

**What I can say with evidence in hand:**
1. The text is not a natural language under any substitution (simple, homophonic, or into Latin/Italian specifically). §4, §9, §16.
2. It is not an abbreviation of Latin, and not a simple verbose cipher of a language with real word spaces. §10, §11.
3. Its words are built from a rigid slot system (prefix · core · suffix) in which prefix and suffix are chosen independently, endings determine a word's context behavior, and glyph shapes change with line position. §5, §8, §14.
4. Word order within a line carries very little information: the sequence of ending classes is indistinguishable from a within-line shuffle. §15. Neighboring words do not agree. §8.
5. Words are strongly local: they resemble the other words on their line, and pages are more self-similar than Latin prose. §5, §6.
6. Simple "meaningless generator" models do not reproduce the whole statistical profile either; a tuned self-citation model reproduces all of it except a sequential `…y → qo…` preference. §12, §17, §18.

**My current best reading of the evidence:** the writing is a *system*, not a language put through a cipher. The two live options are (a) a constructed notation (a category or numbering system, in which each "word" is a coded item and the running text is a list rather than prose), or (b) a text produced by a procedure that mostly copies-and-varies. The `y → qo` linkage and the topical page structure lean me slightly toward (a) over (b), but I would not bet heavily. Nothing here supports (c) "a real language waiting for the right key".

**Next experiments, in order of value:**
- Build a per-line "template" model: represent each line as a sequence of slot-triples and check whether lines in the stars section follow a small number of templates (as a list/recipe notation would).
- Test whether `qo` is a separable particle: compare the distribution of `X` vs `qoX` for the same X across positions and sections.
- Fit a proper Hidden Markov Model over glyphs (3–6 states) and compare the learned states to the slot grammar; do the same for Latin as a control.
- Label study: for the pharma jars and the star labels, test whether labels on the same page share prefixes more than labels across pages (a numbering scheme would show this).
- Get a higher-resolution scan (Beinecke's public scans are ~5000 px) so the illustrations, the month names, and the marginalia can be read; this PDF is too low-res for that.

## Appendix: EVA glyph key (so you can read the readings)

| EVA | what the glyph looks like | behavior |
|---|---|---|
| `o` | small circle | most common; word-initial or medial |
| `a` | like a Latin a | medial; almost always followed by `i`, `r`, `l` |
| `y` | like a 9 with a tail | ends 40% of words; also word-initial |
| `e` | like a c | medial only, often doubled (`ee`) |
| `ch` | two c's joined by a bar (one glyph) | very common word-initial |
| `sh` | `ch` with a hook on top | like `ch` |
| `i` | a minim (short stroke) | only in runs `in`, `iin`, `iiin` after `a`/`o` |
| `n` | final minim with a curl | ends the `-aiin` group |
| `d` | like an 8 | initial (`daiin`) or before `y` (`-dy`) |
| `l` | like a knotted loop | common word-final |
| `r` | like a hooked stroke | common word-final |
| `s` | like `r` with a flourish | initial (`s`, `saiin`) or final (line-end) |
| `k` `t` `p` `f` | the tall "gallows" letters (one or two loops, one or two legs) | `k`/`t` medial after `o`; `p`/`f` mostly paragraph-initial |
| `cth` `ckh` `cph` `cfh` | a gallows drawn on top of a `ch` ("pedestal" gallows) | mostly A-language, herbal |
| `q` | like a 4 with a tail | only word-initial, only before `o` |
| `m` `g` | flourished finals | line-end variants of other endings |

## 20. Follow-up experiments (`data/qo.out`, `hmm.py`, `data/templates.out`)

- **`qo` is conditioned by the previous word.** 104 stems occur both bare (`okaiin`, `okeey`, `okedy`, `ol` …) and with `q` (`qokaiin`, `qokeey` …); totals 4,771 bare vs 4,205 q-forms, so it is a productive alternation, not separate vocabulary. The word *before* a q-form ends in `y` 75% of the time; before the bare form, only 35%. Line position is the same for both. So `q` is not a property of the word; it is a property of the *junction* `…y | qo…`. Read plainly: after a word ending in `y`, the next `o`-word gets a `q` hung on the front. This is the mechanism behind the `-edy → qo-` phrases in §18 and it is the most language-like thing in the corpus (it behaves like sandhi, or like a ligature across a space). Language B does this twice as often as A (18% vs 10% of tokens).
- **HMM over glyphs (5 states, Baum–Welch).** Voynich learns a cleaner cycle than Latin: initial state (`ch d sh q k s`) → vowel-like state (`o a y i e l`, next-state certainty 0.99) → `l r k t iin d` → back, with a terminal state (`y e d s`). Mean transition entropy 1.08 bits vs Latin 1.33; emission entropy 2.42 vs 2.93. Both texts show consonant/vowel alternation; Voynich is more rigid. Log-likelihood per glyph −2.17 vs Latin −2.55, the same gap the bigram entropy showed.
- **No line templates.** In the stars, herbal and bio sections, every line has a unique prefix/suffix skeleton, and the first-three-word skeletons are as diverse as after shuffling. The text is not a formulaic list with repeated line shapes, which weakens the "recipe list" version of the notation idea. Lines are varied the way prose is, even though word order inside them is not.
- **Labels on the same page share their first two glyphs 17% of the time vs 8% across pages.** Labels are grouped per page by prefix, which fits a page-local naming or numbering scheme (e.g. the jars on f88r: `otchdy otararain soaiin dalam sary okoral oko okchos am`).

Updated scoreboard after §20: H1 dead; H2 weak; H3 (abbreviated Latin) dead by §11; H5 (codebook) poor; H4 (procedural gibberish) fits nearly everything but not the `y|qo` junction rule or the excess word-order MI without extra machinery; H6 (constructed notation) fits the slot grammar, label grouping and page topicality, but the absence of line templates and the `y|qo` sandhi are odd for a bare notation. The honest summary is: **a rule-governed writing system whose rules I can now state in some detail (slots, junction rule, line-position allographs, page-local labels), with no evidence yet of a natural language underneath it.** The next step toward "translation" is not more cipher search; it is to pin down what the *units of meaning* are (word? line? label group?) by tying labels to the pictures, which needs a higher-resolution scan than this PDF.

## 21. High-resolution source (added 2026-09-16)

The Beinecke Library serves MS 408 through a public IIIF manifest (`https://collections.library.yale.edu/manifests/2002046`), 213 canvases at roughly 2,800 × 3,800 px each. `data/beinecke_index.tsv` lists canvas number, folio label and image URL. Full-size JPEGs are in `beinecke/` (not committed; ~450 MB). Any page region can be fetched directly at any size with the IIIF syntax, e.g. `https://collections.library.yale.edu/iiif/2/1006076/300,300,1400,800/full/0/default.jpg` for a crop of f1r. At this resolution individual glyphs, the marginalia, and the zodiac month names are readable.

## 22. Correction and the zodiac label count (2026-09-16, after the high-res pass)

**Parser bug fixed.** IVTFF marks continuation loci with `&` as well as `+`/`=`; my parser skipped `&` loci, which dropped 325 lines, almost all of them labels (the earlier §6 label figures were computed on 781 label tokens; the true count is 1,198). Re-ran `stats1.py` and `tests2.py`. The label conclusions hold and sharpen: 861 label types, 83% hapax, 46% ever occur in running text, only 1.0% begin with `q` (vs 15% in text), 54% begin with `o`.

**Zodiac labels: exactly 30 per sign.** Counting nymph labels per wheel after the fix: Pisces 30, Aries-dark 15, Aries-light 15, Taurus-light 15, Taurus-dark 15, Gemini 29 (one illegible), Cancer 30, Leo 30, Virgo 30, Libra 30, Scorpio 30, Sagittarius 30. Total 299. The two Aries and two Taurus pages pair up to 30. This is exactly the structure of a degree-by-degree (or day-by-day) calendar table, and it is the first place where the text has a countable external meaning: **each label is the name/entry for one of 30 units of a sign.** Ten signs × 30 = 300 slots, of which 299 are legible.

What that lets me test next: whether the 30 labels of a sign are ordered (degree 1 … 30) in some way that repeats between signs, i.e. whether label *i* of Pisces resembles label *i* of Aries. If labels are names of degrees or of the "faces" or the paranatellonta stars, there could be a pattern across signs; if they are personal names of 300 different things, there won't be.

Result of the zodiac-label test (`data/zodiac_labels.out`):
- The 30 labels of a sign are **not** aligned by position with the 30 of another sign: mean edit distance between label *i* of one sign and label *i* of another is 5.94, the same as for random positions (5.96). So there is no shared "degree 1, degree 2 …" naming that repeats across signs.
- The labels are, however, a tight family: 83 of 299 start with `ot`, 76 with `ok`; endings `-y` 82, `-dy` 54, `-al` 29, `-m` 27, `-ar` 26, `-aiin` 18. Only 29 label types recur at all within the zodiac (`otaly` ×5, `okal` ×4, `okaly` ×4). About 90% of the 300 slots carry a *distinct* string.
- The sign families differ: Pisces/Aries/Taurus labels are `ot-/ok- + al/ar/am` (`otal, otar, okal, otaldar, okaram`); Virgo/Libra/Scorpio/Sagittarius labels shift to `o-ee-/ok-eo- + dy/y` (`oeedy, okeody, oteedy, ykeedy`). That is the same A→B drift seen in the running text, playing out across the zodiac wheels in order. So the labels were written in the order the wheels are bound, and the writer's habits shifted as they went.
- Comparison with other label sets: bio (nymph) labels 60% `o`-initial, 40% `ot/ok`; pharma jar labels 50% / 31%; cosmo 54% / 27%; astro 46% / 27%; **herbal plant labels only 19% / 5%**. The `ot-/ok-` shape is the shape of "things beside figures, stars and jars", not of plant names.

Interpretation: 300 mostly-unique strings, one per degree, nearly all built from `o + gallows + (a/e-vowel run) + (l/r/m/dy/y)`, with no repeating structure across signs. That is *exactly* what a list of 300 different star or degree names would look like in a scheme where every name is spelled in a fixed template. It is also what a random 300-draw from the slot grammar would look like. What separates the two is whether the same label means the same thing when it recurs elsewhere: `otaly` appears in Pisces, Aries, Leo (×2) and Scorpio, and also as a pharma-jar label on f88r and f99v. I'll follow that thread in the pharma section.

## 23. Second pass in search of something new (2026-09-16, later)

Checked against the literature as I went (Currier 1976; Feaster's positional gradients; the "linestart transformation" post of 2016; the two 2026 arXiv papers on positional constraints and on units; the Voynichdecomp repository). Results, and their status:

| finding | my numbers | status |
|---|---|---|
| `y` → `qo` junction | P(qo | prev ends y) 0.27 vs 0.07 otherwise, ratio 3.9 | Currier 1976 |
| junction vanishes at line breaks | ratio 1.13 across line breaks, 1.35 across paragraphs; glyph MI 0.195 within line vs 0.046 across (random 0.039) | described (cross-line MI = 0 in Voynichdecomp; Feaster) |
| s/d/y added at line start | `saiin` 46% line-initial vs `daiin` 19%; s-X vs d-X pooled 0.30 vs 0.15; y-X vs o-X 0.21 vs 0.05 | described 2016 |
| ch-words displaced to 2nd position | ch-initial 3.2% at position 1, 22.3% at position 2, 17% mid-line | corollary of the above |
| -m avoided on paragraph-final lines | 9.2% vs 16.7% (stars section 8.6% vs 28.6%) | consistent with the known "m where space is tight" idea |
| labels on a page repeat more than chance | zodiac 15 duplicate pairs vs 4.9 expected | minor |
| zodiac labels not aligned by degree across signs | same-position edit distance 5.94 vs random 5.96 | negative |
| starred-paragraph first words are not star labels | 17 of 292 (chance 39) | negative |
| vertical neighbors more similar than horizontal | min edit distance to word above/below 3.18 vs random 3.66 | Timm & Schinner |

**Geometric test (`layout_dp.py`, `data/layout_stats.out`).** I tried to test two physical hypotheses on the scans of Quire 20: (a) if `s`/`d`/`y` are *added* at line start, such lines should begin further left; (b) if `-m` is a space-saving form, `-m` lines should end closer to the right margin and be more compressed. Row detection plus dynamic-programming alignment to the transcription worked (the overlay `crops/overlay_f104v.png` shows paragraph-final lines correctly identified), but edge measurement is too noisy: the left-edge spread is ±45 px (a glyph is ~33 px), and only 63% of continuing lines were measured as reaching the margin when nearly all do by eye. Within that noise: no left shift for s/d/y lines (medians 0 px), and `-m` lines are no closer to the margin than `-y` lines (P within 40 px: 0.47 vs 0.48) and no denser (33.4 vs 33.5 px per glyph). I record this as **inconclusive, leaning against the crowding explanation for `-m`**, and not as a result. Word-level segmentation would be needed to do it properly.

## 24. A new fact about the zodiac labels (2026-09-16): the labels switch from `a`-built to `e`-built words halfway through the zodiac, and the ring text on the same wheels does not

Scripts: `zodiac_drift.py` (feature rates), `zodiac_bness.py`, `zodiac_ae.py`, `data/zodiac_ae.out`, `data/zodiac_ae2.out`.

**Statistic.** For each word, an a/e index = (#a − #e)/(#a + #e), from +1 (only `a`) to −1 (only `e`). Averaged per wheel, wheels in binding order (which is also zodiacal order). Permutation tests shuffle words across wheels.

| wheel | folio | nymph labels (a/e index) | ring text on the same wheel |
|---|---|---|---|
| Pisces | f70v2 | +0.63 | +0.03 |
| Aries dark | f70v1 | +0.49 | −0.17 |
| Aries light | f71r | +0.24 | −0.24 |
| Taurus light | f71v | +0.91 | −0.01 |
| Taurus dark | f72r1 | +0.74 | +0.09 |
| Gemini | f72r2 | +0.77 | +0.16 |
| Cancer | f72r3 | +0.44 | −0.32 |
| Leo | f72v3 | +0.04 | −0.48 |
| Virgo | f72v2 | −0.28 | −0.16 |
| Libra | f72v1 | −0.40 | +0.23 |
| Scorpio | f73r | −0.33 | −0.13 |
| Sagittarius | f73v | −0.43 | −0.11 |

- Labels: step between the first seven wheels (f70v–f72r) and the last five (f72v–f73v) = +0.88, permutation p < 0.0001 (0 of 10,000); Spearman trend with order ρ = −0.77, p = 0.005. The same on the Takahashi (VT) and Zandbergen (RF) transliterations: step +0.87 and +0.90, both p < 0.0001. Restricting to labels of 4–7 glyphs (length control): step +0.92, p < 0.0001.
- Ring text on the very same pages: step +0.07 (p = 0.22), trend ρ = +0.03 (p = 0.94). VT and RF agree. Correlation between the label mean and the ring-text mean across the 12 wheels: 0.18. The two vocabularies on one page are not coupled.
- Within each wheel, all rings agree (e.g. Taurus light rings +0.94/+0.83; Libra rings −0.40/−0.40), so it is not a ring effect.
- Composition: `a`-only labels are 60–91% of the labels on Pisces–Gemini and 20–23% on Virgo–Sagittarius; `e`-only labels 0–18% early and 48–65% late. What actually changes is the vowel after the gallows and the ending: early labels are `ot`/`ok` + `a` + `-l/-r/-m/-iin` (`otal, otar, okaram, otalaiin`), late labels are `ok`/`ot` + `e(e)` + `-dy/-ey/-y` (`okeody, oteedy, okeey, ykeedy`). `ot-` falls from 62 to 23, `ok-` rises from 36 to 42 (of ~190 and ~156 labels).
- This is *not* a general property of labels: the same page-blocking test on the bio nymph labels (8 pages, p = 0.16), the pharma jar labels (14 pages, p = 0.64) and the cosmological labels (p = 0.14) finds nothing. Running text on all pages shows page-to-page variation in a/e (p < 0.0001 everywhere) but it is small (variance of page means 0.01–0.04, versus 0.23 for the zodiac labels).
- It is also not the Currier A→B drift: scored with a glyph-bigram A/B discriminant trained on the running text, the labels show no trend at all (ρ ≈ 0), while the ring text does drift toward B across the same wheels (ρ = +0.71 to +0.78, p ≤ 0.016). So the labels and the ring text change in *different* directions along the same sequence of pages: the text becomes more B-like, the labels swap their vowel.

**Why I think this is new.** Zandbergen's label page and his language-classification page treat the zodiac labels as one group ("Ce-" dialect) and give one hapax figure for all 299; the recent voynich.ninja thread on zodiac labels noticed only that `o`-initial labels decline and that Cancer and Sagittarius are outliers; the 2026 arXiv papers and the Voynichdecomp repository do not analyze labels per wheel; nothing I found mentions the `a`/`e` composition of labels or contrasts labels with the ring text of the same wheel. Some earlier readers must have seen `otal…` in Pisces and `okeedy…` in Sagittarius, but I find no statement of the switch, its location, its strength, or the fact that the co-located text does not share it.

**What it means (carefully).** The labels are not a random draw from "labelese": a property of a label (its vowel) is set by which wheel it is on, in a way that changes once, around the turn of folio 72, and that the scribe did not apply to the running text on the same page. Three readings: (1) the labels encode something that differs between the first half of the zodiac year and the second (a per-sign or per-season class marker, as a real astrological table of degrees, terms or faces would carry); (2) the labels were produced by a procedure with a "setting" that was changed between two sittings, while the text was produced continuously; (3) the labels were copied from two different source lists. I cannot choose between these from the text alone, but each is testable: (1) predicts the missing Capricorn and Aquarius wheels would have been `e`-labels and that other label systems tied to the calendar (f67r1 twelve labels, f69r twenty-eight) show the same partition; (2) predicts the change point sits at a physical break (it does: f72r → f72v); (3) predicts vocabulary overlap between the `a`-half labels and one text section and between the `e`-half labels and another.

Follow-up I ran: the 12 labels round the sun on f67r1 and the 28 on f69r are checked in §25.

## 25. The calendar wheels before the zodiac (`data/calendar_labels.out`)

Same a/e index on the label sets of the astronomical wheels: f67r2 (moon phases) +0.25, f67v1 +0.46, f67v2 +0.67, f68r1 (star names) −0.15, f68r2 (star names) −0.14, f68r3 +0.19, f69r (28 divisions) +0.31. So the two pages of *named stars* are `e`-leaning like the late zodiac labels, and the calendar-type wheels are `a`-leaning like the early zodiac labels. That is consistent with reading (1) in §24 (the vowel marks a class of item) but the sets are small and mixed; it does not settle it. What is settled is the zodiac contrast itself.

## 26. Robustness of the zodiac label switch (`zodiac_robust.py`, `data/zodiac_robust.out`)

All three transliterations (ZL, Takahashi VT, Zandbergen RF) give the same answer on every check:

| check | ZL | VT | RF |
|---|---|---|---|
| best change point (searched over all 11 splits) | Cancer / Leo | Cancer / Leo | Cancer / Leo |
| split statistic at best point | 10.8 | 10.9 | 11.0 |
| 99.9th percentile of the same max-over-splits statistic under shuffling | 4.5 | 4.1 | 4.4 |
| step with any one wheel left out | 0.84 to 0.97 | 0.83 to 0.93 | 0.86 to 0.98 |
| bootstrap 95% interval for the step | 0.72 to 1.04 | 0.71 to 1.02 | 0.74 to 1.06 |
| distinct label types, early vs late a/e mean | +0.56 vs −0.28 | +0.54 vs −0.29 | +0.55 vs −0.30 |
| label types shared between the halves | 18 | 19 | 12 |

**Where the break falls physically.** The best split is between Cancer (f72r3) and Leo (f72v3): the recto and verso of the same foldout leaf. Every wheel on the recto side of that leaf and before it has `a`-labels. Every wheel on its verso and after has `e`-labels. So the switch happens when the page was turned over, not somewhere in the middle of a writing surface.

**Not a scribe change.** Lisa Fagin Davis assigns all the zodiac pages to one scribe, her Scribe 4. The ring text on the same wheels shows no switch. A new scribe would change both. So the same person wrote `a`-labels on one side of the leaf and `e`-labels on the other, and kept writing the ring text the same way throughout.

**Status: I believe this is a new, documented fact about the script.** I searched Zandbergen's label and language pages, the voynich.ninja zodiac-label thread, the Cipher Mysteries "labelese" post, the 2026 arXiv work, the Voynichdecomp repository and the Zenodo zodiac paper. None reports a vowel switch in the labels, its location at the f72 recto/verso, or the contrast with the co-located ring text.

## 27. Do the two label halves come from different parts of the book? (`zodiac_sources.py`, `data/zodiac_sources.out`)

For each early (`a`) and late (`e`) zodiac label I checked whether the same word occurs in the text of other sections, excluding the zodiac pages themselves.

- **Exact matches:** no section favors either half. Every difference is under 0.10, and all permutation p-values are 0.11 or higher. Herbal-A, herbal-B, bio, stars, pharma and astro text all look the same to both halves. So do the bio, pharma and astro label sets.
- **Near matches:** allowing one deleted glyph, late labels match text more often in every section, by a similar margin: herbal-A 0.74 vs 0.51, stars 0.87 vs 0.67, bio 0.65 vs 0.50. The uplift is uniform, not tied to one section.
- **Reading:** the `e`-labels are simply closer to ordinary running-text word shapes everywhere. The `a`-labels are a more distinctive "labelese" style. There is no sign that the two halves were copied from two sections of the book. Reading (3) of §24 is not supported. Readings (1), a category marker, and (2), a changed procedure, remain.
- **Dark and light pairs:** Aries dark +0.49 vs light +0.24, Taurus light +0.91 vs dark +0.74. The darker or lighter drawing does not predict the vowel, so the split is not a day/night or color code within those signs.

## 28. Do labels name things mentioned in the text next to them? (`label_para.py`, `data/label_para.out`)

If a jar-section label named an ingredient, a plain-language recipe written right under it should mention it. I tested every label of three or more glyphs. For each one I compared how often it occurs in the paragraph directly after it with how often it occurs in the other paragraphs on the same page. Permutation null: a random paragraph from the same page.

| label set | labels | in paragraph right after | in other paragraphs on page | p |
|---|---|---|---|---|
| pharmacy jars and simples | 178 | 0.022 | 0.043 | 0.94 |
| bath nymphs | 49 | 0.102 | 0.099 | 0.48 |
| astro, cosmo, zodiac | 193 | 0.026 | 0.015 | 0.22 |

Result: **negative**. A jar label is no more likely to appear in its own recipe than in another recipe on the page. Only 4 of 178 pharmacy labels do so at all: `okol`, `chol`, `sheol`, `doldam`. This fits a forum report of no textual overlap between matched herbal and pharmacy pictures. If the labels are names, the text beside them does not repeat those names in the same written form.

## 29. Forum review and a correction to the novelty claim

See `FORUM_REVIEW.md`. The closest prior work to §24 is a voynich.ninja thread, "Currier A/B split is not what we thought it was!" (5710). It proposes a per-folio switch between `o` and `e` after `ch`/`sh` in running text. My zodiac finding differs in three ways. It is in the labels. It is carried mainly by `a`/`e` after `k`/`t`. It is **absent** from the ring text on the same folios: `o` share after `ch`/`sh` in ring text is 0.32 early vs 0.28 late, and `a` share after gallows is 0.25 vs 0.22. That last point contradicts a single switch state per folio. I now describe the result as an extension of that thread, not an isolated discovery.

## 30. Word-to-letter homophonic decipherment with a working control (`wordcipher2.py`, `runs/`)

**Hypothesis.** Each of the 300 most frequent Voynich word types stands for one Latin letter, with many word types per letter, as in a homophonic or Naibbe-style cipher. These 300 types cover 62% of paragraph tokens, 21,755 tokens in all. The search is simulated annealing over the type-to-letter key: 10 million steps, 8 restarts each. It is scored by a Latin letter 4-gram model, trained on half of Pliny, plus a penalty for drifting from Latin letter frequencies.

**Controls.**
- **Positive:** the other half of Pliny, enciphered by me into the same 300 Voynich word types with a random homophonic key. Same length, same method.
- **Negative:** meaningless text from a word-level Markov chain trained on the Voynich text.

| input | best score per character, 8 restarts | Latin dictionary coverage | key recovered |
|---|---|---|---|
| real Latin, reference | −2.160 | 0.898 | |
| Latin control, 4 restarts | **−2.160** | **0.898** | **100% of tokens** |
| Latin control, other 4 restarts | −2.61 to −2.62 | 0.22 to 0.24 | 9 to 10% |
| meaningless Markov text | −2.77 to −2.81 | 0.15 to 0.17 | |
| **Voynich** | **−2.77 to −2.82** | **0.15 to 0.20** | |

**Result: negative, and a clean one.** The search recovers a hidden Latin key exactly, token for token, in half of its restarts. On the Voynich text, no restart gets anywhere near a Latin solution. Its best is −2.77 per character, the same as meaningless text and far below the −2.16 a real decipherment reaches. If the 300 commonest Voynich words were a homophonic encoding of Latin letters, this search would have found it.

**Limits.**
- Only Latin was tested.
- Only one letter per word was allowed. The Naibbe cipher also maps words to letter *pairs*.
- Only the 300 commonest types were used. The other 38% of tokens were dropped, which also breaks letter adjacency in the Voynich input. The control had no dropped tokens, which may flatter it.

Next versions should add Italian and German targets, allow bigram mappings, and drop the same fraction of tokens from the control.

## 31. Correction to §30, with matched controls (`runs2/`, `data/wordcipher_bands.out`)

§30 compared the Voynich score with a Latin control that had **no** missing tokens. That was the wrong benchmark. Restricting to the top 300 word types removes 38% of Voynich tokens, and gaps lower the score of even a correct solution. I reran with controls that drop 38% of tokens at random, and added Italian (Dante) as a second target. Best score per character, grouped:

| target language | input | runs | best | worst |
|---|---|---|---|---|
| Latin | control, 38% dropped, **key recovered** (89–90% of tokens) | 3 | −2.741 | −2.748 |
| Latin | control, 38% dropped, search failed | 3 | −2.760 | −2.774 |
| Latin | meaningless Markov text | 8 | −2.774 | −2.809 |
| Latin | **Voynich** | 8 | **−2.771** | −2.818 |
| Italian | control, 38% dropped, **key recovered** (94–95% of tokens) | 3 | −2.735 | −2.741 |
| Italian | control, 38% dropped, search failed | 3 | −2.791 | −2.798 |
| Italian | meaningless Markov text | 6 | −2.844 | −2.888 |
| Italian | **Voynich** | 6 | **−2.872** | −2.899 |

**What changes.** The claim in §30 that the Voynich score was "far below a real decipherment" was overstated for Latin: the true gap is small (−2.771 vs −2.741). The corrected statement is:

- **Latin:** no Voynich restart reached the band of recovered keys. The best Voynich restart sits among the failed searches and the meaningless text. The margin is narrow, 0.02 to 0.03 per character.
- **Italian:** the Voynich text scores below even the failed Italian searches, and no better than meaningless text. The margin to a recovered key is wide, 0.13 per character.
- **Restart odds:** each control restart found the key half the time. If the Voynich text were solvable to the same degree, the chance that all 8 Latin restarts miss is about 1 in 256, and that all 6 Italian restarts miss is about 1 in 64. This assumes the Voynich problem is no harder than the control.

**Still untested:** one key per Currier language, since A and B could use different keys; words standing for letter pairs, as in the Naibbe cipher; and other target languages.

## 32. Currier language B alone (`runs3/`)

In case languages A and B use different keys, the same word-to-letter search was run on B paragraph text only. Language B has 15,382 tokens after keeping its own top 300 word types, which cover 66% of its tokens. The controls drop 33.6% of tokens to match.

| target | input | best score per character | key recovered |
|---|---|---|---|
| Latin | control, seed 2 | −2.693 | 90% of tokens |
| Latin | control, seed 1 | −2.719 | failed |
| Latin | **Voynich B**, 2 restarts | **−2.768**, −2.785 | |
| Italian | control, seeds 1 and 2 | −2.736, −2.748 | both failed |
| Italian | **Voynich B**, 2 restarts | **−2.833**, −2.834 | |

**Result.** Language B on its own scores below even the failed control searches, in both languages. For Latin, the gap to a recovered key is 0.075 per character, wider than on the mixed A+B text in §31. Only 2 restarts per condition were run, so this rests on few runs. It agrees with §31.

**Summary of the word-level cipher tests (§30–32).** A one-word-per-letter homophonic encoding of Latin or Italian, using the 300 commonest word types, is not supported for the whole text or for language B alone. The search demonstrably finds such keys when they exist. Still open are words standing for letter pairs, as in the Naibbe cipher, and other target languages.

## 33. Letter-or-pair word cipher (Naibbe form): the test cannot tell a cipher from gibberish (`pairchipher.py`, `runs3/pair_smoke_*`)

**Setup.** Each of language B's 300 commonest word types may stand for a single letter or for one of the 60 commonest Latin letter pairs. A Latin control was enciphered that way, with 40% of plaintext positions taken as pairs, and with 33.6% of tokens dropped to match the Voynich input. The score is a Latin 4-gram model per decoded letter, plus a letter-frequency penalty. Scoring the total instead of per letter was tried first and rejected: it prefers keys that emit fewer letters, and scored a wrong key above the true one.

**Result.**

| input | best per-letter score | share of words mapped to pairs | decoded sample |
|---|---|---|---|
| Latin control, **true key** | −2.626 | 40% by construction | real Latin with gaps |
| Latin control, search result | **−2.151** | 97% | "eterinisera…", key 1% correct |
| Voynich language B | −2.209 | 98% | "tulireresisiuemeuenilitares…" |
| meaningless Markov text | −2.188 | 98% | "denomaturenisidetatasinis…" |
| Voynich B with word order **shuffled** | **−2.156** | 97% | "erumeritonisinumesumones…" |

**Conclusion.** With pairs allowed, the search maps almost every word to a common Latin pair and assembles fluent-looking pseudo-Latin. It does this for real ciphertext, for meaningless text, and for shuffled text, and all of them score *better than the true key*. Shuffled Voynich text, which has no word order at all, scores best of the Voynich variants. So a letter-model decipherment of a letter-or-pair word cipher is **not falsifiable**. It will produce Latin-looking output from anything, and a better score means nothing. This explains why Naibbe-style parses of the Voynich text give "Latinish gibberish", and why any claimed decipherment of this form must be judged by something other than how Latin-like its output reads. The evidence would have to be dictionary words in context, agreement with pictures, or a key that holds up on held-out pages.

**What this means for "a measurable translation".** Language-model scoring can refute the one-word-per-letter form (§30–32) but not the pair form. A measurable translation of the pair form, or of anything richer, needs an external anchor: a word tied to a picture or a known name, checked on pages the key was not fitted to.

## 34. Do the zodiac wheels name their sign? A held-out test (`zodiac_names.py`, `data/zodiac_names.out`)

**Logic.** Aries and Taurus are each drawn on two wheels. If a wheel's ring text or labels contain the sign's name, both wheels of a pair should share that word, and the other ten wheels should lack it. The other 64 wheel pairings, which show different signs, serve as the null.

| measure | Aries pair | Taurus pair | 64 non-matching pairs |
|---|---|---|---|
| ring-text word overlap, Jaccard index | 0.064, rank 56 of 66 | 0.118, rank 8 of 66 | mean 0.085, max 0.155 |
| label overlap, Jaccard index | 0.000, rank 39 of 66 | 0.077, **rank 1** of 66 | mean 0.020, max 0.074 |
| ring-text words shared by the pair and on no other wheel | none | `chal`, `okeodaly` | mean 0.86 per pair, max 5 |
| labels shared by the pair and on no other wheel | none | `char`, `otaiin` | mean 0.45 per pair, max 3 |

**Result: negative.**
- **Aries:** the two wheels share no exclusive word, and their overlap is below average.
- **Taurus:** the labels of its two wheels overlap more than any other pairing. The shared exclusive words are `char`, used 84 times in the whole manuscript, and `otaiin`, used 155 times. Words that common cannot be the name of one sign.
- **Chance:** two exclusive shared words is ordinary for any pairing of wheels.

With one miss and one weak hit from only two testable pairs, there is no evidence that the ring text or labels name the sign. If a sign name is written on these pages, it is not a repeated word form.

## 35. Do pharmacy labels name the herbal plant they redraw? (`pharma_match.py`, `data/pharma_match.out`)

**Ground truth.** The ZL transliteration file carries 13 notes that a herbal plant is redrawn in the pharmacy section, with row and column in the pharmacy page. They are credited to Petersen, Stolfi, FSG and GL, and 4 are marked certain. Zandbergen's illustrations page confirms one more directly: f37v is the same plant as item 203 at the lower left of f102r1.

**Test.** For each match, I looked up the label written beside that pharmacy drawing. I then checked whether that word, or a variant one glyph shorter, appears in the paragraph text of the matching herbal page. The null is the rate for the same word on the other 127 herbal pages.

| herbal page | pharmacy position | label | on herbal page | on random herbal pages, exact / variant |
|---|---|---|---|---|
| f18v, tentative | f102r2 row 3, col 1 | `loeekadag` | no | 0.00 / 0.00 |
| f19r, tentative | f102v1 [2,2] | `ypcholdy` | no | 0.00 / 0.00 |
| f23r, **certain** | f102r2 [3,1] | `loeekadag` | no | 0.00 / 0.00 |
| f37v, confirmed by Zandbergen | f102r1 [3,1] | `ddardsh` | no | 0.00 / 0.00 |
| f47v, **certain** | f102r2 [1,1] | `kodaiig` | no | 0.00 / 0.00 |
| f48r, tentative | f89v2 [3,4] | `sada` | no | 0.00 / 0.00 |
| f48v, tentative | f89v1 [1,4] | `darshody` | no | 0.00 / 0.00 |
| f90v1 and f90v2, tentative | f100r [1,3] | `otear` | no | 0.00 / 0.16 |
| f96v, tentative | f99r [4,1] | `yteoldy` | no | 0.00 / 0.05 |

The pairs f1v (certain), f32v and f39r have no label at the given position.

**Result: negative, 0 of 10.** Not one label appears on its matching herbal page, exactly or as a variant. These labels are also almost absent from the herbal text generally: the null rate is 0 for 8 of the 10. So the test is weak, because the words hardly occur in herbal paragraphs at all. What it does show is that **the name written beside a pharmacy copy of a plant is not repeated in the text of that plant's herbal page**, not even for the four certain matches.

**Caveat.** I assumed labels run in the same order as the drawings in each row. That is how the ZL numbering reads, but I did not check each position against the scans. A wrong position would pair a plant with its neighbor's label.

## 36. Does a pharmacy recipe share vocabulary with the herbal page of the plant it shows? (`pharma_text_match.py`)

For 11 of the attested herbal–pharmacy picture matches, I compared the herbal page's words with the pharmacy paragraph under the matching drawing row. Similarity weights shared rare words more. The null pairs each herbal page with a random pharmacy paragraph, from 36 with at least 10 words.

- **Mean similarity:** matched pairs 0.457, unmatched 0.574. Matched pairs are *less* similar than random.
- **Rank among 36 paragraphs:** only f48v (rank 4) and f32v (rank 11) place their match in the top third. f19r ranks its match last.
- **Permutation p:** 0.96.

**Result: negative.** A recipe beside a copy of a plant uses no more of that plant's herbal-page vocabulary than any other recipe does. Together with §35, there is no detectable textual link between the two drawings of the same plant, in labels or in running text.

## 37. Held-out word-order test for the letter-or-pair cipher (`pairchipher.py` with `HOLD=1`, `runs4/`)

§33 showed that a letter-model score cannot tell a Naibbe-form cipher from gibberish. This is a criterion that can. Fit the key on the first half of the token sequence. Then decode the second half twice: once in its real order, and once with its tokens shuffled (20 shuffles). A real key turns real word order into real letter order, so it should score much better in order than shuffled. A key that only matches letter frequencies gains almost nothing from order. Language B, Latin target, 4 million annealing steps, 3 seeds per input. Score is the Latin 4-gram log-probability per decoded letter on held-out text.

| input | key | in-order gain over shuffled, per letter |
|---|---|---|
| Latin control | **true key** | **+0.429, +0.437, +0.474** (z 45 to 48) |
| Latin control | fitted by search, 0.2–0.9% of tokens correct | +0.021, +0.029, +0.037 |
| **Voynich B** | fitted | **+0.026, +0.028, +0.031** |
| meaningless Markov text | fitted | +0.054, +0.073, +0.098 |
| Voynich B, word order shuffled | fitted | +0.001, +0.004, +0.013 |

**Result: negative.** On held-out text, the keys fitted to Voynich B gain 0.03 per letter from word order. That is the gain of a *wrong* key fitted to real Latin ciphertext, and less than a fifteenth of what the true key gains. The Voynich text's word order does carry some structure: the shuffled version gains nothing, and Markov text built from Voynich word pairs gains a little more than the real text. But no fitted key turns that structure into Latin letter order.

**What this adds.** The fitted key on the control, which is 99% wrong, still scores better on the training half than the true key (−2.07 to −2.09 vs −2.62). The held-out order gain ranks them correctly, by a factor of 15. So this gain is a working pass/fail test for any claimed word-to-chunk key: a proposed decipherment should gain about 0.4 per letter from word order on pages it was not fitted to. None of the 3 Voynich searches comes close.

**Limits.** This uses Latin only, one search length, and 3 seeds. The search never found the true key on the control in this form, so the test checks whether a *found* key is real. It does not show that a real key would be found.

## 38. §37 repeated with Italian and German targets (`runs4/batch2.sh`, `runs4/summary2.out`)

Same setup as §37: Language B, 4 million annealing steps, 3 seeds. Italian is Dante; German is Goethe's *Faust*, with the Project Gutenberg header left in. Held-out gain from word order, per decoded letter:

| target | true key on control | key fitted to control (98–99% wrong) | **key fitted to Voynich B** |
|---|---|---|---|
| Latin (§37) | +0.43 to +0.47 | +0.02 to +0.04 | **+0.03** |
| Italian | +0.55 to +0.56 | +0.04 to +0.06 | **+0.05 to +0.08** |
| German | +0.58 to +0.61 | +0.05 to +0.08 | **+0.03 to +0.05** |

**Result: negative in all three languages.** The Voynich keys fall in the range of wrong keys. Italian is slightly above that range, at +0.08 at best, but a true key gains about seven times as much. For German the Voynich keys gain less than the wrong control keys. No letter-or-pair key found for Latin, Italian or German turns Voynich word order into that language's letter order on held-out text.

## 39. §37 repeated with consonantal Hebrew (`runs4/batch3.sh`, `runs4/summary3.out`)

Genesis, consonantal, with the five final forms merged into their ordinary letters and the 22 letters mapped onto 22 Latin placeholders. Half of it trains the 4-gram model; the other half is the control plaintext. Genesis is short, so the control has about 6,070 tokens against Voynich B's 7,691. The language model is also weaker, trained on only about 5,000 words, which is why the true key's gain is lower than in the European languages.

| input | key | held-out gain from word order, per letter |
|---|---|---|
| Hebrew control | true key | +0.275, +0.280, +0.282 |
| Hebrew control | fitted, 99% wrong | −0.005 to −0.002 |
| **Voynich B** | fitted | **+0.015, +0.025, +0.026** |

**Result: negative.** The Voynich keys gain a tenth of what a true key gains. They do a little better than the wrong control keys, by about 0.02. That is the same small surplus seen in Italian (§38), and the shuffled-Voynich run in §37 traces it to the text's own word-order structure (the `y | qo` junctions and split words of §18), not to a key.

**§37–39 together.** Across Latin, Italian, German and Hebrew, no letter-or-pair key found by search turns Voynich B word order into the target language's letter order on held-out text. True keys gain 0.28 to 0.61 per letter. Voynich keys gain 0.015 to 0.08.

## 40. Is the first word of a herbal page the plant's name? (`firstword.py`, `data/firstword.out`)

A common proposal is that each herbal page opens with the plant's name. If so, that word, or the same word without its opening gallows, should come back later on its own page more than other words do. I used 124 herbal pages with at least 4 paragraph lines. For each word I compared how often it recurs on its own page with how often it would by chance, given its frequency on the other herbal pages. The gallows-stripped match counts `kchol`, `pchol`, `tchol` and `fchol` as one form, because nearly every page opens with a gallows letter (§6).

| word position | recurs on own page, exact | obs/exp, exact | recurs, gallows stripped | obs/exp, gallows stripped |
|---|---|---|---|---|
| **first word of page** | **0.02** | 2.06, from 2 cases | **0.14** | **1.48** |
| second word of page | 0.16 | 1.55 | 0.16 | 1.56 |
| first word of later lines | 0.19 | 1.43 | 0.24 | 1.57 |
| mid-line words | 0.30 | 1.81 | 0.33 | 1.81 |

**Result: negative.** The first word of a page is the *least* likely word on the page to come back on it. Only 2 of 124 recur exactly, and 17 recur once the gallows is stripped. It does recur more on its own page than on a random herbal page (17 vs 4.7 in 1,000 shuffles, p < 0.001). But that holds for every word in this text, because pages reuse their own vocabulary (§5). Its own-page excess, 1.48, is below that of an ordinary mid-line word, 1.81. Nothing marks the page-opening word as the page's topic.

**Limit.** There is no plaintext control. A real herbal could name its plant once and then use pronouns. So this does not rule out a name in first position. It shows only that the text does not repeat the opening word the way a topic word would be repeated.

## 41. Does the f49v margin glyph index its line? (`f49v_margin.py`, `data/f49v_margin.out`)

Each of the 26 text lines on f49v has a single glyph beside it in the left margin. In ZL order the column reads `f o r y e 140 k s p o 192 y e 140 164 p o 192 y e 140 d y e k y`, where the numbers are ZL codes for rare glyphs. If the column indexed its lines, each margin glyph should match something in its own line. The null shuffles the column against the lines, 10,000 times.

| relation | observed | shuffled mean | p |
|---|---|---|---|
| equals first glyph of the line | 1 of 26 | 1.0 | 0.68 |
| starts some word in the line | 3 | 3.2 | 0.68 |
| equals last glyph of the line | 0 | 2.1 | 1.00 |
| occurs anywhere in the line | 12 | 13.6 | 0.90 |

**Result: negative.** The margin glyph has nothing to do with the line beside it. The column has a structure of its own instead. The block `p o 192 y e 140` comes twice, at lines 9–14 and 16–21, and the opening `f o r y e 140` shares its last three glyphs with it. So the column is a sequence written for its own sake, a drill or an ordering, and not a line index. That agrees with the reading in `VISUAL_SURVEY.md`.

## 42. Do the single-glyph sequences share one ordering? (`keyseq.py`, `data/keyseq.out`)

The manuscript has four runs of isolated glyphs:
- the third ring of f57v, a 17-glyph cycle written four times: `o l d r v x k m f 169 v t r 170 171 y c 172`
- the start of the fifth ring of f57v: `o v l r m aiin d 170 c f s y l k x l r 171`
- the single glyphs in the left margin of f66r (34)
- the margin column of f49v (26, §41)

If they were copies of one reference order, such as an alphabet, a cipher wheel or a table index, each should share a long ordered run with the f57v cycle. I measured the longest common subsequence with the cycle, allowing any rotation and two passes round it. The null is the same glyphs shuffled, 2,000 times.

| sequence | length | LCS with the f57v cycle | shuffled mean | p |
|---|---|---|---|---|
| f57v ring 5 head | 18 | 10 | 9.6 | 0.54 |
| f66r margin glyphs | 34 | 12 | 11.1 | 0.32 |
| f49v margin column | 26 | 8 | 7.1 | 0.25 |

**Result: negative.** They share glyphs but not their order. Not even the fifth ring on the same page follows the ring-3 order more than a shuffle does. The f57v cycle is the only one of these that repeats exactly, and it is not reused as an ordering anywhere else.

## 43. §37 repeated on Currier language A (`runs4/batch4.sh`, `runs4/summary4.out`)

In case A uses a different key from B. A's paragraph text is shorter: its 300 commonest types cover 63.7% of its tokens, which leaves about 3,600 training tokens. Controls drop 36.3% of tokens to match. Latin and Italian targets, 3 seeds each.

| target | true key on control | key fitted to control (wrong) | **key fitted to Voynich A** |
|---|---|---|---|
| Latin | +0.43 to +0.45 | −0.003 to +0.024 | **−0.015 to +0.007** |
| Italian | +0.49 to +0.52 | +0.002 to +0.027 | **+0.003 to +0.013** |

**Result: negative.** The keys fitted to language A gain nothing from word order on held-out text, the same as wrong keys. A has even less usable word order than B: B's small surplus of 0.02–0.03 over wrong keys, which §39 traced to its `y | qo` junctions, is gone here. That fits language A having about half B's rate of `qo` junctions (§20).

## 44. Acrostic test: the first glyphs of consecutive lines alternate (`acrostic.py`, `acrostic_lag.py`, `data/acrostic*.out`)

**Question.** Could a message be carried by the first glyph of each line, as in an acrostic? If so, the sequence of line-initial glyphs down a page should have letter-like dependencies. The null shuffles lines within their page or paragraph, which keeps each page's mix of initials. Paragraph-first lines are excluded, because they open with a gallows (§6). Lines interrupted by a drawing are single loci in ZL (`<->` inline), so splitting is not a factor.

**Result.** There is structure, but it is not an acrostic. It is an **alternation**:

| sequence | same initial at lag 1 | lag 2 | lag 3 | lag 4 |
|---|---|---|---|---|
| Voynich, within paragraph (shuffle) | **0.086** (0.148) | **0.194** (0.149) | 0.170 (0.152) | 0.180 (0.154) |
| language A only | **0.055** (0.137) | 0.178 (0.141) | | |
| language B only | **0.109** (0.158) | 0.205 (0.156) | | |
| Latin prose, Pliny, 9-word lines | 0.080 (0.077) | 0.077 (0.076) | | |
| Italian verse, Dante | 0.091 (0.105) | 0.098 (0.105) | | |

All Voynich lag-1 deficits and lag-2 excesses have p < 0.003 against 300 shuffles. Consecutive lines avoid sharing an initial: 42% fewer repeats than chance, and 60% fewer in language A. Lines two apart share one 30% more often. Latin prose shows nothing. Dante's verse has a small lag-1 deficit and no lag-2 excess. By section, the repeat deficit is largest in the herbal section (0.061 vs 0.150) and smallest in the stars section (0.164 vs 0.184).

**What carries it.** The strongest avoided transitions are `q→q` (23 against 89 expected), `o→o` (37 against 89), `ch→ch` and `s→ch`. The strongest favored ones are `q→ch` (56 against 23), `q→sh`, `o→q` (132 against 76) and `d→q`. The excess survives with self-repeats removed (MI over non-repeat pairs 0.327 vs 0.269, p < 0.002). It is not the `y | qo` junction carried across the line break: a line starts with `q` 16.1% of the time after a line ending in `y` and 14.2% otherwise.

**Prior work.** A voynich.ninja summary of Tavi's line-pattern talk (thread 4343) already reports `o→q` lines and the avoidance of `o-o` and `q-q` starts. This section quantifies that observation against a within-paragraph shuffle and plaintext controls, and adds the lag-2 excess and the A/B difference. It is a confirmation, not a discovery.

**Meaning for decipherment.** A line's first glyph depends on the previous line's first glyph, in an ABAB pattern found in neither Latin prose nor Italian verse. That is a layout rule working at the level of the line, like the other line-position effects (§2, §23). It makes an acrostic reading of line initials impossible: an acrostic's letters would follow plaintext letter order, not an alternation. It is also one more piece of evidence that lines were composed as units, with their openings chosen in relation to the line above.

**Follow-up (`couplet.py`, `data/couplet.out`).** The alternation is not tied to fixed couplets. Counting from the paragraph start, the repeat deficit is the same at both phases: lines 2→3, 4→5 … 0.084 against 0.148, and lines 3→4, 5→6 … 0.074 against 0.149. So it works as a free-running rule, "do not start a line the way the line above started", not as a pairing of lines. It is also specific to line starts. Inside a line, consecutive words share their initial glyph at the shuffle rate (0.156 vs 0.151).

## 45. Bax (2014): the "plant names" are page-opening words (`bax_test.py`, `data/bax_test.out`)

Stephen Bax's "A proposed partial decoding of the Voynich script" (2014) reads ten words as proper names and derives 14 sound values from them (Appendix 1, p. 56). It is the best known bottom-up proposal. I took its EVA forms, reconstructing each from his sound table and the page he cites:

| page, Bax's plant | EVA word | Bax's reading | where it stands | tokens in the manuscript |
|---|---|---|---|---|
| f2r, Centaurea | `kydainy` | KNTəIRN, "kantairon" | first word of the page | 1 |
| f3v, hellebore | `koaiin` | KAUR | first word of the page | 1 |
| f29v, Nigella | `kooiin` (+ `shor`) | KAUR CHAR | first word of the page | 2 (also opens f2v) |
| f31r, cotton | `keedey` | KOOTON | first word of the page | 1 |
| f27r, crocus | `ksor` | KSAR | first word of the page | 1 |
| f41v, coriander | `keeredal` | KOORATU | marginal label | 1 |
| f16r, juniper | `oror` | ARAR | inside longer words on f16r | 8, none on a herbal page |

**What this shows.**
- **The names are page openings.** Five of the six plant names are the first word of their herbal page, the slot where nearly every page starts with a gallows letter (§6) and where words almost never recur (§40). Being unique to the page, which makes a word look like a name, is therefore automatic for these words and carries no evidence.
- **The /k/ is the opening gallows.** Bax's sound /k/, which appears in six of his ten names, rests on that gallows. `k` opens 24 of 128 herbal pages; the other openers are `p` 57, `t` 26 and `f` 7. It is 4 times commoner there than inside a line (0.19 vs 0.048). Choosing plants whose names begin with K, from pages that open with `k`, would give his matches whatever the opening glyph means.
- **Stripped, two names are ordinary words.** Without the gallows, `koaiin` becomes `oaiin`, 25 tokens elsewhere, and `ksor` becomes `sor`, 50 tokens and a common line opener (§2). On f3v itself, `ykoaiin` follows a few words after `koaiin`, so the "name" also appears with a `y` prefix inside the line.
- **The juniper word is not a word.** `oror` never stands alone on the juniper page. Its 8 free-standing occurrences are on bio, pharma and stars pages and on f116v, not on any plant page.

**Verdict.** These readings are not refuted letter by letter, because most glyphs in them are hapax. But their supporting evidence, a K-initial word unique to its plant's page, is a positional artifact of the page-opening slot and would arise without any decoding. A held-out check is possible: if `k` = /k/ and `o` = /a/, the 24 `k`-opened herbal pages should depict plants with K-names more often than the `p`- and `t`-opened pages. That needs plant identifications made blind to the text, which I do not have.

## 46. Held-out test of Bax's /k/ against independent plant identifications (`plantids.py`, `bax_heldout.py`, `data/bax_heldout*.out`)

**Data.** voynich.nu lists "tentative identifications" per folio from two people who worked from the drawings: Ellie Velinska (ELV) and Th. Petersen (ThP). `plantids.py` extracts them into `data/plantids.json`, 138 folios, of which 62–74 are herbal pages that open with a gallows. The first proposed name in each entry is used.

**Prediction.** If Bax is right that the page-opening `k` is the sound /k/ (§45), `k`-opened pages should show plants whose names begin with a /k/ sound (`k`, `q`, or `c` not before `e`/`i`) more often than `p`-, `t`- and `f`-opened pages do. A broader version: the opening gallows matches the name's initial (`k`~C/K, `p`~P, `t`~T, `f`~F). The null shuffles names across pages, 10,000 times. The main run excludes Bax's own anchor pages (f2r, f3v, f16r, f27r, f29v, f31r, f41v).

| identifier | /k/ names on `k`-opened pages | on `p`/`t`/`f` pages | p | gallows matches initial | shuffled | p |
|---|---|---|---|---|---|---|
| ELV | 0 of 12 | 7 of 50 | 1.00 | 6 | 6.3 | 0.65 |
| ThP | 4 of 13 | 5 of 57 | 0.052 | 10 | 6.4 | 0.069 |

**Result: not supported.** With ELV's identifications the prediction fails outright: none of the 12 `k`-opened pages has a /k/-name. With ThP's there is a weak trend, 4 of 13 against 5 of 57. Its hits are *crossolatea*, *campanula*, *contellaria* and "like coxcomb?". It does not reach p < 0.05 even before correcting for two identifiers and two statistics. It also depends on a rule I loosened after a first run: counting `cy` as /k/ added one hit to each identifier. Two independent identifiers disagree, and the one that agrees does so weakly. The page-opening gallows does not carry the first sound of the plant's name.

**Caveat.** These identifications are themselves uncertain, often marked "?", and the two sources agree on only a minority of pages. A real signal would have to show through that noise. A 31% vs 9% rate on 13 pages could be such a signal, or could be chance. A third set of identifications made without seeing the text, such as Sherwood's or Janick & Tucker's, would settle it. I did not find a folio-level list of either.

**Third identifier (`sherwood_ids.py`, `data/plantids_sherwood.json`, `data/bax_heldout_sherwood.out`).** Edith Sherwood's site is offline. The Wayback Machine holds 4 of its 14 plant-list pages, which give a Latin name for 27 folios, 19 of them usable herbal pages. /k/-names on `k`-opened pages: **2 of 6** (*Cycas*, *Cynara*); on `p`/`t`/`f` pages: 1 of 13 (*Chelidonium*). One-sided Fisher p = 0.22. Both hits again depend on counting `cy` as /k/. Pooled over the three identifiers: 6 of 31 `k`-pages against 13 of 120 other pages, 19% vs 11%. ELV contradicts the other two, and no single set reaches significance. **Verdict unchanged: not supported.**

## 47. Cheshire's proto-Romance alphabet against reassigned controls (`cheshire_test.py`, `data/cheshire_test.out`)

**Source.** Gerard Cheshire, "Linguistic missing links" (2017, LingBuzz 003737), Figs. 1–27. These figures define the sign values behind his 2019 *Romance Studies* paper. Read against EVA:
- **Vowels:** `o`→o, `a`→a, `y`→a ("free a"), `e`→e, `ch`→e ("long e"), `sh`→ae, `i`→i, `ii`→u
- **Consonants:** `q`→d, `d`→n, `l`→r, `r`→s, `s`→t, `n` and `m`→s ("sitting s"), `k`→l, `t`→m, `p`→p, `f`→qu
- **Bench gallows:** `ckh`→ele, `cth`→eme, `cph`→epe, `cfh`→eque

The EVA correspondences are my reading of his glyph drawings. Two choices are open to argument: `ch` as a single e, and `r`/`s` as standing s / t.

**Test.** Apply the table mechanically to all 34,765 paragraph tokens it covers (99.5%). Then count decoded words of three or more letters found in a Latin lexicon (Pliny) or an Italian one (Dante). (An earlier draft said "Pliny plus the Vulgate"; `data/ref/latin_vulgate.txt` turned out to be empty, so the lexicon was Pliny alone. The numbers are unchanged.) Matching uses his own allowances: e and i are interchangeable, and double letters collapse. Two nulls, 300 draws each:
1. the same letter values shuffled across glyphs at random
2. shuffled only within his vowel glyphs and within his consonant glyphs, which keeps the vowel/consonant skeleton he chose

| lexicon | Cheshire, tokens | random reassignment | p | class-preserving reassignment | p |
|---|---|---|---|---|---|
| Latin | 0.127 | 0.054 | 0.02 | 0.108 (max 0.235) | 0.31 |
| Italian | 0.067 | 0.046 | 0.19 | 0.081 (max 0.201) | 0.62 |
| Latin or Italian | 0.173 | 0.082 | 0.02 | 0.157 (max 0.310) | 0.36 |

By type, the class-preserving p values are 0.23, 0.28 and 0.21.

**Result: negative.** His table beats a fully random one only because it puts vowels on the vowel-like glyphs, which Sukhotin's algorithm finds without any decipherment (§8). Once that skeleton is kept, his particular choice of letters is unremarkable. A third of the reshuffled tables find more Latin words than his does, and the best find almost twice as many. His commonest readings, `daiin`=*naus*, `chedy`=*eena*, `qokeedy`=*doleena*, `ol`=*or*, are not words in either lexicon, apart from chance hits like *or* and *as*.

**Note on falsifiability.** Cheshire writes that a mechanical rendering is "naive" and that translation requires choosing among Latin, Italian, Portuguese, Catalan and other cognates. That freedom is what lets any table, including the reshuffled ones, yield words. This test removes it. Under fixed rules his values do no better than their own permutations.

## 48. Hauer & Kondrak's Hebrew identification also picks Hebrew for gibberish (`langid.py`, `data/langid.out`)

Hauer & Kondrak (TACL 2016) identified the source language of the Voynich text as Hebrew. One of their measures compares *decomposition patterns*: the pattern of repeated letters within each word, such as `abca` for a four-letter word whose first and last letters match. They then decoded with anagrammed Hebrew. I reimplemented two of their measures: the sorted letter-frequency profile and the decomposition-pattern distribution (L1 distance). I ran them on the Voynich text, in EVA units with the `ch`, `sh` and bench-gallows ligatures as single glyphs, and on three meaningless inputs. The references are my five languages, not their 380 translations of the Universal Declaration of Human Rights.

| input | nearest by letter-frequency profile | nearest by decomposition patterns | pattern distance: Hebrew / next |
|---|---|---|---|
| Voynich | Latin | **Hebrew** | 0.643 / 0.699 |
| slot self-citation generator, meaningless (§17) | Latin | **Hebrew** | 0.661 / 0.826 |
| word Markov chain, meaningless | Latin | **Hebrew** | 0.646 / 0.702 |
| Voynich glyphs shuffled at random across words | Latin | **Hebrew** | **0.629** / 0.690 |

**Result.** The decomposition-pattern measure calls every one of these inputs Hebrew. It gives the shuffled version, which has no word-internal order at all, an even closer match than the real text. So, on this measure, "closest to Hebrew" comes from word length and the rate of repeated glyphs within a word. Voynich words average 4.4 glyphs, against 4.38 for consonantal Hebrew. It carries no information about the language. The letter-frequency measure calls everything Latin, which is just as uninformative.

**Limits.** I used two of their measures and five reference languages. Their full method also includes a trial-decipherment measure and the whole UDHR corpus. But the point does not depend on the number of languages: a measure that gives the same answer for gibberish and for glyph-shuffled text cannot support the choice of a language. A language identification is evidence only if it fails on meaningless text built to the same statistics.

## 49. A reusable checker for proposed sign tables (`validate_mapping.py`, `mappings/*.json`, `data/validate_mapping*.out`)

Any claimed decipherment that assigns sounds to glyphs can be written as a JSON table, EVA unit → letters, and run through two controls in one command:

    python3 validate_mapping.py mappings/<name>.json [draws]          # on the Voynich text
    CONTROL=1 python3 validate_mapping.py mappings/<name>.json [draws] # positive control

1. **Dictionary hits.** The share of decoded word tokens of three or more letters found in a Latin lexicon (the first half of Pliny) and an Italian one (Dante). Matching is lenient: e/i and k/c are merged and double letters collapse. The proposed table is compared with reshuffled tables that keep its own vowel/consonant split (§47). Units whose value mixes vowels and consonants stay fixed.
2. **Word-order gain.** Decode the second half of the text in its real word order and in shuffled word order, and score both with a Latin letter 4-gram model trained on the first half of Pliny. Compare with the reshuffled tables.

**Positive control.** `CONTROL=1` replaces the Voynich text with the *second* half of Pliny, encoded into EVA with the inverse of the table. Only letters that have a single-letter value can be encoded, so 39% of tokens survive with Cheshire's table. The checker should then single out the true table.

| input, table | tokens covered | Latin hits (reshuffled mean, p) | Italian hits (p) | word-order gain (reshuffled mean, p) |
|---|---|---|---|---|
| **control**: Pliny encoded with Cheshire's table | 39.4% | **0.587** (0.040, p < 0.01) | 0.205 (p < 0.01) | +0.019 (+0.005, p < 0.01) |
| Voynich, Cheshire 2017 (§47) | 99.2% | 0.094 (0.083, p 0.28) | 0.067 (p 0.71) | +0.072 (+0.071, p 0.48) |
| Voynich, Bax 2014 first-choice values | 30.3% | 0.020 (0.015, p 0.20) | 0.039 (p 0.69) | −0.022 (+0.007, p 0.99) |

Each Voynich row uses 200 reshuffled tables; the control uses 100.

**Result.** The checker passes its control: on encoded Latin the true table beats every reshuffled table on all three measures. On the Voynich text, both published tables are ordinary members of their own reshuffled families on every measure. Bax's values decode only 30% of the text, because many common glyphs (`ch`, `l`, `t`, `p`, `q`) have no value in his table. On that 30% they gain *less* from word order than 99% of reshuffled tables.

**Scale of the word-order gain.** Shuffling whole words changes only the letter 4-grams that span word boundaries. So the gain is small even for a true table (+0.019 here). It is much smaller than the 0.4–0.6 in §37, where the shuffled units were single letters or letter pairs. What matters is how the gain ranks within the reshuffled family, not its size. The Voynich gain is larger in absolute terms (+0.07) for *every* table, reshuffled ones included. It comes from the text's own repeated word sequences, not from any table.

Future claims can be added to `mappings/` and checked the same way. A table that deserves attention has to beat its reshuffled family on the Voynich text the way the true table does on the control.

## 50. Are the starred paragraphs one per day? (`stars_count.py`, `data/stars_visual.tsv`, `data/stars_count.out`)

The stars section (quire 20) is a run of short entries, each marked with a star in the margin. A calendar of one entry per day would give about 360 or 365 of them. The bifolio f109–f110, 4 pages, is lost.

**First attempt, withdrawn.** Counting ZL paragraphs gives 285 on the 23 surviving pages, projecting to 335 ± 6, and I first concluded that 360 or 365 was unlikely. That was wrong, because ZL paragraphs are not the starred entries. On f108v, f111r and f111v, ZL has 7, 6 and 8 paragraphs where the scans show 16, 17 and 19 stars.

**Stars counted on the scans.** I counted the stars by eye from left-margin strips of the Beinecke images (`crops/stars_m*.jpg`, not committed). The counts are probably accurate to about ±1 per page, and they are in `data/stars_visual.tsv`.
- **Surviving pages:** 323 stars on 23 pages. Full pages hold 14.2 on average (sd 2.4, min 10, max 19).
- **Lost pages:** if they were average, they held about 57 ± 5, for a total of about **380 ± 5**, before counting error. The counting error adds roughly another ±10.
- **Reaching 365** needs 10.5 per lost page, at the bottom of the observed range: only f105r and f105v, at 10, are sparser.
- **Reaching 360** needs 9.2 per lost page, below any surviving page.

**Result: inconclusive.** A 365-entry calendar is possible if the four lost pages were as sparse as the sparsest surviving ones. The central estimate, about 380, is above 365. The data neither support nor exclude one entry per day.

**Side result.** ZL's paragraph division undercounts the starred entries by 38 overall. Any analysis of the stars section that treats ZL paragraphs as entries (§23's "starred-paragraph first words", for one) works with merged entries on f108v, f111r, f111v and f116r.

## 51. Do herbal pages showing the same plant share vocabulary? (`sameplant.py`, `data/sameplant.out`)

If the herbal text describes the plant drawn beside it, two pages showing the same plant should share more words than two unrelated pages. The plant identifications come from voynich.nu (ELV and ThP) and Sherwood (§46), made from the drawings. Only the name fields are used, with attributions such as "(O'Neill)" removed, and names are matched on their first six letters. Of 106 identified herbal pages, 35 same-language, non-adjacent page pairs share a proposed genus: two *Mentha*, three *Aristolochia*, three borages, two *Primula*, *Nymphaea*, *Helleborus*, *Rumex*, *Veronica* and others. Similarity is the cosine of tf-idf word vectors. The null draws, for each pair, a different-genus pair of the same Currier language at a similar folio distance (in bins of 10 folios), because nearby pages share vocabulary through drift (§8). 5,000 draws.

| pairs | mean cosine |
|---|---|
| same proposed genus (35) | 0.0361 |
| matched different-genus pairs | 0.0387 |

p = 0.77. **Result: negative.** Pages identified as the same plant share no more vocabulary than unrelated pages of the same language and distance. The highest pair, f40v and f50r, both called artichoke by ThP (cosine 0.134), ranks among the top 16 of all 4,961 same-language herbal page pairs. It is the only same-genus pair that stands out. Pairs this high make up 0.3% of all pairs, so among 35 pairs chance gives at least one about 10% of the time. A single striking pair is therefore weak evidence, and the group as a whole is at chance. Together with §35–36 (herbal vs pharmacy copies) and §40 (page-opening words), there is no sign that the herbal text varies with the plant drawn. **Caveat:** the identifications are uncertain, and a wrong identification adds noise. But that noise would weaken a real effect, not reverse it, and here the same-plant pairs come out slightly *below* the null.

## 52. Do the two 28-ish diagrams share names, as two lists of lunar mansions would? (`mansions.py`, `data/mansions.out`)

**Counts.** Several astronomical diagrams have cycle-sized counts in ZL:
- 12 radial entries on f67r1, 12 star labels on f67r2, 12 labels on f67v1 and 12 outer-ring lines on f68v2
- **28 radial entries on f69v**, the count voynich.nu links to the 28 lunar mansions
- **29 star labels on f68r1**, and 24 on f68r2

If f69v and f68r1 both listed the mansions, by name or by their stars, they should share word forms.

**Test.** For each of the 36 label or ring sets with at least 15 distinct words, I measured the share of f69v's 28 radial words that occur in the set, exactly or within one glyph edit.

| set | exact shared | f69v words within 1 edit | rank of 36 |
|---|---|---|---|
| fRos labels (139) | 5 | 0.62 | 1 |
| f72v1 zodiac labels | 2 | 0.48 | 2 |
| f69r outer ring | 6 | 0.45 | 3 |
| **f68r1 star labels (28)** | **0** | **0.17** | **25** |

**Result: negative.** The star labels of f68r1 share no word with f69v's 28 entries, and fewer near-matches than most other sets. f69v's words (`okeody`, `okeey`, `oteol`, `ytody`, `sar`…) are closest to the large fRos label set and the zodiac labels, which is just the common `o + gallows + ending` label family (§6, §22). The 28 and 29 counts may still reflect a lunar-mansion scheme, but the two diagrams do not name the same 28 things in the same written form.

## 53. Where things stand after §30–52

**Ruled out, with controls that pass:**
- **Word stands for a letter (homophonic), Latin and Italian.** §30–32.
- **Word stands for a letter or letter pair (Naibbe form), held-out word-order test.** Latin, Italian, German and Hebrew, both Currier languages. §37–39, §43.
- **Published sign tables.** Bax 2014 and Cheshire 2017 score like reshuffled versions of themselves. §45–47, §49.
- **Hebrew identification by decomposition patterns** (Hauer & Kondrak). It also picks Hebrew for gibberish. §48.
- **Bax's page-opening /k/** against plant identifications made from the drawings. Not supported by three identifiers. §46.

**No link found between text and picture:**
- labels vs the paragraph beside them (§28)
- pharmacy labels and recipes vs the herbal page of the same plant (§35–36)
- zodiac sign names (§34)
- page-opening words as plant names (§40)
- same-plant herbal pages (§51)
- the two 28/29-entry astronomical diagrams (§52)

**Structure confirmed or quantified:**
- line-initial alternation between consecutive lines (§44, confirming Tavi's observation)
- the f49v margin column is a sequence of its own, not a line index (§41)
- the single-glyph sequences share no ordering (§42)
- the stars section has about 323 starred entries, not ZL's 285 paragraphs; a 365-day reading is possible only if the lost bifolio was sparse (§50)

**Tools for testing future claims:** `validate_mapping.py` (§49), and the held-out word-order test in `pairchipher.py` (`HOLD=1`, §37).

**Honest summary.** No word or glyph has a meaning that survives a control. Every test that could have tied the text to the pictures came back at chance. That is what meaningless text would give. It is also what a text would give if it named things in a form unrelated to the pictures, or if it were not about the pictures at all. The tests here cannot separate those three.

## 54. Montemurro & Zanette's keyword structure comes from section drift (`mzinfo.py`, `data/mzinfo.out`)

Montemurro & Zanette (PLoS ONE 2013) measured how far words cluster in parts of the text rather than spreading evenly. Their statistic, I(s), is the drop in a word's positional entropy across parts of s words, relative to a shuffled text, in bits per word. They found Voynich keywords that behave like the topical words of a real text. I computed I(s) for the Voynich text, the tuned self-citation generator of §17 (meaningless, with local copying), and Latin (Pliny), all at about 35,000 words.

| s (words per part) | Voynich, whole | generator | Pliny |
|---|---|---|---|
| 500 | 0.308 | 0.306 | 0.405 |
| 1000 | 0.311 | 0.282 | 0.448 |
| 2000 | 0.297 | 0.241 | 0.499 |
| 4000 | 0.285 | 0.193 | 0.477 |

On the whole text, Voynich clusters more than the generator at large scales. But the whole text mixes sections and both Currier languages, which use different vocabularies (§2, §8). Within single homogeneous stretches, with the generator retrained on the same stretch:

| stretch | s | Voynich | generator |
|---|---|---|---|
| herbal, language A (8,015 words) | 500 / 1000 / 2000 | **0.094 / 0.078 / 0.054** | 0.324 / 0.279 / 0.191 |
| language B, all sections (23,175 words) | 500 / 1000 / 2000 | 0.235 / 0.221 / 0.193 | 0.306 / 0.274 / 0.231 |

**Reference: a real Latin herbal.** Macer Floridus, *De viribus herbarum*, has 77 plant chapters averaging 184 words; the text is from Latin Wikisource (`data/ext_herbal/`, not committed). Cut to herbal A's length, 8,015 words:

| s | 100 | 200 | 500 | 1000 | 2000 |
|---|---|---|---|---|---|
| Macer | 0.035 | 0.046 | 0.055 | 0.058 | 0.051 |
| Voynich herbal A | 0.102 | 0.113 | 0.091 | 0.079 | 0.054 |

**Result.**
- **Whole text.** Its large-scale clustering comes from the differences between sections and between A and B. Inside one stretch, the Voynich text is less clustered than the copying generator.
- **Herbal A vs a real herbal.** Herbal A is *more* clustered than Macer at page scale (100–200 words: 0.10–0.11 vs 0.035–0.046) and about equal at 2,000 words. My first reading, that a real herbal should be much more clustered than herbal A, was wrong. A verse herbal in inflected Latin names each plant only a few times, so its words spread almost evenly.
- **Ranking.** At page scale herbal A falls between a real herbal and a meaningless copying generator, and does not settle which it resembles.

What the word-clustering measure does show is that Montemurro & Zanette's "keywords" do not need meaning to arise. The text's section- and language-level drift produces them, and within a stretch its clustering is matched or exceeded by a meaningless generator.

**Limits.** The generator was tuned on the whole text, so its local copying may be too strong for one stretch. Macer is verse and Latin is inflected, which spreads word forms. A prose herbal, or a lemmatized comparison, would be a fairer reference.

## 55. Herbal pages have fewer page-exclusive repeated words than a real herbal (`namewords.py`, `namewords2.py`, `data/namewords*.out`)

**Idea.** A herbal names its plant, and often a few other page-specific things, more than once on that plant's page and nowhere else. Call a word *name-like* on a page if it occurs there two or more times and on no other page of the same set. Reference: Macer Floridus (§54). Its chapter title, the plant's name, occurs inside its own chapter in 73 of 77 chapters.

**Correction to the first version.** The first version of this section compared 95 Voynich herbal-A pages with 66 Macer chapters and reported 6% vs 27%, p = 3 × 10⁻⁷. That comparison was confounded. Whether a word is exclusive to one page depends on how many other pages there are, and the Voynich side had more. With page *counts* matched as well as page lengths, the gap shrinks, though it does not vanish.

**Matched comparison.** Pages are cut to 84 words, keeping only pages that have at least that many. Random subsets of n pages, 300 draws. Each cell gives the share of pages with a name-like word / the share of within-page repeated words that are found on no other page.

| n pages | herbal A | Macer | herbal B |
|---|---|---|---|
| 10 | 0.70 / 0.125 | 0.66 / 0.178 | 0.52 / 0.079 |
| 20 | 0.40 / 0.054 | 0.48 / 0.107 | 0.23 / 0.028 |
| 30 | 0.24 / 0.029 | 0.39 / 0.078 | |
| 45 | **0.12** / 0.013 (5–95%: 0.09–0.16) | **0.33** / 0.058 (0.27–0.42) | |

Herbal A has only 49 pages of 84+ words, so its n = 45 draws overlap heavily and its range is narrow by construction.

All sections at n = 15 pages: bio B 0.31, herbal A 0.52, herbal B 0.31, pharma A 0.67, stars B 0.41; Macer 0.54. The self-citation generator, on all 95 herbal-A page lengths, gives 0.96, against 0.06 for the real herbal-A pages.

**Result.**
- **Small sets look alike.** With 10–15 pages, herbal A looks like Macer.
- **The difference grows with the set.** As more pages are included, the words a Voynich herbal page repeats turn up on other pages, and the rate falls fast: 0.70 → 0.12 from 10 to 45 pages. In Macer it falls slowly: 0.66 → 0.33. A herbal's page-repeated names stay exclusive however many chapters are added. Herbal A's page-repeated words are moderately rare words that recur elsewhere in the book.
- **Size of the gap.** At 45 pages it is about threefold, outside the sampling ranges. It is smaller than the fivefold of the first version.
- **Not all sections.** Pharmacy pages (0.67 at n = 15) have more page-exclusive repeats than Macer. Bio and herbal B have fewer.
- **The generator fails.** The slot self-citation generator (§17) repeats its own fresh variants and overshoots badly (0.96). A copy-and-vary procedure would have to re-copy established words, not its own new ones.

**Interpretation.** Herbal A pages do not keep a repeated, page-specific name the way a real herbal does. The name could be written once, spelled differently each time, or the text could not be about the plant. This agrees with §40 and §51, but it is a quantitative difference, not an absence.

**Limits.** Macer is verse in inflected Latin. Inflection lowers its exact-form repetition, so the gap may be underestimated. There is only one reference herbal.

## 56. Are labels repeated in their own page's text? Only as much as any word is (`label_page.py`, `data/label_page.out`)

§28 compared a label with the paragraph beside it against other paragraphs *on the same page*. This compares the label with the whole running text of its own page (paragraphs, circular and radial text) against the running text of another page of the same section. The null reassigns labels to random pages of the section, 5,000 draws. The baseline is general page locality (§5): an ordinary running-text word of 3+ glyphs, checked against the rest of its own page versus a random page.

| section | labels | in own page's text | random page | p | label ratio | ordinary-word ratio (locality) |
|---|---|---|---|---|---|---|
| cosmo | 198 | 37 | 18.2 | < 0.001 | 2.04× | 1.86× |
| zodiac | 331 | 32 | 26.0 | 0.09 | 1.23× | 1.17× |
| bio | 117 | 24 | 23.8 | 0.54 | 1.01× | 1.14× |
| pharma | 244 | 16 | 16.0 | 0.55 | 0.99× | 1.20× |
| astro | 137 | 5 | 7.3 | 0.92 | 0.69× | 1.50× |

**Result: negative.** The one significant section, cosmo, is explained by locality: its labels recur in their own page's text 2.04 times as often as on another page, but so does an ordinary word, 1.86 times. Everywhere else labels are tied to their page *less* than ordinary words are. Pharmacy labels match their own page's recipes exactly as often as a random page's recipes. The two striking pharmacy cases, `opcheor` on f89r2 and `doldam` on f99v, occur on their own page as a label and in the text and nowhere else in the book. They are the kind of coincidence 244 labels produce.

Together with §28, §35 and §52: a label is not a word the nearby text uses, at any scale from the adjacent paragraph to the page.

## 57. Do the herbal plants run in alphabetical order, as in *Circa instans*? (`alphaorder.py`, `data/alphaorder.out`)

The dominant late-medieval herbals, *Circa instans* and the illustrated *Tractatus de herbis*, arrange plants alphabetically by Latin name. If the Voynich herbal copied such a model, the plants identified from the drawings should run roughly alphabetically through the folios. The bifolios are known to be bound out of order, so the test is also run within quires. Statistic: Spearman correlation between folio order and the alphabetical rank of the first proposed name. 5,000 shuffles.

| identifier | pages | rho, all herbal | p | mean rho within quires |
|---|---|---|---|---|
| ELV | 76 | −0.20 | 0.08 | −0.18 (8 quires) |
| ThP | 86 | −0.01 | 0.91 | +0.04 (9 quires) |
| Sherwood | 27 | −0.20 | 0.31 | −0.42 (4 quires, few pages) |

**Result: negative.** No identifier shows any alphabetical trend, overall or within quires. The weak negative values are not significant and do not agree across identifiers. Either the herbal does not follow an alphabetical model, or the identifications, or the leaf order, are too unreliable to show it. A Latin-alphabetical source would have shown a clear positive rho if most identifications were right.

## 58. What size of unit makes Voynich look like a natural script? (`bpe_units.py`, `data/bpe_units.out`)

§4 merged a few common digraphs; this does it systematically. Glyphs within words are merged by byte-pair encoding, the most frequent adjacent pair at each step, and the inventory grows from the 25 EVA glyphs. At each inventory size: unigram entropy h1, conditional entropy h2 (next unit given the current one, with the word boundary as a unit), and units per word. The same procedure is run on Latin letters (Pliny).

| units | Voynich h1 / h2 / units per word | Latin h1 / h2 / units per word |
|---|---|---|
| 25 (raw EVA) | 3.87 / 2.10 / 4.96 | 4.01 / 3.40 / 6.01 (24 letters) |
| 30 | 4.14 / 2.40 / 4.00 | 4.26 / 3.58 / 5.48 |
| 40 | 4.39 / 2.90 / 3.01 | 4.66 / 3.83 / 4.88 |
| 50 | 4.57 / 3.17 / 2.64 | |
| **60** | **4.67 / 3.34 / 2.39** | |
| 80 | 4.85 / 3.55 / 2.14 | |
| Latin syllables (rough split) | | 6.52 / 4.42 / 2.79, inventory 1,588 |

**Result.**
- **Units as letters do not work.** Voynich reaches the predictability of Latin *letters* (h2 about 3.4) only at about 60 units. By then a word is 2.4 units long, where Latin averages 6 letters. Read as letters of a European language, those units would give implausibly short words. That holds for any choice of merges, not only the common digraphs of §4. So a verbose cipher of an alphabetic text, with several glyphs per letter, does not fit unless word spaces are not real word boundaries.
- **Units as syllables almost fit.** About 60 units at 2.4 per word is the profile of a small syllabary, a few dozen signs and two or three per word, like the Japanese kana. The fit is only in size: Latin syllables number about 1,600 types (top 60 cover 63% of tokens) and are far less predictable (h2 4.4). So the Voynich units cannot be one sign per Latin syllable either. A syllabic reading needs a language with a small syllable inventory, or a script that writes only part of each syllable.

This is a constraint, not a reading. It narrows the scripts the Voynich could be, if it is a script at all: not an alphabet with real word spaces; possibly a small syllabary or an abbreviating system.

## 59. A Polynesian comparison: Māori is close to Voynich on entropy (`bpe_units.py`, `data/bpe_units.out`)

The Māori New Testament (ebible.org `mri`, not committed) was cut to the same token count as the Voynich paragraph text. Māori writes only (C)V syllables (consonants h k m n p r t w ng wh; five vowels), so every word splits uniquely into syllables.

| text | units | h1 | h2 | units per word |
|---|---|---|---|---|
| Voynich, raw EVA | 25 | 3.87 | 2.10 | 4.96 |
| **Māori, letters** | 15 | 3.44 | **2.49** | 3.34 |
| Latin, letters | 24 | 4.01 | 3.40 | 6.01 |
| Voynich, merged to 50 units (§58) | 50 | 4.57 | 3.17 | 2.64 |
| **Māori, syllables** | 52 | 4.12 | **3.10** | 1.93 |

**Result.**
- **Raw glyphs.** Voynich's conditional entropy (2.10) sits between Māori letters (2.49) and nothing European. Notes §2, §4 and §19 said that h2 of about 2.1 is lower than any natural language. That claim was tested only on Latin, Italian, German, English and Hebrew. A Polynesian language closes most of the gap.
- **Merged units.** With glyphs merged to about 50 units, Voynich resembles the Māori syllabary closely: inventory 50 vs 52, h2 3.17 vs 3.10. The difference is word length, 2.6 vs 1.9 units.

**Prior work.** Bennett (1976) found Hawaiian to be the language closest to Voynich in entropy (voynich.nu, "a2_char"). Lindemann & Bowern (2020), over 294 Wikipedia languages, found that glyph manipulations do not bring Voynich into the natural range. The Māori figures here confirm the Polynesian point with a measured second case. Whether Lindemann & Bowern's 294 languages include Māori or Hawaiian I have not checked, so I do not claim agreement or disagreement with them.

**Meaning.** This does not suggest the text is Polynesian. Its date and place exclude that historically. What it shows is that the low entropy, the strongest statistical argument against a natural language (§7, H1), is matched by natural languages with a small CV syllable structure. Strictly, the entropy argument excludes a European alphabetic plaintext written one glyph per letter, not natural language as such. Correct §7's H1 verdict accordingly: *dead for European alphabetic plaintext; open for a language with a small, simple syllable inventory under some notation.*

## 60. A Kober/Ventris-style syllabic grid cannot be recovered from context alone, even in Māori (`grid.py`, `data/grid.out`)

If the units of §58 were a consonant×vowel syllabary, the next step would be the Linear B method: arrange signs in a grid where rows share a consonant and columns share a vowel. Before trying that on Voynich, I tested whether the grid can be recovered from distributional context, on Māori syllables (§59), where the true grid is known. Each sign is described by the distribution of signs to its left, or to its right. The signs are clustered by k-means on Hellinger-transformed distributions, 10 seeds. Agreement with the true classes is normalized mutual information (NMI). The baseline is random labels with the same number of classes.

| clustering | vs vowel (5 classes) | random 5-way | vs consonant (10 classes) | random 10-way |
|---|---|---|---|---|
| left context | 0.19 | 0.12 | 0.41 | 0.31 |
| right context | 0.21 | 0.13 | 0.40 | 0.36 |

All values are means over seeds.

**Result: the positive control nearly fails.** In a real CV syllabary, context clusters recover the consonant classes only slightly better than random labels, 0.40 vs 0.31–0.36. They recover the vowels a little better, 0.20 vs 0.12. Context alone does not reveal the grid. Ventris needed inflectional alternations, Kober's "triplets": the same stem with different endings, where the alternating signs share a consonant. He also needed place names as anchors. So I do not apply this method to the Voynich units: a null result there would mean nothing.

The Kober-triplet version is possible in principle, since the Voynich slot grammar has stem + ending alternations (§8). But it assumes the endings are inflections spelled syllabically, which §8 (prefix and suffix independent, no agreement) argues against.

## 61. Lossy Italian syllabary, one sign per unit: control recovered exactly, Voynich far off (`syllabary.py`, `runs5/`)

Tests the family left open by §58–59: a small syllabary for a European language. Target: Italian (Dante). Each syllable is reduced to a *sign* made of its onset (at most two consonants) and vowel, dropping codas as Linear B does, and the 60 commonest signs are kept. Sign-bigram model, with word boundaries, trained on the first half of Dante. Voynich paragraph glyphs (12,000 words) are BPE-merged to exactly 60 units (§58). The search looks for the unit→sign mapping that maximizes the model's score per token, by annealing, 400,000 steps, 3 seeds.

**Many-to-one search is degenerate.** With many-to-one mappings allowed, the search on the positive control finds keys that score *better* than the true key (−2.08 vs −2.28) while mapping only 5–10% of units correctly. This is the collapse of §33. Since both inventories have 60 items, the search was restricted to one-to-one mappings (swap moves).

| input | best score per token, 3 seeds | key recovered |
|---|---|---|
| Italian (held-out half), signs randomly relabeled | **−2.277** in all three | **100%** of units in all three |
| true Italian with true signs (reference) | −2.277 | |
| **Voynich, 60 BPE units** | **−3.375 to −3.421** | |
| slot self-citation generator, 60 BPE units | −3.866 | |

**Result: negative.** The one-to-one search recovers a hidden Italian syllabary key exactly. On the Voynich text it ends 1.1 nats per token below a real decipherment. That is much closer to gibberish than to Italian, though the Voynich does fit better than the generator. A 60-sign onset+vowel syllabary of Italian, one sign per Voynich unit, does not fit.

**Limits.** The Voynich units are BPE merges chosen by frequency, and the true units of a syllabary could be cut differently. Only Italian was tested, with one syllable model. A homophonic syllabary, several Voynich units per sign, was not tested, because the many-to-one form is degenerate under this score (§33).

**Extension: Latin, and 40 / 60 / 80 signs (`runs5/batch2.sh`, `runs5/summary2.out`).** Same one-to-one search, 2 seeds per cell. The Latin model is trained on the first half of Pliny; the control uses the second half.

| target, signs | control: best (true) | key recovered | Voynich best | gap to true |
|---|---|---|---|---|
| Italian, 40 | −1.987 (−1.987) | 100%, 100% | −3.38 | 1.39 |
| Italian, 60 | −2.277 (−2.277) | 100% ×3 | −3.38 to −3.42 | 1.10 |
| Italian, 80 | −2.42 / −2.44 (−2.42) | 100%, 97% | −3.45 to −3.48 | 1.03 |
| Latin, 40 | −2.423 (−2.423) | 100%, 100% | −3.06 to −3.08 | 0.65 |
| Latin, 60 | −2.777 (−2.777) | 100%, 100% | −3.26 to −3.29 | 0.50 |
| Latin, 80 | −2.93 / −2.95 (−2.93) | 97%, 93% | −3.37 to −3.39 | 0.45 |

Scores are per token.

**Result: negative throughout.** The control key is recovered at 93–100% in every cell, so the search works at all three sizes and in both languages. Voynich ends 0.45–1.39 nats per token below the true-key score in every cell. The Latin gaps are smaller than the Italian ones because Latin signs are less predictable to begin with, so the true score is lower. A one-sign-per-unit syllabary of Italian or Latin, at 40–80 signs, does not fit the Voynich units.

## 62. One-to-one codebook, Voynich word → Italian word: negative, with a partly powered control (`codebook.py`, `runs6/`)

H5 (codebook / nomenclator) was judged "poor" in §7 from the hapax rate, but never tested directly. Here the 300 commonest Voynich word types are mapped one-to-one onto the 300 commonest Italian word types (Dante, first half), and all other words count as one out-of-vocabulary (OOV) token. The score is an Italian word-bigram model per token, searched by swap annealing, 1.5 million steps, 2 seeds. 22,000 tokens per input.

| input | OOV share | best score per token | key recovered |
|---|---|---|---|
| Italian held-out half, top-300 types relabeled | 0.40 | −3.379, −3.388 (true key −3.283) | 33% and 28% of types; 36% and 18% of the top 50 |
| **Voynich** | 0.37 | **−4.369, −4.372** | |

**Result: negative for Italian.** With a similar OOV share, the Voynich input ends about 1.0 nat per token below even the partly recovered control, and 1.1 below the true key. The control's own recovery is incomplete: the word-bigram model is sparse, and many swaps of rare words do not change the score. So this test is less sharp than the syllabary test of §61. But a gap of 1 nat per token is far outside the control's range. The best Voynich decoding reads `_ _ mi _ lor _ _ da quelle _ _ _ si da _ _ fia _ tuoi tuoi _ _ valle…`: Italian function words strung together without syntax.

**Not usable, recorded so the mistakes are not repeated:**
- **Latin.** Pliny's 300 commonest forms cover only 27% of tokens (OOV share 0.73), because Latin is heavily inflected. The score is then dominated by OOV→OOV transitions, and the search beats the true key while recovering 0–3% of types. A Latin codebook test would need lemmatized text.
- **Generator.** Its top 300 types cover only 32% of its tokens (OOV share 0.68), so its scores are not comparable with the Voynich input's.

**Repair attempts for the codebook test, both failed (`runs6/summary2.out`, `runs6/summary3.out`).**
1. **Latin cut to 4-letter stems** (`latin4`). The top 300 stems cover 54% of tokens, but the control still beats its true key (−3.05 vs −3.21) while recovering 0–2% of types.
2. **Scoring only in-vocabulary → in-vocabulary transitions** (`INV=1`). The Italian control now recovers *nothing* (0%, score −5.71 vs true −4.83), and the Latin-stem control again beats its true key without recovering it.

So at this scale, 300 types and about 22,000 tokens, the word-bigram codebook search is underpowered. A sparse word-bigram model has many near-equivalent optima that are not the true key. The only cell with any power is the original Italian run above (28–33% recovered), and that is the only codebook result I count: Voynich about 1 nat per token below it. A properly powered codebook test would need a smoother language model (class-based or neural), or far more text than the Voynich provides.

## 63. Zodiac labels as 30 ordered entries: no alignment under any rotation or reflection (`zodiac_align.py`, `data/zodiac_align.out`)

§22 compared label *i* of one sign with label *i* of another in ZL's order, and found nothing. But ZL's order depends on where the transcriber began each ring and which way they read. If the 30 labels per sign were degree numbers, day names or decan names in a fixed sequence, *some* rotation or reflection should line them up. For the 7 complete signs (Pisces, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius), each sign's labels were ordered ring by ring and by clock angle within a ring. Then, for every pair, I took the best mean label similarity (1 − normalized edit distance) over all 30 rotations × 2 directions. The same maximum was computed after shuffling one sign's labels, which keeps the multiple-comparison advantage of taking a maximum.

- 21 pairs. 1 has p < 0.05 (chance expects 1.1).
- That pair, Virgo–Scorpio (similarity 0.410 vs 0.367 for shuffled), has p = 0.011 with 5,000 shuffles, above the Bonferroni threshold of 0.0024 for 21 pairs. Its best alignment has **no** exact label match. The similarity comes from shared `ok-/ot- … -eedy` shapes (`ykeeor/ykeeory`, `yteedy/oyteedy`, `okeody/okeey`). Virgo and Scorpio are both on the `e`-side of the f72 label switch (§24), so they share label style.

**Result: negative.** Under no rotation or direction do the 30 labels of one sign correspond to those of another. A fixed 30-name sequence, the same degree or day names on every wheel, is excluded. It is also excluded for any start point or reading direction.

## 64. Homophonic syllabary: the held-out order test cannot separate a cipher from gibberish here (`syllabary.py` with 100 units, `runs5/summary3.out`)

This tests the many-to-one form left open in §61. 100 units map onto 60 Italian onset+vowel signs. The control is Italian with each sign split into 1+ homophones (100 labels in all). The Voynich and generator inputs are BPE-merged to 100 units. The key is fitted on the first half of the words, by annealing, 400,000 steps, 3 seeds. On the second half, the gain is the score in true order minus the score with the units shuffled *within each word*. (A bigram model with word boundaries is blind to whole-word shuffles, so §37's token shuffle has no direct analogue here.)

| input | train score per token | held-out within-word order gain | key recovered |
|---|---|---|---|
| Italian control, true key | −2.278 | **+0.69 to +0.70** | |
| Italian control, fitted key | −2.087 to −2.098 (beats true) | +0.32 to +0.35 | 10–13% |
| **Voynich** | −2.224 to −2.234 | **+0.50 to +0.51** | |
| self-citation generator (meaningless) | −2.580 | **+0.60** | |

**Result: the test fails.** Meaningless generator text gains almost as much from within-word order as a true key does, and more than the Voynich. Its words follow the rigid slot grammar (§5), so any key that maps word-initial units to word-initial syllables and word-final units to word-final syllables gains from that order. The search also never finds the true homophonic key (10–13% correct), while its wrong keys again beat the true key on the training score (§33). So the homophonic syllabary stays **untested**: neither the training score nor this held-out gain can tell a real key from a fitted one on text with Voynich-like word structure. A usable test would have to measure dependencies *across* words, and a bigram model with boundary tokens has none.

**Bookkeeping.** The three generator runs are identical because `generators2.py` calls `random.seed(11)` when executed, which overrides the run's seed. The same applies to the generator runs in §61 and §62. The generator text is therefore a single sample in all of them.

## 65. Cross-word held-out test for Italian syllabaries (one-to-one and homophonic): calibrated, and negative (`syllabary.py` with `TRI=1`, `runs5/summary4.out`)

This is the fix for §64. The score is now a sign *trigram* over the running sequence, with the boundary as a sign. That captures (last sign of word 1, boundary, first sign of word 2), so shuffling whole words changes the score. The held-out gain, real word order minus shuffled word order on the second half, then measures dependencies *between* words. Meaningless copying text has almost none (§17). The key is fitted on the first half, by annealing, 400,000 steps, 3 seeds. The generator's seed override (§64) is fixed, so its runs are now independent samples.

| input | units → 60 signs | key recovered | train score per token | held-out cross-word gain |
|---|---|---|---|---|
| Italian control, true key | | | −2.148 | **+0.074 to +0.078** |
| Italian control, one-to-one search | 60 | **100%** ×3 | −2.148 | **+0.078 to +0.079** |
| Italian control, homophonic search | 100 | 13–19% | −2.215 to −2.245 | +0.002 to +0.007 |
| **Voynich** | 60 | | −3.70 to −3.74 | **−0.006 to +0.006** |
| **Voynich** | 100 | | −2.439 to −2.444 | **−0.002 to +0.001** |
| generator (meaningless) | 60 / 100 | | −4.08 to −4.12 / −2.58 to −2.60 | −0.001 to +0.002 |

**The measure is calibrated.** A true key gains about +0.077 from cross-word order, and wrong keys, including the homophonic control's 13–19%-correct keys, gain essentially nothing. Unlike the within-word gain of §64, the meaningless generator also gains nothing.

**Result: negative for both forms.** The keys fitted to the Voynich text, one-to-one or homophonic, gain nothing from word order on held-out text, the same as wrong keys and gibberish. The Voynich does have cross-word dependencies (the `y | qo` junction, §20), but no fitted key turns them into Italian syllable order across words.

**Limits.** As in §37, this shows the keys found for the Voynich are not real. It does not show that a real homophonic key would be found, since the search misses the true key on the homophonic control. Italian only, 60 signs, frequency-based BPE units.

This closes the gap §61 and §64 left. The homophonic Italian syllabary is now covered by a test that passes its control, and fails on the Voynich.

**Latin, and the noise level of the cross-word gain (`runs5/summary5.out`, `runs5/nullkeys.out`).** The same test with Latin (Pliny) as target. A null distribution was added: the gain of 30 *random* one-to-one keys on the same input.

| target | true key gain | random keys on the control: mean ± sd | Voynich fitted key gain | random keys on Voynich: mean ± sd (max) |
|---|---|---|---|---|
| Italian | +0.078 | +0.006 ± 0.010 | +0.003 (seed 1) | +0.001 ± 0.010 (+0.020) |
| Latin | +0.010 | +0.001 ± 0.007 | +0.016, +0.007 | +0.001 ± 0.010 (+0.024) |

- **Italian.** The true key's gain is about 7 sd above random keys, so the test has power. The Voynich keys sit inside the random-key range. Negative, as stated above.
- **Latin.** The true key gains only +0.010, about 1.3 sd above random keys, because Latin word order is free and syllables at word boundaries barely depend on each other. The test has **no power** for Latin. The Voynich value, +0.016, is within the random-key range (max +0.024) and means nothing.
- **Homophonic Latin (100 units).** The search collapses again: its training score beats the true key's (−1.64 vs −2.67) with zero gain, on the control and on the Voynich alike.

So §65's conclusion holds for **Italian only**. Latin syllabaries remain covered only by the training-score test of §61.

## 66. Where things stand after §54–65

**New exclusions, each with a control that passes:**
- **Italian or Latin syllabary, one sign per merged unit, 40–80 signs.** The control key is recovered at 93–100%, and Voynich falls 0.45–1.39 nats per token short (§61).
- **Italian syllabary, one-to-one or homophonic, by the cross-word held-out test.** The true key gains 7 sd over random keys, and the Voynich keys sit at random-key level (§65).
- **Codebook, Voynich word → Italian word.** Voynich falls 1 nat per token short of a partly recovered control (§62).
- **A fixed 30-name sequence on the zodiac wheels,** under any start point or direction (§63).

**Untested, because the controls fail, recorded so they are not mistaken for exclusions:**
- Latin codebook (§62)
- Latin syllabary by cross-word gain (§65)
- homophonic syllabary by within-word gain (§64)
- syllabic grid from context (§60)

**Structural results:**
- **Entropy.** The low-entropy argument rules out a European *alphabetic* plaintext, not natural language as such: Māori comes close (§59). Merged to about 50–60 units, Voynich has the size profile of a small syllabary (§58).
- **Topic clustering.** It does not separate meaning from a copying procedure (§54).
- **Page-exclusive repeated words.** Herbal-A pages have about three times fewer than a real Latin herbal at matched size (§55). Labels are tied to their page no more than any word is (§56). The identified plants run in no alphabetical order (§57).

**Method lessons**, now applied throughout:
1. Every search needs a positive control run under the same conditions.
2. Many-to-one keys collapse under language-model scores, so use one-to-one keys or held-out tests.
3. Held-out gains need a random-key null.
4. Compare at matched page counts, not only matched page lengths (§55).
5. Check reference files (the empty Vulgate, §49) and generator seeds (§64).

## 67. Catalan syllabary (*Tirant lo Blanch*, 1490): strongest control yet, Voynich negative (`syllabary.py catalan`, `runs5/summary6.out`)

**Why Catalan.** The later-hand month names on the zodiac pages are usually read as Occitan or Catalan. Catalan is a Romance language with fairly simple syllables, and the cross-word test has power for Italian (§65).

**Source.** The Valencian *Tirant lo Blanch* (1490), from Catalan Wikisource page transcriptions of the 1873–1905 edition, about 98,000 words (`data/ext_cat/`, not committed). The page wikitext encodes letters as templates: `{{s}}` for long s, `{{ct}}`, `{{Maj|…}}`. A first fetch that stripped them produced damaged words like "pert" for *expert*, and was redone. The editor's introduction is skipped. `y` is read as i, as in the old orthography.

**Test.** As in §65: 60 onset+vowel signs, 60 Voynich BPE units, one-to-one search, 400,000 steps, 3 seeds. Sign trigram across word boundaries, cross-word held-out gain, and 30 random keys as the null.

| input | train score per token | key recovered | held-out cross-word gain | random keys: mean ± sd |
|---|---|---|---|---|
| Catalan control | −1.826 (= true key) | **100%** ×3 | **+0.143 to +0.145** | +0.003 to +0.009 ± 0.012–0.014 |
| **Voynich** | **−3.904 to −3.912** | | **−0.004 to +0.014** | −0.003 ± 0.008–0.011 |

**Result: negative.** This is the strongest calibration of any target so far: the true key's cross-word gain is about 10 sd above random keys. On the Voynich, the best one-to-one key falls 2.1 nats per token below the true Catalan score, and gains no more from word order than random keys do. A 60-sign onset+vowel syllabary of Catalan, one sign per merged unit, is excluded on both measures.

**Limits** as before: frequency-based BPE units, one syllable model, and the homophonic form not found on its own control (§64–65).

## 68. Letter-or-pair word cipher (Naibbe form), held-out word-order test, Catalan target (`pairchipher.py catalan`, `runs4/summary7.out`)

Same as §37–39 with *Tirant lo Blanch* as plaintext and language model (§67): Language B, 4 million steps, 3 seeds. `y` is read as i, so decodings containing `y` are rejected outright (zero frequency in the target).

| input | key | held-out gain from word order, per letter |
|---|---|---|
| Catalan control | true key | +0.604 to +0.628 |
| Catalan control | fitted, about 99% wrong | +0.047 to +0.078 |
| **Voynich B** | fitted | **+0.032 to +0.048** |

**Result: negative.** The Voynich keys gain no more from word order than wrong keys fitted to real Catalan ciphertext, and about a fifteenth of a true key. With §37–39, the letter-or-pair word cipher is now excluded by the held-out test for Latin, Italian, German, Hebrew and Catalan.

## 69. One-to-one codebook, Voynich word → Catalan word (`codebook.py catalan`, `runs6/summary4.out`)

Same as §62 with *Tirant lo Blanch*. Catalan is less inflected than Latin: its top 300 word types leave an OOV share of 0.31, against Voynich's 0.37. Word-bigram model, swap annealing, 1.5 million steps, 2 seeds.

| input | OOV share | best score per token | key recovered |
|---|---|---|---|
| Catalan control (held-out half, relabeled) | 0.31 | −3.542, −3.531 (true key −3.373) | **38%, 39%** of types; 40%, 38% of the top 50 |
| **Voynich** | 0.37 | **−4.450, −4.470** | |

**Result: negative.** This is the best-powered codebook control so far, recovering 38–39% of the key, better than Italian's 28–33%. The Voynich falls 0.9 nat per token below it, with a slightly higher OOV share. That difference favors the Voynich, because OOV transitions score high (§62). Its best decoding is Catalan words in no syntax: `_ _ en _ feu _ _ mes feren _ _ _ a mes _ _ hon _ voluntat voluntat _ _ hagues a sera…`. A word-for-word codebook into Catalan is excluded at this level of power, as for Italian.

## 70. One word → one letter (homophonic), Catalan target, language B (`wordcipher2.py catalan`, `runs7/summary.out`)

Same as §32: 300 commonest B word types (66% of tokens), with controls dropping 33.6% of tokens to match. Annealing, 10 million steps, 3 seeds; the target is *Tirant lo Blanch*.

**Bug found and fixed first.** In the first Catalan run all six searches stood still at their starting key. `y` is read as i in Catalan, so `y` has zero frequency. But the initial key gave every letter at least one word type, so the letter-frequency penalty (KL against the target frequencies) was infinite. Every step then evaluated to NaN and was rejected. Letters absent from the target are now excluded from the key. Latin and Italian contain every letter of the alphabet used, so the earlier runs (§30–32) were not affected. I checked this.

| input | best score per letter | key recovered |
|---|---|---|
| Catalan control, seeds 1 and 3 | −2.605, −2.615 (true key −2.62 to −2.64) | **97%, 96%** of types |
| Catalan control, seed 2 | −2.719 | 2% (search failed) |
| **Voynich B** | **−2.793 to −2.807** | |

**Result: negative.** The search recovers the Catalan key in 2 of 3 restarts. All three Voynich restarts end below even the failed control search, 0.19 per letter short of a recovered key. Together with §30–32, a one-word-per-letter homophonic cipher of the 300 commonest words is excluded for Latin, Italian and Catalan.

## 71. Homophonic Catalan syllabary (100 units → 60 signs): the control is found for the first time, and Voynich is negative (`runs5/summary7.out`)

This is §64–65's homophonic form with Catalan as target (§67): sign trigram across words, 400,000 steps, 3 seeds, 30 random many-to-one keys as the null. Unlike Italian (13–19%) and Latin (collapse), the Catalan homophonic control is *partly found*.

| input | train score per token | units correctly mapped | held-out cross-word gain | random keys: sd |
|---|---|---|---|---|
| Catalan control, true key | −1.826 | | +0.145 to +0.147 | |
| Catalan control, fitted | −1.905 to −1.937 | **56–68%** | **+0.029 to +0.077** | 0.005–0.009 |
| **Voynich** | **−2.781 to −2.844** | | **−0.001 to +0.001** | 0.008 |
| generator (meaningless) | −3.12 to −3.26 | | −0.000 to +0.000 | 0.004–0.007 |

**Result: negative, with a working control.** Partly correct homophonic keys on the Catalan control gain 4–10 sd from cross-word order. The Voynich keys gain nothing, sitting exactly at random-key level, and end about 0.9 nat per token below the control's fit. This is the first homophonic-syllabary test whose control finds most of the key. The homophonic Catalan syllabary at 100 units is excluded on both measures.

**Currier A and B separately (`SUBSET=A|B`, `runs5/summary8.out`).** All syllabary runs above mix A and B, which would hide a real key if the two used different keys. Rerun on each language alone, against Catalan, 2 seeds, 20 random keys per run. A has only about 11,300 words, so its fitting half is about 5,600 words, smaller than the controls'.

| subset, units | train score per token (true Catalan −1.83) | cross-word gain | random keys: mean ± sd |
|---|---|---|---|
| A, 60 one-to-one | −3.84, −3.85 | +0.007, +0.013 | about −0.004 to +0.002 ± 0.009 |
| A, 100 homophonic | −2.71, −2.75 | +0.003, +0.005 | about −0.003 ± 0.008 |
| B, 60 one-to-one | −3.91, −3.92 | +0.018, +0.023 | about −0.003 to +0.005 ± 0.009–0.010 |
| B, 100 homophonic | −2.69, −2.74 | +0.000, +0.004 | about −0.002 ± 0.008 |

Random-key means and sds differ slightly between seeds.

**Result: unchanged.** No subset comes near the control. The best case, B with one-to-one keys, gains about 2 sd over random keys, a seventh of the true key's +0.14. Its training fit is 2.1 nats per token below a real Catalan key. Random keys on B gain nothing, so the excess appears only for fitted keys. It may come from a fitted key exploiting B's own cross-word habits (the `y | qo` junction), but I have not tested that. Either way it is nothing like a decipherment. Splitting A from B does not rescue the syllabary readings.

## 72. A rule-based model of the text: how far simple scribal rules go (`scorecard.py`, `gen3.py`, `gen3_fit.py`, `gen3_check.py`, `data/scorecard_*.out`, `data/gen3_*.out`)

**Scorecard.** `scorecard.py` measures any text laid out on the real page and line structure (34,950 paragraph tokens) on: type/token ratio, hapax share, word length, h2, adjacent repeats, line-initial repeat ratio (§44), page-exclusive repeat rate at 40 pages (§55), and the `y | qo` junction ratio (§20).

**The §17 generator fails five of these.** Types/tokens 0.36 vs 0.20, h2 2.47 vs 2.10, line-initial ratio 1.30 vs 0.50 (no alternation), page-exclusive rate 0.99 vs 0.30, junction ratio 1.01 vs 3.88.

**A rule model.** To separate the *sequence* question from word formation, the lexicon is the real set of word types, so word-internal statistics match by construction. The writing process then has five parameters:
- **One-shot words.** With probability `p_new`, write a new word that is never reused, drawn from the real hapaxes.
- **Local copying.** With `p_local`, copy a non-one-shot word from earlier on the page.
- **Page topic.** With `topic_p`, use one of `topic_n` page-favored words.
- **Junction rule.** After a `y`-final word, prefix `q` to an `o`-word (`p_q`); otherwise strip `q` from a `qo`-word (`p_unq`).
- **Line rule.** With `p_alt`, redraw a line's first word if it starts like the previous line.

These were fitted by random and local search. Best: `p_new 0.22, p_local 0.03, topic_p 0.08, topic_n 26, p_q 0.92, p_unq 0.39, p_alt 0.62`, and `p_rep 0.006` for immediate repeats.

| statistic | real | model, 3 independent samples |
|---|---|---|
| types/tokens | 0.197 | 0.192–0.193 |
| hapax share | 0.674 | 0.712–0.718 |
| h2 | 2.102 | 2.085–2.090 |
| adjacent repeats | 0.008 | 0.007–0.009 |
| line-initial repeat ratio | 0.504 | 0.474–0.517 |
| y→qo junction ratio | 3.875 | 3.56–3.92 |
| **page-exclusive rate** | **0.302** | **0.436–0.460** |

**Result.**
- **Most statistics are matched.** Two scribal rules (prefix `q` after `y`; do not start a line like the line above), one-shot words for 22% of tokens, and a little page-topic reuse reproduce all the sequence statistics except one. Copying is rare (3%), much rarer than in Timm & Schinner-type self-citation.
- **The remaining mismatch.** Page-exclusive repetition stays about 50% too high. The real text keeps even *less* page-specific repetition than this model: its page-favored words recur elsewhere more.
- **What the parameters say.** 22% of tokens are single-use, which is the page-specific vocabulary written once (§55). Junction and line rules are near-deterministic (0.92 and 0.62).

**What this does and does not show.** It does not show the text is meaningless: the lexicon is the real one, so the model inherits whatever the words encode. It shows that the *sequence-level* oddities can be described as a few explicit scribal rules applied on top of a word stream. The word stream itself has almost no topic structure, and the page-specific words appear once. A meaningful text written under such rules would look the same, so this does not decide between meaning and procedure. It does say where meaning would have to live, if anywhere: in the choice of words, not in their arrangement.

A plug-in word-pair MI check was tried and dropped. At this sparsity it gave the real text a *negative* excess over its own within-line shuffle, so it is bias-dominated and unlike the class-level measure of §17.

**Follow-up: the mismatch is local copying (`data/gen3_favmin.out`, `data/gen3_check_nocopy.out`).** Restricting page-favored words to common words lowers the page-exclusive rate only slightly (0.35–0.47). Switching mechanisms off shows the source. With no local copying, a light page topic alone (`topic_p 0.08`) gives 0.26–0.29, matching the real 0.30. Adding even 3% copying from earlier on the page raises it to 0.43–0.46. With `p_local = 0`, every statistic on the scorecard is matched:

| statistic | real | model, no copying, 3 samples |
|---|---|---|
| types/tokens | 0.197 | 0.193 |
| hapax share | 0.674 | 0.713–0.717 |
| h2 | 2.102 | 2.088–2.091 |
| adjacent repeats | 0.008 | 0.008–0.009 |
| line-initial repeat ratio | 0.504 | 0.455–0.482 |
| page-exclusive rate | 0.302 | 0.258–0.291 |
| y→qo junction ratio | 3.875 | 3.65–3.82 |

**Meaning, corrected after a further check (`gen3_vertical.py`, `data/gen3_vertical.out`; refined again in §73, which supersedes the near-copy reading below).** The real text is matched best with no *exact* copying from earlier on the page. I first wrote that this cuts against self-citation. It does not. Timm & Schinner's vertical-neighbor effect (§23) is not on the scorecard. A word's minimum edit distance to the words near the same position in the line above is 3.46, against 3.81 for the same positions on another page, a difference of 0.35. Every rule model shows no such effect: −0.01 with no copying, −0.01 with 3% copying, +0.03 with 15% exact copying.

So the real text contains **near-copies**, words resembling those just above them, while exact page-specific repetition stays low. That is what copy-*and-modify* predicts, and what neither exact copying nor a plain word stream produces. The two observations fit together if most "new" words are modified versions of nearby ones. That would also explain why the page-specific vocabulary is written only once (§55). A complete model needs a modification step that turns a nearby word into a similar new form. The rule model here borrows its forms from the real lexicon, so it cannot show that. What this section does establish: the junction and line rules are near-deterministic scribal rules, and exact local copying is rare.

## 73. The vertical-neighbor effect, split into its parts (`vertical2.py`, `data/vertical2.out`)

The 0.35 difference in §72 compared the line above with *any other page*, so page and section similarity were counted as "vertical". Here the same measure (minimum edit distance from a word to the words at positions j−1..j+1) is taken against four kinds of line. Each figure is the mean of 5 runs of 4,000 words.

| comparison line | Voynich | sd over runs |
|---|---|---|
| (a) the line directly above | 3.412 | 0.020 |
| (b) same page, 3 or more lines away | 3.501 | 0.018 |
| (c) another page of the same section, Currier language and hand | 3.640 | 0.013 |
| (d) any other page | 3.801 | 0.016 |

The gradient splits into a nearby-line part (b−a) of +0.09 (sd 0.025), a page part (c−b) of +0.14 (sd 0.016), and a section, language and hand part (d−c) of +0.16 (sd 0.015).

**Position.** Within the line above, a window at the word's own position is no closer than a window 4 or more positions away: 3.382 against 3.352, a difference of −0.03 (sd 0.013). The slight reversal is a window-edge effect, since a line-initial word has a two-word window. Pliny shows it too (4.98 against 4.88). Nothing here is specific to the word directly above. What exists is a closeness to nearby lines.

**Reference texts**, laid out in order on the Voynich page and line shapes, with the Voynich section labels applied to the resulting consecutive chunks:

| text | (a) | (b) | (c) | (d) | nearby lines | page | section |
|---|---|---|---|---|---|---|---|
| Pliny (Latin) | 5.036 | 5.147 | 5.239 | 5.304 | +0.111 (sd 0.020) | +0.092 (sd 0.031) | +0.065 (sd 0.034) |
| Dante (Italian) | 3.480 | 3.503 | 3.530 | 3.524 | +0.022 | +0.027 | −0.006 |
| *Tirant* (Catalan) | 3.557 | 3.595 | 3.608 | 3.636 | +0.038 | +0.013 | +0.028 |

**Meaning.** The nearby-line part is the same size in the Voynich (+0.09, about 2.3% of the any-page distance) as in Pliny's topical prose (+0.11, about 2.1%). It needs no copying mechanism. A text that stays on one subject for a few lines produces it. The Voynich differs in the page and section parts. Its total gradient is about 10% of the any-page distance, against 5% for Pliny and 1–2% for Dante and *Tirant*. The section part includes the Currier A/B and hand differences, which are differences of spelling or dialect, not of subject. So the Voynich word forms cluster strongly by page and by section, while exact repetition of page-specific words stays low (§55).

This replaces the conclusion added to §72. The vertical-neighbor effect does not by itself show copy-and-modify. Its line-scale part is ordinary, and nothing in it is tied to position. What remains to explain is the page-scale and section-scale clustering of *forms* (similar, not identical, words). Both a meaningful text, whose spelling of related words or inflections varies by topic, and a page-wise copy-and-modify procedure could produce it. The rule model of §72 produces none of it, because its page favorites are drawn from the global lexicon.

## 74. Can a stem model produce the page clustering of word forms? (`gen4.py`, `gen4_fit.py`, `gen4_tradeoff.py`, `gen4_mut.py`, `pageshuffle.py`, `data/gen4_*.out`, `data/pageshuffle.out`)

**What carries the clustering in the real text** (`vertical2.py`, 5 runs of 4,000 words). Ignoring words identical to the target leaves most of the gradient: nearby lines +0.074, page +0.119, section +0.143, against +0.088, +0.139 and +0.161 with them. So the clustering is mostly of *near* forms, not repeats. One-shot words take part: their page part is +0.117 (sd 0.023), on a larger any-page distance of 4.89. Recurrent words give +0.122 (sd 0.027).

**Model-free check.** Shuffle the real words among the pages of their own section, language and hand group, keeping page and line shapes:

| | real | within-group shuffles (6) |
|---|---|---|
| page-exclusive rate (40 pages) | 0.299 | 0.187 (0.156–0.204) |
| page part of the gradient | +0.121 | −0.004 (−0.026 to +0.009) |
| page part, identical words ignored | +0.093 | −0.003 (−0.029 to +0.015) |

The page-exclusive figure here differs slightly from §72 (0.302) because the draws differ. Both page effects are real and lie far outside the shuffles. Exact repeats concentrate on pages more than chance (0.30 against 0.19), and near forms do too. The section part needs no explanation beyond the groups' different vocabularies. A model drawing each group from its own real lexicon gives +0.14 to +0.17, against +0.17 real.

**The stem model.** It extends §72. Each group draws from its own real lexicon and its own one-shot words, and each page takes stems from a group stem set. A share `p_kl` of lexicon draws is the closest of `k_l` draws to a page stem, by edit distance divided by length; one-shot words are the closest of `k_h`. With `k_l`=3, two seeds each:

| p_kl | page part | section part | page-exclusive | hapax share | h2 |
|---|---|---|---|---|---|
| 0 | +0.01, +0.03 | +0.14, +0.12 | 0.38, 0.38 | 0.71 | 2.09 |
| 0.5 | +0.07, +0.08 | +0.22 | 0.38, 0.40 | 0.72 | 2.03 |
| 0.75 | +0.11, +0.13 | +0.23 | 0.39, 0.37 | 0.73 | 2.00 |
| 1.0 | +0.16, +0.18 | +0.31, +0.29 | 0.41, 0.45 | 0.74–0.75 | 1.96–1.97 |
| real | +0.15 (this run) | +0.17 | 0.30 | 0.67 | 2.10 |

(A first run of this table left an older neighbor-pull option, `p_nl`=0.2, switched on. These are the rerun figures with it off. The pattern did not change.)

A random search over all parameters (4 × 40 draws, `data/gen4_fit_*.out`) found no setting that matches everything. The best fits keep page-exclusive near 0.34 but reach only +0.04 to +0.08 on the page part. Pulling the page part up to the real value overshoots the section part, raises the one-shot share and lowers h2. Even the baseline, with group lexicons and no stems, is already too high on page-exclusive and one-shot share.

**A variation step** (`gen4_mut.py`, `data/gen4_mut.out`). One-shot words are made by joining the head of a page stem to the tail of a real one-shot word, cut at random glyph boundaries. This keeps h2 at the real value (2.09) and, with half the one-shot words made this way, the one-shot share as well (0.66). But it yields almost no page clustering: −0.01 to +0.05 across `p_mut` 0–1 and two seeds. Crossover with a random tail destroys most of the resemblance to the stem.

**Meaning.** The real text has two page-level properties at once. Exact repeats concentrate on pages, and so do similar-but-different forms, with 75–85% of the page part remaining when identical words are ignored. Selecting forms that resemble page stems reproduces the second only by distorting the vocabulary statistics. The model draws on the real lexicon at random and then selects, so it is too crude to rule the copy-and-vary family out. It is not a fit either, and the meaningless-text hypothesis still lacks a generator that passes every test. Topical text in a language whose related words share stems, such as inflections or compounds, would produce both properties naturally. That does not show the Voynich text is such a text. It means this statistic does not separate the two hypotheses yet.

## 75. Pages have their own spelling profile, of the size topical text has (`gen4_mut.py edit [page]`, `pageprofile.py`, `data/gen4_mut_*.out`, `data/pageprofile.out`)

**Edit-based variation fails too.** One-shot words were made by changing 1 or 2 glyphs of a page stem, each new glyph drawn given the glyph before it. Page part: −0.015 to +0.039 (`data/gen4_mut_edit.out`). With the stem taken from the words already written on the same page, in self-citation style, it is −0.039 to +0.008 (`data/gen4_mut_page.out`). The real value is +0.15. At `p_mut`=1 with one edit, the second version also pushes page-exclusive to 0.63–0.65. The reason is that each variant resembles one source word. A random line elsewhere on the page rarely contains that word, so the gradient hardly moves. The real page part, which survives when identical words are ignored (§74), must be diffuse: a word is closer to many words on its page, not to one source.

**Direct test.** For a set of word features, I took the variance of the per-page rate across the 186 pages with 60 or more words. The ratio is that variance over the mean variance of 20 within-group shuffles (§74), where 1 means no page profile beyond the section, language and hand group. In the Voynich every feature lies far outside the shuffles:

- starts ch 2.89, ends n 2.62, starts sh 2.43, starts o 2.37
- ends r 1.93, has t 1.92, starts d 1.78, has a 1.73, has k 1.72, length 6+ 1.72, has ckh/cth 1.70
- ends y 1.65, ends l 1.64, has ee 1.63, has p/f 1.44, starts qo 1.34, ends dy 1.19

The largest shuffle for any feature was 1.16.

**Against reference texts.** Language-neutral features were used: the 6 commonest first letters, last letters and contained letters of each text. Each text was laid out in order on the Voynich pages, with the same group labels.

| text | median ratio | range over 18 features |
|---|---|---|
| Voynich | 1.78 | 1.18–2.62 |
| Pliny (Latin) | 1.98 | 1.30–4.42 |
| Dante (Italian) | 1.42 | 0.95–2.39 |
| *Tirant* (Catalan) | 1.37 | 0.96–3.42 |

**Meaning.** Each Voynich page has its own spelling profile, beyond its section, language and hand. It is about as strong as the page-to-page variation that changing subject produces in Pliny, and stronger than in Dante or *Tirant*. Together with §73–74, this accounts for the page clustering of word forms. It is the size a topical text has, so it does not single out the Voynich. None of the generators tried here produces it: rule model, stem selection, crossover, glyph edits, or copy-with-variation from the page. A meaningless-text procedure would need a page-level bias over glyph choices, such as a per-page preference for certain prefixes and suffixes. Something of that kind could be built and would match by design. So this statistic constrains generators but does not decide between meaning and its absence.

## 76. Do same-plant herbal pages share a spelling profile? (`sameplant_profile.py`, `data/sameplant_profile.out`)

This is §51 with the page profile of §75 in place of shared words. If each page's profile comes from its subject, pages drawn with the same plant should be closer in profile. A random per-page bias would not produce that. The profile is 17 word-feature rates, z-scored within Currier language, and the distance is Euclidean. The pairs and the null are those of §51: same language, similar folio distance, 5,000 draws. Only pages with 60 or more words are used, which leaves 24 same-genus pairs.

| pairs | mean profile distance |
|---|---|
| same proposed genus (24) | 5.585 |
| matched different-genus pairs | 5.705 (sd 0.229) |

p = 0.30. **Result: negative, and weakly powered.** Adjacent folios of the same language are much closer than folios 10 or more apart (5.420 against 5.820, a difference of 0.40). With 24 pairs, only an effect of about that size, roughly 0.45, would reach p < 0.05. The same-plant pairs come out 0.12 closer, inside the null. So the page profile tracks position in the book, through drift or a shared exemplar, far more than the plant identifications do. As in §51, wrong identifications would dilute a real effect.

## 77. Two outside leads checked: the f17r marginal line, and edge-glyph coupling (`edgemi.py`, `data/edgemi.out`)

**f17r.** N. Pelling (Cipher Mysteries, 22 January 2026) reads the line at the top of f17r as Occitan, "meilhor aller lucent ben balsamina [...]". He reports that UV and multispectral images show Voynichese-like text at its end. A Voynichese word written after a plant name would be a crib. In the Beinecke color scan (`beinecke/033_17r.jpg`), enhanced by background subtraction and channel stretching, the end of the line shows only a faint group beginning with something like "g", followed by stains. No Voynichese glyph can be read from it. Using this lead needs the multispectral images. ZL does not transcribe the line; its page comment gives "mull*av alhor lucz hev vellome o ***".

**Edge-glyph coupling.** A 2026 preprint (arXiv 2608.17096) reports about 0.2 bits of mutual information between the last glyph of a word and the first glyph of the next. That is above every prose control, and published imitators fail to reproduce it. Here the excess is over within-line shuffles, or over permutations for the separator split:

| | edge MI | excess |
|---|---|---|
| real text, corpus as used throughout (ZL `.` and `,` both treated as spaces) | 0.205 | +0.188 |
| rule model of §72 (`y→qo` junction rule) | 0.146 | +0.134 |
| rule model with the junction rule off | 0.009 | −0.001 |
| ZL certain spaces (`.`) only | 0.173 | +0.163 |
| ZL uncertain spaces (`,`) only | 0.598 | +0.517 |

**Meaning.** The 0.2-bit figure has two sources:
- **Uncertain spaces.** These are 8% of junctions, but they behave like word-internal glyph pairs: `r|a`, `s|a` and `o|l` are 3–5 times over-represented, with 28–45% of their cases across a comma. The preprint makes the same point.
- **Certain spaces.** The one scribal rule already in the §72 model (`y` followed by `qo`) reproduces most of the remaining 0.163 bits.

So edge coupling is not a separate mystery. It comes from one known junction rule plus transcription spaces that are not real word breaks. A generator that includes the junction rule passes this test, and the generators that fail it lack the rule. The residual (0.03 bits) sits mostly in `r|a`, `n|ch`, `n|sh`, `l|d` and `l|k`, together with an avoidance of `y|ch` and `y|sh`. That last pattern is the other side of `y|qo`.

## 78. The f17r marginal line in the 2014 multispectral images (`crops/f17r_msi_line.png`, `crops/f17r_msi_end.png`)

The Lazarus Project images of ten pages, f17r among them, are public. They are linked from L. F. Davis, "Multispectral imaging and the Voynich Manuscript", Manuscript Road Trip, 8 September 2024, in a Google Drive folder. I downloaded the two processed f17r images (true-color MNF and ink-1 SAM rule) to `data/ext_msi/`, which is not committed.

The images make the whole line visible. The Latin-script part reads roughly as Pelling has it (§77): "maſhor aſtor lucz hev valſamina" or similar. After it come two more groups, which the color scan does not show:

1. A group of about 6–7 glyphs. It begins with a clear round "o". Next comes a tall stroke with a looped head rising well above the line, and a looped ornament sits above it. Then come minim-like strokes, a closed loop, and a c- or s-like glyph with a dot. In shape it resembles EVA `ot…` or `op…` followed by `ii`/`ee` strokes and a final `s`. That is the pattern of real words like `oteos` and `otees` (26 and 12 occurrences), but the middle glyphs are not certain enough to transcribe.
2. A three-letter group, perhaps "ard", "aud" or "ord", ending in a letter whose ascender curves back to the left. It looks like the same cursive as the Latin-script words. None of `ard`, `ord`, `aid`, `ad` occurs as a Voynich word.

**What this gives.** The first group may be Voynichese written in the same ink and line as a plant name, which supports Pelling's observation. It is still not a usable crib, for three reasons:
- its glyphs cannot be fixed with confidence;
- nothing shows it is a gloss of "balsamina" rather than a pen trial or a copied word;
- the reading "balsamina" itself is unconfirmed, and the identification lists used in §46 and §51 give no plant for f17r to check it against.

This is a job for a palaeographer working on the full-resolution multiband files, not for statistics.

## 79. The faint full-page text on f116v in the multispectral images is offset from f116r (`crops/f116v_msi_offset_mirrored.png`)

The f116v "faded text" processing in the Lazarus set (`Voynich_116v_…_faded_text_…_as_L_RGB.jpg`) shows faint lines of script across the whole page below the known marginalia. Unmirrored, the glyph shapes look reversed. Mirrored, they read as ordinary Voynichese in the style of f116r: repeated `okeey`- and `qok`-type words and gallows. The lowest clear line reads roughly "…ol cheey qor ar… ol…". That matches f116r line 49, `sysor,shey.qokey.okeolan.chey.qol.or.cheey.qor.arom.ol.lkan`. The text is therefore ink offset from the facing page, f116r, and not lost writing on f116v, so it adds nothing to the transcription.

The other processed images in the set (f8r, f26r, f47r, f70v1, f71r, f93r) were downloaded to `data/ext_msi/`. The f102v1 download returned an HTML page instead of an image. I looked at those six only at overview resolution, about 900 pixels high. They show no marginal writing beyond what the color scans show. f47r shows a second set of leaf outlines overlapping the plant, either offset or underdrawing, but no text. A follow-up looked at the top margins of f26r and f47r at full resolution. They show only stains and offset shapes, plus the folio numbers. f8r and f93r were checked at overview resolution only, and showed no marginal writing beyond the folio numbers. f70v1 and f71r carry the known Latin-script month names. I did not search them further. Of the imaged pages, f1r (Davis 2024: Roman alphabets beside Voynich glyphs, an owner's attempt at decipherment) and f17r (§78) are the ones with marginal writing of interest.

## 80. Do the results depend on the EVA alphabet or on uncertain spaces? First part (`alphabet.py`, `parse_ivtff.py` with `JOIN=1`, `data/corpus_GC.tsv`, `data/corpus_ZLjoin.tsv`, `data/bpe_units_GC.out`, `data/bpe_units_ZLjoin.out`, `runs8/`)

**Corpora.** `data/corpus_GC.tsv` comes from Glen Claston's v101 transliteration (voynich.nu `GC2a-n.txt`, kept in `data/ext_gc/`, not committed). v101 writes one character per glyph and counts several EVA stroke groups as single signs: 68 symbols, of which the top 25 cover 97.9%. `data/corpus_ZLjoin.tsv` is ZL with uncertain spaces (`,`) joined instead of treated as word breaks, which gives 32,593 paragraph words instead of 35,051. Scripts choose a corpus with `CORPUS=…`; `ALPH=chars` treats each character as a glyph.

**Unit-entropy profile (§58).**
- v101 raw, 70 units: h1 4.04, h2 2.56, 3.89 units per word.
- v101 at 80 units: h2 3.11, 2.89 per word. At 100 units: h2 3.53, 2.38 per word.
- Latin letters, 24 units: h2 3.41, 6.02 per word.
- ZL with uncertain spaces joined is almost unchanged from §58: h2 3.39 at 60 units, 2.57 per word.

So under v101 too, glyphs are far more predictable than letters. Latin-letter predictability comes only with about 2.4–2.9 units per word, the syllabary-sized profile of §58. That conclusion does not depend on EVA's stroke-level splitting.

**Substitution decipherment (§9 Latin, §16 Italian) on v101,** 25,000 annealing steps, seed 1. The 25 commonest v101 glyphs are kept as units and the rest folded into one unit. Figures are decoded words of 4+ letters found in the dictionary.

| | Latin | Italian |
|---|---|---|
| positive control (§9, §16) | 93.7% | 100% |
| Voynich, v101 | 12.2% | 29.6% |
| Markov text built from v101 (negative control) | 14.9% | 6.0% |
| Voynich, EVA (§9, §16) | 15.0% | 20.5% |

The Latin result is at the level of meaningless text. The Italian figure is higher than its v101 Markov control and than EVA. But it is far from the control's 100%, and the output is not Italian ("i en ra arti sesa ret n er se rsea ertii ere…"). Short Italian words are common, so the 4+ letter rate rises with junk like `erti`, `seti` and `reti`. The verdict is unchanged: no substitution into Latin or Italian is found. One run each; more seeds would firm up the Italian comparison.

**Not yet done:** the word-level tests (Naibbe held-out, word→letter, codebook, cross-word syllabary) on the joined-space corpus, the syllabary test on v101, and the page transcribed by eye and compared with ZL.
