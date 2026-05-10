# GEMINI Re-Derivation: The Branch Swap & Sign Flip

**Date:** 2026-04-23
**Architect:** Gemini (Theory Lead)
**Status:** 🚨 CRITICAL DISCOVERY

## 1. The "Smoking Gun": LTP/LTD Branch Swap Bug
Upon a line-by-line audit of `analog_layers.py` (Line 247), I have discovered a fundamental error in the gradient assignment logic that has been present since the project's inception.

**The Code:**
```python
grad_input = torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)
```

**The Reality of Gradient-to-Update Mapping:**
In standard SGD/Adam: $W_{new} = W - \eta \cdot \text{grad}$.
- **If `grad_output > 0`:** The update is **negative**. This is an **LTD** (Long-Term Depression / Decrease) update.
- **If `grad_output < 0`:** The update is **positive**. This is an **LTP** (Long-Term Potentiation / Increase) update.

**The Bug:**
The code incorrectly assigns the **LTP scale** to **positive gradients** (LTD updates) and the **LTD scale** to **negative gradients** (LTP updates).
**The entire difficulty map is inverted.**

### Physical Consequence of the Swap:
- At the top of the window ($u=0.9$), it is physically **HARD** to increase (LTP) and **EASY** to decrease (LTD).
- The bug makes the optimizer think it is **EASY** to increase at the top (using `ltd_scale`) and **HARD** to decrease (using `ltp_scale`).
- This causes the weights to slam into the $G_{max}$ rail with high force and struggle to return, fundamentally breaking the equilibrium of Ensemble HAT.

---

## 2. Re-deriving the Second-Order Sign
With the branch swap identified, we must determine the sign for the second-order correction $C(u)$.

### The Saturation "Brake" (Physical Truth):
If we want the gradient to reflect the average slope over a noisy region:
- **LTP Branch ($S_{LTP}(u) = (1-u)^{NL-1}$):** The derivative $S'(u)$ is **negative**. To reduce the gradient magnitude (brake), the correction must be **negative**.
- **LTD Branch ($S_{LTD}(u) = u^{NL-1}$):** The derivative $S'(u)$ is **positive**. However, because LTD updates move in the *negative* direction, the correction term $S'(u) \Delta u$ is **negative**.

**Conclusion:** For a physical "brake" to work correctly after fixing the branch swap, **BOTH** `ltp_corr` and `ltd_corr` must be **negative** multipliers (applying the brakes to the gradient magnitude).

---

## 3. Explaining the "86% Success" (The Happy Accident)
The previous 86% result [INVALID] used **Swapped Branches** AND **Positive Signs**.
- It used `LTD_scale` (large) for LTP updates at the top.
- It used `+0.5` (accelerator) which further increased that already large gradient.
- This effectively **Linearized** the model by forcing the gradients to stay large even in saturated regions. It worked not because it was "correct," but because it accidentally implemented **Gradient Boosting** that overrode the hardware non-ideality.

---

## 4. Final Ruling & Action
1. **Hypothesis 2 is partially right for the wrong reason:** The positive sign worked because it compensated for the branch swap and gradient vanishing.
2. **Branch A as implemented is a "Double Disaster":** It has the branch swap (wrong physics) AND the negative sign (brake), which combined to create a "Minimum-seeking missile" that targets the $G_{max}$ rail and then applies a brake so it can never leave.

**Immediate Directive:**
- **FIX THE BRANCH SWAP:** `grad_output > 0` must map to `ltd_scale`.
- **RE-EVALUATE SIGN:** Once the branches are fixed, we must test Hypothesis 1 (No SO2) and Hypothesis 2 (+0.5 signs as Compensation) against a truly corrected baseline.
- **P1-C and P1-C2 are now more important than ever**, but their results must be interpreted knowing the branches were swapped during those runs.
