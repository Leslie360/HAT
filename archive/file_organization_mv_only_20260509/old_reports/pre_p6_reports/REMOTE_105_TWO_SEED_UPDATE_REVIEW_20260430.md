# Remote 105 Two-Seed Update Review

**Date:** 2026-04-30 10:35 CST
**Reviewer:** Codex
**Source:** User-relayed Remote 105 table, seeds 123 and 456.

## 1. Raw Data Preserved

| Arch | HAT | Seed | Source | Fresh | Std | Delta |
|---|---|---:|---:|---:|---:|---:|
| deit | proportional | 123 | 50.24% | 50.20% | 0.10% | -0.04pt |
| deit | proportional | 456 | 54.44% | 54.19% | 0.09% | -0.25pt |
| deit | digital | 123 | 48.22% | 48.22% | 0.00% | 0.00pt |
| deit | digital | 456 | 53.61% | 53.61% | 0.00% | 0.00pt |
| deit | ensemble | 123 | 45.26% | 40.44% | 0.43% | -4.82pt |
| deit | ensemble | 456 | 44.52% | 41.11% | 0.35% | -3.41pt |
| deit | standard | 123 | 40.61% | 6.38% | 0.85% | -34.23pt |
| deit | standard | 456 | 41.19% | 6.84% | 0.83% | -34.35pt |
| vit | proportional | 123 | 49.03% | 49.00% | 0.09% | -0.03pt |
| vit | proportional | 456 | 54.06% | 53.90% | 0.13% | -0.16pt |
| vit | digital | 123 | 48.83% | 48.83% | 0.00% | 0.00pt |
| vit | digital | 456 | 54.58% | 54.58% | 0.00% | 0.00pt |
| vit | ensemble | 123 | 43.64% | 40.24% | 0.36% | -3.40pt |
| vit | ensemble | 456 | 44.79% | 40.08% | 0.36% | -4.71pt |
| vit | standard | 123 | 39.22% | 5.22% | 0.51% | -34.00pt |
| vit | standard | 456 | 38.43% | 8.62% | 0.94% | -29.81pt |

## 2. T105-E Ablation Preserved

Target: `deit_proportional_seed456`

| Condition | Acc |
|---|---:|
| noise_off | 54.52% |
| source | 54.44% |
| fresh | 54.19% |
| digital | 53.61% |

Remote interpretation: `noise_off > digital = +0.91pt`, suggesting regularization gain.

Codex interpretation: promising, but still provisional until exact command/env and seed789 close. The ablation is useful because it separates train-time noise regularization from fresh-noise evaluation.

## 3. Per-Seed P vs D

| Arch | seed123 | seed456 |
|---|---:|---:|
| deit | P 50.20 > D 48.22 (+1.98pt) | P 54.19 > D 53.61 (+0.58pt) |
| vit | P 49.00 > D 48.83 (+0.17pt) | P 53.90 < D 54.58 (-0.68pt) |

## 4. Current Technical Judgment

1. **DeiT proportional is now the strongest 105 signal.** It beats same-architecture digital in both seeds and has near-zero fresh degradation.
2. **ViT is not yet consistent.** Seed456 has `vit_digital=54.58%`, higher than proportional by 0.68pt. This weakens any global claim that proportional universally beats digital.
3. **Robustness claim is stronger than superiority claim.** Across both architectures and both seeds, proportional has fresh delta <= 0.25pt, while standard collapses by ~30-34pt and ensemble loses ~3-5pt.
4. **Standard collapse is expected under the config matrix.** Standard trains with C2C=0 and evaluates with C2C=0.05, so the experiment is a valid negative control for train/eval noise mismatch, not a mysterious failure.
5. **Do not ask Opus yet.** User plans to wait for Remote 105's full report today. That is correct; Opus should see seed789 and reproducibility metadata if possible.

## 5. Gate Status Against Opus Remote Brief

| Gate | Status | Comment |
|---|---|---|
| G105-1 naming semantics | not closed | Need confirm Source vs Train naming. |
| G105-2 same-arch digital | partially closed | `deit_digital` and `vit_digital` exist for seeds 123/456. |
| G105-3 multi-seed | not closed | Need seed789; several jobs running. |
| G105-4 fresh protocol audit | not closed | Need n_instances, MC repeats, D2D/C2C policy. |
| G105-5 reproducibility | not closed | Need git SHA/env/commands. |

## 6. Recommendation For Remote 105

Continue the in-progress jobs. Highest priority is completing seed789 for:

- `deit_proportional_seed789`
- `deit_digital_seed789`
- `vit_proportional_seed789`
- `vit_digital_seed789` (must start if not running)

Also return in the final report:

1. Exact command for each cell.
2. Dataset identity, class count, image size, pretrained flag, epochs, optimizer, lr, batch size.
3. Whether `Source` is test/source accuracy or train-set accuracy.
4. Fresh protocol: number of fresh instances, MC repeats, D2D/C2C sampling policy.
5. Full per-seed mean/std table.

## 7. Provisional Narrative If Seed789 Confirms

Safe wording:

> Remote 105 suggests proportional HAT is a robust cross-architecture training mode: it preserves fresh-instance accuracy with near-zero degradation, while standard train-clean/eval-noisy deployment collapses and ensemble loses several points. Same-architecture superiority over digital is clear for DeiT but not yet stable for ViT; therefore the current defensible claim is robustness and regularization potential, not universal digital superiority.


---

## 8. P1 Return Addendum — Repro / Naming / Fresh Protocol

**Received:** 2026-04-30, user-relayed Remote 105 update.

### 8.1 Reproducibility Packet

