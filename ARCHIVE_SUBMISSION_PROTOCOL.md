# HAT Archive Submission Protocol

> Any experimental packet that intends to be claim-locked, peer-reviewed, or paper-submitted must satisfy the completeness rules below. Missing items will be rejected at audit.

---

## 1. Per-Row Artifact Rule

Every row in the manifest must have a corresponding source-backed artifact file committed to the repo.

| Artifact type | Required? | Acceptable formats |
|---------------|-----------|-------------------|
| Per-row JSON sidecar | **Yes** | `.json` with complete metadata envelope |
| Per-row eval log | Recommended | `.log` (stdout + stderr) |
| Checkpoint payload | **No** | Never commit model weights to git. Store checkpoint SHA256 in JSON instead. |

**Verification:**
```bash
git ls-tree -r --name-only origin/107-clean <artifact_dir> | wc -l
# must equal or exceed manifest row count
```

## 2. JSON Metadata Envelope (Mandatory Fields)

Every eval JSON must include:

```json
{
  "run_id": "...",
  "commit": "...",
  "git_status_short": "...",
  "command": "...",
  "config": { ... },
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
  "layer_label": "...",
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

If any field is unavailable, write `UNKNOWN` and explain why in `notes`. Do not silently omit fields.

## 3. Manifest TSV

A tab-separated manifest must be committed alongside the JSONs. Columns:

```text
run_id, json_filename, checkpoint_family, checkpoint_path, checkpoint_sha256,
code_commit, git_status_short, corrected_noise_code_path, corrected_noise_function_or_diff,
train_command, eval_command, config_path_or_inline_config, dataset_name, dataset_split,
tokenizer_or_preprocess, context_length, stride, batch_size, ppl_definition,
analog_layers, layer_label, train_seed, d2d_seed, c2c_seed, eval_seed,
sigma_c2c, sigma_d2d, ppl, old_bugged_reference_if_any, comparison_valid, notes
```

## 4. Report Markdown

A human-readable report must summarize:
- Total rows, claim-lockable rows, blocked rows
- Breakdown by family / configuration
- Blocker list (if any)
- Output file paths
- Verification commands with expected counts

## 5. Code Immutability

- Do not modify Paper1 sources for Paper2 experiments.
- All eval commands must be reproducible from committed code at the stated `commit`.
- If a bug fix is required mid-experiment, note `corrected_noise_commit` and re-run the affected subset (P0) before full re-run.

## 6. JSON Serialization Safety

All `json.dump` calls in the eval pipeline must use `default=str` as a fallback, and any recursive sanitizer must handle:
- `torch.dtype` / `numpy.dtype`
- numpy scalars (`np.float32`, `np.int64`, etc.)
- `tuple`, `set`, `bytes`
- scalar tensors (`hasattr(obj, 'item')`)

## 7. Checklist Before Push

- [ ] Artifact count >= manifest row count
- [ ] Every manifest `run_id` matches one JSON filename
- [ ] `checkpoint_sha256` computed and non-empty for all non-digital rows
- [ ] `commit` hash exists on `origin/107-clean`
- [ ] `json.dump` uses `default=str` or equivalent sanitizer
- [ ] No checkpoint payloads in git
- [ ] Report includes verification commands
