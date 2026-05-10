<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Round Q Advance Brief — GPU Window Justification

> **Task:** K-X25
> **Date:** 2026-04-21
> **Trigger:** Round P ends Day 14. CX-J1b/c/d outcomes determine Round Q shape.
> **Authority:** This memo gates the next GPU authorization. No window is opened without a signed branch decision.

---

## 0. Situation Summary

Round P closed with CX-J1 (joint MLP-linear + Ensemble HAT, NL = 2.0) landing at **30.53 ± 7.07 %** fresh-instance accuracy—statistically indistinguishable from the MLP-only (32.12 %) and all-linear (32.60 %) baselines. The ~30 % ceiling under severe nonlinearity is therefore **not a training-recipe artifact**.

The diagnostic trio **CX-J1b/c/d** (executed in Round P Tier 1+) is designed to falsify three distinct hypotheses about the ceiling's origin:

| Experiment | Hypothesis Tested | Expected if Ceiling Holds |
|:-----------|:------------------|:--------------------------|
| **CX-J1b** | QKV MAC nonlinearity is the bottleneck | ~30 % (softmax/projection still nonlinear) |
| **CX-J1c** | Full attention linearization breaks the ceiling | ~30 % (MLP nonlinear + softmax retained) |
| **CX-J1d** | First-order surrogate is too coarse | ~30 % (ceiling is structural, not surrogate artifact) |

Round Q's scientific purpose, scope, and compute budget are fully contingent on which of these experiments break the ceiling. This memo pre-stages four mutually exclusive branches so that the Day-14 gate decision takes ≤10 minutes.

---

## 1. Decision Tree

```
                    ┌─────────────────────────────────────┐
                    │  CX-J1b/c/d results land (Day 10–14) │
                    └──────────────┬──────────────────────┘
                                   │
           ┌───────────────────────┼───────────────────────┐
           │                       │                       │
     J1d ≥ 50 %?             J1c ≥ 50 %?             J1b ≥ 50 %?
     (surrogate break)       (attention break)       (QKV break)
           │                       │                       │
           ▼                       ▼                       ▼
    ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
    │  BRANCH D   │        │  BRANCH C   │        │  BRANCH B   │
    │ 2nd-Order   │        │ All-Linear  │        │ QKV-Eng     │
    │ Surrogate   │        │ + Ensemble  │        │ Paper       │
    │   Paper     │        │   HAT Dep.  │        │             │
    └─────────────┘        └─────────────┘        └─────────────┘
           │                       │                       │
           └───────────────────────┼───────────────────────┘
                                   │
                            ALL THREE ~30 %
                                   │
                                   ▼
                          ┌─────────────┐
                          │  BRANCH A   │
                          │ Structural  │
                          │ Limit +     │
                          │ Higher-Order│
                          │  Surrogate  │
                          └─────────────┘
```

### Priority Rule

Evaluate branches in **D → C → B → A** order. J1d is the most theoretically decisive (it reframes the entire research program from architecture to modeling). If J1d succeeds, Round Q is automatically Branch D regardless of J1b/c. If J1d fails but J1c succeeds, Branch C. If J1d and J1c fail but J1b succeeds, Branch B. Only if all three cluster ~30 % do we fall through to Branch A.

| Branch | Trigger Condition | Round Q Paper Type | Venue Target |
|:------:|:------------------|:-------------------|:-------------|
| **A** | J1b ~30 % ∧ J1c ~30 % ∧ J1d ~30 % | Structural-limit theory + higher-order surrogate validation | *Nature Electronics* or COLT / NeurIPS Theory |
| **B** | J1b ≥ 50 % ∧ J1c < 50 % (implied) | QKV-focused engineering: selective linearization protocols | *Nature Electronics* or IEDM |
| **C** | J1c ≥ 50 % ∧ J1d < 50 % | All-linear attention + Ensemble HAT deployment study | *Nature Electronics* (primary), NeurIPS-Hardware (co-lead) |
| **D** | J1d ≥ 50 % | 2nd-order surrogate fidelity: from caricature to calibrated model | MLSys / ISCA (surrogate-architecture co-design) |

*Threshold convention: "breaks ceiling" = fresh-instance accuracy ≥ 50 % on CIFAR-10 with 95 % CI not overlapping the 30 % cluster. This is a deliberately conservative bar to avoid false positives.*

---

## 2. Round Q Task List (Per Branch)

