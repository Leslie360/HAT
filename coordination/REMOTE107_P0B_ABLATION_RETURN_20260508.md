# P0-B Paired HAT Checkpoint Ablations — 2026-05-08

**Status:** Complete — 24 eval jobs across 3 checkpoints.

---

## 1. Method

For each K107-A1 checkpoint (train seeds 42, 123, 456), run 4 paired eval modes:

| Mode | Analog patch | sigma_c2c | sigma_d2d | Eval seeds | Purpose |
|:---:|:---:|:---:|:---:|:---:|:---|
| B1 | OFF | 0 | 0 | 1× | HAT fine-tuned digital checkpoint |
| B2 | ON | 0 | 0 | 1× | Quantization/patch-only overhead |
| B3 | ON | 0 | 0.02 | 3× (42, 456, 1001) | Nominal D2D hardware overhead |
| B4 | ON | 0 | 0.05 | 3× (42, 456, 1001) | High D2D hardware overhead |

Evaluator: `p3_hat_train.evaluate_ppl` (ctx_len=512, stride=256, batch_size=1).

---

## 2. Results

### Seed 42

| Mode | Analog | C2C | D2D | Eval seed | PPL |
|:---:|:---:|:---:|:---:|:---:|:---:|
| B1 | OFF | 0 | 0 | — | 18.99 |
| B2 | ON | 0 | 0 | 42 | 19.01 |
| B3 | ON | 0 | 0.02 | 42 | 19.44 |
| B3 | ON | 0 | 0.02 | 456 | 19.47 |
| B3 | ON | 0 | 0.02 | 1001 | 19.46 |
| B4 | ON | 0 | 0.05 | 42 | 19.60 |
| B4 | ON | 0 | 0.05 | 456 | 19.64 |
| B4 | ON | 0 | 0.05 | 1001 | 19.61 |

### Seed 123

| Mode | Analog | C2C | D2D | Eval seed | PPL |
|:---:|:---:|:---:|:---:|:---:|:---:|
| B1 | OFF | 0 | 0 | — | 19.09 |
| B2 | ON | 0 | 0 | 123 | 19.10 |
| B3 | ON | 0 | 0.02 | 42 | 19.55 |
| B3 | ON | 0 | 0.02 | 456 | 19.56 |
| B3 | ON | 0 | 0.02 | 1001 | 19.56 |
| B4 | ON | 0 | 0.05 | 42 | 19.71 |
| B4 | ON | 0 | 0.05 | 456 | 19.74 |
| B4 | ON | 0 | 0.05 | 1001 | 19.71 |

### Seed 456

| Mode | Analog | C2C | D2D | Eval seed | PPL |
|:---:|:---:|:---:|:---:|:---:|:---:|
| B1 | OFF | 0 | 0 | — | 19.05 |
| B2 | ON | 0 | 0 | 456 | 19.07 |
| B3 | ON | 0 | 0.02 | 42 | 19.43 |
| B3 | ON | 0 | 0.02 | 456 | 19.44 |
| B3 | ON | 0 | 0.02 | 1001 | 19.45 |
| B4 | ON | 0 | 0.05 | 42 | 19.58 |
| B4 | ON | 0 | 0.05 | 456 | 19.59 |
| B4 | ON | 0 | 0.05 | 1001 | 19.59 |

---

## 3. Interpretation

### 3.1 HAT fine-tuning gain (pretrained → B1)

| Train seed | Pretrained digital (22.18) | B1 (HAT-fine-tuned, no patch) | Gain |
|:---:|:---:|:---:|:---:|
| 42 | 22.18 | 18.99 | **−3.19** |
| 123 | 22.18 | 19.09 | **−3.09** |
| 456 | 22.18 | 19.05 | **−3.13** |

HAT training with analog noise improves the **clean digital** PPL by ~3.1 points. This is a strong regularization effect: training under analog noise forces the model to learn more robust representations that generalize better even when the analog patch is removed.

### 3.2 Quantization/patch overhead (B1 → B2)

| Train seed | B1 | B2 | Δ |
|:---:|:---:|:---:|:---:|
| 42 | 18.99 | 19.01 | +0.02 |
| 123 | 19.09 | 19.10 | +0.01 |
| 456 | 19.05 | 19.07 | +0.02 |

The analog KV patch itself (256 states, no noise) adds only **~+0.02 PPL**. This confirms that the multi-level conductance quantization scheme is effectively lossless after HAT training.

### 3.3 Physical D2D noise overhead (B2 → B3/B4)

| Train seed | B2 | B3 mean | B4 mean | Δ B2→B3 | Δ B2→B4 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 42 | 19.01 | 19.46 | 19.62 | +0.45 | +0.61 |
| 123 | 19.10 | 19.56 | 19.72 | +0.46 | +0.62 |
| 456 | 19.07 | 19.44 | 19.59 | +0.37 | +0.52 |

D2D=0.02 adds **~+0.43 PPL**, D2D=0.05 adds **~+0.58 PPL**. The overhead is modest and consistent across train seeds.

### 3.4 Verdict

The analog KV cache is viable because:
1. HAT training **improves** clean performance (regularization gain).
2. The analog patch itself is **effectively lossless** (+0.02 PPL).
3. Physical noise adds only **+0.4–0.6 PPL** at nominal/high D2D.

---

## 4. Files

- `deliverable/results_v3/p0b_ablation/summary.csv`
- `deliverable/results_v3/p0b_ablation/eval_k107_a1_last1_seed*.json` (24 files)
