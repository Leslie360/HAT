# CODEX Remote Parity Triage Report

Date: 2026-04-22
Repo: `compute_vit`
Purpose: answer the 3 concrete parity questions needed to explain the local-vs-remote J1d mismatch.

## Executive Findings

1. In the local code, `NL_LTP`, `NL_LTD`, `use_second_order_ste`, and `delta_g_eff` do **not** change the quantizer's forward value in `StraightThroughQuantize.forward()`.
   - They are stored in `ctx` and only used in `StraightThroughQuantize.backward()`.
   - Therefore, if remote is seeing a large **epoch-0 source-domain** gap, the first suspect is **not** forward-time NL distortion inside `STE.forward()`.

2. The local baseline checkpoint MD5 is:
   - `af0d9a6be75de766a2621ae058a61393`  `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

3. Local `train_one_epoch()` computes training accuracy using the batch predictions from the **same forward pass used to compute loss**, before any re-forward after the optimizer step.
   - Concretely: `outputs = model(inputs)` -> `loss.backward()` -> `optimizer.step()` -> compute `predicted` from the already-computed `outputs` tensor.
   - So `epoch 0 train_acc=88.05%` is **not** a post-update re-evaluation metric.

---

## 1. Local `analog_layers.py`

### 1.1 `StraightThroughQuantize.forward` / `backward`

File: `analog_layers.py:162-249`

```python
@staticmethod
def forward(ctx, x: torch.Tensor, n_levels: int,
            x_min: float, x_max: float,
            nl_ltp: float = 1.0, nl_ltd: float = -1.0,
            inl_table: Optional[torch.Tensor] = None,
            use_second_order_ste: bool = False,
            delta_g_eff: float = 0.0) -> torch.Tensor:
    eps = 1e-8
    scale = x_max - x_min + eps
    x_clamped = torch.clamp(x, x_min, x_max)
    ctx.save_for_backward(x_clamped)
    ctx.x_min = float(x_min)
    ctx.x_max = float(x_max)
    ctx.nl_ltp = float(nl_ltp)
    ctx.nl_ltd = float(nl_ltd)
    ctx.use_second_order_ste = bool(use_second_order_ste)
    ctx.delta_g_eff = float(delta_g_eff)

    if inl_table is not None:
        x_flat = x_clamped.flatten()
        dist = torch.abs(x_flat.unsqueeze(1) - inl_table.unsqueeze(0))
        indices = torch.argmin(dist, dim=1)
        x_quant_flat = inl_table[indices]
        return x_quant_flat.view_as(x_clamped)
    else:
        x_norm = (x_clamped - x_min) / scale
        x_quant = torch.round(x_norm * (n_levels - 1)) / (n_levels - 1)
        return x_quant * scale + x_min

@staticmethod
def backward(ctx, grad_output: torch.Tensor):
    (x_clamped,) = ctx.saved_tensors
    x_min = ctx.x_min
    x_max = ctx.x_max
    nl_ltp = abs(ctx.nl_ltp)
    nl_ltd = abs(ctx.nl_ltd)

    grad_input = grad_output
    eps = 1e-8
    conductance_span = max(x_max - x_min, eps)

    if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
        ltp_ratio = ((x_max - x_clamped) / conductance_span).clamp_min(eps)
        ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)
    else:
        ltp_scale = torch.ones_like(grad_output)

    if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
        ltd_ratio = ((x_clamped - x_min) / conductance_span).clamp_min(eps)
        ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)
    else:
        ltd_scale = torch.ones_like(grad_output)

    grad_input = torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)

    if getattr(ctx, 'use_second_order_ste', False) and getattr(ctx, 'delta_g_eff', 0.0) > 0.0:
        delta_g = ctx.delta_g_eff
        if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltp_corr = 0.5 * nl_ltp * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g
        else:
            ltp_corr = torch.zeros_like(grad_output)

        if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltd_corr = 0.5 * nl_ltd * (nl_ltd - 1.0) * torch.pow(ltd_ratio.clamp_min(eps), nl_ltd - 2.0) * delta_g
        else:
            ltd_corr = torch.zeros_like(grad_output)

        correction = torch.where(grad_output >= 0, grad_output * ltp_corr, grad_output * ltd_corr)
        grad_input = grad_input + correction

    return grad_input, None, None, None, None, None, None, None, None
```

### 1.2 `AnalogLinear.forward`

File: `analog_layers.py:560-579`

```python
def forward(self, x: torch.Tensor) -> torch.Tensor:
    """Full analog inference pipeline.

    x: (..., in_features)
    returns: (..., out_features)
    """
    _record_input_sparsity(self, x)
    # Step 1: Float weight → quantized differential conductance pair
    G_pos, G_neg = self._weight_to_conductance(self.weight)

    # Step 2: Optional retention decay
    G_pos, G_neg = self._apply_retention(G_pos, G_neg)
    retained_diff = G_pos - G_neg

    # Step 3: Apply noise (D2D fixed + C2C re-sampled)
    W_eff = self._apply_noise(G_pos, G_neg)
    W_eff = W_eff * self._conductance_to_weight_scale(self.weight, retained_diff)

    # Step 4: Vector-Matrix Multiplication
    return F.linear(x, W_eff, self.bias)
