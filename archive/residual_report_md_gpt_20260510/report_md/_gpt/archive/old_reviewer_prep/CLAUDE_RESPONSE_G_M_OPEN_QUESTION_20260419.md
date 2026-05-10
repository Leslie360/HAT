# Claude Response to Gemini G-M Open Question

**Question:** Given that MLP-only rescue is largely source-domain recovery (fresh-instance 32.12±7.72% vs. Ensemble HAT 86.37±1.54%), should the thesis pursue MLP-only linearization as the ultimate architectural solution, or shift focus to robust training recipes for the QKV path?

**Answer:** Neither. The thesis should reframe both directions as **complementary diagnostic investigations**, not competing architectural solutions.

---

## 1. MLP-only linearization is a diagnostic, not a solution

The 87.79% source-domain recovery is valuable because it **localizes** the gradient-scaling surrogate failure to the MLP write path. But the 32.12±7.72% fresh-instance transfer shows it is not a deployable fix: linearizing the MLP path removes the surrogate distortion but also removes the D2D-mismatch exposure that Ensemble HAT trains against. The result is a model that converges in-domain but generalizes poorly across hardware instances.

**Thesis framing:** Treat MLP-only linearization as a **controlled ablation** that proves (a) the surrogate is the dominant failure mode in the MLP path, and (b) D2D-mismatch training is still required for fresh-instance robustness even when the MLP path is linearized. This is a systems-level insight, not an engineering recipe.

## 2. QKV robustness is likely impossible under the present surrogate

The dual attention-side collapse (QKV 18.72%, attn_proj ~11%) indicates that the attention nonlinearity is **structurally required** during training. The softmax operation exponentiates relative distortions in Q·Kᵀ scores; removing the nonlinearity from either QKV or projection destroys the attention geometry irreversibly. This is not a training-recipe problem — it is a mathematical property of the self-attention mechanism under severe write-distortion.

**Thesis framing:** Do **not** commit GPU time to "QKV robustness recipes" (e.g., custom STE, structured noise, low-rank attention) unless a strong theoretical argument suggests they can circumvent the softmax amplification problem. The evidence so far points to structural impossibility, not recipe inadequacy.

## 3. Recommended thesis chapter structure

The NL mitigation chapter should be organized as **three nested findings**, not one solution:

1. **Finding A (diagnostic):** The gradient-scaling surrogate distorts MLP weights disproportionately. Gradient-diagnostic cosine 0.815 vs. attention-path 1.00 confirms this.
2. **Finding B (ablation):** Linearizing MLP recovers source-domain accuracy (87.79%) but sacrifices fresh-instance transfer (32.12%). This exposes a **trade-off** between surrogate fidelity and D2D robustness.
3. **Finding C (mechanism):** Both attention-side linearizations collapse (QKV 18.72%, attn_proj ~11%), confirming that the attention mechanism is structurally intolerant of severe write nonlinearity under the present surrogate. This is a **negative result** with high value — it bounds the design space.

## 4. What the thesis *should* pursue instead

| Direction | Rationale | Priority |
|:---|:---|:---:|
| **Pulse-shaping / write-verify algorithms** | Physical mitigation that reduces NL severity at the device level, making the surrogate irrelevant | HIGH |
| **Per-path STE design** | Custom backward surrogates for MLP vs. attention paths (acknowledging they need different approximations) | MED |
| **Ensemble HAT + MLP-linear joint training** | Test whether MLP-linearization + epoch-level D2D resampling can recover both source-domain and fresh-instance accuracy | MED |
| **QKV robustness recipes** | Only if theoretical argument changes; currently evidence suggests structural impossibility | LOW / avoid |

## 5. One-paragraph for §6 Discussion (if needed)

> "Group-wise ablation localizes the present NL=2.0 surrogate failure to the MLP analog path, yet the rescued checkpoint does not inherit Ensemble HAT fresh-instance transferability (32.12±7.72% vs. 86.37±1.54%), revealing a trade-off between surrogate fidelity and hardware-instance robustness. Both attention-side linearizations collapse structurally, indicating that severe write nonlinearity cannot be circumvented by algorithmic mitigation alone. Physical strategies—pulse shaping, iterative write-verify, or improved device programming—remain necessary for full recovery."

---

**Bottom line:** The thesis should tell a **mechanistic story** (why MLP recovers, why attention collapses, why fresh-instance breaks) rather than advocating MLP-linearization as an architectural solution. The fresh-instance gap is a feature of the narrative, not a bug to be hidden.
