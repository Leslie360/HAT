# TX-14 Table 2 Evidence — 2026-04-17

## Scope

This note answers the numeric-source questions raised in `CODEX_DISPATCH_20260417_fix_gpt.md` for `paper/latex_gpt/sections/05_results.tex`.

## Direct Answers First

### V2 vs V3 on CIFAR-10

- `V2` checkpoint-best training accuracy (`quantize-only`, no noise during train/eval in the training run):
  - `97.38%`
  - Sources:
    - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L16)
    - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L20)

- `V2` under canonical-noise evaluation (`sigma_c2c=5%`, `sigma_d2d=10%`, 10 eval runs):
  - `97.39% ± 0.00%`
  - Sources:
    - [v2_under_noise_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v2_under_noise_results_gpt.json#L17)

- `V3` checkpoint-best CIFAR-10 accuracy (`canonical noise active`, no HAT):
  - `89.54%`
  - Sources:
    - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L44)
    - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L46)

Conclusion:

- `97.39%` belongs to `V2 under canonical-noise evaluation`, not to `V3`.
- `V3` on CIFAR-10 is `89.54%`.
- So the old Table 2 `V3 = 97.39 ± 0.05%` entry was a label/value mix-up.

## Per-Row Evidence

### 1. ResNet-18 FP32 CIFAR-10: `94.98%` -> `95.46%`

- Source used:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L10)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L133)
  - [RESNET_CHECKPOINT_AUDIT_20260416.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md#L74)

Interpretation:

- `95.46%` is the recorded best / replayed value for `R1`.
- The earlier `94.98%` in `05_results.tex` did not match the locked ResNet audit artifacts.

### 2. ResNet-18 R3 CIFAR-10: `17.34 ± 0.15%` -> `16.48%`

- Source used:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L36)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L135)

Clarification:

- `16.48%` is the checkpoint-best value.
- `17.30 ± 0.26%` is the Monte Carlo evaluation summary for the same regime.
- I removed `±` because I normalized grouped cross-dataset rows to best-checkpoint values to follow [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md#L27), which says grouped bars / main cross-dataset narrative should use best-checkpoint values rather than MC means.

### 3. ResNet-18 R4 CIFAR-10: `91.23 ± 0.12%` -> `90.37%`

- Source used for `90.37%`:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L49)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L136)

- Source for the post-fix replay value in discussion:
  - [RESNET_CHECKPOINT_AUDIT_20260416.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md#L76)

Clarification:

- `90.37%` is the original checkpoint-best value.
- `89.60%` is the later post-fix replay value from the compatibility-loader audit.
- This is a real semantic mismatch between `best checkpoint` and `post-fix reevaluation`, not a missing source.

### 4. Tiny-ViT V3 CIFAR-10: `97.39 ± 0.05%` -> `89.54%`

- Source used:
  - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L45)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L46)
  - [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md#L20)

Clarification:

- `97.39%` is the canonical-noise evaluation result for `V2`, documented in [v2_under_noise_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v2_under_noise_results_gpt.json#L19).
- It should not appear in the `V3` row.
- So the `V3 -> 89.54%` correction was a label correction, not a silent value substitution.

### 5. Tiny-ViT V4 CIFAR-10: `97.52 ± 0.05%` -> `91.94%`

- Source used:
  - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L73)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L72)
  - [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md#L20)

- Separate source for the 10-run MC re-evaluation of the single canonical V4 checkpoint:
  - [\_codex\_verify\_v4\_canonical\_eval\_cuda\_20260407.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.json#L22)
  - This gives `91.69 ± 0.23%`.

Clarification:

- `91.94%` is the checkpoint-best value for the canonical single V4 run.
- `87.95 ± 0.27%` is the later three-seed aggregate for a different statistic family and is already documented separately in the supplement / lock files.
- `97.52 ± 0.05%` does not match either the canonical best-checkpoint family or the canonical MC family for V4 CIFAR-10.

## Current Assessment

The underlying issue is not missing provenance. It is that the previous Table 2 mixed three different statistic families:

1. checkpoint-best values
2. single-checkpoint Monte Carlo means
3. later multi-seed aggregates

The `V3=97.39` entry is the clearest hard error because it is actually a `V2` number.

The remaining decision is editorial:

- either keep Table 2 as a best-checkpoint cross-dataset table and then align the ResNet discussion wording to that convention
- or revert the table to MC-style rows and make the caption explicit about mixing regimes

At minimum, `R4 90.37` in the table and `R4 89.60` in discussion should no longer coexist without explanation.
