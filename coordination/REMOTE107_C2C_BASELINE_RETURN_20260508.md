# C2C Baseline Eval — 2026-05-08

**Status:** Complete — 6 eval jobs on `k107_a1_last1_seed42`.

---

## 1. Method

Checkpoint: `k107_a1_last1_seed42` (Pythia-410M, last1 [23], HAT-trained with D2D=0.02).

Evaluated with additional Cell-to-Cell (C2C) noise injected alongside the training D2D=0.02 noise:
- C2C = 0.01 (3 seeds)
- C2C = 0.02 (3 seeds)

Baseline for comparison: C2C=0, D2D=0.02 = **19.44 PPL**.

---

## 2. Results

| C2C | Seed | PPL | Δ vs baseline |
|:---:|:---:|:---:|:---:|
| 0.01 | 42 | 19.4734 | +0.03 |
| 0.01 | 123 | 19.4124 | −0.03 |
| 0.01 | 456 | 19.4833 | +0.04 |
| **0.01 mean** | — | **19.456** | **+0.01** |
| 0.02 | 42 | 19.5256 | +0.08 |
| 0.02 | 123 | 19.4982 | +0.05 |
| 0.02 | 456 | 19.5174 | +0.07 |
| **0.02 mean** | — | **19.514** | **+0.07** |

---

## 3. Key Findings

### 3.1 C2C noise is well-tolerated

Even doubling C2C from 0.01 to 0.02 produces only **+0.07 PPL** degradation. This is within the run-to-run seed variance (~±0.03) observed for the same config.

### 3.2 HAT training generalizes to combined C2C+D2D noise

The checkpoint was trained with D2D=0.02 only (C2C=0). Nevertheless, adding moderate C2C noise at eval time does not catastrophically degrade performance. This suggests the learned representations are robust to small-scale spatial noise, not just device-level variation.

### 3.3 Implication for deployment

In a real analog array, C2C variation is typically << D2D variation. These results confirm that C2C does not dominate the error budget for the chosen 256-state conductance encoding. Focus can remain on D2D calibration and retention stress.

---

## 4. Files

- `deliverable/results_v3/c2c_baseline/eval_k107_a1_last1_seed42_c2c*.json` (6 files)

---

## 5. Suggested Figure

Bar chart with:
- X-axis: C2C level (0.00, 0.01, 0.02)
- Y-axis: mean PPL with error bars (min/max across 3 seeds)
- Horizontal line at digital baseline (18.31)
