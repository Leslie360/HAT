# Remote 107 Metadata Patch — 2026-05-08

**Status:** P0 complete — both train and eval scripts patched and verified.

---

## 1. What Changed

Modified `p3_hat_train.py` and `p3_hat_eval.py` so every JSON output now includes a complete metadata envelope.

### 1.1 New Fields (both scripts)

| Field | Source | Train | Eval |
|:---|:---|:---:|:---:|
| `git_commit` | `git rev-parse HEAD` | ✅ | ✅ |
| `git_status_short` | `git status --short` | ✅ | ✅ |
| `script` | `os.path.basename(__file__)` | ✅ | ✅ |
| `command` | `" ".join(sys.argv)` | ✅ | ✅ |
| `mode` | literal `"train"` / `"eval"` | ✅ | ✅ |
| `model` | `args.model_name` / `args.checkpoint_dir` | ✅ | ✅ |
| `dataset_train` | `"wikitext-2-raw-v1 (train)"` | ✅ | `null` |
| `dataset_eval` | `"wikitext-2-raw-v1 (test)"` | ✅ | ✅ |
| `train_seed` | `args.seed` | ✅ | `null` |
| `train_d2d_seed` | `args.d2d_seed` | ✅ | `null` |
| `eval_d2d_seed` | `d2d_seed` (eval local) | `null` | ✅ |
| `n_states` | `args.n_states` | ✅ | ✅ |
| `sigma_c2c` | `args.sigma_c2c` | ✅ | ✅ |
| `sigma_d2d` | `args.sigma_d2d` | ✅ | ✅ |
| `retention_step_time` | `args.retention_step_time` | ✅ | ✅ |
| `analog_layers` | sorted list | ✅ | ✅ |
| `ctx_len` | `args.max_length` | ✅ | ✅ |
| `stride` | `max_length // 2` (train) / `max_length` (eval) | ✅ | ✅ |
| `max_steps` | `args.max_steps` | ✅ | `null` |
| `batch_size` | `1` (no batching in current recipe) | ✅ | ✅ |
| `ppl_before` | pre-HAT eval | ✅ | — |
| `ppl_after` | post-HAT eval | ✅ | — |
| `ppl` | eval PPL | — | ✅ |
| `wall_clock_time` | `time.time() - start_time` | ✅ | ✅ |
| `gpu_id` | `CUDA_VISIBLE_DEVICES` env var | ✅ | ✅ |
| `gpu_name` | `torch.cuda.get_device_name(0)` | ✅ | ✅ |

### 1.2 Preserved Legacy Fields

Train still outputs: `epochs`, `lr`, `losses`.

---

## 2. Example Outputs

### 2.1 Train JSON

`test_meta_seed42.json` (10-step smoke test):

```json
{
  "git_commit": "2b57a2272ef629df39b56a6eabf461bd43e55797",
  "git_status_short": "M p3_hat_eval.py\nM p3_hat_train.py\n...",
  "script": "p3_hat_train.py",
  "command": "p3_hat_train.py --name test_meta --model_name EleutherAI/pythia-410m-deduped --sigma_d2d 0.02 --sigma_c2c 0.01 --max_steps 10 --seed 42 --analog_layers 23 --output_dir /tmp/test_meta_train",
  "mode": "train",
  "model": "EleutherAI/pythia-410m-deduped",
  "dataset_train": "wikitext-2-raw-v1 (train)",
  "dataset_eval": "wikitext-2-raw-v1 (test)",
  "train_seed": 42,
  "train_d2d_seed": 3373,
  "eval_d2d_seed": null,
  "n_states": 256,
  "sigma_c2c": 0.01,
  "sigma_d2d": 0.02,
  "retention_step_time": 0.0,
  "analog_layers": [23],
  "ctx_len": 512,
  "stride": 256,
  "max_steps": 10,
  "batch_size": 1,
  "epochs": 1,
  "lr": 1e-05,
  "ppl_before": 23.299391239025578,
  "ppl_after": 21.84852454917814,
  "losses": [3.069, 3.303, ...],
  "wall_clock_time": 156.01,
  "gpu_id": "7",
  "gpu_name": "NVIDIA PH402 SKU 200"
}
```

### 2.2 Eval JSON

`eval_410m_last1_v2_seed42_c2c0.0_d2d0.0_seed42.json`:

```json
{
  "git_commit": "2b57a2272ef629df39b56a6eabf461bd43e55797",
  "git_status_short": "M p3_hat_eval.py\nM p3_hat_train.py\n...",
  "script": "p3_hat_eval.py",
  "command": "p3_hat_eval.py --checkpoint_dir ... --n_states 256 --sigma_d2d 0.0 --sigma_c2c 0.0 --max_length 512 --output_dir /tmp/test_meta_eval --d2d-seed 42",
  "mode": "eval",
  "model": "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/410m_last1_v2_seed42",
  "dataset_train": null,
  "dataset_eval": "wikitext-2-raw-v1 (test)",
  "train_seed": null,
  "train_d2d_seed": null,
  "eval_d2d_seed": 42,
  "n_states": 256,
  "sigma_c2c": 0.0,
  "sigma_d2d": 0.0,
  "retention_step_time": 0.0,
  "analog_layers": [23],
  "ctx_len": 512,
  "stride": 512,
  "max_steps": null,
  "batch_size": 1,
  "ppl": 18.57946135715318,
  "wall_clock_time": 64.79,
  "gpu_id": "7",
  "gpu_name": "NVIDIA PH402 SKU 200"
}
```

---

## 3. Backward Compatibility

- Old JSONs in `results/paper2/` are **not** rewritten. Only newly produced JSONs carry the envelope.
- `hat_config.json` inside checkpoints is untouched.
- No CLI argument changes — existing launcher scripts work without modification.

---

## 4. Verification

- [x] Train smoke test (10 steps, 410M, GPU 7) — passes, JSON schema validated
- [x] Eval smoke test (410m_last1 checkpoint, GPU 7) — passes, JSON schema validated
- [x] Git fields populate correctly when run inside repo
- [x] GPU fields populate correctly on CUDA device
- [x] `command` field captures full argv

---

## 5. Files Changed

```
M p3_hat_train.py
M p3_hat_eval.py
```

---

## 6. Ready for K107-A

Metadata patch is live. All new train/eval runs will carry full provenance. Proceeding to K107-A canonical selective KV re-run.
