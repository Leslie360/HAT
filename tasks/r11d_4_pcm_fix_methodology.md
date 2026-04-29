# Task: R11D-4 PCM Methodology Fix & Re-run

**task_id:** r11d_4_pcm_fix_methodology
**priority:** HIGHEST (addresses 4 blocked critic issues)
**target output:** `outputs/r11d_4_pcm_fix_report.md`
**gpu_hours:** ~15
**owner:** ds_flash (coder) → codex (reviewer) → gemini (critic)

---

## Background

R11D-4 PCM training completed (100 epochs, 87.73% best, 87.49±0.07% fresh eval) but was blocked by Gemini critic for 4 methodological issues. This task fixes all 4 and re-runs training + evaluation.

**Issue 1 — Fresh eval config overwritten:**
`eval_aihwkit_fresh.py` loads checkpoint with `torch.load(..., weights_only=False)`, which restores the saved RPU config. The saved config has `modifier_enable_during_test=False`, overriding the test-time noise injection. Result: fresh eval measures forward IO noise, not cross-instance D2D robustness.

**Issue 2 — PCM write non-linearity never triggered:**
Standard `optim.AdamW` + `InferenceRPUConfig` never calls `AnalogOptimizerMixin.post_update_step()`. PCM pulse-update physics (the core non-linearity) is never activated during training. The experiment is forward-only HWA, not true PCM-aware training.

**Issue 3 — Missing drift axis:**
No `drift_analog_weights()` eval. PCM devices drift over time; this is a core deployment stress axis.

**Issue 4 — Documentation conflict:**
Report references stale 87.34% instead of locked 87.28% (R10E canonical).

---

## Goal

Fix all 4 issues, re-train Tiny-ViT-5M on CIFAR-10 with true PCM-aware training, and run complete eval (fresh + drift).

---

## Fix 1: eval_aihwkit_fresh.py — Preserve test-time modifier config

**File to modify:** `paper2_aihwkit_baseline/eval_aihwkit_fresh.py`

Current problematic code (approximate location):
```python
ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
# ckpt['rpu_config_spec'] has modifier_enable_during_test=False
```

**Required fix:** After loading checkpoint, explicitly re-enable test-time modifier:
```python
# After loading checkpoint and building model
cfg = InferenceRPUConfig()
cfg.forward.inp_res = ckpt['args']['inp_res']
cfg.forward.out_res = ckpt['args']['out_res']
cfg.modifier.type = WeightModifierType.ADD_NORMAL
cfg.modifier.std_dev = ckpt['args']['modifier_std_dev']
cfg.modifier.enable_during_test = True  # FORCE enable for fresh eval
# Rebuild model with corrected config
```

**OR** simpler: save `eval_rpu_config` alongside checkpoint and load that for eval.

**Verification:** Run eval on R10E baseline (`checkpoints/best.pt`) with fixed script. Should get ~87.28% (matches locked R10E canonical), not ~87.73%.

---

## Fix 2: Training script — Use AIHWKit AnalogOptimizerMixin

**File to modify:** `paper2_aihwkit_baseline/r11d4_train_pcm.py`

Current code:
```python
optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.wd)
```

**Required fix:** Use AIHWKit's analog-aware optimizer to trigger `post_update_step()`:
```python
from aihwkit.optim import AnalogSGD  # or AnalogAdamW if available

# Option A: AnalogSGD (guaranteed available)
optimizer = AnalogSGD(model.parameters(), lr=args.lr, weight_decay=args.wd)

# Option B: If AnalogAdamW exists in aihwkit 1.1.0, use it
# optimizer = AnalogAdamW(model.parameters(), lr=args.lr, weight_decay=args.wd)
```

**Important:** `AnalogSGD` is the safe choice (guaranteed in aihwkit 1.1.0). If `AnalogAdamW` is not available, use `AnalogSGD` and document the change from AdamW.

**Why this matters:** `AnalogSGD` calls `post_update_step()` on `AnalogLinear` layers, which applies PCM pulse-update physics (non-linear conductance changes, bounded conductance states, device-to-device variation).

**Fallback:** If `AnalogSGD` import fails, the fix is impossible — report failure and fall back to documenting the limitation.

---

## Fix 3: Add drift eval

**New file:** `paper2_aihwkit_baseline/eval_aihwkit_drift.py`

After fresh eval, run drift eval:
```python
# Load best checkpoint
model.load_state_dict(ckpt['model_state_dict'])

# Apply drift
for module in model.modules():
    if hasattr(module, 'drift_analog_weights'):
        module.drift_analog_weights()  # or module.drift_analog_weights(t_inference=3600)

# Evaluate at multiple drift times: 0s (baseline), 3600s (1h), 86400s (24h)
```

