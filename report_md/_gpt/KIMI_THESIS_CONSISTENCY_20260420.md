<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 9cdbe77 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Thesis Cross-Chapter Consistency Report

**Date:** 2026-04-20  
**Scope:** `paper/thesis/chapter_*.tex` (Chapters 1–8)  
**Reference:** `report_md/_gpt/KIMI_THESIS_NARRATIVE_ARC_20260420.md`

---

## Summary Table

| Category | CRITICAL | SHOULD-FIX | COSMETIC | Total |
|----------|----------|------------|----------|-------|
| Locked numbers consistency | 0 | 11 | 4 | 15 |
| Figure-reference validity | 3 | 1 | 0 | 4 |
| Acronym-definition order | 0 | 12 | 0 | 12 |
| Forward/backward section references | 4 | 2 | 0 | 6 |
| Narrative coherence | 0 | 8 | 0 | 8 |
| **Total** | **7** | **34** | **4** | **45** |

---

## 1. Locked Numbers Consistency

### Anchor inventory

| # | Anchor | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | Ch6 | Ch7 | Ch8 |
|---|--------|-----|-----|-----|-----|-----|-----|-----|-----|
| 1 | Ensemble HAT 86.37 ± 1.54% | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 | V4 canonical 87.95 ± 0.27% | — | — | — | ✓ | ✓ | — | ✓ | ✓ |
| 3 | NL=2.0 global 27.72 ± 0.82% | — | — | — | ✓ | ✓ | — | ✓ | ✓ |
| 4 | MLP-only 87.79% / 32.12±7.72% | — | — | — | ✓ | ✓ | — | ✓ | ✓ |
| 5 | All-linear 87.49% / 84.81% / 32.60±9.18% | — | — | — | ✓ | ✓ | partial | partial | partial |
| 6 | Correlated D2D (i.i.d./ρ0.3/ρ0.5) | — | — | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| 7 | OPECT 88.53 ± 0.08% | — | — | — | — | ✓ | — | ✓ | — |
| 8 | Inverse-gamma +5.8 pp at γ=2.0 | — | — | — | — | ✓ | — | ✓ | — |
| 9 | Retention plateau 79.13–79.51% | — | — | — | ✓ | — | ✓ | ✓ | partial |

### Detailed locked-number issues

