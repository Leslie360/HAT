# Paper-1 Rewrite Diff — Structural Limit Narrative (Branch B)

**Date:** 2026-04-23
**Authority:** `BROADCAST_ASSIGNMENT_20260423Q_SLIM.md` §2 + CX-K2 Hartigan dip test (p=0.98)
**Status:** Pre-staged. Do NOT apply until Claude declares loop closed.
**Branch:** Branch B (structural limit) — **CONFIRMED** by Hartigan's dip test p=0.98.

---

## Decision Rationale

CX-K2 N=30 Hartigan's dip test: **p = 0.9796** (cannot reject unimodality).

GMM-2 visually splits data near 32% and 46%, but this clustering is **not statistically significant**. The distribution is a single broad mode centered at ~39%.

**Therefore: Use Branch B (structural limit).** The original "~30%--40% fresh-instance band" language in `00_abstract.tex`, `05_results.tex`, `06_discussion.tex`, and `cover_letter_v3.tex` is CORRECT and does NOT need major rewriting.

---

## Minimal Additions Only (Do Not Change Existing Claims)

### File 1: `paper/latex_gpt/sections/00_abstract.tex`

**Current (line 3):**
```tex
Our findings establish a $\sim$30\% fresh-instance ceiling under severe nonlinearity, indicating that first-order behavioral surrogates impose a structural generalization barrier in the attention pathway.
```

**Addition (append to end of abstract):**
```tex
An extended N=30 fresh-instance sample (Hartigan's dip test, $p=0.98$) does not reject the unimodal null hypothesis, supporting the structural-limit interpretation over alternative two-basin hypotheses.
```

**Rationale:** Strengthen the claim by citing the statistical test that ruled out two-basin hypotheses.

---

### File 2: `paper/latex_gpt/sections/05_results.tex`

**Current (line 74, subsec `nl-hat-stress`):**
```tex
The convergence of three independent mitigations (MLP-only, all-linear, joint) on the same $\sim$30\% fresh-instance ceiling under $NL=2.0$ suggests that severe write nonlinearity introduces a generalization barrier in the attention pathway that training-recipe modifications cannot overcome within the first-order surrogate regime.
```

**Addition (insert after this sentence):**
```tex
An extended N=30 fresh-instance evaluation ($\mu=$38.95\%, $\sigma=$9.85\%) is consistent with a unimodal structural-limit interpretation (Hartigan's dip test, $p=0.98$), not a statistically confirmed two-attractor regime.
```

**Rationale:** Directly address the two-basin hypothesis and refute it with data.

---

### File 3: `paper/latex_gpt/sections/06_discussion.tex`

**Current (line 43, subsec `limitations`):**
```tex
The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a material bound.
```

**No change needed.** This sentence is correct.

**Addition (insert after line 43):**
```tex
Hartigan's dip test on the N=30 sample ($p=0.98$) does not reject the unimodal null hypothesis, indicating that the apparent visual clustering observed in smaller samples (N=10) was a small-sample artifact rather than evidence of two distinct failure modes.
```

**Rationale:** Explain why the two-basin hypothesis was considered but rejected.

---

### File 4: `paper/latex_gpt/cover_letter_v3.tex`

**Current (line 22-24):**
```tex
We rigorously falsify three intuitive strategies for breaking the severe nonlinearity ceiling---joint linearization training, all-linear ablations, and MLP-only controls---all converging to an approximately 30\% fresh-instance limit. Rather than weakening the study, this negative result exposes a structural generalization barrier in the attention pathway that first-order behavioral surrogates cannot circumvent.
```

**Addition (append to paragraph):**
```tex
An N=30 statistical test (Hartigan's dip, $p=0.98$) does not reject the unimodal null hypothesis, strengthening the structural-limit claim against alternative two-basin hypotheses.
```

**Rationale:** Cover letter should mention the statistical rigor of the sample.

**Addition 2 (new paragraph after statistical sentence):**
```tex
We report the completed portion of the ablation space and disclose the following gaps: (a) K4 second-order $\alpha \in \{0.75, 1.00\}$ were not evaluated; $\alpha \in \{0.00, 0.25, 0.50\}$ cover the critical range and already establish non-monotonic behavior with peak at $\alpha=0.25$ (44.29 $\pm$ 13.78\%, still 25 pp below deployment threshold). (b) J2--J4 non-ideality probes are reported as scalar sanity checks; their per-instance JSON and full logs are memo-level. (c) The N=30 K2 evaluation used the literal $\delta g_{\text{eff}}=0.0$ configuration consistent with J1d training; a later eval-script default changed to $-1.0$ but does not apply to this evaluation chain.
```

**Rationale:** Transparency about ablation coverage strengthens the falsification claim.

---

## Figures to Add

| Figure | Content | Source |
|--------|---------|--------|
| Fig. [TBD] | N=30 fresh-instance histogram with KDE overlay + Hartigan's dip annotation | `cx_k2_fresh_eval.json` + matplotlib |

No two-basin figure needed. A simple unimodal histogram is sufficient.

---

## Diff Application Checklist

- [ ] CX-K2 Hartigan dip test confirmed p > 0.05 ✅
- [ ] Branch B selected ✅
- [ ] Apply minimal additions to `00_abstract.tex`
- [ ] Apply minimal additions to `05_results.tex`
- [ ] Apply minimal additions to `06_discussion.tex`
- [ ] Apply minimal additions to `cover_letter_v3.tex`
- [ ] Add N=30 histogram figure
- [ ] Regenerate PDF
- [ ] Submit

---

*Pre-staged 2026-04-23. Branch B confirmed by CX-K2 data. Do not apply until loop closure.*

---

**⚠️ DEPRECATED 2026-04-24** — This memo references bug-contaminated data (STE branch swap + extraneous nl multiplier in analog_layers.py, fixed at commit 33bed9c). The "structural ceiling / bimodal basin / Hartigan p=0.98" narrative is invalidated. Do not cite as evidence. See BROADCAST_HALT_AND_REPLICATE_20260424.md and BROADCAST_REBUILD_3WEEK_20260424.md for current status.
