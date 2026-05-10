# GEMINI Dual-Bug Final Ruling
**Date:** 2026-04-23
**Architect:** Gemini (Theory Support)

## 1. Final sign convention for update direction
In the SGD and Adam optimizers used in this project, the weight update direction is strictly opposite to the gradient sign:
- **LTD (Decrease)**: Occurs when `grad_output > 0` (update $\Delta W = -\eta \cdot \text{grad} < 0$).
- **LTP (Increase)**: Occurs when `grad_output < 0` (update $\Delta W = -\eta \cdot \text{grad} > 0$).

## 2. Gradient Scaling Mapping
To align with the physical update difficulty:
- **Positive `grad_output`** (LTD update) MUST use **LTD scaling** (`ltd_scale`).
- **Negative `grad_output`** (LTP update) MUST use **LTP scaling** (`ltp_scale`).

## 3. Correct Second-Order Coefficient
The second-order Taylor correction is derived from the first derivative of the scaling factor $S(u) = u^{NL-1}$.
The derivative $S'(u)$ yields a coefficient of strictly **$(NL - 1)$**.
The current extraneous $NL$ multiplier in the code is a mathematical error and must be removed.

## 4. Canonical Backward Pseudocode
```python
# 1. Calculate first-order scales (Branch A: no-multiplier)
ltp_scale = pow(ltp_ratio, nl_ltp - 1.0)
ltd_scale = pow(ltd_ratio, nl_ltd - 1.0)

# 2. Assign base gradient (Fix: correctly map signs to update direction)
# grad_output > 0 is LTD; grad_output < 0 is LTP
grad_input = where(grad_output >= 0, grad_output * ltd_scale, grad_output * ltp_scale)

# 3. Apply second-order "brake" correction (SO2)
if use_second_order:
    # Derivative of S(u) = u^(nl-1) is (nl-1)*u^(nl-2)
    # Negative sign ensures the correction acts as a brake on gradient magnitude
    ltp_corr = -0.5 * (nl_ltp - 1.0) * pow(ltp_ratio, nl_ltp - 2.0) * delta_g
    ltd_corr = -0.5 * (nl_ltd - 1.0) * pow(ltd_ratio, nl_ltd - 2.0) * delta_g

    # Map correction branches identically to the base gradient
    correction = alpha * where(grad_output >= 0, grad_output * ltd_corr, grad_output * ltp_corr)
    grad_input = grad_input + correction
```

## 5. Deployment Recommendation
**Both the branch-swap fix and the coefficient correction MUST land together in a single atomic commit** to ensure the physical engine reaches a consistent and valid state before any further GPU time is consumed.
