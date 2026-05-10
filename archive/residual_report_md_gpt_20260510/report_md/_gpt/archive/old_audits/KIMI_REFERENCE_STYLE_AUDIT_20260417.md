# Reference-Format and Style Audit — 2026-04-17

**Scope:** Audit `paper/latex_gpt/refs_gpt.bib` against Nature-family expectations (clean DOIs, consistent capitalization, complete venue metadata, no duplicates, no broken placeholders).
**Method:** Read-only inspection of the live `.bib` source; no `.tex` edits performed.

---

## Executive Summary

| Issue category | Count | Severity |
|:---------------|:------|:---------|
| Missing DOI | 2 | **High** |
| Bib-key / year mismatch | 4 | **Medium** |
| Incomplete author lists (`and others`) | 2 | **Medium** |
| Non-standard venue label | 1 | **Medium** |
| Missing volume/issue/pages where available | ~6 | Low–Medium |
| Inconsistent capitalization in titles | ~3 | Low |

Overall, the bibliography is **usable for review** but has a handful of fixable inconsistencies that risk looking under-curated to a meticulous reviewer or editor.

---

## Concrete Fix List (by Bib Key)

### `joshi2020accurate` — Missing DOI
**Current:** No `doi` field.
**Fix:** Add `doi = {10.1038/s41467-020-16108-9}`.

### `tobin2017domain` — Missing DOI
**Current:** No `doi` field.
**Fix:** Add `doi = {10.1109/IROS.2017.8202133}`.

### `choi2019pact` — Year / bib-key mismatch
**Current:** Bib key says `2019`, but the work is ICML 2018 (arXiv:1805.06085). The `year` field is also listed as `2018`, which is correct, but the key is confusing.
**Fix:** Rename key to `choi2018pact` **or** add a note: `note = {ICML 2018}`.
*Impact:* If keys are frozen in the LaTeX source, renaming requires a global find/replace; otherwise, leaving the mismatch is tolerable but not ideal.

### `peng2020dnnneurosim` — Year / bib-key mismatch
**Current:** Bib key says `2020`, but the IEEE TCAD publication year is `2021` (the `year` field is correctly 2021).
**Fix:** Rename key to `peng2021dnnneurosim` or accept the legacy mismatch.

### `crosssim2026` — Year / bib-key mismatch
**Current:** Bib key says `2026`, actual publication year of the Sandia report is `2024`.
**Fix:** Rename key to `crosssim2024`.

### `zhang2026opect` — Year / bib-key mismatch
**Current:** Bib key says `2026`, actual Nature Communications publication year is `2025`.
**Fix:** Rename key to `zhang2025opect`.

### `vincze2026dualplasticity` — Year / bib-key mismatch
**Current:** Bib key says `2026`, actual Advanced Electronic Materials publication year is `2025`.
**Fix:** Rename key to `vincze2025dualplasticity`.

### `wang2025oectarray` — Incomplete author list
**Current:** `author = {Wang, Shuai and others}`.
**Fix:** Expand to full author list if available, or remove `and others` and use `et al.` style: `Wang, Shuai and ...`. In BibTeX, `and others` is technically valid but looks like a placeholder. Better to list at least the first 6–9 authors and then `and others` if the list is very long.

### `liu2025optoelectronic` — Incomplete author list
**Current:** `author = {Liu, L. and Li, Z. and Zheng, Y. and others}`.
**Fix:** Same as above—expand the author list to publication-grade completeness.

### `olizaman2023dmm` — Non-standard venue / title
**Current:** `journal = {NSF Public Access Repository}`; title is garbled in some views; this is actually an arXiv preprint (arXiv:2201.09342).
**Fix:** Convert to `@misc` or `@online`:
```bibtex
@misc{olizaman2023dmm,
  author = {Md Oli-Uz-Zaman and Sajjad A. Khan and Argha Basak and Swaroop Ghosh},
  title  = {Reliability Improvement in {RRAM}-based {DNN} for Edge Computing},
  year   = {2023},
  eprint = {2201.09342},
  archivePrefix = {arXiv},
  doi    = {10.48550/arXiv.2201.09342}
}
```

### `kim2025hemlet` — Missing URL / eprint details
**Current:** Only `eprint = {2511.15397}` and `archivePrefix = {arXiv}` are present, but no `url` or `doi`.
**Fix:** Add `url = {https://arxiv.org/abs/2511.15397}` and `doi = {10.48550/arXiv.2511.15397}` for completeness.

### `wei2020voltagedifferential` — Very long author string ending in `and others`
**Current:** Lists ~11 authors and then `and others`. Conference papers often have long author lists, but if the list exceeds ~15 names, consider truncating to the first 10 and appending `and others`.

