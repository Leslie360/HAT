# TX-14 Table 2 Response — 2026-04-17

## Direct answers to the blocking questions

### V2 vs V3 on CIFAR-10

- `V2` (`quantize-only`, no noise in the training run) checkpoint-best CIFAR-10 accuracy:
  - `97.38%`
  - Sources:
    - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L16)
    - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L20)

- `V2` under canonical-noise evaluation (`sigma_c2c=5%`, `sigma_d2d=10%`, 10 eval runs):
  - `97.39% ± 0.00%`
  - Source:
    - [v2_under_noise_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v2_under_noise_results_gpt.json#L17)

- `V3` (`canonical noise active`, no HAT) checkpoint-best CIFAR-10 accuracy:
  - `89.54%`
  - Sources:
    - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L44)
    - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L46)

Conclusion:

- `97.39%` is a `V2 under canonical-noise evaluation` number.
- `89.54%` is the actual `V3` checkpoint-best CIFAR-10 number.
- Therefore the old `V3 = 97.39 ± 0.05%` row was a label/value mix-up rather than evidence that V3 remained near-noiseless on CIFAR-10.

## Per-row provenance for the challenged edits

### ResNet-18 FP32 CIFAR-10: `94.98%` -> `95.46%`

- Sources:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L10)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L133)
  - [RESNET_CHECKPOINT_AUDIT_20260416.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md#L74)

Interpretation:

- `95.46%` is the recorded best / replayed value for `R1`.

### ResNet-18 R3 CIFAR-10: `17.34 ± 0.15%` -> `16.48%`

- Sources:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L36)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L135)

Interpretation:

- `16.48%` is the checkpoint-best value.
- `17.30 ± 0.26%` is the Monte Carlo summary for the same regime.
- The `±` disappeared because the table was normalized to checkpoint-best values.

### ResNet-18 R4 CIFAR-10: `91.23 ± 0.12%` -> `90.37%`

- Sources for `90.37%`:
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json#L49)
  - [train_resnet18_full_20260403_095144.log](/home/qiaosir/projects/compute_vit/logs/train_resnet18_full_20260403_095144.log#L136)

- Source for the post-fix replay value in the discussion:
  - [RESNET_CHECKPOINT_AUDIT_20260416.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md#L76)

Interpretation:

- `90.37%` is the original checkpoint-best value.
- `89.60%` is the later post-fix replay value after the compatibility-loader audit.
- This is a statistic-family mismatch, not a missing-source problem.

### Tiny-ViT V3 CIFAR-10: `97.39 ± 0.05%` -> `89.54%`

- Sources:
  - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L44)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L46)
  - [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md#L20)

Interpretation:

- `97.39%` belongs to `V2 under canonical-noise evaluation`.
- `89.54%` is the correct `V3` checkpoint-best value.

### Tiny-ViT V4 CIFAR-10: `97.52 ± 0.05%` -> `91.94%`

- Sources:
  - [train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log](/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v2v7_ampfix_20260404_231605_driver_gpt.log#L73)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json#L72)
  - [CANONICAL_RESULT_LOCK_gpt.md](/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md#L20)

- Separate MC source for the same canonical single V4 checkpoint:
  - [\_codex\_verify\_v4\_canonical\_eval\_cuda\_20260407.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.json#L22)
  - `91.69 ± 0.23%`

Interpretation:

- `91.94%` is the checkpoint-best value.
- `87.95 ± 0.27%` is a later three-seed aggregate from a different statistic family.
- `97.52 ± 0.05%` does not match the canonical best-checkpoint family or the canonical MC family for V4 CIFAR-10.

## Editorial resolution adopted in the manuscript

- Keep Table `tab:result-summary` as a checkpoint-best cross-dataset table, consistent with its current caption.
- Keep `V3 = 89.54%` and `V4 = 91.94%` in that table.
- Preserve the discussion-side `89.60%` only as a post-fix replay value, and explicitly explain the difference from the `90.37%` checkpoint-best number so the two values do not coexist without context.

## Status

- TX-15 citation patch already landed in [01_introduction.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/01_introduction.tex#L7).
- The manuscript now includes an explicit explanation of the `R4 90.37%` vs `89.60%` distinction in [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex).
