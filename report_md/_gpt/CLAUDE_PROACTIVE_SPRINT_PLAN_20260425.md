# CLAUDE PROACTIVE SPRINT PLAN — Depth Investment Phase
**Date:** 2026-04-25 01:50 CST
**From:** Claude (Chief Architect)
**Trigger:** User directive "我们得有自己的步骤" — replace passive wait with proactive depth investment
**Duration:** ~1-2 weeks
**Status:** ACTIVE (replaces calm-before-trigger Round-6 with active Round-7)

---

## 0. Premise

8×40GB returns next week. PhD data is indeterminate-but-not-imminent. Sitting on R6-1 housekeeping for a week is wasteful. The buffer should become **substantive depth investment** that converts our submission from "scrubbed and accurate" into "Nat Electronics editor-friendly with theoretical novelty + empirical mechanism + tooling positioning".

Four investment axes, all using existing assets, no dependence on triggers:

| Axis | What | Why it matters |
|:--|:--|:--|
| **Theory deepening** | Higher-order Taylor + PAC-Bayes bound + flat-minima connection | Moves Ensemble HAT from "method that works" to "principled method with generalization theory" |
| **Empirical mechanism** | Hessian / loss landscape / CKA / per-layer sensitivity on existing checkpoints | Makes the theoretical predictions concretely visible, gives reviewer "I can see why it works" feeling |
| **Writing polish** | Senior-paper editorial, design-rules callout, reproducibility cookbook | Lifts manuscript from "accurate" to "elegant"; reduces reviewer friction |
| **Tooling positioning** | Competitor analysis vs CrossSim/AIHWKit/NeuroSim deepened | Positions paper in analog CIM tooling landscape Nat Electronics readers care about |

---

## 1. Sprint phases (with timeline)

### Phase 1: Theory deepening (Days 1-3, Kimi)

Build on KIMI-THEORY-1 to a 5-7 page theoretical contribution.

**Add to Supp Note S-Theory:**

1. **§S.7 Higher-order corrections** (1 page)
   - Beyond second-order Taylor: derive third- and fourth-order moments under Gaussian D2D
   - Show when second-order approximation breaks down (large σ, near-saturation weights)
   - Connect to existing Supp Note S6 schematic with rigor

2. **§S.8 PAC-Bayes generalization bound** (2 pages)
   - Treat Ensemble HAT as PAC-Bayesian posterior over D2D-perturbed weights
   - Derive a McAllester-style bound: gen. error ≤ training loss + KL(posterior‖prior)/n + slack
   - Show that the bound is tight when posterior aligns with implicit gradient-L2 regularizer
   - Implication: the +76pp / +78pp empirical generalization gap has a theoretical floor

3. **§S.9 Flat minima connection** (1-2 pages)
   - Cite Hochreiter & Schmidhuber 1997 + Keskar et al. 2017 + Foret et al. 2021 (SAM)
   - Show Ensemble HAT objective is equivalent (up to second order) to minimizing a SAM-style sharpness penalty along the D2D-mismatch direction
   - This is a **structural analogue** (per Round-2 D5 wording discipline) — not exact, but tight under typical σ_D2D

4. **§S.10 Limitations of the theoretical framework** (0.5 page)
   - Heavy-tailed D2D: second-order breaks down
   - Spatially correlated D2D: AR(1) extension via Fisher metric (already in S.5)
   - Non-uniform σ_D2D across layers: per-layer Fisher coefficients vary

**Deliverable:** Updated `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` (extends existing). Word count target: ~3500-4500 (up from current ~3200).

### Phase 2: Empirical mechanism (Days 1-5, Codex local GPU)

Lightweight analyses on existing M-series + canonical Ensemble HAT checkpoints. NO new training. Each analysis is standalone.

**Job E1 — Hessian eigenspectrum (~2 GPU-h total, all checkpoints)**
- Use Hutchinson trace estimator + Lanczos for top-50 eigenvalues
- Compare Standard HAT vs Ensemble HAT vs Proportional HAT (all 6 M-series + canonical)
- Hypothesis: Ensemble HAT lands on flatter minimum (smaller top eigenvalues)
- Deliverable: `paper/figures/figS_hessian_spectrum.{png,pdf}` + JSON

