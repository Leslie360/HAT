# GEMINI DATA RELEASE REVIEW — 2026-04-19

**Reread of canonical state:**
I have re-read `release_artifacts/source_data_v0_MANIFEST.md`, `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md`, and `report_md/_gpt/REPRODUCIBILITY_PACKAGE_PLAN_20260418.md`.

## 1. Schema Sufficiency for NC Reviewers

**Verdict:** PARTIALLY SUFFICIENT.
The current v0 schema successfully enables the regeneration of Figure 4 (headline accuracy) and the severe-NL supplementary tables. However, it lacks the raw data for several critical secondary results.

**Missing Figure Data (Critical for NC):**
1. **Fig 3 (Contour Map):** The manifest lists `iso_accuracy_contour_data.json`, but doesn't include the per-cell raw Monte Carlo draws ($n=10$) used to compute the mean/std. Reviewers may challenge the statistical significance of the heatmap gradients.
2. **Fig 6 (Frontend Compensation):** The manifest excludes the source JSON for the $\gamma_{\text{phys}}$ sweep results (`a23_experiment_results.json` is missing from the v0 ZIP).
3. **Fig 7 (Retention):** The manifest does not include the raw retention decay logs for the 10,000s duration.

## 2. Code-Snapshot Ledger Granularity

**Verdict:** APPROPRIATE.
The file-level granularity with `.tex` line-anchors is excellent. It allows a reviewer to trace exactly which JSON file produced which sentence in the LaTeX source.

**Recommendation:** Line-level `.tex` links are only needed for the "Headline Results" (H1-H8). For the rest of the manuscript, file-level linking is sufficient. Adding line-level mapping to everything would create a maintenance nightmare with every paragraph edit.

## 3. Top 3 Reviewer Gaps

1. **"The Black Box Trainer" gap:** While the *inference* code is well-traced, the training loops for the canonical V4 and C4 checkpoints are only linked at a high level. A reviewer might challenge the "implicit Monte Carlo" claim without seeing the exact resampling hook in `train_tinyvit.py`.
2. **Environmental Reproducibility gap:** The ledger lists `.py` files but doesn't provide a `requirements.txt` or `conda_env.yml` snapshot. Without a pinned environment (especially `torch` and `torchvision` versions), reproducibility is hindered by dependency drift.
3. **Statistical Rawness gap:** Most bundled data is "Pre-aggregated" (Means and Std). Nature journals increasingly request the "Source Data" in its rawest form (i.e., the individual accuracy values for every seed/trial), especially for claims like $p < 10^{-15}$.

## 4. Recommendations for v1 ZIP (Priority Ranking)

1. **PRIORITY 1: Figure 6 & 7 Source Arrays.** Add the missing $\gamma$ sweep and retention JSONs to allow full regeneration of §5 visual evidence.
2. **PRIORITY 2: Environment Definition.** Include the `compute_vit/requirements.txt` and a minimal setup guide.
3. **PRIORITY 3: Multi-Seed Raw Exports.** Export individual MC accuracies (not just means) for the OPECT baseline ($n=10$) and the Ensemble HAT fresh-instance transfer tests.
4. **PRIORITY 4: README Integration.** Link the ZIP manifest directly into the new `compute_vit/README.md` (Task CX-Y).
