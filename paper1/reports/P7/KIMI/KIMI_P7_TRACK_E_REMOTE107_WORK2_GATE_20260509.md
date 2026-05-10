# Kimi P7 Track E: Remote 107 Work-2 Gate

**Date:** 2026-05-09
**Scope:** Analog KV-cache for LLM inference — Work-2 only
**Status:** Strong Work-2 direction; NEVER Paper-1

---

## 1. Local Clone Status

| Item | Value |
|------|-------|
| Local review path | `HAT_107_clean_review/` |
| Remote branch | `107-clean` |
| Freeze commit | `cc0a3ab` (canonical freeze), `c154392` (latest with CORE_MATH_REPRO_PACKET) |
| Latest remote commit | `a0e7f92` (2026-05-09) |

---

## 2. Corrected-Noise Rerun Status

**Complete.** All P0–P3 experiments finished.

| Phase | Status | Key Result |
|-------|--------|------------|
| P0A — Baseline verification | ✅ Complete | Canonical baseline = 22.18 PPL |
| P0B — Paired ablations | ✅ Complete | 3 train seeds × 4 modes (B1–B4) |
| P1 — Layer scope (K107-A) | ✅ Complete | last1=19.45, last2=20.14, all=37.13 |
| P2 — Retention sweep (K107-B) | ✅ Complete | Periodic refresh improves ~0.3 PPL |
| P2 — n_states sweep (K107-C) | ✅ Complete | n_states=64 optimal, 256 production |
| P2 — EPSC stress | ✅ Complete | All pass (max 20.76 @ σ=0.15) |
| P3 — Scale check | ✅ Complete | Pythia-1B (14.60), 2.8B (13.34) |
| P3 — 2.8B C2C sweep | ✅ Complete | σ_c2c=0.10 adds only +0.26 PPL |
| P3 — 2.8B EPSC | ✅ Complete | σ=0.15 → 13.91 PPL |

---

## 3. Core Mathematical/Noise Code Regions

These must be archived for Work-2 reproducibility:

| File/Region | Purpose | Location on 107-clean |
|-------------|---------|----------------------|
| `p3_hat_train.py:67-78` | Conductance mapping (differential pair) | `analogize_kv_tensor` |
| `p3_hat_train.py:80-88` | Quantization (STE with NL scaling) | Forward write path |
| `analog_layers.py:170-289` | NL scaling backward | LTP/LTD branch |
| `p3_hat_train.py` | C2C injection equation | `inject_c2c_noise` |
| `p3_hat_train.py` | D2D injection equation | `inject_d2d_noise` |
| `p3_hat_train.py` | Retention equation | `apply_retention_drift` |
| `eval_llm_kv_cache.py` | Sliding-window PPL scoring | ctx=512, stride=256, bs=1 |

**Archive recommendation:** Snapshot these files into `work2_107_repro_archive/` with git commit hash and env metadata.

---

## 4. Required Metadata Template

For every 107 result used in Work-2:

| Field | Required Value |
|-------|---------------|
| Git commit | `cc0a3ab` or later |
| Branch | `107-clean` |
| Python | 3.11.15 |
| PyTorch | 2.4.1+cu121 |
| CUDA | 12.1 |
| Model | `EleutherAI/pythia-410m-deduped` (canonical) |
| Dataset | `wikitext-2-raw-v1` test split |
| Context length | 512 |
| Stride | 256 |
| Batch size | 1 |
| Analog layers | `last1` (layer 23) for 410M |
| Noise config | `sigma_d2d=0.02`, `sigma_c2c=0.0`, `n_states=256` (nominal) |
| Train seeds | 42, 123, 456 |
| Eval seeds | 42, 456, 1001 |
| Checkpoint path | `checkpoints/_gpt/cross_arch_tinyimagenet/...` |
| JSON path | `deliverable/results_v3/...` |

---

## 5. Work-2 Narrative Gate

**Terminal-layer selective HAT is promising IF:**

| Condition | Required | Actual | Pass |
|-----------|----------|--------|------|
| Corrected-noise last1 PPL ≤ 25 | ✅ Yes | 19.45 @ D2D=0.02 | ✅ PASS |
| Corrected-noise last2 PPL ≤ 25 | ✅ Yes | 20.14 @ D2D=0.02 | ✅ PASS |
| All-layer PPL catastrophic | ✅ Yes | 37.13 @ D2D=0.02 | ✅ PASS |
| HAT training improves clean digital | ✅ Yes | 22.18 → 19.04 (−3.1 PPL) | ✅ PASS |
| Analog patch overhead negligible | ✅ Yes | +0.02 PPL (B1→B2) | ✅ PASS |
| Physical noise overhead modest | ✅ Yes | +0.42 PPL (B2→B3) | ✅ PASS |
| Scale trend favorable | ✅ Yes | Improves with model size | ✅ PASS |

**Narrative gate: OPEN.** Work-2 manuscript can proceed.

---

## 6. Classification

| Claim | Classification | Rationale |
|-------|----------------|-----------|
| 107 selective KV-cache viable | `work2-kv-cache` → **Work-2 main claim** | Strong evidence, 3 seeds, multiple sweeps |
| 107 all-layer analog KV | `exclude` | Catastrophic (37+ PPL), permanently abandoned |
| 107 scale-up (1B/2.8B) | `work2-kv-cache` | Improves with scale, strengthens narrative |
| 107 vs Paper-1 | **Strictly separate** | No 107 content in Paper-1 |

---

## 7. GitHub-Safe Task File

`report_md/_gpt/REMOTE_107_PHASE_P7_CORRECTED_NOISE_AND_METADATA_TASKLIST_20260509.md`

Content: Archive core math code, ensure metadata template compliance, prepare Work-2 manuscript outline.

---

## 8. Verdict

| Check | Result |
|-------|--------|
| Local clone/branch recorded | ✅ 107-clean, cc0a3ab |
| Corrected-noise data complete | ✅ P0–P3 all finished |
| Core math code identified | ✅ 7 regions mapped |
| Metadata template complete | ✅ 15 fields |
| Work-2 narrative gate | ✅ OPEN |
| Paper-1 separation | ✅ Verified — no 107 in Paper-1 |

**Track E Status: COMPLETE — 107 is Work-2 ready.**

---

*Report by kimi. 2026-05-09.*
