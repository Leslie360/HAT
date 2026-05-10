# Final Proofread Report — Manuscript LaTeX Sections
**Date:** 2026-04-19
**Scope:** `compute_vit/paper/latex_gpt/sections/*.tex`
**Tools:** Manual scan (no `aspell`/`hunspell` installed)

---

## Summary

The manuscript is in strong shape. The dominant issues are **style/consistency** (hyphenation of *nonlinearity/non-linearity*, *frontend/front-end/front end*, section-reference symbols) and a few **minor grammar** gaps (missing commas, article agreement). One **critical** maintenance issue is noted: a hardcoded section number (`Section 5.4`) that should be a `
ef`.

**High-priority recommendations:**
1. Standardize `nonlinearity` (no hyphen) everywhere.
2. Standardize `front end` (noun) vs `front-end` (adjective).
3. Replace `§` and hardcoded `Section 5.4` with `Section~\ref{...}`.
4. Define QKV/Q/K/V on first use.
5. Fix missing comma in conclusion line 7.

---

## Issues by File

### `00_abstract.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 5 | `$86.37 \pm 1.54\%` (spaced) vs `88.53$\pm$0.08\%` (unspaced) | Choose one spacing convention around `\pm` throughout the manuscript (recommend thin space or no space consistently). | style |
| 5 | `severe nonlinear write (NL=2.0)` | NL is clear in context, but if strict acronym policy is desired, spell out on first use, e.g., `nonlinearity level (NL=2.0)`. | minor |

---

### `01_introduction.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 7 | `No clear framework yet connects reported organic-device characteristics` | `No clear framework yet exists that connects reported organic-device characteristics` (or `Yet no clear framework connects...`). | minor |
| 13 | `hybrid analog--digital deployment` (en-dash) | Standardize compound: methodology uses `analog/digital` (slash). Pick one form (`analog--digital` or `analog/digital`) globally. | style |
| 15 | `inverse-gamma frontend compensation` | `inverse-gamma front-end compensation` (adjective form takes hyphen). | style |
| 17 | `physically-motivated inverse-gamma frontend compensation` | `physically motivated inverse-gamma front-end compensation` (adverb + participle: remove hyphen; also `frontend` → `front-end`). | style |

---

### `02_related_work.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 7 | `Section 5.4 shows` | `Section~\ref{subsec:hardware-transferability} shows` (hardcoded number breaks if sections shift). | **critical** |
| 8 | `paper-locked baseline` | Clarify wording (e.g., `publication-locked baseline` or `literature-fixed baseline`); current phrasing is jargon-heavy. | minor |
| 22 | `linear projections (QKV, output, feed-forward)` | `linear projections (query-key-value, or QKV, output, feed-forward)` — QKV is undefined on first use. | minor |

---

### `03_methodology.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 8 | `The system-level split and the operator-level rationale are summarized in the Supplementary Information following established practice` | `...Supplementary Information, following established practice...` (add comma to disambiguate modifier). | minor |
| 8 | `Q/K/V and output projections` | Define on first use: `query/key/value (Q/K/V) and output projections` (or unify with `QKV` used later). | minor |
| 26 | `\S\ref{subsec:retention-drift}` | `Section~\ref{subsec:retention-drift}` ( inconsistent with `Section~\ref{...}` used elsewhere). | style |
| 38 | `Monte Carlo--estimated` | `Monte Carlo-estimated` (hyphen, not en-dash, for compound modifier) or reword as `estimated by Monte Carlo`. | style |
| 44 | `re-samples per forward pass` | `resamples per forward pass` (elsewhere uses `resamples` without hyphen). | minor |
| 46 | `physical frontend model` | `physical front-end model` (adjective). | style |
| 64 | `frontend calibration` | `front-end calibration` (adjective). | style |
| 64 | `frontend-theory derivation` | `front-end theory derivation` (remove awkward compound; `front-end` modifies `theory`). | style |

---

### `04_experimental_setup.tex`

No issues found beyond those noted in global consistency checks.

---

