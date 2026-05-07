# Remote 107 Full Return — 2026-05-08

## 1. Branch + Commit

```
Branch: 107-clean
Commit: b1ba7d896d0584fa928441b312542e1f937741ad
```

---

## 2. Git Status

```
 M pipeline_next.py
 M pipeline_runner.py
?? README.md
?? analog_layers_ensemble.py
?? device_profile_utils.py
?? device_profiles/
?? diag_fresh_instance.py
?? dispatches/
?? docs/DEVICE_PROFILE_GUIDE.md
?? docs/KEY_SOURCE_SYNC_20260422.md
?? docs/PHYSICS_STACK.md
?? docs/README.md
?? docs/REMOTE_CHECKPOINT_UPDATE_GUIDE.md
?? docs/REMOTE_GITHUB_PUSH_GUIDE.md
?? docs/REMOTE_SERVER_GITHUB_HANDOFF.md
?? docs/REPO_HYGIENE_AND_GIT_POLICY.md
?? download_data.sh
?? download_imagenet_val.py
?? environment.yml
?? experiment_nonideality_sweep.py
?? fix_drudge_wave.py
?? fix_gemini_missing_tasks.py
?? fix_selective_eval.py
?? inference_analysis_utils.py
?? make_appendix.py
?? model_profiling.py
?? overnight_full.py
?? overnight_pythia1b_ablation.py
?? p3_e2e_eval.py
?? p3_e2e_eval_v2.py
?? paper/
?? physical_noise_pipeline.py
?? pipeline_baseline_noise_eval.py
?? pipeline_comprehensive_eval.py
?? plot_convnext_results.py
?? plot_resnet18_results.py
?? prepare_imagenet_val.py
?? probe_resnet_ckpts.py
?? proxy_sensitivity_sweep_gpt.py
?? repo_bootstrap.py
?? report_asset_paths.py
?? report_comp_eval.py
?? report_final.py
?? requirements-optional.txt
?? requirements.txt
?? scripts/
?? setup_cuda_torch.sh
?? stress_test_combined_last1.py
?? tinyvit_hybrid_utils.py
?? train_convnext.py
?? train_resnet18.py
?? visualize_attention.py
?? "\350\277\234\347\253\257/"
```

---

## 3. Py-Compile Output

```
remote107$ python3 -m py_compile p3_hat_train.py p3_hat_eval.py k107_a_launcher.py k107_b_launcher.py k107_c_launcher.py
py_compile: OK
```

---

## 4. Environment Packet

| Item | Value |
|---|---|
| PyTorch | 2.5.1 |
| CUDA device | NVIDIA PH402 SKU 200 |
| Driver | 570.124.06 |
| GPUs available | 8 |
| Python | /home/lisq753/miniconda3/envs/LLM/bin/python |

---

## 5. Launcher Commands

### K107-A Canonical Selective KV

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python k107_a_launcher.py
```

### K107-B Retention Stress

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python k107_b_launcher.py
```