| File | Line | Priority | Issue | Suggested fix |
|------|------|----------|-------|---------------|
| `chapter_3_hat_taxonomy.tex` | — | SHOULD-FIX | **Anchor 2 (V4 87.95±0.27%) missing.** Ch3 discusses the canonical V4 experiment extensively but never quotes its source-domain accuracy. | Add parenthetical after first mention of "canonical V4 experiment": `($87.95\pm0.27\%$ source-domain accuracy)`. |
| `chapter_6_physical_realism.tex` | — | SHOULD-FIX | **Anchors 2, 3, 4 missing entirely.** Ch6 is a physical-realism extension chapter but does not restate the canonical baselines against which extensions are judged. | Add a "Reference baselines" paragraph in §`sec:pr-intro` listing anchors 1–4 so the reader has local context. |
| `chapter_7_deployment.tex` | — | SHOULD-FIX | **Anchor 5 incomplete.** Ch7 cites `32.60 ± 9.18%` fresh-instance (lines 85, 144) but **never states the source-domain pair** `87.49%` (best) / `84.81%` (final). | Add source-domain numbers when all-linear is first mentioned in §`sec:collapse-zone` or Table `tab:danger-zone`. |
| `chapter_8_outlook.tex` | — | SHOULD-FIX | **Anchor 5 incomplete.** Ch8 cites `32.60 ± 9.18%` (line 31) but omits `87.49%` / `84.81%`. | Include the full anchor in the joint-experiment description. |
| `chapter_6_physical_realism.tex` | 384 | SHOULD-FIX | **Anchor 5 incomplete.** Only fresh-instance `32.60 ± 9.18%` appears; source-domain numbers absent. | Add source-domain ceiling numbers in the cross-cutting principle paragraph. |
| `chapter_1_hat_instance_overfitting.tex` | — | COSMETIC | **Anchors 4, 5 missing.** Ch1 introduces the fresh-instance concept but does not cite the severe-NL ceilings. | Optional: add a forward-reference sentence in the implications section citing the MLP/all-linear bounds. |
| `chapter_3_hat_taxonomy.tex` | — | COSMETIC | **Anchors 6, 7, 8, 9 missing.** Ch3 focuses on cadence and noise-profile taxonomy; physical-extension numbers are out of scope but a forward pointer would help. | Optional: add a single sentence in §`sec:summary` noting that physical-realism extensions (Ch6) validate the block-stationary guarantee under correlated D2D and retention drift. |
| `chapter_5_mitigation.tex` | — | COSMETIC | **Anchor 9 (retention plateau) missing.** Ch5 is a mitigation chapter but does not cite the retention plateau. | Optional: add retention plateau to the mitigation-synthesis table. |
| `chapter_8_outlook.tex` | 239 | COSMETIC | **Anchor 9 imprecise.** Uses "accuracy stabilises near 79%" instead of the locked range `79.13–79.51%`. | Change to `stabilises in the $79.13$--$79.51\%$ plateau`. |
| `chapter_1_hat_instance_overfitting.tex` | 13 | SHOULD-FIX | **± spacing inconsistency.** Uses `86.37\,$\pm$\,1.54\%` (thin-space) while all other chapters use `86.37\pm1.54\%` (no space). | Standardise to `\pm` without thin spaces, or apply thin spaces globally. |
| `chapter_4_failure_modes.tex` | 173–175 | SHOULD-FIX | **Correlated D2D std-dev inconsistency.** Ch4 uses `86.33 ± 1.61%` / `84.57 ± 2.39%` / `82.12 ± 3.95%`, but Ch5 line 77 uses `86.33±1.61%` (no spaces). | Standardise spacing around `\pm` and between numbers and `%`. |
| `chapter_5_mitigation.tex` | 86 | SHOULD-FIX | **Inverse-gamma anchor imprecise.** States "restores +5.8 pp accuracy (from 84.04% to 89.85% ...)" but the locked anchor is only the **+5.8 pp** figure; the 84.04% / 89.85% are ResNet-18 deterministic numbers, not Tiny-ViT. | Clarify that `+5.8` pp is the locked cross-architecture gain, while the absolute percentages are ResNet-18 deterministic evaluations. |
| `chapter_5_mitigation.tex` | 77 | SHOULD-FIX | **Correlated D2D std-dev spacing.** Uses `86.33\pm1.61%` etc. without space before `%`, while Ch4 uses `\,\%`. | Standardise to `\,\%` globally. |
| `chapter_4_failure_modes.tex` | 66 | SHOULD-FIX | **Per-batch number stale.** Claims per-batch resampling "raises fresh-instance accuracy further to $89.48 \pm 0.36\%$". This number is **inconsistent** with Ch3 (86.16%) and Ch5 (86.16%) held-out ablations. The 89.48% figure does not appear elsewhere in the thesis and may be a manuscript draft artifact. | **Verify or remove.** If unverified, replace with language consistent with Ch3/Ch5: "per-batch resampling underperforms per-epoch in the held-out ablation." |

---

## 2. Figure-Reference Validity

### All `\label{fig:...}` definitions

| Label | Defined in | Referenced in | Status |
|-------|-----------|---------------|--------|
| `fig:thesis-fresh-instance` | Ch1 (L21), **Ch4 (L52)** | Ch1, Ch4, Ch5 | **DUPLICATE LABEL** |
| `fig:cadence-visual` | Ch3 (L62) | Ch3 | OK |
| `fig:fresh-instance-ablation` | Ch3 (L118) | Ch3 | OK |
| `fig:design-plane` | Ch3 (L263) | Ch3 | OK |
| `fig:retention-curve` | Ch2 (L120) | Ch2 | OK |
| `fig:frontend-compensation` | Ch2 (L144) | Ch2 | OK |
| `fig:weight-mapping` | Ch2 (L220) | Ch2 | OK |
| `fig:nl-gradient` | Ch2 (L255) | Ch2 | OK |
| `fig:system-arch` | Ch2 (L270) | Ch2 | OK |
| `fig:supp-nl-gradient-repeat` | Ch4 (L109) | Ch4 | OK |
| `fig:supp-corr-d2d-repeat` | Ch4 (L183) | Ch4 | OK |
| `fig:retention-curve-repeat` | Ch4 (L218) | Ch4 | OK |
| `fig:thesis-fresh-instance-c5` | Ch5 (L74) | Ch5 | OK |
| `fig:corr-d2d-c5` | Ch5 (L83) | Ch5 | OK |
| `fig:nl-gradient-c5` | Ch5 (L121) | Ch5 | OK |
| `fig:fresh-instance-ablation-c5` | Ch5 (L233) | Ch5 | OK |

