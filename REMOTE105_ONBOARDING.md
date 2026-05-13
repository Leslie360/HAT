# Remote 105 Onboarding — HAT TinyImageNet Cross-Architecture Validation

**Last updated:** 2026-05-13
**Branch:** `105-remote-results`
**GitHub:** `git@github-105:Leslie360/HAT.git`
**Agent role:** Experiment-only validation (run experiments, preserve data, provide tables; do NOT write manuscript prose or edit LaTeX).

---

## 1. What Is This?

Remote 105 is the cross-architecture validation server for the HAT (Hybrid Analog/Digital Training) project.

**Core question:** Does proportional-noise HAT outperform pure digital training when evaluated on fresh analog hardware instances (with resampled D2D noise)?

**Testbed:** TinyImageNet-200 with ViT/DeiT.

**Validation scope:**
- Base comparison: DeiT-Small vs ViT-Small, `digital` vs `proportional`, seeds `123/456/789`
- Follow-up: ViT `digital` / `proportional` seed `2025`
- Controls: completed DeiT `ensemble` / `standard` seed `789`
- Fresh eval: 10 instances × 5 MC runs per instance
- Targeted diagnostics: ViT noise-off ablations and 30-instance fresh-eval follow-ups

---

## 2. Environment

| Item | Value |
|---|---|
| Python | 3.11.15 |
| PyTorch | 2.4.1+cu121 |
| CUDA | 12.1 |
| timm | 1.0.26 |
| GPU | 8× NVIDIA PH402 SKU 200 |
| Dataset | `../data/tiny-imagenet-200` (train 100K, test 10K) |
| Conda env | `hat` |
| Working dir | `original_repo/` |

---

## 3. Key Files

| File | Purpose |
|---|---|
| `train_vit_tinyimagenet.py` | Training script (digital/proportional/ensemble/standard) |
| `eval_fresh_instances_vit.py` | Fresh instance evaluation (10×5) |
| `eval_t105e_noise_off.py` | T105-E ablation (evaluate proportional checkpoint with noise disabled) |
| `analog_layers.py` | Proportional noise implementation |
| `docs/handoff/20260508_full_return.md` | Main return report to local team |
| `docs/handoff/20260513_followup_return.md` | Seed2025 + control-completion addendum |
| `docs/handoff/REMOTE105_CANONICAL_FREEZE_20260508.md` | Frozen canonical package |
| `docs/handoff/REMOTE105_VIT_SEED456_OUTLIER_NOTE_20260508.md` | Outlier diagnostic |
| `results/summary/remote105_tinyimagenet_all_available_summary.csv` | All seeds machine-readable table |
| `results/summary/remote105_tinyimagenet_seed789_summary.csv` | Seed789 subset with completed DeiT controls |
| `results/json/*seed789*_fresh_eval.json` | Seed789 JSON results |
| `results/json/*seed2025*_fresh_eval.json` | ViT seed2025 follow-up JSONs |
| `report_md/_gpt/json_gpt/*noise_off.json` | ViT noise-off diagnostics |
| `report_md/_gpt/json_gpt/*` | Historical JSON results (seed123/456/789) |
| `checkpoints/_gpt/cross_arch_tinyimagenet/` | All checkpoints (best.pt + last.pt + train.log) |

---

## 4. Exact Commands

### Training

```bash
cd original_repo
conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch {deit_small_patch16_224|vit_small_patch16_224} \
  --hat-type {digital|proportional|ensemble|standard} \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed {123|456|789|2025} --device cuda:{gpu_id} --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet
```

**Important:** The script has NO `--resume` flag. If training is killed, it restarts from epoch 0. The `last.pt` is saved each epoch but never auto-loaded.

### Fresh Eval

```bash
conda run -n hat python -u eval_fresh_instances_vit.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/{arch}_{hat_type}_seed{seed}/best.pt \
  --device cuda:{gpu_id} \
  --output results/json/{arch}_{hat_type}_seed{seed}_best_fresh_eval.json
```

Protocol: 10 instances × 5 MC runs. D2D resampled per instance. C2C resampled per forward.

### T105-E Ablation (noise off)

