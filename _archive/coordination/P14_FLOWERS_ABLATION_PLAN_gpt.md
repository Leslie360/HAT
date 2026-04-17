# P14 Flowers-102 Noise-Magnitude Ablation Plan

## Goal

Provide the smallest defensible ablation for the reviewer concern that Flowers-102 HAT failure was never tested against a lower-noise control.

The minimal useful comparison is:

- existing Flowers-102 baseline: `V1` digital FP32
- existing Flowers-102 standard-noise anchor: `V3`
- existing Flowers-102 standard HAT result: `V4`
- new Flowers-102 zero-noise / near-zero-noise control: `V2`

That gives a direct noise-magnitude story without opening a large hyperparameter search.

## Recommended Design

1. Run `Tiny-ViT` on `Flowers-102` with `V2` only.
2. Use the same paper-facing recipe as the existing Flowers-102 runs:
   - dataset: `flowers102`
   - experiment: `V2`
   - pretrained: `True`
   - epochs: `100`
   - batch size: `64`
   - AMP: enabled if stable
3. Compare the new `V2` control against the already-locked `V3` and `V4` numbers.

Why this is defensible:

- `V2` is the `sigma -> 0` endpoint of the exact same hybrid stack.
- `V3/V4` already show the standard-noise regime.
- The reviewer gap is not "run another big benchmark"; it is "show at least one lower-noise control."

## Exact Commands

Single-seed pilot, recommended first run:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/train_tinyvit.py \
  --dataset flowers102 \
  --experiment V2 \
  --epochs 100 \
  --batch-size 64 \
  --seed 42 \
  --pretrained \
  --amp \
  --save-dir /home/qiaosir/projects/compute_vit/checkpoints/_gpt/flowers102_ablation \
  --num-workers 4 \
  2>&1 | tee /home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_flowers102_v2_ablation_s42_gpt.log

/home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/train_tinyvit.py \
  --dataset flowers102 \
  --experiment V2 \
  --mode eval \
  --batch-size 64 \
  --seed 42 \
  --pretrained \
  --amp \
  --checkpoint /home/qiaosir/projects/compute_vit/checkpoints/_gpt/flowers102_ablation/V2_hybrid_no_noise_best.pt \
  --eval-runs 10 \
  2>&1 | tee /home/qiaosir/projects/compute_vit/logs/_gpt/eval_tinyvit_flowers102_v2_ablation_s42_gpt.log
```

If GPU time allows, repeat the same pair for seeds `123` and `2026`.

## Reusable Assets

- Training script: `/home/qiaosir/projects/compute_vit/train_tinyvit.py`
- Existing Flowers-102 anchors:
  - `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/flowers102/V1_fp32_digital_baseline_best.pt`
  - `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/flowers102/V3_hybrid_standard_noise_standard_train_best.pt`
  - `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/flowers102/V4_hybrid_standard_noise_hat_best.pt`
- Existing Flowers-102 result file:
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json`
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/csv_gpt/tinyvit_flowers102_v134_results_gpt.csv`

## File Paths to Touch If We Extend the Ablation

No code changes are required for the minimal `V2` control run.

If we later want a true multi-point sigma sweep, the only likely code change is:

- `/home/qiaosir/projects/compute_vit/train_tinyvit.py`

to add command-line overrides for `sigma_c2c` / `sigma_d2d` and optionally `noise_mode`.

## Intended Paper Use

The result should be written as a bounded ablation, not as proof of causality:

- `V2` tells us whether the failure is already present when analog noise is removed.
- `V3/V4` tell us how much the standard noise regime changes the outcome.
- Together they support the existing `low-data boundary` framing without overclaiming universal data starvation.