### `05_results.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 13 | `(§\ref{subsec:nl-hat-stress})` | `(Section~\ref{subsec:nl-hat-stress})` (standardize section-reference style). | style |
| 29 | `noise-data interaction` | `noise--data interaction` (en-dash for coordinate compound, matching `analog--digital` style). | style |
| 36 | `0~s $\rightarrow$ 82.66\%` | `0~s to 82.66\%` (avoid math arrow in prose; or use en-dash `0~s--82.66\%`). | style |
| 51 | `Above 6-bit, degradation is dominated by D2D` | `Above 6 bits, degradation...` or `In the above-6-bit regime, degradation...` (when used as a noun, plural `bits`). | minor |
| 51 | `($\geq$6-bit, $\sigma_{\mathrm{D2D}} \leq 15\%$)` | `($\geq$6~bits, $\sigma_{\mathrm{D2D}} \leq 15\%$)` (same noun rule; add thinspace after `\geq` for readability). | minor |
| 56 | `($\sigma_{\mathrm{C2C}}=5\%$, $NL=1.0$, 10 MC runs per point)` | `($\sigma_{\mathrm{C2C}}=5\%$, $NL=1.0$, 10~MC runs per point)` (add thinspace between number and unit/MC). | style |
| 60 | `\subsection{Non-Linear Writing and Hardware-Aware Training}` | `\subsection{Nonlinear Writing and Hardware-Aware Training}` (standardize to `nonlinear` without hyphen). | style |
| 63 | `overwhelming standard HAT` | `substantially outperforming standard HAT` (or `dominating standard HAT`); `overwhelming` as a participial adjective is slightly informal. | style |
| 82 | `labeled as n/a` | `labeled as N/A` (standard capitalization). | minor |
| (global) | `\pm` spacing varies: `97.37$\pm$0.05\%` vs `$86.37 \pm 1.54\%` | Standardize: either no spaces (`$86.37\pm1.54\%$`) or thin spaces (`$86.37\,\pm\,1.54\%$`) everywhere. | style |

---

### `06_discussion.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 21 | `the Transformer architecture` | `the transformer architecture` (generic noun, lowercase mid-sentence). | minor |
| 23 | `moderate non-linearities` | `moderate nonlinearities` (standardize to unhyphenated form). | style |
| 23 | `Transformer inference` | `transformer inference` (generic noun). | minor |
| 25 | `frontend distortion` | `front-end distortion` (adjective). | style |
| 26 | `frontend-theory note` | `front-end theory note` (adjective + noun). | style |
| 38 | `10–50\%` | Verify LaTeX source uses `--` (en-dash) consistently with other ranges (e.g., `71--77\%`). If a literal Unicode en-dash is used, replace with `--` for source consistency. | style |
| 43 | `a hook-based check shows moderate ADC calibration errors change V4 accuracy` | `a hook-based check shows that moderate ADC calibration errors change V4 accuracy` (add `that` for clarity). | minor |
| 43 | `not a materials bound` | `not a material bound` (singular attributive noun) or `not a materials-science bound`. | minor |

---

### `07_conclusion.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 7 | `while within the operational envelope device-to-device variability becomes` | `while within the operational envelope, device-to-device variability becomes` (add comma after introductory phrase). | minor |
| 7 | `severe write non-linearity setting` | `severe write nonlinearity setting` (standardize). | style |

---

### `08_appendix.tex`

| Line | Original | Suggested Fix | Priority |
|------|----------|---------------|----------|
| 43 | `Supp.Fig.8` | `Supplementary Fig.~8` (match main-text style; or define abbreviated form if journal permits). | style |
| 63 | `moderate write non-linearity` | `moderate write nonlinearity` (standardize). | style |
| 142 | `non-linearity coefficients` | `nonlinearity coefficients` (standardize). | style |

---

## Global Consistency Recommendations

