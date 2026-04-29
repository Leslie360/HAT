# Task: Audit R11D-4 PCM Fix — Training & Eval Code Review

**task_id:** audit_r11d4_pcm_fix
**priority:** HIGHEST (code correctness before re-run)
**target output:** `outputs/audit_r11d4_pcm_fix.md`
**gpu_hours:** 0 (code review only)
**owner:** ds_flash (coder) → codex (reviewer) → gemini (critic)

---

## Background

R11D-4 PCM training was stopped because the process did not appear in `nvidia-smi` Processes list, suggesting it may have been running on CPU instead of GPU. Before restarting training, the fix code must be audited for correctness.

Three files were modified/created:
1. `paper2_aihwkit_baseline/r11d4_train_pcm.py` — switched from `AdamW` to `AnalogSGD`
2. `paper2_aihwkit_baseline/eval_aihwkit_fresh.py` — added `replace_rpu_config` fix after `load_state_dict`
3. `paper2_aihwkit_baseline/eval_aihwkit_drift.py` — new drift evaluation script

---

## Goal

Audit all three files for correctness, GPU utilization, and methodological soundness.

### Check 1: Training script (`r11d4_train_pcm.py`)

**Specific concerns:**
1. `AnalogSGD` import and usage — does `AnalogSGD(model.parameters(), lr=5e-4, weight_decay=0.05)` correctly trigger PCM pulse-update physics via `post_update_step()`?
2. `CosineAnnealingLR` compatibility — does `AnalogSGD` work with PyTorch's standard scheduler?
3. GPU binding — why did the training process NOT show up in `nvidia-smi` Processes? Is `model.to(device)` actually moving AnalogLinear layers to CUDA?
4. Learning rate — `AnalogSGD` typically needs higher LR than `AdamW` (5e-4 may be too low for SGD). Should LR be adjusted?
5. Momentum — `AnalogSGD` default momentum may differ from AdamW's adaptive moments. Is this a problem?

### Check 2: Fresh eval script (`eval_aihwkit_fresh.py`)

**Specific concerns:**
1. `replace_rpu_config` fix — after `load_state_dict`, does iterating `model.modules()` and calling `replace_rpu_config` on all `AnalogLinear` layers correctly restore `enable_during_test=True`?
2. Tile audit — the script now records tile config in JSON. Does this correctly prove the fix worked?
3. Device transfer — should `model.to(device)` happen BEFORE or AFTER `replace_rpu_config`?

### Check 3: Drift eval script (`eval_aihwkit_drift.py`)

**Specific concerns:**
1. `apply_drift` function — does `module.drift_analog_weights(t_inference=t)` correctly apply PCM drift?
2. Model rebuild per time point — rebuilding the model for each drift time is correct (avoids cumulative drift), but is it efficient?
3. `enable_during_test=False` for drift eval — is this correct? Drift eval should measure conductance drift, not D2D noise.

### Check 4: GPU verification

Write a minimal test script that:
1. Creates a single `AnalogLinear` with `PCMPresetUnitCell`
2. Moves it to CUDA
3. Runs one forward pass
4. Verifies the process shows up in `nvidia-smi`

If the process does NOT show up, document why (AIHWKit may run simulation on CPU even when PyTorch tensor is on GPU).

---

## Decision rule

**Approve** if:
- All 3 files are technically correct
- GPU binding issue is explained or fixed
- No blocking methodology flaws

**Reject** if:
- `AnalogSGD` usage is incorrect (e.g., wrong signature, missing arguments)
- `replace_rpu_config` fix does not actually restore `enable_during_test=True`
- GPU is not being used (training would take hours instead of ~1.5h)
- Any blocking issue found

---

## Done definition

- `outputs/audit_r11d4_pcm_fix.md` exists with:
  1. File-by-file audit results
  2. GPU binding diagnosis
  3. List of required fixes (if any)
  4. Go / No-go recommendation for training restart