### Branch A — Structural Limit Confirmed (Default Fallback)
*If all three diagnostics hit ~30 %, the ceiling is a structural property of first-order NL surrogate × attention block.*

| # | Task ID | Description | Owner | Deliverable |
|:--:|:--------|:------------|:-----:|:------------|
| A1 | **Q-A1** | Higher-order surrogate sweep: 2nd-order (κ = 0.25, 0.50, 0.75) + 3rd-order pilot | Codex | `cx_higher_order_sweep.json` |
| A2 | **Q-A2** | Formal proof expansion: turn heuristic sketch into lemma-theorem structure for appendix | Gemini | `structural_limit_formal.tex` |
| A3 | **Q-A3** | Cross-architecture limit test: ConvNeXt-Tiny + ResNet-18 under identical severe-NL protocol | Codex | `cross_arch_limit.json` |
| A4 | **Q-A4** | Deployment envelope quantification: vary σ_d2d, array size, head count; contour the "prohibited" zone | Codex | `deployment_envelope_data.json` + Fig. 5 draft |
| A5 | **Q-A5** | Theory paper manuscript: Introduction + Related Work + Formal Statement + Diagnostic Evidence + Conclusion | Kimi | `paper_theory/draft_v0/` (8 sections) |
| A6 | **Q-A6** | Grant proposal pivot: reframe Aim 1 from "mitigation" to "characterization of fundamental limits" | Gemini | `grant_limit_characterization.md` |
| A7 | **Q-A7** | Defense Q-bank: 10 new Q&A on "how do you know it's structural and not just a bug?" | Kimi | `defense_structural_qa.md` |
| A8 | **Q-A8** | Rebuttal pre-positioning: draft OBJ-structural-limit response letter paragraphs | Kimi | `rebuttal_structural_pre_draft.md` |

### Branch B — QKV-Specific Bottleneck
*If J1b alone breaks the ceiling, the barrier is localized to QKV MAC arrays; projection and softmax are sufficiently robust.*

| # | Task ID | Description | Owner | Deliverable |
|:--:|:--------|:------------|:-----:|:------------|
| B1 | **Q-B1** | QKV-linear + Ensemble HAT full run: 3 seeds, full eval, CIFAR-10 + CIFAR-100 | Codex | `qkv_ensemble_full.json` |
| B2 | **Q-B2** | Hardware-cost analysis: energy/area/latency of digital QKV vs. analog QKV at iso-accuracy | Gemini | `qkv_hardware_cost.json` + table |
| B3 | **Q-B3** | QKV-specific gradient compensation: NL-aware STE with per-head κ tuning | Codex | `qkv_ste_v2.py` + ablation data |
| B4 | **Q-B4** | Scaling study: head-count sweep (2, 4, 6, 8 heads) under QKV-linear regime | Codex | `qkv_head_scaling.json` |
| B5 | **Q-B5** | Cross-dataset validation: Flowers-102, SVHN under QKV-linear + Ensemble HAT | Codex | `qkv_cross_dataset.json` |
| B6 | **Q-B6** | QKV-focused engineering paper: selective linearization as a deployable protocol | Kimi | `paper_qkv/draft_v0/` (6 sections) |
| B7 | **Q-B7** | Industrial brief: NVIDIA-internal CIM team slide deck on selective-linearization ROI | Gemini | `industrial_qkv_brief.md` |
| B8 | **Q-B8** | Patent landscape scan: prior art on selective analog/digital partitioning in attention | Kimi | `patent_landscape_qkv.md` |

### Branch C — Full-Attention Linearization Works
*If J1c breaks the ceiling, linearizing both QKV and projection is sufficient; the softmax-normalized dot-product itself is not the barrier when its MAC inputs are clean.*