| Category | Current State | Recommended Fix |
|----------|---------------|-----------------|
| **nonlinearity / non-linearity** | 5× `nonlinearity`, 4× `non-linearity` | Use `nonlinearity` everywhere (no hyphen). |
| **frontend / front-end / front end** | Noun: `front end` (correct); Adjective: mixed `frontend`, `front-end` | Adjective always `front-end`; noun always `front end`. |
| **Section references** | `Section~\ref{...}`, `\S\ref{...}`, `§\ref{...}`, hardcoded `Section 5.4` | Always use `Section~\ref{...}` (or `\S~\ref{...}` if journal requires §, but pick one). |
| **Analog vs analogue** | All `analog` (US) | ✅ Consistent; keep as-is. |
| **bit vs bits (noun)** | `Above 6-bit` (results), `Below 6 bits` (abstract/intro) | Noun form: `bits`; adjective form: `bit` (e.g., `6-bit ADC`). |
| **En-dash ranges** | Mostly `--` in LaTeX source | Ensure all ranges (D2D--ADC, 71--77%, 5-to-6-bit) use `--` and not literal Unicode en-dashes. |

---

## Acronym First-Use Audit

| Acronym | First-Use Location | Status |
|---------|-------------------|--------|
| CIM | `01_introduction.tex` L5: `Compute-in-memory (CIM)` | ✅ Defined |
| SRAM | `01_introduction.tex` L5: `static random-access memory (SRAM)` | ✅ Defined |
| HAT | `00_abstract.tex` L5: `hardware-aware training (HAT)` | ✅ Defined |
| D2D | `00_abstract.tex` L5: `device-to-device (D2D)` | ✅ Defined |
| ADC | `00_abstract.tex` L5: `analog-to-digital converter (ADC)` | ✅ Defined |
| OPECT | `00_abstract.tex` L5: `organic photoelectrochemical transistor (OPECT)` | ✅ Defined |
| ViT | `01_introduction.tex` L7: `Vision Transformer (ViT)` | ✅ Defined |
| CNN | `01_introduction.tex` L7: `convolutional neural network (CNN)` | ✅ Defined |
| MLP | `01_introduction.tex` L17: `multi-layer perceptron (MLP)` | ✅ Defined |
| IR | `01_introduction.tex` L19: `current--resistance, or IR, drop` | ✅ Defined |
| C2C | `03_methodology.tex` L15: `cycle-to-cycle (C2C)` | ✅ Defined |
| STE | `03_methodology.tex` L15: `straight-through estimator (STE)` | ✅ Defined |
| DNTT | `03_methodology.tex` L46: `dinaphtho-thieno-thiophene (DNTT)` | ✅ Defined |
| LTP / LTD | `03_methodology.tex` L46: `long-term potentiation` / `long-term depression` | ✅ Defined |
| MC | `05_results.tex` L18: `Monte Carlo (MC)` | ✅ Defined |
| PCM | `05_results.tex` L82: `phase-change memory (PCM)` | ✅ Defined |
| RRAM | `05_results.tex` L82: `resistive random-access memory (RRAM)` | ✅ Defined |
| QKV / Q/K/V | `02_related_work.tex` L22: `linear projections (QKV...)` / `03_methodology.tex` L8: `Q/K/V` | ⚠️ **Undefined on first use**. Recommend expanding to `query-key-value (QKV)` at first occurrence. |
| ReLU | `06_discussion.tex` L26: `ReLU saturation` | ⚠️ Undefined, but ubiquitous; define if strict (`rectified linear unit (ReLU)`). |
| GELU | `03_methodology.tex` L8: `GELU activation` | ⚠️ Undefined, but common; define if strict. |
| ReRAM | `06_discussion.tex` L43: `ReRAM literature` | ⚠️ Undefined; recommend `resistive RAM (ReRAM)` or `resistive random-access memory (ReRAM)` on first use. |
| PIM | `02_related_work.tex` L24: `ViT-on-PIM` | ⚠️ Undefined; recommend `processing-in-memory (PIM)` on first use. |
| JSON | `03_methodology.tex` L79: `JSON parameter bundle` | ⚠️ Common; define if strict (`JavaScript Object Notation (JSON)`). |
| GPU | `02_related_work.tex` L20: `GPU-accelerated` | ⚠️ Common; define if strict (`graphics processing unit (GPU)`). |

---

## Spelling Notes

No obvious misspellings were detected during manual scanning. Words verified:
- *multilevel* (preferred over *multi-level* in this domain)
- *memristive, optoelectronic, photoresponse, provenance, heterogeneous, perceptron*
- *non-idealities* (correctly hyphenated)
- *front-end / frontend* (see consistency note above)

---

*End of report.*