### `fastirdrop2025` — Missing volume/issue/pages
**Current:** Only `year` and `doi` are present.
**Fix:** Add `volume`, `number`, and `pages` if known from the IEEE Xplore record. At minimum, the DOI is present, so this is lower priority.

### `iconniv2025` — Year field says 2026, but DOI may resolve to 2025/2026 Early Access
**Current:** `year = {2026}`. The DOI `10.1145/3777381` may correspond to a 2025 or 2026 ACM TACO article.
**Fix:** Verify the exact publication year via the ACM portal; adjust if necessary.

### `sun2024survey` — Volume/pages present, but check page format
**Current:** `pages = {25-42}` (hyphen, not en-dash).
**Fix:** Use `--` in BibTeX to produce an en-dash: `pages = {25--42}`.

### `gebregiorgis2023organiccim` — Good example
**Current:** Has `volume = {70}`, `number = {12}`, `pages = {6520--6525}`, `doi = {10.1109/ted.2023.3327947}`.
**Status:** ✅ This entry is publication-complete and should be used as a formatting model.

---

## Inconsistent Capitalization

Nature-style bibliographies generally expect **sentence case** for article titles, with proper nouns and acronyms protected by braces. Current `.bib` uses a mix:

- `peng2020dnnneurosim` — Title is title-case and uses `{DNN\allowbreak+\allowbreak NeuroSim}` protection correctly.
- `crosssim2026` — Title is sentence-case (`CrossSim: Sandia's simulator for analog AI accelerators`).
- `zhang2026opect` — Title is sentence-case.
- `wei2020voltagedifferential` — Title is title-case (`A Voltage-Mode Sensing Scheme with Differential-Row Weight Mapping...`).

**Recommendation:** Standardize to **sentence case** for all `@article` and `@inproceedings` titles, keeping braces around acronyms (e.g., `{CIM}`, `{ADC}`, `{RRAM}`, `{DNN}`). This is a low-priority polish item.

---

## Duplicate / Near-Duplicate Concepts

- **Organic review papers:** `xu2025emerging`, `photonics2025organicreview`, and (to a lesser extent) `guo2024organic` all serve the "organic synaptic devices" introduction. They are not duplicates, but the manuscript should ensure each is cited for a distinct point so the bibliography does not look padded.
- **ViT quantization:** `liu2021ptqvit`, `li2022qvit`, `lin2023vitptq` — all legitimate, but make sure the text distinguishes their specific claims (post-training vs. fully-quantized vs. integer-only).

---

## Broken or Likely Placeholder Venues

| Bib key | Current venue | Assessment |
|:--------|:--------------|:-----------|
| `olizaman2023dmm` | `NSF Public Access Repository` | ❌ Not a real journal; reformat as arXiv. |
| `kim2025hemlet` | `arXiv preprint` | ⚠️ Acceptable, but add URL/DOI. |
| `wang2025oectarray` | `Journal of Materials Chemistry C` | ✅ Real journal, but author list is placeholder-quality. |

---

## References Cited in Text but Weakly Tied to Claims

| Bib key | In-text location | Strength assessment |
|:--------|:-----------------|:--------------------|
| `zeng2023organicmemristor` | Introduction / Related Work | Cited for "long retention tails"; the paper is about organic memristors broadly. Acceptable but generic. |
| `jung2024organicfilaments` | Introduction / Related Work | Cited for "multilevel memory" and "synaptic behavior". Acceptable. |
| `bettayeb2024memristorattention` | Introduction / Related Work | Cited to justify keeping attention digital. The paper supports analog attention acceleration, which is actually the *opposite* of the manuscript's claim. **Weak / potentially contradictory.** Consider removing or rephrasing the sentence so that the citation is used to acknowledge a competing view rather than as direct support. |

---

## Recommended Priority Order for Fixes

1. **Add missing DOIs** to `joshi2020accurate` and `tobin2017domain` (highest reviewer-trust impact).
2. **Reformat `olizaman2023dmm`** from a fake journal entry to a proper arXiv/misc entry.
3. **Expand or prune** `wang2025oectarray` and `liu2025optoelectronic` author lists.
4. **Decide on bib-key / year mismatches** (`choi2019pact`, `crosssim2026`, `zhang2026opect`, `vincze2026dualplasticity`, `peng2020dnnneurosim`). If the `.tex` source is still editable, a global find/replace is worth the effort.
5. **Add `url`/`doi`** to `kim2025hemlet`.
6. **Standardize title capitalization** to sentence case (lowest priority).

---

*End of audit.*
