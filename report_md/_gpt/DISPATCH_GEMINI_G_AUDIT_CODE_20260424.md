# DISPATCH GEMINI G-AUDIT-CODE — Independent Code Audit at Commit 9cdbe77
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Gemini (ERROR-FINDING MODE ONLY per BROADCAST_REBUILD_3WEEK)
**Priority:** HIGH (final bug-insurance before submission)
**Depends on:** None — standalone code inspection
**Time budget:** unconstrained

---

## 1. Objective

Perform an **independent static audit** of the two core analog layer files at commit `9cdbe77` (the post-fix code). Goal: hunt for a **third bug** or any remaining latent correctness issue before we commit to the post-fix narrative across the whole paper. This is the **final bug-insurance layer**.

You are NOT designing experiments, writing theory, or editing papers. You are auditing code. Three things: correctness, edge cases, numerical stability.

---

## 2. Files in scope

Audit these at commit `9cdbe77`:

1. `analog_layers.py` — MLP-path analog CIM primitive with STE
2. `analog_layers_ensemble.py` — Ensemble HAT wrapper with per-epoch D2D resampling
3. `test_dual_bug_fix.py` — test suite currently passing 5/5
4. `test_groupwise_nl_wrapper.py` — test suite currently passing 8/8

---

## 3. Specific checks (you must do ALL of these, do not skip)

### 3.1 LTP/LTD branch consistency under all NL values

The known bug 1 was LTP/LTD branch swap. Verify at commit 9cdbe77:
- Under `grad_output >= 0` (LTP branch): conductance increase formula uses `(1 - g_norm)^(1/NL_LTP)` scaling. Confirm `NL_LTP > 0` assumed and handled.
- Under `grad_output < 0` (LTD branch): conductance decrease formula uses `g_norm^(1/|NL_LTD|)` scaling. Confirm `NL_LTD` sign convention (should be negative) is handled consistently.
- At `NL_LTP = 1.0, NL_LTD = -1.0` (canonical): both branches should reduce to linear STE. Verify this both analytically and via small symbolic test.
- At `NL_LTP = 2.0, NL_LTD = -2.0` (severe): both branches use proper nonlinear scaling. Verify there is no sign-flip or missing absolute-value.

### 3.2 Second-order Taylor correction

The known bug 2 was an extraneous `nl` multiplier in the second-order correction. Verify:
- The second-order term (if still present) has no stray multiplicative factor.
- Taylor expansion derivation in code comments (if any) matches the code.
- At NL=1, second-order correction should vanish (pow(x, NL-1) = 1 dependency). Verify.

### 3.3 Numerical stability near boundaries

Check behavior near these conductance values:
- `g = 0` (fully reset): does `g^(1/NL)` or `(1-g)^(1/NL)` cause NaN/Inf for NL > 1? Look for clipping / epsilon.
- `g = 1` (fully set): symmetric concern with `(1-g)^(1/NL)`.
- `g = g_min = 0.0...` epsilon: gradient should not explode.
- Under AMP (mixed precision): fp16 underflow in `pow(small_ratio, NL-1)`. Check for upcast to fp32 around critical ops.

### 3.4 Gradient-flow correctness in STE

Straight-through estimator: forward uses quantized/nonlinear transform, backward uses identity or corrected gradient. Verify:
- `torch.autograd` bookkeeping is correct — `.detach()` or `torch.no_grad()` on the right side.
- Gradient magnitudes reasonable: compute analytical Jacobian at a few points and compare to autograd output via `torch.autograd.gradcheck`.
- No gradient leakage through device-noise tensors (C2C noise should not have grad).

### 3.5 Ensemble mask resampling

In `analog_layers_ensemble.py`:
- Mask `M` is sampled from `N(0, σ_D2D²)` — verify **zero mean** (not biased).
- Resampling schedule: per-epoch (NOT per-batch). Check the hook point. CX-regression test checks this, but confirm it directly.
- Mask shape matches weight shape — no broadcasting error that could collapse the mask to 1D accidentally.
- Multi-GPU / DataParallel scenarios: does each GPU see a consistent mask within an epoch? If not, flag as a concurrency correctness issue.

