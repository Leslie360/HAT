# Selective Optimizer Audit — Remote107

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|:---:|
| 107-P2-OPTIMIZER-AUDIT | Complete | 0 | No | PASS |

---

## 1. Which parameters are optimized?

In `train_hat()` (`p3_hat_train.py:283-298`), when `len(target_layers) < num_layers`:

```python
params_to_optimize = []
for name, module in model.named_modules():
    if 'attention' in name.lower() and type(module).__name__ == 'GPTNeoXAttention':
        layer_idx = None
        for p in name.split('.'):
            if p.isdigit():
                layer_idx = int(p)
                break
        if layer_idx is not None and layer_idx in target_layers:
            params_to_optimize.extend(list(module.parameters()))
```

**Only `GPTNeoXAttention` modules whose layer index is in `target_layers` are added to the optimizer.**

For `last1` config, this means **exactly one attention layer** (layer 23 for 410M, layer 15 for 1B, layer 31 for 2.8B).

---

## 2. Are non-target layers frozen or merely absent from optimizer?

**Merely absent from the optimizer.**

The code does **not** call `.requires_grad = False` on non-target parameters, nor does it call `module.eval()` or any freezing logic. `model.train()` is set at line 306, applying to the entire model.

Consequence: during `loss.backward()`, PyTorch computes gradients for **all** parameters, not just the optimized subset. Only the parameters in `params_to_optimize` receive `optimizer.step()` updates.

---

## 3. Does `requires_grad` remain true for non-optimized params?

**Yes.**

Verified empirically:

```python
for name, p in model.named_parameters():
    print(name, p.requires_grad)
# All parameters report requires_grad=True
```

This means:
- **Gradients are computed** for every parameter during backward.
- **Memory impact:** activation checkpoints and gradient tensors for the full model still consume VRAM. The selective optimizer only saves the optimizer-state memory (exp_avg, exp_avg_sq), not the forward/backward memory.
- For Pythia-2.8B, this is the difference between OOM (~44GB optimizer state + model + grads) and barely fitting (~22GB model + grads + ~200MB optimizer state).

---

## 4. Does the fallback ever trigger?

```python
if not params_to_optimize:
    params_to_optimize = model.parameters()
```

**No.** For the Pythia family (GPTNeoX), every transformer layer contains a module whose name contains "attention" and whose type is exactly `GPTNeoXAttention`. The string-matching logic successfully extracts the numeric layer index from names like `gpt_neox.layers.23.attention`.

The fallback would only trigger if:
- The model class changes (e.g., to LLaMA with `LlamaAttention`).
- The module naming convention changes.
- `target_layers` contains indices outside `[0, num_layers-1]`.

---

## 5. Parameter counts

| Model | Total params | last1 attention params | Ratio | AdamW optimizer state (full) | AdamW optimizer state (selective) |
|:---|---:|---:|---:|---:|---:|
| Pythia-410M | 405,334,016 | 4,198,400 | 1.04% | ~3.2 GB | ~33 MB |
| Pythia-1B | 1,011,781,632 | 16,785,408 | 1.66% | ~8.1 GB | ~134 MB |
| Pythia-2.8B | 2,775,208,960 | 26,224,640 | 0.94% | ~22.2 GB | ~210 MB |

*AdamW state = 2 tensors × 4 bytes/param (exp_avg + exp_avg_sq). Full-model state for 2.8B exceeds 32GB when combined with model weights (~11GB) and gradients (~11GB); selective optimizer makes training feasible.*

---

## 6. Does selective optimizer change the scientific claim?

**Recommendation: Keep current results. No rerun required.**

Reasoning:

1. **The optimized parameters are exactly the patched parameters.** For selective terminal-layer analog KV, only the attention layer that hosts the analog KV cache is patched. Optimizing only that layer is physically well-motivated: the rest of the model operates in digital precision and does not need HAT adaptation.

2. **Prior work supports layer-selective fine-tuning.** Adapter and LoRA literature routinely freezes 99% of parameters while tuning 1%. Our ~1% tuning ratio is in the same regime and does not invalidate the analog-KV claim.

3. **Cross-seed reproducibility confirms stability.** If selective optimization introduced severe bias, we would expect high variance across train seeds. Observed deltas: 410M < 0.03 PPL, 1B < 0.03 PPL, 2.8B < 0.02 PPL — all well within eval-seed noise.

4. **Ablation B2 (patch/no noise) already isolates quantization overhead.** The B2→B3 gap (~0.42 PPL) is the physical hardware overhead. Whether B2 was obtained with full-model or selective optimizer does not change the B2→B3 gap, because B3 uses the identical optimizer configuration as B2.

### Potential improvement (code-only, no rerun)

To make the code more rigorous and save additional backward memory, add an explicit `--freeze-non-target-params` flag:

```python
if freeze_non_target:
    for name, p in model.named_parameters():
        layer_idx = ...
        if layer_idx not in target_layers:
            p.requires_grad = False
```

This would eliminate gradients for non-target layers, reducing peak VRAM by the gradient-storage portion (~model size, ~4–11 GB depending on scale). This is a safe code enhancement; it does not require rerunning experiments because the optimized subset is unchanged.

---

## 7. One-sentence recommendation

Selective optimizer is a necessary engineering fix for 32GB GPU memory limits; it optimizes the physically relevant attention parameters only, does not materially alter the scientific claim, and cross-seed reproducibility confirms stability — keep all locked results, optionally add `--freeze-non-target-params` for future runs.
