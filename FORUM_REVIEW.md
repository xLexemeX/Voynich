# voynich.ninja review (2026-09-16)

What I read on the forum, what it adds, and how it bears on the findings in `NOTES.md`. Threads were read through the forum's public archive pages. Some links inside threads are hidden from logged-out readers, so a few details, like the herbal-to-pharmacy picture match list, were not visible.

## Threads read

| thread | what it establishes | bearing on my work |
|---|---|---|
| Zodiac labels (4829) | `o`-initial labels fall from 29/30 in Aries to 15/30 in Sagittarius. Cancer and Sagittarius have more `y`-initial labels. Duplicates always start with `o`. | Related observation, different glyph: an initial-glyph count. No one reports the `a`/`e` switch, its location, or a comparison with ring text. |
| Currier A/B split is not what we thought it was! (5710) | A per-folio "boolean switch": the vowel after `ch`/`sh` is `o` on some folios and `e` on others. 195 of 197 folios classify cleanly. Word templates split into fixed-`o`, fixed-`e` and switchable. The switch is independent of the `d`/`l` ratio. | **The closest prior work.** It is the same *kind* of phenomenon, a vowel set per writing unit. It does not cover labels or the zodiac folios. See the comparison below. |
| Bifolio as a functional unit? (5131) | Lisa Fagin Davis and a collaborator report, via latent semantic analysis, that conjoint bifolia are textually closer in the bath and stars sections, but not the herbal. Another member notes 4 of 10 exceptions in the stars quire. | Supports the idea that the physical writing unit, a sheet side or bifolio, carries text statistics. Consistent with my switch landing at the f72 recto/verso. |
| Can LAAFU effects be modeled? (4869) | René Zandbergen: 85% of paragraph-first lines start with `p t k f`, and 85% of other lines start with `d s y o q`. `m` and `g` favour line ends. Jorge Stolfi proposes that justification explains line effects. | My line-start and `-m` results are known. No one there measured dependencies *across* a line break, but that was measured elsewhere (Voynichdecomp). |
| A brief summary of Voynichese spelling and grammar (4779) | David Jackson's rule list: `q` before `o`, `i` before `i`/`n`, `y`→`qo` junction, `m` at line ends but not paragraph ends, substitution classes `ch/sh`, `t/k`, `l/r`, `y/o`, `o/a`, `l/m`. | Confirms that `-m` avoids paragraph ends, which my §23 measured, is already known. |
| Paragraph layout (5970) | Paragraphs start on a fresh line with an enlarged gallows. The previous paragraph's last line is left short. Stolfi: `p`/`f` "puffs" fill the whole first line but never spill into the second. | Known. |
| Textual relationship between matching Herbal and Pharma illustrations (6044) | Picture matches exist, and Fagin Davis has a list in preparation. A member's computer analysis found no significant textual overlap. | Agrees with my negative label-to-paragraph test in §28. |
| The Naibbe cipher (4848, page 4) | The cipher's author parsed all of Language B as Naibbe ciphertext without tuning. The output was "Latinish gibberish". | A word-level decipherment was attempted without a search for the key. My runs add a key search with a positive control. |
| Binary ritual calendar (4698), label catalogue (3862), zodiac rare features (2210) | Speculative or iconographic. No label statistics by sign. | No overlap. |

## Is the zodiac label vowel switch new? Checked against the closest thread

The forum's switch is defined on running text, per folio, by the vowel after `ch`/`sh`. If a folio has one switch state, its labels and its text should agree. On the zodiac wheels they do not (`data/switch_compare.out`):

| measure | early wheels f70v–f72r | late wheels f72v–f73v |
|---|---|---|
| labels: share of `o` after `ch`/`sh` | 0.53 (n=15) | 0.10 (n=21) |
| labels: share of `a` after a gallows | 0.78 (n=93) | 0.34 (n=88) |
| ring text: share of `o` after `ch`/`sh` | 0.32 (n=155) | 0.28 (n=113) |
| ring text: share of `a` after a gallows | 0.25 (n=267) | 0.22 (n=163) |

- The labels switch on both measures, most clearly on the vowel after a gallows. The `ch`/`sh` counts in labels are small.
- The ring text on the same folios does not switch on either measure. It stays `e`-dominant throughout.

**Revised novelty claim.** A per-folio vowel switch in running text is already proposed on the forum, by user Labyrinthinesecurity. What I have not found anywhere is:

1. a switch in the **zodiac labels**, carried mainly by the vowel after `k`/`t`;
2. its location at the **f72 recto/verso**;
3. its **dissociation from the running text on the same folios**, which contradicts a pure one-state-per-folio model.

I credit the forum thread as the nearest prior work and treat my result as an extension that also tests their model.

## Useful leads from the forum not yet followed

- The "Most certain plant IDs" curated thread (3617) gives external ground truth for plants. A future label or name test should use only those pages.
- The "Counts" curated thread (2455) collects agreed-on counts for checking my numbers.
- Stolfi's justification hypothesis for line effects could be tested with the layout measurements, once word-level segmentation of the scans works.
