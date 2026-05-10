# DS Audit: IdealDevice / Digital Eval Protocol + Paper-Facing PCM Source References

**Date:** 2026-05-09
**Auditor:** DS (per Codex dispatch 2026-05-09T12:15)
**Scope:**
  1. Audit IdealDevice/digital ablation eval paths for analogous train/eval noise-protocol mismatch
  2. Confirm Table 1 / Table 2 digital and IdealDevice results affected status
  3. Check all paper-facing PCM numbers cite correct source files
  4. Verify old 77.86% 6-bit number no longer used as canonical
  5. Verify old eval-only dispatch marked obsolete

---

## Part 1: IdealDevice / Digital Ablation Protocol Audit

### Verdict: **PASS** — No protocol mismatch affecting published numbers.

### 1.1 Eval Path

All IdealDevice and digital ablation numbers in Tables 1–3 of the paper are generated via the **same** `eval_aihwkit_fresh.py` script that PCM numbers use. This script always:
- Builds the model from scratch with `cfg.modifier.enable_during_test = True` (line 34)
- Applies post-load RPU config re-application (lines 140-153)
- Runs 10 fresh instances × 5 MC passes

### 1.2 Training Scripts — All Use `enable_during_test=False`

| Training Script | Line | `enable_during_test` |
|----------------|------|---------------------|
| `r11d1_train.py` (IdealDevice baseline) | 85 | `False` |
| `train_aihwkit_baseline.py` (HAT variants) | 86 | `False` |
| `r11d_hat_pcm.py` | 129, 133 | `False` |
| `r11d_adaptive_noise_train.py` | 123 | `False` |

This is the same bug pattern as PCM — training-time test eval runs noise-free.

### 1.3 Why IdealDevice Numbers Are NOT Affected

Same physical mechanism as 4-bit and 8-bit PCM: quantization resolution dominates at the extremes.

**IdealDevice 4-bit baseline (14.64%):**
- inp_res = out_res = 1/16 = 0.0625
- Training best = 15.01% vs Fresh eval = 14.64% → diff = **0.37 pp** ✅
- At 4-bit resolution, quantization noise is ~6.25% of full range. ADD_NORMAL (std_dev=0.1) is comparable but not decisive. The near-collapse to 14.64% is caused by quantization + D2D mismatch, not by `enable_during_test` flag.

**IdealDevice 8-bit baseline (87.28%):**
- inp_res = out_res = 1/256 = 0.00390625
- Training best ≈ Fresh eval (no meaningful gap)
- At 8-bit, residual noise is absorbed by fine quantization grid.

**Ensemble HAT 4-bit (86.16%):**
- The mechanism preventing overfit is epoch-level D2D mask resampling (Eq. 4 in paper), not the `enable_during_test` flag.
- Fresh eval is correct regardless of training-time `enable_during_test`.

**Digital reference (98.06%) / Hybrid baseline (97.39%):**
- These use `InferenceRPUConfig` but with `modifier.type = WeightModifierType.NONE` (no noise).
- `enable_during_test` is irrelevant when no noise modifier is configured.

### 1.4 Source File Verification

| Paper Value | Source Checkpoint | Source File | Match? |
|------------|------------------|-------------|--------|
| 87.28 ± 0.13% | `checkpoints/best.pt` | `checkpoints/fresh_eval.json` | ✅ mean=87.28% |
| 14.64 ± 0.11% | `r11d_1_4bit/best.pt` | `r11d_1_4bit/fresh_eval.json` | ✅ mean=14.64% |
| 86.16 ± 0.19% | Ensemble HAT 4-bit (3-seed aggregate) | training_history (individual) + fresh_eval (aggregate) | ✅ Computed from seed-level data |
| 98.06 ± 0.14% | Digital ref (non-RPU baseline) | training_history.json | ✅ Verified |
| 97.39 ± 0.08% | Hybrid baseline | training_history.json | ✅ Verified |
| 10.00 ± 0.00% | Fixed-mask HAT 4-bit | training_history.json | ✅ Verified (algorithmic floor) |

---

## Part 2: Paper-Facing PCM Source References — Full Cross-Reference

### 2.1 Main Text PCM Precision Ladder (Table: `tab:pcm_precision_ladder`)

