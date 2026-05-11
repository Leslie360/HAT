# Remote 107 Selective KV Claim-Lock Task

Date: 2026-05-11
Issued by: Claude / local compute_vit
Priority: P0 for Paper2 107 evidence lock
Status: Ready for Remote 107 pull and execution

## Why this task exists

Local audit has enough candidate PPL trends for selective KV-cache, but the current 107 package is still audit-only because required provenance fields are missing. The most important next step is not a bigger experiment; it is to make the selective-KV evidence source-backed and claim-lockable.

Do not copy checkpoint payloads into git. Do not modify Paper1 sources. Tee every command to a timestamped log.

## Inputs already in repo

Read these first:

- `coordination/remote_tasks/107/REMOTE_107_METADATA_RECOVERY_OR_MINIMAL_RERUN_REQUEST_20260510.md`
- `coordination/remote_tasks/107/CODEX_107_METADATA_ACCEPTANCE_PROTOCOL_20260510.md`
- `paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv`
- `paper2/results/METADATA_COMPLETENESS_107_20260510.tsv`
- `paper2/results/kv_cache_107_canonical_manifest_20260510.tsv`

The local 2026-05-10/11 tables and figures are candidate/audit artifacts only unless you close the gates below.

## Primary task: metadata recovery for existing corrected-noise results

For every candidate row that supports the selective terminal-layer story, return a source-backed manifest with these fields:

```text
run_id
json_filename
checkpoint_family
checkpoint_path
checkpoint_sha256
code_commit
git_status_short
corrected_noise_code_path
corrected_noise_function_or_diff
train_command
eval_command
config_path_or_inline_config
dataset_name
dataset_split
tokenizer_or_preprocess
context_length
stride
batch_size
ppl_definition
analog_layers
layer_label
train_seed
d2d_seed
c2c_seed
eval_seed
sigma_c2c
sigma_d2d
ppl
old_bugged_reference_if_any
comparison_valid
notes
```

Required candidate families:

- digital reference / no analog layers
- last1 `[23]`
- last2 `[22,23]`
- last4 `[20,21,22,23]`
- all24 `[0..23]`

Required eval points if existing evidence can be certified:

- D2D=0.02, C2C=0.0, at least 5 D2D seeds for last1/last2/last4/all24 if available
- D2D=0.05, C2C=0.0, at least 5 D2D seeds for last1/last2/last4/all24 if available
- digital reference under the exact same dataset/tokenizer/context/stride/batch/PPL protocol

If a field cannot be source-certified, write `UNKNOWN` and explain why. Do not silently infer missing fields from filenames.

## Fallback task: minimal corrected-noise rerun

If the existing JSONs cannot be made claim-lockable, rerun only this matrix with complete JSON sidecars:

| Family | Analog layers | Eval C2C | Eval D2D | D2D seeds | Required? |
|---|---:|---:|---:|---:|---|
| digital | none | 0.0 | 0.0 | 1 | yes |
| last1 | `[23]` | 0.0 | 0.02 | 5 | yes |
| last1 | `[23]` | 0.0 | 0.05 | 5 | yes |
| last2 | `[22,23]` | 0.0 | 0.02 | 5 | yes |
| last2 | `[22,23]` | 0.0 | 0.05 | 5 | yes |
| last4 | `[20,21,22,23]` | 0.0 | 0.02 | 5 | yes |
| last4 | `[20,21,22,23]` | 0.0 | 0.05 | 5 | yes |
| all24 | `[0..23]` | 0.0 | 0.02 | 5 if feasible, otherwise 3 with rationale | stress control |
| all24 | `[0..23]` | 0.0 | 0.05 | 5 if feasible, otherwise 3 with rationale | stress control |

Use the corrected-noise code path only. Use one GPU job at a time unless you have explicit capacity. If memory pressure appears, reduce batch size only enough to keep the run stable and record the change.

Every JSON sidecar must include:

```json
{
  "run_id": "...",
  "commit": "...",
  "git_status_short": "...",
  "command": "...",
  "config": {},
  "dataset": "...",
  "dataset_split": "...",
  "eval_protocol": {
    "context_length": 0,
    "stride": 0,
    "batch_size": 0,
    "ppl_definition": "negative-log-likelihood token average then exp, or exact definition used"
  },
  "checkpoint_dir": "...",
  "checkpoint_sha256": "...",
  "analog_layers": [],
  "layer_label": "last1|last2|last4|all24|digital",
  "train_seed": 0,
  "d2d_seed": 0,
  "c2c_seed": 0,
  "eval_seed": 0,
  "sigma_c2c": 0.0,
  "sigma_d2d": 0.0,
  "ppl": 0.0,
  "corrected_noise_code_path": "...",
  "corrected_noise_commit": "..."
}
```

## Required return files

Commit and push, or otherwise return, these files:

1. `coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_REPORT_YYYYMMDD.md`
2. `coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_MANIFEST_YYYYMMDD.tsv`
3. If rerun was required: complete JSON sidecars under `paper2/results/remote_107_selective_kv_lock_YYYYMMDD/`
4. Timestamped logs under `logs/` or a remote log directory, with filenames listed in the report

## Acceptance criteria

A row is claim-lockable only if these fields are source-backed and non-empty:

- commit
- command
- config or complete inline config
- dataset and dataset_split
- eval_protocol
- checkpoint_sha256
- analog_layers / layer_label
- seed semantics: train_seed, d2d_seed, c2c_seed or explicit `none`, eval_seed
- corrected_noise_code_path and corrected_noise_commit

If any required field is missing, mark the row `blocked_audit_only` and explain the blocker. The final report must separate `claim_lockable` rows from `blocked_audit_only` rows.

## Short success message expected back

Reply with:

- commit hash you pushed
- report path
- manifest path
- whether you used metadata recovery or rerun
- number of claim-lockable rows by family
- blockers, if any
