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
- **Neighbourhood density.** Among word types seen at least twice, a Voynich word has on average **8.9** other words at edit distance 1. Latin: 1.3. Italian: 3.3. German: 3.5. The Voynich lexicon is a dense cloud of near-identical strings (`chedy/shedy/chey/shey/qokedy/qokeedy/okedy...`).
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
| H1 Natural language, simple substitution | **dead** | h2 2.1 vs ≥3.1; positional glyph rules; neighbourhood density |
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
- **No agreement between neighbours.** In Latin, the ending of a word predicts the ending of the next (adjective–noun agreement): excess MI 0.40 bits. In Voynichese: 0.04 bits. There is no inflectional agreement.
- **But the word boundary is not neutral.** A word ending in `y` is followed by a `q`-word 1.8× more often than chance and by an `a`-word 6× *less* often; `r|a` 3×; `o|r` 6×; `s|a` 5×. Whatever produces the text "sees across" the space.
- **Prefix and suffix are independent.** Decomposing 29.5k tokens into prefix (`qo/o/q/y/s/d/ch/sh`) + core + suffix (`aiin/ain/dy/edy/ey/y/ol/al/or/ar/…`): MI(prefix, suffix) = 0.08 bits (shuffled baseline 0.003) versus Latin 1.17. The core does constrain the suffix (excess MI ≈ 0.96 bits, Latin ≈ 1.4). Prefix and suffix are chosen essentially independently of each other, which is how a *combinatorial code* behaves and not how morphology behaves.
- Zipf's law of abbreviation (frequent words are short) holds: r = −0.32 (Latin −0.29).
- **Labels reused across sections:** `okol`, `otedy`, `otol`, `okain`, `otchdy`, `okaiin`, `otaly`, `okary` … each on 4–6 different folios spanning zodiac, bio, pharma, cosmo. Almost every multi-folio label has the shape `o + gallows(k/t) + ending`. Labels are a restricted sub-vocabulary.

## 9. Controlled decipherment experiment (`decipher.py`, `data/decipher.out`)

Question: if Voynich glyph-units (26 units: `ch sh cth ckh cph cfh iin in ee` plus single glyphs) map onto Latin letters, with up to 4 units allowed to be nulls and many-to-one allowed, can a search find the mapping? Objective = Latin character 4-gram log-likelihood (trained on Pliny, Roman numerals removed), optimised by simulated annealing (25k steps). Judge by % of decoded words found in a Latin dictionary.

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

| transform of Latin | types | hapax | word len | h2 | edit-1 neighbours |
|---|---|---|---|---|---|
| plain | 13,684 | 0.71 | 6.07 ± 2.71 | 3.40 | 0.9 |
| vowels removed (except initial) | 9,567 | 0.62 | 3.60 ± 1.63 | 3.30 | 8.5 |
| truncated to 5 letters | 7,502 | 0.49 | 4.37 ± 1.09 | 3.47 | 2.8 |
| first 2 + last 2 letters | 5,355 | 0.37 | 3.67 ± 0.71 | 3.28 | 13.9 |
| consonant skeleton + final vowel | 10,556 | 0.63 | 3.75 ± 1.71 | 3.27 | 8.0 |
| syllables treated as words | 2,157 | 0.40 | 2.54 ± 0.82 | 2.98 | 13.6 |
| verbose 2-glyph cipher, 6-symbol alphabet | 13,684 | 0.71 | 12.1 ± 5.4 | 2.48 | 0.1 |
| **Voynich** | 7,829 | 0.69 | 4.97 ± 1.83 | **2.14** | 8.9 |

Abbreviation can reproduce the short, regular words and the dense neighbourhoods, but *never* the low glyph entropy: every abbreviated Latin stays at h2 ≥ 3.27. The only transform that lowers h2 is a verbose cipher, which blows up word length. No single transform reproduces the whole profile. Whatever Voynichese is, it has *both* a small effective alphabet with rigid ordering *and* a vocabulary with Latin-like richness.

## 12. Do the "meaningless text" generators reproduce everything? (`generators.py`)

| | types | hapax | word len | h2 | nbrs | same-line vs random dist | adjacent repeats | word-order MI |
|---|---|---|---|---|---|---|---|---|
| Voynich (paragraph text) | 6,983 | 0.68 | 4.97±1.80 | 2.11 | 6.8 | 2.52 vs 3.16 | 0.82% | 0.18 |
| table-and-grille (independent slots, my implementation) | 13,290 | 0.69 | 5.53±1.96 | 2.48 | 8.9 | 3.42 vs 3.53 | 0.05% | 0.00 |
| self-citation (copy-and-mutate, my implementation) | 11,072 | 0.68 | 2.99±1.34 | 3.61 | 24.0 | 1.65 vs 2.43 | 0.72% | 0.02 |

A naive grille gets the entropy nearly right but produces no line-locality, no repeats, and no word-order dependence. A naive self-citation gets the line-locality and repeats but wrecks the glyph statistics. The real text has all of these at once. That doesn't rescue "it's a language", but it does mean the popular "it's a Rugg grille / it's a Timm copy-machine" explanations are, in their simple forms, *also* insufficient. Anyone claiming a generator explains it should have to pass this whole table. (A tuned generator that mutates only within the slot grammar and copies from nearby lines might; that is a future experiment.)

