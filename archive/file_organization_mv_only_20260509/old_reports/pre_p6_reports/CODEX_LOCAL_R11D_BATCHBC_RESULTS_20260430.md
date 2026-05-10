# Codex Local R11D Batch B/C Results

**Date:** 2026-04-30 10:20 CST
**Codex raw-artifact correction:** 2026-05-01. The table below has been updated to match the current `training_history.json`, `fresh_eval.json`, and `drift_eval.json` files. Earlier values in this report were stale after later reruns wrote the same artifact paths.
**Scope:** Local R11D Batch B/C after UnitCell 3-seed closure.
**Status:** COMPLETE. Optional 6-bit pilot launched after completion.

## 1. Completed Runs

| Batch | Run ID | Preset / mode | Precision | Seed | Best test | Final test | Fresh mean ± std | Drift 0s | Drift 1h | Drift 1d |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B | `t13v2_r11d_5a_pcm_PCMPresetDevice_seed123` | `PCMPresetDevice` | 8-bit | 123 | 76.88% | 76.84% | 76.8026 ± 0.0425% | 76.94% | 76.70% | 76.87% |
| B | `t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123` | `PCMPresetDevice` | 4-bit | 123 | 76.47% | 76.20% | 76.3798 ± 0.0407% | 76.37% | 74.72% | 73.19% |
| C | `r11d_5a_pcm_oracle_seed123_clean` | clean oracle, `modifier_std_dev=0.0` | 8-bit | 123 | 76.80% | 76.74% | 76.6994 ± 0.0488% | 76.94% | 76.66% | 76.67% |

## 2. Immediate Interpretation

1. **PCMPresetDevice does not collapse.** Both 8-bit and 4-bit PCMPresetDevice reproduce the UnitCell-level story at seed 123.
2. **Preset dependence is low for the headline.** 8-bit is drift-flat; 4-bit is trainable/fresh-stable but retention-limited.
3. **Clean oracle invalidates the old ~61% diagnostic.** With clean provenance, `modifier_std_dev=0.0` recovers to ~76.8%. The previous oracle diagnostic should be retracted as contaminated or non-comparable.
4. **Training-time ADD_NORMAL modifier is not necessary for 8-bit PCM source/fresh accuracy under this clean run.** Do not claim modifier noise is essential regularization based on the old oracle.
5. **4-bit precision-drift trade-off remains intact.** 4-bit `PCMPresetDevice` drops from 76.37% at 0s to 73.19% at 1d, while 8-bit stays flat.

## 3. Decision Update

Batch B/C closes two local questions:

- `PCMPresetDevice` is compatible with the PCM narrative.
- Old no-modifier oracle is invalid; clean oracle matches standard 8-bit PCM.

Next local GPU action per queue:

```bash
bash paper2_aihwkit_baseline/run_kimi_r11d_6bit_pilot_20260430.sh
```

The 6-bit pilot was launched after this review.

## 4. Artifact Paths

```text
paper2_aihwkit_baseline/checkpoints/t13v2_r11d_5a_pcm_PCMPresetDevice_seed123/
paper2_aihwkit_baseline/checkpoints/t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_oracle_seed123_clean/
```

Each completed run has:

```text
best.pt
last.pt
training_history.json
fresh_eval.json
drift_eval.json
```
