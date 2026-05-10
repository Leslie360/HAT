# Broadcast: Post-Fix Rerun Decision

**Date:** 2026-04-23 22:30 CST
**Decision authority:** User (qiaosir)
**Executed by:** Kimi Code CLI
**Status:** ACTIVE — Rerun queue launched

---

## Decision Summary

After review of Codex independent final review (`CODEX_FINAL_REVIEW_20260423.md`) and discussion of the dual-bug invalidation matrix (`KIMI_DUAL_BUG_INVALIDATION_MATRIX_20260423.md`), the user has decided:

> **We will rerun all key experiments on post-fix code rather than attempting to salvage pre-fix results.**

This is the correct research-integrity decision. Pre-fix training results involving `NL != 1` or second-order STE are contaminated by:
1. Branch swap bug (`grad_output >= 0` mapped to `ltd_scale` instead of `ltp_scale`)
2. Extraneous `nl` multiplier bug (`nl*(nl-1)` instead of `(nl-1)`)

R1 clean anchor (first-order V4 standard) already completed: **34.5612±8.7878%** fresh-instance transfer.

---

## Immediate Actions

### 1. Code State Confirmation
- Git HEAD: `33bed9c` (tertiary bug fix: SO2 branch mapping)
- Working tree: dirty (paper edits staged)
- `analog_layers.py` verified: all three bugs fixed (branch swap, extraneous nl multiplier, SO2 branch mapping)
- `test_dual_bug_fix.py`: all 5 tests pass

### 2. Pre-Fix Data Status

| Result Family | Status | Action |
|:---|:---|:---|
| V4 standard (NL=1) forward-only | ✅ **VALID** | Retain in manuscript |
| V4 severe-NL inference-only (27.72%) | ✅ **VALID** | Retain as forward-only observation |
| Digital FP32 baselines | ✅ **VALID** | Retain |
| Ensemble HAT 86.37±1.54% | ❌ **INVALID** | Rerun required |
| severe-NL retraining 27.72±0.82% | ❌ **INVALID** | Rerun required |
| CX-K2 N=30 38.95±9.85% | ❌ **INVALID** | Rerun required |
| K4 α=0.25 44.29±13.78% | ❌ **INVALID** | Rerun required |
| Joint MLP-linear 30.53±7.07% | ❌ **INVALID** | Rerun required |
| Proportional-noise HAT 97.37±0.05% | ❌ **INVALID** | Rerun required |
| OPECT transfer 88.53±0.08% | ❌ **INVALID** | Rerun required |

### 3. Manuscript Status

- **Current state:** Pre-fix draft with invalid core claims
- **Action:** Mark as "SUPERSEDED — post-fix rerun in progress"
- **Do not submit** until rerun completes and narrative is rewritten

### 4. Rerun Queue (Priority Order)

**P0 — Critical Path (blocks manuscript rewrite):**
1. **Ensemble HAT post-fix** (V4, NL=2.0, epoch-resampled D2D)
   - Same-instance training + 10×5 fresh eval
   - Purpose: Verify if epoch-resampling actually works under clean code

2. **Severe-NL structural limit post-fix** (K2 equivalent)
   - First-order or second-order, NL=2.0
   - N=30 fresh eval if same-instance looks interesting
   - Purpose: Verify structural limit claim

**P1 — Supporting Claims:**
3. Standard HAT baseline (already have R1: 34.56% fresh)
4. Proportional-noise HAT post-fix
5. OPECT literature-profile transfer (needs Ensemble HAT checkpoint)

**P2 — Ablation Matrix:**
6. Joint MLP-linear + Ensemble HAT
7. MLP-only linearization
8. All-linear ablation
9. K4 α sweep (if struct limit confirmed)

---

## Consequences for Other Agents

- **Codex:** Stand by for rerun result review. Figure generation scripts may need updating if new numbers diverge significantly from pre-fix.
- **Claude:** Paper rewrite is **BLOCKED** until P0 rerun completes. Do not proceed with K-SLIM or narrative closure until clean data available.
- **Gemini:** If still active, standby for potential ablation design.

---

## Risk Acknowledgment

Rerun may produce **worse numbers** than pre-fix (R1 already shows ~35% vs old ~86%). This is acceptable. The goal is **true numbers**, not beautiful numbers. If Ensemble HAT under clean code does not significantly outperform standard HAT, we will report that honestly and pivot the narrative to "what we learned about the problem" rather than "what solution we found."

---

*Next update: When first P0 rerun (Ensemble HAT) completes or fails.*
