# DS-2: Semantic Reference Audit

Date: 2026-05-01
Scope: 16 unique `\citep` keys cited in `supplementary.tex` and `supplementary/S_*.tex`

## Summary

| Severity | Count |
|:---------|:------|
| BLOCKER | 0 |
| MAJOR | 3 |
| MINOR | 5 |
| OK | 8 |

---

## BLOCKER (0)

None. All 16 DOIs/URLs resolved successfully (53 doi_redirected + 14 resolved from prior audit).

---

## MAJOR (3)

### M1. `zhang2025opect` — bib key does not match first author

- **Bib entry**: author = "Xu Liu" (first author)
- **Key implies**: Zhang is the first author → INCORRECT
- **Context**: Organic OPECT parameter table in supplementary.tex. Cited for conductance range, cycle-to-cycle noise, D2D mismatch extraction.
- **Risk**: Reviewer searches for "Zhang 2025 OPECT" and cannot find it. The paper exists (Nature Communications, DOI 10.1038/s41467-025-66891-6) but under first author Liu.
- **Recommendation**: Rename key to `liu2025opect` or `liu2026opect`. Update all `\citep{zhang2025opect}` → `\citep{liu2025opect}`.
- **Patch applied**: Recommend only (not modifying bib without approval).

### M2. `kim2025hemlet` — bib key does not match first author

- **Bib entry**: author = "Wang, Cong" (first author)
- **Key implies**: Kim is the first author → INCORRECT
- **Context**: Cited in supplementary.tex layer-mapping table for hybrid CIM ViT softmax mapping.
- **Risk**: Same confusion — reviewer searches by key/name and misses the reference.
- **Recommendation**: Rename key to `wang2025hemlet`.
- **Patch applied**: Recommend only.

### M3. `lin2024hardsea` — bib key does not match first author

- **Bib entry**: author = "Shiwei Liu" (first author)
- **Key implies**: Lin is the first author → INCORRECT
- **Context**: Cited in supplementary.tex layer-mapping table for depthwise conv, QK^T, softmax digital mapping.
- **Risk**: Same as above.
- **Recommendation**: Rename key to `liu2024hardsea`.
- **Patch applied**: Recommend only.

---

## MINOR (5)

### m1. `vincze2025dualplasticity` — year mismatch

- Bib key year: 2025
- Bib entry `year`: 2026
- Note: "Published online 2025-12-03"
- Verdict: Key reflects online publication year, bib entry uses print year. Acceptable but inconsistent. Recommend aligning to 2025 (online) or 2026 (print) consistently.
- Risk: LOW. Neither year is wrong, only inconsistent.
- Action: Recommend only.

### m2. `wu2023bwq` — year mismatch

- Bib key year: 2023
- Bib entry `year`: 2024
- Verdict: Likely preprint year (2023) vs publication year (2024). Common pattern. Minor.
- Risk: LOW.
- Action: No action needed.

### m3. `peng2020dnnneurosim` — year mismatch

- Bib key year: 2020
- Bib entry `year`: 2021
- Verdict: Same as m2. Preprint vs publication.
- Risk: LOW.
- Action: No action needed.

### m4. `perez2021tighter` — special-character author parsing

- Bib entry: author = "Mar{\'i}a P{\'e}rez-Ortiz..."
- Key prefix: "perez" (acceptable abbreviation of "Pérez-Ortiz")
- Verdict: Abbreviated key is reasonable. The special characters in the bib entry are correct LaTeX.
- Risk: LOW.
- Action: No action needed.

### m5. `crosssim2024` — institutional author

- Author: "Sandia National Laboratories"
- Key: "crosssim" (tool name, not author)
- Verdict: OK for tool/repository references.
- Risk: LOW.
- Action: No action needed.

---

## Citation Context Assessment

All 16 references were checked for citation-context overclaim. None found.

| Reference | Context | Verdict |
|:----------|:--------|:--------|
| `rasch2021aihwkit` | AIHWKit as simulation toolkit; fresh eval numbers | ✅ Appropriate |
| `peng2020dnnneurosim` | Inorganic simulator comparison | ✅ Appropriate |
| `crosssim2024` | Inorganic simulator comparison | ✅ Appropriate |
| `zhang2025opect` | Organic device parameter extraction | ✅ Appropriate |
| `vincze2025dualplasticity` | Retention parameter extraction | ✅ Appropriate |
| `kim2025hemlet` | CIM ViT architecture mapping | ✅ Appropriate |
| `lin2024hardsea` | Analog/digital layer mapping | ✅ Appropriate |
| `wu2023bwq` | Depthwise conv crossbar utilization | ✅ Appropriate |
| `foret2021sharpness` | SAM comparison in theory section | ✅ Appropriate |
| `andriushchenko2022understanding` | SAM successors | ✅ Appropriate |
| `keskar2017large` | Large-batch / sharp minima | ✅ Appropriate |
| `mcallester1999pac` | PAC-Bayes framework | ✅ Appropriate |
| `mcallester1999some` | McAllester bound equation | ✅ Appropriate |
| `dziugaite2017computing` | PAC-Bayes nonvacuous bounds | ✅ Appropriate |
| `perez2021tighter` | PAC-Bayes numerical vacuity | ✅ Appropriate |
| `tobin2017domain` | Domain randomization analogy | ✅ Appropriate |

---

## Files Checked

- `paper/latex_gpt/refs_gpt.bib` (730 lines, 43 used keys)
- `paper/latex_gpt/supplementary.tex` (15 `\citep` occurrences)
- `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` (PAC-Bayes + SAM citations)
- `paper/latex_gpt/source_data/manifest_bib_key_audit_20260501.json`
- `paper/latex_gpt/source_data/manifest_bib_doi_resolution_20260501.json`

Main `paper/latex_gpt/main.tex` has 0 citation commands — the paper body likely has no reference section yet or uses a different citation mechanism.

---

## Overall Verdict

**No BLOCKER issues.** The bibliography is semantically sound. The 3 MAJOR items are key-naming conventions (first-author surname mismatch) that should be fixed before public release to avoid reviewer confusion. The 5 MINOR items are cosmetic year inconsistencies. All citation contexts are appropriate and do not overclaim.
