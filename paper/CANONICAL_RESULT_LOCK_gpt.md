# ⚠️ 勘误声明 (Erratum) — 2026-04-24

**Task 35 (27.72 ± 0.82% severe-NL) is bug-contaminated and INVALID.**

The `analog_layers.py` STE backward pass contained two bugs affecting all NL≠1.0 training. Fixed at commit `9cdbe77`. Post-fix Standard HAT @ NL=2.0 reaches ~82% (CX-M1 replication pending).

Do not cite Task 35 as evidence. See `report_md/_gpt/BROADCAST_REBUILD_3WEEK_20260424.md` for full audit.

---

# Canonical Result Lock (GPT)

This file records the locked result values and wording boundaries for the English submission package.

Use it during:
- final template migration
- table and caption writing
- Gemini cross-checking against `paper_zh/`

It is intentionally narrower than `MASTER_PLAN.md`: this file is for manuscript wording, not project management.

## 1. Canonical Cross-Dataset Results

These are the primary cross-dataset numbers that support the main paper narrative.

### Tiny-ViT-5M

| Dataset | V1 FP32 | V3 Standard-noise | V4 HAT |
|:--|--:|--:|--:|
| CIFAR-10 | 97.48 | 89.54 | 91.94 |
| CIFAR-100 | 86.94 | 44.06 | 65.48 |
| Flowers-102 | 97.97 | 4.81 | 22.48 |

### ConvNeXt-Tiny

| Dataset | C1 FP32 | C3 Standard-noise | C4 HAT |
|:--|--:|--:|--:|
| CIFAR-10 | 90.74 | 70.48 | 89.91 |
| CIFAR-100 | 64.12 | 23.86 | 60.54 |
| Flowers-102 | 33.22 | 3.79 | 3.35 |

## 2. Best vs Monte Carlo Rule

The paper must not silently mix checkpoint-best values and Monte Carlo means.

### Allowed usage

- `Fig.4` / `Fig.5` and the main cross-dataset narrative:
  - use the canonical **best-checkpoint** values above
- retention, transferability, proportional-noise evaluation, and other explicit stochastic stress tests:
  - use **Monte Carlo mean ± std**

### Important special case

For `ConvNeXt / Flowers-102`, the best-checkpoint and MC values are both relevant:

| Metric family | C3 | C4 |
|:--|--:|--:|
| Best checkpoint | 3.79 | 3.35 |
| MC mean ± std | 1.57 ± 0.83 | 2.03 ± 0.68 |

The manuscript should preserve the distinction instead of collapsing these into a single number.

## 3. Corrected Retention Lock

The corrected Tiny-ViT V4 retention curve is:

| Time | Accuracy (%) |
|:--|--:|
| 0 s | 91.63 |
| 1 s | 82.66 |
| 10 s | 79.13 |
| 100 s | 79.05 |
| 1000 s | 79.35 |
| 10000 s | 79.51 |

Manuscript shorthand:
- `rapid early drop followed by a broad plateau near 79%`

Do **not** reuse the obsolete `84.28%` wording.

## 4. Physical-Extension Result Lock

These belong to the `§5.9` physical-stress narrative and should not be mixed into the canonical cross-dataset grouped bars.

| Task | Locked interpretation | Value |
|:--|:--|:--|
| Task 34 | distribution-matched proportional-noise recovery | `97.37 ± 0.05%` |
| Task 34 transfer | no transfer back to uniform-noise semantics | `10.38 ± 0.44%` |
| Task 35 | nonlinear write remains a major failure mode | `27.72 ± 0.82%` |
| Task 36 | ConvNeXt remains much stronger under proportional-noise HAT | `91.91 ± 0.08%` |

## 5. Locked Wording Boundaries

### Flowers-102

- Write as:
  - `low-data boundary`
  - `data-volume floor for stochastic hardware-aware regularization`
- Do not write as:
  - universal method failure
  - proof that HAT is useless on small datasets

### Task 12 / Fig.10

- Write as:
  - `Zero-Shot Hardware Transferability`
- Do not write as:
  - cross-device peak-performance comparison

### Framework realism

- Keep the manuscript-wide downgrade:
  - `first-order behavioral simulation framework`

### Task 34

- Write as:
  - `distribution-matched recovery`
- Do not write as:
  - universal robustness to all noise laws

### Task 36

- Write as:
  - `architecture-gap evidence under richer physics`
- Do not write as:
  - proof that CNNs are universally robust

## 6. Alignment Note for Gemini

If `paper_zh/` mirrors the English results later, it should follow this file rather than reconstructing numbers from chat history or intermediate logs.
