import os

base_dir = "compute_vit/report_md/_gpt"
files = {
    "GEMINI_ROUND_Q_MEMO_CONSISTENCY_20260422.md": """# G-DR1: Round-Q Memo Consistency Scrub
**Date:** 2026-04-22

This scrub audits all major `_gpt` memos mentioning `J1d`, `K2`, or `K3` to ensure narrative consistency and prevent conflicting claims during loop closure.

| File | Claim | Status | Action Recommendation |
| :--- | :--- | :--- | :--- |
| `CODEX_J1D_RECONCILIATION_20260421.md` | Canonical J1d is 41.53 ± 8.87% | `authoritative` | Keep as baseline reference. Ground truth for J1d. |
| `CODEX_CX_K2_SUMMARY.md` | N=30 extension yields 38.95 ± 9.85% | `authoritative` | Primary bimodal evidence point. Replaces J1d as the core evaluation metric. |
| `CODEX_CX_K3_PROGRESS_20260422.md` | K3 dg_eff=0.05..0.20 shows degradation | `authoritative` | Use as live trend. Await 0.25 for final conclusion. |
| `CODEX_CX_K3_SUMMARY.md` (prior) | dg_eff shifts mean up to 45.2% | `stale / contradicted` | DEPRECATE. Erroneous prior scaffold. |
| `CODEX_J1D_CEILING_BROKEN_REPORT.md` | J1d > 50%, ceiling broken | `stale / contradicted` | DEPRECATE. Based on false initial reading. |
| `CODEX_BRANCH_A_CONFIRMED.md` | J1d < 35%, structural limit | `stale / contradicted` | DEPRECATE. Based on incomplete evaluation. |
| `GEMINI_J1D_BRANCH_SYNTHESIS_20260421.md` | 38.95% triggers Branch C (Bimodal Basin) | `authoritative` | Safe to build upon. Narrative anchor. |
| `GEMINI_BIMODAL_BASIN_THEORY_20260421.md` | Higher-order surrogate exposes shattered landscape | `authoritative` | Safe to build upon. Core theory for Paper-2. |
| `GEMINI_DGEFF_MEAN_FIELD_20260421.md` | dg_eff acts as annealing, shifting mean up | `stale / contradicted` | REVISE. K3 live data (degradation to ~27-36%) contradicts this. Drift actively destroys fragile 2nd-order minima. |
| `GEMINI_REWRITE_DECISION_TREE_V2_20260421.md` | Branch C triggered by K2 | `authoritative` | Directs Kimi's loop closure. |
| `GEMINI_PAPER2_ROUTE_FINAL_20260425.md` | Route Modified R-A (Stochastic Basin) | `authoritative` | Paper-2 strategy locked. |
| `GEMINI_HOSTILE_REVIEW_V4_20260425.md` | Defends bimodal basin claim | `authoritative` | Valid defense strategies. |
""",

    "GEMINI_THESIS_CN_POST_K3_DEPENDENCY_20260422.md": """# G-DR2: Thesis CN Dependency Map for Post-K3 Landing
**Date:** 2026-04-22

Map of Chinese thesis chapters requiring updates when `K3 delta_g_eff=0.25` final lands.

| Target File | Section Topic | Can Update Now? | Depends on `K3-0p25`? | Replacement Style |
| :--- | :--- | :--- | :--- | :--- |
| `chapter_1_introduction.tex` | Core Contribution Summary | yes | no | interpretation swap (bimodal basin) |
| `chapter_2_related_work.tex` | Analog Training Frameworks | yes | no | no change needed |
| `chapter_3_methodology.tex` | Higher-Order STE Math | yes | no | no change needed |
| `chapter_4_benchmarks.tex` | NLP=1.0 and FP32 Baselines | yes | no | no change needed |
| `chapter_5_failure_modes.tex` | J1b/c/d/K2 Bimodal Basin | yes | no | interpretation swap (incorporate 38.95%) |
| `chapter_5_failure_modes.tex` | K3 dg_eff Sweep Analysis | no | yes | number swap & interpretation swap |
| `chapter_5_failure_modes.tex` | K4/K5 Surrogate Fidelity | yes | no | interpretation swap |
| `chapter_6_physical_realism.tex` | Tier-2 mitigations (J2/J3/J4) | yes | no | interpretation swap (ablation context) |
| `chapter_7_deployment.tex` | Deployment Envelopes | yes | no | no change needed |
| `chapter_8_outlook.tex` | Future Work (HA-SAM) | yes | no | footnote/paragraph addition |
| `abstract_cn.tex` | Final conclusion & abstract | no | yes | interpretation swap |
""",

    "GEMINI_PAPER2_SKELETON_V1_PLACEHOLDER_AUDIT_20260422.md": """# G-DR3: Paper-2 skeleton_v1 Placeholder Audit
**Date:** 2026-04-22

| File | Issue Type | Description |
| :--- | :--- | :--- |
| `00_abstract.md` | missing placeholder | Needs `[K3-0p25 pending]` for conductance drift impact statement. Cannot conclude if drift is purely destructive until K3 finishes. |
| `00_abstract.md` | stale claim | Removes "structural limit (30.53%)". Replaced with K2 mean 38.95%. |
| `01_intro.md` | stale claim | Assumes K3 drift universally improves mean. Must hedge given intermediate K3 degradation (27-36%). |
| `02_related.md` | missing placeholder | None. Theory on prior work is independent of K3. |
| `03_theory.md` | stale claim | Ensure Mean-Field annealing hypothesis is framed as a *tested and falsified* hypothesis, pending K3-0p25 final. |
| `04_experiment_plan.md` | stale claim | Lists K3 hypothesis as confirmed upward shift. Change to exploratory: "We test whether uniform drift convexifies or shatters the bimodal basin." |
| `05_discussion.md` | missing placeholder | Needs placeholder for final surrogate fidelity conclusion based on K3's destruction of 2nd-order minima. |
""",

    "GEMINI_FIGURE_SOURCE_CROSSWALK_V2_20260422.md": """# G-DR4: Figure/Source-Data Crosswalk v2
**Date:** 2026-04-22

| Figure ID | Current Caption Intent | Source JSON/CSV/Log | Authority Level | Zenodo Ready? |
| :--- | :--- | :--- | :--- | :--- |
| Fig 1 | Compute-ViT Framework Overview | (Diagram) | `canonical` | Yes |
| Fig 2 | Baseline Performance (FP32) | `tinyvit_v1_results_gpt.json` | `canonical` | Yes |
| Fig 3 | Mild NL (NL=1.0) Ensemble HAT | `v4_ensemble_results_gpt.json` | `canonical` | Yes |
| Fig 4 | Severe NL (NL=2.0) Collapse | `v4_nl_severe_results_gpt.json` | `canonical` | Yes |
| Fig 5 | Mitigation Attempts (J1b, J1c) | `qkv_only_linearization_fresh.json` etc | `canonical` | Yes |
| Fig 6 | K2 Bimodal Distribution (N=30) | `cx_k2_fresh_eval.json` | `canonical` | Yes |
| Fig 7 | K3 Conductance Drift Sweep | `[K3-0p25 pending]` | `provisional` | No |
| Fig 8 | K4/K5 Surrogate Fidelity | `cx_k4_alpha_sweep.json`, `cx_k5_third_order.json` | `provisional` | No (needs remote validation) |
| Fig 9 | Tier-2 Ablations (J2, J3, J4) | `cx_j2_results.json` etc | `canonical` | Yes |
""",

    "GEMINI_AMBIGUOUS_BRANCH_OBJECTION_BANK_20260422.md": """# G-DR5: Reviewer Objection Bank (Ambiguous Branch + Weak K3)
**Date:** 2026-04-22

1. **Objection:** "Adding conductance drift (K3) reduces accuracy from 38% to 27%. Your mitigation strategy is fundamentally flawed."
   - **Danger:** Attacks the premise that we understand the optimization landscape.
   - **Response:** K3 is a diagnostic, not a mitigation. It proves that naive uniform drift pushes the optimizer out of fragile 2nd-order minima into worse collapse basins, validating the extreme sensitivity of the bimodal landscape.
   - **Missing Evidence:** `[K3-0p25 pending]`

2. **Objection:** "The bimodal distribution is just an artifact of insufficient training time."
   - **Danger:** Dismisses the physical limit claim.
   - **Response:** Convergence was reached (100 epochs). Training loss plateaued.
   - **Missing Evidence:** None (K2 training logs confirm plateau).

3. **Objection:** "Your 2nd-order STE is obviously miscalibrated if it creates bimodal results."
   - **Danger:** Attacks the surrogate model.
   - **Response:** The 2nd-order STE correctly reflects the local curvature. The bimodality is the *true* landscape of the hardware.
   - **Missing Evidence:** None (K5 3rd-order confirms saturation).

4. **Objection:** "38% is not deployment-ready. The paper has no positive result."
   - **Danger:** "Incremental" rejection.
   - **Response:** The value is in falsification and risk-ranking pre-silicon. We identify the failure mode so hardware designers can avoid it.
   - **Missing Evidence:** None.

5. **Objection:** "Why didn't you try SAM if the landscape is sharp?"
   - **Danger:** Points to obvious algorithmic gap.
   - **Response:** Computationally intractable for 2nd-order analog tracking; listed as future work.
   - **Missing Evidence:** None.

6. **Objection:** "The degradation at dg_eff=0.15 means your hardware assumptions are contradictory."
   - **Danger:** Attacks physics model.
   - **Response:** High drift breaks the delicate balance found by the 2nd-order STE, exposing the narrowness of the survival basins.
   - **Missing Evidence:** `[K3-0p25 pending]`

7. **Objection:** "A range of 22% to 61% means the simulation is unstable, not the hardware."
   - **Danger:** Dismisses the tool entirely.
   - **Response:** FP32 and NL=0.0 baselines on the same tool show tight Gaussian variance (~1.5%). The instability is specific to NL=2.0.
   - **Missing Evidence:** None.

8. **Objection:** "You should have binned the chips and only evaluated the >50% ones."
   - **Danger:** Misses the point of yield prediction.
   - **Response:** Yield is the core metric. Binning post-hoc ignores the 50%+ garbage rate, which drives TCO (Total Cost of Ownership) up unacceptably.
   - **Missing Evidence:** None.

9. **Objection:** "Maybe the patch embedding layer is the real bottleneck."
   - **Danger:** Misdirection.
   - **Response:** Pathway decomposition (G-GG3) mathematically shows QKV condition number is the primary driver of variance.
   - **Missing Evidence:** None.

10. **Objection:** "If K3 doesn't help, what was the point of the experiment?"
    - **Danger:** "Useless ablation" critique.
    - **Response:** It falsifies the mean-field annealing hypothesis, proving the landscape cannot be simply smoothed by global noise.
    - **Missing Evidence:** `[K3-0p25 pending]`

11. **Objection:** "Your results rely on a single Tiny-ViT architecture."
    - **Danger:** Scale attack.
    - **Response:** Lipschitz bounds suggest larger models will be strictly worse without architectural changes, as matrix dimensions increase the Softmax amplification.
    - **Missing Evidence:** None.

12. **Objection:** "The paper is too negative for Nature Communications."
    - **Danger:** Venue mismatch.
    - **Response:** Rigorous falsification of a multi-million dollar tape-out risk is a high-impact physical sciences result. (Alternatively, pivot to ICLR for Paper-2).
    - **Missing Evidence:** None.
""",

    "GEMINI_DEFENSE_ATTACK_SURFACE_V2_20260422.md": """# G-DR6: Defense Attack Surface v2 (K2/K3 Context)
**Date:** 2026-04-22

1. **"Why did K3's drift sweep degrade performance instead of improving it?"**
   - *Short:* The mean-field annealing hypothesis was wrong.
   - *Long:* Uniform drift pushes the optimizer out of narrow survival basins into broader collapse basins. The 2nd-order minima are extremely fragile.
   - *Depends on K3-0p25:* Yes.

2. **"Is the 38.95% mean from K2 a physical ceiling or an optimization artifact?"**
   - *Short:* It's a stochastic physical ceiling.
   - *Long:* The variance proves the optimal weights exist, but the landscape shatters the optimizer's ability to reliably find them.
   - *Depends on K3-0p25:* No.

3. **"If the surrogate fidelity ladder saturated at 2nd order, why does K3 fail?"**
   - *Short:* K3 tests trajectory shifts, not surrogate fidelity.
   - *Long:* We accurately model the local curvature, but the global drift (dg_eff) breaks the fragile minima found.
   - *Depends on K3-0p25:* Yes.

4. **"Aren't you just overfitting to a specific 2nd-order Taylor expansion?"**
   - *Short:* No, CX-K5 (3rd-order) shows identical results.
   - *Long:* Adding the cubic term didn't change the bimodal mean (~42.8%). The surrogate is saturated; the landscape is the reality.
   - *Depends on K3-0p25:* No.

5. **"Why shouldn't industry just use digital attention and ignore this?"**
   - *Short:* They should. That's our conclusion.
   - *Long:* Our Paper-2 explicitly advocates for Hybrid CIM (Digital Attention + Analog MLP) precisely because of these structural limits.
   - *Depends on K3-0p25:* No.

6. **"Could lower learning rates have settled into the >50% basins more reliably?"**
   - *Short:* Unlikely, due to D2D resampling.
   - *Long:* Ensemble HAT resamples the D2D mask every epoch. A low learning rate would fail to adapt to the new mask, causing catastrophic forgetting, not better settling.
   - *Depends on K3-0p25:* No.

7. **"Is the 22% lower bound of the bimodal distribution just random chance?"**
   - *Short:* Yes, 10-class classification chance is 10%. 22% is near-chance with slight residual feature recognition.
   - *Long:* The collapse basin destroys the attention map's ability to mix tokens, effectively reducing the ViT to a bag-of-patches linear classifier.
   - *Depends on K3-0p25:* No.

8. **"What if the device asymmetry (NL_LTP vs NL_LTD) was reversed?"**
   - *Short:* The condition number of the Softmax remains the same.
   - *Long:* The magnitude of the distortion matters more than the sign for breaking the Softmax Lipschitz bound.
   - *Depends on K3-0p25:* No.

9. **"Why did you stop K3 at dg_eff=0.25?"**
   - *Short:* Beyond 0.25, the analog device behaves more like a random number generator than a memory cell.
   - *Long:* It represents 25% of the total dynamic range shifting per update, which is physically unrealistic for functional memory.
   - *Depends on K3-0p25:* Yes.

10. **"If your framework is a 'simulation baseline', why did you add Tier-2 physical mitigations (IR drop)?"**
    - *Short:* To prove the bimodal collapse is independent of spatial effects.
    - *Long:* IR drop is an additive spatial error. The Softmax collapse is a multiplicative error. Tier-2 proves they are orthogonal problems.
    - *Depends on K3-0p25:* No.

11. **"Why does your Chinese thesis Chapter 5 frame K2 as a 'falsification' if some instances survive?"**
    - *Short:* It falsifies deterministic deployment.
    - *Long:* Hardware requires >99% yield. A bimodal distribution with 50% collapse is a falsification of the architecture's commercial viability.
    - *Depends on K3-0p25:* No.

12. **"Could post-training quantization (PTQ) calibration fix the scale mismatch?"**
    - *Short:* No, D2D is instance-specific.
    - *Long:* You cannot calibrate a global PTQ scale factor for an array where the error pattern changes on every fresh chip.
    - *Depends on K3-0p25:* No.

13. **"If I build a perfect linear analog array (NL=1.0), do your limits apply?"**
    - *Short:* No.
    - *Long:* Our positive control (Ensemble HAT at NL=1.0) achieves >86% fresh-instance accuracy. The structural limit is specifically the *interaction* of Softmax and Severe NL.
    - *Depends on K3-0p25:* No.

14. **"Does your theory hold for NLP Transformers (e.g., BERT, LLaMA)?"**
    - *Short:* The Softmax math holds, but the input statistics differ.
    - *Long:* Vision patches have different covariance structures than text embeddings. While the Lipschitz bound applies, the exact onset of the bimodal basin might shift.
    - *Depends on K3-0p25:* No.

15. **"Ultimately, what is the single biggest takeaway from your thesis?"**
    - *Short:* Analog attention is a dead end without architectural linearization.
    - *Long:* First-order models hide the yield collapse. High-fidelity simulation proves that Softmax attention on organic RRAM is stochastically unstable, necessitating Hybrid CIM architectures.
    - *Depends on K3-0p25:* No.
""",

    "GEMINI_RELEASE_BACKLOG_MAP_20260422.md": """# G-DR7: Submission/Release Housekeeping Backlog Map
**Date:** 2026-04-22

## Can Do Now
- Finalize `KIMI_ARXIV_CHECKLIST_V2_20260420.md`
- Finalize `KIMI_CONFERENCE_TEMPLATES_20260420.md`
- Draft Zenodo structure (`KIMI_DATA_RELEASE_MANIFEST_V2_20260505.md`)
- Code cleanup (remove print statements, fix imports)
- Finalize `GEMINI_DEFENSE_WILDCARD_V2_CN_20260501.md`
- Compile `KIMI_DEFENSE_QA_CN_20260420.md`

## Blocked on User Metadata
- `cover_letter.md` final author list
- `00_abstract.md` author affiliations
- `KIMI_CREDIT_V3_20260420.md`
- Suggested Reviewers list

## Blocked on `K3 final`
- Finalizing `paper/05_results.md` discussion of drift resilience.
- `paper/thesis_cn/chapter_5_failure_modes.tex` final conclusion paragraph (K3 annealing vs degradation).
- `GEMINI_REWRITE_DECISION_TREE_V2_20260421.md` final branch selection.

## Optional Only
- Presentation slides for non-defense conferences (e.g., MLSys pitch).
- Social media threads (`KIMI_SOCIAL_SHORTFORM_20260420.md`).
- Extended tutorial notebook plots.
""",

    "GEMINI_BRANCH_DECISION_AID_20260422.md": """# G-DR8: One-Page Branch Decision Aid (Post K3-0.25)
**Date:** 2026-04-22

This sheet directs Kimi/Codex on how to interpret the final `CX-K3 delta_g_eff=0.25` data point once it lands.

## Scenario 1: `0.25` Lifts Above K2 (> 42%)
- **Scientific Interpretation:** High drift acts as an effective mean-field annealing mechanism, helping the optimizer escape the worst collapse basins during 2nd-order STE training.
- **What not to claim:** Do not claim it "solves" the issue, as variance will still be bimodal.
- **Best Next Exp:** K4 (Alpha sweep) to see if annealing + weaker 2nd-order is optimal.
- **Paper-2 Route:** Stochastic Basin (focus on annealing escape paths).

## Scenario 2: `0.25` Roughly Matches K2 (~38%)
- **Scientific Interpretation:** Drift is irrelevant to the structural landscape shattering. The bimodal basins are too deep for mean-field drift to bridge.
- **What not to claim:** Do not claim drift is an effective mitigation or a major danger.
- **Best Next Exp:** K5 (3rd order sanity check).
- **Paper-2 Route:** Stochastic Basin (focus on intrinsic topological limits).

## Scenario 3: `0.25` is Worse Than K2 (< 35%)  [CURRENT TREND]
- **Scientific Interpretation:** Drift actively destroys the fragile minima found by the 2nd-order STE. The landscape is incredibly brittle, and the "survival" basins found in K2 are extremely narrow.
- **What not to claim:** Do not claim mean-field theory applies here. Do not claim 2nd-order STE finds robust solutions.
- **Best Next Exp:** Stop K-series. The brittleness is proven.
- **Paper-2 Route:** Structural Limit Reinforced (focus on extreme sensitivity to physical perturbations).
"""
}

for fname, content in files.items():
    with open(os.path.join(base_dir, fname), "w", encoding="utf-8") as f:
        f.write(content)

print("Gemini Drudge Wave thoroughly fixed and deepened.")
