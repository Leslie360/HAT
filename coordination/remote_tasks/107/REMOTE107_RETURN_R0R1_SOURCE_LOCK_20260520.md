# Remote107 Return — R0/R1 Source Lock — 2026-05-20

## One-Line Verdict

R0 all 3 fixes applied; R1 mechanism-control verdict is **C** (HAT fine-tuning dominates); source-lock package committed at `source_lock_20260520/`.

## Files Pushed

- `coordination/REMOTE107_COMPLETE_HISTORY.md` — updated R1 7/7, verdict, stats
- `results/remote107/source_lock_20260520/` — 9 files:
  - `README_PROTOCOL.md`, `PACKAGE_MANIFEST.json`
  - `remote107_paper2_results_summary_20260520.json` + `.csv`
  - `source_json_inventory_20260520.csv` (all lm_eval JSONs with SHA256)
  - `checkpoint_inventory_20260520.csv` (all checkpoint dirs)
  - `r1_mechanism_controls_summary_20260520.csv` (7 R1 rows with metrics)
  - `logs_inventory_20260520.csv` (all 204 log files with SHA256)
  - `sha256sum.txt` (full checksum manifest)
- `coordination/remote_tasks/107/REMOTE107_RETURN_R0R1_SOURCE_LOCK_20260520.md`

## R0 Fixes

| Item | Status | Detail |
|------|--------|--------|
| R0-F1: Source-Lock Package | **Done** | `source_lock_20260520/` with 9 files, all SHA256-verified |
| R0-F2: Entry-Level `git_commit_hat` | **Done** | All 19 entries normalized to `"deployed_as_directory"` (commit `0a4468d`) |
| R0-F3: R1 Compact CSV | **Done** | 7 rows × 17 columns, metrics extracted from JSON summary keys, verified correct |

## R1 Mechanism-Control Table

| Condition | PPL (lambada) | ΔPPL | Lambada Acc | ΔAcc | Verdict Component |
|-----------|:---:|:---:|:---:|:---:|:---|
| base_clean (raw HF) | 14.94 | — | 0.4500 | — | Baseline |
| patched_zero_last1 | 15.04 | -0.10 | 0.4502 | +0.000 | Patching overhead negligible |
| patched_zero_last2 | 15.23 | -0.29 | 0.4493 | -0.001 | Patching overhead small |
| patched_zero_last4 | 16.75 | -1.81 | 0.4279 | -0.022 | Patching overhead noticeable |
| patched_zero_all24 | 20.88 | -5.93 | 0.4000 | -0.050 | Patching overhead severe |
| **hat_quant_zero_noise** | **13.53** | **+1.41** | **0.4712** | **+0.021** | **HAT FT improves baseline** |
| hat_d2d_0p05 | 14.97 | -0.03 | 0.4549 | +0.005 | HAT + noise → parity |

**Decision Rule (A–E):** **C — HAT Fine-Tuning Dominates**

- **A (patching overhead dominates)**: No — last1/last2 patching adds only +0.1–0.3 PPL
- **B (zero-noise quantization dominates)**: No — HAT zero-noise improves over base
- **C (HAT fine-tuning dominates)**: **Yes** — hat_quant_zero_noise achieves PPL 13.53 vs base 14.94 (Δ=-1.41), proving the fine-tuning process itself is the primary mechanism. This improvement largely compensates for analog patch overhead.
- **D (physical noise benefit)**: No — adding σ_d2d=0.05 brings PPL back to 14.97 (near parity with 14.94), reversing the fine-tuning gain
- **E (mixed)**: Secondary — noise model matters for last2+ patching configs, but the dominant signal is C

## LFS / Source Integrity

- All 204 lm_eval JSON files are **raw (not LFS)**, self-contained, SHA256-verified
- 66 MB per-file size confirmed; these are large because they contain per-request loglikelihoods
- Checkpoints directory contains ~230 checkpoint folders with training artifacts
- Source-lock sha256sum.txt covers all 9 package files plus the summary JSON

## Open Gaps

| Gap | Status | Plan |
|-----|--------|------|
| p69b_fixed1000 clean eval | Running on GPU5 (~31%, ~4.9h remaining) | Sequential -> analog, then update summary JSON |
| Large JSON compression (66MB files) | Deferred | LFS is available but not yet configured for this branch; may add `.gitattributes` |
| VLM 5K eval claim-lock manifest | Not started | Low priority — VLM experiments are exploratory/diagnostic-only |
| PR from 107-clean -> master | Not created | Requires gh CLI or GitHub token; user can create manually at `https://github.com/Leslie360/HAT/compare/master...107-clean` |

## Recommended Next Action

1. Wait for GPU5 p69b_fixed1000 clean + analog to finish (~5h from now)
2. Extract metrics and add 2 entries to paper2_results_summary.json
3. Update source_lock with the new JSON files
4. Final commit + push with `Remote107 Return - Full Closure - 2026-05-20`
5. Create PR from `107-clean` to `master`
