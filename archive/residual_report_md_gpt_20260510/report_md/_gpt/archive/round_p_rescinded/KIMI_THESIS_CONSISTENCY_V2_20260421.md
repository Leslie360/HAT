<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Thesis Cross-Chapter Consistency Report V2 (Post-Pivot)

**Scope:** All 8 thesis chapters in `compute_vit/paper/thesis/chapter_*.tex`
**Date:** 2026-04-21
**Checker:** Automated cross-reference, locked-number, framing, figure-label, and acronym audit.

---

## 1. Executive Summary

| Check | Status | Highest Severity |
|-------|--------|------------------|
| Locked numbers (9 anchors) | **PASS with caveat** | SHOULD-FIX (86.33 variant) |
| Negative-result framing (severe NL) | **FAIL** | CRITICAL (Ch.8 pre-pivot language) |
| Forward/backward refs (Ch.5 §6) | **FAIL** | SHOULD-FIX |
| Figure labels (duplicates / broken refs) | **FAIL** | CRITICAL (Ch.4 orphan figure) |
| Acronym order (undefined acronyms) | **FAIL** | SHOULD-FIX |

**Total issues:** 10 (2 CRITICAL, 6 SHOULD-FIX, 2 COSMETIC)

---

## 2. Check 1 — Locked Numbers

### 2.1 Anchor inventory

| Anchor | Canonical form | Occurrences | Verdict |
|--------|---------------|-------------|---------|
| 86.37 | `$86.37\pm1.54\,\%$` | Ch.1×1, Ch.3×5, Ch.4×3, Ch.5×9, Ch.6×1, Ch.7×4, Ch.8×3 | **Identical** |
| 87.95 | `$87.95\pm0.27\,\%$` | Ch.3×1, Ch.4×1, Ch.5×4, Ch.6×1, Ch.7×2, Ch.8×1 | **Identical** |
| 27.72 | `$27.72\pm0.82\,\%$` | Ch.4×2, Ch.5×2, Ch.6×1, Ch.7×2, Ch.8×1 | **Identical** |
| 32.12 | `$32.12\pm7.72\,\%$` | Ch.4×3, Ch.5×6, Ch.6×1, Ch.7×2, Ch.8×1 | **Identical** |
| 32.60 | `$32.60\pm9.18\,\%$` | Ch.4×2, Ch.5×5, Ch.6×1, Ch.7×1, Ch.8×1 | **Identical** |
| 84.57 | `$84.57\pm2.39\,\%$` | Ch.4×1, Ch.5×2, Ch.6×2, Ch.7×2, Ch.8×2 | **Identical** |
| 82.12 | `$82.12\pm3.95\,\%$` | Ch.4×1, Ch.5×2, Ch.6×2, Ch.7×2, Ch.8×2 | **Identical** |
| 88.53 | `$88.53\pm0.08\,\%$` | Ch.5×2, Ch.7×2 | **Identical** |
| 30.53 | `$30.53\pm7.07\,\%$` | Ch.5×4 | **Identical** |

All nine anchors appear in their locked forms everywhere they are cited.

### 2.2 Variant number inconsistency (SHOULD-FIX)

A **different** i.i.d. mean `$86.33\pm1.61\,\%$` appears in tables that purport to show the *canonical* Ensemble HAT baseline:

- `chapter_4_failure_modes.tex:142` — Table `tab:fresh-instance-nl`, row "Canonical Ensemble HAT"
- `chapter_5_mitigation.tex:77,141,245` — Table `tab:fresh-instance-nl-c5` and `tab:three-mitigation-ceiling`
- `chapter_6_physical_realism.tex:73,400` — Table `tab:correlated-d2d-full` (i.i.d. baseline) and summary
- `chapter_7_deployment.tex:71` — prose reference to the i.i.d. baseline
- `chapter_8_outlook.tex:53,118` — summary bullets

