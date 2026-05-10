# Remote 107 Metadata Recovery Or Minimal Rerun Request

Date: 2026-05-10
Issued by: Codex
Status: Standby task. Use only if CC metadata harvest cannot close the evidence gates locally.

## Purpose

The current returned 107 JSON files contain useful PPL values but lack the metadata required for Paper2 claims. If local metadata recovery fails, Remote 107 must return either a signed metadata manifest for the existing results or a minimal corrected-noise rerun with complete JSON sidecars.

## Option A - signed manifest for existing results

Return a single Markdown report plus TSV/CSV manifest that covers every claim-candidate JSON row.

Required columns:

```text
run_id
json_filename
checkpoint_path
checkpoint_sha256
code_commit
corrected_noise_file
corrected_noise_function
train_command
eval_command
config_path
dataset_name
dataset_split
tokenizer_or_preprocess
context_length
stride
batch_size
analog_layers
train_seed
d2d_seed
c2c_seed
eval_seed
sigma_c2c
sigma_d2d
ppl
old_bugged_reference_if_any
notes
```

Rules:

- Do not send checkpoint payloads.
- Do not change old JSON values silently.
- If a field cannot be certified, write `UNKNOWN` and explain why.
- Include `git status --short` and `git rev-parse HEAD`.
- Include the exact code path/line range or diff that fixes the corrected-noise bug.

## Option B - minimal rerun with complete sidecars

If a signed manifest cannot be produced, rerun only the minimal matrix needed to lock the selective-KV claim.

### Required matrix

| Family | Analog layers | Eval noise | D2D seeds | Purpose |
|---|---|---|---|---|
| Digital reference | none | no analog noise | 1 | PPL reference under same eval protocol |
| Last1 | `[23]` | D2D=0.02, 0.05 | at least 5 | selective terminal route |
| Last2 | `[22,23]` | D2D=0.02, 0.05 | at least 5 | deployment-cost comparison |
| Last4 | `[20,21,22,23]` | D2D=0.02, 0.05 | at least 5 | scaling control |
| All24 | `[0..23]` | D2D=0.02, 0.05 | at least 5 if feasible, otherwise 3 with rationale | stress control |

Optional but useful:

| Family | Analog layers | Eval noise | D2D seeds | Purpose |
|---|---|---|---|---|
| Last1 combined | `[23]` | C2C=0.01 + D2D=0.02 | at least 5 | mixed-noise robustness |
| Last2 combined | `[22,23]` | C2C=0.01 + D2D=0.02 | at least 5 | mixed-noise cost comparison |

## Required JSON sidecar fields for rerun

Every JSON must include:

```json
{
  "run_id": "...",
  "commit": "...",
  "git_status_short": "...",
  "command": "...",
  "config": {...},
  "dataset": "...",
  "dataset_split": "...",
  "eval_protocol": {
    "context_length": 0,
    "stride": 0,
    "batch_size": 0,
    "ppl_definition": "..."
  },
  "checkpoint_dir": "...",
  "checkpoint_sha256": "...",
  "analog_layers": [],
  "train_seed": 0,
  "d2d_seed": 0,
  "c2c_seed": 0,
  "sigma_c2c": 0.0,
  "sigma_d2d": 0.0,
  "retention_step_time": 0.0,
  "ppl": 0.0,
  "corrected_noise_code_path": "...",
  "corrected_noise_commit": "..."
}
```

## Old-vs-corrected comparison

Return a separate table:

```text
old_run_id
old_status
old_ppl
corrected_run_id
corrected_ppl
matched_checkpoint_family
matched_analog_layers
matched_eval_noise
matched_eval_protocol
trend_preserved
comparison_valid
notes
```

Set `comparison_valid=false` if context length, checkpoint family, analog layers, eval protocol, or seed semantics differ.

## Return format

Return:

1. `REMOTE_107_METADATA_RECOVERY_REPORT_YYYYMMDD.md`
2. `REMOTE_107_METADATA_MANIFEST_YYYYMMDD.tsv` or `.csv`
3. Rerun JSONs only if Option B is used
4. No checkpoint payloads unless explicitly requested

## Codex acceptance boundary

Codex will accept only source-backed rows. Any row with missing `commit`, `command`, `dataset`, `eval_protocol`, `checkpoint_sha256`, or seed semantics remains audit-only.
