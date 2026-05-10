# Codex Phase P6 Final Acceptance

Date: 2026-05-09 18:35 Asia/Shanghai
Owner: Codex
Scope: P6 experiment-completion verification, seed123 6-bit correction, final submission bundle resync, next-phase routing.

## 1. Verdict

**P6 is accepted after Codex repair.**

Kimi completed the requested P6 evidence closure and DS/Mimo both identified the same real issue: after the 6-bit seed123 rerun, the authoritative CSV/source JSON had moved to the new 6-bit values, while part of the manuscript and the final submission bundle still carried old values.

Codex did not accept the bundle at that intermediate state. Codex repaired the working tree, rebuilt the PDFs, resynchronized the final submission bundle, refreshed manifests/SHA256, and re-ran focused stale-value scans.

Final status:

| Area | Status | Codex verdict |
|---|---:|---|
| Scientific values | Fixed | PASS |
| Working LaTeX/PDF | Rebuilt | PASS |
| Final submission bundle | Resynced | PASS |
| Source data | Updated | PASS |
| Canonical JSON manifest | Updated | PASS |
| SHA256 manifest | Refreshed and verified | PASS |
| Old 6-bit strings | Removed from active/bundle files | PASS |
| Paper-1 submission readiness | Yes | PASS |

## 2. Locked P6 Numbers

Use these values for Paper-1 unless Codex explicitly reopens the freeze.

| Precision | Source best | Fresh mean | Fresh std | Retention 1h | Retention 24h/1d | Delta drift | Definition |
|---|---:|---:|---:|---:|---:|---:|---|
| 8-bit PCM | 77.64% | 77.60% | 0.64 pp | 77.49% | 77.57% | 0.04 pp | retention 0s minus 24h/1d |
| 6-bit PCM | 68.40% | 68.44% | 6.03 pp | 68.46% | 68.36% | 0.04 pp | retention 0s minus 24h/1d |
| 4-bit PCM | 76.64% | 76.68% | 0.37 pp | 74.04% | 72.64% | 4.01 pp | retention 0s minus 24h/1d |

Important: Delta drift is **not** fresh minus 24h. It is the paired retention-evaluation drop from 0s to 24h/1d. Gemini's earlier Fresh-minus-24h mutation remains rejected.

## 3. Seed123 6-bit Closure

The previous 6-bit seed123 gap is closed.

| Item | Value |
|---|---:|
| seed123 best source | 68.51% |
| seed123 fresh | 68.4884 +/- 0.0336% |
| seed123 retention 0s | 68.44% |
| seed123 retention 1h | 68.53% |
| seed123 retention 1d | 68.58% |
| seed123 retention delta | -0.14 pp |

This seed is now included in the 6-bit aggregate. The resulting 6-bit story is not inflated: mean accuracy is lower than the old interrupted-run value, but the drift-vs-precision conclusion is cleaner because the source-data hole is closed.

## 4. Codex Repairs Applied

Codex applied the following repairs after the DS/Mimo audits:

| File area | Repair |
|---|---|
| `paper/latex_gpt/supplementary.tex` | Updated 6-bit caption and seed123 row from stale/interrupted values to final rerun values. |
| `paper/latex_gpt/cover_letter.tex` | Updated 6-bit headline from old 68.55% to 68.44%. |
| `paper/latex_gpt/sections/` | Verified active main sections use 68.44% / 0.04 pp. |
| `paper/latex_gpt/source_data/` | Regenerated Figure 1/2 and table CSVs from updated values. |
| `paper/latex_gpt/source_data/canonical_json/` | Refreshed manifest and added seed123 training history. |
| `paper/latex_gpt/main.pdf` | Rebuilt. |
| `paper/latex_gpt/supplementary_main.pdf` | Rebuilt. |
| `paper/latex_gpt/cover_letter.pdf` | Rebuilt. |
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Resynced from working submission tree. |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Recreated from repaired final bundle. |
| final `MANIFEST_FILES.txt` and `SHA256SUMS.txt` | Refreshed and verified. |

## 5. Final Bundle Verification

Accepted submission artifact:

`release_artifacts/paper1_submission_bundle_20260509_final/`

Accepted tarball:

`release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`

Verification results:

| Check | Result |
|---|---:|
| Final bundle files | 135 manifest entries |
| SHA256 entries | 134 entries, excluding `SHA256SUMS.txt` itself |
| SHA256 check | OK |
| PDFs present | `main.pdf`, `supplementary_main.pdf`, `cover_letter.pdf` |
| Active stale scan for `68.55`, `0.07 pp`, old seed123 values | 0 hits |
| PDF text stale scan | 0 hits for old 6-bit values |
| Final source-data old-protocol scan | 0 active hits |
| Build/checkpoint residue scan | 0 hits |
| Files larger than 10 MB | 0 |
| Local PCM guard | PASS |
| Canonical JSON manifest | 47 items, 0 missing |

## 6. DS/Mimo Audit Reconciliation

DS was correct to flag the stale 6-bit issue.

Mimo correctly fixed active main-section `.tex` files but did not fully close the final-bundle path or the supplementary seed123 table. Codex has now closed those remaining gaps.

Updated arbitration:

| Agent | P6 contribution | Codex assessment |
|---|---|---|
| Kimi | Completed the actual rerun/statistical/source-data work. | Accepted. |
| DS | Found the critical stale-value mismatch. | Accepted; finding was real. |
| Mimo | Fixed part of the active manuscript and defense framing. | Accepted with Codex completion of the final-bundle gap. |
| Gemini | Visual-only unless explicitly asked; no scientific-value edits. | Restriction remains active. |

## 7. Experiment Completeness Decision

Paper-1 is experimentally sufficient for submission.

That does **not** mean the whole research program is exhausted. It means further experiments should not keep moving Paper-1's frozen numerical claims unless they reveal a correctness issue.

| Workstream | Status | Next action |
|---|---|---|
| Paper-1 local PCM/Ensemble HAT | Sufficient and frozen | Packaging, final visual polish, reviewer bundle only. |
| Local GPU for Paper-1 | Not required | Do not run open-ended training that can destabilize frozen claims. |
| Remote 105 | Useful supplement/validation only | Wait for server recovery and final seed789 package. |
| Remote 107 | Strong Work-2 direction | Continue corrected-noise KV-cache experiments separately. |
| Thesis/appendix visuals | Still worth improving | Visual pipeline only; no scientific-value mutation. |

## 8. Remaining Non-Blocking Risks

| Risk | Severity | Handling |
|---|---:|---|
| Large dirty working tree | Medium | P7 must create a clean commit/branch plan before any push. |
| Remote 105 delayed | Low for Paper-1 | Keep as supplement candidate, not a submission blocker. |
| Remote 107 corrected-noise rerun may shift absolute PPL | Low for Paper-1, medium for Work-2 | Keep separate from Paper-1 claims. |
| Appendix figure aesthetics | Medium for presentation | Gemini/user visual pass continues; scientific tables already locked. |
| Old drafts in history | Low | Kimi already removed active `.kimi_draft*`; verify before commit. |

## 9. Codex Final Decision

P6 is closed.

The current final submission bundle is the accepted Paper-1 package. Further work should move to P7: final freeze, repo hygiene, release branch discipline, remote result ingestion, and Work-2 planning.
