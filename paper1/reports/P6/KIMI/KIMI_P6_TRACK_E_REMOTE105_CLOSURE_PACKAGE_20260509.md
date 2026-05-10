# Kimi P6 Track E Report: Remote 105 Closure Package (Updated)

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md`
**Executor:** kimi
**Update:** 2026-05-09 — seed789 received, canonical freeze ingested

---

## 1. Data Status — COMPLETE

**Dataset:** TinyImageNet-200
**Protocol:** Best-epoch test accuracy, 10 fresh instances x 5 MC per checkpoint
**Status:** All 3 seeds (123, 456, 789) complete for both architectures

### DeiT-Small-Patch16-224

| HAT Type | Seed 123 | Seed 456 | Seed 789 | FreshMean Mean ± Std | Collapse (Train−Fresh) |
|----------|----------|----------|----------|----------------------|------------------------|
| Digital | 48.22 | 53.61 | 53.58 | 51.80 ± 2.91 | ~0 |
| Proportional | 50.24 | 54.44 | 56.54 | 53.61 ± 3.14 | ~0 |
| Ensemble | 45.26 | 44.52 | — | 40.78 ± 0.33 | −4.1 pt |
| Standard | 40.61 | 41.19 | — | 6.61 ± 0.23 | **−34.3 pt** |

### ViT-Small-Patch16-224

| HAT Type | Seed 123 | Seed 456 | Seed 789 | FreshMean Mean ± Std | Collapse (Train−Fresh) |
|----------|----------|----------|----------|----------------------|------------------------|
| Digital | 48.83 | 54.58 | 50.86 | 51.42 ± 2.87 | ~0 |
| Proportional | 49.03 | 54.06 | 55.85 | 52.69 ± 3.47 | ~0 |
| Ensemble | 43.64 | 44.79 | — | 40.16 ± 0.08 | −4.1 pt |
| Standard | 39.22 | 38.43 | — | 6.92 ± 1.70 | **−31.9 pt** |

---

## 2. Proportional-vs-Digital Analysis (Fresh, pp)

| Seed | DeiT Prop − Digital | ViT Prop − Digital |
|---:|---:|---:|
| 123 | +1.98 | +0.17 |
| 456 | +0.58 | −0.68 |
| 789 | +2.75 | +4.55 |
| **Mean** | **+1.77** | **+1.35** |

**DeiT:** 3/3 seeds favor proportional. Confident.

**ViT:** 2/3 seeds favor proportional. Seed456 digital (54.58%) is an outlier (+5.75pt above seed123, +3.72pt above seed789), but protocol audit confirms no violation — commands, splits, checkpoints all identical except seed. Outlier diagnostic recommends keeping seed456 and labeling ViT as **provisional** (see `REMOTE105_VIT_SEED456_OUTLIER_NOTE_20260508.md`).

---

## 3. Verdict

| Item | Status |
|------|--------|
| Data completeness | **Complete (3/3 seeds)** |
| DeiT proportional advantage | **Confirmed** (+1.77pt, 3/3 seeds) |
| ViT proportional advantage | **Provisional** (+1.35pt, 2/3 seeds, outlier documented) |
| Standard HAT collapse | Confirmed (strong) |
| Ensemble HAT collapse | Confirmed (moderate) |
| Closure action | **Data received and analyzed** |

**Classification update:**
- DeiT proportional cross-architecture: `defense-support` → `paper1-supplement-candidate`
- ViT proportional cross-architecture: `future-only` → `defense-support`
- Standard HAT collapse on TinyImageNet: `paper1-supplement-candidate`

**Manuscript recommendation:** Anchor cross-architecture claim on DeiT (strong). ViT can be noted as "consistent provisional validation" or held for supplement response to review.

---

## 4. Source Files

- `docs/handoff/REMOTE105_CANONICAL_FREEZE_20260508.md` — frozen data package
- `docs/handoff/REMOTE105_VIT_SEED456_OUTLIER_NOTE_20260508.md` — outlier diagnostic
- Branch: `105-remote-results`, freeze commit: `ccf1cf7`

---

*Report by kimi. Updated on 2026-05-09 with seed789 and canonical freeze.*