```bash
conda run -n hat python -u eval_t105e_noise_off.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/deit_small_patch16_224_proportional_seed456/best.pt \
  --device cuda
```

---

## 5. Results Summary

### DeiT

| HAT | Seed | Source | Fresh | Std | Fresh-Source |
|---|---|---:|---:|---:|---:|
| digital | 123 | 48.22 | 48.22 | 0.00 | 0.00 |
| proportional | 123 | 50.24 | 50.20 | 0.10 | -0.04 |
| digital | 456 | 53.61 | 53.61 | 0.00 | 0.00 |
| proportional | 456 | 54.44 | 54.19 | 0.09 | -0.25 |
| digital | 789 | 53.58 | 53.58 | 0.00 | 0.00 |
| proportional | 789 | 56.54 | 56.33 | 0.13 | -0.21 |

**P-D fresh gap:** seed123 +1.98pt, seed456 +0.58pt, seed789 +2.75pt. **Average +1.77pt.**

### ViT

| HAT | Seed | Source | Fresh | Std | Fresh-Source |
|---|---|---:|---:|---:|---:|
| digital | 123 | 48.83 | 48.83 | 0.00 | 0.00 |
| proportional | 123 | 49.03 | 49.00 | 0.09 | -0.03 |
| digital | 456 | **54.58** | **54.58** | 0.00 | 0.00 |
| proportional | 456 | 54.06 | 53.90 | 0.13 | -0.16 |
| digital | 789 | 50.86 | 50.86 | 0.00 | 0.00 |
| proportional | 789 | 55.85 | 55.41 | 0.10 | -0.44 |
| digital | 2025 | 50.00 | 50.00 | 0.00 | 0.00 |
| proportional | 2025 | 49.77 | 49.85 | 0.08 | +0.08 |

**P-D fresh gap:** seed123 +0.17pt, seed456 -0.68pt, seed789 +4.55pt, seed2025 -0.15pt. **Average +0.97pt (2/4 seeds favor proportional).**

### Standard (Negative Control)

| Arch | Seed | Source | Fresh | Collapse |
|---|---|---:|---:|---:|
| DeiT | 123 | 40.61 | 6.39 | -34.23pt |
| DeiT | 456 | 41.19 | 6.84 | -34.35pt |
| DeiT | 789 | 41.28 | 5.77 | -35.51pt |
| ViT | 123 | 39.22 | 5.22 | -34.00pt |
| ViT | 456 | 38.43 | 8.62 | -29.81pt |

### Ensemble (Partial Recovery)

| Arch | Seed | Source | Fresh | Degradation |
|---|---|---:|---:|---:|
| DeiT | 123 | 45.26 | 40.44 | -4.82pt |
| DeiT | 456 | 44.52 | 41.11 | -3.41pt |
| DeiT | 789 | 44.73 | 39.92 | -4.81pt |
| ViT | 123 | 43.64 | 40.24 | -3.40pt |
| ViT | 456 | 44.79 | 40.08 | -4.71pt |

### T105-E Ablation

| Condition | Acc |
|---|---|
| noise_off | 54.52% |
| fresh | 54.19% |
| digital | 53.61% |

Regularization gain: **+0.91pt** (noise_off > digital).

### Additional 20260513 Diagnostics

| Experiment | Result |
|---|---:|
| ViT proportional seed456 noise_off | 53.99% |
| ViT proportional seed789 noise_off | 55.49% |
| DeiT proportional seed789 fresh `30x5` | 56.32 ± 0.12 |
| ViT proportional seed789 fresh `30x5` | 55.46 ± 0.11 |

---

## 6. Key Findings

1. **DeiT proportional > digital in all 3 base seeds.** Highly confident.
2. **ViT is mixed after seed2025.** `proportional` beats `digital` in `2/4` seeds, with fresh-gap mean `+0.97pt`, but seed variance is too high for a stable positive claim.
3. **Fresh degradation for proportional remains tiny** on the main DeiT / ViT checkpoints, and the `30x5` seed789 follow-ups stay in the same mean / std regime.
4. **Standard mode still collapses ~-34 to -35pt, and ensemble still degrades ~-3 to -5pt**, validating the control story after completing DeiT seed789.
5. **Overall label:** DeiT-validated / ViT-mixed. Remote105 no longer supports a strong positive cross-architecture claim on ViT.

