# Remote 107 Clean Branch Review — 2026-04-30

## Scope

Fetched and inspected new GitHub branch:

- Branch: `origin/107-clean`
- HEAD: `ecda16c`
- Commit: `107 clean deliverable branch`
- Inspection worktree: `/tmp/hat_107_clean`

This branch was inspected read-only. It was **not** merged into local working branch.

## Structural Verdict

`107-clean` is a standalone/orphan clean deliverable branch. It has no parent commit in the inspected commit object.

This is good for remote clone/use:

```bash
git clone -b 107-clean git@github.com:Leslie360/HAT.git HAT_107_clean
```

It is **not** a normal merge target for local main/current branch.

Reasons:

- It intentionally removes most repository history/content and leaves a small 107 deliverable set.
- Total inspected worktree size is ~2.6 MB.
- No checkpoint blobs are present.
- Only 204 files are present.

## Contents

Present key files:

- `RESULTS_SUMMARY.md`
- `deliverable/README.md`
- `deliverable/code/p3_hat_train.py`
- `deliverable/code/p3_hat_eval.py`
- `deliverable/code/analog_kv_cache.py`
- `deliverable/code/analog_layers.py`
- `deliverable/code/amp_utils.py`
- `deliverable/pipeline/pipeline_runner.py`
- `deliverable/results_v2/*.json`
- `deliverable/p0_p3_archive/*.json`
- Root convenience scripts: `p3_hat_train.py`, `p3_hat_eval.py`, `pipeline_runner.py`, `pipeline_d2d_seed.py`, `pipeline_next.py`, `pipeline_health.sh`

## Checks Run

Syntax check passed:

```bash
python -m py_compile deliverable/code/p3_hat_train.py deliverable/code/p3_hat_eval.py pipeline_d2d_seed.py pipeline_runner.py pipeline_next.py
```

Result: `PY_COMPILE_OK`.

## Fixes Confirmed

### 1. `--d2d-seed` exists in deliverable training code

`deliverable/code/p3_hat_train.py` now separates training seed and D2D pattern seed:

- `--seed`: training RNG
- `--d2d-seed`: D2D device-instance pattern seed

D2D buffer generation now uses:

```python
torch.manual_seed(d2d_seed + layer_idx)
```

This resolves the previous issue where D2D was always fixed by `0xD2D + layer_idx` regardless of CLI seed.

### 2. `hat_config.json` persistence exists

Training now writes sidecar metadata next to checkpoint:

```json
{
  "analog_layers": [...],
  "d2d_seed": ...,
  "n_states": ...
}
```

### 3. Eval auto-loads checkpoint metadata

`deliverable/code/p3_hat_eval.py` now auto-loads `analog_layers` and `d2d_seed` from `hat_config.json` if CLI overrides are not provided.

This fixes the selective-layer eval footgun where a last1/last2 checkpoint could be accidentally evaluated as all-layer.

### 4. `deliverable/code` imports are portable

`deliverable/code/p3_hat_train.py` and `deliverable/code/p3_hat_eval.py` now use:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

This is better than the previous hardcoded `/home/lisq753/projects/HAT/HAT` path.

## Remaining Issues

### R107-CLEAN-1 — `pipeline_d2d_seed.py` is same-instance ablation, not cross-instance fresh eval

The new `pipeline_d2d_seed.py` trains:

- D2D=0.02 with `d2d_seed={42,123,456,789,1001}`
- D2D=0.04 with `d2d_seed={42,123,456,789,1001}`

Then it evaluates each checkpoint at D2D={0.02,0.04,0.05}. However, eval does **not** explicitly sweep a separate eval `d2d_seed`; it auto-loads the checkpoint's `hat_config.json`, so train and eval use the same D2D device pattern.

This answers:

- Can HAT adapt to different fixed device instances if trained on each instance?

It does **not** answer:

- Does one trained checkpoint generalize to fresh unseen D2D device instances?