**Output:** `checkpoints/r11d_4_pcm/drift_eval.json` with accuracy at t=0, 3600, 86400 seconds.

**Note:** `drift_analog_weights()` API may vary by aihwkit version. Check actual signature. Common forms:
- `module.drift_analog_weights()` — drift by default time
- `module.drift_analog_weights(t_inference_seconds=3600)` — explicit time
- `module.drift_analog_weights(t_inference=3600)` — another variant

Document which form was used.

---

## Fix 4: Documentation — Use locked numbers

**File:** `outputs/r11d_4_pcm_fix_report.md`

Use locked canonical values:
- R10E baseline: **87.28%** (not 87.34%)
- R11D-2 (σ=0.20): **87.52%** (not 87.60%)
- R11D-4 PCM: use fresh eval from this re-run

---

## Protocol

### Environment
```bash
source /home/qiaosir/miniconda3/etc/profile.d/conda.sh
conda activate aihwkit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
```

### Training config
- Model: Tiny-ViT-5M from timm
- Dataset: CIFAR-10
- Optimizer: **AnalogSGD** (lr=5e-4, weight_decay=0.05) — or AnalogAdamW if available
- Scheduler: CosineAnnealingLR, T_max=100, eta_min=1e-6
- Epochs: 100
- Batch: 64
- Seed: 42
- Forward precision: 8-bit (`inp_res=out_res=1/256`)
- PCM device: PCMPresetUnitCell
- Modifier: ADD_NORMAL, σ=0.10, enable_during_test=False (training)

### Outputs
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/best.pt`
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/last.pt`
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/training_history.json`
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/fresh_eval.json` (fixed eval)
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/drift_eval.json` (new)
- Log: `paper2_aihwkit_baseline/logs/r11d_4_pcm_fix_*.log`

---

## Decision rule (for reviewer/critic phase)

**Approve** if:
1. Training uses `AnalogSGD` or `AnalogAdamW` (not standard AdamW)
2. Fresh eval script explicitly sets `modifier_enable_during_test=True` after loading checkpoint
3. Drift eval produces results for at least t=0 and t=3600s
4. Report uses locked canonical numbers (87.28% for R10E)
5. Provenance fields complete

**Reject** if:
1. Still using standard `optim.AdamW` (Fix 2 not applied)
2. Fresh eval config still overwritten (Fix 1 not applied)
3. No drift eval (Fix 3 not applied)
4. Documentation uses stale numbers (Fix 4 not applied)

---

## Specific output expected

Pipeline should produce in `outputs/r11d_4_pcm_fix_report.md`:
1. **Config summary** — optimizer type, PCM preset, exact RPU config
2. **Training curve** — best accuracy, convergence, comparison to first R11D-4 run
3. **Fresh eval** (fixed) — mean ± std, per-instance, proof that modifier was enabled
4. **Drift eval** — accuracy at t=0, 3600s, (optional 86400s)
5. **Comparison table** — R10E vs R11D-4(first) vs R11D-4(fixed)
6. **Protocol footnote** — for manuscript if approved

---

## Files the pipeline should read
- `paper2_aihwkit_baseline/eval_aihwkit_fresh.py` — to fix
- `paper2_aihwkit_baseline/r11d4_train_pcm.py` — to modify for AnalogSGD
- `paper2_aihwkit_baseline/checkpoints/best.pt` — R10E baseline for verification
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/best.pt` — first R11D-4 checkpoint

---

## Constraints
- **Must use analog-aware optimizer** — standard AdamW is not acceptable
- **Must fix eval config overwrite** — fresh eval must measure true D2D
- **Must add drift eval** — new file, new metric
- **Match R10E recipe** except optimizer and eval fixes
- **Single seed** (42)
- **Report negative results** — if AnalogSGD collapses accuracy vs AdamW, that's a finding

---

## Fallbacks
- If `AnalogAdamW` unavailable → use `AnalogSGD` and document
- If `AnalogSGD` unavailable → report failure, task aborts
- If drift API signature unknown → try common forms, document which worked
- If OOM with AnalogSGD → reduce batch to 32

---

## Done definition
- Training completes with analog-aware optimizer
- Fixed fresh eval JSON exists with correct modifier config
- Drift eval JSON exists
- Report in `outputs/r11d_4_pcm_fix_report.md`
- All 4 critic issues addressed with evidence
