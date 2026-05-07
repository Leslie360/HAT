# P3 Pythia-2.8B Scale Check — 2026-05-08

**Status:** Complete — seed42 + seed123 trained and evaluated.

---

## 1. Method

Model: `EleutherAI/pythia-2.8b-deduped` (32 layers, last1 = layer 31).

Training:
- 100 steps, lr=1e-5, batch_size=1
- D2D=0.02, C2C=0.0, n_states=256
- analog_layers = [31]
- **Selective optimizer:** Only patched attention layer params optimized (memory fix for 32GB GPU)

Evaluations:
- D2D=0.02 (3 eval seeds)
- D2D=0.05 (3 eval seeds)

---

## 2. Results

### Seed 42

| Eval D2D | Eval seed | PPL |
|:---:|:---:|:---:|
| 0.02 | 42 | 13.31 |
| 0.02 | 456 | 13.34 |
| 0.02 | 1001 | 13.34 |
| **0.02 mean** | — | **13.33** |
| 0.05 | 42 | 13.41 |
| 0.05 | 456 | 13.42 |
| 0.05 | 1001 | 13.44 |
| **0.05 mean** | — | **13.43** |

### Seed 123

| Eval D2D | Eval seed | PPL |
|:---:|:---:|:---:|
| 0.02 | 42 | 13.34 |
| 0.02 | 456 | 13.34 |
| 0.02 | 1001 | 13.34 |
| **0.02 mean** | — | **13.34** |
| 0.05 | 42 | 13.42 |
| 0.05 | 456 | 13.44 |
| 0.05 | 1001 | 13.45 |
| **0.05 mean** | — | **13.44** |

---

## 3. Interpretation

### 3.1 Result replicates across train seeds

| Train seed | D2D=0.02 mean | D2D=0.05 mean |
|:---:|:---:|:---:|
| 42 | 13.33 | 13.43 |
| 123 | 13.34 | 13.44 |
| Δ | +0.01 | +0.01 |

The difference between train seeds is negligible (~0.01 PPL), well within eval seed variance.

### 3.2 Scale advantage over Pythia-1B

| Model | D2D=0.02 mean | D2D=0.05 mean |
|:---:|:---:|:---:|
| Pythia-410M | ~19.46 | ~19.62 |
| Pythia-1B | 14.60 | 14.80 |
| Pythia-2.8B | **13.34** | **13.44** |

Compared to Pythia-1B last1 (D2D=0.02 ≈14.6 PPL), Pythia-2.8B last1 achieves **13.34 PPL** — an additional **1.26 PPL improvement**.

Compared to Pythia-410M last1 (D2D=0.02 ≈19.5 PPL), Pythia-2.8B achieves a massive **6.1 PPL improvement**.

This confirms that analog KV cache viability **continues to improve with model scale**. The trend 410M → 1B → 2.8B shows monotonic PPL gains.

### 3.3 D2D=0.05 viability

D2D=0.05 adds only ~+0.10 PPL over D2D=0.02 at the 2.8B scale, indicating robust noise tolerance. This is significantly lower than the ~+0.20 PPL overhead observed at 1B scale.

---

## 4. Files

- Checkpoints:
  - `HAT_kv107/paper2/results/remote107/checkpoints/p2d8b_last1_d2d002_seed42`
  - `HAT_kv107/paper2/results/remote107/checkpoints/p2d8b_last1_d2d002_seed123`
- Training metadata:
  - `HAT_kv107/paper2/results/remote107/p2d8b_last1_d2d002_seed42.json`
  - `HAT_kv107/paper2/results/remote107/p2d8b_last1_d2d002_seed123.json`
- Eval results: `deliverable/results_v3/p2d8b_2d8b/*.json` (12 files)

---

## 5. Verdict

**LOCK** for Pythia-2.8B selective terminal-layer analog KV.

| Claim | Status | Value |
|:---|:---:|:---|
| Cross-seed reproducibility | **PASS** | Δ < 0.02 PPL |
| D2D=0.02 viability | **PASS** | ~13.34 PPL |
| D2D=0.05 viability | **PASS** | ~13.44 PPL |
| Scale advantage vs 1B | **PASS** | +1.26 PPL better |
| Scale advantage vs 410M | **PASS** | +6.1 PPL better |
