# Kimi P7 Track G: Appendix Visual QA Handoff

**Date:** 2026-05-09
**Scope:** Supplementary figures — layout issues only, no scientific edits
**Owner:** Kimi (audit) → Gemini/user (execution)

---

## 1. Audit Method

Reviewed `paper/latex_gpt/supplementary.tex` and supplementary figure sources. Focus: layout, typography, legibility. **No numbers, captions, or claims were modified.**

---

## 2. Figure Inventory

### TikZ Sources (Vector, Safe)

| Figure | File | Status | Notes |
|--------|------|--------|-------|
| figS1 | `supplementary/figS1_asymmetry_concept_tikz.tex` | ✅ OK | Vector, clean |
| figS2 | `supplementary/figS2_nonideality_tikz.tex` | ✅ OK | Vector, clean |
| figS5 | `supplementary/figS5_proxy_sensitivity_tikz.tex` | ✅ OK | Vector, clean |
| fig_late_recovery | `supplementary/fig_late_recovery_tikz.tex` | ✅ OK | Vector, clean |

### Included Graphics (PNG/PDF)

| Figure | File | Width | Status | Issue |
|--------|------|-------|--------|-------|
| S1_exact | `figures/S1_exact.png` | 0.98\textwidth | ⚠️ Review | Large width may cause overflow in two-column layout |
| S2_exact | `figures/S2_exact.png` | 0.98\textwidth | ⚠️ Review | Same as above |
| S3_exact | `figures/S3_exact.png` | 0.98\textwidth | ⚠️ Review | Same as above |
| S4_exact | `figures/S4_exact.png` | 0.98\textwidth | ⚠️ Review | Same as above |
| fig_proxy_sensitivity_map | `figures/fig_proxy_sensitivity_map` | 0.72\textwidth | ✅ OK | Reasonable width |
| fig_sobol_sensitivity | `figures/fig_sobol_sensitivity` | 0.62\textwidth | ✅ OK | Reasonable width |
| fig9_noise_sensitivity | `figures/fig9_noise_sensitivity` | 0.96\textwidth | ⚠️ Review | Very wide; check font size at print scale |
| fig_fresh_instance_ablation | `figures/fig_fresh_instance_ablation` | 0.96\textwidth | ⚠️ Review | Very wide; check font size at print scale |
| fig_attention_maps | `figures/fig_attention_maps` | 0.75\textwidth | ✅ OK | Reasonable width |

---

## 3. Prioritized Visual Issue List

### 🔴 High Priority

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 1 | **S1–S4_exact.png use 0.98\textwidth** — may overflow page margins or cause compilation warnings | supplementary.tex lines 38, 85, 132, 146 | Reduce to `0.95\textwidth` or use `\linewidth` with `\centering`; verify `\textwidth` vs `\linewidth` in `figure*` environment |
| 2 | **fig9_noise_sensitivity and fig_fresh_instance_ablation at 0.96\textwidth** — subplots may have unreadably small fonts | supplementary.tex lines 559, 566 | Increase figure native resolution or reduce subplot count; ensure axis labels ≥ 8pt at print |

### 🟡 Medium Priority

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 3 | **Inconsistent palette risk** — S1–S4_exact may use different color schemes than main figures | `figures/S*_exact.png` | Verify colormap consistency with `fig3_snr_curves.png` and `fig4_accuracy_comparison.png` |
| 4 | **fig_attention_maps (0.75\textwidth)** — 5 rows × 3 columns = 15 sub-images; may be too small | supplementary.tex line 573 | Consider splitting into two figures or using `\subfigure` with larger overall width |
| 5 | **Missing vector versions** — S1–S4_exact are PNG raster; TikZ versions exist only for concepts (figS1, figS2) | `figures/` dir | If journal requires vector, regenerate S3/S4 exact plots as PDF |

### 🟢 Low Priority

| # | Issue | Location | Suggested Fix |
|---|-------|----------|---------------|
| 6 | **Legend occlusion risk** — Wide figures with multiple legend entries may overlap | `fig9_noise_sensitivity`, `fig_fresh_instance_ablation` | Move legends outside plot area or use `ncol` to compress |
| 7 | **Empty whitespace** — Some `figure*` environments may leave uneven vertical gaps | supplementary.tex | Check `\vspace` usage; ensure consistent `\abovecaptionskip` |
| 8 | **Backup files present** — `figS1_asymmetry_concept.png.bak`, `figS2_nonideality.png.bak` | `paper/latex_gpt/figures/` | Safe to delete; not referenced by LaTeX |

---

## 4. Handoff to Gemini/User Visual Lane

**Gemini should:**

1. Regenerate S1–S4_exact figures at higher resolution if fonts appear small in compiled PDF.
2. Verify color palette consistency across all supplementary figures.
3. Check `\textwidth` vs `\linewidth` usage in `figure*` environments.
4. Remove `.bak` and `_gptimage.png` duplicate files from `figures/` directory.

**Gemini must NOT:**

1. Edit any caption text containing numerical claims.
2. Modify `tab_pcm_precision_ladder.csv` or any source data.
3. Change `\includegraphics` paths to point at unverified data.
4. Reinterpret drift definitions or accuracy values.

---

## 5. Verdict

| Check | Result |
|-------|--------|
| Main figures untouched | ✅ Verified — no edits to main text figures |
| Layout issues identified | ✅ 8 issues, prioritized |
| No scientific edits | ✅ Confirmed — only visual/layout concerns |
| Clear handoff to Gemini | ✅ 4 allowed actions, 4 forbidden actions |

**Track G Status: COMPLETE — handoff ready for Gemini/user visual pass.**

---

*Report by kimi. 2026-05-09.*