| # | Task ID | Description | Owner | Deliverable |
|:--:|:--------|:------------|:-----:|:------------|
| C1 | **Q-C1** | Full-attention-linear + Ensemble HAT full run: 3 seeds, CIFAR-10/100 | Codex | `attn_linear_ensemble.json` |
| C2 | **Q-C2** | All-linear + Ensemble HAT full run: push the upper bound (MLP also linearized) | Codex | `all_linear_ensemble.json` |
| C3 | **Q-C3** | ImageNet-100 pilot: deferred Tier-4 experiment now justified (100–150 GPU-h) | Codex | `imagenet100_pilot.json` |
| C4 | **Q-C4** | Energy-delay-product analysis: full-attention-linear vs. all-linear vs. digital baseline | Gemini | `edp_analysis.json` + Fig. 5 draft |
| C5 | **Q-C5** | FPGA prototype planning: RTL feasibility for linear-attention + analog MLP hybrid | Gemini | `fpga_plan.md` |
| C6 | **Q-C6** | Cross-dataset at scale: Tiny-ImageNet-200 validation if ImageNet-100 succeeds | Codex | `tiny_imagenet_pilot.json` |
| C7 | **Q-C7** | Deployment paper manuscript: "Conditional Viability of Analog CIM for ViT" | Kimi | `paper_deployment/draft_v0/` (8 sections) |
| C8 | **Q-C8** | Ensemble HAT cadence optimization: per-batch vs. per-epoch under linear-attention regime | Codex | `hat_cadence_v2.json` |

### Branch D — Surrogate-Fidelity Issue
*If J1d breaks the ceiling, the first-order surrogate g → g^NL is too coarse; higher-order write dynamics reveal learnable compensations.*

| # | Task ID | Description | Owner | Deliverable |
|:--:|:--------|:------------|:-----:|:------------|
| D1 | **Q-D1** | 2nd-order κ sweep: κ ∈ {0.1, 0.3, 0.5, 0.7, 0.9} with NaN-guarded training | Codex | `kappa_sweep.json` |
| D2 | **Q-D2** | 3rd-order extension: cubic term in Taylor expansion; test saturation hypothesis | Codex | `third_order_pilot.json` |
| D3 | **Q-D3** | Piecewise-polynomial surrogate: breakpoint at g_mid with independent left/right curvature | Codex | `piecewise_nl_pilot.json` |
| D4 | **Q-D4** | Cross-simulator validation: replicate 2nd-order behavior in CrossSim + AIHWKIT | Codex | `cross_sim_higher_order.json` |
| D5 | **Q-D5** | Physical realism audit: map κ to filament-dynamics parameters from Zhang 2025 OPECT data | Gemini | `kappa_physical_mapping.md` |
| D6 | **Q-D6** | Surrogate calibration protocol: automated fit from measured write curves to κ + higher-order coeffs | Codex | `surrogate_calibrator_v2.py` |
| D7 | **Q-D7** | Surrogate-fidelity paper: "Beyond g^NL: Higher-Order Behavioral Models for Analog CIM Training" | Kimi | `paper_surrogate/draft_v0/` (7 sections) |
| D8 | **Q-D8** | Open-source surrogate library: pip-installable `compute_vit.surrogate` subpackage | Codex | `compute_vit/surrogate/` module + tests |

---

## 3. Compute Budget (Per Branch)

All estimates assume A100/RTX 5070 Ti equivalent; Tiny-ViT V4 on CIFAR-10 baseline is ~12 GPU-h per seed.

| Branch | Experiment Load | GPU-Hours | Storage | Notes |
|:------:|:----------------|:---------:|:-------:|:------|
| **A** | Higher-order sweep (3 κ × 3 seeds) + cross-arch (2 arch × 3 seeds) + envelope (9 grid pts × 3 seeds) | **~180 h** | ~40 GB | Dominated by grid sweep; can be pruned to ~120 h if envelope is sampled, not full-grid |
| **B** | QKV-ensemble (3 seeds × 2 datasets) + head scaling (4 configs × 3 seeds) + cross-dataset (3 datasets × 3 seeds) | **~150 h** | ~35 GB | Head scaling is cheap (~6 h each); CIFAR-100 adds ~30 % overhead |
| **C** | Attn-linear ensemble (3 seeds × 2 datasets) + all-linear (3 seeds) + ImageNet-100 (3 seeds, 100 epochs) + Tiny-ImageNet (conditional) | **~280 h** | ~80 GB | ImageNet-100 is the dominant cost; if excluded, drops to ~130 h |
| **D** | κ sweep (5 values × 3 seeds) + 3rd-order (3 seeds) + piecewise (3 seeds) + cross-sim (2 frameworks × 3 seeds) | **~140 h** | ~30 GB | CrossSim replication is CPU-light; AIHWKIT adds ~20 h |

### Shared Overhead (All Branches)

| Item | GPU-Hours | Purpose |
|:------|:---------:|:--------|
| Fresh-instance eval (10 instances × 5 MC passes × checkpoints) | ~10 h | Standardized across all branches |
| Statistical re-runs (n = 5 seeds for key claims) | +30 % | Applied to the primary claim only |
| NaN / crash recovery buffer | +15 % | Conservative margin for higher-order instability |

