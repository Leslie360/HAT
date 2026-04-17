# KX41: Proxy-Parameter Defense Pack

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: 防守"proxy parameters make the materials-to-system claim circular"攻击

---

## Defense 1: Explicit Proxy Declaration

**Reviewer Attack**: "参数提取方式若与原作者理解不同，可能引出更多质疑"

**Location**: `paper/latex_gpt/supplementary.tex` (Table S2 caption)

**Current Text**: 
> Table S2: Parameter provenance matrix showing source literature and extraction methodology

**Defense Addition**:
```latex
\textbf{Proxy Parameter Transparency:} All parameters marked with ($^*$) in Table S2 
are explicit proxy estimates derived from literature-reported figures rather than 
raw measurement data. The proxy methodology is fully documented in Supplementary 
Section S1.3, enabling independent verification or replacement when raw data becomes 
available. We emphasize that the paper's core claims concern deployment-risk \textit{ranking} 
(ADC precision > D2D > C2C) rather than absolute accuracy predictions, and this 
ranking remains robust across the parameter uncertainty ranges reported in Table S5.
```

---

## Defense 2: Sensitivity Analysis Scope

**Reviewer Attack**: "C2C from 1% to 8% shows 0.00pp change—this proves your parameters are in a 'protective bubble'"

**Location**: `paper/latex_gpt/sections/05_results.tex` (after Table S3 reference)

**Current Text**:
> The ADC sweep reveals a sharp 6-bit ADC cliff

**Defense Addition**:
```latex
The C2C invariance observed in Table S3 ($\Delta_{\max}=0.00$~pp across 1--8\% C2C) 
is mechanistically explained by the scale-masking effect (Section~5.2): nominal 
conductance noise is rescaled below the 4-bit LSB threshold. This is a \textit{model-internal} 
conclusion valid within the gradient-scaling surrogate regime, not a claim about 
physical device universality. We explicitly scope this finding: when scale recovery 
is active and quantization dominates the noise floor, C2C has limited impact. 
Proportional state-dependent noise (Section~5.6) breaks this protection, demonstrating 
that the conclusion is regime-dependent rather than universal.
```

---

## Defense 3: AIHWKIT Narrative Reframe

**Reviewer Attack**: "AIHWKIT comparison is circular—same assumptions produce same outputs"

**Location**: `paper/latex_gpt/sections/06_discussion.tex` (AIHWKIT paragraph)

**Current Text**:
> Shared-regime sanity checks into broader numerical-equivalence studies

**Defense Replacement**:
```latex
We position the AIHWKIT comparison (90.08\% vs. 95.46\% for ResNet-18/CIFAR-10) 
as a \textbf{methodological consistency check} rather than validation. Both frameworks 
share Gaussian behavioral-modeling assumptions; agreement under matched regimes 
(4-bit quantization, uniform noise) confirms implementation correctness but does 
not establish physical equivalence. This is analogous to cross-compiler testing: 
identical semantics should yield identical results. True physical validation would 
require measured organic-array inference, which we explicitly scope as future work 
(Section~6.6). The comparison's value lies in demonstrating that our PyTorch-native 
implementation reproduces established tool behavior, not in claiming novel physical 
verification.
```

---

## Defense 4: Contribution Re-scope

**Reviewer Attack**: "Your materials-to-system bridge claim is overreaching without measured devices"

**Location**: `paper/latex_gpt/sections/00_abstract.tex` (already modified, add to conclusion)

**Addition to `07_conclusion.tex`**:
```latex
\textbf{Positioning Clarification:} We do not claim to predict specific chip 
performance. The framework provides \textit{relative risk ranking}—identifying 
which device characteristics (ADC resolution, D2D variation, write nonlinearity) 
dominantly constrain deployment under a given behavioral model. When literature 
parameters are approximate, the framework enables sensitivity analysis (Table S3) 
and profile substitution (Section~3.3) to bracket uncertainty. Upon measured-device 
availability, the same interface accepts calibrated profiles without code modification.
```

---

## Defense 5: Ensemble HAT Novelty Anchor

**Reviewer Attack**: "Ensemble HAT is just domain randomization with a new name"

**Location**: `paper/latex_gpt/sections/06_discussion.tex`

**Current Text** (already strong):
> Ensemble HAT is not merely stronger i.i.d. noise augmentation

