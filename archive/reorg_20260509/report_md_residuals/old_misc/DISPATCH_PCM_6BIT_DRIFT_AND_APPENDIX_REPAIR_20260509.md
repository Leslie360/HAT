# DISPATCH — PCM 6-bit Drift Closure + Appendix Content Repair

**Date:** 2026-05-09
**Issued by:** Codex
**Priority:** P0 / blocking for Paper-1 data and supplementary freeze
**Applies to:** Kimi, DS, Mimo, Gemini, Codex

---

## 0. Supersedes Previous Dispatch

This dispatch **supersedes and cancels**:

`report_md/_gpt/DISPATCH_KIMI_PCM_CORRECTED_EVAL_20260509.md`

Reason: DS corrected the bug diagnosis. The earlier 9-checkpoint eval-only queue is a no-op. The eval path was already correct; the critical mismatch was in the training-time protocol for 6-bit PCM.

Do **not** spend GPU or human time re-running the nine old 4/6/8-bit fresh evals unless a later auditor produces new evidence.

---

## 1. Canonical PCM Status After DS + Kimi Reconciliation

### 1.1 Valid / Invalid Numbers

| Precision | Fresh Mean | Seed Std | Drift Status | Current Ruling |
|---|---:|---:|---|---|
| 4-bit PCM | 76.68% | ~0.4% | 0→24h drop about 4 pp | Keep old canonical numbers |
| 5-bit PCM | ~63% | n/a | non-frontier | Kill; no seed expansion |
| 6-bit PCM | 68.55% | 6.03% | incomplete for new protocol | Replace old 77.86%; needs drift closure |
| 8-bit PCM | 77.60% | ~0.8% | ~0 pp | Keep old canonical numbers |

### 1.2 Narrative Ruling

The old claim **"6-bit is the Pareto midpoint / sweet spot" is dead**.

Use this replacement framing:

- **8-bit PCM:** strongest practical PCM operating point; high fresh accuracy and stable drift.
- **4-bit PCM:** aggressive low-precision regime; good fresh accuracy but material drift penalty.
- **6-bit PCM:** seed-sensitive transition zone; lower mean, high variance, drift-stable but not Pareto-dominant.
- **5-bit PCM:** non-frontier; killed.

The non-monotonic pattern `4-bit high -> 6-bit dip -> 8-bit high` should be treated as a physical quantization-D2D interaction, not as a plotting mistake.

---

## 2. Kimi Task — 6-bit Drift Closure

### Objective

Complete the missing drift evaluation for **new-protocol 6-bit PCM checkpoints**.

### Required Inputs

Use these current new-protocol checkpoint directories:

```text
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/
```

Known current state:

| Seed | fresh_eval.json | training_history.json | drift_eval.json |
|---:|---|---|---|
| 123 | present | missing | present |
| 456 | present | present | missing |
| 457 | present | present | missing |
| 789 | present | present | missing |

### Required Work

1. Run drift eval for seeds `456`, `457`, and `789` only.
2. Preserve existing files. If overwriting is unavoidable, first copy the old file to a timestamped backup.
3. Use the same drift protocol as seed123 and the canonical 4/8-bit drift evaluations.
4. Confirm the output JSON records:
   - checkpoint path
   - precision / resolution
   - seed
   - drift times
   - accuracies at each time
   - tile audit / RPU config fields if available
5. Write a short report to:

```text
report_md/_gpt/KIMI_6BIT_DRIFT_CLOSURE_20260509.md
```

### Report Must Include

| Seed | Fresh | Drift t=0 | Drift t=1h | Drift t=24h | 0→24h drop | Verdict |
|---:|---:|---:|---:|---:|---:|---|
| 123 | existing | existing | existing | existing | existing | already available |
| 456 | fill | fill | fill | fill | fill | new |
| 457 | fill | fill | fill | fill | fill | new |
| 789 | fill | fill | fill | fill | fill | new |

Also provide the 4-seed mean/std for fresh and the 4-seed mean/std for 24h drift drop.

### Kill Criteria

Stop and broadcast immediately if any new 6-bit drift result shows:

- 0→24h drop worse than 2 pp, or
- fresh/drift mismatch larger than 3 pp at t=0, or
- checkpoint metadata contradicts `enable_during_test=True`.

---

## 3. DS Task — Protocol Audit Follow-up

### Objective

Close the remaining protocol risk after the PCM correction.

### Required Work

1. Audit IdealDevice / digital ablation eval paths for analogous train/eval noise-protocol mismatch.
2. Confirm whether Table 1 / Table 2 digital and IdealDevice results are affected or unaffected.
3. Check that all paper-facing PCM numbers now cite the correct source files.
4. Verify that the old `77.86%` 6-bit number is no longer used as a canonical result.
5. Verify that the earlier eval-only dispatch is marked obsolete in downstream reports.

