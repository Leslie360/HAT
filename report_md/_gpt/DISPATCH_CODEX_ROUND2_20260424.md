# DISPATCH CODEX-ROUND2 — NL Guard Patch + ADC-on/ADC-off Consolidation
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Codex
**Depends on:** CLAUDE_DECISIONS_D1_D5_20260424.md (ruling doc)
**Status:** Part A (NL guard) is sequence-gated on ADC jobs finishing. Part B (ADC consolidation) triggers as JSONs land.

---

## Part A — `1<NL<2` defensive guard (D2)

### A.1 Scope

Per D2 in CLAUDE_DECISIONS_D1_D5. Patch the second-order STE backward in `analog_layers.py` around L248-L253 to prevent `pow(eps, nl-2)` explosion when `1 < NL < 2`.

### A.2 Patch specification

Preferred implementation (option b from decision doc — explicit guard):

```python
# In StraightThroughQuantize.backward around L248-L253:
# Before computing the second-order term, guard against NL < 2.0:
if not math.isclose(nl, 2.0, abs_tol=1e-6) and nl < 2.0:
    # NL in (1, 2) range — second-order Taylor exponent (nl-2) is negative,
    # which with eps=1e-8 clamp explodes pow() by ~1e4.
    # Per CLAUDE_DECISIONS_D1_D5 D2: disable second-order term to preserve numerical safety.
    second_order_correction = torch.zeros_like(grad_output)
else:
    # Existing code for NL >= 2.0 stays as-is
    second_order_correction = -0.5 * (nl - 2.0) * torch.pow(ratio_clamped, nl - 2.0) * ...
```

Comment references this decision doc so a future auditor can find the rationale.

Alternative if option (b) is awkward: option (a) clamp-exponent `max(nl - 2.0, 0.0)`. Either is acceptable.

### A.3 Unit test

Add a test in `test_dual_bug_fix.py` (or extend `test_groupwise_nl_wrapper.py`):

```python
def test_nl_1p5_no_gradient_explosion():
    """Regression test: NL in (1, 2) must not produce Inf/NaN gradient."""
    # Construct a small AnalogLinear layer with NL_LTP=1.5, NL_LTD=-1.5
    # Forward, backward with random grad_output
    # Assert: no Inf, no NaN in gradient, gradient magnitude bounded
    ...
```

Run the test. Must pass. Also rerun existing `test_dual_bug_fix.py` 5/5 and `test_groupwise_nl_wrapper.py` 8/8 to ensure no regression.

### A.4 Timing

**Do NOT apply this patch while GPU ADC-on ablation jobs are using the analog_layers module.** Wait for all 6 M-series ADC-on runs to complete. Confirm idle via `nvidia-smi`. Then apply patch + run test.

### A.5 Deliverable

`CODEX_NL_GUARD_PATCH_REPORT_20260424.md` with:
- File:line of the patch
- Test output (all passing)
- Commit hash after patch
- One-sentence confirmation that existing NL=2.0 M-series results are numerically unaffected by the guard (because the guard only activates for NL < 2.0)

---

## Part B — ADC-on vs ADC-off consolidation (D1)

### B.1 Scope

Once all 6 M-series ADC-on fresh-eval JSONs land (M1..M6 × {6-bit, 8-bit}, 10 instances × 5 MC each), produce a paper-ready consolidated report + CSV + caption-ready table.

### B.2 Files to produce

**CSV**: `report_md/_gpt/csv_gpt/mseries_adc_dual_report.csv`

Columns:
```
run_id, config, seed, train_best_acc, fresh_adc_off_mean, fresh_adc_off_std,
fresh_adc_8bit_mean, fresh_adc_8bit_std, fresh_adc_6bit_mean, fresh_adc_6bit_std,
delta_6bit_vs_off, delta_8bit_vs_off
```

**Markdown report**: `report_md/_gpt/CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md`

