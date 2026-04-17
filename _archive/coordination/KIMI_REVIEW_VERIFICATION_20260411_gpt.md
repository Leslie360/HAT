# Kimi Review Verification - 2026-04-11

**Owner:** Codex  
**Purpose:** Verify whether Kimi's 4.10 reviewer synthesis and handoff still match the actual manuscript and experiment state.

## Bottom line

Kimi's pass was **good at finding issue families**, but **not fully reliable as a live status tracker**.

Safe interpretation:

- `issue discovery`: mostly useful
- `current-state tracking`: partially stale
- `recommended use`: reviewer checklist, not source of truth

## What was re-checked

We cross-checked Kimi's notes against:

1. `report_md/审稿人意见-4.10.md`
2. Current manuscript sources under `paper/latex_gpt/`
3. Current sync / coverage docs
4. Actual experiment logs, especially:
   - `logs/_gpt/p13_aihwkit_full_cifar10_gpu_r2.log`
   - `logs/_gpt/p13_runtime_heartbeat.log`

## Verified findings

### 1. Kimi correctly identified the major reviewer themes

These concerns were real and worth acting on:

- statistical rigor / multi-seed expectations
- energy-model transparency
- AIHWKIT / inorganic-toolkit comparison pressure
- canonical parameter provenance
- clarity issues such as V1--V8 notation, stale wording, year mismatches, and table annotations

So as a **reviewer-intent summary**, Kimi was directionally correct.

### 2. Kimi's task-state tracking is now outdated

Several items flagged as pending in the Kimi handoff are no longer pending:

- **AIHWKIT shared-regime sanity check is complete**
  - evidence: `logs/_gpt/p13_aihwkit_full_cifar10_gpu_r2.log`
  - final result: digital `95.46%`, AIHWKIT proxy `90.08 ± 0.21%`, delta `-5.38%`
  - manuscript landing: `paper/latex_gpt/supplementary.tex`

- **P13 is finished, not still running**
  - evidence: `logs/_gpt/p13_runtime_heartbeat.log`
  - watcher stop recorded at `2026-04-10 22:36:05`

- **Several wording/year fixes are already landed**
  - `single-run estimate` marker for ConvNeXt--Flowers-102
  - Zhang / Vincze year cleanup in reviewer-facing prose
  - removal of `still being accumulated`
  - removal of reviewer-facing wording such as `Reviewer feedback repeatedly emphasized`

### 3. The manuscript is cleaner than the old Kimi handoff implies

Verified via repository-wide searches:

- no `and others` / `Author et al.` / `TBD` / `TODO` placeholders in manuscript sources or bibliography
- no reviewer-facing prose such as `during review` or `Reviewer feedback`
- no LaTeX log hits for undefined references/citations in current `main.log` and `supplementary_main.log`

## What is truly closed

### Closed A. AIHWKIT comparison pressure

Not expanded into a full ViT head-to-head, but a **bounded shared-regime sanity check now exists and is explicitly scoped as such**. The paper no longer overclaims equivalence.

### Closed B. Energy-model transparency

Now explicitly documented:

- `E_analog-MAC = 100 fJ`
- `E_ADC,8b = 25 fJ`
- `E_DAC,8b = 30 fJ`
- `t_ADC,8b = 100 ns`
- `SAR-like 8-bit readout proxy`

These appear in:

- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/supplementary.tex`

The main text also now qualifies `11.45x` as an **upper-bound** and gives routing-overhead sensitivity bounds down to `9.90x`.

### Closed C. Stale wording / annotation issues

Closed examples:

- `still being accumulated` removed
- `33.22%*` explicitly explained as a `single-run estimate`
- `10.00%` formatting normalized
- reviewer-facing prose removed from supplement/appendix

## What is only partially closed

### Partial 1. Statistical rigor

Key claims now have reported uncertainty, but we should **not overstate this as universal multi-seed closure**.

Safe wording:

- the paper has strong statistics for its central claims
- some auxiliary/control claims remain explicitly labeled as single-run or bounded sanity checks

### Partial 2. Absolute energy comparison

Current state is defensible:

- FP32-referenced `11.45x` is explicitly labeled an upper-bound
- routing-overhead sensitivity is quantified
- INT8 context is discussed

What is **not** present:

- a fully matched chip-to-chip head-to-head against a concrete commercial NPU under identical workload conditions

### Partial 3. Physical validation depth

The manuscript is still:

- literature-calibrated
- first-order behavioral
- not pulse-accurate
- not directly validated against a lab-measured closed-loop deployment

That limitation is disclosed, but it remains real.

## Where Kimi became misleading

### 1. Old pending tasks still presented as blocking

This is the main issue. The handoff still described P13 and several text fixes as unfinished after they had already been completed.

### 2. AIHWKIT ask framed too rigidly

Reviewer pressure was about **shared-regime numerical sanity**, not necessarily a full ViT replication. The present response uses a bounded ResNet-18 shared-regime benchmark, which is weaker than a full ViT comparison but still materially responsive.

### 3. Issue discovery got mixed with readiness judgment

Kimi was good at identifying concerns, but its `ready / blocking` judgment should not be trusted without manuscript/log verification.

## Practical policy

Use Kimi outputs in this project as:

- good reviewer-signal mining
- good pressure-testing
- not authoritative state tracking

Source of truth should remain:

1. manuscript source
2. experiment logs
3. `REVIEWER_COVERAGE_MATRIX_gpt.md`
4. `AGENT_SYNC_gpt.md`

## Final verdict

Kimi did **not** badly read the reviewer comments, but it **did partially misrepresent the current execution state** by leaving already-completed fixes and experiments in a pending/blocking posture.

Safe summary:

- `review interpretation`: mostly useful
- `status bookkeeping`: needs Codex verification
- `current manuscript state`: ahead of the Kimi handoff
