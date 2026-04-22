# IR-Drop Preliminary Experimental Spec v2

**Date:** 2026-04-20 | **Scope:** Minimal-effort circuit-aware layer for crossbar IR-drop in Ensemble HAT.

---

## 1. Physical Model

For an M×N crossbar, treat wordlines (WL) and bitlines (BL) as resistive buses. The voltage drop at cell (i,j) is:

$$\Delta V_{ij} = \underbrace{\sum_{k=0}^{i} I_{WL,k} \cdot R_{line}}_{\text{WL drop}} + \underbrace{\sum_{k=0}^{j} I_{BL,k} \cdot R_{line}}_{\text{BL drop}}$$

where $R_{line}$ is the uniform segment resistance and $G_{ij}$ is the cell conductance. Current through cell (i,j) is $I_{ij} = (V_{WL} - V_{BL}) \cdot G_{ij}$.

**Assumptions:** uniform $R_{line}$, static $G_{ij}$, single-sided drivers, ideal selectors. **Neglect sneak paths and capacitive coupling.** Worst-case drop occurs at the farthest cell (M−1, N−1) with all cells conducting.

## 2. Array Geometry Choice

For fixed total capacity, worst-case drop scales roughly with the longest line length. Back-of-envelope: if $I_{cell} = 1\,\mu A$ and $R_{line} = 0.5\,\Omega$:

| Geometry | $\Delta V_{WL}$ (approx.) | $\Delta V_{BL}$ (approx.) | Verdict |
|---|---|---|---|
| **128×64** | 4.1 mV | 2.0 mV | **Lowest drop** |
| 256×256 | 32.8 mV | 32.8 mV | Highest drop |
| 512×128 | 131 mV | 32.8 mV | WL-dominated, worst |

**Recommendation:** Use **128×64** for the first pass to minimize IR-drop artifacts.

## 3. Implementation Strategy

| Option | Approach | Effort | Rec. |
|---|---|---|---|
| **A** | Pre-compute static IR-drop correction matrix per geometry; apply as additive bias during analog MAC | Minimal | **✓ First pass** |
| B | Full SPICE co-simulation per MAC | Significant | Too expensive |
| C | Neural surrogate trained on SPICE samples | Medium | Deferred to v3 |

**Option A:** Compute $\Delta V_{ij}$ once per geometry under unit conductance, scale by actual inputs, and add as bias: $I_{out,j}^{corr} = I_{out,j} + \sum_i \Delta V_{ij} \cdot G_{ij}$.

## 4. Profile Integration

Add to `DeviceProfile`:

```yaml
ir_drop_enabled: bool   # default false
array_geometry: tuple   # e.g., (128, 64)
```

When enabled, the analog MAC wrapper loads the pre-computed correction matrix for the specified geometry.

## 5. Success Criterion

With IR-drop enabled, run Ensemble HAT ranking-preservation tests.

- **Pass:** Kendall’s $\tau \geq 0.95$ between analog and ideal rankings.
- **Threshold:** If $\tau < 0.95$, the acceptable geometry is the largest where $\tau \geq 0.95$. Expected threshold: **≤ 256×256**.

## 6. Compute Estimate

- **Option A:** Negligible. One-time $\mathcal{O}(MN)$ pre-compute; runtime is a vectorized add.
- **Option C:** Significant. SPICE sampling (~hours) + training (~GPU hours).

## 7. Limitations

| Phenomenon | Captured? |
|---|---|
| Sneak paths | No |
| Non-uniform $R_{line}$ / process variation | No |
| Capacitive coupling (transient) | No |
| Selector ON-resistance | No |
| Thermal self-heating | No |

This model gives a **lower-bound** on IR-drop. If Option A degrades ranking, full parasitics will be worse.
