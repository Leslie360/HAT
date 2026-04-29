# CODEX_R11D_RESULTS_REVIEW_20260429

**Date:** 2026-04-29 CST  
**Scope:** Review of newly landed R11D corrected multi-seed / oracle / T1-3 outputs.

## 1. Valid Completed Result

### R11D-7 4-bit PCM seed=123

Status: **VALID / CANONICAL**

- Script: `paper2_aihwkit_baseline/r11d4_train_pcm.py`
- Code SHA: `a07df95452a84dbcd8b7bb6358716335ceaa2116b22c338392bbbddb7a21999c`
- Preset: `PCMPresetUnitCell`
- Optimizer: `AnalogSGD`
- Config: 4-bit PCM, `inp_res=out_res=0.0625`, `modifier_std_dev=0.10`, batch size 64, seed 123
- Best test: **76.74%** at epoch 97
- Final test: **76.33%** at epoch 100
- Runtime: 2.86h

Interpretation:
- This matches the original R11D-7 seed=42 result (76.54%) within +0.20pp.
- This is strong evidence that 4-bit PCM convergence is not a single-seed accident.
- Do not lock the final narrative until seed=456 and 8-bit PCM seeds finish, but the first corrected replicate supports the current PCM 4-bit claim.

## 2. Diagnostic Completed Result

### T1-4 Oracle: 8-bit PCM, modifier_std_dev=0.0

Status: **DIAGNOSTIC ONLY / NOT PAPER-FACING**

- Best test: **61.36%** at epoch 98
- Final test: 61.19% at epoch 100
- Preset: `PCMPresetUnitCell`
- Optimizer: `AnalogSGD`
- Caveat: launched from temporary extended script; checkpoint provenance has `args_has_pcm_preset=True`, `pcm_preset=None`, non-canonical code SHA.

Interpretation:
- The result is useful diagnostically: removing training-time modifier noise drops 8-bit PCM from ~76.96% to 61.36%.
- This suggests the `modifier_std_dev=0.10` path acts as necessary regularization/noise exposure rather than simply a penalty.
- Because provenance is non-canonical, this should not be placed in paper-facing tables unless rerun under a locked script.

## 3. Invalid / Stopped Result

### T1-3 PCMPresetDevice rerun

Status: **INVALID / STOPPED BY CODEX**

I stopped the active T1-3 run during review.

Invalidity reasons:
- It violated the active strategy gate: no parallel non-multi-seed GPU work before corrected multi-seed completes.
- It was launched from cwd `paper2_aihwkit_baseline/checkpoints`, causing artifacts to be written under nested `checkpoints/paper2_aihwkit_baseline/...` paths.
- It used `--batch-size 128`, while the intended preset comparison must match baseline training conditions unless explicitly defined as a batch-size ablation.
- The output directory overlaps with previously invalid/partial `PCMPresetDevice_seed42` naming.

Action taken:
- Killed only the T1-3 processes.
- Left `R11D-7 seed=456` and the corrected multi-seed pipeline running.
- Added `INVALID_DO_NOT_USE.md` to the nested T1-3 artifact directory.

## 4. Current Active Run

### R11D-7 4-bit PCM seed=456

Status: **RUNNING / VALID SO FAR**

- Script: canonical `r11d4_train_pcm.py`
- Config: same as seed=123 except seed=456
- Early log: epoch 9 best 32.58% at review time; still too early to judge.

## 5. Decision

- Continue corrected multi-seed pipeline without launching additional GPU tasks.
- After all four training runs finish, compute seed mean/std for train best and then run fresh eval on the corrected seed checkpoints if GPU budget allows.
- Do not restart T1-3 until all corrected multi-seed runs finish and the launcher is fixed to `cd /home/qiaosir/projects/compute_vit` before execution.

## 6. Update — pipeline false-completion bug found (2026-04-29 10:08 CST)

During follow-up review, the completed multi-seed pipeline was found to contain a false completion:

- `R11D-7 seed=456` printed `=== r11d_7_pcm_4bit seed=456 complete ===`, but the checkpoint directory had no `training_history.json` and no `last.pt`.
- The log stops at epoch 46; partial `best.pt` is epoch 41 with test_acc 66.08%.
- Root cause: `run_pcm_multi_seed_v2.sh` used `set -e` but not `pipefail`, so a failed/interrupted Python process inside `python ... | tee -a log` could be masked by `tee` returning 0.

Actions taken:
- Patched `run_pcm_multi_seed_v2.sh` to `set -euo pipefail`.
- Added post-run artifact checks for `training_history.json` and `last.pt`.
- Archived the partial seed456 directory as `r11d_7_pcm_4bit_seed456_PARTIAL_PIPEFAIL_BUG_20260429_100717` with `INVALID_DO_NOT_USE.md`.
- Launched a clean canonical rerun of `R11D-7 seed=456` with correct AIHWKit `LD_LIBRARY_PATH`.

Valid completed corrected runs so far:
- `R11D-7 seed=123`: best 76.74%.
- `R11D-5a seed=123`: best 77.00%.
- `R11D-5a seed=456`: best 78.36%.

Pending:
- Clean rerun of `R11D-7 seed=456`.

Decision:
- Do not compute final 4-bit PCM seed mean/std until the clean rerun completes.
- Do not use the partial seed456 best=66.08% in any table or narrative.
