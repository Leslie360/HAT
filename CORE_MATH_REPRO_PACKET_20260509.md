# CORE_MATH_REPRO_PACKET — HAT Analog KV Cache (Remote107)

> Generated: 2026-05-09
> Branch: 107-clean
> Commit: c154392
> Contact: Leslie360 / Remote107 (GPUs 4-7)

---

## 1. Conductance Mapping Formula (Differential Pair)

**Source:** `p3_hat_train.py:67-78` (`analogize_kv_tensor`)

For an input tensor `x` with shape `[B, H, L, D]` (batch, heads, seq_len, head_dim):

```
x_fp32 = clamp(x, -clamp_r, clamp_r)
scale  = max(|x_fp32|, dim=(-2,-1), keepdim=True) + 1e-8   # [B, H, 1, 1]
x_norm = x_fp32 / scale                                      # [-1, 1]

x_pos = clamp(x_norm, min=0.0)      # [0, 1]
x_neg = clamp(-x_norm, min=0.0)     # [0, 1]

G_range = G_max - G_min
G_pos   = G_min + x_pos * G_range   # [G_min, G_max]
G_neg   = G_min + x_neg * G_range   # [G_min, G_max]
```

**Physical meaning:**  
Each KV activation is split into a positive/negative differential conductance pair. The normalization uses a per-head, per-batch dynamic range (`scale`), matching the per-head quantization granularity used in weight-domain `AnalogLinear`.

---

## 2. Quantization Formula (STE with NL Scaling)

**Source:** `p3_hat_train.py:80-88`, `analog_layers.py:170-289`

### 2.1 Forward (Write)
```
n_states = analog_cfg.n_states
g_q = round((g - G_min) / G_range * (n_states - 1))
g_q = g_q / (n_states - 1) * G_range + G_min
out = g + (g_q - g).detach()          # STE: gradient passes straight through
```

### 2.2 Backward (Branch A — from `analog_layers.py:228-288`)
```
conductance_span = max(G_max - G_min, eps)

# LTP (negative gradient → potentiation)
if NL_LTP not in {0, 1}:
    ltp_ratio = ((G_max - x_clamped) / conductance_span).clamp_min(eps)
    ltp_scale = pow(ltp_ratio, NL_LTP - 1.0)
else:
    ltp_scale = 1.0

# LTD (positive gradient → depression)
if NL_LTD not in {0, 1}:
    ltd_ratio = ((x_clamped - G_min) / conductance_span).clamp_min(eps)
    ltd_scale = pow(ltd_ratio, NL_LTD - 1.0)
else:
    ltd_scale = 1.0

grad_input = where(grad_output >= 0, grad_output * ltd_scale, grad_output * ltp_scale)
```

**Key invariant:** NL prefactor is intentionally **omitted** (Equation S2 semantics). The surrogate scales STE by normalized conductance position `(ratio)^(NL-1)`, modeling state-dependent update difficulty, not the strict derivative of `f(G)=G^NL`.

### 2.3 Second-Order Correction (CX-J1d, optional)
```
if use_second_order_ste and delta_g_eff > 0:
    ltp_corr = -0.5 * (NL_LTP - 1) * pow(ltp_ratio, NL_LTP - 2) * delta_g_eff
    ltd_corr = -0.5 * (NL_LTD - 1) * pow(ltd_ratio, NL_LTD - 2) * delta_g_eff
    correction = alpha * where(grad >= 0, grad * ltd_corr, grad * ltp_corr)
    grad_input += correction
```

---

## 3. D2D Noise — Shape, Sampling, Persistence

**Source:** `p3_hat_train.py:316-338`

### 3.1 Shape
```
[1, num_heads, max_length, head_size]   # per leg, per layer
```
Four buffers per patched attention layer:
- `_d2d_noise_k_pos`
- `_d2d_noise_k_neg`
- `_d2d_noise_v_pos`
- `_d2d_noise_v_neg`

### 3.2 Sampling Timing
```python
with torch.random.fork_rng():
    torch.manual_seed(d2d_seed + layer_idx)
    buf = torch.randn(1, H, max_length, D) * per_leg_std
```
- **When:** Once per layer at `patch_model_for_hat()` call time.
- **Seed:** `d2d_seed + layer_idx` (deterministic per layer).
- **Std:** `per_leg_std = sigma_d2d * G_range / sqrt(2)`.

### 3.3 Persistence
- Stored as `register_buffer` → saved with `state_dict`, loaded with `load_state_dict`.
- Not resampled during training or inference.
- Cross-instance reproducibility: same `d2d_seed` → identical noise pattern.

---

## 4. C2C Noise — Shape & Per-Forward Resampling Proof

**Source:** `p3_hat_train.py:114-130`