### Authorization Threshold

| Branch | Minimum Ask | Recommended Ask | Conditional Extension |
|:------:|:-----------:|:---------------:|:----------------------|
| A | 120 h | 180 h | +60 h if envelope goes full-grid |
| B | 100 h | 150 h | +50 h for FPGA co-design pre-study |
| C | 180 h | 280 h | +100 h for ImageNet-1k (if 100 succeeds) |
| D | 100 h | 140 h | +40 h for measured-data calibration |

---

## 4. Timeline — 2-Week Round Q Shape

All branches follow the same phase structure; only the contents of Codex GPU slots change.

```
Day:  1   2   3   4   5   6   7   8   9  10  11  12  13  14
      ├─────┤ └─┬─┘ └───────┬───────┘ └─┬─┘ └───────┬───────┘
      Phase α   Phase β       Phase γ       Phase δ
```

### Phase α — Days 1–3: Branch Selection + Infrastructure

| Agent | Activity |
|:------|:---------|
| **Claude** | Ratify branch selection from CX-J1b/c/d data; broadcast canonical assignment |
| **Codex** | Checkout Round Q branch; run 3-epoch smoke for the chosen experiment path; verify NaN-free |
| **Kimi** | Stage paper skeleton for the selected branch (reuse Round P skeleton if applicable) |
| **Gemini** | Produce 1-page technical spec for the branch's flagship experiment |

### Phase β — Days 4–9: Core Experiments + Manuscript Drafting

| Agent | Branch A | Branch B | Branch C | Branch D |
|:------|:---------|:---------|:---------|:---------|
| **Codex** | Higher-order sweep + cross-arch | QKV-ensemble + head scaling | Attn-linear + ImageNet-100 pilot | κ sweep + 3rd-order pilot |
| **Kimi** | Theory paper §1–§4 draft | QKV paper §1–§4 draft | Deployment paper §1–§4 draft | Surrogate paper §1–§4 draft |
| **Gemini** | Formal proof + envelope spec | Hardware-cost model | EDP + FPGA plan | Physical κ mapping |

### Phase γ — Days 10–12: Analysis + Figure Lock

| Agent | Activity |
|:------|:---------|
| **Codex** | Fresh-instance eval; statistical report; checkpoint inventory update |
| **Kimi** | Results section draft; figure captions; table formatting |
| **Gemini** | Figure generation (vector); proof sketches / hardware tables |

### Phase δ — Days 13–14: Integration + Round R Preview

| Agent | Activity |
|:------|:---------|
| **Claude** | Phase-δ audit; manuscript completeness gate; Round R scope preview |
| **Kimi** | Full draft compile; bibliography consistency; cover letter draft |
| **Gemini** | Red-team review; hostile-review simulation; industrial brief |
| **Codex** | Final checkpoint bundle; reproducibility manifest; data release prep |

### Gantt by Branch

```
Branch A (Theory + Higher-Order)
Day  1  2  3  4  5  6  7  8  9  10 11 12 13 14
Codex [smoke][====higher-order sweep====][cross-arch][eval]
Kimi  [skeleton========][draft §1-4=============][§5-8==][compile]
Gemini[proof spec][formal structure][envelope====][red team]

Branch B (QKV Engineering)
Day  1  2  3  4  5  6  7  8  9  10 11 12 13 14
Codex [smoke][==QKV ensemble===][head scale][cross-ds][eval]
Kimi  [skeleton========][draft §1-4=============][§5-6==][compile]
Gemini[hw cost spec][model========][patent scan][red team]

Branch C (All-Linear Deployment)
Day  1  2  3  4  5  6  7  8  9  10 11 12 13 14
Codex [smoke][=attn linear=][all-linear][ImageNet-100====][eval]
Kimi  [skeleton========][draft §1-4=============][§5-8==][compile]
Gemini[EDP spec][model========][FPGA plan][red team]

Branch D (2nd-Order Surrogate)
Day  1  2  3  4  5  6  7  8  9  10 11 12 13 14
Codex [smoke][===κ sweep===][3rd-order][piecewise][cross-sim][eval]
Kimi  [skeleton========][draft §1-4=============][§5-7==][compile]
Gemini[physical map spec][κ→OPECT fit][calibrator][red team]
```

