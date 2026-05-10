# Codex Local R11D 6-bit 3-Seed Result — 2026-04-30

## Status

Completed artifacts exist for:

- `r11d_6bit_pcm_seed123`
- `r11d_6bit_pcm_seed456`
- `r11d_6bit_pcm_seed789`

Each has:

- `training_history.json`
- `fresh_eval.json`
- `drift_eval.json`

A diagnostic rerun is now active:

- `r11d_6bit_pcm_seed456_full100`
- Same config as seed456, but `--early-stop-patience 0` to force full 100 epochs.
- Log: `paper2_aihwkit_baseline/logs/r11d_6bit_pcm_seed456_full100_20260430_180342.log`

## 1. Raw 6-bit Results

| run_id | seed | epochs run | best epoch | best test | fresh mean ± std | drift 0s | drift 1h | drift 1d | 0s→1d drop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `r11d_6bit_pcm_seed123` | 123 | 100 | 97 | 77.33% | 77.3598 ± 0.0404% | 77.35% | 77.26% | 77.19% | 0.16pp |
| `r11d_6bit_pcm_seed456` | 456 | 56 | 46 | 69.07% | 69.0750 ± 0.0241% | 68.97% | 69.06% | 68.92% | 0.05pp |
| `r11d_6bit_pcm_seed789` | 789 | 100 | 100 | 77.81% | 77.7520 ± 0.0357% | 77.69% | 77.75% | 77.65% | 0.04pp |

## 2. 3-Seed Statistics

| Metric | Mean | Std |
|---|---:|---:|
| Source best | 74.7367% | 4.9133pp |
| Fresh eval | 74.7289% | 4.9004pp |
| Drift 0s | 74.6700% | 4.9393pp |
| Drift 1h | 74.6900% | 4.8819pp |
| Drift 1d | 74.5867% | 4.9129pp |
| Mean drift drop 0s→1d | 0.0833pp | — |

## 3. Comparison With Existing 4-bit / 8-bit PCM UnitCell

| Precision | Fresh mean | Fresh std across seeds | Drift 0s mean | Drift 1d mean | Drift drop |
|---|---:|---:|---:|---:|---:|
| 8-bit | 77.5953% | 0.6392pp | 77.6133% | 77.5733% | 0.0400pp |
| 6-bit | 74.7289% | 4.9004pp | 74.6700% | 74.5867% | 0.0833pp |
| 4-bit | 76.6836% | 0.3737pp | 76.6433% | 72.6367% | 4.0066pp |

## 4. Interpretation

The 6-bit line is mixed:

1. **Drift behavior is excellent.** Across all three seeds, 6-bit is essentially drift-flat at 1 day, comparable to 8-bit and much better than 4-bit.
2. **Seed123 and seed789 are strong.** Both are at or above 77.3% fresh and validate the 6-bit Pareto intuition.
3. **Seed456 is a major instability event.** It reaches only 69.07% best test and dominates the 3-seed std.
4. **The current 6-bit 3-seed mean cannot be presented as a clean precision midpoint.** With seed456 included, 6-bit underperforms 4-bit in mean accuracy, despite better drift.
5. **The key unresolved question is whether seed456 is a true bad basin or an early-stop artifact.** seed456 stopped at epoch 56 after best epoch 46; seed789 kept improving all the way to epoch 100.

## 5. Seed456 Training-Curve Note

Seed456 last 20 epochs are unstable, not smoothly converging:

```text
best epoch 46: test_acc=69.07%
epoch 49: 58.87%
epoch 51: 55.34%
epoch 55: 53.30%
epoch 56: 64.63%
```

This looks like a bad/noisy training basin. However, because seed789's late gains occur near epoch 87-100, a full 100-epoch seed456 rerun is needed before calling it a true seed failure.

## 6. Action Taken

Launched diagnostic rerun:

```bash
RUN=r11d_6bit_pcm_seed456_full100
python paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "$RUN" \
  --seed 456 \
  --epochs 100 \
  --batch-size 64 \
  --lr 0.001 \
  --wd 0.05 \
  --momentum 0.0 \
  --device cuda \
  --workers 0 \
  --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
  --log-interval 1 \
  --inp-res 0.015625 \
  --out-res 0.015625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 0 \
  --early-stop-min-delta 0.0
```

After training, the command chain will run fresh and drift eval automatically.

## 7. Decision Pending

Do not lock the 6-bit narrative until `r11d_6bit_pcm_seed456_full100` completes.

Possible outcomes:

| Outcome | Interpretation | Next action |
|---|---|---|
| seed456 recovers to ~76-78% | early stop was too aggressive / late recovery matters | update 6-bit as strong Pareto midpoint |
| seed456 remains ~69% | 6-bit has real seed/basin instability | do not make 6-bit central; use as opportunity/appendix with caveat |
| seed456 worsens/collapses | 6-bit unstable under current LR/noise | test lower LR or exclude from main line |

## 8. Artifact Paths

```text
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/   # running
```