### Output

Write:

```text
report_md/_gpt/DS_IDEALDEVICE_AND_PCM_PROTOCOL_AUDIT_20260509.md
```

Use this verdict format:

```text
PASS / CONDITIONAL PASS / FAIL
```

A PASS requires explicit file-path evidence, not only reasoning.

---

## 4. Mimo Task — Narrative and Reviewer-Risk Repair

### Objective

Prepare the reviewer-safe narrative after the 6-bit midpoint collapse.

### Required Work

1. Replace the old midpoint story with the new three-regime PCM story:
   - 4-bit: quantization-dominated / drift-costly
   - 6-bit: D2D-sensitive transition zone
   - 8-bit: deployment-stable practical point
2. Identify every place in main text, appendix, captions, tables, and response notes where `6-bit`, `Pareto`, `midpoint`, or `sweet spot` appears.
3. For each occurrence, classify it as:
   - keep
   - soften
   - rewrite
   - delete
4. Produce a hostile-review paragraph: what a reviewer would attack after seeing `68.55 ± 6.03%`.
5. Propose replacement wording for the Results paragraph and the relevant supplementary caption.

### Output

Write:

```text
report_md/_gpt/MIMO_PCM_NARRATIVE_REPAIR_20260509.md
```

---

## 5. Appendix Content Repair After Gemini Figure Pass

Gemini owns visual figure editing under user direction. Other agents must **not** redraw or restyle figures unless explicitly told.

The next task is content-level appendix repair after Gemini's visual pass.

### 5.1 Kimi Appendix Task — Mechanical Consistency

Check the supplementary LaTeX and source data for:

1. Figure numbering `S1`–`S21` has no gaps, duplicates, or stale references.
2. Every panel label `A/B/C/D` matches the caption and in-text reference.
3. Every table cell is either filled or explicitly marked `n.e.` / `not evaluated` with a note.
4. Percent vs decimal format is consistent.
5. Units are consistent: pp, %, h, s, epochs, seeds.
6. All abbreviations are expanded on first use in the supplement: PCM, D2D, C2C, HAT, ADC, DAC, PPL, KV, MC.
7. Captions describe the result without excessive discussion.
8. No obsolete 6-bit midpoint wording remains.

Output:

```text
report_md/_gpt/KIMI_APPENDIX_CONTENT_CONSISTENCY_20260509.md
```

### 5.2 DS Appendix Task — Data Integrity

Audit that every appendix figure/table value matches its source JSON/CSV/MD.

Required columns:

| Figure/Table | Displayed value | Source file | Source key/row | Match? | Notes |
|---|---:|---|---|---|---|

Special attention:

- S-figures containing PCM 4/6/8-bit precision ladder.
- Any table still using old 6-bit `77.86%`.
- Any drift plot using old 6-bit backup directories.
- Any `fresh mean ± std` values copied manually.

Output:

```text
report_md/_gpt/DS_APPENDIX_DATA_INTEGRITY_AUDIT_20260509.md
```

### 5.3 Mimo Appendix Task — Readability / Reviewer Lens

Review the supplement as a hostile reviewer, but do not edit figures directly.

Check:

1. Is any appendix section too verbose for what the data says?
2. Are any equations non-original and unnecessary in the main explanatory flow?
3. Are figure captions doing too much interpretation?
4. Are any visual conclusions under-supported by the numbers?
5. Does the appendix clearly separate completed experiments from killed / not-evaluated experiments?

Output:

```text
report_md/_gpt/MIMO_APPENDIX_REVIEWER_RISK_AUDIT_20260509.md
```

### 5.4 Gemini Boundary

Gemini may continue visual refinement, but data semantics are frozen unless the user or Codex issues a new data patch. If Gemini changes a figure asset, it must leave enough provenance for Kimi/DS to map each panel to source data.

---

## 6. Codex Integration Task

Codex will integrate reports after Kimi/DS/Mimo finish:

1. Decide final PCM wording.
2. Update the paper task queue.
3. Mark old 6-bit claims obsolete.
4. Check appendix consistency before any final paper freeze.
5. Broadcast final acceptance / required rework.

No final freeze is allowed until:

- 6-bit drift closure exists for seeds 456/457/789, and
- DS IdealDevice audit returns PASS or CONDITIONAL PASS with bounded caveats, and
- appendix content audit confirms no stale 6-bit midpoint claims.

---

## 7. One-Line Execution Summary

Cancel old eval-only PCM queue; complete only new-protocol 6-bit drift data; audit IdealDevice protocol; rewrite PCM story around 8-bit dominance and 6-bit transition behavior; then run appendix content/data/readability audits after Gemini's visual pass.