---

## 7. Directory Structure

```
original_repo/
├── checkpoints/_gpt/cross_arch_tinyimagenet/
│   ├── deit_small_patch16_224_{digital|proportional|ensemble|standard}_seed{123|456|789}/
│   │   ├── best.pt
│   │   ├── last.pt
│   │   └── train.log
│   ├── vit_small_patch16_224_{digital|proportional}_seed{123|456|789|2025}/
│   │   ├── best.pt
│   │   ├── last.pt
│   │   └── train.log
│   └── vit_small_patch16_224_{ensemble|standard}_seed{123|456}/
│       ├── best.pt
│       ├── last.pt
│       └── train.log
├── docs/handoff/
│   ├── 20260508_full_return.md
│   ├── 20260513_followup_return.md
│   ├── REMOTE105_BOUNDARY_AND_NEXT_TASKS_20260508.md
│   ├── REMOTE105_CANONICAL_FREEZE_20260508.md
│   └── REMOTE105_VIT_SEED456_OUTLIER_NOTE_20260508.md
├── report_md/_gpt/json_gpt/
│   └── *_best_fresh_eval.json (all seeds)
├── results/
│   ├── json/ (*seed789* fresh eval JSONs)
│   └── summary/ (CSV tables)
├── train_vit_tinyimagenet.py
├── eval_fresh_instances_vit.py
├── eval_t105e_noise_off.py
└── analog_layers.py
```

---

## 8. Git Workflow

```bash
# Fetch latest
git fetch origin

# Switch to working branch
git switch 105-remote-results

# Pull safety: do NOT use --ff-only if histories diverged;
# use merge instead when codex adds task files.

# Push results
git add <specific-files>
git commit -m "..."
git push origin HEAD:105-remote-results
```

**Remote URL:** `git@github-105:Leslie360/HAT.git` (SSH alias defined in `~/.ssh/config`).

**Important:** Local `105-remote-results` and remote `105-remote-results` have occasionally diverged. If push fails with "non-fast-forward", fetch first, merge codex's task commits, then push again. Do NOT force-push unless explicitly clearing a stale remote state.

---

## 9. Known Issues / Caveats

1. **No resume in training script.** Kill = restart from epoch 0. `last.pt` exists but is not auto-loaded.
2. **Nohup log redirect broken with `conda run`.** Training logs go to `train.log` inside `save_dir`; eval has no persistent log (stdout only).
3. **Older metadata-gap notes are stale.** The current checked seed123/456 JSONs already include `commit_hash`, `pytorch_version`, `cuda_device_name`, and `git_worktree_dirty`.
4. **ViT digital seed456 remains a high outlier.** 54.58% vs 48.83 / 50.86 / 50.00 on seeds 123 / 789 / 2025. No protocol violation found; treat as legitimate seed variance, not artifact.
5. **Two follow-up trainings stopped before a clean terminal logger line.** `vit_small_patch16_224_proportional_seed2025` and `deit_small_patch16_224_ensemble_seed789` were evaluated from saved `best.pt`; no checkpoint corruption was observed, but the logs do not show an explicit final `Finished.` line.

---

## 10. Contacts / Handoff

- **Dispatcher:** Codex (via GitHub commits to `105-remote-results`)
- **Local team:** Reads `docs/handoff/` and `results/`
- **Remote agent:** You (run experiments, return JSON/CSV/Markdown)

**Rule:** Do not edit manuscript LaTeX, do not polish figures, do not change narrative framing beyond short experimental recommendations in handoff docs.

---

## 11. If You Need to Reproduce

```bash
cd original_repo
git checkout 105-remote-results
# DeiT proportional seed789 example:
conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch deit_small_patch16_224 --hat-type proportional \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed 789 --device cuda:0 --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet
```

All seeds, architectures, and HAT modes use the **same hyperparameters** except `--arch`, `--hat-type`, and `--seed`.