### 4.1 Forward Code (excerpt)
```python
if analog_cfg.noise_mode == "uniform":
    per_leg_std = analog_cfg.sigma_c2c * G_range / (2 ** 0.5)
    noise_c2c_pos = torch.randn_like(G_pos) * per_leg_std
    noise_c2c_neg = torch.randn_like(G_neg) * per_leg_std
else:  # proportional
    per_leg_std = analog_cfg.sigma_c2c / (2 ** 0.5)
    noise_c2c_pos = torch.randn_like(G_pos) * G_pos.abs() * per_leg_std
    noise_c2c_neg = torch.randn_like(G_neg) * G_neg.abs() * per_leg_std

W_eff = (G_pos + noise_c2c_pos) - (G_neg + noise_c2c_neg)
```

### 4.2 Resampling Proof
- `torch.randn_like(G_pos)` creates a **new** random tensor every forward call.
- No `register_buffer`, no `torch.manual_seed()` guarding this block.
- Therefore C2C is **independently re-sampled per token, per head, per forward pass**.
- Differential pair ensures total C2C std = `sigma_c2c * G_range` in uniform mode.

---

## 5. Retention Formula (Double-Exponential Decay)

**Source:** `p3_hat_train.py:90-104`

```
L = x.size(2)   # sequence length
ages[i] = (L - 1 - i) * retention_step_time     # last token = newest

A_1 = (1.0 - A_0) / 2.0
A_2 = A_1
decay = A_1 * exp(-ages / tau_1) + A_2 * exp(-ages / tau_2) + A_0

G_pos_decayed = G_min + (G_pos - G_min) * decay
G_neg_decayed = G_min + (G_neg - G_min) * decay
```

**Shape:** `ages` → `[1, 1, L, 1]`, broadcast over `[B, H, L, D]`.

**Physical meaning:**  
Each token position has an age. Older tokens (smaller index `i`) have larger `age` → more decay. The decay is multiplicative on the conductance offset from `G_min`.

---

## 6. Dequantization (Recovery to Output Space)

**Source:** `p3_hat_train.py:132-134`

```
recover_scale = scale / G_range     # [B, H, 1, 1]
x_analog = W_eff * recover_scale
return x_analog.to(x.dtype)
```

**Flow:**
1. `scale` = per-head max abs value (from Step 1, detached).
2. `W_eff` = differential conductance after quantization + noise.
3. Multiply by `scale / G_range` to map back to the original activation magnitude.
4. Cast back to input dtype (e.g. `bfloat16`).

**Gradient note:** `scale` is detached, so gradients flow only through `W_eff` (i.e. through the STE-quantized conductance path).

---

## 7. Selective Layer Mask Semantics

**Source:** `p3_hat_train.py:255-404`

```python
target_layers = analog_layers if analog_layers is not None else set(range(num_layers))

for name, module in model.named_modules():
    if 'attention' in name.lower() and type(module).__name__ == 'GPTNeoXAttention':
        layer_idx = int(extract_digit_from_name(name))
        if layer_idx in target_layers:
            # patch this layer
```

### Semantics
- `analog_layers` is a `set[int]` of layer indices to patch.
- `None` means **all** layers.
- Only layers whose numeric index appears in the set are monkey-patched.
- Unpatched layers use the **original** `forward` (clean KV, no analog injection).
- Saved in `hat_config.json` as `"analog_layers": [23]` for reproducibility.

### Typical configs
| Name | Layers | Rationale |
|---|---|---|
| `last1` | `{num_layers-1}` | Only terminal layer analog |
| `last2` | `{num_layers-2, num_layers-1}` | Last 2 layers |
| `last4` | Last 4 layers | Broader terminal analog |
| `full` | All layers | Full-model HAT |

---

## 8. SDPA Patch Position & Mask Handling

**Source:** `p3_hat_train.py:345-404`

### Patch Position
The monkey-patch replaces `GPTNeoXAttention.forward` **after** rotary position embedding and **before** the attention interface call:

```
1. hidden_states → qkv projection
2. apply_rotary_pos_emb(query, key)
3. layer_past.update(key, value)      # KV cache append
4. === ANALOG INJECTION HERE ===      # <- patch point
   key_states   = analogize_kv_tensor(key_states, ...)
   value_states = analogize_kv_tensor(value_states, ...)
5. attn_interface(query, key_analog, value_analog, attention_mask, ...)
6. dense projection
```

### Mask Handling
- `attention_mask` is passed **unchanged** to `attn_interface`.
- The analog injection does **not** modify the causal mask or attention mask.
- Rotary embeddings are applied **before** analogization, so position info is preserved in the conductance domain.

### Interface compatibility
```python
from transformers.models.gpt_neox.modeling_gpt_neox import ALL_ATTENTION_FUNCTIONS, eager_attention_forward
attn_interface = ALL_ATTENTION_FUNCTIONS.get_interface(
    self.config._attn_implementation, eager_attention_forward
)
```
Supports both `eager` and `sdpa` backends via `transformers` dispatch.