---

## 5. Risk — What If None of the Branches Pan Out?

The "all three ~30 %" outcome is **not** a failure state—it is Branch A, the scientifically strongest position. However, four genuine risk scenarios require contingency planning:

### Risk 1: Inconclusive Results (Ambiguous Zone)

**Scenario:** J1b/c/d land in the 35–45 % range—above the 30 % cluster but below the 50 % success threshold. The ceiling is softened but not broken.

**Mitigation:**
- Extend Round Q by 3 days with a **power-analysis sweep**: increase n from 3 to 5 seeds and re-test the best-performing condition.
- If the mean shifts above 50 % with tighter CI, upgrade to the corresponding branch.
- If the mean stays ambiguous, default to **Branch A (theory)** but soften the formal claim from "hard ceiling" to "soft barrier with steep diminishing returns."

### Risk 2: Implementation Failure (NaNs / Bugs)

**Scenario:** Higher-order surrogate (J1d) experiences gradient instability despite NaN guards; QKV-linear (J1b) path has shape-mismatch bugs that consume the GPU window without producing data.

**Mitigation:**
- **Pre-staged smoke tests** (Day 1–3 of every branch) are mandatory. No full run begins without a 3-epoch loss-curve sanity check.
- **Fallback experiment:** If the flagship experiment is blocked, pivot to the next branch in priority order (D → C → B → A) using already-working code paths.
- **Code freeze rule:** No new `analog_layers.py` refactors after Day 2 of Round Q. Only hyperparameter sweeps and config changes.

### Risk 3: Resource Unavailability (GPU Window Lost)

**Scenario:** The A100/RTX 5070 Ti is preempted, under maintenance, or reallocated to a higher-priority project before Round Q completes.

**Mitigation:**
- **Checkpoint-every-epoch policy** is already in place. Any interrupted run resumes from the latest checkpoint without loss.
- **Priority-ranked task list:** Within each branch, tasks are ordered so that the first 3 tasks alone produce a publishable minimum viable result. Remaining tasks are "nice to have."
- **Cloud fallback:** Budget预留 ¥2,000 for AutoDL / Vast.ai emergency rental if local GPU is offline >48 h during Round Q.

### Risk 4: Negative Result Is Rejected by Reviewers (Branch A Risk)

**Scenario:** Branch A produces a rigorous negative result, but journal reviewers dismiss it as "not a contribution" or demand a positive engineering fix.

**Mitigation:**
- **Pre-positioning in Round P:** The rebuttal MASTER and defense Q-bank already contain "negative result as contribution" framing. Round Q deepens this with formal proof structure.
- **Dual-audience manuscript:** Branch A paper is written for *Nature Electronics* (device-circuit-system audience) with a mathematical appendix for theory reviewers. The device audience values fundamental limits; the theory audience values formal statements.
- **Escape hatch:** If Branch A is rejected, the higher-order surrogate data (Task A1) is spun into a standalone short paper for MLSys or ICLR Workshop, reframed as "surrogate calibration methodology" rather than "negative result."

### Risk 5: Measured Data Arrives Mid-Round Q

**Scenario:** The lab delivers measured OPECT device profiles during Round Q, making simulation-only claims suddenly appear stale.

**Mitigation:**
- **Immediate fold-in rule:** Measured data always takes priority. Round Q pauses; a 48-hour calibration sprint (κ fitting, profile ingest, single-seed validation) is inserted.
- If measured data confirms the simulation prediction, it **strengthens** whichever branch is active (simulation-to-hardware closure is a major contribution).
- If measured data contradicts the simulation, Round Q pivots to **measured-data-first** mode: the branch selection is re-evaluated with real profiles.

---

## 6. Gate Checklist — Day 14 Decision

Before authorizing Round Q, confirm:

- [ ] CX-J1b/c/d raw `.json` results are on disk and peer-reviewed by Claude.
- [ ] Branch selection follows D → C → B → A priority.
- [ ] GPU hours for the chosen branch are reserved / confirmed available.
- [ ] 3-epoch smoke script for the chosen branch has been run and passed.
- [ ] Round P deliverables (thesis v1.0, NC bundle v3, defense slides v2) are archived and will not be reopened during Round Q.
- [ ] User has been notified of the branch choice and compute ask.

---

*End of brief. This document is locked until CX-J1b/c/d results land. Any agent modifying this file before results are available must append a justification block below this line.*
