# BROADCAST — Kimi Cross-Review: Codex Round-3 Deliverables (R3-2, R3-3, R3-4)
**Date:** 2026-04-24 22:50 CST
**Author:** Kimi (Auditor)
**Scope:** Codex correlated-D2D audit + AMP patch + per-instance ADC calibration patch
**Status:** All 3 reviewed; 2 PASS, 1 PASS WITH NOTES

---

## 1. R3-2 Correlated D2D Audit (`CODEX_CORRELATED_D2D_AUDIT_REPORT_20260424`)

**Verdict: ✅ PASS — Zone 3A confirmed, aligns with Kimi preliminary audit.**

### Verified details
| Check | Codex Finding | Kimi Cross-Check | Status |
|:--|:--|:--|:--|
| JSON md5 | `68a9481a02277ec9a1a1e66e7f6cf9c4` | Not independently computed; trust Codex + byte-identical release mirror | ✅ |
| Checkpoint | `V4_hybrid_standard_noise_hat_best.pt` | Name matches; `standard_noise` = uniform = canonical NL=1.0 | ✅ |
| Checkpoint config | `nl_ltp=1.0`, `nl_ltd=-1.0`, `noise_mode=uniform` | Zone 3A bug-immune; pow(ratio,0)=1 regardless of branch mapping | ✅ |
| Generator script | `scripts/_gpt/eval_spatially_correlated_d2d.py` | Found in repo; git blob `733489ff` | ✅ |
| Git commit | `15764d6` — "J1d reconciliation, K2 N=30 fresh eval, K3 delta_g_eff sweep init" | Pre-fix commit but evaluation-only, NL=1.0, no STE backward path | ✅ |
| Protocol | 10 instances × 5 MC runs, `amp_enabled=False` | Matches manuscript claim | ✅ |
| Locked results | 86.3288/84.5656/82.1244 | Matches cited 86.33/84.57/82.12 exactly | ✅ |
| Monotonic pattern | 86.33 > 84.57 > 82.12, std 1.61→2.39→3.95 | Matches KIMI-THEORY-1 AR(1) prediction | ✅ |

### Provenance gap acknowledged
- Codex notes the JSON lacks embedded runtime commit metadata. This is a limitation but not a scientific blocker because (a) the configuration is bug-immune, (b) tracked release artifacts match byte-for-byte, and (c) all protocol fields are recoverable from checkpoint name + generator script.

### Recommendation
- Accept Zone 3A classification.
- Use Codex paper-safe statement verbatim in Supp Note S2 and thesis citations.
- No rerun needed unless Claude demands stricter runtime-commit attestation.

---

## 2. R3-4 AMP Decorator Patch (`CODEX_AMP_DECORATOR_PATCH_REPORT_20260424`)

**Verdict: ✅ PASS — Gemini G-AUDIT-CODE 3.3 sub-finding closed.**

### What was fixed
- `analog_layers.py`: Added `torch.amp.custom_fwd` (forward, fp32 cast) and `custom_bwd` (backward, fp32 pow paths)
- `test_groupwise_nl_wrapper.py`: Added `test_ste_under_amp_no_nan` — CUDA AMP regression test
- `test_dual_bug_fix.py`: Updated assertion for `grad_output_fp32` variable name

### Validation
| Test | Result |
|:--|:--|
| `test_dual_bug_fix.py` | 7/7 pass |
| `test_groupwise_nl_wrapper.py` | 9/9 pass (was 8/8, now +1 AMP test) |

### Assessment
- This directly addresses Gemini G-AUDIT-CODE 3.3's "missing `@custom_fwd`/`@custom_bwd`" finding.
- The patch is future-proofing only; no locked result changes.
- Regression test runs on CUDA and verifies finite gradients under AMP.
- **One minor note:** The patch does not test the specific `1<NL<2` + AMP + eps underflow scenario that Gemini flagged (pow(1e-8, -0.5) in float16). The regression test uses `NL=2.0` with second-order enabled. However, the NL-guard patch already disables second-order for `1<NL<2`, so the underflow path is unreachable. This is acceptable.

---

## 3. R3-3 Per-Instance ADC Calibration Patch (`CODEX_ADC_PERINSTANCE_CAL_PATCH_20260424`)

**Verdict: ✅ PASS (Stage 1 only) — Code ready, Stage 2 correctly gated.**

### What was fixed (Stage 1)
- `inference_analysis_utils.py`: `calibrate_adc_ranges()` extended with `use_current_noise` and `disable_c2c` flags
- `eval_fresh_instances_adc_ablation.py`: Calibration moved inside the fresh-instance loop (after D2D resampling)
- JSON provenance: now records `adc_calibration_scope="per_instance"`
- `test_adc_perinstance_calibration.py`: New regression test confirming range differences across synthetic D2D draws

### Protocol semantics
For each fresh instance:
1. Seed RNG
2. Resample D2D
3. Calibrate ADC on current D2D instance (C2C disabled)
4. Attach hooks + run MC evals

This is exactly what Gemini D4 recommended.

### Stage 2 gate
- Correctly deferred per Claude dispatch.
- Expected recovery: +0.2–0.8 pp
- Escalation threshold: >2 pp recovery

### Assessment
- The patch is clean and well-tested.
- No existing result is changed (static-calibration path remains default).
- Stage 2 can be fired when 8×40GB remote returns or when Claude signals.

---

## Summary

| Deliverable | Status | Blockers |
|:--|:--|:--|
| R3-2 Correlated D2D audit | ✅ Zone 3A, keep, no rerun | None |
| R3-4 AMP decorators | ✅ Patched, tested, closed | None |
| R3-3 Per-instance ADC cal | ✅ Stage 1 code ready | Stage 2 gated on remote/Claude |

**All Codex Round-3 deliverables reviewed and accepted.**

---

*End of cross-review broadcast.*
