# ResNet Checkpoint Audit — 2026-04-16

## Scope

Audit of the saved ResNet-18 checkpoints using the same `build_model -> strict load -> evaluate`
path as training, with `num_workers=0` to avoid sandbox multiprocessing issues.

## Original reproduction command

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_resnet18_checkpoints.py \
  --num-workers 0 \
  --output /tmp/resnet_eval_summary.json
```

## Results

| Checkpoint | Expected best_acc | Re-eval acc | Verdict |
|:--|--:|--:|:--|
| `checkpoints/R1_FP32_baseline_best.pt` | 95.46% | 95.46% | OK |
| `checkpoints/R2_4bit_no_noise_best.pt` | 94.12% | 10.00% | Mismatch |
| `checkpoints/R4_4bit_noise_HAT_best.pt` | 90.37% | 10.00% | Mismatch |
| `checkpoints/resnet18_cifar100/R1_FP32_baseline_best.pt` | 78.64% | 78.64% | OK |
| `checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt` | 1.00% | 1.00% | OK |

## Additional isolation

Using `checkpoints/R4_4bit_noise_HAT_best.pt` on CIFAR-10:

| Evaluation mode | Accuracy |
|:--|--:|
| Analog noisy | 10.00% |
| Analog clean (`noise_enabled=False`, `sigma_c2c=0`, `sigma_d2d=0`) | 10.00% |
| Extracted effective digital weights | 10.00% |

## Root cause update

The earlier mismatch was caused by a legacy checkpoint compatibility bug, not by corrupted weights.

- The older CIFAR-10 analog ResNet checkpoints do not serialize `restore_weight_scale` in `exp_cfg`.
- The current `ExperimentConfig` default is `restore_weight_scale=True`.
- The analog layer default used by the original ResNet pipeline was `restore_weight_scale=False`.
- Reconstructing the config with the current default therefore changes the inference path at load time.

Direct verification:

| Checkpoint | `restore_weight_scale=True` | `restore_weight_scale=False` |
|:--|--:|--:|
| `checkpoints/R2_4bit_no_noise_best.pt` | 10.00% | 94.12% |
| `checkpoints/R4_4bit_noise_HAT_best.pt` | 10.00% | 90.25% |

This reproduces the full collapse and the recovery with a single config bit. The saved analog weights are valid; the loader fallback was wrong for legacy checkpoints.

## Fix

- Added `load_experiment_config_from_checkpoint()` to `train_resnet18.py`.
- If a checkpoint is missing `restore_weight_scale`, the loader now falls back to `False` for backward compatibility.
- Updated `eval_resnet18_checkpoints.py` and the ResNet debug scripts to use the compatibility loader.

## Post-fix validation

Command:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_resnet18_checkpoints.py \
  --num-workers 0 \
  --output /tmp/resnet_eval_summary_after_fix.json
```

Results:

| Checkpoint | Expected best_acc | Re-eval acc | Verdict |
|:--|--:|--:|:--|
| `checkpoints/R1_FP32_baseline_best.pt` | 95.46% | 95.46% | OK |
| `checkpoints/R2_4bit_no_noise_best.pt` | 94.12% | 94.12% | OK |
| `checkpoints/R4_4bit_noise_HAT_best.pt` | 90.37% | 89.60% | Near-match |
| `checkpoints/resnet18_cifar100/R1_FP32_baseline_best.pt` | 78.64% | 78.64% | OK |
| `checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt` | 1.00% | 1.00% | OK |

The remaining `0.77 pp` gap on CIFAR-10 `R4` is consistent with Monte Carlo variation from analog noise during evaluation and is no longer a catastrophic load failure.

## Superseded conclusion

The original conclusion below is preserved as the pre-fix audit snapshot:

- `R1` loads and evaluates correctly.
- `R2` and `R4` both collapse after strict load.
- `R4` remains collapsed even when all analog noise is disabled.
- The extracted effective digital weights also collapse.

This narrows the problem to checkpoint/state incompatibility for the analog ResNet path, or to an earlier training/save-time mismatch that produced a checkpoint whose stored `best_acc` does not match the saved weights.

## Artifacts

- Script used: [eval_resnet18_checkpoints.py](/home/qiaosir/projects/compute_vit/eval_resnet18_checkpoints.py)
- Pre-fix JSON summary: `/tmp/resnet_eval_summary.json`
- Post-fix JSON summary: `/tmp/resnet_eval_summary_after_fix.json`