**Job E2 — Loss landscape along D2D direction (~1 GPU-h)**
- For canonical Ensemble HAT vs Standard HAT, plot loss as function of D2D perturbation magnitude
- Show that Ensemble HAT loss is flatter in the D2D direction
- Deliverable: `paper/figures/figS_d2d_loss_landscape.{png,pdf}`

**Job E3 — Cross-checkpoint CKA similarity (~30 min)**
- CKA (Centered Kernel Alignment) on layer activations across M-series checkpoints
- Question: do Standard / Ensemble / Proportional checkpoints converge to similar representations under severe NL?
- Deliverable: `paper/figures/figS_cka_mseries.{png,pdf}` + interpretation paragraph

**Job E4 — Per-layer mismatch sensitivity (~2 GPU-h)**
- For canonical Ensemble HAT, perturb one layer's D2D mask at a time, measure accuracy drop
- Identify which layers are most fragile (likely MLP > attention QKV > LayerNorm-adjacent)
- Deliverable: `paper/figures/figS_per_layer_sensitivity.{png,pdf}` + table

**Job E5 — Checkpoint averaging (~30 min, optional bonus)**
- Average Standard HAT seeds 123 + 456 weights, evaluate on fresh instances
- Question: does seed averaging recover the Ensemble HAT generalization without per-epoch resampling?
- Deliverable: `paper/figures/figS_checkpoint_avg.{png,pdf}` (likely negative result, still publishable)

**Total Codex Phase 2 budget: ~6-8 GPU-h**

### Phase 3: Writing polish (Days 4-7, Kimi)

After Phase 1 + 2 outputs land. Senior-paper editorial pass on the integrated manuscript.

**Tasks:**
1. **Section opening + closing sentences**: every section starts with a strong topic sentence and ends with a clear bridge. Audit all.
2. **Discussion narrative arc**: restructure §6 to follow Diagnosis → Treatment → Mechanism → Implications. The "Mechanism" subsection now hosts Phase 1 theory + Phase 2 empirical.
3. **Design rules callout**: add a one-page boxed callout at end of §6 titled "Design rules for organic optoelectronic CIM transformer deployment". 5-7 actionable rules with quantitative thresholds.
4. **Reproducibility cookbook**: new Supp Note S-Reproducibility (~3 pages) — step-by-step "reproduce paper-1 from clone to fresh-eval" guide. Code commit, env setup, dataset, training command, eval command, expected wall-clock, expected accuracy.
5. **Figure captions self-contained**: every caption must be readable without body text. Audit all 10+ figures.
6. **Acknowledgments + Author contributions + Funding**: skeleton in cover letter, fill in for submission.

**Deliverable:** Updated canonical `.tex` files (or `.kimi_draft_v4` sidecars if Kimi prefers). Plus new `paper/latex_gpt/supplementary/S_reproducibility.tex`.

### Phase 4: Defense prep + tooling positioning (Days 7-10, Kimi)

Two parallel sub-phases:

**Phase 4A — Defense slides + Q&A**
- Update `KIMI_DEFENSE_BEAMER_20260423.tex` to current state
- Update `KIMI_DEFENSE_QA_PREP_20260420.md` with post-fix numbers + new theory
- Add slide-by-slide narration script
- Anticipated questions document for committee

**Phase 4B — Tooling positioning supplementary**
- Expand current CrossSim footnote (Outlook §47) into a proper Supp Note S-Tooling
- Honest comparison: our framework vs CrossSim vs AIHWKit vs NeuroSim
- What each does well, where each diverges
- Position our contribution as complementary, not adversarial
- Cite Rasch et al. 2023 (AIHWKit) explicitly as the conceptual ancestor of train-surrogate / eval-ADC-hook discipline
- Add one comparison table

**Deliverables:**
- Updated defense materials in `report_md/_gpt/`
- New `paper/latex_gpt/supplementary/S_tooling_comparison.tex`

### Phase 5: Sprint integration (Days 10-12, Claude)

