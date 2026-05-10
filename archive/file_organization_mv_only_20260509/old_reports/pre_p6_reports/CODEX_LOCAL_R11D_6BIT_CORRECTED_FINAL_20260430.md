# Codex Local R11D 6-bit Corrected Final — 2026-04-30

## Executive Verdict

The 6-bit PCM line is **rescued and strong** after the seed456 full-100 diagnostic.

Original seed456 result (`69.07%`) was an early-stop artifact. With the same seed/config but no early stop, seed456 recovers to:

- best test: **78.49%**
- fresh: **78.4716 ± 0.0453%**
- drift 1d: **78.39%**

Therefore 6-bit should be treated as a valid Pareto midpoint candidate, not a failed/unstable line.

## 1. Corrected 6-bit 3-Seed Table

| run_id | seed | epochs | best epoch | best test | fresh mean ± std | drift 0s | drift 1h | drift 1d | 0s→1d drop |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `r11d_6bit_pcm_seed123` | 123 | 100 | 97 | 77.33% | 77.3598 ± 0.0404% | 77.35% | 77.26% | 77.19% | 0.16pp |
| `r11d_6bit_pcm_seed456_full100` | 456 | 100 | 99 | 78.49% | 78.4716 ± 0.0453% | 78.50% | 78.32% | 78.39% | 0.11pp |
| `r11d_6bit_pcm_seed789` | 789 | 100 | 100 | 77.81% | 77.7520 ± 0.0357% | 77.69% | 77.75% | 77.65% | 0.04pp |

## 2. Corrected 6-bit Statistics

| Metric | Mean | Std |
|---|---:|---:|
| Source best | 77.8767% | 0.5829pp |
| Fresh eval | 77.8611% | 0.5639pp |
| Drift 0s | 77.8467% | 0.5908pp |
| Drift 1h | 77.7767% | 0.5305pp |
| Drift 1d | 77.7433% | 0.6054pp |
| Mean drift drop 0s→1d | 0.1033pp | — |

## 3. Precision Comparison After Correction

| Precision | Source best mean ± std | Fresh mean ± std | Drift 0s mean | Drift 1d mean | Mean 0s→1d drop |
|---|---:|---:|---:|---:|---:|
| 8-bit PCM | 77.6400 ± 0.6835% | 77.5953 ± 0.6392% | 77.6133% | 77.5733% | 0.0400pp |
| 6-bit PCM | 77.8767 ± 0.5829% | 77.8611 ± 0.5639% | 77.8467% | 77.7433% | 0.1033pp |
| 4-bit PCM | 76.7067 ± 0.4609% | 76.6836 ± 0.3737% | 76.6433% | 72.6367% | 4.0067pp |

## 4. Interpretation

### What changed

Before the diagnostic, 6-bit looked unstable because seed456 early-stopped at epoch 56 with best 69.07%.

The full-100 rerun shows seed456 had late recovery:

```text
epoch 62: test 72.54%
epoch 75: test 76.20%
epoch 85: test 77.00%
epoch 88: test 77.71%
epoch 94: test 78.21%
epoch 97: test 78.33%
epoch 99: test 78.49%
```

The original early-stop policy killed the run before the late low-LR recovery phase.

### Scientific read

6-bit now has the best aggregate accuracy among the three precision points in this local R11D matrix, while remaining essentially drift-flat at 1 day.

This supports a stronger precision ladder:

- 8-bit: stable high-precision baseline, drift-flat.
- 6-bit: Pareto sweet spot / midpoint, drift-flat and accuracy-competitive.
- 4-bit: still trainable and fresh-stable, but drift-limited over 1 day.

### Paper/narrative implication

Do not frame 6-bit as failed. Frame it as:

> 6-bit PCM preserves 8-bit-like drift immunity and matches or slightly exceeds 8-bit accuracy in this CIFAR-10 local matrix, while 4-bit exposes the precision-drift trade-off.

Caveat:

- The 6-bit result depends on full 100-epoch training; early-stop patience=10 is too aggressive for noisy PCM late recovery.
- Future PCM runs should not use short patience unless the LR schedule has already reached the low-LR recovery phase.

## 5. Operational Rule Update

For local R11D PCM precision-ladder runs:

- Do not use early stopping with patience=10 before validating the late recovery behavior.
- Prefer full 100 epochs for canonical precision-ladder numbers.
- If early stopping is used, set a minimum epoch floor, e.g. no early stop before epoch 90.

## 6. Artifact Paths

```text
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/
```

Key files per run:

```text
training_history.json
fresh_eval.json
drift_eval.json
best.pt
last.pt
```

## 7. Result Status

Status: **CANONICAL for local R11D 6-bit UnitCell precision-ladder comparison**, subject to normal paper-level audit.

Do not use the early-stopped `r11d_6bit_pcm_seed456` in final 6-bit statistics except as an early-stop failure diagnostic.