### 3.6 Noise injection order

There are C2C noise (per-read), D2D mismatch (per-device), and ADC quantization. Verify the **order of operations**:
- Expected: `W_effective = (W_ideal * (1 + M_D2D)) + ξ_C2C`, then ADC-quantize the output current, then scale-recovery (inverse gain calibration).
- Check code matches this order. Order matters: C2C INSIDE D2D is different from C2C OUTSIDE D2D.

### 3.7 Scale recovery calibration

Paper's Eq.~\ref{eq:scale-recovery} describes scale recovery. Verify:
- The gain calibration constant is computed from the noise-free state (not from a noisy forward pass).
- Scale recovery is applied AFTER ADC quantization, BEFORE downstream layers.
- In `--noise-mode proportional`, the scale recovery is still meaningful (the calibrated gain is not annihilated by state-dependent noise).

### 3.8 Configuration flag consistency

Check that `exp_cfg` fields saved with checkpoints correctly record:
- `nl_ltp`, `nl_ltd` (both, not just one)
- `noise_mode` ("uniform" / "proportional" / "measured" placeholder)
- `hat_training` (True = Ensemble, False = Standard — confirm this encoding)
- `sigma_d2d`, `sigma_c2c`
- `batch_size`, `seed`, `amp_enabled`

The CX-REGRESSION guard already checks these — verify it's actually wired to every training script, not just some.

---

## 4. Output format

Produce `GEMINI_G_AUDIT_CODE_20260424.md` with the following structure:

```markdown
# Gemini G-AUDIT-CODE Report
Commit audited: 9cdbe77
Auditor: Gemini
Date: <YYYY-MM-DD>

## Summary
- Total checks performed: N
- Pass: N
- Fail: N
- Flag-for-review: N

## Per-check results

### Check 3.1 LTP/LTD branch consistency
- Status: PASS / FAIL / FLAG
- File:line reference: analog_layers.py:L123-L145
- Finding: ...
- Recommended action (if FAIL/FLAG): ...

### Check 3.2 Second-order Taylor correction
(same structure)

... (repeat for all 8 checks 3.1-3.8)

## Latent issues found (if any)
<List any issue outside the 8 checks, with severity High/Moderate/Low and file:line.>

## Third-bug hypothesis
<If you found or suspect a third bug, describe it here with reproducer. If nothing found, state "No third bug identified under the checks performed.">

## Recommendations
<Ordered list of any follow-up audit steps.>
```

---

## 5. Constraints and discipline

- **Static audit only.** Do not run experiments. Read code, reason symbolically, run small unit test reproductions if needed.
- **Independence principle**: Do not read Codex's CX-AUDIT-1 before producing your findings. Deliver your report first, then Claude will cross-reference. This is a BLIND second opinion.
- **No new theory**, no paper edits, no experiment design — you are in error-finding mode per BROADCAST_REBUILD_3WEEK §3.
- **Report negative findings honestly**: if 8/8 checks pass and no third bug found, say so. A clean audit report is as valuable as a bug-catching one.
- **File:line discipline**: every finding must cite a specific file and line range. No vague "something in the noise code looks off".

---

## 6. What makes this audit succeed

A report that either:
- (a) identifies a real correctness issue we missed — we fix it and re-run regression guards; or
- (b) cleanly confirms no third bug under 8 specific checks — we cite this report in Supp Note S-Verification as the third-party audit layer.

Either outcome is publishable infrastructure.

---

## 7. Delivery

1. Write report to `report_md/_gpt/GEMINI_G_AUDIT_CODE_20260424.md`.
2. Append status block to `AGENT_SYNC_gpt.md`.
3. Flag Claude via one-line summary in `AGENT_INTERCOM_HUB_20260424.md`.

**No time budget.** Do it thoroughly.
