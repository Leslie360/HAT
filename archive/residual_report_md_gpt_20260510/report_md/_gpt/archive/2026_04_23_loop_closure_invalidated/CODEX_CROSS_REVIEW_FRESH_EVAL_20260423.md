# Codex Cross-Review: Post-Fix Ensemble HAT Fresh Eval

Date: 2026-04-23 CST

Scope: independent verification of `postfix_ensemble_hat_v4_nl20_fresh_eval.json`, the evaluation path, checkpoint metadata, arithmetic, and comparison against the R1 fresh-instance baseline.

All paths below are relative to `/home/qiaosir/projects/compute_vit`.

## Reviewed Artifacts

| Artifact | Status | Notes |
|:---|:---|:---|
| `report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json` | Found | SHA256 `07663a2ee84b688fa4b7911294f185d5081da2a92452964114e10383c9c1a337`; modified `2026-04-23 23:45:24 +0800` |
| `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt` | Found | SHA256 `a897e9f043c3081f0ad5729894026062bd0000d38e9e2ffb510e7d75df4d8cfa`; modified `2026-04-23 23:33:40 +0800` |
| `logs/_gpt/postfix_ensemble_hat_fresh_eval.log` | Found | Log instance accuracies match the JSON rounded display |
| `run_postfix_eval.sh` | Found, untracked | Launch command passes `--nl-ltp 2.0 --nl-ltd -2.0 --noise-mode uniform` |
| `eval_fresh_instances_postfix.py` | Found, untracked | Evaluator pushes NL overrides into module configs before fresh D2D resampling |

Note: The same relative JSON/checkpoint paths do not exist under `/home/qiaosir/projects` directly; the valid artifact root is `compute_vit/`.

## JSON Verification

The JSON records:

- checkpoint: `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt`
- experiment: `V4`
- protocol: `10` fresh instances x `5` MC runs per instance
- NL settings: `nl_ltp=2.0`, `nl_ltd=-2.0`
- noise mode: `uniform`
- instance means:
  `[80.086, 82.106, 81.658, 81.770, 82.494, 81.322, 82.402, 81.802, 81.568, 81.740]`

These match the reported rounded accuracies:

`[80.09, 82.11, 81.66, 81.77, 82.49, 81.32, 82.40, 81.80, 81.57, 81.74]`

The fresh-eval log also matches the JSON:

- mean: `81.6948%`
- std: `0.6381%`
- range: `80.09--82.49%`

## Independent Arithmetic

From the JSON `instance_means`:

| Statistic | Value |
|:---|---:|
| N | `10` |
| Mean | `81.694800000000%` |
| Population std, ddof=0 | `0.638104818976%` |
| Sample std, ddof=1 | `0.672621537964%` |
| Min | `80.086000%` |
| Max | `82.494000%` |
| Range width | `2.408000 pp` |

The JSON `cross_instance_mean=81.6948` is correct.

The JSON `cross_instance_std=0.6381048189756912` is also correct, but it is the population standard deviation (`numpy.std`, `ddof=0`), not the sample standard deviation used by several other fresh-eval scripts in this repository.

## NL Evaluation Path

I found no evidence of an NL mismatch in this post-fix fresh eval.

Evidence:

- `run_postfix_eval.sh` passes `--nl-ltp 2.0 --nl-ltd -2.0 --noise-mode uniform` to `eval_fresh_instances_postfix.py`.
- `eval_fresh_instances_postfix.py` overrides `cfg.nl_ltp` and `cfg.nl_ltd`, then pushes those values into every module with a `config` object via `module.config.NL_LTP` and `module.config.NL_LTD`.
- The later call to `set_uniform_noise(...)` only updates `noise_enabled`, `sigma_c2c`, `sigma_d2d`, and `noise_mode`; it does not overwrite NL values.
- The checkpoint metadata itself also contains `exp_cfg.nl_ltp=2.0` and `exp_cfg.nl_ltd=-2.0`.

Conclusion: the eval script path used correct NL values (`2.0`, `-2.0`) for this JSON.

## Checkpoint Metadata

Loaded checkpoint metadata from `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt`:

| Field | Value |
|:---|:---|
| `epoch` | `41` |
| `best_epoch` | `41` |
| `best_acc` | `82.26` |
| `dataset` | `cifar10` |
| `num_classes` | `10` |
| `amp_enabled` | `True` |
| state dict keys | `338` |
| classifier shape | `(10, 320)` |

Checkpoint `exp_cfg`:

| Field | Value |
|:---|:---|
| `name` | `V4_hybrid_standard_noise_hat` |
| `use_hybrid` | `True` |
| `n_states` | `16` |
| `nl_ltp` / `nl_ltd` | `2.0` / `-2.0` |
| `sigma_c2c` / `sigma_d2d` | `0.05` / `0.10` |
| `noise_mode` | `uniform` |
| `noise_enabled` | `True` |
| `hat_training` | `True` |
| `adc_bits` | `8` |
| `epochs` | `100` |
| `batch_size` | `64` |
| `lr` / `weight_decay` | `0.0005` / `0.05` |

