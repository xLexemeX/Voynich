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