```

### 1.3 Where NL actually enters the analog layer

File: `analog_layers.py:431-451`

```python
# Quantization-sensitive mapping stays in float32 under AMP.
with autocast_disabled_context(W.device.type):
    W_fp32 = W.float()

    # Split into positive and negative parts
    W_pos = torch.clamp(W_fp32, min=0.0)
    W_neg = torch.clamp(-W_fp32, min=0.0)

    # Normalize by max absolute weight (detached to avoid gradient through normalizer)
    w_abs_max = W_fp32.abs().max().detach() + eps
    W_pos_norm = W_pos / w_abs_max  # in [0, 1]
    W_neg_norm = W_neg / w_abs_max  # in [0, 1]

    # Map to conductance range [G_min, G_max]
    G_range = cfg.G_max - cfg.G_min
    G_pos = cfg.G_min + W_pos_norm * G_range
    G_neg = cfg.G_min + W_neg_norm * G_range

    # Quantize to discrete conductance levels
    G_pos = ste_quantize(G_pos, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff)
    G_neg = ste_quantize(G_neg, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff)
```

### 1.4 Practical interpretation

- `AnalogLinear.forward()` itself does **not** explicitly distort conductance with NL.
- The local code path is:
  - `AnalogLinear.forward()`
  - `->_weight_to_conductance()`
  - `-> ste_quantize(...)`
- In this local implementation, `ste_quantize.forward()` still does plain clamp-normalize-round-denormalize.
- `NL_LTP/NL_LTD/use_second_order_ste/delta_g_eff` affect **gradient flow**, not the quantized forward conductance value.

If remote has implemented NL as a forward-time conductance distortion, that alone could explain a large epoch-0 source-domain mismatch.

---

## 2. Local baseline checkpoint MD5

Command:

```bash
md5sum checkpoints/V4_hybrid_standard_noise_hat_best.pt
```

Result:

```text
af0d9a6be75de766a2621ae058a61393  checkpoints/V4_hybrid_standard_noise_hat_best.pt
```

This is the local authoritative MD5 for the baseline warm-start checkpoint.

---

## 3. Local `train_one_epoch()` implementation

File: `train_tinyvit_ensemble.py:407-441`

```python
def train_one_epoch(model: nn.Module, trainloader, optimizer, criterion, device: str,
                    exp_cfg: TinyViTExperimentConfig, frontend: Optional[nn.Module] = None,
                    amp_enabled: bool = False, scaler=None):
    """Run one training epoch and return (loss, accuracy)."""
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in trainloader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)

        if frontend is not None:
            inputs = frontend(inputs, mode="compensated")

        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)

        if scaler is not None and scaler.is_enabled():
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)

    return running_loss / total, 100.0 * correct / total
```

### Interpretation of local epoch-0 train accuracy

- The per-batch `predicted` is computed from the same `outputs` tensor used for the loss.
- That `outputs` tensor is generated **before** `optimizer.step()`.
- The code does **not** do a second forward pass after the update.
- Therefore, local `epoch 0 train_acc` is an average of **pre-update batch predictions**, accumulated over the first epoch.

This means the local `epoch 0 train_acc=88.05%` is not explained by “the metric was computed after one optimizer step on each batch.”

---

## 4. Local surviving J1d epoch log

Source log: `logs/_gpt/cx_j1d_20260421.log`

Available surviving markers are:

```text
[2026-04-21 10:15:24]   Epoch   0/100: train_loss=0.3628, train_acc=88.05%, test_acc=81.86% (best=81.86%), lr=0.000500
[2026-04-21 10:50:23]   Epoch  19/100: train_loss=0.1237, train_acc=95.81%, test_acc=87.78% (best=88.48%), lr=0.000457
[2026-04-21 11:26:37]   Epoch  39/100: train_loss=0.0685, train_acc=97.67%, test_acc=88.56% (best=89.92%), lr=0.000335
[2026-04-21 12:02:55]   Epoch  59/100: train_loss=0.0280, train_acc=99.07%, test_acc=89.61% (best=90.74%), lr=0.000180
[2026-04-21 12:38:46]   Epoch  79/100: train_loss=0.0069, train_acc=99.77%, test_acc=89.89% (best=91.02%), lr=0.000052
[2026-04-21 13:14:29]   Epoch  99/100: train_loss=0.0049, train_acc=99.86%, test_acc=89.49% (best=91.02%), lr=0.000000
```

Important limitation:
- The local surviving artifact does **not** include epochs 1-4.
- So the only trustworthy early local point we can currently quote is epoch 0.

---

## 5. What remote should check first

Given the current local evidence, the most likely parity breakers are:

1. **Checkpoint mismatch**
   - Verify MD5 exactly equals `af0d9a6be75de766a2621ae058a61393`.

2. **Forward-path NL mismatch**
   - Local code does **not** apply NL distortion in `STE.forward()`.
   - If remote does, epoch-0 source-domain numbers will diverge immediately.

3. **Warm-start path mismatch**
   - The local J1d lane warm-starts from the baseline checkpoint and resets optimizer/scheduler state.

4. **Metric interpretation mismatch**
   - Local `epoch 0 train_acc` is computed from pre-update batch outputs within epoch 0.
   - It is not a post-update re-evaluation metric.

If remote confirms all 4 are aligned and still sees `~23%` vs local `88%`, then the next suspect is no longer reporting logic; it is a deeper code-path difference in model construction or warm-start loading.
