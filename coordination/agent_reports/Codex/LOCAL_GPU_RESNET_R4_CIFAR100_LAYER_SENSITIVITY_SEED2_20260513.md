# Local GPU ResNet R4 CIFAR-100 Layer Sensitivity Seed-2 Report

Date: 2026-05-13 21:07 CST
Owner: Codex
Evidence grade: provisional

## Goal

Run an independent second D2D-seed layer-sensitivity ranking for the repaired ResNet-18 CIFAR-100 R4 checkpoint, to test whether the previously observed sensitive-layer ordering is stable enough to remain useful for architecture-generality discussion.

## Command

```bash
/home/qiaosir/miniconda3/bin/python scripts/eval_resnet_layer_sensitivity.py \
  --experiment R4 \
  --dataset cifar100 \
  --batch_size 128 \
  --layer_seeds 3 \
  --base_seed 20260514 \
  --device cuda \
  --raw_out thesis/results/cnn_vs_vit_hat/resnet_r4_cifar100_layer_sensitivity_seed2_raw_20260513_210401.tsv \
  --summary_out thesis/results/cnn_vs_vit_hat/resnet_r4_cifar100_layer_sensitivity_seed2_summary_20260513_210401.tsv
```

Log:

- `logs/resnet_r4_cifar100_layer_sensitivity_seed2_20260513_210401.log`

## Outputs

- Raw TSV:
  `thesis/results/cnn_vs_vit_hat/resnet_r4_cifar100_layer_sensitivity_seed2_raw_20260513_210401.tsv`
- Summary TSV:
  `thesis/results/cnn_vs_vit_hat/resnet_r4_cifar100_layer_sensitivity_seed2_summary_20260513_210401.tsv`

## Key numbers

- Baseline accuracy mean: `69.92%`
- Top-5 sensitive layers in this replicate:
  1. `layer2.0.conv2` `8.0033 pp`
  2. `layer1.0.conv1` `7.7967 pp`
  3. `layer3.0.conv1` `5.8367 pp`
  4. `layer4.1.conv1` `5.5800 pp`
  5. `conv1` `5.0733 pp`

## Stability against the first ResNet CIFAR-100 run

Reference first run:

- `thesis/results/cnn_vs_vit_hat/resnet_r4_layer_sensitivity_summary_20260512_165300.tsv`

Comparison:

- First-run baseline: `70.36%`
- Second-run baseline: `69.92%`
- Top-5 overlap: `4/5`
- Pearson correlation of per-layer mean accuracy drop across all 21 analog layers: `0.9717`

First-run top-5:

1. `layer1.0.conv1` `9.1367 pp`
2. `layer2.0.conv2` `7.7700 pp`
3. `layer3.0.conv1` `6.1067 pp`
4. `layer4.1.conv1` `5.8600 pp`
5. `layer1.1.conv2` `5.1300 pp`

Interpretation:

- The same four layers remain in the top-5 across both runs: `layer1.0.conv1`, `layer2.0.conv2`, `layer3.0.conv1`, `layer4.1.conv1`.
- Ordering between the two most sensitive layers swaps, but the sensitive set is stable.
- `conv1` replaces `layer1.1.conv2` in the second run, so the lower edge of the top-5 remains seed-sensitive.

## Verdict

This replicate strengthens the claim that ResNet-18 CIFAR-100 under R4 has a stable high-sensitivity core rather than a fully random layer ranking, but the evidence remains provisional because it is still one repaired checkpoint with repeated D2D resampling rather than a multi-checkpoint architecture study.