**Problem:** `chapter_6_physical_realism.tex:61` explicitly states that the correlated-D2D sweep uses "the canonical Tiny-ViT V4 Ensemble HAT checkpoint (the same checkpoint that yields `$86.37\pm1.54\,\%` under i.i.d. conditions)," yet the table reports `$86.33\pm1.61$`. The two means differ by 0.04 pp and the standard deviations differ by 0.07 pp. Readers will assume a transcription error.

**Fix:** Align all i.i.d. canonical Ensemble HAT references to the locked `$86.37\pm1.54\,\%$`. If `$86.33\pm1.61$` is a separate evaluation (e.g., a re-run with a different seed), add a footnote explaining the discrepancy; otherwise replace with the locked number.

---

## 3. Check 2 — Negative-Result Framing (Severe NL)

**Rule:** Every chapter that mentions severe NL must frame it as a *structural limit / generalization barrier*, not as a training artifact or optimization gap.

| Chapter | Mentions severe NL? | Framing | Verdict |
|---------|--------------------|---------|---------|
| Ch.1 | Yes (line 10) | "structural generalization barrier … rather than an optimization gap" | ✅ PASS |
| Ch.2 | No | — | N/A |
| Ch.3 | Yes (proportional-noise collapse) | Frames cross-regime collapse as distributional misalignment, not structural NL limit | ⚠️ Indirect |
| Ch.4 | Yes (extensively) | "structural destruction," "structural collapse," "structurally required" | ✅ PASS |
| Ch.5 | Yes (extensively) | "structural barrier," "structural property," "not a training artifact," "fundamental generalization barrier" | ✅ PASS |
| Ch.6 | Yes (line 385) | "surrogate-fidelity problem, not a statistics problem" — acceptable but not the required phrasing | ⚠️ Weak |
| Ch.7 | Yes (lines 11, 142–146) | Describes the `$32\,\%` ceiling and collapse zone but **never explicitly states** that the failure is structural rather than an optimization gap | ❌ SHOULD-FIX |
| Ch.8 | Yes (lines 28–48) | **"The ceiling is almost certainly an artifact of fixed-mask training"** — this is the *opposite* of the post-pivot framing and directly contradicts Ch.5 §6 | ❌ **CRITICAL** |

### CRITICAL — Ch.8 pre-pivot language

**File:** `chapter_8_outlook.tex`
**Lines:** 28–48 (Section `sec:immediate-next-steps`, subsection `subsec:joint-mlp-ensemble`)

**Issue:** The Outlook chapter presents the joint MLP-linear + Ensemble HAT experiment (CX-J1) as an *unfinished thesis-completion experiment* and claims that the `$\sim$30\%` ceiling is "almost certainly an artifact of fixed-mask training." This is pre-pivot language. Ch.5 §6 (`sec:structural-limit`) already reports the CX-J1 result (`$30.53\pm7.07\,\%` fresh-instance) and concludes that the ceiling is a **structural generalization barrier** that survives even distributional (epoch-resampled) training.

**Fix:** Rewrite the subsection to:
1. Acknowledge that CX-J1 was already executed in Ch.5 §6 and failed to break the ceiling.
2. Frame the `$\sim$30\%` limit as a *structural property of the first-order NL surrogate acting on the attention pathway*.
3. Pivot the "thesis-completion experiment" proposal to the **falsification experiments** CX-J1b/c/d (QKV-linear, output-projection-linear, attention-free architecture) proposed in Ch.5 §6, or to the ImageNet-100 scaling pilot.

**Suggested replacement for lines 33–37:**

> Chapter~\ref{chap:failure-mode-atlas} established the hardest open boundary in the current atlas. Under a global severe write nonlinearity of `$\mathrm{NL}=2.0$`, Tiny-ViT V4 collapses to `$27.72\pm0.82\,\%$` on CIFAR-10. Chapter~\ref{chap:mitigation-case-studies}, \S\ref{sec:structural-limit}, reports the decisive CX-J1 experiment that couples MLP-only linearization with Ensemble HAT resampling under `$NL=2.0$`; the result (`$91.36\,\%` source-domain, `$30.53\pm7.07\,\%` fresh-instance) falsifies the hypothesis that the `$\sim$32\,\%` ceiling is merely an optimization gap. The ceiling is therefore a **structural generalization barrier** imposed by the interaction of the first-order NL surrogate with the attention pathway, not an artifact of fixed-mask training. The remaining thesis-completion experiments are the falsification protocol CX-J1b/c/d proposed in \S\ref{sec:structural-limit} and the ImageNet-100 scaling pilot described below.

