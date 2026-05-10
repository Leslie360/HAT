# CC 107 Remote Metadata Harvest — 2026-05-10

## 1. Executive verdict

**Verdict:** `partial_metadata_recovered`; effective gate status is `claim_lock_blocked`.

I recovered source-backed family-level protocol information from the remote 107 scripts and summaries, but the current local result JSONs do not contain the per-row provenance envelope required by Codex. The rows therefore remain audit-only unless a signed manifest is supplied or the minimal corrected-noise matrix is rerun with the patched JSON sidecars.

Blocking fields for claim lock:

- no per-row `git_commit` / exact producer `command` in the legacy JSONs;
- no checkpoint SHA-256 manifest found locally;
- no complete source-backed `old_vs_corrected` table matching checkpoint family, exact analog layers, noise setting, context/stride, and seed semantics;
- protocol conflict remains for eval stride: code and metadata patch say eval stride is `max_length`/512, while a v3 plot summary says canonical stride is 256.

Primary support:

- JSON coverage log: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:1-99`.
- Remote git state log: `/home/qiaosir/projects/compute_vit/logs/CC_107_REMOTE_GIT_STATE_20260510_112148.log:1-2`.
- Hash/comparison search log: `/home/qiaosir/projects/compute_vit/logs/CC_107_HASH_AND_COMPARISON_SEARCH_20260510_112430.log:1-12`.

## 2. Remote git state

- Branch: `107-clean`.
- HEAD: `cf1d2a2fcc71aae89534ed8c75ea6bab4d9e8532`.
- Dirty status: no short-status entries were emitted by the logged command.

Source: `/home/qiaosir/projects/compute_vit/logs/CC_107_REMOTE_GIT_STATE_20260510_112148.log:1-2`.

Important chronology from local git inspection:

- `2b57a2272ef629df39b56a6eabf461bd43e55797`, 2026-05-07 10:44:59 +0800, added many `results/paper2/eval_*.json` files.
- `c5e1c4a795876879832a0972b1275cb0fc2d90e2`, 2026-05-07 10:57:40 +0800, patched `p3_hat_train.py` and `p3_hat_eval.py` to emit the full metadata envelope.

This ordering means many existing JSONs were produced before the metadata patch. The patch document explicitly says old JSONs are not rewritten: `/home/qiaosir/projects/remote_reviews/107/coordination/REMOTE107_METADATA_PATCH_20260508.md:122-127`.

## 3. Corrected-noise code path

Recovered code paths:

- Conductance-domain KV analogization is implemented in `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:31-130`.
  - It maps KV tensors to differential conductance legs, applies STE quantization, applies fixed D2D offsets, applies C2C read noise, then recovers to tensor space.
  - C2C is re-sampled in the forward path at `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:110-126`.
- Model patching and D2D buffer creation are in `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:135-260`.
  - D2D per-layer seed semantics are source-backed at `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:176-180`: per-layer seed is `d2d_seed + layer_idx`.
- Eval applies the patch before PPL evaluation at `/home/qiaosir/projects/remote_reviews/107/p3_hat_eval.py:92-100`.
- Eval auto-loads `analog_layers` and `d2d_seed` from `hat_config.json` when available, otherwise uses `0xD2D=53714`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_eval.py:60-74`.

Caveat: these code paths support the corrected-noise implementation currently present in the clone, but they do not by themselves prove which exact historical code SHA produced each legacy result row.

## 4. Command recovery

### Exact per-row commands

Not recovered. The inspected result families are legacy JSONs and do not embed `command`.

Evidence:

