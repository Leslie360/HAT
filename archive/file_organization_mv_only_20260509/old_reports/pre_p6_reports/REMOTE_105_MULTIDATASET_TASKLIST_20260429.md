# Remote 105 Multi-Dataset Validation Task List

**Date:** 2026-04-29
**Owner:** Remote 105 agent
**Coordinator:** Codex
**Scope:** Work-1 HAT architecture / dataset validation. Do not run Work-2 KV-cache tasks from this file.

## 0. Clone / Update

Use the clean `main` branch. Remote 105 is pull-only; do not push from the server.

```bash
git clone -b main https://github.com/Leslie360/HAT.git HAT_105
cd HAT_105
```

If already cloned:

```bash
cd HAT_105
git fetch origin main
git checkout main
git pull --ff-only
```

Read first:

```text
REMOTE_105_MULTIDATASET_TASKLIST_20260429.md
REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md
report_md/_gpt/REMOTE_105_SEED123_DELIVERY_REVIEW_20260429.md
```

## 1. Received Seed-123 Signal

Remote 105 reported seed=123:

| Architecture | HAT | Best Train Acc | Fresh Mean | Fresh Std | Status |
|---|---|---:|---:|---:|---|
| deit | proportional | 50.24% | 50.20% | 0.10% | best |
| vit | proportional | 49.03% | 49.00% | 0.09% | stable |
| vit | digital | 48.83% | 48.83% | 0.00% | no-noise ceiling |
| deit | ensemble | 45.26% | 40.44% | 0.43% | -4.8pt |
| vit | ensemble | 43.64% | 40.24% | 0.36% | -3.4pt |
| deit | standard | 40.61% | 6.38% | 0.85% | collapsed |
| vit | standard | 39.22% | 5.22% | 0.51% | collapsed |

Codex interpretation: strong signal, but not final evidence until same-architecture baselines and multi-seed validation are complete.

## 2. Critical Caveats To Fix

1. **Do not claim proportional > digital using `deit_proportional` vs `vit_digital`.** Architecture is confounded. Need `deit_digital` and same-architecture comparisons.
2. Clarify what "Best Train Acc" means. If it is training-set accuracy, the values are unexpectedly close to fresh results and need explanation. If it is source/test accuracy, rename it.
3. Confirm fresh protocol: number of fresh chip instances, number of MC repeats, whether D2D is resampled per instance, and whether C2C is resampled per read.
4. Confirm dataset and class count. The ~50% ceiling suggests either a hard dataset/architecture setting or a short-training regime. Report dataset, epochs, pretrained flag, image size, optimizer, lr, batch size.
5. Standard collapse is useful, but only if standard truly means "no train-time noise / eval-time noise only" under the same source/fresh protocol.

## 3. Required Reproducibility Packet

Return one Markdown file with:

```bash
git rev-parse HEAD
git status --short
git diff --stat
git diff -- .
python - <<'PY'
import torch, json, sys
try:
    import timm
except Exception as e:
    timm = None
print(json.dumps({
  'python': sys.version,
  'torch': torch.__version__,
  'cuda': torch.version.cuda,
  'cuda_available': torch.cuda.is_available(),
  'device_count': torch.cuda.device_count(),
  'devices': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
  'timm': getattr(timm, '__version__', None),
}, indent=2))
PY
```

Also return for every run:

```text
run_id, architecture, hat_mode, dataset, seed, epochs, batch_size, lr, optimizer,
pretrained, image_size, source_metric_name, best_source, best_epoch,
fresh_instances, mc_repeats, fresh_mean, fresh_std, command, checkpoint_path
```

Do not return checkpoints or long logs.

## 4. Priority Experiments

### T105-A: Same-Architecture Baseline Closure, Seed 123

Complete missing cells so claims are not architecture-confounded.

Minimum matrix:

| Architecture | Modes |
|---|---|
| vit | digital, standard, ensemble, proportional |
| deit | digital, standard, ensemble, proportional |

`deit_digital` is mandatory because current best comparison uses `deit_proportional` against `vit_digital`, which is not valid.

Return exact commands and result table.

### T105-B: Multi-Seed CIFAR/Main-Dataset Validation

Run seeds:

```text
123, 456, 789
```

Priority cells:

1. deit proportional
2. deit digital
3. vit proportional
4. vit digital
5. deit ensemble
6. vit ensemble
7. deit standard and vit standard only if resources allow; otherwise one additional seed is enough to confirm collapse.

Report mean ± std across seeds for source and fresh.

Kill criterion: if proportional advantage over same-architecture digital is <0.3 percentage points after 3 seeds, downgrade the claim to "matches digital while preserving fresh robustness", not "exceeds digital".

### T105-C: Multi-Dataset Validation

Run only datasets already available or approved on the server. Do not download if policy forbids it.

Priority order:

1. current dataset used in seed=123 table, complete multi-seed first
2. CIFAR-100 if available
3. Flowers102 or Tiny-ImageNet only if already cached/approved

For each dataset, minimum modes:

```text
digital, proportional, ensemble, standard
```

Use the same architecture first (`deit` if seed=123 deit remains best after T105-A). Add `vit` only if GPU time permits.

### T105-D: Fresh Robustness Protocol Audit

For the best proportional run and one digital baseline, return:

- per-instance fresh accuracy list
- seed list used for fresh instances
- D2D/C2C noise parameters
- whether source and fresh share any noise state
- whether eval is deterministic for digital baseline

### T105-E: Proportional Regularization Claim Test

If same-architecture proportional still beats digital, run one ablation:

1. proportional train noise on, eval noise off
2. proportional train noise on, eval fresh noise on
3. digital baseline

Purpose: separate regularization benefit from eval-noise robustness.

## 5. Result Return Format

Return compact Markdown chunks only. Do not push from the server.

```text
REMOTE_RESULT_CHUNK 001/N
# Remote 105 Return

## Verdict

## Reproducibility Packet

## Commands

## Results Tables

## Per-Instance Fresh Lists

## Failures / Warnings

## Next Requested Action
REMOTE_RESULT_CHUNK_END 001/N
```

## 6. Current Decision Logic

After T105-A/B:

- If proportional > same-architecture digital by >=0.5 pt and std is small, keep the claim: proportional HAT acts as robustness training and regularization.
- If proportional roughly equals digital but has fresh zero-degradation, claim: proportional preserves digital accuracy while enabling cross-instance robustness.
- If proportional loses to digital but remains fresh-stable, claim: proportional trades small source accuracy for deployment robustness.
- If standard remains ~5-6% fresh, use it as the negative control: eval-only noise injection is not enough.
