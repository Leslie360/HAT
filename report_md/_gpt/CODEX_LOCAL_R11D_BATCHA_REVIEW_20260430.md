# Codex Review — Local R11D Batch A Complete

**Date:** 2026-04-30  
**Reviewer:** Codex  
**Scope:** Local R11D extended drift and combined fresh+drift results.

## 1. Inputs Reviewed

- `outputs/R11D_EXTENDED_DRIFT_SUMMARY_20260429.md`
- `outputs/R11D_FRESH_DRIFT_SUMMARY_20260429.md`
- Six corrected local UnitCell checkpoints:
  - `r11d_7_pcm_4bit_seed123`
  - `r11d_7_pcm_4bit_seed456_clean`
  - `r11d_7_pcm_4bit_seed789`
  - `r11d_5a_pcm_seed123`
  - `r11d_5a_pcm_seed456`
  - `r11d_5a_pcm_seed789`

## 2. Result Review

### Extended drift, 0s to 3d

| Config | 0s | 1h | 1d | 3d | Drop 0s->3d |
|---|---:|---:|---:|---:|---:|
| 4-bit PCM | 76.63 ± 0.39% | 74.17 ± 0.42% | 72.60 ± 0.78% | 71.85 ± 0.81% | -4.78pp |
| 8-bit PCM | 77.60 ± 0.69% | 77.62 ± 0.57% | 77.56 ± 0.58% | 77.70 ± 0.53% | +0.10pp |

### Combined fresh+drift

| Config | 0s | 1h | 1d | Drop 0s->1d |
|---|---:|---:|---:|---:|
| 4-bit PCM | 76.67 ± 0.37% | 74.21 ± 0.38% | 72.68 ± 0.69% | -3.99pp |
| 8-bit PCM | 77.59 ± 0.66% | 77.57 ± 0.60% | 77.51 ± 0.67% | -0.08pp |

## 3. Technical Judgment

1. **4-bit PCM is trainable and fresh-stable, but retention-limited.** The degradation is smooth and monotonic enough to support a precision-drift trade-off narrative, not a noisy artifact.
2. **8-bit PCM is the deployment-safe reference.** Across 3 days it is effectively flat within measurement noise.
3. **Combined fresh+drift validates the evaluation stack.** Matched points differ from extended drift by <0.2pp, so no immediate pipeline conflict is visible.
4. **No more UnitCell repeat seeds are needed now.** The 3-seed table plus extended/fresh+drift closure is sufficient for the current claim.

## 4. Remaining Local Questions

The next local GPU work should answer these, in order:

1. **Preset dependence:** Does `PCMPresetDevice` reproduce the UnitCell story or expose device-model sensitivity?
2. **Training-noise necessity:** Does clean no-modifier training really stay near ~61%, or was the old oracle diagnostic contaminated?
3. **6-bit Pareto bridge:** Is there a midpoint between 4-bit retention-limited and 8-bit drift-safe?

## 5. Assigned Local Queue

See `report_md/_gpt/KIMI_LOCAL_GPU_QUEUE_20260430.md`.

Execution order:

1. Batch B/C script:
   - `bash paper2_aihwkit_baseline/run_kimi_r11d_batch_bc_20260430.sh`
2. Optional Batch D pilot:
   - `bash paper2_aihwkit_baseline/run_kimi_r11d_6bit_pilot_20260430.sh`

## 6. Paper-Facing Status

Ready to use with caveat:

> PCM device physics enable stable 4-bit training and fresh-instance transfer, but 4-bit retention drift creates an explicit deployment trade-off. 8-bit PCM is drift-safe under the tested 3-day window.

Not yet ready:

- Generalizing beyond `PCMPresetUnitCell`.
- Claiming modifier noise is necessary under clean provenance.
- Claiming a 6-bit Pareto optimum.
