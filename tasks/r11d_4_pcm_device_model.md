# Task: R11D-4 AIHWKit PCM Device Model

**task_id:** r11d_4_pcm
**priority:** HIGHEST (orthogonal stress axis; unblocked by arbitration)
**target output:** `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/`
**gpu_hours:** ~15
**owner:** ds_flash (coder) → codex (reviewer) → gemini (critic)

---

## Background

R11D-1/2/3 used `InferenceRPUConfig` with `device=IdealDevice()` and `WeightModifierType.ADD_NORMAL`. This is an ideal-device abstraction with Gaussian noise injection.

R11D-4 tests a **realistic device model**: AIHWKit's built-in PCM preset, which models non-linear conductance update via realistic pulse-response physics. This is an orthogonal stress axis to ADD_NORMAL noise magnitude and forward-path discretization.

**Arbitration note:** Decision E locked — R11D-4 is unblocked and should launch now. PCM uses its own device config (`PCMPresetUnitCell` / `PCMPresetDevice`), distinct from `inp_res/out_res` semantics.

---

## Goal

Train Tiny-ViT-5M on CIFAR-10 using AIHWKit with PCM device model, then run fresh-eval (10 instances × 5 MC).

Compare to:
- R10E baseline: 87.34 ± 0.14% (IdealDevice, 8-bit, σ=0.10)
- R11D-2: 87.52 ± 0.05% (IdealDevice, 8-bit, σ=0.20)

**Key question:** Does PCM non-linearity collapse AIHWKit where ADD_NORMAL didn't?

---

## Protocol

### Environment
```bash
source /home/qiaosir/miniconda3/etc/profile.d/conda.sh
conda activate aihwkit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
```

### Base config (match R10E except device model)
- Model: Tiny-ViT-5M from timm
- Dataset: CIFAR-10
- Optimizer: AdamW, lr=5e-4, cosine schedule, warmup=5
- Epochs: 100
- Batch: 64
- Seed: 42
- Forward precision: 8-bit (`inp_res=out_res=1/256`) — match R10E to isolate device-model effect

### PCM device config

Create a new training script `r11d4_train_pcm.py` (copy from `train_aihwkit_baseline.py`) with modified `make_rpu_config()`:

```python
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.presets import PCMPresetUnitCell  # or PCMPresetDevice
from aihwkit.simulator.parameters.inference import WeightModifierParameter, WeightModifierType

def make_rpu_config():
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = 1.0 / 256
    cfg.forward.out_res = 1.0 / 256
    # Replace IdealDevice with PCM preset
    # AIHWKit PCM preset provides realistic non-linear pulse update
    # Try: PCMPresetUnitCell, or PCMPresetDevice from aihwkit.simulator.presets
    # If unavailable, try SoftBoundsDevice or LinearStepDevice as fallback
    cfg.device = PCMPresetUnitCell()  # or equivalent
    # Keep modifier for training noise if needed, or rely on PCM intrinsic noise
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = 0.10  # match R10E
    cfg.modifier.enable_during_test = False
    return cfg
```

**Important:** If `PCMPresetUnitCell` import fails, try:
- `from aihwkit.simulator.presets.devices import PCMPresetDevice`
- `from aihwkit.simulator.presets import PCMPresetDevice`
- Fallback: `from aihwkit.simulator.presets import SoftBoundsDevice` or `LinearStepDevice`

Document which preset was actually used in the training_history.json.

### Outputs
- Checkpoint: `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/best.pt`
- Training history: `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/training_history.json`
- Fresh eval: `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/fresh_eval.json`
- Log: `paper2_aihwkit_baseline/logs/r11d_4_pcm_<timestamp>.log`

### Fresh eval
Use existing `eval_aihwkit_fresh.py` (10 instances × 5 MC, seeds 1000-1009).

---

## Decision rule (for reviewer/critic phase)

**Approve** if:
- Training completes 100 epochs (or early stops with reason)
- Fresh eval JSON is generated with 10-instance statistics
- Provenance fields (commit_hash, code_sha256, GPU name) are present
- PCM preset choice is documented

**Reject** if:
- Training crashes due to PCM config (try fallback device; if all fail, report negative result)
- OOM (reduce batch to 32 and retry)
- Fresh eval missing or corrupted

---

## Specific output expected

The pipeline should produce in `outputs/r11d_4_pcm_report.md`:
1. **Config summary** — which PCM preset was used, exact RPU config string
2. **Training curve** — best accuracy, final accuracy, convergence speed vs R10E
3. **Fresh eval** — mean ± std, per-instance breakdown
4. **Comparison table** — R10E vs R11D-4 (same 8-bit forward, different device model)
5. **Protocol footnote text** — for later manuscript integration:
   > "R11D-4 uses AIHWKit's built-in PCM preset, which models non-linear conductance update via realistic pulse-response physics. This is distinct from the R11D-1/2/3 ADD_NORMAL abstraction."

---

## Files the pipeline should read
- `paper2_aihwkit_baseline/train_aihwkit_baseline.py` — base script to copy
- `paper2_aihwkit_baseline/eval_aihwkit_fresh.py` — fresh eval
- `paper2_aihwkit_baseline/checkpoints/best.pt` — R10E baseline for comparison
- `paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/fresh_eval.json` — R11D-2 result

---

## Constraints
- **Match R10E recipe exactly** except device model
- **8-bit forward precision** (isolate device-model variable)
- **Single seed** (42)
- **Report negative results** — if PCM doesn't collapse AIHWKit, that's a finding
- **Fallback devices allowed** — if PCM preset unavailable, use SoftBoundsDevice or LinearStepDevice and document

---

## Done definition
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/best.pt` exists
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/fresh_eval.json` exists with mean/std
- `paper2_aihwkit_baseline/checkpoints/r11d_4_pcm/training_history.json` exists
- Report in `outputs/r11d_4_pcm_report.md`
- Log in `paper2_aihwkit_baseline/logs/`