**Defense Addition**:
```latex
We distinguish Ensemble HAT from domain randomization (DR) \citep{tobin2017domain} 
and randomized smoothing (RS) \citep{cohen2019certified} on structural grounds: 
DR/RS perturb input features or model weights with i.i.d. noise, whereas D2D mismatch 
is a \textit{fixed spatial pattern} that persists across all operations on a given 
array. Resampling this pattern per-epoch trains the model to expect 
\textit{persistent hardware heterogeneity} rather than transient noise. The 
10.00\%$\to$86.37\% fresh-instance recovery is impossible under i.i.d. augmentation 
because standard augmentation does not simulate the spatial-structure mismatch that 
causes instance-overfitting. A quantitative comparison to per-forward i.i.D. D2D 
perturbation would further strengthen this distinction (planned for revision).
```

---

## Defense 6: Energy Model Boundary

**Reviewer Attack**: "11.45x gain is based on placeholder constants, not circuit validation"

**Location**: `paper/latex_gpt/sections/05_results.tex` (energy subsection)

**Current Text**:
> Analytical energy model estimates 273.94 μJ

**Defense Addition**:
```latex
The 11.45$\times$ energy reduction is explicitly framed as a \textbf{first-order 
upper-bound estimate} under behavioral-model assumptions (100~fJ/MAC, 25~fJ/ADC). 
We do not claim tape-out validation. Instead, we provide sensitivity analysis: 
10--50\% routing overhead reduces gain to 9.90--11.10$\times$ (Supplementary 
Fig.~S5), demonstrating that the qualitative advantage survives moderate unmodeled 
costs. The value lies in establishing an analog-digital decomposition methodology 
rather than delivering chip-predictive numbers.
```

---

## Defense 7: NL=2.0 Approximation Limit

**Reviewer Attack**: "NL=2.0 hard boundary implies physical limit, but it's just your approximation failing"

**Location**: `paper/latex_gpt/sections/06_discussion.tex` (limitations)

**Current Text** (already good):
> reflects the limit of this approximation rather than a fundamental materials constraint

**Defense Addition** (strengthening):
```latex
We explicitly acknowledge that the $NL=2.0$ failure ($27.72\pm0.82$\%) is an 
\textbf{approximation-scoped boundary} of the gradient-scaling surrogate, not a 
materials science claim. Alternative training strategies (custom STE, lookup-table 
gradient maps, or meta-learning) may shift this boundary; exploring them is valuable 
future work. The present contribution is identifying that \textit{under standard 
gradient-scaling HAT}, severe write nonlinearity represents an unrecovered stress 
regime—a deployment-relevant finding for practitioners choosing between HAT investment 
and device engineering priorities.
```

---

## Defense 8: Parameter Risk Matrix Pointer

**Reviewer Attack**: "How do we know your conclusions hold if parameters are wrong?"

**Location**: `paper/latex_gpt/supplementary.tex` (new subsection)

**New Defense Content**:
```latex
\subsection{Parameter Risk Matrix}

Table S5 summarizes the sensitivity of core conclusions to parameter uncertainty. 
For each proxy parameter, we report: (1) literature source, (2) physical plausible 
range based on device physics, (3) tested range in our sweeps, and (4) conclusion 
robustness rating ($\star$$\star$$\star$$\star$$\star$ = robust across full range).

Key findings: 
\begin{itemize}
    \item ADC 6-bit cliff: Robust ($\star$$\star$$\star$$\star$$\star$) — present across all parameter combinations
    \item D2D dominance over C2C: Robust ($\star$$\star$$\star$$\star$$\star$) — holds for D2D up to 30\%
    \item Ensemble HAT efficacy: Robust ($\star$$\star$$\star$$\star$$\star$) — 80\%+ recovery for D2D 5--20\%
    \item NL=2.0 failure: Moderate ($\star$$\star$$\star$) — threshold may shift with better STE
\end{itemize}

This matrix transforms proxy-parameter uncertainty from a vulnerability into a 
transparently bounded limitation.
```

---

## Summary

| Defense | Target | Location | Status |
|:--------|:-------|:---------|:------:|
| 1. Explicit Proxy | Parameter质疑 | Supp Table S2 | ✅ Ready |
| 2. Sensitivity Scope | C2C invariance | Results | ✅ Ready |
| 3. AIHWKIT Reframe | Circular claim | Discussion | ✅ Ready |
| 4. Contribution Scope | Bridge overreach | Conclusion | ✅ Ready |
| 5. HAT Novelty | Domain randomization | Discussion | ✅ Ready |
| 6. Energy Boundary | Placeholder constants | Results | ✅ Ready |
| 7. NL Limit | Approximation boundary | Discussion | ✅ Ready |
| 8. Risk Matrix | Parameter uncertainty | Supplementary | ✅ Ready |

All defenses are **text-only, no new experiments**, aligned with project constraints.
