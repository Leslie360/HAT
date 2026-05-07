# P3 Pythia-6.9B Feasibility Probe — Remote107

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|:---:|
| 107-P3-6P9B-FEASIBILITY | Complete (analytical) | 0 | N/A | **BLOCKED — hardware limit** |

---

## 1. Model Specification

| Spec | Value |
|:---|:---|
| Model | `EleutherAI/pythia-6.9b-deduped` |
| Layers | 32 |
| Hidden dim | 4096 |
| Attention heads | 32 |
| Head dim | 128 |
| Total parameters | ~6.9 B |
| Last1 attention params | ~67.1 M (4 × hidden_size² = 4 × 4096²) |

---

## 2. Memory Budget Analysis (Current Script)

Current `p3_hat_train.py` uses `torch.float32` (line 416):

```python
model = AutoModelForCausalLM.from_pretrained(args.model_name, torch_dtype=torch.float32)
```

### 2.1 Selective optimizer only (current code, no other changes)

| Component | Size | Notes |
|:---|---:|:---|
| Model weights (fp32) | ~27.6 GB | 6.9B × 4 bytes |
| Gradients (all params, fp32) | ~27.6 GB | `requires_grad=True` for all; selective optimizer does not freeze |
| Activations (bs=1, seq=512) | ~2–4 GB | Forward activations for one layer at a time + cache |
| Optimizer state (selective, last1) | ~0.4 GB | AdamW exp_avg + exp_avg_sq for 52M params |
| **Total estimated** | **~58 GB** | **Far exceeds 32 GB GPU VRAM** |

### 2.2 Even with full `requires_grad=False` freezing

| Component | Size |
|:---|---:|
| Model weights | ~27.6 GB |
| Gradients (last1 only) | ~0.2 GB |
| Activations | ~2–4 GB |
| Optimizer state | ~0.4 GB |
| **Total** | **~30–32 GB** |

This is at the absolute edge of 32 GB. Any CUDA fragmentation, dataset tensor, or intermediate buffer pushes it over.

---

## 3. What Would Be Required to Fit

To safely run 6.9B on a 32GB GPU, at least one of the following is required:

1. **FP16 / BF16 weights** — halves model weight memory to ~13.8 GB. Current script has no AMP support.
2. **Gradient checkpointing** — trades compute for memory. Not currently implemented.
3. **CPU offloading** (e.g., DeepSpeed ZeRO-Offload) — moves optimizer states and/or parameters to host RAM. Not currently implemented.
4. **Tensor-parallel or pipeline-parallel multi-GPU training** — splits model across GPUs. Current script is single-GPU only.
5. **Smaller batch/sequence** — already at bs=1, seq=512; further reduction yields marginal savings.

---

## 4. Phase A Decision

**Skipped actual smoke test.**

Reason: The analytical budget above makes it unnecessary to download ~14GB of weights to confirm OOM. Even under the most optimistic selective-optimizer + frozen-gradients scenario, the memory budget is ~30–32 GB with zero headroom for fragmentation or dataset tensors.

If we had:
- FP16 support + gradient checkpointing, **or**
- 48GB+ GPUs (A40, A6000), **or**
- 2× 32GB GPUs with model parallelism,

…then 6.9B would be feasible. On the current 8× 32GB setup with the current fp32 single-GPU script, it is **not safely feasible**.

---

## 5. Recommendation

| Option | Effort | Risk | Recommendation |
|:---|:---:|:---:|:---|
| Add FP16 + AMP to training script | 2–4 hours | Medium (numerical stability) | **Do now if 6.9B is a manuscript requirement** |
| Add DeepSpeed ZeRO-Offload | 4–8 hours | Medium (new dependency) | Do if FP16 alone insufficient |
| Upgrade to 48GB GPUs | $$$ | None | Not available on Remote107 |
| Skip 6.9B, claim 410M→1B→2.8B trend | 0 hours | Low | **Acceptable** — trend is already monotonic and strong |

**One-sentence recommendation for Codex:** 6.9B is blocked by 32GB VRAM under fp32; adding FP16/AMP support would unlock it, but the existing 410M→1B→2.8B monotonic scale trend is already publication-ready without 6.9B.