### Broken / external figure references

| File | Line | Priority | Issue | Suggested fix |
|------|------|----------|-------|---------------|
| `chapter_1_hat_instance_overfitting.tex` | 21 | **CRITICAL** | **Duplicate label** `fig:thesis-fresh-instance` also defined in Ch4 L52. LaTeX will emit "multiply defined label" warning and the second definition wins, breaking Ch1's reference. | Rename Ch4's label to `fig:thesis-fresh-instance-c4` (consistent with Ch5's `-c5` suffix) and update Ch4's `\ref`. |
| `chapter_3_hat_taxonomy.tex` | 61 | **CRITICAL** | **External figure reference** `\ref{fig:ensemble-hat-concept}` points to a manuscript figure that does not exist in the thesis tree. | Mark as external: `(Figure~\ref{fig:ensemble-hat-concept} of the manuscript)` — already partially present in caption, but the `\ref` will still break. Replace with plain text: `manuscript Figure~S3` or create a thesis-local dummy label. |
| `chapter_4_failure_modes.tex` | 46, 171, 207 | **CRITICAL** | **Caption references manuscript figures without local labels.** Captions cite `Fig.~S3`, `Fig.~S4`, `Fig.~S5`, `Fig.~S6` and `Fig.~7` from the manuscript. These are plain-text citations, not `\ref` calls, so they will not break compilation, but they are **unverifiable** in a standalone thesis build. | Ensure all `\includegraphics` paths are correct (verified OK) and decide whether to add a `\label` for each reused manuscript figure in the thesis, or keep as plain-text with a `"(manuscript)"` qualifier. |
| `chapter_5_mitigation.tex` | 72, 81, 119, 231 | SHOULD-FIX | **Reused figure paths lack `.pdf` / `.png` extension consistency.** Some use extensionless paths (`figS3_ensemble_hat`), others are explicit. All target files exist in both `.pdf` and `.png`, so compilation is safe, but best practice is to be explicit. | Standardise to `.pdf` for vector figures and `.png` for raster, or rely on the existing ambiguity (low risk). |

### `\includegraphics` inventory (all paths verified on disk)

| File | Line | Path | File exists? |
|------|------|------|--------------|
| Ch1 | 19 | `../latex_gpt/figures/figS3_ensemble_hat` | ✓ (pdf + png) |
| Ch2 | 118 | `../latex_gpt/figures/fig7_retention_curve` | ✓ (pdf + png) |
| Ch2 | 142 | `../latex_gpt/figures/fig6_physical_compensation` | ✓ (pdf + png) |
| Ch2 | 218 | `../latex_gpt/figures/fig2_weight_mapping` | ✓ (pdf) |
| Ch2 | 253 | `../latex_gpt/figures/fig_nl_gradient_distortion` | ✓ (pdf + png) |
| Ch2 | 268 | `../latex_gpt/figures/fig1_system_architecture` | ✓ (pdf) |
| Ch3 | 60 | `../latex_gpt/figures/figS3_ensemble_hat` | ✓ |
| Ch3 | 116 | `../latex_gpt/figures/fig_fresh_instance_ablation` | ✓ (pdf + png) |
| Ch4 | 50 | `../latex_gpt/figures/figS3_ensemble_hat` | ✓ |
| Ch4 | 107 | `../latex_gpt/figures/fig_nl_gradient_distortion` | ✓ |
| Ch4 | 181 | `../latex_gpt/figures/figS_corr_d2d` | ✓ (pdf + png) |
| Ch4 | 216 | `../latex_gpt/figures/fig7_retention_curve` | ✓ |
| Ch5 | 72 | `../latex_gpt/figures/figS3_ensemble_hat` | ✓ |
| Ch5 | 81 | `../latex_gpt/figures/figS_corr_d2d` | ✓ |
| Ch5 | 119 | `../latex_gpt/figures/fig_nl_gradient_distortion` | ✓ |
| Ch5 | 231 | `../latex_gpt/figures/fig_fresh_instance_ablation` | ✓ |

---

## 3. Acronym-Definition Order

### Acronyms used before first definition in each chapter

| Acronym | First defined | Used undefined in | Priority | Suggested fix |
|---------|---------------|-------------------|----------|---------------|
| **HAT** | Ch1 L8 | Ch4 L8 ("hardware-aware training (HAT)" is actually defined there — OK), but Ch2 L29 uses "hardware-aware training" without the acronym. | COSMETIC | Ch2 is framework; acronym optional. No action required. |
| **C2C** | Ch2 L68 | Ch1 (not used), Ch4 uses without explicit expansion, Ch5 uses without expansion, Ch6 L19 defines it, Ch7 uses without expansion, Ch8 uses without expansion. | SHOULD-FIX | Add "cycle-to-cycle (C2C)" on first use in Ch4, Ch5, Ch7, Ch8. |
| **MLP** | **Never expanded** | First used Ch4 L20. | SHOULD-FIX | Add "multi-layer perceptron (MLP)" on first use in Ch4. |
| **QKV** | **Never expanded** | First used Ch4 L20. | SHOULD-FIX | Add "query/key/value (QKV)" on first use in Ch4. |
| **OPECT** | **Never expanded** | First used Ch5 L77. | SHOULD-FIX | Add expansion: "organic phototransistor (OPECT) proxy" or similar. |
| **ViT** | **Never expanded** | First used Ch1 L8 ("Tiny-ViT"). | SHOULD-FIX | Add "Vision Transformer (ViT)" on first use in Ch1. |
| **CNN** | **Never expanded** | First used Ch7 L236. | SHOULD-FIX | Add "convolutional neural network (CNN)" on first use in Ch7. |
| **NRE** | **Never expanded** | First used Ch7 L276. | SHOULD-FIX | Add "non-recurring engineering (NRE)" on first use in Ch7. |
| **FPGA** | **Never expanded** | First used Ch8 L125. | SHOULD-FIX | Add "field-programmable gate array (FPGA)" on first use in Ch8. |
| **PAC-Bayes** | **Never expanded** | First used Ch8 L152. | SHOULD-FIX | Add "probably approximately correct (PAC)–Bayes" or define PAC separately. |
| **MBConv** | **Never expanded** | First used Ch2 L262. | SHOULD-FIX | Add "mobile inverted bottleneck convolution (MBConv)" on first use in Ch2. |
| **JSON** | **Never expanded** | First used Ch3 L158. | SHOULD-FIX | Add "JavaScript Object Notation (JSON)" on first use in Ch3. |
| **SPICE** | **Never expanded** | First used Ch2 L280. | SHOULD-FIX | Add "Simulation Program with Integrated Circuit Emphasis (SPICE)" on first use in Ch2. |
| **DNL** | Ch2 L149 | — | OK |
| **LTP / LTD** | Ch4 L75 | — | OK |
| **LLM** | Ch8 L66 | — | OK |
| **DNTT** | Ch4 L203 | — | OK |
| **ADC / DAC** | Ch2 L149, L156 | — | OK |
| **STE** | Ch2 L175 / Ch3 L9 | — | OK |
| **CIM** | Ch4 L8 | — | OK |
| **GPU** | Ch2 L280 | — | OK (common term) |

---

## 4. Forward / Backward Section References

### Broken internal references

| File | Line | Priority | Issue | Suggested fix |
|------|------|----------|-------|---------------|
| `chapter_2_framework.tex` | 102 | **CRITICAL** | `Chapter~\ref{chap:severe-nl}` — label `chap:severe-nl` **does not exist** in the thesis. The closest equivalent is `chap:failure-mode-atlas` (Ch4) or the severe-NL discussion spans Ch4–Ch5. | Replace with `Chapter~\ref{chap:failure-mode-atlas}` or rephrase to avoid a specific chapter reference. |
| `chapter_4_failure_modes.tex` | 223 | **CRITICAL** | `Appendix~\ref{subsec:retention-comparison}` — this appendix subsection **does not exist** in the thesis tree. | Remove the reference or create the appendix stub. |

### Manuscript-only references (will break in standalone thesis compilation)

The following `\ref{...}` calls target manuscript labels that are **not present** in the thesis source. If the thesis is compiled standalone, these will produce `??` placeholders.

| File | Lines | Priority | Referenced manuscript labels |
|------|-------|----------|------------------------------|
| `chapter_3_hat_taxonomy.tex` | 11, 18, 43, 89, 158, 231 | **CRITICAL** | `sec:methodology`, `subsec:nl-hat-stress`, `subsec:hybrid-deployment`, `subsec:hardware-transferability`, `subsec:profile-interface` |
| `chapter_4_failure_modes.tex` | 26, 40, 44, 62, 75, 77, 167, 203, 227, 256 | **CRITICAL** | `sec:results`, `sec:discussion`, `subsec:modeling-nonidealities`, `subsec:transferability`, `subsec:physical-stress`, `subsec:limitations`, `sec:appendix-provenance`, `tab:provenance`, `subsec:energy-results` |
| `chapter_5_mitigation.tex` | (none via `\ref`) | — | — |
| `chapter_6_physical_realism.tex` | 19, 42, 162, 224, 281 | **CRITICAL** | `subsec:limitations`, `subsec:retention-drift` |
| `chapter_7_deployment.tex` | 126, 203, 236, 293, 304 | **CRITICAL** | `subsec:iso-accuracy`, `subsec:energy-results`, `subsec:quantization-noise`, `sec:discussion`, `subsec:limitations` |
| `chapter_8_outlook.tex` | 143 | SHOULD-FIX | `subsec:frontend-interface` (of Ch2 — this one actually **does** exist in the thesis, but the reference syntax `Section~\ref{subsec:frontend-interface} of Chapter~\ref{chap:framework}` is valid) |

**Suggested fix for manuscript-only refs:** Convert all manuscript `\ref{sec:...}` and `\ref{subsec:...}` calls to plain text: e.g. `manuscript Section~5.1` or `the manuscript's methodology section`. Alternatively, compile the thesis as a child document of the manuscript master so the labels resolve.

### Valid internal cross-references (sampled)

All `\ref{chap:*}` and `\ref{sec:*}` pointing to thesis-local labels were verified against the label inventory and are **valid**, except those flagged above.

---

## 5. Narrative Coherence

### Boundary-sentence audit (K-V7 narrative arc)

The narrative arc specifies 7 verbatim boundary sentences. **None appear verbatim** in the current draft.

| Boundary | Arc sentence | Actual text | Status |
|----------|--------------|-------------|--------|
| **Ch1 → Ch2** | *"To make those claims falsifiable, the thesis now introduces the simulation framework every subsequent experiment inherits."* | Ch1 ends with bullet items; no explicit Ch1→Ch2 bridge. | **MISSING** |
| **Ch2 → Ch3** | *"With the instrument in place, the first question is how HAT behaves when training and deployment instances differ."* | Ch2 L320: "With the framework in place, the next chapter turns to the first major experimental boundary: what happens when the write nonlinearity becomes severe..." | **MISALIGNED** — points to severe-NL (Ch4/5) rather than HAT taxonomy (Ch3). |
| **Ch3 → Ch4** | *"The taxonomy reveals symptoms, but symptoms are not diagnoses; the next section names the diseases."* | Ch3 L277: "This insight motivates the experimental focus of Chapter~\ref{chap:hat-instance-overfitting}, where the block-stationary guarantee is tested under severe nonlinear write and spatially correlated mismatch." | **MISALIGNED** — jumps back to Ch1 instead of forward to Ch4 (failure-mode atlas). |
| **Ch4 → Ch5** | *"Each named failure now receives its remedy, with recovery ceilings explicitly measured."* | Ch4 L284: "Together, the atlas and its themes provide the methodological foundation for the thesis experiments that follow..." | **PARAPHRASED** — acceptable but not verbatim. |
| **Ch5 → Ch6** | *"These recoveries assume idealized noise; the next chapter reintroduces the physical world."* | Ch5 ends with summary paragraphs; no explicit pointer to Ch6. | **MISSING** |
| **Ch6 → Ch7** | *"Surviving physical realism is necessary but not sufficient; the thesis now translates survival into deployment rules."* | Ch6 L409: "The synthesis ... maps each extension to a contribution tier ... and connects the extensions back to the failure-mode atlas." No Ch7 pointer. | **MISSING** |
| **Ch7 → Ch8** | *"The envelope is where the thesis ends and the next project begins."* | Ch7 ends with a standard concluding paragraph; no Ch8 pointer. | **MISSING** |

### Detailed narrative-coherence issues

| File | Line | Priority | Issue | Suggested fix |
|------|------|----------|-------|---------------|
| `chapter_1_hat_instance_overfitting.tex` | 42–47 | SHOULD-FIX | **Missing Ch1→Ch2 boundary sentence.** Ch1 ends with bullet points that point forward to "later severe-NL chapter" and "correlated-D2D robustness chapter" but never explicitly bridges to Ch2 (framework). | Add a closing paragraph before the bullet list: *"To make those claims falsifiable, the thesis now introduces the simulation framework every subsequent experiment inherits."* (per arc). |
| `chapter_2_framework.tex` | 320 | SHOULD-FIX | **Ch2→Ch3 pointer misaligned.** Currently points to "severe nonlinearity" (Ch4/5 territory). Ch3 is the HAT taxonomy. | Rewrite closing sentence: *"With the instrument in place, the first question is how HAT behaves when training and deployment instances differ."* |
| `chapter_3_hat_taxonomy.tex` | 277 | SHOULD-FIX | **Ch3 forward pointer jumps to Ch1.** Should point to Ch4 (failure-mode atlas). | Replace with: *"The taxonomy reveals symptoms, but symptoms are not diagnoses; the next chapter names the diseases."* and update `\ref{chap:failure-mode-atlas}`. |
| `chapter_4_failure_modes.tex` | 284 | SHOULD-FIX | **Ch4→Ch5 boundary paraphrased.** Acceptable but arc requests verbatim sentence. | Consider inserting verbatim boundary sentence at start of summary: *"Each named failure now receives its remedy, with recovery ceilings explicitly measured."* |
| `chapter_5_mitigation.tex` | 317–332 | SHOULD-FIX | **Missing Ch5→Ch6 boundary.** Summary ends with generic closing; no pointer to physical-realism extensions. | Add closing sentence: *"These recoveries assume idealized noise; the next chapter reintroduces the physical world."* |
| `chapter_6_physical_realism.tex` | 409 | SHOULD-FIX | **Missing Ch6→Ch7 boundary.** Synthesis closes by connecting back to Ch4, not forward to Ch7. | Add closing sentence: *"Surviving physical realism is necessary but not sufficient; the thesis now translates survival into deployment rules."* |
| `chapter_7_deployment.tex` | 344 | SHOULD-FIX | **Missing Ch7→Ch8 boundary.** Standard conclusion with no outlook pointer. | Add closing sentence: *"The envelope is where the thesis ends and the next project begins."* |
| `chapter_8_outlook.tex` | 17 | SHOULD-FIX | **Missing Ch8 backward pointer to Ch7.** Ch8 opens with a broad bridge but does not explicitly cite the deployment envelope of Ch7 as its immediate predecessor. | Add explicit backward pointer in introduction: *"The preceding chapter constructed the deployment envelope; this chapter steps outside it to propose the next-generation theory and hardware roadmap."* |

---

## Appendix: Quick-Reference Patch Priority

### CRITICAL (blocks standalone compilation or causes broken links)
1. **Duplicate label** `fig:thesis-fresh-instance` (Ch1 + Ch4).
2. **Broken chapter ref** `\ref{chap:severe-nl}` in Ch2.
3. **Manuscript-only `\ref` calls** (~25 instances) will render as `??` in standalone thesis.
4. **Missing appendix ref** `\ref{subsec:retention-comparison}` in Ch4.

### SHOULD-FIX (copy-editor pass)
5. Add missing locked-number anchors to Ch3, Ch6, Ch7, Ch8 where incomplete.
6. Expand all unexpanded acronyms (MLP, QKV, OPECT, ViT, CNN, NRE, FPGA, PAC-Bayes, MBConv, JSON, SPICE).
7. Insert or restore all 7 narrative-arc boundary sentences.
8. Fix Ch2 and Ch3 forward-pointer misalignments.
9. Standardise `\pm` and `%` spacing globally.
10. Verify or remove the stale `89.48 ± 0.36%` per-batch claim in Ch4.

### COSMETIC
11. Add optional forward references for out-of-scope locked numbers (Ch1, Ch3, Ch5).
12. Standardise figure-path extensions.
