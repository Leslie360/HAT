# Pre-Submission Checklist

**Target journal:** Nature Communications
**Current state:** CLAUDE-A FINAL Option B locked, all-linear COMPLETE, attn_proj-only RUNNING, R1–R4 + extensions landed, guard script 16/16 PASS.

---

## Locked Numbers Consistency

- [x] H1 `S_ADC=0.98` — verified by `scripts/_gpt/check_locked_numbers.py` (16/16 PASS)
- [x] H2 `S_D2D=0.92` — verified by same
- [x] H3 `+5.8 pp at γ_phys=2.0` — verified `a23_experiment_results.json` key `2.0_1e-11`
- [x] H4 `Ensemble HAT 86.37±1.54%` — verified `v4_ensemble_results_gpt.json`
- [x] H5 `10.00%` standard-HAT collapse — verified `fresh_instance_eval.json`
- [x] H6 `27.72±0.82%` NL=2.0 — verified `v4_nl2_hat_eval_results_gpt.json`
- [x] H7 `88.53±0.08%` OPECT — verified `literature_profile_eval.json`
- [x] H8 `98.06%` FP32 baseline — verified `tinyvit_v1_results_gpt.json` (NOTE: 97.48% single-seed train best vs 98.06% 3-seed mean; manuscript uses 98.06% consistently)
- [x] L1 `87.79%` MLP-only NL mitigation — verified `v4_nl2_mlp_linear_comp_train_results_gpt.json`
- [x] L3 `51.65%` E3 learnable γ — verified `learnable_gamma_20260418_110011_g2.0_s42.json`
- [x] Energy claims (`~11×`, `~60% digital`, `~88% analog`) — verified `analog_layers.py` EnergyProfiler

> **Guard script:** `scripts/_gpt/check_locked_numbers.py` — 16/16 PASS on 2026-04-18.

---

## Manuscript Content

### R1 Abbreviations (✅ Done)
- [x] A1 ADC — abstract
- [x] A2 OPECT — abstract
- [x] A3 HAT — abstract
- [x] A4 D2D — abstract
- [x] A6 NL — abstract
- [x] A7 LTP/LTD — §3
- [x] A8 CNN — §1
- [x] A9 ViT — §1
- [x] A10 MLP — §1
- [x] A11 SRAM — §1
- [x] A13 MC — §5
- [x] A14 IR drop — §1
- [x] A16 DNTT — §3
- [x] A18 PCM/RRAM — Fig 10 caption
- [x] A21 LSB — supplementary
- [x] A23 SNR — supplementary

### R2 Data Rigor (✅ Done)
- [x] D1 OPECT 88.53% → 88.53±0.08% (n=10)
- [x] D2 97.39% V2 zero-noise → 97.39±0.00% (n=10 deterministic evaluations) in §5.1
- [x] D3 +5.8 pp → single-seed deterministic evaluation
- [x] D4 p<10⁻¹⁵ → one-sample t-test, n=10
- [x] D5 Cadence values 88.41/87.18/86.16 → supplementary Fig caption labels as exploratory single-run; spread not available by design
- [x] D6 Retention plateau "near 79%" → cites Supplementary Fig.~\SuppFigRetention with full numerics (79.13--79.51%)
- [x] D7 Best-checkpoint rule disclosure → §5.1: "All accuracy values reported for noisy and HAT deployments are best-checkpoint results unless otherwise stated."
- [x] D8 Compound stress 89.61% → "single-run compound stress test" in §6
- [x] D9 CrossSim 14.43 pp → corrected to actual n=1 clean / n=3 noisy runs with explicit 1,000-image subset disclosure in §6 and Supplementary Note SX.Y
- [x] D10 seed policy → "independently per grid point"
- [x] D11 Zhang C2C-insensitivity identical rows → 08_appendix.tex explicitly defends as stability result, not copy-paste artifact
- [x] D12 Energy placeholder caveat → survives in §3, §6, supplementary, cover letter
- [ ] D13 Fig 4 mixed error bars — caption already discloses; **reviewer-facing risk**. Options: (a) keep with current caption, (b) split panel, (c) compute MC for bare cells. **Decision deferred to post-attn_proj.**

