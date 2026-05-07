# Remote105 Canonical Freeze — TinyImageNet Cross-Architecture Validation

**Date:** 2026-05-08
**Branch:** `105-remote-results`
**Freeze commit:** `ccf1cf7`
**Executor:** Remote105 (Claude)
**Role:** Experiment-only validation; no manuscript prose.

---

## 1. Environment

| Item | Value |
|---|---|
| Python | 3.11.15 |
| PyTorch | 2.4.1+cu121 |
| CUDA | 12.1 |
| timm | 1.0.26 |
| GPU | 8x NVIDIA PH402 SKU 200 |
| Dataset | TinyImageNet-200 (`../data/tiny-imagenet-200`) |

---

## 2. Exact Commands

### Training

```bash
conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch {deit_small_patch16_224|vit_small_patch16_224} \
  --hat-type {digital|proportional} \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed {123|456|789} --device cuda:{gpu_id} --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet
```

### Fresh Eval

```bash
conda run -n hat python -u eval_fresh_instances_vit.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/{arch}_{hat_type}_seed{seed}/best.pt \
  --device cuda \
  --output results/json/{arch}_{hat_type}_seed{seed}_best_fresh_eval.json
```

Fresh protocol: 10 instances × 5 MC runs per instance. D2D resampled per instance.

---

## 3. Per-Seed Results

### DeiT

| HAT | Seed | Source (%) | Fresh (%) | Std (%) | Fresh-Source (pp) |
|---|---|---:|---:|---:|---:|
| digital | 123 | 48.22 | 48.22 | 0.00 | 0.00 |
| proportional | 123 | 50.24 | 50.20 | 0.10 | -0.04 |
| digital | 456 | 53.61 | 53.61 | 0.00 | 0.00 |
| proportional | 456 | 54.44 | 54.19 | 0.09 | -0.25 |
| digital | 789 | 53.58 | 53.58 | 0.00 | 0.00 |
| proportional | 789 | 56.54 | 56.33 | 0.13 | -0.21 |

### ViT

| HAT | Seed | Source (%) | Fresh (%) | Std (%) | Fresh-Source (pp) |
|---|---|---:|---:|---:|---:|
| digital | 123 | 48.83 | 48.83 | 0.00 | 0.00 |
| proportional | 123 | 49.03 | 49.00 | 0.09 | -0.03 |
| digital | 456 | 54.58 | 54.58 | 0.00 | 0.00 |
| proportional | 456 | 54.06 | 53.90 | 0.13 | -0.16 |
| digital | 789 | 50.86 | 50.86 | 0.00 | 0.00 |
| proportional | 789 | 55.85 | 55.41 | 0.10 | -0.44 |

---

## 4. Proportional-vs-Digital Deltas (Fresh, pp)

| Seed | DeiT Prop − Digital | ViT Prop − Digital |
|---:|---:|---:|
| 123 | +1.98 | +0.17 |
| 456 | +0.58 | -0.68 |
| 789 | +2.75 | +4.55 |
| **Mean** | **+1.77** | **+1.35** |

---

## 5. Metadata Gap Note

Seed 123/456 JSONs lack `commit_hash`, `pytorch_version`, `cuda_device_name`, and `git_worktree_dirty`. These values are known:

- Git commit: `fbfda71` (branch `remote-exploration`)
- PyTorch: 2.4.1+cu121
- CUDA: 12.1
- GPU: NVIDIA PH402 SKU 200

Seed 789 JSONs contain full metadata (`commit_hash=a6c2ea1`). All JSONs contain required fields: arch, hat_type, seed, best_epoch, source_acc, fresh_mean, fresh_std, instances, mc_runs.

---

## 6. Experimental Recommendation

**Proportional HAT should be treated as provisionally validated across both DeiT and ViT on TinyImageNet-200; DeiT confidence is high (3/3 seeds), ViT confidence is moderate (2/3 seeds, one digital outlier) and sufficient for provisional cross-architecture claims without requiring additional seeds for manuscript boundary.**