- `results/paper2`: 993 JSONs, 993 legacy/no envelope, `command` count 0: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:1-24`.
- `results/d2d_seed_ablation`: 256 JSONs, 256 legacy/no envelope, `command` count 0: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:25-49`.
- `deliverable/results_v2`: 49 JSONs, 49 legacy/no envelope, `command` count 0: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:50-74`.

### Launcher command patterns

Recovered as family-level launcher patterns, not per-row proof:

- D2D seed ablation launcher builds eval commands with `p3_hat_eval.py --checkpoint_dir ... --n_states ... --sigma_d2d ... --sigma_c2c ... --max_length ... --output_dir ... --d2d-seed ...`: `/home/qiaosir/projects/remote_reviews/107/pipeline_d2d_seed.py:152-183`.
- D2D seed ablation task matrix uses D2D seeds `[42, 123, 456, 789, 1001]`, train D2D `{0.02, 0.04}`, and eval D2D `{0.02, 0.04, 0.05}`: `/home/qiaosir/projects/remote_reviews/107/pipeline_d2d_seed.py:64-101`.
- v2 deliverable launcher builds eval/train commands with `p3_hat_eval.py` / `p3_hat_train.py`, fixed `max_length=512`, `n_states=256`, and output under the remote `OUT_DIR`: `/home/qiaosir/projects/remote_reviews/107/deliverable/pipeline/pipeline_runner.py:203-235`.
- v2 deliverable task matrix covers generalization eval, selective layer sweep, seed repeats, and D2D sweep/convergence: `/home/qiaosir/projects/remote_reviews/107/deliverable/pipeline/pipeline_runner.py:36-146`.

Claim-lock note: these patterns can justify reconstruction for planning, but Codex protocol says reconstructed commands are not enough for claim lock unless independently supported.

## 5. Protocol recovery

### Dataset

Recovered for current scripts:

- Training uses `load_dataset("wikitext", "wikitext-2-raw-v1", split="train")`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:322-323`.
- Evaluation uses `load_dataset("wikitext", "wikitext-2-raw-v1", split="test")`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:376-399`.
- Metadata patch intended future JSONs to record `dataset_train` and `dataset_eval`: `/home/qiaosir/projects/remote_reviews/107/coordination/REMOTE107_METADATA_PATCH_20260508.md:21-22`.

### Context length and stride

Recovered, but with a conflict:

- Launchers set `max_length=512`: `/home/qiaosir/projects/remote_reviews/107/pipeline_d2d_seed.py:30-61` and `/home/qiaosir/projects/remote_reviews/107/deliverable/pipeline/pipeline_runner.py:38-47`.
- Training iterates with stride `max_length // 2`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:333-370`.
- Eval iterates with stride `max_length`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:376-399`.
- Metadata patch states train stride is `max_length // 2` and eval stride is `max_length`: `/home/qiaosir/projects/remote_reviews/107/coordination/REMOTE107_METADATA_PATCH_20260508.md:31-32`.
- v3 summary says canonical eval settings are `ctx=512, stride=256, bs=1`: `/home/qiaosir/projects/remote_reviews/107/deliverable/results_v3/k107_plot_ready.json:1-9`.

Because the legacy JSONs do not record `ctx_len` or `stride`, Codex should treat stride as unresolved for claim-lock rows.

### Batch size and PPL

- Metadata patch describes `batch_size=1`: `/home/qiaosir/projects/remote_reviews/107/coordination/REMOTE107_METADATA_PATCH_20260508.md:33-40`.
- The eval loop processes one tokenized text window at a time and computes PPL as `exp(sum(nlls) / total_predicted)`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:376-399`.

### Analog layers

- Legacy `results/paper2` has `analog_layers` in all 993 usable JSONs: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:12-15`.
- D2D seed ablation has `analog_layers` in 254 of 256 JSONs: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:37-40`.
- The pipeline encodes selective layer sets for last2 `[22, 23]` and last4 `[20,21,22,23]`: `/home/qiaosir/projects/remote_reviews/107/deliverable/pipeline/pipeline_runner.py:99-115`.

### Seed semantics

- Training seed is `--seed`, default 42 in `p3_hat_train.py`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:413-438`.
- D2D seed is a separate device-instance seed, default `0xD2D`, with per-layer seed `d2d_seed + layer_idx`: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:135-180`.
- D2D seed ablation explicitly uses `[42, 123, 456, 789, 1001]`: `/home/qiaosir/projects/remote_reviews/107/pipeline_d2d_seed.py:64-101`.
- C2C noise is sampled during forward evaluation/training and no C2C random seed is captured in legacy JSONs: `/home/qiaosir/projects/remote_reviews/107/p3_hat_train.py:110-126` and `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:4-23`.

## 6. Checkpoint provenance

Partial only.

- `results/paper2` contains `checkpoint_dir` for all 993 usable JSONs: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:11-15`.
- `results/d2d_seed_ablation` contains `checkpoint_dir` for 138 JSONs: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:36-40`.
- `deliverable/results_v2` contains `checkpoint_dir` for 20 JSONs: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:61-65`.
- No local checkpoint SHA-256 manifest was found by the bounded search; only an unrelated script path matched the filename search, and grep found no checkpoint-hash evidence: `/home/qiaosir/projects/compute_vit/logs/CC_107_HASH_AND_COMPARISON_SEARCH_20260510_112430.log:1-12`.

Checkpoint hashes are therefore blocked unless Codex approves a safe local hash procedure or remote 107 provides a signed manifest. I did not move or hash checkpoint payloads.

## 7. Old-vs-corrected map

Partial comparison text exists, but not a claim-lock-safe matched table.

