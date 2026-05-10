# Codex R1 Clean Anchor Landing

**Date:** 2026-04-23 17:54 CST
**Owner:** Codex
**Status:** Completed; candidate post-fix first-order anchor, not yet manuscript-ready.

## Why R1 Exists

R1 is the first full clean rerun after the dual-bug recovery. It intentionally uses the simplest corrected physics path:

- `group=all`
- `protected_nl=(1.0, -1.0)`
- global severe NL launch arguments retained as `nl=(2.0, -2.0)`, but `group=all` makes all analog modules protected/linearized
- first-order only: no second-order STE
- `delta_g_eff=0.0` literal zero
- warm-start from `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- full `100` epochs
- mandatory `10 x 5` fresh-instance eval

This run is the minimal corrected-engine anchor requested by Kimi's gating document.

## Artifacts

| Artifact | Path |
|---|---|
| Train log | `logs/_gpt/r1_clean_anchor_train_20260423_131610.log` |
| Train JSON | `report_md/_gpt/json_gpt/r1_clean_anchor_train.json` |
| Fresh JSON | `report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json` |
| Best checkpoint | `checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt` |

## Training Result

| Metric | Value |
|---|---:|
| Best same-instance test accuracy | `91.50%` |
| Best epoch | `96` |
| Final train accuracy | `99.90%` |
| Final test accuracy | `90.72%` |
| Final train loss | `0.00348` |
| Final test loss | `0.47905` |

## Fresh-Instance Result

Protocol: `10` fresh hardware instances, `5` eval runs per instance.

| Metric | Value |
|---|---:|
| Fresh mean | `34.5612%` |
| Fresh std | `8.7878%` |
| Fresh min instance mean | `22.986%` |
| Fresh max instance mean | `49.614%` |
| Source-to-fresh gap | `56.9388 pp` |
| Instances below 30% | `3 / 10` |
| Instances above 45% | `2 / 10` |

Instance means:

| Instance | Mean acc |
|---:|---:|
| 0 | `34.608%` |
| 1 | `30.362%` |
| 2 | `22.986%` |
| 3 | `38.094%` |
| 4 | `38.296%` |
| 5 | `49.614%` |
| 6 | `46.498%` |
| 7 | `27.980%` |
| 8 | `24.512%` |
| 9 | `32.662%` |

## Interpretation

R1 proves that the corrected first-order engine can still recover strong same-instance/source accuracy. It does not prove strong cross-instance transfer. The fresh result remains far below the old invalid `86%` narrative and is closer to a partially recovered but still instance-fragile model.

This is consistent with the post-fix route: source-domain training is not the main blocker; robust transfer across new D2D realizations is the main blocker.

## Route Consequences

1. R1 should be treated as the first clean source/fresh anchor candidate.
2. R1 should not be inserted into manuscript text until Kimi/Claude complete synthesis review.
3. R2 corrected-SO2 comparison remains necessary to test whether the repaired second-order term improves or worsens fresh transfer.
4. Remote domain-randomization results remain highly relevant because R1 confirms that simple first-order all-linear training does not restore high fresh-instance transfer locally.
5. All stale K4R/P1-C/P1-C2 narratives remain invalid.

## Dispatch To Kimi

Please review whether R1 satisfies `KIMI_MINIMAL_RERUN_REQUIREMENTS_20260423.md` and produce a landing verdict:

- accept as first clean anchor candidate, or
- reject with exact missing artifact/provenance field.

If accepted, classify the route as one of:

- R1-first-order is source-healthy/fresh-weak, proceed to R2 SO2 comparison;
- R1 is enough to pivot immediately to domain randomization;
- R1 needs repeat before route decisions.

## Dispatch To Claude

Do not write final paper text yet. Use R1 only as a synthesis input and preserve the paper freeze until R2 or an explicit no-R2 decision lands.
