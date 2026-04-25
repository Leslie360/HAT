# DISPATCH CODEX-PLOT-REFRESH — Post-Fix Figure Regeneration
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Codex
**Priority:** MEDIUM (after CX-FRESH-EVAL-MSERIES so post-fix data is available)
**Depends on:** CX-FRESH-EVAL-MSERIES delivery, NARRATIVE_PIVOT_20260424.md zone partition
**Time budget:** unconstrained, pure plotting

---

## 1. Objective

Regenerate 3-4 figures that reference severe-NL numbers or need post-fix updates. Keep every bug-immune figure untouched. Deliver PNG+PDF at paper-quality resolution.

---

## 2. Figures to regenerate

### 2.1 Fig 5 "HAT recovery" (`fig5_hat_recovery`)

**Current content**: FP32 → noisy → HAT recovery bars across Tiny-ViT and ConvNeXt on CIFAR-10/100.

**Changes needed**:
- Keep all NL=1.0 canonical bars (these are bug-immune, 86.37±1.54 stays).
- **Remove** the severe-NL bar if currently showing 27.72%.
- **Add** a new post-fix severe-NL panel (or subpanel) showing:
  - Standard HAT NL=2.0: ~83.2 ± 0.9% (remote, 3 seeds) or use local CX-M1+M5 if remote not available
  - Ensemble HAT NL=2.0: ~81.4% (local CX-M2+M6 avg)
  - Proportional HAT NL=2.0: ~84.8 ± 0.7% (remote, 5 seeds)
- Error bars = std across seeds where n ≥ 2, otherwise mark as "single-run"
- Legend distinguishes local vs remote if both shown

Output: `paper/figures/fig5_hat_recovery.{png,pdf}` (overwrite)

### 2.2 Fig S-ensemble (`figS3_ensemble_hat`)

**Current content**: Ensemble HAT concept diagram + fresh-instance transfer panel.

**Changes needed**:
- Left panel (concept): keep as-is, no changes.
- Right panel (fresh-instance transfer):
  - Standard HAT: 10.00% (bug-immune, keep)
  - Ensemble HAT: 86.37 ± 1.54% (bug-immune, keep)
  - **Add**: multi-seed CI ribbon if CX-M2+M6 Ensemble fresh-eval numbers land.
  - **Remove**: any reference to severe-NL ceiling that may exist in caption.

Output: `paper/figures/figS3_ensemble_hat.{png,pdf}` (overwrite)

### 2.3 NEW Fig "post-fix severe-NL summary" (`fig_postfix_severe_nl`)

**Purpose**: Concentrate the post-fix NL=2.0 evidence into one figure for reviewer convenience.

**Content**: 3 grouped bars per HAT type (Standard / Ensemble / Proportional), showing:
- Training best accuracy (across seeds)
- Fresh-instance eval mean
- Error bar = std across seeds

Include:
- Local bars (CX-M series, batch=64)
- Remote bars (R-M series, batch=512) — if available
- A small inset noting batch-size difference

Output: `paper/figures/fig_postfix_severe_nl.{png,pdf}` (NEW)

### 2.4 Cross-host parity supplementary figure (`figS_cross_host_parity`)

**Purpose**: Scatter plot local fresh vs remote fresh for each matching config. 45° line = perfect parity.

**Content**: Each point = one (HAT type, seed) combination. X = local fresh mean, Y = remote fresh mean. Error bars both axes. Diagonal reference line.

Story: confirms within-2σ agreement (if true), which supports the paper's reproducibility claim.

Output: `paper/figures/figS_cross_host_parity.{png,pdf}` (NEW)

---

## 3. Files to DELETE / QUARANTINE (already moved)

Already in `paper/figures/deprecated_20260424/`:
- `fig_structural_limit_signature.{png,pdf}` — keep quarantined, don't restore

No additional deletions.

---

## 4. Figures that must NOT be touched (bug-immune)

Explicit whitelist — do not regenerate:
- `fig_contour_map.pdf` (iso-accuracy map)
- `fig4_accuracy_comparison.pdf` (cross-dataset under canonical 4-bit 5% C2C 10% D2D)
- `fig10_zero_shot_transferability.pdf` (OPECT zero-shot, NL=1.0)
- `fig_kiviat_error_budget.pdf` (if exists)
- All `paper/figures/S*` supplementary figures at NL=1.0

If in doubt whether a figure uses NL=1.0 or NL=2.0 data, **check its source data first**, do not regenerate blindly.

---

## 5. Style constraints

- Color scheme: matplotlib tab10 consistent with existing figures. Do not introduce new colors.
- Font size: match paper style (caption 9pt, labels 10pt)
- Error bars: 1σ unless otherwise noted. Caption must state.
- PDF at vector resolution, PNG at 300dpi, both saved alongside.
- LaTeX-compatible label names (no Unicode in labels).

---

## 6. Deliverables

| File | Status |
|:--|:--|
| `paper/figures/fig5_hat_recovery.{png,pdf}` | Regenerate (post-fix bars added/replaced) |
| `paper/figures/figS3_ensemble_hat.{png,pdf}` | Regenerate (CI ribbon added) |
| `paper/figures/fig_postfix_severe_nl.{png,pdf}` | NEW |
| `paper/figures/figS_cross_host_parity.{png,pdf}` | NEW |
| `report_md/_gpt/CODEX_PLOT_REFRESH_REPORT_20260424.md` | Summary of changes + data sources per figure |

---

## 7. Constraints

- **No new experiments**. Only plotting.
- **Source data transparency**: figure caption / report states exactly which JSON files provided the numbers.
- **Version control**: commit figures with a meaningful message, not "update figures".
- **Do not touch paper text**: only figures in this dispatch.

---

## 8. Success criteria

- Kimi can cite these figures in K-DRAFT-v3 without worrying about bug-contaminated panels.
- Caption text for each new figure is draft-quality (Claude may refine at integration).
- Source-data provenance in report is audit-grade.
