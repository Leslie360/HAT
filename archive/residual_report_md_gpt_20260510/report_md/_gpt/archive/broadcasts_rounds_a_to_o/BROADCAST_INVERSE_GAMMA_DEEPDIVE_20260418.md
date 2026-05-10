# BROADCAST: Inverse-Gamma Frontend Elevated to Core Contribution

**Date:** 2026-04-18
**Decision Authority:** User (Qiao)
**Status:** ✅ PHASE 1 COMPLETE — E3 RUNNING — PAGE TARGET MET

---

## Executive Decision

The inverse-gamma frontend compensation method (implemented as `InverseGammaPreprocessor` + `PhotocurrentSimulator` in `analog_layers.py`, experimentally validated in A2.3 with 5×4 γ/I_dark sweep) is **elevated from a framework component to a named core contribution** of the present manuscript. User confirms this is original work and authorizes full narrative + experimental deepening.

---

## Literature Confidence

Cross-web search (2026-04-18) confirms:

| Component | Prior Art Status |
|-----------|-----------------|
| Sublinear photoresponse $I \propto P^\beta$ ($\beta<1$) | Known physics (perovskite/organic phototransistor literature) |
| Shot noise $\propto I_{\text{photo}}$ | Basic photodetector physics |
| Gamma correction / inverse gamma | Standard ISP (digital cameras, displays) |
| **Inverse-gamma + shot-noise-aware SNR + task-level accuracy evaluation as a CIM system design method** | **No prior publication found** |
| **Bridging photoresponse nonlinearity to ViT attention-map degradation** | **No prior publication found** |
| **Explicit "dark-region recovery vs bright-region noise amplification" as a design trade-off** | **No prior publication found** |
| **Replaceable JSON-profile parameterization of γ_phys for CIM simulation** | **No prior publication found** |

**Verdict:** The method is defensibly original. It does not claim discovery of new physics; it claims **systematic task-level evaluation of a physically-motivated compensation strategy** in an organic optoelectronic CIM context.

---

## Phase 1: Manuscript Refactor — ✅ COMPLETE

### 1.1 Introduction — 3→4 Contributions ✅
**File:** `paper/latex_gpt/sections/01_introduction.tex`

Done. Four-contribution structure live:
> 1. Profile-driven first-order behavioral workflow.
> 2. **Two-stage hierarchy**: sub-6-bit ADC cliff ($S_{\text{ADC}}=0.98$) + **inverse-gamma frontend** (+5.8 pp at $\gamma_{\text{phys}}=2.0$) with shot-noise trade-off.
> 3. Ensemble HAT (10.00% → 86.37 ± 1.54%).
> 4. Literature-profile zero-shot transfer + nonlinear write localization.

### 1.2 Abstract ✅
**File:** `paper/latex_gpt/sections/00_abstract.tex`

Added: "inverse-gamma compensation and shot-noise trade-off analysis"

### 1.3 Results §5.3 — Expanded ✅
**File:** `paper/latex_gpt/sections/05_results.tex`

Expanded from 1 sentence to data-driven paragraph with γ-scan interpretation, +5.8 pp quantification, and shot-noise trade-off note.

### 1.4 Supplementary — Table S5 + Theory Notes ✅
**File:** `paper/latex_gpt/supplementary.tex`

- **Table S5** (`tab:supp-frontend-gamma-scan`): Full 5×4 γ_phys × I_dark accuracy matrix
- **Supplementary Note `note:frontend-theory`**: T1 (ISP distinction) + T3 (ViT attention sensitivity)
- **Supplementary Note `note:optimal-gamma`**: T2 derivation — optimal γ_comp* < 1/γ_phys under shot noise

### 1.5 Page Reduction — Main 20→14 pages ✅

Moved to supplementary to hit Nature Communications target:
- `fig:system-architecture` → `fig:supp-system-architecture`
- `tab:fp32-baselines` → `tab:supp-fp32-baselines`
- `tab:result-summary` → `tab:supp-result-summary`
- `eq:nl-surrogate` → `eq:supp-nl-surrogate`
- Discussion T1/T3 theory → supplementary notes

