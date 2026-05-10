# Higher-Order NL Surrogate Experiment Spec (G-FF3)

**Objective.** Test whether the ~30 % fresh-instance accuracy ceiling is an artifact of the first-order NL surrogate or a structural limit of nonlinear-write attention.

---

## 1. Physical Model

The current surrogate scales backward gradients by a state-dependent power law. For a conductance $g\in[G_{\min},G_{\max}]$ and $\mathrm{NL}=2.0$:

**First-order (current):**
$$
\frac{\partial L}{\partial g}_{\text{eff}}^{(1)} = \frac{\partial L}{\partial g}\cdot\Bigl(\frac{G_{\max}-g}{\Delta G}\Bigr)^{\!\mathrm{NL}-1}
$$

**Second-order surrogate:** expand the true write dynamics to include curvature in the conductance update. The effective gradient becomes
$$
\frac{\partial L}{\partial g}_{\text{eff}}^{(2)} = \frac{\partial L}{\partial g}_{\text{eff}}^{(1)}\cdot\Bigl[1 + \kappa\,\Bigl(\frac{G_{\max}-g}{\Delta G}\Bigr)\Bigr]
$$
where $\kappa\in[0,1]$ is a dimensionless curvature coefficient. Near $G_{\max}$ the bracket term suppresses updates more aggressively than the first-order model, capturing the physical intuition that filament saturation is super-exponential. The same structure applies to LTD with $(g-G_{\min})/\Delta G$. At $\kappa=0$ the model collapses exactly to the first-order baseline, enabling an ablation switch.

---

## 2. Implementation Strategy

| File | Change |
|------|--------|
| `analog_layers_ensemble.py` | Add `nl_order: int = 1` and `nl_curvature: float = 0.0` to `AnalogLinearConfig`. Extend `StraightThroughQuantize.backward` to compute the bracket term when `nl_order >= 2`. |
| `analog_layers_ensemble.py` | Update `ste_quantize` signature to accept `nl_order` and `nl_curvature`, forwarding them to the autograd function. |
| `train_tinyvit_ensemble.py` | Add `nl_order` and `nl_curvature` to `TinyViTExperimentConfig`; wire them into model config and CLI (`--nl-order`, `--nl-curvature`). |
| `eval_nl_fresh_instance_controls.py` | Pass through the new config fields so fresh-instance evaluation uses the same surrogate order as training. |

Backward compatibility: `nl_order=1` (default) reproduces the current code path exactly; no existing checkpoints are invalidated.

---

## 3. Experiment Protocol

**Dataset:** CIFAR-10 (fastest turnaround, well-characterized baseline).

**Conditions:**
- **Baseline (V4-1st):** `NL_LTP=2.0`, `NL_LTD=-2.0`, `nl_order=1`, standard noise ($\sigma_{\text{C2C}}=0.05$, $\sigma_{\text{D2D}}=0.10$), HAT enabled, 100 epochs.
- **Treatment (V4-2nd):** Identical except `nl_order=2`, `nl_curvature=0.5`.

**Training:** from scratch (no warm-start), 3 seeds (42, 123, 456), batch size 64, lr $5\times10^{-4}$, weight decay 0.05.

**Fresh-instance evaluation:** For each trained checkpoint, resample D2D noise over 10 fresh instances and report mean $\pm$ std test accuracy.

---

## 4. Success Criterion

- If **Treatment fresh-instance $\ge 50\%$** on CIFAR-10, the ~30 % ceiling is **surrogate-fidelity specific**. The first-order model is too coarse; higher-fidelity write dynamics reveal learnable compensations that transfer across device instances.
- If **Treatment fresh-instance $\le 35\%$**, the ceiling is **structural**. Even with curvature-corrected gradients, the attention mechanism under conductance-power-law nonlinearity cannot escape the dynamic-range collapse bound.

This is a crisp falsification test: the two hypotheses predict non-overlapping outcome regions.

---

## 5. Compute Estimate

~30 GPU-hours on A100:
- 2 conditions $\times$ 3 seeds $\times$ 100 epochs $\times$ ~3 min/epoch ≈ 30 h.
- Fresh-instance eval (10 instances $\times$ 6 checkpoints) ≈ 1 h additional.

---

## 6. Risk: Numerical Instability

The multiplicative bracket term $[1 + \kappa(\cdot)]$ can amplify gradient variance near conductance boundaries, causing loss spikes or NaNs early in training.

**Mitigation:**
1. **Gradient clipping:** `max_norm=1.0` throughout training.
2. **Curriculum $\kappa$:** anneal `nl_curvature` from 0.0 to 0.5 over the first 20 epochs.
3. **NaN guard:** if any NL-scaled gradient is NaN, fall back to the first-order scale for that step and log a warning.
4. **Mixed-precision safe mode:** run the NL backward in FP32 when `amp` is enabled.