### R3 Calculation Clarity (✅ Done)
- [x] C1 Scale-recovery branch usage → §3: "standard-calibration branch default; retention-recalibration only for V8"
- [x] C2 Shot-noise proportionality constant → §3: "proportionality coefficient absorbed into per-profile frontend calibration"
- [x] C3 Ensemble HAT expectation estimator — "one map per epoch"
- [x] C4 Sobol estimator — "directly from grid of MC means"
- [x] C5 p<10⁻¹⁵ test name — one-sample t-test
- [x] C6 Gradient-scaling definition — "∝ |G|^(NL−1)"
- [x] C7 Hybrid operator list — analog vs digital explicit
- [x] C8 Energy model equation → supplementary §Energy Profiler Implementation: full $E_{\mathrm{total}}$ decomposition with $E_{\mathrm{MAC}}$, $E_{\mathrm{ADC}}$, $E_{\mathrm{DAC}}$, $E_{\mathrm{digital}}$, $E_{\mathrm{buffer}}$
- [x] C9 MC seed reuse across models → §3: "seeds are not shared across the grid or across models"
- [x] C10 Fresh-instance p(M) shape → §3: "i.i.d. Gaussian draw $M' \sim \mathcal{N}(0, \sigma_{\mathrm{D2D}}^2)$"
- [x] C11 "Consistent ~7 pp jump" → §5.3: "mean across all seven D2D levels; per-row jump ranged from 5.8 to 8.1 pp"

### R4 Physical Mapping (✅ Done)
- [x] P1 IR drop — enumerated in Limitations
- [x] P2 Sneak paths — enumerated in Limitations
- [x] P5 Temperature — enumerated in Limitations
- [x] P3/P4 Spatially correlated D2D + heavy-tail — grouped under "noise-model refinements"
- [x] Outlook: "circuit-aware layer explicitly deferred"

---

## Figures & Tables

- [x] Fig 1 — system-architecture figure (moved to supplementary; caption cross-ref verified)
- [x] Fig 2 — retention curve (79% plateau wording verified with full numerics)
- [x] Fig 3 — contour map (S_ADC/S_D2D values verified)
- [x] Fig 4 — cross-dataset accuracy (mixed error-bar disclosure in caption; D13 decision pending)
- [x] Fig 5 — HAT recovery (10-run MC vs single-run labels verified)
- [x] Fig 6 — frontend compensation (γ_phys=2.0, +5.8 pp verified)
- [x] Fig 7 — case-study transfer (88.53±0.08% label verified)
- [x] Table S5 — γ_phys × I_dark sweep (verified 5×4 grid: γ_phys ∈ {0.5,0.7,1.0,1.5,2.0} × I_dark ∈ {10pA,100pA,1nA,10nA})
- [ ] Table SX.N — **NEW** group-wise NL ablation (pending attn_proj completion for row e)

---

## Supplementary

- [x] Verify `tikz` package loads correctly (added to `supplementary_main.tex`)
- [x] Table tab:adc-nonideality — LSB expansion (A21) verified
- [x] Fig S3 — ADC sweep on ConvNeXt
- [x] Fig S5 — cadence scan
- [x] Fig S6 — fresh-instance robustness (p<10⁻¹⁵ caption verified)
- [x] Fig S7/S8 — frontend theory + SNR curves
- [x] Fig S9 — Sobol sensitivity
- [ ] Table tab:provenance — cross-link to PROVENANCE_AUDIT (nice-to-have)

---

## Submission Package

- [x] Main PDF: 15 pp (verified compilation)
- [x] Supplementary PDF: 21 pp (verified compilation)
- [x] Cover letter PDF: 2 pp (verified compilation)
- [ ] Source data for all figures
- [ ] Code snapshot / reviewer archive (see `REPRODUCIBILITY_PACKAGE_PLAN`)
- [ ] Checkpoints tier A/B/C inventory (see `CHECKPOINT_INVENTORY_20260418.md`)

---

## Blockers (must resolve before submission)

1. ~~**all-linear NL mitigation**~~ — ✅ COMPLETE (87.49% best @ epoch 59). Table SX.N row (f) finalized.
2. **attn_proj-only NL mitigation** — 🔄 RUNNING. Started 2026-04-18 ~17:00. ETA ~20 h remaining. Finalizes Table SX.N row (e).
3. ~~**CLAUDE-A final decision**~~ — ✅ Option B LOCKED (supplementary ablation, not 5th contribution).
4. ~~**3-seed error bars for MLP-only and QKV-only**~~ — Thesis defense priority; submission nice-to-have.

---

## Non-blocking nice-to-haves

- [x] `check_locked_numbers.py` guard script — 16/16 PASS
- [ ] PROVENANCE_AUDIT Chinese translation for thesis defense
- [ ] `report_md/_gpt/_closed/` directory organization (post-submission)
- [ ] E5 layer-wise gamma sensitivity (thesis-only priority)
- [ ] E6 γ×NL joint sweep (thesis-only priority)