**Current:** Main = 14 pages, Supplementary = 21 pages.

---

## Phase 2: v2 Deep-Dive — IN PROGRESS

### 2.1 Experimental Expansion

| ID | Experiment | Status | Notes |
|----|-----------|--------|-------|
| E1 | Cross-architecture γ scan | ⏸️ Pending | Time permitting |
| E2 | Cross-dataset γ robustness | ⏸️ Pending | Time permitting |
| E3 | **Learnable compensation exponent** | 🔄 **RUNNING** | 100 epochs, γ_phys=2.0, CIFAR-10. PID 43322 on WSL GPU. |
| E4 | AIHWKIT/CrossSim frontend sanity check | ⏸️ Pending | Low priority |

**E3 Details:**
- Script: `scripts/_gpt/run_learnable_gamma_compensation_gpt.py`
- Log: `logs/learnable_gamma_gpt/e3_run_20260418_110008.log`
- Status: Fixed variant (γ_comp=0.5) training in progress
- Expected output: fixed vs learnable vs none comparison JSON

### 2.2 Theoretical Expansion — ✅ COMPLETE (in supplementary)

| ID | Theory | Status | Location |
|----|--------|--------|----------|
| T1 | Distinguish from ISP gamma correction | ✅ Done | Supplementary Note `note:frontend-theory` |
| T2 | Optimal compensation exponent | ✅ Done | Supplementary Note `note:optimal-gamma` |
| T3 | Attention sensitivity to frontend | ✅ Done | Supplementary Note `note:frontend-theory` |
| T4 | Profile-aware SNR closed form | ⏸️ Partial | Analytical curves in `report_md/images/a23_snr_vs_intensity.png` |

---

## Locked Data Assets (Do Not Regenerate)

| Asset | Location | Key Value |
|-------|----------|-----------|
| A2.3 accuracy matrix | `report_md/json/a23_experiment_results.json` | γ=2.0, I_dark=10pA: raw=84.04%, comp=89.85%, Δ=+5.81pp |
| A2.3 γ=2.0 average | Same JSON | Δ ≈ +5.5 pp across I_dark sweep |
| V6 Tiny-ViT checkpoint | `compute_vit/checkpoints/V6_hybrid_hat_with_physical_frontend_best.pt` | HAT-trained with frontend on |
| SNR curves | `report_md/images/a23_snr_vs_intensity.png` | Analytical, γ_phys=0.5,0.7,1.0,1.5,2.0 |

---

## Risk Assessment

| Risk | Mitigation | Status |
|------|-----------|--------|
| Reviewer claims "inverse gamma is just standard ISP" | T1 explicitly distinguishes ISP gamma (perceptual) from photocurrent linearization + noise-aware task evaluation. | ✅ T1 in supplementary |
| Reviewer claims "sublinear photoresponse is known physics" | Response: we claim **systematic task-level evaluation of compensation** in CIM context. | ✅ Narrative clear in intro/results |
| Overclaiming on "optimal" compensation | Manuscript uses "restores accuracy" not "optimal". T2 framed as theoretical follow-up. | ✅ T2 in supplementary, not main text |
| Narrative shift destabilizes other contributions | 4-contribution structure clean; no overflow. | ✅ Verified |

---

## Next Actions

1. ⏳ **Wait for E3 completion** (~2–3 hours). Result will validate/refute T2 prediction.
2. 📋 **Bib audit** (20+ weak entries from `KIMI_DISPATCH_20260417_bib_finish_gpt.md`) — pending, low priority.
3. 📝 **Cover letter finalization** — update to reflect 14-page main + 21-page supplementary.
4. 🔍 **Figure caption audit** — `fig10_zero_shot_transferability` caption mismatch (claims Ensemble HAT recovery but figure shows Standard HAT collapse) — needs fix.

---

**Signed off by user:** "我觉得完全可以深挖，时间充足放心"
**Broadcast by:** Kimi Code CLI → Claude (handoff after Codex quota exhausted)
**Last Updated:** 2026-04-18 11:05 CST
