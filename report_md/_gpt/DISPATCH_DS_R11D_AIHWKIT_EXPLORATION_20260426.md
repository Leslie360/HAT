# DISPATCH DS R11D — AIHWKit Stress-Regime Exploration
**Date:** 2026-04-26 16:50 CST
**Issued by:** Claude
**Assignee:** DeepSeek
**Authority:** CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN
**Priority:** HIGHEST (Path C — search for regime where Ensemble HAT > AIHWKit)
**Time budget:** ~5-7 days, 50-60 GPU-h

---

## 0. Mission

R10E showed AIHWKit baseline (87.34%) marginally beats Ensemble HAT (86.16%) at canonical settings. **Find a stress regime where AIHWKit collapses but Ensemble HAT survives.** This is method-superiority exploration.

5 sub-experiments + 1 conditional revisit. Each ~12-15 GPU-h.

**Working dir**: `paper2_aihwkit_baseline/` (already set up). Use `aihwkit` conda env + `LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib`.

---

## 1. Common protocol (all 5 sub-tracks)

### 1.1 Environment
```bash
source /home/qiaosir/miniconda3/etc/profile.d/conda.sh
conda activate aihwkit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
```

### 1.2 Base config (modify per sub-track)
- Model: Tiny-ViT-5M from timm
- Dataset: CIFAR-10 (matches R10E)
- Optimizer: AdamW, lr=5e-4, cosine schedule, warmup=5
- Epochs: 100
- Batch: 64
- Seed: 42 (single seed; if R10E's surprise robustness was seed-luck, second seed picks it up)

### 1.3 Outputs per experiment
- Checkpoint: `paper2_aihwkit_baseline/checkpoints/r11d_<id>/best.pt`
- Training history: `r11d_<id>/training_history.json`
- Fresh-eval (10 instances × 5 MC): `r11d_<id>/fresh_eval.json`
- Log: `paper2_aihwkit_baseline/logs/r11d_<id>_<ts>.log`
- Provenance JSON fields: commit_hash, code_sha256, cuda_device_name, pytorch_version, exp_cfg

### 1.4 Eval consistency
Use existing `eval_aihwkit_fresh.py` (already fixed for weights_only). Same 10 fresh seeds (1000-1009).

---

## 2. R11D-1 — AIHWKit at 4-bit precision

### Modify `train_aihwkit_baseline.py:make_rpu_config()`:
```python
def make_rpu_config():
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = 1.0 / 16     # 4-bit (was 1/256 = 8-bit)
    cfg.forward.out_res = 1.0 / 16     # 4-bit
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = 0.10
    cfg.modifier.enable_during_test = False
    return cfg
```

### Run
- ID: `r11d_1_4bit`
- Why: matches paper-1 4-bit precision; tests if AIHWKit survives the same precision floor that paper-1 uses

### Hypothesis
AIHWKit may degrade significantly at 4-bit (paper-1 iso-accuracy shows ~10pp degradation at 4-bit ADC for Tiny-ViT). If AIHWKit drops to ~75-78% while Ensemble HAT survives at ~85% — method-superiority story.

---

## 3. R11D-2 — AIHWKit at σ=0.20 (high noise)

### Modify config:
```python
cfg.modifier.std_dev = 0.20    # was 0.10
```

### Run
- ID: `r11d_2_sigma020`
- Eval: same fresh-eval but with σ_D2D=0.20 in eval (modify `eval_aihwkit_fresh.py:evaluate_fresh()` to inject 0.20 noise)

### Hypothesis
AIHWKit per-batch noise approaches saturation; Wager-style implicit regularization needs σ small. If AIHWKit drops below 75% while Ensemble HAT (paper-1 §5.6) holds ~80% — method-superiority.

---

## 4. R11D-3 — AIHWKit at σ=0.30 (extreme; CONDITIONAL on R11D-2)

### Trigger
Only fire if R11D-2 still > 80%.

### Modify config:
```python
cfg.modifier.std_dev = 0.30
```

### Run
- ID: `r11d_3_sigma030`

---

## 5. R11D-4 — AIHWKit with PCM device model

### Modify `make_rpu_config()`:
```python
from aihwkit.simulator.presets import PCMPresetUnitCell  # or similar
# Replace ADD_NORMAL with realistic PCM device:
from aihwkit.simulator.presets.devices import PCMPresetDevice

cfg = InferenceRPUConfig()
cfg.forward.inp_res = 1.0 / 256
cfg.forward.out_res = 1.0 / 256
# Use PCM model with realistic asymmetric pulse update + drift
# Specific config TBD — pick one of: SoftBoundsDevice, PCMPresetDevice, or LinearStepDevice
# Reference: aihwkit/simulator/presets/devices.py
```

### Run
- ID: `r11d_4_pcm`

### Why
PCM models have realistic non-linear pulse-update (closer to our NL=2.0 abstraction). If AIHWKit collapses on PCM where ADD_NORMAL didn't — proves our framework's NL=2.0 stress test catches what AIHWKit's default doesn't.

### Fallback
If PCM device model is too complex to configure correctly: skip R11D-4, focus on R11D-1/2/3 + R11D-6.

---

## 6. R11D-6 — Ensemble HAT at AIHWKit-matched cadence (CONDITIONAL on R11D-5 cadence finding)

### Trigger
After Kimi's R11D-5 cadence comparison reveals AIHWKit's resample frequency. If AIHWKit resamples per-MINIBATCH (not per-batch as our code did), retrain Ensemble HAT with that cadence.

### Modify `analog_layers_ensemble.py`
Adjust the resample hook to fire per-minibatch (every forward pass) instead of per-epoch.

### Run
- ID: `r11d_6_perminibatch`
- Train canonical Ensemble HAT (NL=1.0, 4-bit hybrid, σ=0.10) but with per-minibatch resample
- Fresh-eval 10 instances × 5 MC

### Hypothesis
If our framework + AIHWKit-matched cadence converges to ~87.34% → confirms cadence is the lever, not the architecture.

---

## 7. Reporting cadence

After each sub-track completes, append to AGENT_SYNC_gpt.md:

```markdown
---
DeepSeek (Path C exploration) | YYYY-MM-DD HH:MM CST

### R11D-N <name> COMPLETE
- ID: r11d_<n>_<tag>
- Train best: X.XX%
- Fresh mean ± std: X.XX ± Y.YY%
- Per-instance: [...]
- Hypothesis verdict: <support / contradict>
- Provenance: commit <hash>, GPU <name>

@Claude — <signal next step>
```

---

## 8. Hard constraints

- **Single seed per experiment** (we'll add multi-seed if a regime shows method-superiority)
- **Match R10E recipe exactly** except for the noise/precision/device knob being varied
- **Pause Round-8 W2 P2** GPU work during R11D windows (paper-1 R11D priority)
- **No paper text edits** (Kimi role)
- **Report negative results** honestly — if AIHWKit survives everywhere, that's a finding too

---

## 9. Failure modes

- AIHWKit GPU compile breaks again → revert to Codex's earlier compile state; document
- PCM device config too complex → skip R11D-4
- 4-bit eval crashes → use 5-bit or 6-bit as compromise; document
- Memory OOM with PCM device → reduce batch to 32

Escalate to @Claude if blocker > 4 hours.

---

## 10. Cold-start refs

- `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md` — master plan
- `paper2_aihwkit_baseline/train_aihwkit_baseline.py` — current 8-bit baseline
- `paper2_aihwkit_baseline/eval_aihwkit_fresh.py` — fresh-eval (already fixed)
- `paper2_aihwkit_baseline/checkpoints/best.pt` — R10E baseline (~87.73 train best, 87.34 fresh)
- `report_md/_gpt/CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md` — R10E setup details
- AIHWKit docs: https://aihwkit.readthedocs.io/

**No deadline.** ~5-7 days expected. Report each landing immediately.
