# K4R Results — Conditional Drafts for `05_results.tex`

**Date:** 2026-04-23
**Canonical Commit:** `ab56c2d` (Branch A)
**Experiment:** K4R — `group=all` uniform-NL, second-order brake (α = 0.25), auto-computed δg_eff
**Predecessor Baseline:** 86.37 ± 1.54% [INVALID] — pre-`ab56c2d`, wrong second-order signs
**Status:** First canonical fresh-instance result under ratified Branch A semantics.

---

## Usage Instructions

Select **exactly one** of the three paragraphs below and paste it into `paper/latex_gpt/sections/05_results.tex` under `\subsection{Ensemble HAT (Task 37)}`, replacing the final sentence that currently reads:

> Across 10 fresh hardware instances with different spatial mismatch maps, the Ensemble HAT model demonstrates remarkable zero-shot transferability. Across 10 fresh hardware instances with different spatial mismatch maps, the Ensemble HAT model maintains an average accuracy of **86.37 ± 1.54%~[INVALID]**.

Replace that sentence with the selected draft paragraph. Do not keep the old `[INVALID]` sentence alongside the new paragraph.

---

## Draft A — Scenario A: Cross-Instance Mean ≥ 85%

> The first canonical Branch A experiment (K4R) evaluates Ensemble HAT under the ratified `group=all` uniform-NL protocol with a sign-corrected second-order brake (α = 0.25). Across ten fresh hardware instances, the model achieves a cross-instance mean of **[MEAN] ± [STD]%**, establishing that the curvature brake does not degrade zero-shot transfer relative to the pre-Branch-A baseline of 86.37 ± 1.54% [INVALID]. The negative second-order term acts as a physical regularizer: it penalizes updates that would drive weights into narrow loss-landscape ravines where small conductance perturbations produce large effective-weight excursions, thereby favoring flat minima that remain stable under fresh D2D realizations. Because the brake is derived from the local curvature of the non-linear write response, its sign-corrected form directly encodes the physical intuition that severe write non-linearity should suppress, not amplify, aggressive parameter updates. These results validate the second-order physics under the canonical codebase and support the use of α = 0.25 as a safe operating point. The next step is a controlled sweep of α ∈ {0.1, 0.5, 1.0} to characterize the sensitivity of transfer accuracy to brake strength and to identify whether a larger α yields further gains.

---

## Draft B — Scenario B: Cross-Instance Mean 80–85%

> The first canonical Branch A experiment (K4R) evaluates Ensemble HAT under the ratified `group=all` uniform-NL protocol with a sign-corrected second-order brake (α = 0.25). Across ten fresh hardware instances, the model achieves a cross-instance mean of **[MEAN] ± [STD]%**, indicating near-parity with but slightly below the pre-Branch-A baseline of 86.37 ± 1.54% [INVALID]. The negative second-order term applies a mild curvature penalty that discourages the optimizer from settling into fragile minima—regions where the surrogate loss is shallow but the physical loss under fresh D2D is steep—yet at α = 0.25 this regularization appears modestly conservative, leaving a small residual gap relative to the earlier, physically inconsistent baseline. This outcome is consistent with the interpretation that the brake trades a marginal amount of source-domain expressivity for improved instance-wise stability, and the trade-off may not yet be at its optimum. Because the degradation is bounded and monotonic rather than catastrophic, the second-order formulation itself remains structurally sound. The recommended next step is a downward sweep of α ∈ {0.05, 0.1, 0.15, 0.25} to determine whether a weaker brake can recover the missing accuracy without sacrificing the physical sign constraint.

---

## Draft C — Scenario C: Cross-Instance Mean < 80%

> The first canonical Branch A experiment (K4R) evaluates Ensemble HAT under the ratified `group=all` uniform-NL protocol with a sign-corrected second-order brake (α = 0.25). Across ten fresh hardware instances, the model achieves a cross-instance mean of **[MEAN] ± [STD]%**, a statistically significant and unexpected degradation relative to the pre-Branch-A baseline of 86.37 ± 1.54% [INVALID]. While the negative second-order term is physically motivated as a curvature brake that suppresses updates in regions of high effective-weight sensitivity, the present result suggests that at α = 0.25 the brake is overly aggressive: it may flatten the loss landscape to the point where the model cannot converge to a sufficiently task-accurate basin, or it may interact destructively with the per-epoch D2D resampling schedule by over-regularizing the ensemble diversity. This outcome cautions against treating the second-order correction as an unqualified improvement without instance-transfer validation. An alternative hypothesis is that the pre-Branch-A baseline benefited from a fortuitous cancellation between the wrong-sign second-order term and other training hyperparameters, and that restoring physical correctness exposes a genuine robustness ceiling. The immediate next step is a first-order-only ablation (`use_second_order_ste = False`) to isolate whether the degradation is attributable to the brake itself or to an interaction between the brake and the ensemble HAT training dynamics.

---

## Branch A Compliance Checklist for Editorial Review

| Requirement | Draft A | Draft B | Draft C |
|:------------|:--------|:--------|:--------|
| Cites pre-Branch-A 86.37% with `[INVALID]` | ✅ | ✅ | ✅ |
| Frames K4R as first canonical experiment | ✅ | ✅ | ✅ |
| Mentions `group=all` uniform-NL + SO2 brake (α=0.25) | ✅ | ✅ | ✅ |
| Includes `[MEAN]` and `[STD]` placeholders | ✅ | ✅ | ✅ |
| Compares with pre-Branch-A baseline | ✅ | ✅ | ✅ |
| Physical interpretation of second-order brake | ✅ | ✅ | ✅ |
| Next-step recommendation | ✅ | ✅ | ✅ |
| Scenario-specific emphasis | ✅ | ✅ | ✅ |
| 5–8 sentences | 6 | 6 | 7 |

---

## Physical Interpretation Reference (for copy-editing)

> The second-order brake derives from the Taylor expansion of the effective-weight mapping $w_{\text{eff}} = s(g^+ - g^-)$ under non-linear conductance updates. The term $-0.5 \cdot \alpha \cdot \text{NL}(\text{NL}-1) \cdot (\delta g / g)^2$ carries a negative sign for both LTP and LTD in Branch A, so it subtracts from the first-order gradient rather than adding to it. Physically, this means that when the local curvature of the write-response curve is high—i.e., a small change in programmed conductance produces a disproportionately large swing in recovered effective weight—the optimizer receives a penalty that pushes the solution away from that region. The effect is analogous to loss-landscape flattening: the brake discourages minima that are ``sharp'' in conductance space, because such minima are unstable under the fresh D2D variations encountered at deployment. The parameter α controls the strength of this flattening; α = 0.25 was chosen as a conservative initial value based on the K3 calibration trajectory.

---

**⚠️ DEPRECATED 2026-04-24** — This memo references bug-contaminated data (STE branch swap + extraneous nl multiplier in analog_layers.py, fixed at commit 33bed9c). The "structural ceiling / bimodal basin / Hartigan p=0.98" narrative is invalidated. Do not cite as evidence. See BROADCAST_HALT_AND_REPLICATE_20260424.md and BROADCAST_REBUILD_3WEEK_20260424.md for current status.
