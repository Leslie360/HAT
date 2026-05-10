# KIMI Round-J Residual Audit — 2026-04-19

Scope: verify the Round-J residual items `K-Q4`, `K-Q5`, `K-Q6`, `K-Q7`, and `K-Q9` against the current manuscript source.

## Result

All five residuals are present in source. No additional manuscript edit was required in this audit pass.

## Itemized check

### K-Q4 — abstract framing hedge
- Status: PASS
- Evidence:
  - `paper/latex_gpt/sections/00_abstract.tex:3`
    - "profile-driven first-order behavioral simulation framework"
  - `paper/latex_gpt/sections/00_abstract.tex:7`
    - "simulation-based materials-to-system decision aid"
- Assessment:
  - The abstract now frames the work as behavioral and decision-aid-oriented rather than predictive.

### K-Q5 — CrossSim 14.43 pp softening
- Status: PASS
- Evidence:
  - `paper/latex_gpt/sections/06_discussion.tex:47`
    - "a large qualitative divergence of 14.43 pp at n=3, preliminary"
  - `paper/latex_gpt/supplementary.tex:792`
    - protocol disclosure + confidence intervals + explicit throughput constraint note
- Assessment:
  - The CrossSim comparison is now hedged as preliminary and qualitative, with the subset protocol disclosed.

### K-Q6 — ImageNet / larger-scale scope boundary
- Status: PASS
- Evidence:
  - `paper/latex_gpt/sections/06_discussion.tex:47`
    - explicit statement that extrapolation to ImageNet-scale deployment is outside the present evidence base
  - `paper/latex_gpt/sections/00_abstract.tex:7`
    - edge-vision deployment framing retained
- Assessment:
  - The current text bounds the empirical scope and does not overclaim large-scale readiness.

### K-Q7 — forward pointer / formal-method reference in results
- Status: PASS
- Evidence:
  - `paper/latex_gpt/sections/05_results.tex:63`
    - "formally defined in Section~\ref{sec:methodology}, Eq.~\ref{eq:hat-ensemble}"
  - `paper/latex_gpt/sections/05_results.tex:41`
    - fresh-instance collapse sentence points forward to Eq.~`hat-ensemble`
- Assessment:
  - The results section now points readers back to the formal Ensemble HAT definition rather than relying on prose alone.

### K-Q9 — per-batch HAT one-liner / exploratory cadence caveat
- Status: PASS
- Evidence:
  - `paper/latex_gpt/sections/05_results.tex:63`
    - "88.41% (50-epoch training ablation), versus 87.18% (fixed) and 86.16% (per-batch)"
  - `paper/latex_gpt/supplementary.tex:480`
    - figure caption states this is an exploratory 50-epoch scan and not the final paper-locked estimate for every schedule
- Assessment:
  - The per-batch comparison remains, but it is now correctly scoped as an exploratory cadence scan.

## Overall conclusion

Round-J residuals are closed at the source-text level. Remaining gates are experimental/package-level (`CX-CA` full correlated-D2D harvest and downstream bundle refresh), not manuscript residuals from the Round-J text sweep.
