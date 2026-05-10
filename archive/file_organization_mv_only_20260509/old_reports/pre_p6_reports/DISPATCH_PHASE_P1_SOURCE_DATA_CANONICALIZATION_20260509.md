# Dispatch Phase P1 — Source-Data Canonicalization and Release Guard

Date: 2026-05-09
Issued by: Codex
Execution protocol: Kimi-first phased workflow

## Objective

Make the Paper-1 data package release-safe. The active manuscript is now semantically consistent, but the archival source-data layer still contains stale 2026-05-01 copied JSON artifacts. This phase must rebuild or quarantine the source-data package so a reviewer/release bundle cannot accidentally cite old 6-bit results.

## Executor Assignment

- **Kimi**: primary executor. Complete the whole phase end-to-end.
- **DS**: audit after Kimi delivery only. Focus on provenance, stale-path detection, and reproducibility guard strictness.
- **Mimo**: audit after Kimi delivery only. Focus on reviewer-facing claim consistency and release-bundle clarity.
- **Gemini**: no action unless the user asks for visual second-pass work.
- **Codex**: final acceptance after Kimi + DS/Mimo reports.

## Inputs

Read these first:

1. `report_md/_gpt/CODEX_FINAL_ACCEPTANCE_PCM_FREEZE_20260509.md`
2. `report_md/_gpt/KIMI_6BIT_DRIFT_CLOSURE_20260509.md`
3. `report_md/_gpt/MIMO_PCM_NARRATIVE_REPAIR_20260509.md`
4. `report_md/_gpt/CODEX_APPENDIX_CONTENT_REPAIR_20260509.md`
5. `paper/latex_gpt/source_data/manifest_paper1_spine.json`
6. `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv`
7. `scripts/_gpt/check_local_pcm_precision_ladder.py`

## Required Work

### 1. Canonical JSON cleanup

Rebuild or quarantine `paper/latex_gpt/source_data/canonical_json/` so active release artifacts no longer expose stale old-protocol 6-bit data as canonical.

Minimum acceptable outcome:

- New manifest name: `manifest_canonical_json_20260509.json` and `.csv`.
- Old manifest `manifest_canonical_json_20260501.*` must be marked superseded or moved into a clearly named deprecated/quarantine folder.
- Old `pcm_6bit_seed456_full100` must not appear in any active canonical manifest.
- New-protocol 6-bit active sources must include:
  - `r11d_6bit_pcm_seed123/fresh_eval.json`
  - `r11d_6bit_pcm_seed123/drift_eval.json`
  - `r11d_6bit_pcm_seed456/training_history.json`
  - `r11d_6bit_pcm_seed456/fresh_eval.json`
  - `r11d_6bit_pcm_seed456/drift_eval.json`
  - `r11d_6bit_pcm_seed457/training_history.json`
  - `r11d_6bit_pcm_seed457/fresh_eval.json`
  - `r11d_6bit_pcm_seed457/drift_eval.json`
  - `r11d_6bit_pcm_seed789/training_history.json`
  - `r11d_6bit_pcm_seed789/fresh_eval.json`
  - `r11d_6bit_pcm_seed789/drift_eval.json`
- Explicitly record that `r11d_6bit_pcm_seed123/training_history.json` is missing and therefore excluded from source-best aggregation.

Do not delete raw checkpoint directories. If moving copied JSON inside `paper/latex_gpt/source_data`, use a deprecated folder and preserve hashes.

### 2. Source-data manifest alignment

Ensure these active source-data files agree:

- `paper/latex_gpt/source_data/manifest_paper1_spine.json`
- `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv`
- `paper/latex_gpt/source_data/fig1_paper1_spine.csv`
- `paper/latex_gpt/source_data/fig2_paper1_decision_map.csv`
- new `manifest_canonical_json_20260509.*`

The active 6-bit claim must remain:

- fresh mean 68.55%
- fresh seed std 6.03 pp
- 1 h mean 68.57%
- 24 h mean 68.46%
- 24 h drift 0.07 pp
- role: D2D-sensitive transition zone, not Pareto midpoint

### 3. Guard hardening

Add or update a guard script if needed so this command set catches stale active-release artifacts:

```bash
python scripts/_gpt/check_local_pcm_precision_ladder.py
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100|75\.43|72\.67" \
  paper/latex_gpt/sections paper/latex_gpt/supplementary.tex paper/latex_gpt/supplementary/*.tex paper/latex_gpt/cover_letter.tex paper/latex_gpt/source_data scripts/_gpt \
  --glob '!paper/latex_gpt/source_data/deprecated*/**'
```

Expected result: no active hits. Hits inside explicitly deprecated/quarantine folders are acceptable only if excluded by the guard and documented.

### 4. Compile and artifact check

Run:

```bash
cd paper/latex_gpt
tectonic main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
pdftotext main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|pending" || true
pdftotext supplementary_main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|6-bit.*pending|pending.*6-bit" || true
```

### 5. Deliverable report

Write:

`report_md/_gpt/KIMI_PHASE_P1_SOURCE_DATA_CANONICALIZATION_REPORT_20260509.md`

Required sections:

1. Files changed
2. Active canonical manifest summary
3. Deprecated/quarantined artifacts summary
4. Hash/provenance table
5. Guard command outputs
6. Compile outputs
7. Remaining risks, if any
8. One-line verdict: release-safe or not release-safe

## Kill Criteria

Stop and broadcast a blocker if any of these occur:

- An active source-data manifest still references `r11d_6bit_pcm_seed456_full100`.
- Active manuscript or source-data CSV still contains 77.86 / 75.43 / 72.67 as the 6-bit or active PCM-ladder claim.
- The new manifest cannot account for every active JSON source used in `tab_pcm_precision_ladder.csv`.
- `main.pdf` or `supplementary_main.pdf` cannot be generated.

## Success Criteria

This phase is complete only when:

- Active manuscript numbers match source CSVs.
- Active source-data manifests point only to current-protocol artifacts.
- Old artifacts are preserved but clearly deprecated/quarantined.
- Guard scripts and grep checks fail loudly on stale old-protocol references.
- DS and Mimo can audit without needing to infer which files are canonical.