---

## 4. Check 3 — Forward / Backward References (Ch.5 §6)

**Rule:** Ch.5 new §6 (`sec:structural-limit`) must be referenced from Ch.1, Ch.6, and Ch.8.

| Source chapter | Reference found? | Context |
|----------------|-----------------|---------|
| Ch.1 | ❌ No | Ch.1 line 10 references "Chapter~5" generally but does **not** cite `sec:structural-limit` or the structural-limit framing. |
| Ch.6 | ❌ No | No reference to `sec:structural-limit` or to Ch.5's structural-limit analysis. Ch.6 discusses the MLP-only / all-linear bounds but only in the context of the failure-mode atlas (Ch.4). |
| Ch.8 | ❌ No | Ch.8 references Ch.4 for the ceiling (line 33) and never cites `sec:structural-limit` or `chap:mitigation-case-studies`. |

**Fix:** Add explicit backward/forward references in three locations:

1. **Ch.1, line 10** (`chapter_1_hat_instance_overfitting.tex`):
   > A natural hypothesis is that protecting the MLP blocks while resampling device noise would break the ceiling. Chapter~\ref{chap:mitigation-case-studies}, \S\ref{sec:structural-limit}, reports the falsification of this hypothesis …

2. **Ch.6, introduction or synthesis** (`chapter_6_physical_realism.tex`):
   Add a sentence in `sec:pr-synthesis` connecting the physical-realism extensions back to the structural limit:
   > The severe-NL fresh-instance ceiling documented in Chapter~\ref{chap:mitigation-case-studies}, \S\ref{sec:structural-limit}, remains the hardest bound: even when D2D mismatch is i.i.d. and the MLP path is perfectly linearized, the attention pathway enforces a `$\sim$30\,\%` generalization barrier under the first-order gradient-scaling surrogate.

3. **Ch.8, line 33** (`chapter_8_outlook.tex`):
   Replace the Ch.4-only reference with a dual reference to Ch.4 and Ch.5 §6, as suggested in the CRITICAL fix above.

---

## 5. Check 4 — Figure Labels

### 5.1 Duplicate labels

No duplicate `\label{fig:…}` or `\label{tab:…}` identifiers were found across the 8 chapters. ✅

### 5.2 Broken / orphaned references

| Ref | Points to | Problem | Severity |
|-----|-----------|---------|----------|
| `\ref{fig:thesis-fresh-instance}` in Ch.4 line 46 | `fig:thesis-fresh-instance` (defined in Ch.1) | Ch.4 defines its **own** figure `fig:thesis-fresh-instance-c4` (line 52) but **never references it**. The text accidentally points to Ch.1's figure instead. | **CRITICAL** |

**Fix:** In `chapter_4_failure_modes.tex` line 46, change:

```latex
Figure~\ref{fig:thesis-fresh-instance} reuses the manuscript's fresh-instance transfer visualization …
```

to:

```latex
Figure~\ref{fig:thesis-fresh-instance-c4} reuses the manuscript's fresh-instance transfer visualization …
```

### 5.3 Equation refs

All `\ref{eq:…}` citations resolve to existing `\label{eq:…}` entries. ✅

### 5.4 Table refs

All `\ref{tab:…}` citations resolve to existing `\label{tab:…}` entries. ✅

---

## 6. Check 5 — Acronym Order

### 6.1 Undefined or late-defined acronyms

