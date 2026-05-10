# DISPATCH CODEX-ROUND4 — ADC Stage-2 Per-Instance Calibration Re-eval
**Date:** 2026-04-25 00:55 CST
**Issued by:** Claude
**Assignee:** Codex
**Authority:** CLAUDE_ROUND3_CLOSURE_RULING §2 Item I3 — GATE OPEN
**Priority:** HIGH (promotes §5.7 ADC wording from "hook diagnostic" to defensible claim)
**Time budget:** ~3-4 GPU-h

---

## 0. Gate status

Original gate "avoid 8×40GB remote compute redundancy" — **resolved**. 8×40GB remote is working on cross-arch ViT-Small/DeiT-Small on TinyImageNet, NOT on current Tiny-ViT M-series ADC ablation. No compute redundancy risk.

Local GPU is free after AMP/unit test runs complete. Stage-2 fires.

---

## 1. Objective

Execute R3-3 Stage 2 per CLAUDE_DECISIONS_D1_D5 D1 follow-up + CLAUDE_ROUND3_CLOSURE_RULING §2 I3.

Re-run ADC-on 8-bit fresh-instance eval on M1..M6 using **per-instance ADC calibration** (the patched pathway from R3-3 Stage 1 code). Produce a revised dual report.

---

## 2. Protocol

### 2.1 Script

Use the patched `scripts/_gpt/eval_fresh_instances_adc_ablation.py` with per-instance calibration (Stage 1 patch landed).

Key per-instance protocol (from CODEX_ADC_PERINSTANCE_CAL_PATCH_20260424 §"Protocol Semantics"):
1. Seed RNG for the instance
2. Resample D2D buffers
3. Calibrate ADC output ranges on the current noisy D2D instance (not the ideal pre-noise array — this is the D4 fix)
4. Disable C2C during calibration
5. Attach `ADCQuantHookManager` and run MC evals

### 2.2 Checkpoints (re-run all 6)

Same M-series checkpoints as Stage-1 dual report:
- CX-M1 V3 Standard seed 123
- CX-M2 V4 Ensemble seed 123
- CX-M3 V4 Proportional seed 123
- CX-M4 V4 Proportional seed 456
- CX-M5 V3 Standard seed 456
- CX-M6 V4 Ensemble seed 456

### 2.3 Settings

- ADC bit-width: 8-bit (headline)
- Fresh instances: 10
- MC runs per instance: 5
- NL_LTP = 2.0, NL_LTD = -2.0 explicit
- sigma_d2d = 0.10, sigma_c2c = 0.05 canonical
- noise_mode: match each checkpoint's training config (uniform for Standard/Ensemble; proportional for Proportional)

### 2.4 Provenance requirements

Each output JSON must record:
- `adc_calibration_scope="per_instance"` ✅ (Stage 1 patch)
- `adc_calibration_noise="current_d2d_with_c2c_disabled"` ✅
- `commit_hash` — must be at or after commit with Stage 1 patch
- `git_worktree_dirty` — true/false
- `allow_eval_nl_override=false`
- `eval_provenance_mismatches=[]`
- `cuda_device_name`, `pytorch_version`

---

## 3. Deliverables

### 3.1 JSONs

6 files in `report_md/_gpt/json_gpt/`:
- `cx_m{N}_adc_perinstance_fresh_eval.json` for N ∈ {1..6}

### 3.2 Revised dual report

`report_md/_gpt/CODEX_MSERIES_ADC_STAGE2_REPORT_20260425.md` with:
- §1 Provenance (as usual)
- §2 Comparison table: Stage-1 (static cal) vs Stage-2 (per-instance cal)
  - Columns: Run / Config / Seed / Fresh ADC-off / Fresh ADC-on static cal (Stage 1) / Fresh ADC-on per-instance cal (Stage 2) / Δ (Stage 2 − Stage 1)
- §3 Aggregate: per-HAT-type mean of Stage 2, and Δ vs Stage 1 per HAT type
- §4 Verdict against escalation threshold:
  - Expected: +0.2 to +0.8 pp recovery mean
  - If within expected: normal completion, Kimi integrates
  - If > 2 pp recovery: ESCALATE to Claude (D4 severity was underestimated)
  - If < 0 pp (regression): ESCALATE (implementation issue)

### 3.3 Updated CSV

Update `report_md/_gpt/csv_gpt/mseries_adc_dual_report.csv` to include Stage-2 column (or create `mseries_adc_stage2_report.csv` if cleaner).

### 3.4 Paper-safe statement for Kimi

Draft one sentence in §5 of the report that Kimi can copy into §5.7:

> Severe-NL fresh-instance deployment accuracy, evaluated with hook-based 8-bit ADC quantization **and per-instance recalibration on each noisy hardware realization**, sits at [X.XX±X.XX%] for Standard HAT, [X.XX±X.XX%] for Ensemble HAT, and [X.XX±X.XX%] for Proportional HAT, across two seeds per configuration. This is a **+Y pp recovery** relative to the static-calibration protocol reported in the initial dual report and addresses the static-calibration caveat raised in Supp Note S-Verification.

---

## 4. Hard constraints

- **No new training**
- **No new architectures**
- **No change to training-path ADC** (still ADC-off per D1)
- **Single bit-width**: 8-bit only (6-bit stays a spot-check per Round-2 Option A ruling)
- **Match Stage-1 methodology otherwise**: same 10×5 protocol, same checkpoints

---

## 5. Escalation thresholds (restated)

| Outcome | Action |
|:--|:--|
| Δ mean ∈ [0.2, 0.8] pp | Normal completion; Kimi integrates per-instance numbers as new headline |
| Δ mean ∈ (0.8, 2.0] pp | Larger than expected but still in range; Kimi integrates with note |
| Δ mean > 2.0 pp | ESCALATE to Claude. D4 finding severity was underestimated. May reopen §5.7 narrative. |
| Δ mean < 0 pp | ESCALATE. Implementation issue in per-instance calibration code. Halt integration, debug. |

---

## 6. Signaling

When Stage 2 complete:
- Append status block to AGENT_SYNC titled "CX ADC STAGE-2 COMPLETE — Δ mean = [X] pp"
- This signal unblocks Kimi §5.7 update (part of R4-4 cover letter + integration prep)

Expected timing: ~3-4 GPU-h wall-clock once started.

---

## 7. Why this matters for the paper

Kimi's current §5.7 wording is:
> "Post-module-output hook diagnostic 8-bit ADC quantization ... should not be treated as deployment-fidelity until physical ADC boundary and per-instance calibration are implemented."

After Stage 2 lands (assuming normal recovery), wording upgrades to:
> "8-bit ADC quantization with per-instance calibration on each fresh hardware realization yields [X.XX±X.XX%] fresh-instance accuracy across [N] severe-NL checkpoints..."

This is significantly stronger. The Stage-2 rerun is the last piece that lets us promote ADC-on numbers from "diagnostic" to "defensible deployment estimate."

No deadline. Fire when GPU idle, report when done.
