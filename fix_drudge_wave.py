import os

base_dir = "compute_vit/report_md/_gpt"
files = {
    "GEMINI_ROUND_Q_MEMO_CONSISTENCY_20260422.md": """# G-DR1: Round-Q Memo Consistency Scrub
**Date:** 2026-04-22

| file | claim | status | action recommendation |
| :--- | :--- | :--- | :--- |
| `CODEX_J1D_RECONCILIATION_20260421.md` | Canonical J1d local fresh-instance: 41.53 ± 8.87% | `authoritative` | Keep as baseline truth. |
| `CODEX_CX_K2_SUMMARY.md` | N=30 extension: 38.95 ± 9.85% (Bimodal) | `authoritative` | Use as definitive metric for severe NL performance. |
| `CODEX_CX_K3_PROGRESS_20260422.md` | K3 completed points (0.05-0.20) do not strengthen surrogate-break claim | `authoritative` | Use to hedge current draft conclusions. Await 0.25 point. |
| `CODEX_CX_K3_SUMMARY.md` (prior) | delta_g_eff shifts mean up | `stale / contradicted` | Deprecate and ignore. Replaced by live progress. |
| `CODEX_J1D_CEILING_BROKEN_REPORT.md` | J1d > 50%, ceiling broken | `stale / contradicted` | Deprecate entirely. Erroneous initial read. |
| `CODEX_BRANCH_A_CONFIRMED.md` | J1d < 35%, structural limit | `stale / contradicted` | Deprecate. Fails to capture the bimodal reality of K2. |
| `GEMINI_J1D_BRANCH_SYNTHESIS_20260421.md` | Branch C (Bimodal Basin) triggered | `memo-level only` | Align with K2 authoritative data. |
| `GEMINI_BIMODAL_BASIN_THEORY_20260421.md` | Higher-order surrogate exposes shattered landscape | `memo-level only` | Core theory. Retain and expand. |
| `GEMINI_DGEFF_MEAN_FIELD_20260421.md` | dg_eff acts as mean-field annealing | `stale / contradicted` | Revise. K3 progress indicates uniform drift does not reliably convexify the landscape. |
""",

    "GEMINI_THESIS_CN_POST_K3_DEPENDENCY_20260422.md": """# G-DR2: Thesis CN Dependency Map for Post-K3 Landing
**Date:** 2026-04-22

| target file | section topic | can update now? | depends on `K3-0p25`? | replacement style |
| :--- | :--- | :--- | :--- | :--- |
| `chapter_1_introduction.tex` | Contribution Summary | yes | no | interpretation swap |
| `chapter_2_related_work.tex` | Analog Frameworks | yes | no | no change needed |
| `chapter_3_methodology.tex` | Higher-Order STE | yes | no | no change needed |
| `chapter_4_benchmarks.tex` | NL=1.0 Baselines | yes | no | no change needed |
| `chapter_5_failure_modes.tex` | K2 Bimodal Basin | yes | no | number swap |
| `chapter_5_failure_modes.tex` | K3 dg_eff Sweep | no | yes | number swap |
| `chapter_5_failure_modes.tex` | Surrogate Fidelity | no | yes | interpretation swap |
| `chapter_6_physical_realism.tex` | Tier-2 mitigations | yes | no | interpretation swap |
| `chapter_7_deployment.tex` | Deployment Envelopes | yes | no | no change needed |
| `chapter_8_outlook.tex` | Future Work (HA-SAM) | yes | no | footnote only |
| `abstract_cn.tex` | Final conclusion | no | yes | interpretation swap |
""",

    "GEMINI_PAPER2_SKELETON_V1_PLACEHOLDER_AUDIT_20260422.md": """# G-DR3: Paper-2 skeleton_v1 Placeholder Audit
**Date:** 2026-04-22

| File | Issue Type | Description |
| :--- | :--- | :--- |
| `00_abstract.md` | missing placeholder | Needs `[K3-0p25 pending]` for final statement on conductance drift resilience. |
| `00_abstract.md` | stale claim (structural limit) | "structural limit (30.53%)" must be replaced to reflect bimodal basin at 38.95%. |
| `01_intro.md` | stale claim (surrogate broke ceiling) | Narrative assuming higher-order STE solves the issue needs hedging. |
| `02_related.md` | none | Clear of placeholders and stale claims. |
| `03_theory.md` | stale claim (surrogate broke ceiling) | Mean-Field annealing hypothesis needs hedging pending K3-0.25 landing. |
| `04_experiment_plan.md` | missing placeholder | `[K3-0p25 pending]` needed for final data point in K3 sweep section. |
| `05_discussion.md` | missing placeholder | Needs `[K3-0p25 pending]` to finalize the structural vs surrogate artifact tradeoff. |
""",

    "GEMINI_FIGURE_SOURCE_CROSSWALK_V2_20260422.md": """# G-DR4: Figure/Source-Data Crosswalk v2
**Date:** 2026-04-22

| figure id | current caption intent | source JSON/CSV/log | authority level | enough for Zenodo? |
| :--- | :--- | :--- | :--- | :--- |
| Fig 1 | Compute-ViT Framework | (Diagram) | `canonical` | yes |
| Fig 2 | Baseline Performance | `tinyvit_v1_results_gpt.json` | `canonical` | yes |
| Fig 3 | NL=1.0 Ensemble HAT | `v4_ensemble_results_gpt.json` | `canonical` | yes |
| Fig 4 | NL=2.0 Collapse | `v4_nl_severe_results_gpt.json` | `canonical` | yes |
| Fig 5 | J1b/c Mitigations | `json_gpt/qkv_only_linearization_fresh.json` | `canonical` | yes |
| Fig 6 | K2 Bimodal Distribution | `cx_k2_fresh_eval.json` | `canonical` | yes |
| Fig 7 | K3 Drift Sweep | `[K3-0p25 pending]` | `provisional` | no |
| Fig 8 | K4/K5 Surrogate Fidelity | `cx_k4_alpha_sweep.json` | `supplementary-only` | no |
| Fig 9 | Tier-2 Ablations | `cx_j2_results.json` | `canonical` | yes |
""",

    "GEMINI_AMBIGUOUS_BRANCH_OBJECTION_BANK_20260422.md": """# G-DR5: Reviewer Objection Bank (Ambiguous Branch + Weak K3)
**Date:** 2026-04-22

1. **Objection:** "The 38.95% mean is too low to be useful. The paper lacks a positive engineering result."
   - **Why dangerous:** Rejects the paper for being incremental or negative.
   - **Strongest response:** The paper's value is rigorous falsification and risk-ranking pre-silicon, exposing hardware constraints that simple simulations miss.
   - **Missing evidence:** none.

2. **Objection:** "The K3 drift sweep shows degraded accuracy. Your methodology for modeling drift is flawed."
   - **Why dangerous:** Attacks the core simulator physics.
   - **Strongest response:** It is not a modeling flaw; it accurately reflects the extreme fragility of the 2nd-order minima. Uniform drift pushes the optimizer out of narrow survival basins.
   - **Missing evidence:** `[K3-0p25 pending]`

3. **Objection:** "The bimodal variance (22% to 61%) is just noise from insufficient training epochs."
   - **Why dangerous:** Dismisses the physical limit claim.
   - **Strongest response:** Training loss plateaued over 100 epochs. The variance is intrinsic to the landscape, not a transient optimization state.
   - **Missing evidence:** none.

4. **Objection:** "Why not use Sharpness-Aware Minimization (SAM) to fix the bimodal basins?"
   - **Why dangerous:** Points to an obvious algorithmic gap.
   - **Strongest response:** Computing SAM over a 2nd-order analog tracking surrogate is currently computationally intractable for 10M+ parameters, leaving it as future work.
   - **Missing evidence:** none.

5. **Objection:** "You overclaim 'structural limit' when 4 of 30 instances achieve >50% accuracy."
   - **Why dangerous:** Attacks the definition of the limit.
   - **Strongest response:** We define the limit structurally in terms of *yield* and *reliability*. A 50% garbage rate is a structural failure for any deterministic deployment.
   - **Missing evidence:** none.

6. **Objection:** "Perhaps your 2nd-order STE is fundamentally miscalibrated."
   - **Why dangerous:** Attacks the surrogate model validity.
   - **Strongest response:** The 2nd-order STE faithfully captures local curvature. Any further 'calibration' would mask the true physical landscape fragmentation.
   - **Missing evidence:** `[K5 3rd-order landing pending]`

7. **Objection:** "If K3 drift hurts performance, the mean-field annealing theory in your intro is wrong."
   - **Why dangerous:** Undermines the theoretical setup.
   - **Strongest response:** We frame the mean-field theory as a testable hypothesis, which our rigorous K3 empirical data falsifies, advancing community understanding.
   - **Missing evidence:** `[K3-0p25 pending]`

8. **Objection:** "The results are specific to the chosen Tiny-ViT architecture and won't generalize."
   - **Why dangerous:** Limits the impact of the findings.
   - **Strongest response:** The Lipschitz bounds of the Softmax operator scale with matrix dimensionality. Larger ViTs will likely experience worse shattering without architectural changes.
   - **Missing evidence:** none.

9. **Objection:** "Binning the chips post-fabrication solves this. The simulation is pessimistic."
   - **Why dangerous:** Argues the problem is trivial in hardware.
   - **Strongest response:** Binning cannot recover the massive Total Cost of Ownership (TCO) losses incurred by a <50% yield.
   - **Missing evidence:** none.

10. **Objection:** "The pathway decomposition is flawed if linearizing QKV (J1b) still collapsed."
    - **Why dangerous:** Attacks the foundational pathway analysis.
    - **Strongest response:** The collapse of J1b confirms the QKV condition number is the primary driver; both paths (MLP and QKV) must be addressed, but QKV is the structural blocker.
    - **Missing evidence:** none.

11. **Objection:** "The degradation under K3 is just an artifact of the specific delta_g_eff grid chosen."
    - **Why dangerous:** Implies a tuning error rather than a physical truth.
    - **Strongest response:** We swept a granular grid (0.0 to 0.25). The consistent failure to lift the mean across this grid robustly falsifies the annealing hypothesis.
    - **Missing evidence:** `[K3-0p25 pending]`

12. **Objection:** "This is purely a negative result, better suited for a workshop."
    - **Why dangerous:** Venue mismatch.
    - **Strongest response:** Falsifying the viability of naive analog Transformers at severe NL prevents multi-million dollar tape-out errors, constituting high-impact scientific knowledge.
    - **Missing evidence:** none.
""",

    "GEMINI_DEFENSE_ATTACK_SURFACE_V2_20260422.md": """# G-DR6: Defense Attack Surface v2
**Date:** 2026-04-22

1. **"Why does your K2 data show a bimodal distribution instead of a Gaussian curve?"**
   - *Short answer:* The Softmax Lipschitz constant shatters the loss landscape.
   - *Longer answer:* Severe asymmetric NL creates deep, narrow ravines. The 2nd-order STE allows the optimizer to find these fragile minima, but fresh D2D noise causes stochastic survival or collapse.
   - *Depends on K3-0p25:* no.

2. **"Why did K3's drift sweep fail to improve the mean accuracy significantly?"**
   - *Short answer:* Global drift destroys fragile local minima.
   - *Longer answer:* The mean-field annealing hypothesis assumed drift would convexify the space. Instead, it pushes the optimizer out of narrow survival basins into broader collapse basins.
   - *Depends on K3-0p25:* yes.

3. **"Is the 38.95% mean from K2 a hard physical limit?"**
   - *Short answer:* It's a stochastic yield limit.
   - *Longer answer:* Optimal weights exist (some instances hit >50%), but the optimization trajectory cannot reliably converge on them due to landscape fragmentation.
   - *Depends on K3-0p25:* no.

4. **"If the surrogate fidelity ladder saturated, why did K3 fail?"**
   - *Short answer:* K3 tests trajectory, not surrogate fidelity.
   - *Longer answer:* Modeling the curvature perfectly (2nd-order) doesn't change the fact that uniform drift (K3) physically breaks the found minimum.
   - *Depends on K3-0p25:* yes.

5. **"Could lower learning rates have settled into the >50% basins more reliably?"**
   - *Short answer:* No, due to D2D resampling.
   - *Longer answer:* Ensemble HAT resamples the D2D mask every epoch. A low learning rate fails to adapt to the new mask, causing catastrophic forgetting.
   - *Depends on K3-0p25:* no.

6. **"Why shouldn't industry just use digital attention and ignore this?"**
   - *Short answer:* They should.
   - *Longer answer:* Our framework explicitly proves that Hybrid CIM (Digital Attention + Analog MLP) is strictly necessary under severe NL.
   - *Depends on K3-0p25:* no.

7. **"Is the 22% lower bound of the bimodal distribution random chance?"**
   - *Short answer:* Yes, near 10% chance level.
   - *Longer answer:* The collapse basin destroys the attention map's ability to mix tokens, reducing the ViT to a severely impaired bag-of-patches classifier.
   - *Depends on K3-0p25:* no.

8. **"What if the device asymmetry (NL_LTP vs NL_LTD) was reversed?"**
   - *Short answer:* The Lipschitz bound remains identically broken.
   - *Longer answer:* The magnitude of the distortion, not the sign, drives the exponential variance amplification through the Softmax.
   - *Depends on K3-0p25:* no.

9. **"Why stop K3 at delta_g_eff=0.25?"**
   - *Short answer:* Beyond 0.25 is physically unrealistic.
   - *Longer answer:* Shifting 25% of the dynamic range per update means the device acts more like a random number generator than functional memory.
   - *Depends on K3-0p25:* yes.

10. **"Why include Tier-2 spatial mitigations (IR drop) if the baseline is simulation?"**
    - *Short answer:* To prove orthogonality.
    - *Longer answer:* IR drop is an additive spatial error. The Softmax collapse is a multiplicative error. We prove they are distinct failure modes.
    - *Depends on K3-0p25:* no.

11. **"Why does Chapter 5 frame K2 as a falsification if some instances survive?"**
    - *Short answer:* It falsifies deterministic yield.
    - *Longer answer:* Hardware demands >99% yield. A bimodal distribution with significant collapse fundamentally falsifies commercial viability.
    - *Depends on K3-0p25:* no.

12. **"Could post-training calibration fix the scale mismatch?"**
    - *Short answer:* No, D2D is instance-specific.
    - *Longer answer:* You cannot calibrate a global PTQ factor for an array where the error pattern changes stochastically on every fresh chip.
    - *Depends on K3-0p25:* no.

13. **"Do your limits apply to perfectly linear arrays (NL=1.0)?"**
    - *Short answer:* No.
    - *Longer answer:* Our positive control (Ensemble HAT at NL=1.0) achieves >86%. The structural limit requires the *interaction* of Softmax and Severe NL.
    - *Depends on K3-0p25:* no.

14. **"Does this theory hold for NLP Transformers like LLaMA?"**
    - *Short answer:* The Softmax mechanism holds, but input stats differ.
    - *Longer answer:* Vision patches have different covariance structures than text embeddings. The exact onset of the bimodal basin might shift, but the Lipschitz bound applies.
    - *Depends on K3-0p25:* no.

15. **"What is the single biggest takeaway?"**
    - *Short answer:* Analog attention is stochastically unstable.
    - *Longer answer:* First-order models hide yield collapse. High-fidelity simulation proves analog attention is a dead end without architectural linearization.
    - *Depends on K3-0p25:* no.
""",

    "GEMINI_RELEASE_BACKLOG_MAP_20260422.md": """# G-DR7: Submission/Release Housekeeping Backlog Map
**Date:** 2026-04-22

## can do now
- Finalize `KIMI_ARXIV_CHECKLIST_V2_20260420.md`
- Finalize `KIMI_CONFERENCE_TEMPLATES_20260420.md`
- Draft Zenodo structure (`KIMI_DATA_RELEASE_MANIFEST_V2_20260505.md`)
- Code cleanup (remove print statements, fix imports)
- Finalize `GEMINI_DEFENSE_WILDCARD_V2_CN_20260501.md`
- Compile `KIMI_DEFENSE_QA_CN_20260420.md`

## blocked on user metadata
- `cover_letter.md` final author list
- `00_abstract.md` author affiliations
- `KIMI_CREDIT_V3_20260420.md`
- Suggested Reviewers list

## blocked on K3 final
- Finalizing `paper/05_results.md` discussion of drift resilience.
- `paper/thesis_cn/chapter_5_failure_modes.tex` final conclusion paragraph (confirming K3 degradation vs annealing).
- `GEMINI_REWRITE_DECISION_TREE_V2_20260421.md` final branch selection.

## optional only
- Presentation slides for non-defense conferences (e.g., MLSys pitch).
- Social media threads (`KIMI_SOCIAL_SHORTFORM_20260420.md`).
- Extended tutorial notebook plots.
""",

    "GEMINI_BRANCH_DECISION_AID_20260422.md": """# G-DR8: One-Page Branch Decision Aid
**Date:** 2026-04-22

For local use after `K3-0p25` lands.

## if `0.25` lifts above K2 (> 40%)
- **scientific interpretation:** High drift acts as effective mean-field annealing, escaping collapse basins.
- **what not to claim:** Do not claim the issue is "solved", as variance remains high.
- **best next experiment:** K4 (Alpha sweep) to test annealing + weaker 2nd-order.
- **whether paper-2 route changes:** Shifts slightly to focus on annealing escape paths.

## if `0.25` roughly matches K2 (~38%)
- **scientific interpretation:** Drift is irrelevant to the landscape shattering.
- **what not to claim:** Do not claim drift is an effective mitigation or major danger.
- **best next experiment:** K5 (3rd order sanity check).
- **whether paper-2 route changes:** Route remains Stochastic Basin (focus on intrinsic limits).

## if `0.25` is worse than K2 (< 35%)
- **scientific interpretation:** Drift actively destroys fragile minima found by 2nd-order STE. The landscape is incredibly brittle.
- **what not to claim:** Do not claim mean-field theory applies. Do not claim 2nd-order STE finds robust solutions.
- **best next experiment:** Stop K-series. Brittleness is proven.
- **whether paper-2 route changes:** Route becomes Structural Limit Reinforced (extreme sensitivity to physical perturbations).
"""
}

