# Experiment Roadmap: All Proposed Additions (R11D + Proactive Sprint + Future Rounds)
**Date:** 2026-04-26
**Author:** Claude (Chief Architect)
**Scope:** Complete consolidated list of every proposed experiment, analysis, and integration task across R11D Path C, Proactive Sprint Plan, and Round 4-8 roadmap

---

## Part A: R11D Path C — AIHWKit Stress Regime Exploration

*Source: `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md`*

### Completed ✅

| Track | Config | Train Best | Fresh Mean | Status |
|:---|:---|---:|---:|:---|
| R11D-1 | 4-bit, σ=0.10 | 15.01% | **14.64 ± 0.11%** | ✅ COMPLETE |
| R11D-2 | 8-bit, σ=0.20 | 87.60% | **87.52 ± 0.05%** | ✅ COMPLETE |
| R11D-3 | 8-bit, σ=0.30 | 87.57% | **87.40 ± 0.05%** | ✅ COMPLETE |

### Key Finding
AIHWKit collapses **only at 4-bit** (14.64%). At 8-bit, σ=0.10→0.30 changes fresh by only 0.12 pp. **Precision, not noise, is the lever.** Path B (method-superiority at 4-bit) is confirmed.

### Pending / Queued

| Track | Description | Owner | GPU-h | Status |
|:---|:---|:---|---:|:---|
| R11D-4 | AIHWKit PCM device model (realistic non-linear pulse-update) | DS | ~15 | QUEUED |
| R11D-5 | Cadence ablation: code-level comparison of AIHWKit per-minibatch vs our per-batch | Kimi | 0 | QUEUED |
| R11D-6 | Ensemble HAT retrained with per-minibatch cadence (matches AIHWKit schedule) | DS | ~12 | CONDITIONAL (on R11D-5) |
| R11D-T1 | Theory: per-batch (Wager-style L2) vs per-epoch (SAM-style sharpness) | Kimi | 0 | QUEUED |
| R11D-T2 | Method Operating Envelope Plot (all regimes visualized) | Gemini | 0 | PENDING DATA |

---

## Part B: Proactive Sprint — Depth Investment (12 Days)

*Source: `CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md`*

### Phase 1: Theory Deepening (Days 1-3, Kimi)

Add to Supp Note S-Theory:

1. **§S.7 Higher-order corrections** (1 page)
   - Third- and fourth-order moments under Gaussian D2D
   - Breakdown conditions: large σ, near-saturation weights

2. **§S.8 PAC-Bayes generalization bound** (2 pages)
   - McAllester-style bound over D2D-perturbed weights
   - Show tightness when posterior aligns with implicit gradient-L2
   - Implication: +76pp gap has theoretical floor

3. **§S.9 Flat minima connection** (1-2 pages)
   - Cite Hochreiter 1997 + Keskar 2017 + Foret 2021 (SAM)
   - Ensemble HAT ≈ SAM-style sharpness penalty along D2D direction (structural analogue)

4. **§S.10 Limitations** (0.5 page)
   - Heavy-tailed D2D breaks second-order
   - Spatial correlation: AR(1) via Fisher metric
   - Per-layer σ_D2D variation

**Deliverable:** `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` (~3500-4500 words)

### Phase 2: Empirical Mechanism (Days 1-5, Codex/DS)

All eval-only on existing checkpoints. **NO new training.**

| Job | Description | GPU-h | Deliverable |
|:---|:---|---:|:---|
| E1 | Hessian eigenspectrum (Hutchinson + Lanczos top-50) | ~2 | `figS_hessian_spectrum.{png,pdf}` |
| E2 | Loss landscape along D2D direction | ~1 | `figS_d2d_loss_landscape.{png,pdf}` |
| E3 | CKA similarity across M-series checkpoints | ~0.5 | `figS_cka_mseries.{png,pdf}` |
| E4 | Per-layer mismatch sensitivity (perturb one layer at a time) | ~2 | `figS_per_layer_sensitivity.{png,pdf}` |
| E5 | Checkpoint averaging (seeds 123+456) — likely negative result | ~0.5 | `figS_checkpoint_avg.{png,pdf}` |

**Total Phase 2 budget: ~6-8 GPU-h**

### Phase 3: Writing Polish (Days 4-7, Kimi)