## 13. What is actually readable on the pages

- The zodiac wheels (PDF pages ~124–131; f70v2 Pisces, f71r Aries, …) carry month names in a *later* hand in Latin script (`mars`, `abril`, `may`, `yony`, `jollet`, `augst`, `septembre`, `octembre`, `novembre`, `decembre`), in a Franco-Occitan spelling. This is literature knowledge; in this PDF the foldouts are shrunk to ~770 px and the names are not legible. They tell us an early owner labelled the signs, and nothing about the Voynich script.
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

Mutual information between class and suffix is 0.75 bits of the 2.25 bits of class entropy; with prefix 0.48 bits. So a word's *behaviour in context* is largely readable off its ending. In an inflected language that is partly true too (case endings signal role), so this is consistent with both a language and a code, but it says the endings are functional, not decorative.

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

Everything is now in the right neighbourhood except the excess adjacent-word mutual information. The real text has a specific *sequential* preference that copying cannot produce.

## 18. What the sequential preference is (`data/pmi.out`)

The most over-represented adjacent pairs fall into two groups:
1. **Split words.** `o l` (PMI 5.0), `s aiin` (4.0), `r aiin`, `or aiin`, `ar al`, `s ar`. These are almost certainly single words (`ol`, `saiin`, `raiin`, `oraiin`, `aral`, `sar`) that the scribe or the transcriber broke with a space. `saiin` is itself the third most common line-initial word.
2. **`-edy` → `qo-`.** `shedy qokedy`, `shey qokain`, `chedy qokain`, `chedy qokeey`, `shedy qokaiin`, `qol chedy`, `ol shedy`. A `ch/sh…y` word is followed by a `qo…` word far more than chance, and `qo…` words are almost never labels (§6). The chain `ol → chedy/shedy → qokedy/qokain` looks like a fixed phrase skeleton in language B. It is the best candidate I have for a "grammatical" pattern, and it needs to be explained by any theory. It's also compatible with `qo` being a prefix that attaches to what follows a `-y` word (a linking particle, or a space that isn't a real boundary).

Removing identical-word pairs does not change the MI (5.55 → 5.59), so repeats aren't the source.

## 19. Where things stand, and what to do next

**What I can say with evidence in hand:**
1. The text is not a natural language under any substitution (simple, homophonic, or into Latin/Italian specifically). §4, §9, §16.
2. It is not an abbreviation of Latin, and not a simple verbose cipher of a language with real word spaces. §10, §11.
3. Its words are built from a rigid slot system (prefix · core · suffix) in which prefix and suffix are chosen independently, endings determine a word's context behaviour, and glyph shapes change with line position. §5, §8, §14.
4. Word order within a line carries very little information: the sequence of ending classes is indistinguishable from a within-line shuffle. §15. Neighbouring words do not agree. §8.
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

| EVA | what the glyph looks like | behaviour |
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
| vertical neighbours more similar than horizontal | min edit distance to word above/below 3.18 vs random 3.66 | Timm & Schinner |

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

**Why I think this is new.** Zandbergen's label page and his language-classification page treat the zodiac labels as one group ("Ce-" dialect) and give one hapax figure for all 299; the recent voynich.ninja thread on zodiac labels noticed only that `o`-initial labels decline and that Cancer and Sagittarius are outliers; the 2026 arXiv papers and the Voynichdecomp repository do not analyse labels per wheel; nothing I found mentions the `a`/`e` composition of labels or contrasts labels with the ring text of the same wheel. Some earlier readers must have seen `otal…` in Pisces and `okeedy…` in Sagittarius, but I find no statement of the switch, its location, its strength, or the fact that the co-located text does not share it.

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

- **Exact matches:** no section favours either half. Every difference is under 0.10, and all permutation p-values are 0.11 or higher. Herbal-A, herbal-B, bio, stars, pharma and astro text all look the same to both halves. So do the bio, pharma and astro label sets.
- **Near matches:** allowing one deleted glyph, late labels match text more often in every section, by a similar margin: herbal-A 0.74 vs 0.51, stars 0.87 vs 0.67, bio 0.65 vs 0.50. The uplift is uniform, not tied to one section.
- **Reading:** the `e`-labels are simply closer to ordinary running-text word shapes everywhere. The `a`-labels are a more distinctive "labelese" style. There is no sign that the two halves were copied from two sections of the book. Reading (3) of §24 is not supported. Readings (1), a category marker, and (2), a changed procedure, remain.
- **Dark and light pairs:** Aries dark +0.49 vs light +0.24, Taurus light +0.91 vs dark +0.74. The darker or lighter drawing does not predict the vowel, so the split is not a day/night or colour code within those signs.

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

**Caveat.** I assumed labels run in the same order as the drawings in each row. That is how the ZL numbering reads, but I did not check each position against the scans. A wrong position would pair a plant with its neighbour's label.

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