Sources:

- `RESULTS_SUMMARY.md` has a `v1 vs v2 (same config)` table: `/home/qiaosir/projects/remote_reviews/107/RESULTS_SUMMARY.md:52-65`.
- `deliverable/README.md` has a shorter v1/v2 comparison: `/home/qiaosir/projects/remote_reviews/107/deliverable/README.md:40-50`.
- `deliverable/results_v2/` is documented as the current corrected v2 result directory, while `deliverable/p0_p3_archive/` is pre-v2/ctx512-bug archive: `/home/qiaosir/projects/remote_reviews/107/deliverable/README.md:19-28`.

Blockers:

- The v1/v2 summary is not tied to per-row exact `git_commit`, producer command, checkpoint hash, or embedded protocol fields.
- It does not provide enough source-backed pairing metadata to satisfy Codex's `old_vs_corrected` acceptance standard.
- The eval stride conflict above prevents safe protocol matching.

I wrote the non-locking extraction to `CC_107_OLD_VS_CORRECTED_MAP_20260510.tsv` under this same directory.

## 8. Metadata completeness verdict by result family

| Family | Local path | Verdict | Source-backed coverage | Blocking fields |
|---|---|---|---|---|
| strict candidate aggregate source | `/home/qiaosir/projects/remote_reviews/107/results/paper2/*.json` | `audit_only` / `blocked_missing_metadata` | 993 usable; `checkpoint_dir`, `analog_layers`, `n_states`, `sigma_c2c`, `sigma_d2d`, `ppl` present; `d2d_seed` present in 939 | `git_commit`, `command`, `dataset_*`, `ctx_len`, `stride`, `checkpoint_sha256`, C2C seed |
| D2D seed ablation | `/home/qiaosir/projects/remote_reviews/107/results/d2d_seed_ablation/*.json` | `partial_metadata_only` for planning only | 256 JSONs; 254 metric-bearing; 138 `checkpoint_dir`; 98 `d2d_seed`; 116 `max_steps` | same envelope fields; incomplete checkpoint and D2D-seed coverage |
| deliverable v2 | `/home/qiaosir/projects/remote_reviews/107/deliverable/results_v2/*.json` | `partial_metadata_only` for planning only | 49 JSONs; 49 metric-bearing; 20 `checkpoint_dir`; 48 `analog_layers`; 28 `max_steps` | same envelope fields; no `d2d_seed`; no hash |
| p0/p3 archive | `/home/qiaosir/projects/remote_reviews/107/deliverable/p0_p3_archive/*.json` | `deprecated_old_bug` / comparison-only | 134 JSONs; 109 metric-bearing | old/pre-v2 archive, missing envelope, no hash |
| deliverable v3 summaries | `/home/qiaosir/projects/remote_reviews/107/deliverable/results_v3/` | `audit_only` summary | summary-level ctx/stride/model and grouped means in `k107_plot_ready.json` / `k107_canonical_summary.csv` | not per-row JSON provenance; no command; no code SHA; no checkpoint hash |

Coverage source: `/home/qiaosir/projects/compute_vit/logs/CC_107_JSON_COVERAGE_20260510_112148.log:1-99`; v3 summary examples: `/home/qiaosir/projects/remote_reviews/107/deliverable/results_v3/k107_plot_ready.json:1-9` and `/home/qiaosir/projects/remote_reviews/107/deliverable/results_v3/k107_canonical_summary.csv:0-56`.

## 9. Recommended next action for Codex

Recommended Codex decision: `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`.

Recommended path:

1. Keep current `FRESH_D2D_SUMMARY_107_20260510.tsv` and `fig_107_*` artifacts audit-only.
2. Ask remote 107 for a signed manifest covering each candidate claim row: code SHA, exact command, config, dataset split, eval protocol, seed semantics, checkpoint path, checkpoint SHA-256, and old-vs-corrected pairing.
3. If no manifest exists, run the minimal corrected-noise matrix using the patched `p3_hat_train.py` / `p3_hat_eval.py` metadata envelope and generate checkpoint hashes locally on the remote host.
4. Reconcile the eval stride conflict before any manuscript table is locked.
5. Do not promote any Work-2/107 JSON into Paper1 source-data paths.

Generated companion TSVs:

- `/home/qiaosir/projects/compute_vit/coordination/agent_reports/Claude/CC_107_COMMAND_AND_CODE_PATHS_20260510.tsv`
- `/home/qiaosir/projects/compute_vit/coordination/agent_reports/Claude/CC_107_OLD_VS_CORRECTED_MAP_20260510.tsv`
