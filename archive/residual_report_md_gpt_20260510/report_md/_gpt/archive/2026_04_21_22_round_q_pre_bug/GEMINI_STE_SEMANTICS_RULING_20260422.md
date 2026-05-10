# GEMINI STE Semantics Ruling
**Date:** 2026-04-22
**Scope:** Theory and parity arbitration.

## 1. Current code semantics
In the local `analog_layers.py` (after the final physical correction), the Straight-Through Estimator (STE) is implemented as follows:
- **First-Order Scale (LTP):** `ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)` (where `ltp_ratio` represents the normalized headroom $1-u$).
- **First-Order Scale (LTD):** `ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)` (where `ltd_ratio` represents the normalized conductance $u$).
- **Second-Order Correction (LTP):** `ltp_corr = -0.5 * (nl_ltp - 1.0) * torch.pow(ltp_ratio, nl_ltp - 2.0) * delta_g`
- **Second-Order Correction (LTD):** `ltd_corr = -0.5 * (nl_ltd - 1.0) * torch.pow(ltd_ratio, nl_ltd - 2.0) * delta_g`

Crucially, the first-order scale does **not** include a leading `nl` multiplier (i.e., it is $u^{NL-1}$, not $NL \cdot u^{NL-1}$).

## 2. Equation-level derivation
The formal definition of the nonlinear-write surrogate in the manuscript (`paper/latex_gpt/supplementary.tex`, Equation S2) explicitly defines the gradient scaling factor $S(G)$ as:

$$
S_{\mathrm{LTP}}(G) = \left(\frac{G_{\max}-G}{G_{\max}-G_{\min}}\right)^{NL_{\mathrm{LTP}}-1}
$$
$$
S_{\mathrm{LTD}}(G) = \left(\frac{G-G_{\min}}{G_{\max}-G_{\min}}\right)^{|NL_{\mathrm{LTD}}|-1}
$$

The mathematical formulation in the paper intentionally omits the $NL$ constant multiplier. This was a design choice to ensure that when $NL=1.0$, the scaling factor strictly reduces to exactly $1.0$ (the identity STE), without introducing a global scaling bias that would inadvertently alter the effective learning rate across the entire network.

The second-order correction is derived via the Taylor expansion of the scaling factor itself: $S(u + \Delta u) \approx S(u) + S'(u)\Delta u$.
For LTP, $S'(u) = -(NL-1)(1-u)^{NL-2}$.
This leads to the $\frac{1}{2} S'(u) \Delta G$ correction term: $-0.5 \cdot (NL-1)(1-u)^{NL-2} \cdot \Delta G$.

## 3. Ruling: multiplier or no multiplier
**RULING: NO MULTIPLIER in the first-order term.**

The first-order STE gradient scaling MUST strictly follow the formula $u^{NL-1}$ without the leading $NL$ coefficient. The current codebase implementation is mathematically sound and perfectly aligned with the published manuscript.

Adding the $NL$ multiplier would violate Equation S2 and artificially inflate the learning rate of the analog layers by a factor of 2.0, destroying hyperparameter parity with the baseline.

## 4. Consequence for parity interpretation
1. **Remote Parity:** Any remote evaluation or reproduction attempt MUST ensure they are NOT applying the $NL$ multiplier in their STE implementation. If a remote branch added the multiplier (e.g., computing $2.0 \cdot u^{1.0}$ instead of $u^{1.0}$), their effective learning rate for analog weights was doubled, which would explain massive divergences or instability in their joint training runs.
2. **Second-Order Parity:** The remote implementation of the second-order term must correctly incorporate the negative sign (i.e., acting as a braking penalty). An inverted sign in the remote code would push the optimizer into sharp ravines, artificially creating a "bimodal collapse."
3. **Local Truth:** The local `analog_layers.py` is the absolute canonical truth for STE semantics. Remote runs that deviate from these exact mathematical formulations cannot be considered valid parities or falsifications of the framework.