| Acronym | First use | First definition | Gap | Severity |
|---------|-----------|------------------|-----|----------|
| **CIM** | Ch.3 line 184 ("CIM simulation") | Ch.4 line 8 ("compute-in-memory (CIM)") | Used 3× in Ch.3 before definition | SHOULD-FIX |
| **FP32** | Ch.5 line 94 ("digital FP32 baseline") | **Never defined** | Used in Ch.5 and Ch.7 without expansion | SHOULD-FIX |
| **PTC** | Ch.6 line 274 (`\text{PTC}`) | **Never defined** | Used in Arrhenius context without expansion | SHOULD-FIX |
| **AR(1)** | Ch.4 line 167 ("separable AR(1)-style correlation") | **Never defined** | Readers may not know "autoregressive" | COSMETIC |

**Fix suggestions:**

1. **CIM** — Add a parenthetical definition at first use in Ch.3, or move the definition earlier to Ch.1 or Ch.3 intro.
2. **FP32** — On first use in Ch.5, write "32-bit floating point (FP32)".
3. **PTC** — In Ch.6 line 274, write "positive temperature coefficient (PTC)".
4. **AR(1)** — In Ch.4 line 167, write "first-order autoregressive (AR(1))".

### 6.2 Correctly defined acronyms (representative sample)

| Acronym | Defined where? | OK? |
|---------|---------------|-----|
| HAT | Ch.1 line 6 ("hardware-aware training (HAT)") | ✅ |
| ViT | Ch.1 line 8 ("Tiny-ViT (Vision Transformer, ViT)") | ✅ |
| D2D | Ch.2 line 63 ("Device-to-device (D2D)") | ✅ |
| C2C | Ch.2 line 68 ("Cycle-to-cycle (C2C)") | ✅ |
| STE | Ch.2 line 175 / Ch.3 line 9 ("straight-through estimator (STE)") | ✅ |
| ADC | Ch.2 line 149 ("analog-to-digital converter … ADC non-idealities") | ✅ |
| MLP | Ch.4 line 20 ("multi-layer perceptron (MLP)") | ✅ |
| QKV | Ch.4 line 20 ("query/key/value (QKV)") | ✅ |
| OPECT | Ch.5 line 77 ("organic phototransistor (OPECT)") | ✅ |
| 1T1R | Ch.7 line 308 ("one-transistor-one-resistor (1T1R)") | ✅ |
| LLM | Ch.8 line 68 ("large language model (LLM)") | ✅ |
| FPGA | Ch.8 line 109 ("field-programmable gate array (FPGA)") | ✅ |
| PAC-Bayes | Ch.8 line 154 ("probably approximately correct (PAC)--Bayes") | ✅ |

---

## 7. Complete Patch List

