# Temperature-Drift Experimental Spec v2

**Date:** 2026-04-20 | **Status:** Design brief — no measured results yet.

---

## 1. Physical Model

Arrhenius-form conductance drift:

\[ G(T,t) = G_0 \cdot \exp\!\left(-\frac{E_a}{k_B T}\right) \cdot f(t) \]

- \(T\): absolute temperature (K); \(k_B = 8.617 \times 10^{-5}\) eV/K
- \(f(t)\): existing double-exponential retention envelope (\(\tau_1, \tau_2, A_0\))
- \(E_a\): 0.3–0.8 eV (organic RRAM typical; bracket with 0.2 eV and 1.0 eV if time permits)
- **Range:** −20 °C (253 K) → 25 °C (298 K, control) → 85 °C (358 K)

**Two effects:**
- **Scale:** exponential prefactor modulates mean conductance before quantization.
- **Noise:** \(\sigma_{\text{C2C}}\) and \(\sigma_{\text{D2D}}\) scale by \(\sqrt{T/T_{\text{nom}}}\).

---

## 2. Profile Integration

Add to `DeviceProfile` (`compute_vit/device_profile_utils.py`):

```python
temperature_celsius: float = 25.0
```

- Validate: \(-40 \le T \le 125\); non-float raises `ValueError`.
- JSON key: `environment.temperature_celsius` in `profile_to_payload()` and `_profile_from_payload()`.
- Default `25.0` preserves backward compatibility.

The analog forward path reads the field at layer construction and computes the Arrhenius multiplier once per instantiation.

---

## 3. Experiment Protocol

| Condition | Train | Evaluate | Purpose |
|-----------|-------|----------|---------|
| Baseline | 25 °C | 25 °C | Control |
| Cold drift | 25 °C | −20 °C | Low-T noise vs. trap variability |
| Hot drift | 25 °C | 85 °C | High-T variance amplification |
| Cycle | 25 °C | 25 → 50 → 85 °C sequential | Ranking stability under sweep |

**Fixed settings:**
- Model: Tiny-ViT-5M, ImageNet-pretrained, CIFAR-10 fine-tuning
- 50 epochs, AdamW, lr = 5×10⁻⁴, batch size 64, cosine schedule
- 16 states, \(\sigma_{\text{C2C}}=5\%\), \(\sigma_{\text{D2D}}=10\%\), 8-bit ADC
- HAT: epoch-level D2D resampling (Ensemble HAT)

**Success criterion:** Ensemble HAT > fixed-mask HAT > naive (no HAT) at **every** temperature. Any inversion flags review.

---

## 4. Compute Budget

| Item | Value |
|------|-------|
| Profiles per temp | 5 (OPECT, RRAM, PCM, Pessimistic, Ideal) |
| Seeds per profile | 3 (42, 123, 2026) |
| Eval runs per checkpoint | 10 MC |
| Time per 50-epoch run | ≈ 2.5 GPU-h (A100, Tiny-ViT CIFAR-10) |

| Sweep | Runs | GPU-hours |
|-------|------|-----------|
| One temperature point | 5 × 3 = 15 | ≈ 38 |
| Full sweep (4 conditions) | 60 | ≈ 150 |
| With 10 % overhead | — | **≈ 165** |

---

## 5. Expected Outcomes

| Temperature | Prediction | Mechanism |
|-------------|------------|-----------|
| 85 °C | Mild degradation (−2 to −5 pp vs. 25 °C) | Thermal noise amplifies \(\sigma_{\text{C2C}}\) |
| −20 °C | Neutral to slight improvement (±1 pp) | Reduced thermal noise; trap variability may dominate |
| Ranking | Preserved | Ensemble HAT regularization is temperature-agnostic |

---

## 6. Blockers / Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| \(E_a\) outside 0.3–0.8 eV | Medium | Sensitivity arms at 0.2 eV and 1.0 eV |
| \(\tau(T)\) coupling unmodeled | High | Fix inference time at 1 s; isolate T effect |
| Spatial thermal gradients ignored | Medium | Document as limitation |
| Compute estimate off by >2× | Low | Pilot 3-run subset before full sweep |
| Ranking inversion at extreme T | Low | Pre-register criterion; expand to 10 seeds if seen |

**Invalidating assumptions:**
1. Thermally reversible hysteresis (not Arrhenius drift).
2. NL_LTP / NL_LTD are themselves temperature-dependent.
3. Photoresponse \(\gamma_{\text{phys}}\) shifts with \(T\) (held constant here).
