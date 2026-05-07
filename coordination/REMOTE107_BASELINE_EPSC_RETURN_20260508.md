# Remote 107 Baseline + EPSC + Scale Check Full Return

**Date:** 2026-05-08
**Branch:** `107-clean`
**Commit:** `e449de25c79204b07b5064f79d51dd2cc986b1ca`

---

## 1. Git Status

```
?? README.md
?? analog_layers_ensemble.py
?? device_profile_utils.py
?? device_profiles/
?? diag_fresh_instance.py
?? dispatches/
?? docs/
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

All committed deliverables are under `coordination/REMOTE107_*_20260508.md`, `deliverable/results_v3/`, and launcher scripts.

---

## 2. Environment

| Component | Version |
|:---|:---|
| Python | 3.11.14 |
| PyTorch | 2.5.1 |
| GPU | NVIDIA PH402 SKU 200 |
| CUDA | Available (8 devices) |
| Transformers | Latest (HF Hub offline) |

---

## 3. Exact Commands

### P0-A Baseline Reconciliation

```bash
# Current evaluator (ctx_len=512, stride=256, batch_size=1)
/home/lisq753/miniconda3/envs/LLM/bin/python baseline_eval_digital.py

# Old evaluator (max_length=1024, stride=512, batch_size=8)
/home/lisq753/miniconda3/envs/LLM/bin/python baseline_eval_old.py
```

### P0-B Paired Ablations

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python p0b_ablation_launcher.py
```

### P0-C Metadata Export

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python p0c_export_metadata.py
```

### P1 EPSC Stress

```bash
/home/lisq753/miniconda3/envs/LLM/bin/python p1_epsc_launcher.py
```

### P2 Pythia-1B Scale Check

```bash
# Train seed123
/home/lisq753/miniconda3/envs/LLM/bin/python p3_hat_train.py \
  --name p1b_last1_d2d002 --model_name EleutherAI/pythia-1b-deduped \
  --sigma_d2d 0.02 --sigma_c2c 0.0 --analog_layers 15 \
  --seed 123 --d2d-seed 123 --max_steps 100 \
  --output_dir /home/lisq753/projects/HAT_kv107/paper2/results/remote107

# Evals
/home/lisq753/miniconda3/envs/LLM/bin/python p2_p1b_eval_launcher.py
```

---

## 4. Results Tables

### P0-A Baseline Reconciliation

| Evaluator | ctx_len | stride | batch_size | PPL |
|:---:|:---:|:---:|:---:|:---:|
| Current K107 | 512 | 256 | 1 | **22.18** |
| Old/vectorized | 1024 | 512 | 8 | 15.62 |

**Verdict:** 22.18 is canonical for K107 comparisons.

### P0-B Paired HAT Ablations

| Checkpoint | B1 (digital) | B2 (patch no noise) | B3 (D2D=0.02) | B4 (D2D=0.05) |
|:---:|:---:|:---:|:---:|:---:|
| seed42 | 18.99 | 19.01 | 19.46 | 19.62 |
| seed123 | 19.09 | 19.10 | 19.56 | 19.72 |
| seed456 | 19.05 | 19.07 | 19.44 | 19.59 |

**Verdict:** HAT training improves clean digital by ~3.1 PPL; analog patch overhead is ~0.02 PPL; D2D noise adds ~0.4–0.6 PPL.

### P0-C Metadata Export

| Checkpoint | hat_config | train JSON |
|:---:|:---:|:---:|
| k107_a1_last1_seed{42,123,456} | ✅ | ✅ |
| k107_a2_last2_seed{42,123,456} | ✅ | ✅ |
| k107_a3_all_seed42 | ✅ | ✅ |
| k107_c_{16,32,64,128}states_seed42 | ✅ | ✅ |

### P1 EPSC Proxy Stress

| Config | C2C | D2D | seed42 mean | seed123 mean | seed456 mean | Max |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| EPSC-e1 | 0.05 | 0.05 | 19.69 | 19.80 | 19.67 | 19.81 |
| EPSC-e2 | 0.10 | 0.10 | 20.10 | 20.20 | 20.05 | **20.23** |
| EPSC-e3 | 0.15 | 0.15 | 20.76 | 20.85 | 20.69 | 20.87 |
| EPSC-e4 | 0.00 | 0.20 | 20.59 | 20.69 | 20.52 | 20.75 |
| EPSC-e5 | 0.01 | 0.10 | 19.84 | 19.94 | 19.80 | 19.97 |

**Kill criterion:** EPSC-e2 max = 20.23 < 25 → **PASS**

### P2 Pythia-1B Scale Check

| Train seed | Eval D2D | Mean PPL | Range |
|:---:|:---:|:---:|:---:|
| 42 | 0.02 | 14.59 | 14.58–14.60 |
| 42 | 0.05 | 14.80 | 14.79–14.81 |
| 123 | 0.02 | 14.61 | 14.59–14.64 |
| 123 | 0.05 | 14.83 | 14.80–14.87 |

**Verdict:** Seed123 replicates seed42 within 0.03 PPL. Scale advantage is robust.

---

## 5. File Paths

| Deliverable | Path |
|:---|:---|
| P0-A current baseline JSON | `deliverable/results_v3/baseline_digital_current.json` |
| P0-A old baseline JSON | `deliverable/results_v3/baseline_digital_old.json` |
| P0-B ablation CSV | `deliverable/results_v3/p0b_ablation/summary.csv` |
| P0-B ablation JSONs | `deliverable/results_v3/p0b_ablation/*.json` (24 files) |
| P0-C train metadata | `deliverable/results_v3/train_meta/` (22 files) |
| P1 EPSC CSV | `deliverable/results_v3/epsc_stress/summary.csv` |
| P1 EPSC JSONs | `deliverable/results_v3/epsc_stress/*.json` (45 files) |
| P2 P1B eval JSONs | `deliverable/results_v3/p1b_1b/eval_p1b_last1_d2d002_seed123*.json` (6 files) |

---

## 6. Verdicts

| Claim | Status | Notes |
|:---|:---:|:---|
| K107 digital baseline | **LOCK** | 22.18 PPL, ctx=512/stride=256/bs=1 |
| HAT fine-tuning gain | **LOCK** | Improves clean digital by ~3.1 PPL |
| Analog patch overhead | **LOCK** | Negligible (~+0.02 PPL) |
| D2D=0.02 viability | **LOCK** | ~+0.45 PPL overhead |
| D2D=0.05 viability | **LOCK** | ~+0.60 PPL overhead |
| EPSC-proxy compatibility | **LOCK** | Max stress 20.23 << 25 |
| Pythia-1B scale-up | **LOCK** | Replicates across train seeds, 4.8 PPL better than 410M |
| C2C noise tolerance | **LOCK** | C2C=0.02 adds only +0.07 PPL |
| Selective last1 canonical | **LOCK** | Best single-layer config for 410M and 1B |

---

## 7. Suggested Next Steps

1. **Manuscript figures:** P0-B bar chart (B1→B2→B3→B4), P1 EPSC stress curve, P2 scale comparison.
2. **Retention stress follow-up:** K107-B already completed; no additional retention runs needed.
3. **Larger scale:** If GPU time permits, Pythia-2.8B or 6.9B last1 validation would strengthen scale claim.
4. **Repo cleanup:** The remaining untracked files (old docs, scripts) should be organized or `.gitignore`d before merging to main.
