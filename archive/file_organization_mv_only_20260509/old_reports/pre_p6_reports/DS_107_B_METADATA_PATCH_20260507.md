# DS-107-B: Metadata Patch Summary

**Date:** 2026-05-07
**Files patched:** `p3_hat_train.py`, `p3_hat_eval.py`
**Codebase:** `docs/data/remote_snapshots_20260507/hat_107_clean/`

---

## Patch Description

Added complete experiment metadata to both training and evaluation JSON outputs, as specified by the K-107-A metadata requirements.

### Training script (`p3_hat_train.py`)

**New imports:** `subprocess`

**New helper:** `_get_git_info()` — captures `git rev-parse HEAD` and `git status --short` for provenance.

**New CLI arguments:**
- `--batch_size` (default: 1) — formerly hardcoded in `train_hat()` call
- `--grad_accum` (default: 4) — formerly hardcoded in `train_hat()` call

**Fields added to training JSON (`result` dict):**

| Field | Source | Example |
|---|---|---|
| `mode` | hardcoded `"train"` | `"train"` |
| `model` | `model.config.model_type` | `"pythia-410m-deduped"` |
| `script` | `os.path.abspath(__file__)` | `"/home/.../p3_hat_train.py"` |
| `command` | `' '.join(sys.argv)` | `"p3_hat_train.py --name ..."` |
| `git_commit` | `_get_git_info()` | `"4ffb72c..."` |
| `git_status_short` | `_get_git_info()` | `"clean"` |
| `batch_size` | `args.batch_size` | `1` |
| `grad_accum` | `args.grad_accum` | `4` |
| `ctx_len` | `args.max_length` | `512` |
| `stride` | `0` (non-overlapping) | `0` |
| `dataset_train` | hardcoded | `"wikitext-2-raw-v1"` |
| `dataset_eval` | hardcoded | `"wikitext-2-raw-v1"` |

**Renamed field in training JSON:**
- `d2d_seed` → **`train_d2d_seed`** (disambiguates from eval D2D seed)

**Renamed field in `hat_config.json`:**
- `d2d_seed` → **`train_d2d_seed`** (so downstream eval can distinguish)

### Evaluation script (`p3_hat_eval.py`)

**New imports:** `subprocess`

**New helper:** `_get_git_info()` (same as training)

**New state:** `train_d2d_seed` captured from `hat_config.json` (reads `train_d2d_seed` key; falls back to old `d2d_seed` key for backward compatibility with pre-patch checkpoints).

**Fields added to eval JSON (`result` dict):**

| Field | Source | Example |
|---|---|---|
| `mode` | hardcoded `"eval"` | `"eval"` |
| `model` | `model.config.model_type` | `"pythia-410m-deduped"` |
| `script` | `os.path.abspath(__file__)` | `"/home/.../p3_hat_eval.py"` |
| `command` | `' '.join(sys.argv)` | `"p3_hat_eval.py --checkpoint_dir ..."` |
| `git_commit` | `_get_git_info()` | `"4ffb72c..."` |
| `git_status_short` | `_get_git_info()` | `"clean"` |
| `train_d2d_seed` | from `hat_config.json` | `53714` |
| `eval_d2d_seed` | CLI override or fallback | `1001` |
| `ctx_len` | `args.max_length` | `512` |
| `stride` | `0` (non-overlapping) | `0` |
| `dataset_eval` | hardcoded | `"wikitext-2-raw-v1"` |

**Renamed field in eval JSON:**
- `d2d_seed` → **`eval_d2d_seed`** (the seed actually used for this eval run)

**JSON output filename:**
- Changed from `..._seed{seed}.json` → `..._evalseed{seed}.json` to clarify the seed in the filename is the eval D2D seed.

### Backward Compatibility

- `hat_config.json` without `train_d2d_seed` (pre-patch checkpoints): eval falls back to `hat_cfg.get("d2d_seed", None)`
- Checkpoints without `hat_config.json` at all: `train_d2d_seed = None`
- `d2d_seed` CLI argument with `default=None` still auto-loads from `hat_config.json` by reading the `d2d_seed` key — this maintains the existing eval workflow

---

## Compilation

```
$ python3 -m py_compile p3_hat_train.py  → train OK
$ python3 -m py_compile p3_hat_eval.py   → eval OK
```

---

## Example JSON Output

### Training (`last1_d2d002_seed42.json`)

```json
{
  "name": "last1_d2d002",
  "mode": "train",
  "model": "pythia-410m-deduped",
  "script": "/home/lisq753/projects/HAT_kv107/paper2/p3_hat_train.py",
  "command": "p3_hat_train.py --name last1_d2d002 --sigma_d2d 0.02 --analog_layers 23 --seed 42 --d2d_seed 53714 --max_steps 100",
  "git_commit": "4ffb72c9e5f3a1b2c3d4e5f6a7b8c9d0e1f2a3b4",
  "git_status_short": "clean",
  "train_seed": 42,
  "train_d2d_seed": 53714,
  "n_states": 256,
  "sigma_c2c": 0.01,
  "sigma_d2d": 0.02,
  "analog_layers": [23],
  "lr": 1e-5,
  "batch_size": 1,
  "grad_accum": 4,
  "max_steps": 100,
  "ctx_len": 512,
  "stride": 0,
  "dataset_train": "wikitext-2-raw-v1",
  "dataset_eval": "wikitext-2-raw-v1",
  "retention_step_time": 0.0,
  "ppl_before": 15.68,
  "ppl_after": 18.42,
  "losses": [...]
}
```

### Evaluation (`eval_last1_d2d002_seed42_c2c0.01_d2d0.02_evalseed1001.json`)

```json
{
  "mode": "eval",
  "model": "pythia-410m-deduped",
  "script": "/home/lisq753/projects/HAT_kv107/paper2/p3_hat_eval.py",
  "command": "p3_hat_eval.py --checkpoint_dir .../checkpoints/last1_d2d002_seed42 --sigma_d2d 0.02 --d2d_seed 1001",
  "git_commit": "4ffb72c9e5f3a1b2c3d4e5f6a7b8c9d0e1f2a3b4",
  "git_status_short": "clean",
  "checkpoint_dir": ".../checkpoints/last1_d2d002_seed42",
  "n_states": 256,
  "sigma_c2c": 0.01,
  "sigma_d2d": 0.02,
  "train_d2d_seed": 53714,
  "eval_d2d_seed": 1001,
  "retention_step_time": 0.0,
  "analog_layers": [23],
  "ctx_len": 512,
  "stride": 0,
  "dataset_eval": "wikitext-2-raw-v1",
  "ppl": 18.42
}
```

Key distinction: `train_d2d_seed=53714` identifies the device instance used during training, while `eval_d2d_seed=1001` identifies the fresh device instance used for this evaluation.