The training code implements epoch-resampled D2D for HAT by calling `resample_all_d2d_noise(model)` at the start of every epoch when `exp_cfg.hat_training` is true. The log confirms the run resampled `42` analog modules.

Critical discrepancy: the prompt and broadcast claim `epoch 10` and same-instance best `81.72%`, but the current checkpoint metadata says `best_epoch=41` and `best_acc=82.26%`.

The checkpoint history explains the likely source of the stale claim:

| Epoch | Test Acc |
|---:|---:|
| `10` | `80.67%` |
| `37` | `81.72%` |
| `41` | `82.26%` |

Therefore:

- The evaluated checkpoint is not an epoch-10 checkpoint.
- `81.72%` is present in history, but at epoch `37`, not epoch `10`.
- The actual checkpoint best is `82.26% @ epoch 41`.
- If comparing fresh to the current checkpoint's same-instance best, the gap is `82.26 - 81.6948 = 0.5652 pp`, not `0.03 pp`.

## R1 Comparison

R1 source checked: `report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json`.

R1 values:

- fresh mean: `34.5612%`
- std in JSON: `8.787805247424789%`
- instance range: `22.986%--49.614%`
- std convention: sample std (`ddof=1`)

Post-fix Ensemble HAT values:

- fresh mean: `81.6948%`
- population std in JSON: `0.6381048189756912%`
- sample std: `0.6726215379642054%`
- instance range: `80.086%--82.494%`

Comparison:

| Metric | R1 | Post-fix Ensemble HAT | Delta |
|:---|---:|---:|---:|
| Fresh mean | `34.5612%` | `81.6948%` | `+47.1336 pp` |
| Fresh std, JSON as reported | `8.7878%` | `0.6381%` | `-8.1497 pp` |
| Fresh std, same sample convention | `8.7878%` | `0.6726%` | `-8.1152 pp` |
| Min instance mean | `22.986%` | `80.086%` | `+57.100 pp` |
| Max instance mean | `49.614%` | `82.494%` | `+32.880 pp` |

Every post-fix Ensemble HAT instance mean is above the best R1 instance mean.

## Discrepancies And Concerns

1. Major provenance discrepancy: checkpoint epoch and same-instance best do not match the claim.

The artifact currently at `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt` is `best_epoch=41`, `best_acc=82.26%`, not epoch 10 / `81.72%`. Do not cite the result as "epoch 10" or "same-instance best 81.72%" unless an older frozen checkpoint is restored and re-evaluated.

2. Std convention mismatch against R1.

The post-fix evaluator uses `np.std(instance_accs)` with default `ddof=0`, while R1's `cross_instance_std=8.7878%` is sample std (`ddof=1`). This does not change the conclusion, but it is not an apples-to-apples uncertainty convention. For consistency with R1 and the paper protocol, report post-fix std as `0.6726%` if using sample std, or explicitly label `0.6381%` as population std.

3. JSON is minimal and omits useful provenance.

Unlike `r1_clean_anchor_fresh_eval.json`, this JSON does not include `train_best_acc`, `train_best_epoch`, per-instance raw MC accuracies, per-instance MC std, dataset, num classes, or resampled module count. The log and checkpoint fill some gaps, but the JSON alone is insufficient for long-term audit.

4. Reproducibility hazard: evaluator and launcher are untracked.

`eval_fresh_instances_postfix.py` and `run_postfix_eval.sh` are currently untracked in git. The checkpoint also does not store a git commit hash or run command. Although `git rev-parse --short HEAD` returns `33bed9c`, the worktree is dirty. The "clean code" claim should be treated as a process claim, not fully recoverable from committed artifacts alone, until the evaluator/launcher are committed or archived with checksums.

5. The headline conclusion remains numerically strong, but cite it with corrected provenance.

The fresh-eval JSON supports `81.6948%` fresh mean over `10 x 5` evaluation under `NL_LTP=2.0`, `NL_LTD=-2.0`, uniform noise. However, the safe phrasing is:

`Post-fix Ensemble HAT, NL=(2.0,-2.0), checkpoint metadata best_acc=82.26% @ epoch 41, fresh-instance mean=81.6948%, population std=0.6381% (sample std=0.6726%), range=80.086--82.494%.`

## Verdict

The fresh-eval arithmetic and NL settings pass cross-review. The comparison against R1 is strongly favorable.

The provenance claim does not pass as written: the evaluated checkpoint metadata contradicts "epoch 10" and "same-instance best 81.72%". Correct the broadcast/report wording, standardize the std convention, and archive or commit the exact evaluator before treating this as a cite-ready safety-critical result.
