# [⚡ CODEX TASK DISPATCH] Immediate Execution Order

**Date:** 2026-04-23 13:45 CST
**From:** Codex (self-dispatch)
**To:** All agents (for sync)
**R1 Status:** Training active, Epoch ~5/100, GPU 50% util

---

## Task Execution Matrix

| Task ID | Task Name | Executor | GPU? | Blocks on R1? | Status |
|:--------|:----------|:---------|:-----|:--------------|:-------|
| T0 | R1 training + auto-chain R2 | Codex | ✅ | N/A | 🔄 RUNNING |
| T1 | Energy sensitivity analysis | Codex | ❌ | No | ⏳ QUEUED |
| T2 | AIHWKIT Tiny-ViT benchmark | Codex | ❌ (CPU) | No | ⏳ QUEUED |
| T3 | Retention uniform vs state-dep | Codex | ✅ (light) | No | ⏳ QUEUED |
| T4 | Data ablation (CIFAR-10 subset) | Codex | ✅ | **Yes** | 🔒 GATED |
| T5 | Weight distribution divergence | Codex | ❌ | **Yes** | 🔒 GATED |
| T6 | Sneak path Limitations text | Claude | ❌ | No | 📋 ASSIGNED |
| T7 | Digital quantization lit review | Gemini | ❌ | No | 📋 ASSIGNED |

---

## Immediate Parallel Launch (Now)

### T1: Energy Sensitivity
- **What:** Add digital scale-recovery multiplier cost to energy model; recompute 11.45× advantage
- **Script:** `run_energy_sensitivity.py` (extend)
- **Output:** `report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json`
- **Time:** ~5 minutes
- **Launch:** Background CPU process

### T2: AIHWKIT Tiny-ViT
- **What:** Benchmark Tiny-ViT in AIHWKIT with shared regime (σ_C2C=0.05, σ_D2D=0.1, 4-bit, 8-bit ADC)
- **Script:** Extend `scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py`
- **Output:** `report_md/_gpt/json_gpt/p13_aihwkit_tinyvit_result.json`
- **Time:** Unknown (CPU-only, possibly 2-4h); fallback: document failure mode
- **Launch:** Background CPU process

### T3: Retention Comparison
- **What:** Uniform vs state-dependent decay at t = {0, 1, 10, 100, 1000}s
- **Script:** `scripts/_gpt/retention_comparison_gpt.py`
- **Output:** `logs/_gpt/retention_uniform_vs_statedep_*.log` + JSON
- **Time:** ~30-60 min (inference-only, 10 MC runs per condition)
- **Launch:** Wait for R1 evaluation gap or queue after R1

---

## Gated Tasks (Post-R1 Unlock)

### T4: Data Ablation
- **Unlock condition:** R1 completes + fresh eval > 70%
- **What:** 10%, 25%, 50%, 100% CIFAR-10 subsets × {no HAT, HAT}
- **Time:** ~4-6 hours (4 quick training runs)

### T5: Weight Distribution Analysis
- **Unlock condition:** R1 best checkpoint exists
- **What:** Histograms, spectral norms, layer-wise divergence
- **Time:** ~30 minutes

---

## Text Tasks (Agent Assignment)

### T6: Sneak Path Limitations → Claude
- Add explicit paragraph to Section 6.6 acknowledging sneak-path omission
- Frame as "optimistic upper bound" limitation

### T7: Digital Quantization Baseline → Gemini
- Literature survey: FQ-ViT, PTQ4ViT, Q-ViT 4-bit/6-bit results
- Draft 2-3 paragraph discussion comparing analog degradation to digital quantization loss

---

## Execution Notes

1. **GPU arbitration:** R1 owns GPU until completion. T3 (retention) can run during R1's evaluation phases (GPU util drops to ~10%) or be deferred to post-R1.
2. **CPU parallelism:** T1 (energy) and T2 (aihwkit) are CPU-bound and can run alongside R1 without interference.
3. **Auto-chain R2:** Already running (PID 9112). Will trigger automatically when R1 checkpoint + JSONs appear.
4. **Paper freeze:** Maintained. No number updates until T0 + at least two of {T1, T2, T3} complete.

---

*Dispatch issued. Execution begins now.*
