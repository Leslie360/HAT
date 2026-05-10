# Codex 107 Metadata Acceptance Protocol

Date: 2026-05-10
Owner: Codex
Purpose: Define how Codex will accept or reject recovered Remote-107 metadata from CC.

## Baseline rule

No Paper2/107 row becomes claim-bearing unless it has source-backed metadata for code version, command, protocol, checkpoint provenance, and seed semantics. Good-looking PPL values are not enough.

## Required source-backed fields

| Field | Acceptance standard |
|---|---|
| `commit` | Exact git SHA of the code that produced the row, with local citation. Branch name alone is insufficient. |
| `corrected_noise_code_path` | File/function/line range or commit diff showing corrected-noise implementation. |
| `command` | Exact train/eval command or launcher command that produced the row/family. Reconstructed commands must be labeled reconstructed and are not enough for claim lock unless independently supported. |
| `config` | Config file or command flags covering model, analog layers, noise, steps, context, batch, stride, and output path. |
| `dataset` | Dataset name and split. If WikiText is used, identify train/test/validation split and preprocessing assumptions if recoverable. |
| `eval_protocol` | Context length, stride/sliding-window rule, batch size, PPL calculation, and evaluation subset policy. |
| `seed_semantics` | Train seed, D2D seed, C2C randomness, eval seed, and whether reported seeds are fresh device instances or repeated evals. |
| `checkpoint_path` | Path string for the exact checkpoint used. |
| `checkpoint_sha256` | Hash from an existing manifest or safe local hash command. Do not copy checkpoint payloads. |
| `old_vs_corrected` | Matched old and corrected rows with same model family, analog layer list, noise setting, context/protocol, and seed semantics. |

## Row status labels

| Label | Meaning |
|---|---|
| `claim_lock_pass` | All required fields are source-backed and row grouping is exact. |
| `claim_lock_partial` | Useful for planning, but one or more required fields are missing. |
| `audit_only` | PPL row is valid as a diagnostic candidate but not for manuscript claims. |
| `blocked_missing_metadata` | Metadata cannot be recovered locally; rerun or signed manifest required. |
| `invalid_mixed_conditions` | Row mixes incompatible checkpoints, protocols, noise settings, or seeds. |
| `deprecated_old_bug` | Old/bugged row retained only for comparison, not as corrected evidence. |

## Acceptance decision tree

1. If any required metadata field is absent for a row, mark that row `claim_lock_partial` or `blocked_missing_metadata`.
2. If a row can only be linked to a broad family such as `last1` or `all24`, but not an exact checkpoint/protocol, keep it `audit_only`.
3. If old-vs-corrected values differ in context length, checkpoint family, analog layers, or eval protocol, mark comparison `invalid_mixed_conditions`.
4. If checkpoint hashes cannot be recovered, claim lock remains blocked even if commands and PPL are known.
5. If CC recovers all metadata for only a subset, Codex may lock only that subset and must keep other rows audit-only.

## Minimum claim-lock table

Before Paper2 drafting, Codex needs a table with these columns:

```text
status
run_id
checkpoint
checkpoint_sha256
analog_layers
train_noise
eval_c2c
eval_d2d
train_seed
d2d_seed
c2c_seed
dataset_split
context_length
stride
batch_size
ppl
json_path
command_source
code_sha
corrected_noise_code_path
notes
```

## If metadata remains blocked

If CC cannot recover enough metadata, the next action is one of:

1. Ask the remote 107 side for a signed manifest covering the missing fields.
2. Rerun the minimal corrected-noise matrix with JSON sidecars containing all required fields.
3. Keep current TSV/figures as audit-only and postpone Paper2 claim drafting.

## Non-negotiable boundaries

- Do not backfill missing metadata by guesswork.
- Do not mix old bugged and corrected-noise rows except in explicitly labeled comparison tables.
- Do not move Work-2 JSONs into Paper1 source-data paths.
- Do not cite draft audit figures as final evidence.
