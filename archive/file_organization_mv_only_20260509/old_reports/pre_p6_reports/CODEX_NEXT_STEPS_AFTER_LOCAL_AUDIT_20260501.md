# Codex Next Steps After Local Audit — 2026-05-01

## Executive Decision

Do not launch more mandatory local GPU experiments for Paper-1 right now. The local experimental spine is sufficient for the current paper claim.

The next bottleneck is manuscript packaging and figure quality, not missing core data.

## Figure/Table Status

### Qualified Now

- Main precision-ladder table in `paper/latex_gpt/sections/05_results.tex` is numerically qualified.
- SI 8/6/4-bit PCM per-seed tables are qualified after provenance correction.
- SI provenance table is corrected: 6-bit seed789 is `patience=10, not triggered`, not `patience=0`.
- SI late-recovery figure has been added via `paper/latex_gpt/supplementary/fig_late_recovery_tikz.tex`; it is generated directly from raw `training_history.json` values.
- Compile/log status: no undefined refs/citations, fatal errors, overfull warnings, TODO/Placeholder/FIXME hits.

### Not Yet Submission-Strong

- Main text has only one numeric table and no main figure. This is technically valid but weak for a paper submission.
- Existing SI figures are usable as supporting diagnostics, but visually heterogeneous and many belong to the old organic/OPECT/front-end storyline.
- A submission-quality Paper-1 needs at least one main summary figure for the new spine.

Recommended main figure:

1. Panel A: AIHWKit IdealDevice 8-bit robust vs 4-bit collapse vs Ensemble HAT 4-bit rescue.
2. Panel B: PCM 4/6/8-bit fresh accuracy with drift drop overlay.
3. Panel C: 6-bit seed456 late recovery / full-schedule warning, or move this to SI and keep main figure clean.

## Experiment Status

### No More Mandatory Local GPU Experiments

The following are closed enough for Paper-1:

- pure 4-bit collapse;
- Ensemble HAT 4-bit rescue;
- PCM UnitCell 4/6/8-bit 3-seed precision ladder;
- 6-bit full-schedule correction;
- 4-bit retention limitation;
- 8-bit/6-bit drift-flat behavior.

### Optional Experiments Only

These should not block manuscript editing:

1. PCMPresetDevice 3-seed replication.
   - Purpose: strengthen device-model sensitivity.
   - Current status: single-seed compatibility only.
   - Placement: SI/thesis, not main claim unless 3-seed completes.

2. Remote 105 cross-architecture validation.
   - Purpose: show DeiT/ViT generality.
   - Current status: delayed by server issue.
   - Placement: optional SI or thesis; not blocking.

3. Remote 107 KV-cache.
   - Purpose: Work-2 paper.
   - Current status: separate project.
   - Placement: one future-work sentence only in Paper-1.

4. Measured-device calibration / real array parameters.
   - Purpose: upgrade from tested UnitCell simulation to measured-device claim.
   - Current status: future work.

## Manuscript Changes Still Needed

### P0 — Must Fix Before Final Submission

1. Title and keywords are still old-story biased.
   - Current title: `Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision`.
   - Problem: main evidence is now low-precision analog / AIHWKit / PCM, not primarily organic optoelectronic.
   - Recommended title: `Hardware-Aware Training and Precision-Retention Frontiers for Low-Precision Analog Vision Inference`.

2. Introduction opening still leads with organic optoelectronic devices.
   - Acceptable only if organic is deliberately retained as the broad motivation.
   - Stronger version: lead with analog CIM / low-precision deployment, then mention organic/optoelectronic and PCM as device classes.

3. Main figure missing.
   - Add a main Figure 1 summarizing the experimental spine.
   - Keep detailed old diagnostic figures in SI.

4. Source-data package missing or not clearly indexed.
   - Build `paper/latex_gpt/source_data/` with CSV/JSON for Table 1 and SI PCM tables.
   - Add a manifest mapping each table/figure to raw artifact paths.

5. Guard script coverage incomplete.
   - `check_locked_numbers.py` does not include the PCM 4/6/8 precision-ladder numbers.
   - Codex added `scripts/_gpt/check_local_pcm_precision_ladder.py`; either keep it as a second guard or integrate it into the main locked-number guard.

### P1 — Strongly Recommended

1. Turn the main precision-ladder table into a visual figure or add a companion figure.
2. Reduce old organic/OPECT/front-end SI prominence or add a short SI note saying these are historical/supporting diagnostics.
3. Add one paragraph in Discussion explicitly saying PCMPresetDevice is single-seed compatibility only, not headline evidence.
4. Create a `CANONICAL_NUMBERS.md` or source-data manifest for humans and agents.

### P2 — Optional Later

1. PCMPresetDevice multi-seed.
2. Remote 105 cross-architecture when server recovers.
3. Work-2 KV-cache separate manuscript.

## Current Operational Priority

1. Fix title/keywords/opening framing.
2. Add main Figure 1 for the locked spine.
3. Build source-data manifest.
4. Keep GPUs idle for Paper-1 unless running optional PCMPresetDevice 3-seed after manuscript packaging is stable.