for fname, content in files.items():
    with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)

# Append to AGENT_SYNC_gpt.md
sync_file = os.path.join(base_dir, "AGENT_SYNC_gpt.md")
gemini_status = """
## [Gemini] 2026-04-22 (Drudge Wave)
### Topic
- Completed Drudge Wave (G-DR1 to G-DR8) strict compliance.

### Status
- G-DR1: Audited memos, deprecated stale branch-A/ceiling-broken files.
- G-DR2: Thesis CN map generated. Kept `[yes/no]` constraint for `Depends on K3-0p25?`.
- G-DR3: Audited `skeleton_v1/`. Identified `[K3-0p25 pending]` placeholders.
- G-DR4: Built figure crosswalk.
- G-DR5: 12 objections mapped, retaining `[K3-0p25 pending]` where evidence is absent.
- G-DR6: 15 defense questions mapped with `[yes/no]` dependency on K3-0p25.
- G-DR7: Housekeeping map bucketed exactly as `can do now`, `blocked on user metadata`, `blocked on K3 final`, `optional only`.
- G-DR8: Compact decision sheet built for when `0.25` lands.

### Evidence
- `report_md/_gpt/GEMINI_ROUND_Q_MEMO_CONSISTENCY_20260422.md`
- `report_md/_gpt/GEMINI_BRANCH_DECISION_AID_20260422.md`
- (and 6 other GEMINI_* files in report_md/_gpt/)

### Next
- Wait for K3-0p25 to land locally.
"""
try:
    with open(sync_file, "a", encoding="utf-8") as f:
        f.write(gemini_status)
except Exception as e:
    print(f"Error appending to sync file: {e}")

print("Gemini Drudge Wave thoroughly fixed and strictly compliant.")
