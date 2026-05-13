# Local GPU ResNet R4 CIFAR-100 TopK Protection Seed-2 Report

Date: 2026-05-13 21:13 CST
Owner: Codex
Evidence grade: provisional

## Goal

Use the second-seed ResNet R4 CIFAR-100 layer-sensitivity ranking to test whether the protection-budget curve remains stable under a fresh set of D2D instances.

## Command

```bash
/home/qiaosir/miniconda3/bin/python scripts/eval_resnet_retention_protection.py \
  --experiment R4 \
  --dataset cifar100 \
  --checkpoint_path checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt \
  --sensitivity_tsv thesis/results/cnn_vs_vit_hat/resnet_r4_cifar100_layer_sensitivity_seed2_summary_20260513_210401.tsv \
  --k_values 0,5,10,15,21 \
  --retention_times 0 \
  --num_instances 10 \
  --mc_runs 3 \
  --batch_size 128 \
  --device cuda \
  --base_seed 20260514 \
  --tsv_out thesis/results/cnn_vs_vit_hat/resnet_r4_topk_protection_seed2_raw_20260513_211016.tsv \
  --summary_out thesis/results/cnn_vs_vit_hat/resnet_r4_topk_protection_seed2_summary_20260513_211016.tsv
```

Log:

- `logs/resnet_r4_cifar100_topk_protection_seed2_20260513_211016.log`

## Outputs

- Raw TSV:
  `thesis/results/cnn_vs_vit_hat/resnet_r4_topk_protection_seed2_raw_20260513_211016.tsv`
- Summary TSV:
  `thesis/results/cnn_vs_vit_hat/resnet_r4_topk_protection_seed2_summary_20260513_211016.tsv`

## Summary

Fresh-only (`retention_time_s=0`) protection curve:

- `fresh_all_analog`: `2.9790±0.8467%`
- `freeze_top5_d2d`: `13.8810±2.0330%`
- `freeze_top10_d2d`: `43.0057±1.7754%`
- `freeze_top15_d2d`: `64.3057±0.5977%`
- `freeze_top21_d2d`: `69.9747±0.2279%`

The repaired checkpoint baseline in the paired layer-sensitivity run was `69.92%`, so top21 fully restores source-D2D performance and top15 recovers most of the gap.

## Comparison to the first ResNet CIFAR-100 topK run

Reference first run:

- `thesis/results/cnn_vs_vit_hat/resnet_r4_retention_protection_summary_20260512_165557.tsv`

First run:

- `fresh_all`: `3.09±0.65%`
- `top5`: `13.99±4.99%`
- `top10`: `40.50±2.93%`
- `top15`: `64.14±0.34%`
- `top21`: `69.96±0.15%`

Second run:

- `fresh_all`: `2.98±0.85%`
- `top5`: `13.88±2.03%`
- `top10`: `43.01±1.78%`
- `top15`: `64.31±0.60%`
- `top21`: `69.97±0.23%`

## Verdict

The protection-budget curve is stable across the second seed. The main conclusion does not move: ResNet-18 CIFAR-100 under R4 still needs a large protection budget, with top5 far from enough, top10 partially useful, and top15 already restoring most accuracy. This remains provisional because it is still one repaired checkpoint family, but it is materially stronger than a single-run curve.