Both are useful, but they must be named differently.

Required action for true fresh-device claim:

- Add a second eval phase where each fixed checkpoint is evaluated with `--d2d-seed` override across `{42,123,456,789,1001}`.
- At minimum, use the train seed 42 checkpoint and evaluate across 5 fresh d2d seeds.
- Better: run a 5x5 train_d2d_seed × eval_d2d_seed matrix for D2D=0.02 and D2D=0.04, but this can be staged after the minimum matrix.

Recommended minimum task:

| Checkpoint | Eval D2D | Eval d2d_seed |
|---|---:|---|
| `hat_d2d002_500_v2_d2dseed42_seed42` | 0.02, 0.04, 0.05 | 42, 123, 456, 789, 1001 |
| `hat_d2d004_500_v2_d2dseed42_seed42` | 0.02, 0.04, 0.05 | 42, 123, 456, 789, 1001 |
| `hat_d2d002_last1_500_v2_seed42` or equivalent | 0.02, 0.04, 0.05 | 42, 123, 456, 789, 1001 |
| `hat_d2d002_last2_500_v2_seed42` or equivalent | 0.02, 0.04, 0.05 | 42, 123, 456, 789, 1001 |

### R107-CLEAN-2 — old result JSONs are not retroactively annotated

`deliverable/results_v2/*.json` still have no `d2d_seed` or `train_seed` fields.

Observed counts:

- result JSON files: 49
- JSONs with `d2d_seed`: 0
- JSONs with `train_seed`: 0

Therefore existing v2 numeric tables remain pre-metadata / provisional. New reruns should produce JSON with explicit seeds.

### R107-CLEAN-3 — root convenience scripts still use hardcoded remote paths

Root `p3_hat_train.py`, root `p3_hat_eval.py`, and root pipeline scripts still contain `/home/lisq753/...` hardcoding.

This is acceptable if the root scripts are 107-only convenience scripts, but the portable reproduction path should be documented as:

- use `deliverable/code/*.py` for portable core scripts
- use root scripts only on 107 server

### R107-CLEAN-4 — README still references `RESULTS_v2.md`, which is not present

`deliverable/README.md` says “See `RESULTS_v2.md` for full tables.” The actual file appears to be root `RESULTS_SUMMARY.md`.

Fix: update README reference or add `RESULTS_v2.md`.

## Current Recommended Response To 107

```text
107-clean branch received and inspected. This is a much better clean deliverable: small (~2.6 MB), no checkpoint blobs, standalone branch, portable deliverable/code imports, --d2d-seed added, and hat_config.json metadata persistence/autoload added. Syntax check passed.

Remaining correction: pipeline_d2d_seed.py currently tests same-instance adaptation, not fresh unseen D2D generalization, because eval auto-loads each checkpoint's own d2d_seed unless overridden. Please label current pipeline as same-instance/device-specific HAT. For fresh-device robustness, add eval override --d2d-seed and run at least:
- train checkpoint d2d_seed=42 for D2D=0.02 and D2D=0.04
- eval D2D={0.02,0.04,0.05}
- eval d2d_seed={42,123,456,789,1001}
Also do this for selective last1/last2 if GPU permits.

Old results_v2 JSONs still lack d2d_seed/train_seed fields, so keep old v2 numbers provisional. New rerun JSONs should include train_seed, d2d_seed, sigma_d2d, sigma_c2c, analog_layers, n_states, commit SHA, and whether eval d2d_seed was loaded from checkpoint or explicitly overridden.

Minor cleanup: deliverable README references RESULTS_v2.md but only RESULTS_SUMMARY.md exists.
```

## Local Integration Recommendation

Do not merge this branch into local main/current branch. Keep using it as a cloneable clean remote deliverable branch. If importing to local archive, copy it into a namespaced folder such as:

- `remote107_clean_deliverable/`

or keep the isolated worktree path only.