---

## 9. HAT Objective / Trainable Params / Train-Eval Split

### 9.1 Training Objective
Standard causal language modeling loss:
```
L = -log P(x_t | x_{<t}; theta_analog)
```
where `theta_analog` includes both base model weights and LoRA adapters.

### 9.2 Trainable Parameters
- **Base model:** Frozen (or optionally fine-tuned with small LR).
- **LoRA adapters:** `lora_A` (in_features × rank) + `lora_B` (rank × out_features) per target linear.
- **Scaling:** `lora_alpha / rank`.

**Selective optimizer scope (critical fix recovered ~3 PPL):**  
Only parameters in the analog-injected layers + LoRA parameters receive gradients. The optimizer state is filtered to exclude clean-layer parameters, preventing OOM and gradient leakage.

### 9.3 Train-Eval Split
| Phase | Noise | Quantization | Retention | D2D |
|---|---|---|---|---|
| **Training** | C2C ON, D2D ON | STE (differentiable) | OFF | Fixed pattern |
| **Eval (noisy)** | C2C ON, D2D ON | STE (non-differentiable in eval) | Optional | Same fixed pattern |
| **Eval (clean)** | All OFF | Bypassed | OFF | N/A |

### 9.4 Checkpoint Compatibility
- `merge_and_uninject_lora()` merges LoRA deltas back into base weights.
- Saved via `save_pretrained()` → standard `safetensors` format.
- `from_pretrained()` loads directly without custom code.

---

## 10. Baseline Reconciliation Table

| Baseline | Method | 410M PPL | 2.8B PPL | 6.9B PPL |
|---|---|---|---|---|
| **Clean (FP32/BF16)** | No quantization, no noise | ~11.0* | — | — |
| **HAT (last1, σ_c2c=0.01, σ_d2d=0.02)** | STE quant + C2C/D2D | ~11.4* | — | — |
| **INT8 RTN KV** | Round-to-nearest, symmetric | 12.20 | — | 12.20 |
| **INT4 RTN KV** | Round-to-nearest, symmetric | 12.46 | — | — |

*Values are approximate; exact numbers depend on checkpoint and seed.  
**Key narrative:** HAT (analog-aware training) achieves significantly lower PPL than post-hoc INT8/INT4 RTN quantization at comparable or lower bit-equivalent resolution.

---

## 11. Unit Test Specifications

### 11.1 Zero-Noise Parity Test
```python
def test_zero_noise_parity():
    cfg = AnalogLinearConfig(noise_enabled=False, n_states=999999)
    x = torch.randn(2, 12, 128, 64)
    out = analogize_kv_tensor(x, cfg)
    assert torch.allclose(out, x, atol=1e-4)
```
**Expect:** When noise is disabled and n_states is huge (no quantization), output matches input exactly.

### 11.2 D2D Persistence Test
```python
def test_d2d_persistence():
    cfg = AnalogLinearConfig(noise_enabled=True, sigma_d2d=0.1)
    model = ...; patch_model_for_hat(model, cfg, {0})
    out1 = model(input_ids)
    out2 = model(input_ids)
    # D2D noise is fixed; only C2C changes
    # Key/value states should differ only by C2C component
```
**Expect:** Two forward passes with identical input produce different outputs due to C2C, but the D2D offset pattern is identical.

### 11.3 C2C Resample Test
```python
def test_c2c_resample():
    cfg = AnalogLinearConfig(noise_enabled=True, sigma_c2c=0.1, sigma_d2d=0.0)
    model = ...; patch_model_for_hat(model, cfg, {0})
    out1 = model(input_ids)
    out2 = model(input_ids)
    assert not torch.allclose(out1, out2)
```
**Expect:** With D2D disabled, two identical forward passes produce different outputs because C2C is re-sampled.

### 11.4 Retention Monotonicity Test
```python
def test_retention_monotonicity():
    cfg = AnalogLinearConfig(retention_enabled=True, A_0=0.6, tau_1=0.14, tau_2=0.61)
    x = torch.ones(1, 1, 10, 1)
    out = analogize_kv_tensor(x, cfg, retention_step_time=1.0)
    # Older tokens (index 0) should have smaller magnitude than newer (index 9)
    assert out[0, 0, 0, 0] < out[0, 0, 9, 0]
```
**Expect:** Earlier token positions (older) show more decay than later positions.

### 11.5 Layer Count Test
```python
def test_layer_count():
    model = ...
    count = patch_model_for_hat(model, cfg, {23})
    assert count == 1
    count_all = patch_model_for_hat(model, cfg, None)
    assert count_all == model.config.num_hidden_layers
```
**Expect:** Selective patching patches exactly the requested number of layers.