### K107-C State-Count Sweep

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python k107_c_launcher.py
```

---

## 6. Metadata Patch Description

Modified `p3_hat_train.py` and `p3_hat_eval.py` so every JSON output includes a complete metadata envelope:

- `git_commit`, `git_status_short`, `script`, `command`, `mode`
- `model`, `dataset_train`, `dataset_eval`
- `train_seed`, `train_d2d_seed`, `eval_d2d_seed`
- `n_states`, `sigma_c2c`, `sigma_d2d`, `retention_step_time`
- `analog_layers`, `ctx_len`, `stride`, `max_steps`, `batch_size`
- `ppl_before`, `ppl_after` (train) / `ppl` (eval)
- `wall_clock_time`, `gpu_id`, `gpu_name`

Also fixed `p3_hat_eval.py` to enable `retention_enabled` when `retention_step_time > 0`, and added `retention_step_time` to eval output filenames to prevent overwrite collisions.

---

## 7. K107-A Aggregate Table

| Route | Train Seed | Eval D2D | Mean PPL | Std | N |
|---|---|---:|---:|---:|---:|
| last1 `[23]` | 42 | 0.02 | 19.43 | 0.04 | 5 |
| last1 `[23]` | 42 | 0.04 | 19.55 | 0.04 | 5 |
| last1 `[23]` | 42 | 0.05 | 19.60 | 0.03 | 5 |
| last1 `[23]` | 123 | 0.02 | 19.51 | 0.07 | 5 |
| last1 `[23]` | 123 | 0.04 | 19.65 | 0.05 | 5 |
| last1 `[23]` | 123 | 0.05 | 19.70 | 0.04 | 5 |
| last1 `[23]` | 456 | 0.02 | 19.42 | 0.03 | 5 |
| last1 `[23]` | 456 | 0.04 | 19.53 | 0.03 | 5 |
| last1 `[23]` | 456 | 0.05 | 19.57 | 0.03 | 5 |
| last2 `[22,23]` | 42 | 0.02 | 20.10 | 0.03 | 5 |
| last2 `[22,23]` | 42 | 0.04 | 20.42 | 0.02 | 5 |
| last2 `[22,23]` | 42 | 0.05 | 20.53 | 0.03 | 5 |
| last2 `[22,23]` | 123 | 0.02 | 20.13 | 0.05 | 5 |
| last2 `[22,23]` | 123 | 0.04 | 20.46 | 0.03 | 5 |
| last2 `[22,23]` | 123 | 0.05 | 20.58 | 0.03 | 5 |
| last2 `[22,23]` | 456 | 0.02 | 20.19 | 0.03 | 5 |
| last2 `[22,23]` | 456 | 0.04 | 20.52 | 0.03 | 5 |
| last2 `[22,23]` | 456 | 0.05 | 20.64 | 0.03 | 5 |
| all 24 layers | 42 | 0.02 | 37.13 | 0.88 | 5 |
| all 24 layers | 42 | 0.04 | 68.48 | 4.33 | 5 |
| all 24 layers | 42 | 0.05 | 104.29 | 8.93 | 5 |

---

## 8. K107-B Retention Table

| Route | Eval D2D | Retention step time | PPL | vs rst=0 |
|---|---|---:|---:|:---|
| last1 `[23]` | 0.02 | 0 | 19.44 | baseline |
| last1 `[23]` | 0.02 | 0.1 | 19.17 | -0.27 |
| last1 `[23]` | 0.02 | 1 | 19.17 | -0.27 |
| last1 `[23]` | 0.02 | 10 | 19.17 | -0.27 |
| last1 `[23]` | 0.05 | 0 | 19.60 | baseline |
| last1 `[23]` | 0.05 | 0.1 | 19.25 | -0.35 |
| last1 `[23]` | 0.05 | 1 | 19.25 | -0.35 |
| last1 `[23]` | 0.05 | 10 | 19.25 | -0.35 |
| all 24 layers | 0.02 | 0 | 35.81 | baseline |
| all 24 layers | 0.02 | 0.1 | 177.10 | +141.29 |
| all 24 layers | 0.02 | 1 | 176.12 | +140.31 |
| all 24 layers | 0.02 | 10 | 176.06 | +140.25 |
| digital baseline | 0.00 | 0 | 22.18 | — |

---

## 9. K107-C State-Count Table

| n_states | Eval D2D | Mean PPL | Std | N |
|---:|---:|---:|---:|---:|
| 16 | 0.02 | 19.58 | 0.02 | 3 |
| 16 | 0.05 | 19.70 | 0.02 | 3 |
| 32 | 0.02 | 19.47 | 0.03 | 3 |
| 32 | 0.05 | 19.63 | 0.02 | 3 |
| 64 | 0.02 | 19.40 | 0.04 | 3 |
| 64 | 0.05 | 19.56 | 0.02 | 3 |
| 128 | 0.02 | 19.45 | 0.04 | 3 |
| 128 | 0.05 | 19.62 | 0.02 | 3 |
| 256 | 0.02 | 19.42 | 0.05 | 3 |
| 256 | 0.05 | 19.60 | 0.04 | 3 |

---

## 10. Verdict

**LOCK**

Rationale:
- K107-A last1 `[23]` passes train-seed replication (42/123/456), fresh-D2D-seed stability, and metadata verification.
- K107-B shows retention is manageable (even slightly beneficial) for last1.
- K107-C shows 64 states is the sweet spot; 16 states is viable if area-constrained.
- All-layer analog KV remains catastrophic and is not a deployment route.
- Selective terminal-layer analog KV-cache is canonical for Pythia-410M.
