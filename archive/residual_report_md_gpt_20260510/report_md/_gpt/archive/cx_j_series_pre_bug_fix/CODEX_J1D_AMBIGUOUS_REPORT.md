# CODEX J1d Ambiguous Report
**Date:** 2026-04-21
**Executor:** Codex
**Trigger:** J1d-2 fresh-instance mean = 41.53%, falling in the 35–50% ambiguous zone per BROADCAST_FINAL_AUTONOMOUS_20260420 §1.2.

---

## 1. J1d-2 Result Summary

| Metric | Value |
|:---|:---|
| Training best accuracy | **91.02%** @ epoch 78 |
| Fresh-instance mean (10×5) | **41.53% ± 8.87%** |
| Fresh-instance range | **27.51% – 51.62%** |
| Fresh-instance median | **43.90%** |

### Per-instance breakdown

| Instance | Seed | Mean Acc (%) | Zone |
|:---:|:---:|:---:|:---|
| 1 | 42 | 27.51 | Collapse (~J1b/J1c) |
| 2 | 142 | 47.65 | Ambiguous-mid |
| 3 | 242 | 47.22 | Ambiguous-mid |
| 4 | 342 | 28.03 | Collapse (~J1b/J1c) |
| 5 | 442 | 42.21 | Ambiguous-mid |
| 6 | 542 | 33.88 | Ambiguous-low |
| 7 | 642 | **51.62** | **Ceiling-broken** |
| 8 | 742 | 44.59 | Ambiguous-mid |
| 9 | 842 | **50.99** | **Ceiling-broken** |
| 10 | 942 | 41.60 | Ambiguous-mid |

---

## 2. Why This Is Ambiguous

### Structural-limit evidence (collapse cohort)
- Instances 1 & 4 collapsed to **27.51%** and **28.03%** — statistically indistinguishable from J1b (26.37%), J1c (28.09%), and MLP-only fresh (32.12%).
- This suggests the **structural-limit hypothesis is NOT falsified** for a subset of fresh-instance draws.

### Ceiling-broken evidence (recovery cohort)
- Instances 7 & 9 reached **51.62%** and **50.99%** — the first time any NL=2.0 configuration has exceeded 50% on fresh-instance transfer.
- The training best of **91.02%** also far exceeds the ~87-88% ceiling of MLP-only linearization.

### Bimodality / instability
- The distribution is **highly variable** (σ = 8.87%, CV = 21.4%).
- There is no clear single mode; the results suggest a mixture of "collapse basins" and "recovery basins" depending on the fresh D2D draw.
- This is consistent with a **stochastic-basin sensitivity** narrative: some D2D realizations fall into a recoverable basin, others into a collapsed basin.

---

## 3. Comparison to Tier-1 Baselines

| Experiment | Train best | Fresh mean | Fresh σ | Interpretation |
|:---|:---:|:---:|:---:|:---|
| J1 (Standard HAT) | ~97% | **30.53 ± 7.07%** | 7.07% | Structural collapse |
| J1b (QKV-only linear) | 26.37% | **~10%** final | — | QKV path structurally fails |
| J1c (Full-attn linear) | 28.09% | **~10%** final | — | Entire attention path fails |
| J1d-2 (2nd-order STE, MLP-prot) | **91.02%** | **41.53 ± 8.87%** | 8.87% | **Partial recovery with bimodal instability** |
| Canonical Ensemble HAT (V4, NL=1.0) | ~97% | **86.37 ± 1.54%** | 1.54% | Deployment-grade |

---

## 4. Pre-authorized Branch Decision

Per BROADCAST_FINAL_AUTONOMOUS_20260420 §1.2:

> `35–50%` (partial recovery) → ⏸ **AMBIGUOUS**. Stop queue. Write `CODEX_J1D_AMBIGUOUS_REPORT.md` with full data; do NOT launch tier-2. Wait for Friday.

**Decision: ⏸ STOP QUEUE. No Tier-2 auto-launch.**

Rationale:
1. The mean (41.53%) is squarely in the ambiguous zone.
2. The high variance (σ=8.87%) and bimodal-like pattern make a binary "collapse vs. breakthrough" framing inappropriate.
3. Launching Tier-2 (J2/J3/J4) under ambiguity would waste GPU hours on a narrative that may need reframing.
4. The architect (Claude) should review this result on Friday and decide whether to:
   - Frame as "partial higher-order recovery with D2D-dependent basin instability"
   - Run additional diagnostics (e.g., sweep delta_g_eff, vary second-order strength)
   - Accept the ambiguity and pivot thesis Ch.5 accordingly

---

## 5. Files Generated

- `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json` — Full 10×5 instance-level data
- `logs/_gpt/cx_j1d_fresh_eval_20260421.log` — Execution log
- `report_md/_gpt/CODEX_CX_J1d_SUMMARY.md` — Updated experiment summary
- This report: `report_md/_gpt/CODEX_J1D_AMBIGUOUS_REPORT.md`

---

## 6. Recommended Actions for Friday Review

1. **Quantify basin instability**: Is the bimodality reproducible? Would 20 or 30 fresh instances sharpen the mean estimate?
2. **Delta-g_eff sweep**: The current run used delta_g_eff=0.0. Would a non-zero value (e.g., 0.15 as in AnalogLinearConfig default) shift the distribution?
3. **Narrative framing memo**: Should the thesis present this as (a) "higher-order surrogate partially recovers but fresh-instance variance remains unacceptable," or (b) "stochastic-basin sensitivity is the true structural property, not uniform collapse"?
4. **Tier-2 hold**: Keep J2/J3/J4 on hold pending narrative decision. If the story becomes "partial recovery + basin instability," Tier-2 (heavy-tailed D2D, temperature) may actually be *more* relevant, not less.