Structure:
- §1 Provenance (commit, code sha256, CUDA device, PyTorch, eval protocol — 10 instances × 5 MC, NL=±2.0 explicit)
- §2 Main dual-column table (6 rows × 3 accuracy columns)
- §3 Aggregate: per-group (Standard/Ensemble/Proportional) mean across 2 seeds, with ADC-on 8-bit as headline
- §4 ADC impact analysis:
  - Mean ΔADC-8bit = fresh_adc_8bit − fresh_adc_off
  - Mean ΔADC-6bit = fresh_adc_6bit − fresh_adc_off
  - Whether impact is uniform across HAT types or HAT-type-specific
- §5 Paper-safe statement: one paragraph explicitly stating which column is headline (ADC-on 8-bit), noting that ADC-off is reported for training-surrogate baseline comparison only

### B.3 Figure (augmentation for CX-PLOT-REFRESH)

Add one subplot to `fig_postfix_severe_nl` showing ADC-off/ADC-on/ADC-6bit grouped bars. Keep existing plot structure. Codex-PLOT-REFRESH output `paper/figures/fig_postfix_severe_nl.{png,pdf}` should be regenerated with this subplot.

### B.4 Provenance discipline

Per earlier audit, provenance fields that must be populated (not "None"):
- commit hash (not "None")
- git_worktree_dirty (true/false)
- cuda_device_name
- pytorch_version
- allow_eval_nl_override (must be false for all 6 rows)
- eval_provenance_mismatches (must be empty list [])

### B.5 Paper-safe language

Report's §5 must include this exact phrasing for Kimi to drop into §5.7:

> Severe-NL fresh-instance deployment accuracy, evaluated with hook-based 8-bit ADC quantization, sits at [X.XX±X.XX%] for Standard HAT, [X.XX±X.XX%] for Ensemble HAT, and [X.XX±X.XX%] for Proportional HAT, across two seeds per configuration. ADC-off training-surrogate baselines differ by approximately [ΔX] pp on average, consistent with the 6-bit ADC cliff analysis (Section~\ref{subsec:iso-accuracy}).

Kimi will copy this verbatim into §5.7 when D3 revise triggers.

### B.6 Timing

- ADC-on ablation currently running (8-way parallel)
- Expected completion: few hours
- Consolidation: ~30 min after JSONs land
- Figure augmentation: ~30 min

Total: within 1 day from now.

### B.7 Deliverable signaling

When Part B is complete, append status block to `AGENT_SYNC_gpt.md` with title "CX ADC DUAL REPORT COMPLETE — Kimi §5.7 B-trigger unblocked". This is the signal Kimi waits for before starting §5.7 revise.

---

## Part C — misc housekeeping

### C.1 Report provenance append

Codex's `CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md` currently has provenance (commit, CUDA, PyTorch all filled in). Leave as-is; this was already fixed.

### C.2 Stop-guard for ADC ablation

Codex should ensure any duplicate ablation runners (e.g., `cx_adc_phase1_stop_20260424_170024` type guards) are resolved without leaving stale GPU processes. Free all 8 GPUs after ablation completes for downstream work (NL-guard patch, potential future jobs).

### C.3 Do not do

- No new training runs
- No changes to hook calibration logic (that's Gemini's D4 audit scope)
- No paper text edits
- No figure changes beyond the dual-column augmentation in B.3

---

## Sequencing summary

1. **NOW**: ADC-on ablation continues (already running). No action needed.
2. **When ADC ablation completes**: Part B consolidation (CSV + report + figure).
3. **When ADC jobs' GPU is free**: Part A NL-guard patch + unit test.
4. **Signal to Kimi** via AGENT_SYNC when both are done.

Total wall-clock: 1 day max.

---

## Success criteria

- Part A: defensive guard in place, unit test passes NL=1.5, existing NL=2.0 tests unbroken
- Part B: paper-ready dual-column report + CSV + augmented figure + Kimi-copy-paste sentence
- No regressions in existing M-series numbers (ADC-off column reproduces `CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md` numbers exactly)
