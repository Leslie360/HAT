# DISPATCH KIMI-THEORY-2 — Theory Deepening (Phase 1)
**Date:** 2026-04-25 01:50 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md Phase 1
**Priority:** HIGH (sprint anchor)
**Time budget:** ~3 days

---

## 0. Mission

Extend KIMI-THEORY-1 from second-order Taylor + implicit gradient-L2 to a more complete theoretical treatment with PAC-Bayes generalization bound + flat-minima connection. Move Ensemble HAT from "method that works" to "principled method with generalization theory".

---

## 1. Sections to add to `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex`

### §S.7 Higher-order corrections (~1 page, ~600 words)

**Goal:** Show when second-order approximation breaks down + provide third-/fourth-order qualitative description.

**Content:**
- Generalize §S.2 Taylor expansion to arbitrary order: $\mathcal{L}_{\text{Ens}} \approx \sum_k \frac{1}{k!} \mathbb{E}_M[(M^\top \nabla)^k \ell]$
- Compute closed-form for k=3 (zero by Gaussian symmetry), k=4 (Wick contractions)
- Show that fourth-order term scales as $\sigma_{\text{D2D}}^4$ — small unless σ ≥ ~20% (we operate at 10%)
- Identify regime where second-order fails: large σ, near-saturation weights (where $\partial^2 \ell / \partial \theta_i^2$ is large)
- Cite proper analog: Roberts & Yaida 2022 "Principles of Deep Learning Theory" for higher-order treatment of weight noise

### §S.8 PAC-Bayes generalization bound (~2 pages, ~1200 words)

**Goal:** Derive a generalization bound for Ensemble HAT, showing the +76pp / +78pp empirical gap has theoretical floor.

**Setup:**
- Treat training as PAC-Bayes posterior $Q$ over D2D-perturbed weights: $Q(W) = \mathcal{N}(W^*; \text{diag}(\sigma_{\text{D2D}}^2 W^{*2}))$ where $W^*$ is the trained weight
- Choose prior $P$ as wide Gaussian centered at random init (or canonical pre-trained checkpoint)
- McAllester 1999 / Dziugaite & Roy 2017 PAC-Bayes bound: $\mathbb{E}_{W \sim Q}[\text{gen error}] \leq \mathbb{E}_{W \sim Q}[\text{train loss}] + \sqrt{(KL(Q\|P) + \log(1/\delta))/(2n)}$
- Compute KL divergence under our diagonal-Gaussian-posterior, wide-Gaussian-prior assumptions

**Key result:**
- The bound's slack term scales as $\sqrt{KL/n}$
- KL is dominated by the per-layer $W^{*2} / \sigma_{\text{prior}}^2$ ratios
- Implication: smaller weight magnitudes → tighter generalization bound. Connects naturally to the implicit gradient-L2 from §S.2 (which penalizes large weights with large gradient sensitivity).

**Honesty constraints:**
- Don't overclaim. PAC-Bayes bounds in deep learning are typically vacuous numerically. Frame as "theoretically motivated structural argument" not "tight empirical prediction".
- Cite Pérez-Ortiz et al. 2021 honestly on PAC-Bayes vacuousness in DNNs.
- Use the bound to **explain the direction** of the empirical gap, not predict its magnitude.

### §S.9 Flat minima connection (~1.5 pages, ~900 words)

**Goal:** Show Ensemble HAT structurally analogous to Sharpness-Aware Minimization (SAM) along D2D direction.

**Content:**
- Define D2D-direction sharpness: $\mathcal{S}_{\text{D2D}}(W) = \mathbb{E}_M[\ell(W \odot (1+M))] - \ell(W)$
- Show $\mathcal{S}_{\text{D2D}}(W) \approx \frac{\sigma_{\text{D2D}}^2}{2} \sum_i W_i^2 (\partial^2 \ell / \partial \theta_i^2)$ (second-order)
- Compare to SAM (Foret et al. 2021): SAM minimizes $\max_{\|\epsilon\| \leq \rho} \ell(W + \epsilon)$
- Ensemble HAT minimizes $\mathbb{E}_M [\ell(W \odot (1+M))]$ — averaged not max'd
- **Connection**: Ensemble HAT ≈ "stochastic SAM in the D2D direction with Gaussian perturbation instead of worst-case"
- Cite: Hochreiter & Schmidhuber 1997 (flat minima generalize), Keskar et al. 2017 (large-batch sharpness), Foret et al. 2021 (SAM), Andriushchenko & Flammarion 2022 (when SAM works)

**Mechanistic implication:**
- Ensemble HAT lands in flat-in-D2D-direction minima
- Fresh D2D realization lands in same flat region with high probability → cross-instance generalization
- This is the **mechanism** for the 86.37% recovery vs 10% Standard HAT collapse

**Honesty:** "Structural analogue", not "exact equivalence". Different perturbation distribution (Gaussian vs adversarial), different averaging (expectation vs max).

### §S.10 Limitations of theoretical framework (~0.5 page, ~300 words)

**Content:**
- Heavy-tailed D2D: second-order Taylor breaks; higher-order moments needed (S.7)
- Spatially correlated D2D: AR(1) Fisher-metric extension already in S.5
- Per-layer non-uniform σ_D2D: each layer's Fisher coefficient varies; framework still applies layerwise
- C2C noise in proportional regime: coupled to D2D (already noted in S.2 remark)
- PAC-Bayes bound numerical vacuousness — informative direction, not magnitude

---

## 2. Bibliography additions

Add to `paper/latex_gpt/refs_gpt.bib`:

