# CLAUDE → CODEX 任务单：R10E AIHWKit Head-to-Head Baseline
**Date:** 2026-04-26 05:20 CST
**Issued by:** Claude (Chief Architect)
**Assignee:** Codex / DeepSeek
**Authority:** DISPATCH_CODEX_R10_EXPERIMENTS_20260425 §4
**Status:** LAUNCHED
**Blocker:** None — GPU idle (1% util, 305 MiB/16 GB, 49°C)
**Time budget:** ~2 days, ~10 GPU-h

---

## 0. Mission
Build and train an AIHWKit analog inference baseline that enables a direct head-to-head comparison against our Standard HAT and Ensemble HAT under matched canonical settings. This closes the last open reviewer concern (D2: AIHWKit baseline absent) and completes Round-10.

---

## 1. Environment Setup (CPU only, no GPU block)

### 1.1 Create isolated conda env
```bash
conda create -n aihwkit python=3.10 -y
conda activate aihwkit
```

### 1.2 Install AIHWKit
```bash
pip install aihwkit
```
- Document exact version: `pip show aihwkit | grep Version`
- If CUDA mismatch / install fails: ESCALATE immediately to AGENT_SYNC; fallback is text-only comparison.

### 1.3 Verify install
```python
python -c "from aihwkit.simulator.configs import InferenceRPUConfig; print('OK')"
```

---

## 2. Build Matching Baseline

### 2.1 Directory
Create `compute_vit/paper2_aihwkit_baseline/` as the workspace.

### 2.2 Architecture
Use **Tiny-ViT-5M** (same as ours). If AIHWKit does not natively support attention layers, implement a Torch+AIHWKit hybrid: analog Linear layers via AIHWKit's `AnalogLinear`, digital path (LayerNorm, Softmax, GELU) stays Torch.

### 2.3 Dataset
CIFAR-10, same preprocessing as ours (32×32, standard normalization).

### 2.4 AIHWKit InferenceRPU Config
Match our canonical non-ideality settings:
| Our Parameter | AIHWKit Equivalent | Value |
|:---|:---|:---|
| σ_D2D = 10% | `noise_model` + `dw_min_std` or `pcm_gamma` | Tune to ~10% weight variation |
| σ_C2C = 5% | `w_noise` (read noise) | Tune to ~5% |
| 4-bit weight | `fwd/bwd/out_res = 2**4 = 16` or `weight_bit = 4` | 4-bit |
| ADC 8-bit | `adc_res = 8` | 8-bit |
| NL = 1.0 (canonical) | Use default linear/weak-nonlinear model | Linear or minimal nonlinearity |

Use AIHWKit's built-in `PCMLikeNoiseModel` or `CustomDriftNoiseModel` to approximate our D2D/C2C noise. Document the exact config dict in JSON provenance.

### 2.5 Training Recipe (match ours)
- Optimizer: AdamW, lr=5e-4, weight_decay=0.05
- Scheduler: cosine, 100 epochs, warmup=5
- Batch: 64
- AMP: enabled (AIHWKit supports mixed precision)
- Seed: 123 (matches our canonical)

### 2.6 Noise Training Mode
Train with AIHWKit's standard "inference noise forward" (analogous to our Standard HAT — one fixed noise realization per forward during training). This is the fairest comparison: their default noisy training vs our Standard HAT.

If AIHWKit has a "robust training" or "multi-tile / multi-instance" mode, document it but do NOT use it as the primary comparison — we want their default vs our Ensemble HAT.

---

## 3. Fresh-Instance Eval Protocol

### 3.1 After training completes
Load the trained AIHWKit checkpoint and run **10 inference repetitions** with freshly sampled D2D noise realizations (AIHWKit's `inference_repeats` or manual loop).

### 3.2 Metrics
- Best training accuracy
- Mean ± std across 10 fresh noise instances
- Per-class prediction distribution (optional but nice — same format as R10B)

---

## 4. Comparison & Reporting

### 4.1 Comparison table
| Method | Train Best | Fresh Mean ± Std |
|:---|:---|:---|
| Standard HAT (ours) | 91.94% | 10.00 ± 0.00% |
| Ensemble HAT (ours, 3-seed) | — | 86.16 ± 0.19% |
| AIHWKit baseline (default noisy train) | [fill] | [fill] |

### 4.2 Honest framing rules
- If AIHWKit fresh ≈ 10% (collapses): STRONG claim — "Ensemble HAT is the first analog training method to demonstrate cross-instance generalization on this task."
- If AIHWKit fresh ≈ 80-90%: Neutral claim — "Ensemble HAT matches established analog HAT libraries under matched settings; the distinctive contribution is the per-epoch resampling discipline and the severe-NL recovery evidence."
- If AIHWKit fresh > 90%: ESCALATE — may require re-assessing novelty claims.

---

## 5. Deliverables

1. `paper2_aihwkit_baseline/` directory with:
   - `train_aihwkit_baseline.py`
   - `eval_aihwkit_fresh.py`
   - `aihwkit_config.yaml` (or .py) documenting exact RPUConfig
   - `requirements.txt` (aihwkit version pinned)

2. `checkpoints/aihwkit_baseline_best.pt` (or AIHWKit's native format)

3. `report_md/_gpt/json_gpt/r10e_aihwkit_fresh_eval.json` — provenance + results

4. `report_md/_gpt/CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md`:
   - AIHWKit version + exact config
   - Training curve summary
   - Fresh-eval results
   - Comparison table
   - Paper-safe paragraph for §5 or Discussion
   - Honest interpretation per §4.2

---

## 6. Escalation Triggers

| Trigger | Action |
|:---|:---|
| AIHWKit install fails (CUDA/env) | ESCALATE — fallback to text-only comparison |
| AIHWKit fresh > 90% | ESCALATE — novelty claim may need reassessment |
| Training diverges / NaN | DEBUG once, then escalate if persists |
| GPU OOM | Reduce batch or use gradient accumulation; document |

---

## 7. Coordination

- This is the **sole remaining R10 track**. All upstream dependencies (R10A/B/D) are complete and integrated.
- No conflict with W2 — GPU is fully available.
- Broadcast progress in AGENT_SYNC after env setup completes and after training completes.
- Do NOT block on this task — if AIHWKit proves intractable after 4 hours of setup, escalate rather than sink cost.

---

## 8. Acceptance Criteria

- [ ] AIHWKit installed in isolated env
- [ ] Training completes (100 epochs or early-stop if >95% train)
- [ ] Fresh-eval (10 instances) completed
- [ ] Comparison table populated
- [ ] Report written with paper-safe paragraph
- [ ] All code + JSON provenance committed to `paper2_aihwkit_baseline/`

**End of task.**