```text
Git SHA: fbfda71018eae5078968aa6f7faba0ae5b2d5ead
Python: 3.11.15
PyTorch: 2.4.1+cu121
timm: 1.0.26
CUDA: 12.1
GPU: 8x NVIDIA PH402 SKU 200
```

Codex gate judgment: useful environment packet received, but **G105-5 is not fully closed** until exact commands, `git status --short`, `git diff --stat`, and per-run config table are returned.

### 8.2 Source Accuracy Definition

Remote clarifies:

```text
Source = test_acc at best epoch, not train_acc.
```

Example:

```text
Epoch 99/100: train_loss=0.1073, train_acc=97.11%, test_acc=54.44% (best=54.44%)
```

Interpretation:

- `train_acc` = training-set accuracy.
- `Source` = validation/test accuracy at best epoch.
- `Fresh` = cross-chip-instance evaluation accuracy.

Codex gate judgment: **G105-1 naming semantics is closed**, provided future tables rename `Source` clearly and do not call it `Best Train Acc`.

### 8.3 Fresh Eval Protocol

Remote clarifies:

```text
Instances: 10
MC runs per instance: 5
Total evals: 50

D2D: resampled once per instance, seed = 42 + idx*100
C2C: resampled every forward pass with torch.randn_like
```

Protocol sketch:

```python
for instance_idx in range(10):
    seed = 42 + instance_idx * 100
    torch.manual_seed(seed)
    resample_d2d_buffers(model)
    for mc_run in range(5):
        loss, acc = evaluate(...)  # C2C resampled in forward
```

Codex gate judgment: **G105-4 fresh protocol is substantially closed**. Remaining nice-to-have: confirm whether eval transforms/data order are deterministic and whether digital mode bypasses noise modules entirely.

### 8.4 Remote Execution Plan

Remote reports:

1. GPU 0 frees in ~1.3h, then start `vit_digital_seed789`.
2. After training completes, run batch fresh eval for four cells.
3. Summarize seed789 and update document.

Current remote GPU status:

| GPU | Task | Progress |
|---:|---|---|
| 0 | `deit_digital_seed456` | epoch 94/100, ~1.3h remaining |
| 7 | `vit_digital_seed456` | epoch 91/100, ~2h remaining |

Codex judgment: plan is correct. The only missing critical launch is `vit_digital_seed789`; do not start lower-priority tasks until this cell is queued.

### 8.5 Updated Gate Status

| Gate | Status | Comment |
|---|---|---|
| G105-1 naming semantics | **closed** | Source = best-epoch test_acc, not train_acc. |
| G105-2 same-arch digital | partially closed | deit/vit digital seeds 123/456 exist; seed789 pending. |
| G105-3 multi-seed | open | seed789 pending. |
| G105-4 fresh protocol audit | **substantially closed** | 10 instances x 5 MC, D2D per instance, C2C per forward. |
| G105-5 reproducibility | partially closed | Env/SHA received; exact commands/diff/status still needed. |

### 8.6 Next Remote 105 Request

For final report, include:

1. Exact commands or config JSON for every run.
2. `git status --short` and `git diff --stat`.
3. Final seed789 table.
4. Per-seed mean/std across seeds 123/456/789.
5. Explicit pass/fail against: proportional > digital, proportional ≈ digital, or proportional < digital for each architecture.

---

## 9. P1 Return Addendum 2 — Git Status / Diff / Commands

**Received:** 2026-04-30, user-relayed Remote 105 update.

### 9.1 Git State

```text
Git SHA: fbfda71018eae5078968aa6f7faba0ae5b2d5ead

Git Status:
 M eval_fresh_instances_vit.py
?? eval_t105e_noise_off.py
?? checkpoints/_gpt/
?? report_md/_gpt/json_gpt/*_fresh_eval.json
?? report_md/_gpt/json_gpt/*_noise_off.json

Git Diff --stat:
 eval_fresh_instances_vit.py | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
```

Environment repeated:

```text
Python: 3.11.15
PyTorch: 2.4.1+cu121
CUDA: 12.1
timm: 1.0.26
GPU: 8x NVIDIA PH402 SKU 200
```

Codex judgment: this substantially improves reproducibility, but final paper use still needs either exact command/config for every cell or a compact table showing only `arch`, `hat-type`, `seed`, and checkpoint path differ across cells.

### 9.2 Exact Command Templates Received

Training example:

```bash
conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch deit_small_patch16_224 --hat-type proportional \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed 456 --device cuda --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet
```

Fresh eval example:

```bash
conda run -n hat python -u eval_fresh_instances_vit.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/deit_small_patch16_224_proportional_seed456/best.pt \
  --device cuda
```

T105-E noise-off example:

```bash
conda run -n hat python -u eval_t105e_noise_off.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/deit_small_patch16_224_proportional_seed456/best.pt \
  --device cuda
```

### 9.3 Updated Gate Status

| Gate | Status | Comment |
|---|---|---|
| G105-1 naming semantics | **closed** | Source = best epoch `test_acc`. |
| G105-2 same-arch digital | partially closed | seeds 123/456 done; seed789 pending. |
| G105-3 multi-seed | open | seed789 pending. |
| G105-4 fresh protocol | **closed enough for review** | 10 x 5, D2D per instance, C2C per forward. |
| G105-5 reproducibility | **substantially closed, not final** | SHA/status/diff/env/command templates received; need per-cell exact config table in final. |

### 9.4 Immediate 105 Request

When seed789 returns, include one final table:

```text
arch, hat_type, seed, train_command_or_config_hash, source_test_acc, fresh_mean, fresh_std, checkpoint_path
```

This is enough for Opus/Codex to judge whether 105 can enter paper-1 supplement.