| Row | Paper Value | Source Data | Status |
|-----|------------|-------------|--------|
| 8-bit PCM Fresh | 77.60% | 3-seed mean of fresh_eval.jsons | ✅ CORRECT |
| 8-bit PCM 1h | 77.59% | drift_eval.jsons | ✅ CORRECT |
| 8-bit PCM 24h | 77.56% | drift_eval.jsons | ✅ CORRECT |
| 8-bit Δ Drift | 0.04 pp | computed | ✅ CORRECT |
| **6-bit PCM Fresh** | **77.86%** | **old-protocol backup checkpoints** | **❌ STALE — must be 68.55%** |
| **6-bit PCM 1h** | **77.83%** | **old-protocol** | **❌ STALE** |
| **6-bit PCM 24h** | **77.76%** | **old-protocol** | **❌ STALE** |
| **6-bit Δ Drift** | **0.10 pp** | **old-protocol** | **❌ STALE** |
| **6-bit Role** | **"Pareto midpoint"** | **narrative** | **❌ STALE — claim dead** |
| 4-bit PCM Fresh | 76.68% | 3-seed mean of fresh_eval.jsons | ✅ CORRECT |
| 4-bit PCM 1h | 75.43% | drift_eval.jsons | ✅ CORRECT |
| 4-bit PCM 24h | 72.67% | drift_eval.jsons | ✅ CORRECT |
| 4-bit Δ Drift | 4.01 pp | computed | ✅ CORRECT |

### 2.2 Supplementary PCM Tables

| Location | Content | Status |
|----------|---------|--------|
| `tab:supp_8bit_pcm` | 8-bit per-seed table | ✅ CORRECT (all values match source) |
| **`tab:supp_6bit_pcm`** | **"3-seed Mean: 77.88%, Fresh: 77.86%, Drop: 0.10 pp"** | **❌ STALE — entire table uses old-protocol backups** |
| `tab:supp_4bit_pcm` | 4-bit per-seed table | ✅ CORRECT (all values match source) |
| `subsec:supp-late-recovery` | "reaches 78.49%" (seed456) | **❌ STALE — uses seed456_full100 old-protocol checkpoint** |
| `tab:supp_provenance` | 6-bit checkpoint paths | **⚠️ PARTIALLY STALE — seed456 points to `_full100` old-protocol; seed123/789 dir names are same but content now retrained** |

### 2.3 Stale 6-bit "Pareto Midpoint" / "77.86%" Occurrences

| File | Line | Phrase | Action |
|------|------|-------|--------|
| `00_abstract.tex` | 3 | "6-bit PCM preserves near-8-bit drift stability... best observed Pareto midpoint" | REWRITE |
| `01_introduction.tex` | 9 | "6-bit PCM provides the best observed Pareto midpoint" | REWRITE |
| `05_results.tex` | Table 2 | "77.86%... Pareto midpoint" | REWRITE |
| `05_results.tex` | 82 | "6-bit is the best observed Pareto midpoint, with 77.86% fresh accuracy" | REWRITE |
| `06_discussion.tex` | 10 | "6-bit precision emerges as a critical Pareto midpoint" | REWRITE |
| `06_discussion.tex` | 41 | "verify whether the 6-bit midpoint persists" | SOFTEN (keep as open question) |
| `07_conclusion.tex` | 7 | "6-bit emerges as the best observed Pareto midpoint" | REWRITE |
| `cover_letter.tex` | 29, 52 | "best observed Pareto midpoint, maintaining 77.86±0.56%" | REWRITE |

**Total stale references:** **10** locations across 7 files.

### 2.4 Fresh 6-bit State (for replacement)

| Seed | Checkpoint | Fresh Mean | Drift 0→24h | Status |
|------|-----------|-----------|-------------|--------|
| 123 | `r11d_6bit_pcm_seed123` | 68.93% | ~0 pp (existing) | ✅ Retrained, drift complete |
| 456 | `r11d_6bit_pcm_seed456` | 62.47% | pending | ✅ Retrained, **drift needed** |
| 457 | `r11d_6bit_pcm_seed457` | 76.69% | pending | ✅ Retrained, **drift needed** |
| 789 | `r11d_6bit_pcm_seed789` | 66.13% | pending | ✅ Retrained, **drift needed** |
| **4-seed mean** | | **68.55%** | ± 6.03% std | |

---

## Part 3: Old Dispatch Obsolete Status

### Verdict: ✅ **Marked obsolete in Codex's revised dispatch**

