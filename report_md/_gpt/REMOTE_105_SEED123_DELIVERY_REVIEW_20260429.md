# Remote 105 Seed-123 Delivery Review

**Date:** 2026-04-29  
**Reviewer:** Codex  
**Scope:** Work-1 architecture / HAT validation, seed=123 report from Remote 105.

## 1. Received Table

| Architecture | HAT | Best Train Acc | Fresh Mean | Fresh Std | Status |
|---|---|---:|---:|---:|---|
| deit | proportional | 50.24% | 50.20% | 0.10% | best |
| vit | proportional | 49.03% | 49.00% | 0.09% | stable |
| vit | digital | 48.83% | 48.83% | 0.00% | no-noise ceiling |
| deit | ensemble | 45.26% | 40.44% | 0.43% | -4.8pt |
| vit | ensemble | 43.64% | 40.24% | 0.36% | -3.4pt |
| deit | standard | 40.61% | 6.38% | 0.85% | collapsed |
| vit | standard | 39.22% | 5.22% | 0.51% | collapsed |

## 2. What Looks Strong

1. **Proportional mode is the strongest current route.** Both `deit` and `vit` proportional show fresh means almost identical to the source/best metric and very low fresh std.
2. **Standard is a useful negative control.** If protocol is correct, standard mode shows that eval-only noise robustness is not sufficient.
3. **Ensemble helps but is not enough.** Ensemble fresh accuracy remains far above standard but loses several points from the source/best metric.

## 3. What Cannot Yet Be Claimed

1. **Do not claim proportional > digital from `deit_proportional` vs `vit_digital`.** This comparison is architecture-confounded. The missing critical run is `deit_digital`.
2. **Do not claim zero degradation until fresh protocol is audited.** Need per-instance list, number of instances, MC repeats, and noise resampling policy.
3. **Clarify "Best Train Acc".** If this is actual training-set accuracy, the low ceiling and near-equality to fresh are surprising. If it is source/test accuracy, rename it.
4. **Single seed is not enough.** The table is seed=123 only. Multi-seed is mandatory before paper-level claims.

## 4. Codex Recommendation

Treat the result as a high-priority signal and run closure experiments immediately:

1. Add `deit_digital` under identical schedule.
2. Complete same-architecture matrix for seed=123.
3. Run seeds 456 and 789 for the priority cells.
4. If same-architecture proportional still beats digital, add the proportional regularization ablation: train-noise-on/eval-noise-off vs train-noise-on/fresh-noise-on.
5. Then move to multi-dataset validation.

The next task file for 105 is `REMOTE_105_MULTIDATASET_TASKLIST_20260429.md`.