```bibtex
@misc{roberts2022principles,
  author={Roberts, Daniel A. and Yaida, Sho},
  title={Principles of Deep Learning Theory},
  year={2022},
  publisher={Cambridge University Press},
  note={Higher-order weight perturbation analysis}
}

@inproceedings{dziugaite2017computing,
  author={Dziugaite, Gintare K. and Roy, Daniel M.},
  title={Computing Nonvacuous Generalization Bounds for Deep Stochastic Neural Networks},
  booktitle={UAI},
  year={2017}
}

@article{perez2021tighter,
  author={Pérez-Ortiz, María and Rivasplata, Omar and Shawe-Taylor, John and Szepesvári, Csaba},
  title={Tighter Risk Certificates for Neural Networks},
  journal={JMLR},
  year={2021}
}

@inproceedings{foret2021sharpness,
  author={Foret, Pierre and Kleiner, Ariel and Mobahi, Hossein and Neyshabur, Behnam},
  title={Sharpness-Aware Minimization for Efficiently Improving Generalization},
  booktitle={ICLR},
  year={2021}
}

@inproceedings{keskar2017large,
  author={Keskar, Nitish S. and Mudigere, Dheevatsa and Nocedal, Jorge and Smelyanskiy, Mikhail and Tang, Ping Tak Peter},
  title={On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima},
  booktitle={ICLR},
  year={2017}
}

@inproceedings{andriushchenko2022understanding,
  author={Andriushchenko, Maksym and Flammarion, Nicolas},
  title={Towards Understanding Sharpness-Aware Minimization},
  booktitle={ICML},
  year={2022}
}
```

---

## 3. Discussion section update

After Phase 1 lands, add 1 paragraph to §6.1 Principal Accuracy Bottlenecks (in `paper/latex_gpt/sections/06_discussion.tex`):

> Ensemble HAT's empirical effectiveness is not merely an engineering trick. Supplementary Note S-Theory derives that the per-epoch resampling objective is, to second order, equivalent to a weighted gradient-$L_2$ regularizer (analogous to dropout-as-$L_2$, Wager et al.\ 2013) and, structurally, to a stochastic Sharpness-Aware Minimization along the device-mismatch direction (analogous to SAM, Foret et al.\ 2021). A PAC-Bayes argument provides a generalization-bound rationale for why fresh hardware-instance accuracy tracks the training-distribution average. Empirical Hessian and loss-landscape analyses (Supp Note S-Mechanism) confirm Ensemble HAT lands in flatter D2D-direction minima.

(Note: §S-Mechanism is the Phase 2 Codex output — Kimi inserts the reference, integration happens at Phase 5.)

---

## 4. Constraints

- **No empirical numbers** in theory note (zone discipline, per Round-2 D5)
- **Cite, don't reprove**, established results (Wager 2013, Foret 2021, etc.)
- **Honesty over flash**: PAC-Bayes is "theoretically motivated direction", not "tight prediction"
- **Structural analogue**: keep this exact language for Wager / SAM connections (per Round-2 D5)
- **No bug-retrospective language** in theory note (continues from Round-2 doctrine)
- **Length discipline**: target totals — §S.7 ~600w, §S.8 ~1200w, §S.9 ~900w, §S.10 ~300w. Total addition ~3000w to existing ~3200w → final ~6200w (~5-6 pages).

---

## 5. Validation checklist

- [ ] All 6 new bib entries added without typos
- [ ] All equation environments balanced
- [ ] Zero unescaped `%`
- [ ] No empirical numbers (grep for `\d+\.\d+%`)
- [ ] No bug-retrospective phrasing
- [ ] §S.7 cites Roberts & Yaida 2022
- [ ] §S.8 cites Dziugaite & Roy 2017 + Pérez-Ortiz 2021
- [ ] §S.9 cites Hochreiter 1997 + Keskar 2017 + Foret 2021 + Andriushchenko 2022
- [ ] §S.10 honest limitations, no overclaim
- [ ] Discussion paragraph (§6.1 addition) drafted as `06_discussion_theory_paragraph.tex.kimi_draft`

---

## 6. Deliverables

| File | Status |
|:--|:--|
| `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | Extended in place (§S.7 + §S.8 + §S.9 + §S.10 added) |
| `paper/latex_gpt/refs_gpt.bib` | 6 new entries |
| `paper/latex_gpt/sections/06_discussion_theory_paragraph.tex.kimi_draft` | New 1-paragraph addition for §6.1 |
| `report_md/_gpt/KIMI_THEORY_2_COMPLETE_<date>.md` | Status + change summary + validation checklist |

---

## 7. If derivation breaks

If PAC-Bayes bound turns out vacuous or contradictory under our setting (which is possible — DNN PAC-Bayes is tricky):
- Document the negative result honestly in `KIMI_THEORY_2_COMPLETE_<date>.md`
- Drop §S.8 from supplementary, keep §S.7 + §S.9 + §S.10
- Discussion paragraph amended to "Wager 2013 + SAM connection only, no generalization bound"
- Total contribution still net-positive (higher-order + flat minima)

This is acceptable. Honesty > completeness.

---

## 8. Timing

Day 1: §S.7 higher-order
Day 2: §S.8 PAC-Bayes
Day 3: §S.9 SAM connection + §S.10 limitations + discussion paragraph + bib

Land per day to AGENT_SYNC. No need to wait for full deliverable.

---

## 9. Success criteria

- Reviewer reading the integrated paper sees: "Ensemble HAT is grounded in implicit regularization theory + PAC-Bayes generalization argument + flat-minima geometric intuition"
- Three independent theoretical lenses converging on the same mechanism
- All citations to canonical works in the field
- Honest scoping of what each theoretical lens does and doesn't predict

This is what moves a Nat Electronics submission from "good engineering" to "good science with engineering implications".