After all four phases land:
- Claude does one integration pass: theory deepening + empirical figures into Supp Note S-Theory; design rules callout into Discussion; reproducibility + tooling Supp Notes wired into supplementary
- pdflatex full compile
- Final consistency grep
- Report sprint completion

---

## 2. What proactively triggers OFF the sprint

| Trigger | Action |
|:--|:--|
| 8×40GB return mid-sprint | Continue sprint; queue cross-arch integration as Phase 6 |
| PhD data lands mid-sprint | Continue sprint; queue R-D0 ingest as Phase 7 |
| User signals "stop, just submit" | Halt at end of current phase, fast-track integration |
| Phase 1 theory derivation breaks (e.g., PAC-Bayes bound is vacuous) | Document the negative result honestly, retain second-order Taylor as primary contribution, drop PAC-Bayes |
| Phase 2 empirical contradicts theory (e.g., Ensemble HAT NOT in flatter minimum) | Major escalation. Reopen NARRATIVE_PIVOT mechanism claim. |

---

## 3. What this sprint is NOT

- Not new training (Phase 2 is eval-only on existing checkpoints)
- Not new architectures
- Not new datasets
- Not retraining existing M-series
- Not narrative pivot (NARRATIVE_PIVOT remains source of truth)
- Not gating any future trigger work

---

## 4. Risk assessment

**Low risk axes:**
- Phase 1 theory: derivations might fail; if so, negative result documented. No paper damage.
- Phase 3 writing polish: pure improvement. No risk.
- Phase 4 positioning: pure improvement. No risk.

**Medium risk axis:**
- Phase 2 empirical: if Hessian / loss-landscape / CKA contradicts theory, we have an honest scientific finding to navigate. Could strengthen or weaken the paper depending on what we find. NOT zero-risk, but the right thing to do.

**Risk-adjusted ROI:** Very high. Worst case = honest negative findings documented. Best case = paper substantially upgraded.

---

## 5. Sequencing

```
Day 1 ────────────────────────────────────────────────────────────────────
  Kimi: Phase 1 starts (higher-order Taylor)
  Codex: Phase 2 E1 starts (Hessian eigenspectrum)
  
Day 2-3 ──────────────────────────────────────────────────────────────────
  Kimi: Phase 1 continues (PAC-Bayes + flat minima)
  Codex: Phase 2 E2-E4 (loss landscape, CKA, per-layer sensitivity)
  
Day 4-5 ──────────────────────────────────────────────────────────────────
  Kimi: Phase 1 lands
  Codex: Phase 2 E5 (optional checkpoint averaging)
  Kimi: Phase 3 writing polish starts
  
Day 6-7 ──────────────────────────────────────────────────────────────────
  Codex: Phase 2 lands
  Kimi: Phase 3 continues
  
Day 7-10 ─────────────────────────────────────────────────────────────────
  Kimi: Phase 4A defense prep
  Kimi: Phase 4B tooling positioning supplementary
  
Day 10-12 ────────────────────────────────────────────────────────────────
  Claude: Phase 5 integration pass
  
[8×40GB returns somewhere in Day 4-7] → queue as separate Phase 6
[PhD data: indeterminate]
```

Estimated 1-2 weeks. Months of buffer absorbs comfortably.

---

## 6. Frozen decisions reaffirmed

All 12 frozen decisions from `CLAUDE_FORWARD_ROADMAP §10` still hold. Sprint adds depth, doesn't change any.

---

## 7. Dispatches

1. `DISPATCH_KIMI_THEORY_2_DEEPENING_20260425.md` (Phase 1)
2. `DISPATCH_CODEX_EMPIRICAL_DEEPENING_20260425.md` (Phase 2)
3. `DISPATCH_KIMI_WRITING_POLISH_20260425.md` (Phase 3)
4. `DISPATCH_KIMI_DEFENSE_TOOLING_20260425.md` (Phase 4)
5. `BROADCAST_ROUND7_PROACTIVE_SPRINT_20260425.md` (master broadcast)

---

## 8. One-line

Replace passive wait with proactive depth investment: 4 phases (theory + empirical + writing + positioning) over 1-2 weeks, all on existing assets, builds submission from "accurate" to "Nat-Electronics-editor-friendly with theoretical and mechanistic novelty".
