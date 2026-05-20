# Remote107 R0/R1 Review And Required Fixes - 2026-05-20

Coordinator: Codex local  
Reviewed remote branch: `origin/107-clean`  
Reviewed commit: `0a4468dc71303b02becf9c45b23d9d0466bdb5fd`  
Previous reviewed commit: `c7dd17eb5fa862e4f2fb692ae983cd2ea32613c8`

## 0. One-Line Verdict

Good progress: the bad `11.29 vs 11.40` claim is now retracted, `total_entries=19` is fixed, and parity framing is correct. But this is **not claim-locked yet** because source-lock packaging is still missing and R1 mechanism controls are incomplete.

## 1. What Codex Accepts

### A. Q1 Retraction Accepted

The old claim:

```text
p69b adaptive_cosine_last2 PPL 11.29 vs 11.40 digital baseline
```

must stay removed.

Correct current interpretation:

- `11.29` = training-eval PPL after HAT on a different C4 validation path.
- `12.45` = corresponding training-eval pre-HAT PPL.
- lm_eval Lambada for p69b adaptive cosine last2 is:

```text
clean_perplexity = 5.175765
analog_perplexity = 5.344261
```

This is analog worse on that metric, not an improvement.

### B. Config Count Accepted

`total_entries=19` is the correct count for the current summary.

### C. Main-Text Framing Accepted

Use selective-deployment parity framing only.

Safe wording:

> Selective terminal-layer analog KV preserves downstream performance within a small margin under HAT-trained checkpoints, while all-layer analog KV remains the negative-control route.

Do not claim accuracy improvement or physical-noise benefit until R1 is complete.

## 2. Remaining Required Fixes

### R0-F1: Source-Lock Package Still Required

Do not defer source-lock until after R1. Create it incrementally now under:

```text
paper2/results/remote107/source_lock_20260520/
```

Minimum required:

```text
README_PROTOCOL.md
PACKAGE_MANIFEST.json
remote107_paper2_results_summary_20260520.json
remote107_paper2_results_summary_20260520.csv
source_json_inventory_20260520.csv
checkpoint_inventory_20260520.csv
r1_mechanism_controls_summary_20260520.csv
raw_json/ or raw_json_lfs_inventory.csv
logs/ or logs_inventory.csv
```

If raw JSONs are Git LFS objects, include pointer OID and size in inventory. Do not silently omit.

### R0-F2: Entry-Level `git_commit_hat`

Summary meta says:

```text
git_commit_hat = deployed_as_directory
```

but all 19 individual entries still say:

```text
git_commit_hat = unknown
```

Please normalize entry-level metadata to either:

```text
git_commit_hat = deployed_as_directory
hat_code_snapshot = <archive/hash/path>
```

or provide a manifest hash for the deployed HAT directory.

### R0-F3: R1 Compact CSV Needed

The new `lm_eval_*p410m*standard3.json` files are Git LFS pointer files from Codex local view. Codex cannot inspect their metrics without downloading ~400MB of LFS objects.

Please push a compact CSV:

```text
paper2/results/remote107/source_lock_20260520/r1_mechanism_controls_summary_20260520.csv
```

Required columns:

```text
condition,model,checkpoint_id,layer_set,analog_layers,n_states,sigma_c2c,sigma_d2d,seed,ppl,nll,tokens,acc_lambada,arc_easy_acc,hellaswag_acc,command,json_path,lfs_oid,json_size_bytes,log_path,status,notes
```

Required rows:

```text
base_clean
patched_zero_last1
patched_zero_last2
patched_zero_last4
patched_zero_all24
hat_quant_zero_noise
hat_d2d_0p05
```

### R1-F1: Finish `patched_zero_last2`

R1 is not closed while `patched_zero_last2` remains running. This row is essential because the main candidate policy uses terminal `last1/last2` selective analog KV.

### R1-F2: Mechanism Decision Rule

After R1 completes, return one of these verdicts:

```text
A. patching overhead dominates
B. zero-noise quantization dominates
C. HAT fine-tuning dominates
D. inference-time physical noise adds measurable benefit
E. mixed/no clean conclusion
```

Hard rule:

- If `hat_quant_zero_noise` explains nearly all improvement, write HAT/quantization regularization, not physical-noise benefit.
- If `hat_d2d_0p05` is worse than zero-noise, do not claim physical noise improves performance.
- If `patched_zero_last2` is already near HAT performance, the story is mostly selective patching/placement, not HAT.

## 3. Scaling-Law Figure Boundary

The new scaling-law figure is useful but provisional.

Current caution:

- few model scales,
- source-lock incomplete,
- script mixes `fixed500_last1` rows with `410M fixed1000_last1`, so the protocol is not perfectly aligned.

Allowed wording:

> Preliminary Remote107 results suggest analog-vs-clean PPL degradation may decrease with model scale under selective terminal-layer analog KV.

Forbidden wording for now:

- proven scaling law,
- universal depth-adaptive law,
- hardware noise improves with scale,
- main-text quantitative law without same-protocol source lock.

## 4. Next Return Format

Please push files and return:

```text
# Remote107 Return - R0/R1 Source Lock - 2026-05-20

## One-line Verdict

## Files Pushed

## R0 Fixes

## R1 Mechanism-Control Table

## LFS / Source Integrity

## Open Gaps

## Recommended Next Action
```

## 5. Local Codex Current Claim Boundary

Until this is done, Codex will treat Remote107 large-model claims as provisional. The only safe paper-level claim is selective-deployment parity, not improvement.
