# Dispatch to DeepSeek — Non-GPU Paper-1 Closure Tasks

Date: 2026-05-01
Owner: DS / any available text-code agent
GPU policy: **Do not use GPU. Do not launch training. Do not run eval jobs.**

## Current State
Codex has closed mandatory local Paper-1 GPU work.

Locked spine:

1. IdealDevice 8-bit stable: 87.28 +/- 0.13% fresh.
2. Pure 4-bit collapse: 14.64 +/- 0.11% fresh.
3. Ensemble HAT 4-bit rescue: 86.16 +/- 0.19% fresh.
4. PCM UnitCell ladder:
   - 8-bit: 77.60 +/- 0.64% fresh, 0.04 pp 1-day drift drop.
   - 6-bit: 77.86 +/- 0.56% fresh, 0.10 pp 1-day drift drop.
   - 4-bit: 76.68 +/- 0.37% fresh, 4.01 pp 1-day drift drop.
5. Current narrative: algorithmic cross-instance robustness first, then PCM precision-retention frontier.

Already verified:

- `check_locked_numbers.py`: 22/22 PASS.
- `check_local_pcm_precision_ladder.py`: PASS.
- Main and supplementary PDFs compile.
- Bib key audit: 0 missing keys.
- DOI/URL endpoint audit: 67/67 endpoint-resolved.
- Full figure inventory exists at `paper/latex_gpt/source_data/manifest_all_figures_20260501.json/csv`.

## DS Work Rules

- No GPU.
- No new result claims unless backed by raw JSON / logs / generated source-data.
- Do not change locked numbers.
- Do not re-expand Paper-1 around 105/107. Remote 105 is optional validation; 107 is Work-2/future work.
- Do not convert `figure_file_only` to `source_data_linked` unless actual source CSV/JSON is reconstructed and linked.
- Prefer additive reports and small LaTeX edits. Avoid large rewrites unless a concrete inconsistency is found.

## Task DS-1: Legacy SI Figure Source-Data Reconstruction

Priority: P1, non-blocking for current draft but important for journal packaging.

Input:

- `paper/latex_gpt/source_data/manifest_all_figures_20260501.csv`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
- candidate generator scripts listed in the manifest.

Goal:

For each `figure_file_only` figure, decide whether source data can be reconstructed without GPU.

Deliverables:

1. `report_md/_gpt/DS_LEGACY_FIGURE_SOURCE_DATA_AUDIT_20260501.md`
2. If reconstructable, add CSV/JSON files under `paper/latex_gpt/source_data/legacy/`.
3. Update a new manifest file, do not overwrite Codex's original manifest unless fully validated.

Required table columns:

- Figure artifact
- Used in LaTeX file/section
- Existing figure file path
- Generator script found? yes/no/path
- Raw data source found? yes/no/path
- Reconstructable without GPU? yes/no
- Action taken
- Residual risk

Priority order:

1. `figS_standard_hat_collapse_mechanism`
2. `figS_d2d_loss_landscape`
3. `figS_per_layer_sensitivity`
4. `figS_hessian_spectrum`
5. `figS_cka_mseries`
6. `figS_checkpoint_avg`
7. `fig9_noise_sensitivity`
8. `fig_fresh_instance_ablation`
9. `fig7_retention_curve`
10. Other legacy figures only if easy.

Kill criterion:

If source raw data cannot be located in 30 minutes for a figure, mark it `figure_file_only_unresolved`; do not invent values.

## Task DS-2: Semantic Reference Audit

Priority: P1.

Input:

- `paper/latex_gpt/refs_gpt.bib`
- `paper/latex_gpt/source_data/manifest_bib_key_audit_20260501.json`
- `paper/latex_gpt/source_data/manifest_bib_doi_resolution_20260501.json`

Goal:

Codex verified key coverage and endpoint existence. DS should do semantic bibliography audit for references actually cited in main/SI text.

Deliverable:

- `report_md/_gpt/DS_SEMANTIC_REFERENCE_AUDIT_20260501.md`

For each used reference, verify:

- title matches DOI/arXiv endpoint,
- venue/year are plausible,
- reference type is correctly labeled: peer-reviewed / preprint / tech report / misc,
- citation context in LaTeX does not overclaim what the reference supports.

Special attention:

- 2025/2026 future-looking references.
- Organic/optoelectronic references retained in SI.
- `zhang2025opect`, `vincze2025dualplasticity`, `crosssim2024`, `rasch2021aihwkit`, `lanza2025memristor`.

Output severity labels:

- BLOCKER: likely false/nonexistent or seriously mismatched.
- MAJOR: reference exists but citation context overclaims.
- MINOR: formatting/metadata issue.
- OK: no action.

Do not use GPU.

## Task DS-3: Hostile Claim Audit for Supplementary Text

Priority: P1.

Codex softened the main text. SI still contains historical/legacy organic, severe-NL, retention, and mechanism material.

Goal:

Find overclaims in supplementary text, especially claims using words like:

- demonstrate, prove, establish, confirm, critical, intrinsic, decisive, optimal, universal, guarantees, dominant, primary.

Deliverable:

- `report_md/_gpt/DS_SUPPLEMENTARY_HOSTILE_CLAIM_AUDIT_20260501.md`

Required output:

- File and line number.
- Quoted phrase.
- Why risky.
- Recommended replacement wording.
- Whether DS applied patch or only recommends patch.

Patch allowed:

- Yes, for clear wording softening only.
- No, for changing numbers or scientific conclusions.

Priority sections:

1. `paper/latex_gpt/supplementary.tex`
2. `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex`
3. `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
4. `paper/latex_gpt/supplementary/S_hardware_calibration.tex`

## Task DS-4: Reviewer Reproducibility Bundle Plan

Priority: P2.

Goal:

Prepare a packaging plan, not the actual tarball unless asked.

Deliverable:

- `report_md/_gpt/DS_REVIEWER_BUNDLE_PLAN_20260501.md`

Must include:

- exact files required for reviewer archive,
- raw JSON/log files behind locked numbers,
- scripts needed to regenerate Fig. 1 and checks,
- scripts that are safe CPU-only,
- files to exclude: checkpoints, large outputs, stale dirs, tmux logs, generated aux files,
- proposed `README_REPRODUCIBILITY.md` outline,
- proposed `MANIFEST_SHA256SUMS.txt` generation command.

Do not create huge archives. Do not add checkpoints.

## Task DS-5: GitHub Clean Branch Checklist

Priority: P2.

Goal:

Create a human-safe checklist for cleaning GitHub without deleting local user data.

Deliverable:

- `report_md/_gpt/DS_GITHUB_CLEAN_BRANCH_CHECKLIST_20260501.md`

Include:

- recommended branch structure,
- what goes to public repo,
- what stays local/private,
- `.gitignore` recommendations,
- large-file policy,
- command sequence for creating a clean branch,
- warning: no `git reset --hard`, no destructive deletion without explicit user approval.

## Do Not Do

- Do not run GPU jobs.
- Do not rerun training/eval.
- Do not edit locked-number JSONs.
- Do not delete files.
- Do not merge 107 KV-cache into Paper-1 main claims.
- Do not claim legacy SI source-data completeness unless reconstructed.

## Final DS Response Format

When done, DS should return:

1. Completed task list.
2. Files changed/created.
3. Any blockers.
4. Any patches applied.
5. Whether main/SI still compile if DS changed TeX.
6. A one-paragraph architecture recommendation.