- Codex dispatch `DISPATCH_PCM_6BIT_DRIFT_AND_APPENDIX_REPAIR_20260509.md` (2026-05-09T12:15) explicitly states:
  > "This supersedes and cancels" the earlier eval-only dispatch `DISPATCH_KIMI_PCM_CORRECTED_EVAL_20260509.md`
- The revised dispatch correctly identifies the bug as "training-time protocol mismatch," not an eval-script bug.
- The 9-checkpoint eval-only queue is correctly cancelled.

**No downstream report has been written to the earlier dispatch**, so there is nothing to recall. The `DISPATCH_KIMI_PCM_CORRECTED_EVAL_20260509.md` file still exists on disk but is semantically superseded.

---

## Part 4: Appendix Content Data Integrity Preview

Per Codex's specification (Section 5.2), a full appendix data integrity audit is to be performed after Gemini's visual pass. This report identifies the known stale entries that the later audit must catch:

| Figure/Table | Displayed Value | Source File | Match? | Notes |
|---|---|---|---|---|
| S-Table: 6-bit PCM | 77.86% | old-protocol backup dirs | ❌ | Must be replaced with retrained 68.55% |
| S-Figure: Late Recovery | 78.49% seed456 | `seed456_full100` old-protocol | ❌ | Must be replaced with retrained 62.47% or removed |
| S-Provenance Table | seed456 → `_full100` | checkpoint dir | ❌ | Must point to `r11d_6bit_pcm_seed456` |
| Main Table 2 6-bit row | 77.86%, Pareto midpoint | N/A (stale) | ❌ | Replace with 68.55% or remove row entirely |
| Cover letter | 77.86% | N/A | ❌ | Must be updated |

---

## Part 5: Recommendations

1. **Freeze all paper PCM data edits** until 6-bit drift closure is complete (Kimi task pending).
2. **Mimo should handle the 10 narrative rewrites** — every "Pareto midpoint" and "77.86%" reference must be replaced.
3. **After 6-bit drift closure:** Update Supplementary Table `tab:supp_6bit_pcm` with retrained per-seed values (seed123=68.93%, 456=62.47%, 457=76.69%, 789=66.13%) and new aggregate.
4. **Late recovery section:** The 78.49% value is from old-protocol seed456_full100. Replace with retrained seed456 value (62.47%) or delete the section entirely (the "late recovery" claim was protocol-dependent).
5. **Provenance table:** Update 6-bit seed456 path to `r11d_6bit_pcm_seed456`.
6. **Cover letter:** Update during final submission prep — it's not peer-reviewed content but must be factually correct.

---

## Part 6: Summary Verdict

| Audit Item | Verdict | Evidence |
|-----------|---------|----------|
| IdealDevice eval protocol | **PASS** | Eval script always uses `enable_during_test=True`. Quantization masks noise effects at 4/8-bit extremes. Training best ≈ fresh eval. |
| Digital ablation protocol | **PASS** | No noise modifier configured for digital/hybrid baselines. `enable_during_test` is irrelevant. |
| Table 1 IdealDevice (87.28%, 14.64%, 86.16%) | **PASS** | All values verified against source JSONs. |
| Table 2 ablation (98.06%, 97.39%, 10.00%, 86.16%) | **PASS** | All values verified. |
| Table 2 PCM ladder 4-bit (76.68%) | **PASS** | Values match source, drift data consistent. |
| Table 2 PCM ladder 8-bit (77.60%) | **PASS** | Values match source, drift data consistent. |
| **Table 2 PCM ladder 6-bit (77.86%)** | **❌ FAIL** | **Stale value. Must be replaced with 68.55%.** |
| Supplementary 6-bit table | **❌ FAIL** | **Entire table stale.** |
| Supplementary late-recovery | **❌ FAIL** | **Uses old-protocol checkpoint.** |
| Supplementary provenance 6-bit | **⚠️ PARTIAL** | seed456 path points to old-protocol dir. |
| All "Pareto midpoint" / "77.86%" references | **❌ FAIL** | **10 occurrences across 7 files.** |
| Old dispatch marked obsolete | **✅ PASS** | Codex revised dispatch explicitly supersedes. |

---

*Report by DS. Data cross-referenced from fresh_eval.json (9 PCM + 3 IdealDevice), training_history.json (13 checkpoints), drift_eval.json (10 checkpoints), and paper LaTeX sources (7 .tex files).*
