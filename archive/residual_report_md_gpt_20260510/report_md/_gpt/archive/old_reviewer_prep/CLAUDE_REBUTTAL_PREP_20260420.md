# CLAUDE Rebuttal Prep — 2026-04-20
## Top-5 Un-Pre-empted Reviewer Objections

**Sources audited:**
- `RESPONSE_LETTER_FINAL_20260419.md` (R1–R11)
- `KIMI_RED_TEAM_AUDIT_20260419.md`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/08_appendix.tex`
- `paper/latex_gpt/supplementary.tex`
- Internal evidence: `sobol_sensitivity.json`, `STATISTICAL_VALIDATION_SUMMARY.md`, `OPEN_SOURCE_READINESS_20260417.md`

---

## 1. No fabricated-array or hardware-in-the-loop validation of the simulator

**Objection:** The entire study is simulation-only; no real organic crossbar array measurements are used to validate whether the simulator predictions match physical reality.

**Where it would likely come from:** §3.5 (measurement-to-simulator pipeline), §5.9 (case study: "calibrated directly from literature"), §6.6/§6.7 (future work). A reviewer will notice that every "device profile" is a literature proxy, and every accuracy number is simulator-output.

**Pre-emptive answer outline:**
- Acknowledge openly that hardware correlation is the critical next step; §6.6 already states this ("close the loop between laboratory characterization and the simulator").
- Emphasize that the framework was architected so literature priors and measured profiles enter through the *same* JSON parameter interface (§3.5, Table `tab:measurement-mapping`), which means the present study is intentionally a simulation baseline that preserves a clean pathway for later recalibration without code changes.
- Cite the bounded cross-framework sanity check with AIHWKIT (§6.6) as at least qualitative trend validation that the simulator produces degradation patterns consistent with a mature inorganic toolkit under matched assumptions.

**Manuscript or response-only?**
- **Add to manuscript NOW.** One sentence in §6.6 or §6.7 should explicitly state that hardware-in-the-loop validation is the highest-priority next step and that the present results are intentionally a simulation baseline under literature priors. This frames the limitation proactively rather than letting a reviewer discover it as a surprise gap.

---

## 2. No analog-digital layer mapping ablation; the 87.7 % split is asserted but not justified

**Objection:** The hybrid mapping rule is fixed by an internal "project handbook" with no exploration of alternative splits. The conclusion that "digital attention creates an analog ceiling" (§3.1, §6.4) assumes a specific mapping that was never varied.

**Where it would likely come from:** §3.1, lines 8–12: "Following the mapping rules fixed in the project handbook, analog execution is assigned to..." A reviewer will ask: what if attention projections were digital and MLPs analog? What if the split were 50/50?

**Pre-emptive answer outline:**
- The mapping logic is grounded in array-utilization principles that are standard in the CIM literature: dense static weights map naturally to crossbars, while dynamic token-dependent operations (QKᵀ, AV, softmax) cannot be pre-programmed into non-volatile arrays.
- The framework already supports arbitrary layer-wise analog/digital assignment via configuration flags, so mapping ablations are future work that requires no structural code changes.
- The energy model is modular; any remapping would update the analog/digital energy fractions automatically, so the "analog ceiling" concept (digital attention dominating cost) is robust to the exact split because attention operations are *inherently* dynamic regardless of where static weights sit.

**Manuscript or response-only?**
- **Add to manuscript NOW.** Insert one sentence in §3.1 acknowledging that the mapping is a design choice motivated by array-utilization principles and that layer-wise mapping ablations are deferred to future work. This prevents the reviewer from interpreting the fixed split as an unjustified assumption.

---

## 3. The 10.00 % chance-level collapse could be a software bug or implementation artifact

**Objection:** The exactly 10.00 % figure (precise chance level for CIFAR-10) is suspiciously clean. R5 rules out AMP artifacts and shows determinism, but no evidence addresses broader code-correctness concerns or independent verification.

**Where it would likely come from:** §5.6 ("collapses to chance-level performance, 10.00 %"), §5.8 (state-dependent noise collapse to 10.0 %), §5.9 (case study collapse to 10.00 %), and the supplementary multi-seed note. A hostile reviewer will push on whether the collapse is a simulator bug rather than a real physical failure mode.

**Pre-emptive answer outline:**
- The determinism across 10 fresh instances × 5 MC evaluations (10.00 ± 0.00 %, R5) and the *differential* architecture behavior (ConvNeXt retains partial functionality under transfer, Tiny-ViT collapses) argues against a universal code bug.
- The structural attention-side collapse is independently confirmed by group-wise linearization ablations: both QKV-linear and projection-linear lanes collapse structurally regardless of exact NL value (Supplementary Table `tab:supp-nl-ablation`), which localizes the failure to the attention mechanism rather than a global coding error.
- The code has passed 51 unit tests and a full `py_compile` pass (`OPEN_SOURCE_READINESS_20260417.md`), and the public smoke-test script reproduces the canonical forward path. A full open-source release is prepared for independent verification.

**Manuscript or response-only?**
- **Response-only.** Adding "this is not a bug" to the manuscript would read as defensive. If raised, the response should cite the multi-architecture differential behavior and the group-wise ablations as independent evidence. The open-source readiness can be mentioned in the response cover letter.

---

## 4. Training variance across random initialization seeds is under-reported; the multi-seed campaign is incomplete

**Objection:** The appendix explicitly admits "the full multi-seed campaign is still being accumulated in the current revision window" (§A.1). Only one seed-42 rerun is shown. For a paper claiming robustness, single-seed training is weak evidence, and the reported ± values reflect only C2C evaluation noise, not training variance.

**Where it would likely come from:** §A.1 (Appendix): "Because the full multi-seed campaign is still being accumulated..." Table in §A.1 shows only a single rerun (88.45 % best, 87.64 ± 0.48 % MC).

**Pre-emptive answer outline:**
- The seed-42 rerun is consistent with the canonical result (within <1 pp), and the Monte Carlo evaluation variance (±0.48 %) is tighter than the cross-instance Ensemble HAT variance (±1.54 %), suggesting that training-seed variance is not the dominant source of uncertainty in this regime.
- The fresh-instance transfer protocol (10 instances × 5 MC) provides stronger evidence of generalization than training-seed variance would, because it explicitly tests robustness to the largest source of variance in analog deployment: manufacturing mismatch.
- The full multi-seed campaign is actively running and will be included in the next revision; the present appendix transparently discloses the interim state.

**Manuscript or response-only?**
- **Response-only.** The appendix already transparently discloses the incomplete multi-seed campaign. Drawing more attention to it in the main text would be counter-productive. If asked, respond with the seed-42 consistency argument and emphasize that cross-instance variance is the harder test.

---

## 5. The title's "Risk-Aware Deployment" claim lacks formal risk metrics or decision-theoretic support

**Objection:** The manuscript (title: *Compute-ViT: A Prospective Simulation Framework for Risk-Aware Deployment...*) uses accuracy as the sole evaluation metric. There is no formal risk quantification—no worst-case guarantees, probability-of-failure, CVaR, or Bayesian decision framework. "Risk-aware" in the title promises more than the paper delivers.

**Where it would likely come from:** Title, abstract (if present), and the complete absence of "risk-aware," "risk ranking," or formal risk terminology in §1–§6. The word "risk" appears only twice in the body ("severe risk for analog foundation models" and "substantial risks"), both as colloquial usage, not methodology.

**Pre-emptive answer outline:**
- "Risk-aware" in the present context means *structured identification and ranking of hardware-induced failure modes* (hardware-instance overfitting, ADC cliffs, retention drift, nonlinear-write boundaries) prior to fabrication closure, not portfolio-theoretic optimization.
- The framework outputs a ranked risk map: which device profiles and operating regimes produce which accuracy deciles. That is exactly what materials scientists and system designers need for go/no-go decisions before tape-out.
- We can tighten the abstract or §1 to make this interpretation explicit—e.g., replacing "risk-aware" with "risk-ranked" or adding a clarifying clause—so the title claim is scoped to the pre-deployment risk-ranking workflow rather than formal decision theory.

**Manuscript or response-only?**
- **Add to manuscript NOW.** Insert one clarifying sentence in §1 (or the abstract, if accessible) defining "risk-aware deployment" as "structured identification and ranking of hardware-induced failure modes prior to fabrication closure." This scopes the claim proactively and prevents a reviewer from interpreting the title as overselling.

---

## Quick-Reference: Why these five?

| # | Objection | Damage if un-prepared | Already in R1–R11? | Evidence strength |
|---|-----------|----------------------|-------------------|-------------------|
| 1 | No hardware validation | **Critical** — undermines entire simulator credibility | No | High (literature-only profiles throughout) |
| 2 | No mapping ablation | **High** — methodological gap in core architecture claim | No | High (§3.1 cites "project handbook" with no ablation) |
| 3 | 10.00 % = possible bug | **High** — could discredit central collapse finding | No (R5 only rules out AMP) | Medium-high (exact chance-level is suspicious) |
| 4 | Incomplete multi-seed | **Medium** — weakens robustness claims | No | High (appendix explicitly admits incompleteness) |
| 5 | "Risk-aware" title oversell | **Medium** — scope/audience objection, easy to fix | No | High (term absent from body) |

---

*Generated: 2026-04-20*
*Verified against: R1–R11 coverage matrix, manuscript §3–§6 + appendix, internal JSON/metadata audits.*