1. Section opening/closing sentences audit
2. Discussion arc restructure: Diagnosis → Treatment → Mechanism → Implications
3. **Design rules callout** (boxed, end of §6): 5-7 actionable rules with quantitative thresholds
4. **Reproducibility cookbook** (Supp Note S-Reproducibility, ~3 pages)
5. Figure captions self-contained audit
6. Acknowledgments + Author contributions skeleton

### Phase 4: Defense Prep + Tooling Positioning (Days 7-10, Kimi)

**4A — Defense:**
- Update `KIMI_DEFENSE_BEAMER_20260423.tex`
- Update `KIMI_DEFENSE_QA_PREP_20260420.md` with post-fix numbers
- Slide-by-slide narration script

**4B — Tooling:**
- Expand CrossSim footnote → Supp Note S-Tooling
- Honest comparison: our framework vs CrossSim vs AIHWKit vs NeuroSim
- Cite Rasch 2023 as conceptual ancestor

### Phase 5: Sprint Integration (Days 10-12, Claude)

- Theory + empirical figures → Supp Note S-Theory
- Design rules → Discussion
- Reproducibility + tooling → supplementary
- Full pdflatex compile
- Final consistency grep

---

## Part C: Round 4-8 Roadmap — Gated Tasks

*Source: `CLAUDE_FORWARD_ROADMAP_20260425.md`*

### Trigger T1: 8×40GB Remote Returns

| Action | Owner | Description |
|:---|:---|:---|
| Cross-host parity review | Claude | 18 fresh-eval JSONs + master report |
| Decision rule application | Claude | Ensemble ≥ Standard + 50pp → promote §5.7 |
| Cross-arch supp section | Kimi | `S_cross_arch.tex` |

### Trigger T2: Work 2 KV-Cache Preliminary

| Action | Owner | Description |
|:---|:---|:---|
| QKV analog path extension | Codex | Extend `analog_layers.py` |
| Warm-start finetune | Codex | 5-10 epochs from V4 canonical |
| Fresh eval: Standard vs Ensemble on attention | Codex | ~3-4 days wall-clock |

### Trigger T3: PhD Measured D2D/C2C Data

| Track | Time | Description |
|:---|---:|:---|
| R-D0 (ingest) | 10 min | QQ plot + Gaussian/heavy-tailed check |
| R-D1 | 6-8 GPU-h | Ensemble HAT at measured D2D, 10×5 MC |
| R-D2 | 12-20 GPU-h | 63-point iso-accuracy map re-run |
| R-D3 | 20-30 GPU-h | Severe-NL Ensemble HAT at measured D2D, 3 seeds |
| R-D4 | 5 GPU-h | AR(1) spatial correlation with measured map |

---

## Part D: Simulator Upgrade Tasks (From Literature Survey)

| # | Feature | Priority | Code Change | Data Source |
|:---|:---|:---|:---|:---|
| 1 | `temperature_c` proxy | P0 | Add Arrhenius/polynomial sigma_d2d(T), tau(T) | Materials & Design 2025 |
| 2 | `max_cycles` decay | P0 | Add cycle counter + G_max narrowing | Science Advances 2025 |
| 3 | `noise_distribution` (lognormal) | P0 | Add torch.distributions.LogNormal option | Nature Communications 2022 |
| 4 | Read disturb acknowledgment | P1 | Text-only in Discussion | N/A (literature gap) |
| 5 | Spatial IR drop (position-dependent) | P1 | Replace rand_like with row/col gradient | Engineering approximations |
| 6 | Sneak path network | P2 | Coupled parasitic conductance model | Needs measured data |
| 7 | Hysteresis | P2 | P-E loop state variable | Needs measured data |

---

## Consolidated Priority Order

**This week (immediate):**
1. R11D-4 PCM (if GPU available after R11D-3) → ~15 GPU-h
2. R11D-5 cadence comparison text → Kimi, 0 GPU, ~4h
3. R11D-T1 theory addendum → Kimi, 0 GPU, ~1 day
4. Phase 2 E1-E5 empirical mechanism → Codex/DS, ~6-8 GPU-h

**Next week:**
5. Phase 1 theory deepening → Kimi, ~3 days
6. Phase 3 writing polish → Kimi, ~4 days
7. R11D-T2 envelope plot → Gemini, once R11D-4 data lands

**When triggers fire:**
8. 8×40GB cross-arch integration (T1)
9. PhD measured data ingest (T3)
10. Work 2 KV-cache (T2)

---

*Merged from: `CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md`, `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md`, `CLAUDE_FORWARD_ROADMAP_20260425.md`, and AGENT_SYNC literature survey actionable items.*
