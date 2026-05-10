# Kimi P6 Track F Report: Remote 107 KV-Cache Closure Package (Updated)

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md`
**Executor:** kimi
**Update:** 2026-05-09 — canonical freeze ingested from 107-clean branch

---

## 1. Data Status — COMPLETE (P0–P3)

**Model:** EleutherAI/pythia-410m-deduped (canonical)
**Evaluator:** `p3_hat_train.evaluate_ppl` (ctx=512, stride=256, batch_size=1)
**Status:** Server recovered. P0B, K107-A, K107-B, K107-C, EPSC stress, and scale checks all complete.

### Baseline Reconciliation

| Protocol | Baseline PPL | Status |
|---|---|---|
| Legacy v1 (ctx=1024/stride=512/bs=8) | 15.62 | **Deprecated** |
| Canonical (ctx=512/stride=256/bs=1) | **22.1849** | Active |

> All gains reported below are relative to the **canonical baseline** (22.18 PPL) or the **HAT-fine-tuned digital patched baseline** (~19.04 PPL).

---

## 2. P0B Paired Ablations — Complete

3 train seeds (42, 123, 456), 4 modes per seed.

| Mode | Description | Mean PPL | Key Finding |
|---|---|---|---|
| B1 | HAT-fine-tuned digital (no patch) | 19.043 | Clean digital after HAT training |
| B2 | Patch ON, no noise | 19.060 | Patch overhead = **+0.02 PPL** (lossless) |
| B3 | Patch ON, D2D=0.02 | 19.483 | Nominal noise = **+0.42 PPL** vs B2 |
| B4 | Patch ON, D2D=0.05 | 19.644 | High noise = **+0.58 PPL** vs B2 |

**HAT regularization gain:** Training under analog noise improves clean digital PPL by **~3.1 points** (22.18 → 19.04).

**Kill criterion:** PPL < 25. All pass comfortably.

---

## 3. Layer Scope Sweep (K107-A)

Analog layers at D2D=0.02, C2C=0.0, n_states=256.

| Scope | D2D=0.02 | D2D=0.04 | D2D=0.05 |
|---|---|---|---|
| last1 (layer 23) | **19.451 ± 0.065** | 19.577 ± 0.063 | 19.621 ± 0.064 |
| last2 (layers 22–23) | 20.142 ± 0.052 | 20.468 ± 0.051 | 20.586 ± 0.054 |
| all (layers 0–23) | 37.132 ± 0.878 | 68.478 ± 4.332 | 104.289 ± 8.928 |

**Route decision:** All-layer analog KV-cache **abandoned** (catastrophic). Selective terminal-layer (last1) is the only viable path. Last2 degrades ~0.7 PPL.

---

## 4. Retention Sweep (K107-B)

| Scope | D2D | 0s | 0.1s | 1.0s | 10.0s |
|---|---|---|---|---|---|
| last1 | 0.02 | 19.444 | 19.168 | 19.168 | 19.168 |
| last1 | 0.05 | 19.604 | 19.251 | 19.251 | 19.251 |
| all | 0.02 | 35.807 | 177.098 | 176.115 | 176.059 |

**Finding:** Periodic refresh **improves** PPL for last1 by ~0.3 PPL. Full-model analog still collapses regardless of refresh.

---

## 5. n_states Sweep (K107-C)

| n_states | D2D=0.02 | D2D=0.05 |
|---|---|---|
| 16 | 19.585 ± 0.020 | 19.702 ± 0.024 |
| 32 | 19.487 ± 0.033 | 19.631 ± 0.020 |
| 64 | **19.398 ± 0.034** | 19.560 ± 0.022 |
| 128 | 19.451 ± 0.039 | 19.622 ± 0.024 |
| 256 | 19.458 ± 0.040 | 19.603 ± 0.037 |

**Finding:** n_states=64 achieves best PPL at D2D=0.02 (19.40). n_states=256 is within 0.06 PPL and chosen for production precision headroom.

---

## 6. EPSC Stress (Device-Agnostic Proxy)

| Config | σ_c2c | σ_d2d | Mean PPL | Max PPL | Status |
|---|---|---|---|---|---|
| EPSC-e1 | 0.05 | 0.05 | 19.718 ± 0.061 | 19.814 | PASS |
| EPSC-e2 | 0.10 | 0.10 | 20.116 ± 0.070 | 20.231 | PASS |
| EPSC-e3 | 0.15 | 0.15 | 20.762 ± 0.073 | 20.869 | PASS |
| EPSC-e4 | 0.00 | 0.20 | 20.604 ± 0.094 | 20.754 | PASS |
| EPSC-e5 | 0.01 | 0.10 | 19.861 ± 0.068 | 19.974 | PASS |

**Kill criterion:** PPL < 25. All configs pass. Maximum stress (σ=0.15) yields 20.76 PPL — only +1.3 PPL above nominal.

---

## 7. Scale Check — Pythia Family

| Model | D2D=0.02 | D2D=0.05 | vs 410M | Trend |
|---|---|---|---|---|
| Pythia-410M | 19.48 | 19.64 | — | Baseline |
| Pythia-1B | 14.60 | 14.82 | −4.88 | Improves |
| Pythia-2.8B | 13.34 | 13.44 | −6.14 | Improves |

**Pythia-2.8B C2C sensitivity:** Even σ_c2c=0.10 adds only +0.26 PPL. EPSC stress at σ=0.15 yields 13.91 PPL — superior noise tolerance vs 410M scale.

**Finding:** Analog KV viability **improves with model scale**.

---

## 8. CORE_MATH_REPRO_PACKET (2026-05-09)

11-section document covering:
1. Conductance mapping formula (differential pair)
2. Quantization formula (STE with NL scaling)
3. C2C injection equation
4. D2D injection equation
5. Retention equation
6. Seed handling protocol
7. Sliding-window PPL scoring
8. Train/test split proof
9. Context-length sweep math
10. Cross-seed variance analysis
11. Reproducibility checklist

Available on 107-clean branch at `CORE_MATH_REPRO_PACKET_20260509.md`.

---

## 9. Verdict

| Item | Status |
|------|--------|
| Local smoke | Pass |
| Corrected-noise rerun | **Complete** (P0B done, 3 seeds) |
| HAT effectiveness | **Strong** — HAT training improves clean digital by ~3.1 PPL |
| Selective-layer route | **Locked** — last1 only (19.45 PPL @ D2D=0.02) |
| Generalization | EPSC stress all pass; C2C sweep complete |
| Scale trend | Confirmed — improves with model size |
| Work-2 decision | **Ready for Work-2 manuscript** |

**Classification update:**
- 107 selective KV-cache with HAT: `work2-kv-cache` → **active Work-2 candidate**
- Pythia-2.8B results: `future-only` → **Work-2 main text candidate**
- All-layer analog KV: `exclude` (permanently abandoned)

**Paper-1 status:** No 107 content in Paper-1. All 107 data is Work-2 only.

---

## 10. Source Files

- `coordination/REMOTE107_K107_CANONICAL_FREEZE_20260508.md` — master freeze
- `coordination/REMOTE107_P0B_ABLATION_RETURN_20260508.md` — P0B raw data
- `coordination/REMOTE107_K107_A_RETURN_20260508.md` — layer scope
- `coordination/REMOTE107_K107_B_RETURN_20260508.md` — retention
- `coordination/REMOTE107_K107_C_RETURN_20260508.md` — n_states
- `coordination/REMOTE107_P1_EPSC_RETURN_20260508.md` — EPSC stress
- `coordination/REMOTE107_P3_P2D8B_RETURN_20260508.md` — Pythia-2.8B
- `CORE_MATH_REPRO_PACKET_20260509.md` — math repro packet
- Branch: `107-clean`, freeze commit: `cc0a3ab`

---

*Report by kimi. Updated on 2026-05-09 with complete canonical freeze from 107-clean.*