| File | Line | Issue | Fix | Severity |
|------|------|-------|-----|----------|
| `chapter_4_failure_modes.tex` | 46 | Broken figure ref: text references `fig:thesis-fresh-instance` (Ch.1) but Ch.4's own figure is labeled `fig:thesis-fresh-instance-c4` and never referenced. | Change `\ref{fig:thesis-fresh-instance}` → `\ref{fig:thesis-fresh-instance-c4}` | **CRITICAL** |
| `chapter_8_outlook.tex` | 33–37 | Pre-pivot language: frames `$\sim$30\%` ceiling as "artifact of fixed-mask training" and treats CX-J1 as future work, contradicting Ch.5 §6. | Rewrite to acknowledge CX-J1 result (`$30.53\pm7.07\,\%`) and frame ceiling as **structural limit**; pivot to falsification experiments CX-J1b/c/d or ImageNet pilot. | **CRITICAL** |
| `chapter_4_failure_modes.tex` | 142 | Locked-number variant: canonical Ensemble HAT reported as `$86.33` instead of `$86.37`. | Replace `$86.33` → `$86.37` and `$1.61` → `$1.54` in canonical row. | SHOULD-FIX |
| `chapter_5_mitigation.tex` | 77, 141, 245 | Locked-number variant: same `$86.33` / `$1.61` discrepancy in Tables `tab:fresh-instance-nl-c5` and `tab:three-mitigation-ceiling`. | Replace with locked `$86.37\pm1.54` or add footnote explaining source of `$86.33`. | SHOULD-FIX |
| `chapter_6_physical_realism.tex` | 73, 400 | Locked-number variant: i.i.d. baseline reported as `$86.33\pm1.61` despite text claiming it is the same checkpoint that yields `$86.37\pm1.54`. | Align with locked number or add explicit footnote. | SHOULD-FIX |
| `chapter_7_deployment.tex` | 71 | Locked-number variant: prose refers to i.i.d. baseline as `$86.33\,\%`. | Use locked `$86.37\,\%` or clarify. | SHOULD-FIX |
| `chapter_8_outlook.tex` | 53, 118 | Locked-number variant: lists `$86.33\pm1.61\,\%` for i.i.d. correlated-D2D baseline. | Use locked `$86.37\pm1.54\,\%` for i.i.d. and note `$86.33` only if it is a distinct measurement. | SHOULD-FIX |
| `chapter_1_hat_instance_overfitting.tex` | 10 | Missing forward ref to Ch.5 §6 (`sec:structural-limit`). | Insert `, \S\ref{sec:structural-limit}` after `Chapter~5`. | SHOULD-FIX |
| `chapter_6_physical_realism.tex` | ~380 (`sec:pr-synthesis`) | Missing backward ref to Ch.5 §6. | Add sentence referencing `\S\ref{sec:structural-limit}` and the structural limit. | SHOULD-FIX |
| `chapter_8_outlook.tex` | 33 | Missing backward ref to Ch.5 §6. | Add `Chapter~\ref{chap:mitigation-case-studies}, \S\ref{sec:structural-limit}` as part of the CRITICAL rewrite. | SHOULD-FIX |
| `chapter_7_deployment.tex` | 11, 142–146 | Weak negative-result framing: describes `$32\%` ceiling without explicitly calling it a **structural limit** (cf. Ch.5). | Add phrase: "…demonstrating a **structural generalization barrier**, not an optimization gap (Chapter~\ref{chap:mitigation-case-studies}, \S\ref{sec:structural-limit})." | SHOULD-FIX |
| `chapter_3_hat_taxonomy.tex` | 184 | Undefined acronym: "CIM simulation" before CIM is defined. | Add definition on first use in Ch.3 (or move definition from Ch.4 to Ch.3). | SHOULD-FIX |
| `chapter_5_mitigation.tex` | 94 | Undefined acronym: "digital FP32 baseline". | Change to "32-bit floating point (FP32) baseline". | SHOULD-FIX |
| `chapter_7_deployment.tex` | 69, 203 | Undefined acronym: "FP32 baseline" and "versus FP32". | Add definition on first use in Ch.7 or back-propagate to Ch.5. | SHOULD-FIX |
| `chapter_6_physical_realism.tex` | 274 | Undefined acronym: `\text{PTC}`. | Change to "positive temperature coefficient (PTC)". | SHOULD-FIX |
| `chapter_4_failure_modes.tex` | 167 | Undefined acronym: "AR(1)-style correlation". | Change to "first-order autoregressive (AR(1))-style correlation". | COSMETIC |
| `chapter_6_physical_realism.tex` | 50 | Undefined acronym: "AR(1)" used in equation caption. | Add "autoregressive (AR(1))" on first use. | COSMETIC |

---

## 8. Supplementary Notes

### 8.1 Ch.5 §6 internal references (sanity check)

`sec:structural-limit` is correctly referenced **within** Ch.5 from:
- Introduction (line 29)
- Case-joint-hat residual open question (line 151)
- Case-joint-hat conclusion (line 221)
- Synthesis (lines 376, 400)
- Summary (line 416)

Internal consistency is good; the issue is the **absence of external** references from Ch.1, Ch.6, and Ch.8.

### 8.2 Cross-chapter figure re-use policy

The thesis deliberately re-uses manuscript figures (paths like `../latex_gpt/figures/…`). This is by design and is not counted as a duplicate label, because each thesis figure gets a distinct `\label` even when the underlying image file is the same. The only problem is the Ch.4 mis-reference identified above.

### 8.3 Manuscript-only refs in comments

Ch.8 comments reference `\ref{sec:methodology}` and `\ref{sec:results}` (manuscript sections). These are inside `%` comments and do not affect thesis compilation. No action needed.

---

*End of report.*
