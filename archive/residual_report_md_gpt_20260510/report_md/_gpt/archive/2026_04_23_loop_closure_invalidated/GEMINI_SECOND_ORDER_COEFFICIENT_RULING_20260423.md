# GEMINI Second-Order Coefficient Ruling
**Date:** 2026-04-23
**Architect:** Gemini (CLI Agent)

## 1. Statement of the exact surrogate being expanded
The implemented first-order scaling surrogate $S(u)$ in `analog_layers.py` (ratified Branch A) is defined as:
$$S(u) = (u_{norm})^{NL-1}$$
where $u_{norm}$ is the normalized distance to the "target" conductance bound:
- For LTP (conductance increase): $u_{norm} = \frac{G_{max} - G}{G_{max} - G_{min}}$
- For LTD (conductance decrease): $u_{norm} = \frac{G - G_{min}}{G_{max} - G_{min}}$

As per **Branch A ratification**, there is **no** $NL$ multiplier in the first-order scale.

## 2. Derivation of the Taylor correction
We seek the Taylor correction for the scaling factor $S(u)$ under a perturbation $\Delta u$ (represented by `delta_g_eff`).
The first-order Taylor expansion of $S(u)$ is:
$$S(u + \Delta u) \approx S(u) + S'(u) \Delta u$$

Taking the derivative of $S(u_{norm}) = (u_{norm})^{NL-1}$ with respect to the raw conductance $G$:
1. For LTP: $u_{norm} = \frac{G_{max} - G}{\Delta G}$. Then $\frac{du_{norm}}{dG} = - \frac{1}{\Delta G}$.
   $$S'(G) = (NL-1) \cdot (u_{norm})^{NL-2} \cdot \left(- \frac{1}{\Delta G}\right)$$
2. For LTD: $u_{norm} = \frac{G - G_{min}}{\Delta G}$. Then $\frac{du_{norm}}{dG} = + \frac{1}{\Delta G}$.
   $$S'(G) = (NL-1) \cdot (u_{norm})^{NL-2} \cdot \left(+ \frac{1}{\Delta G}\right)$$

In our implementation, the correction term is defined as `correction = 0.5 * S'(u) * delta_g`.
The required coefficient for the power term $(u_{norm})^{NL-2}$ is therefore strictly **$(NL-1)$**.

The current code implementation:
`ltp_corr = -0.5 * nl_ltp * (nl_ltp - 1.0) * torch.pow(ltp_ratio, nl_ltp - 2.0) * delta_g`
contains an **extraneous `nl` multiplier**.

## 3. Code verdict
The current code in `analog_layers.py` is **INCORRECT**.
It applies an $NL$ prefactor (2.0 in our severe regime) that is not supported by the Taylor expansion of the ratified first-order surrogate. This artificially doubles the strength of the second-order "brake" compared to the mathematical intent.

## 4. Consequence for K4R
The currently running K4R (and all previous SO2 results) must be treated as **INVALID**.
Because the second-order term is twice as strong as it should be, the "brake" is being applied too aggressively. This contaminates the fresh-instance accuracy and prevents a true evaluation of the bimodal basin hypothesis.

## 5. One-sentence operational recommendation
**Immediately stop K4R, remove the `nl_ltp` and `nl_ltd` multipliers from the `ltp_corr` and `ltd_corr` lines in `analog_layers.py`, and relaunch K4R-v3.**
