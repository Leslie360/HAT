# CODEX CROSS-REVIEW — Kimi THEORY-1 and Gemini G-AUDIT-CODE
**Date:** 2026-04-24
**Reviewer:** Codex
**Scope:** Kimi THEORY-1, Kimi cross-review, Gemini G-AUDIT-CODE, Gemini cross-review, current M-series evaluation path
**Status:** Delivered; no code patch applied in this pass

---

## 0. Executive Verdict

1. **Gemini's ADC bypass finding is materially correct for the current M-series path.** `AnalogLinear.forward()` and `AnalogConv2d.forward()` do not call `ADCQuantizer`; `eval_fresh_instances_postfix.py` calls `run_mc_eval()` directly, and `run_mc_eval()` does not install `ADCQuantHookManager`. Kimi is correct that hook-based ADC support exists, but it is optional and is not active in the current fresh-eval runner. Therefore M-series results must be described as **conductance quantization + D2D/C2C/NL + float output accumulation**, not full ADC-quantized inference.
2. **Kimi THEORY-1 is useful but not integration-ready without edits.** The implicit-regularizer derivation is a good narrative anchor, but several statements must be softened or zoned before Claude integrates: unzoned empirical numbers, over-strong "exact analogy" wording, and an assumption about C2C independence that is not generally true for proportional-noise code paths.
3. **Gemini's 1<NL<2 numerical-stability warning is valid for `analog_layers.py` second-order STE.** Current M-series at `NL=2.0` is not affected; future sweeps crossing `1<NL<2` are unsafe unless guarded.
4. **Kimi underestimates the ADC issue.** The claim that missing ADC causes only `~0-1pp` optimistic bias is not established by evidence. ADC range calibration, DNL, and clipping can be benign or non-benign depending on range and layer distribution; this needs either a caveat or an ablation.

---

## 1. Source-Grounded Checks

### 1.1 Config-sharing fix is present locally

- `analog_layers.py:1367-1409` copies the top-level config and passes `config=copy.copy(config)` into each replacement layer.
- `analog_layers_ensemble.py:1106-1148` does the same.
- `analog_layers.py:1456-1503` and `analog_layers_ensemble.py:1195-1242` also use copied configs in ResNet conversion.

**Verdict:** Remote's config-sharing fix is applied in the local code currently under review.

### 1.2 ADC is not in the default analog forward path

- `analog_layers.py:600-619` computes `G_pos/G_neg`, applies retention/noise, rescales `W_eff`, then returns `F.linear(x, W_eff, bias)`.
- `analog_layers.py:808-823` follows the same pattern for `F.conv2d`.
- `analog_layers_ensemble.py:395-414` and `analog_layers_ensemble.py:561-569` follow the same default pattern.
- `ADCQuantizer` exists at `analog_layers.py:959-1025` and `analog_layers_ensemble.py:704-770`, but is not invoked by those forward methods.

**Verdict:** Gemini's core observation is correct for default training/evaluation.

### 1.3 ADC hook support exists, but current M-series does not enable it

- `inference_analysis_utils.py:576-621` defines `ADCQuantHookManager`, which attaches `ADCQuantizer` via forward hooks.
- `inference_analysis_utils.py:491-528` defines `run_mc_eval()`, and it only calls `evaluate_once()` repeatedly; it does not calibrate ADC ranges or enter `ADCQuantHookManager`.
- `eval_fresh_instances_postfix.py:106-146` loads a bundle, pushes NL/noise settings, resamples D2D, then calls `run_mc_eval()` directly.

**Verdict:** Kimi's nuance is partly right: ADC is implemented and can be injected by hooks. But for the current M-series fresh eval, no hook is active. Gemini's statement should be refined from "ADCQuantizer is completely omitted from the codebase" to "ADCQuantizer is omitted from the default M-series inference path."

### 1.4 Second-order stability risk is real but not current-M-series-active

- `analog_layers.py:271-277` computes `pow(ratio, nl - 2.0)` when second-order STE is enabled.
- For `1 < nl < 2`, the exponent is negative; with `ratio.clamp_min(1e-8)`, this can amplify boundary gradients by orders of magnitude.
- Current M-series uses `NL=2.0`, so exponent `0.0` avoids this path's explosion.
- `analog_layers_ensemble.py` is marked deprecated and lacks second-order STE, so this specific second-order issue is in `analog_layers.py`.

**Verdict:** Valid latent bug. It should be fixed before any future `1<NL<2` or mixed-NL sweeps, but it does not invalidate the current `NL=2.0` M-series.

---

## 2. Review of Kimi THEORY-1

### Passes

- The central distribution-matching idea is coherent: Ensemble HAT optimizes an expectation over D2D maps rather than a single fixed map.
- The second-order expansion correctly gives a variance-weighted sensitivity penalty under small, zero-mean, independent multiplicative D2D assumptions.
- The Methods draft is compact and mostly usable as a sidecar once labels and caveats are adjusted.

### Required Fixes Before Claude Integration

1. **Unzoned empirical numbers inside theory note.** `S_theory_ensemble_hat.tex` contains empirical claims such as `88.41%` vs `86.16%`, `-1.76pp`, `-4.20pp`, and Discussion sidecar contains `76pp/78pp`. Final Push requires every number to map to `NARRATIVE_PIVOT` zone 3A/3B/3C. Kimi's completion report says no numeric results were claimed from theory alone, but the file does contain numeric empirical claims.
2. **C2C independence assumption is too broad.** The theory note says C2C can be absorbed into `L0` because it is independent. In the proportional-noise implementation, `_apply_noise()` adds D2D first and then samples C2C using the post-D2D `W_eff` as the reference. That couples C2C magnitude to D2D for proportional mode. The theory should explicitly limit the derivation to independent additive C2C, uniform noise, or a D2D-dominant approximation.
3. **"Exact analogy" wording is too strong.** The result uses a Taylor expansion and Gauss-Newton/Fisher approximation. The analogy to Wager dropout is structurally useful, but should be phrased as "structural analogue" rather than "exact" unless the assumptions are listed immediately.
4. **Supplementary file is standalone LaTeX.** Gemini's note is correct: Claude must strip `\documentclass`, package imports, `\begin{document}`, and `\end{document}` before inclusion.
5. **Equation label migration needs one owner.** Kimi introduced `eq:hat-ensemble-distribution`; Claude should either alias it to existing `eq:hat-ensemble` references or migrate all references in one pass.

**Codex verdict on Kimi:** Accept as a strong draft, not final manuscript material. It needs caveat tightening and zone labeling before integration.

---

## 3. Review of Gemini G-AUDIT-CODE

### Confirmed Findings

1. **ADC bypass in default forward path:** confirmed with refinement above.
2. **Second-order `1<NL<2` gradient risk:** confirmed.
3. **Config metadata save path:** checkpoint provenance fields are present; current fresh JSONs include `commit_hash`, `git_worktree_dirty`, `cuda_device_name`, `pytorch_version`, `allow_eval_nl_override=false`, and empty mismatch lists.

### Findings That Need Rewording

1. **"Pure float32 MAC" is too broad.** The layers still quantize weights into conductance states via STE and inject D2D/C2C noise into `W_eff`. The missing piece is ADC quantization of output currents and digital post-ADC scale recovery, not all analog modeling.
2. **Scale recovery critique depends on the chosen abstraction.** Applying `_conductance_to_weight_scale()` before `F.linear/F.conv2d` is consistent with a differentiable effective-weight abstraction. It is not physically equivalent to post-ADC digital scaling when ADC quantization is active. So this is best described as an abstraction limitation, not automatically a mathematical bug.
3. **AMP decorator warning is plausible but secondary.** Critical pow regions are already wrapped in fp32 for weight-to-conductance forward. The second-order backward still deserves a guard, but the immediate hard failure mode is the negative exponent, not merely missing decorators.

**Codex verdict on Gemini:** Audit is valuable and caught a real fidelity gap. The report overstates the issue in places; keep the finding, refine the language.

---

## 4. Review of Kimi Cross-Review

Kimi correctly verified that ADC hook support exists, but drew one unsupported quantitative conclusion:

- **Unsupported:** "optimistic bias ~0-1pp, not fatal."
- **Reason:** No ADC-on vs ADC-off ablation is cited for M-series. Hook calibration uses output ranges; noisy output tails and DNL/clipping can change effects. The bias may be small, but it is not proven.

Recommended replacement wording:

> Current M-series numbers are ADC-off/default-forward results. ADC hook support exists and should be treated as a separate fidelity dimension. Until an ADC-on ablation is run, do not assign a pp-level bias magnitude.

---

## 5. Review of Gemini Cross-Review

Gemini's cross-review is directionally correct but should not force an immediate full rerun. Final Push gives months of buffer and forbids new experiments except the already dispatched fresh eval. The right sequencing is:

1. Finish clean M-series fresh eval and plots as dispatched.
2. Mark those results explicitly as ADC-off/default-forward 3C evidence.
3. Ask Claude to decide whether ADC-on ablation becomes a new task after the current queue completes.

---

## 6. Immediate Actions Recommended

1. **For Claude:** Decide whether to document ADC-off default forward as a limitation now or authorize a small ADC-on ablation later.
2. **For Codex:** After current M-series fresh eval finishes, update `CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md` with an explicit ADC-off/default-forward caveat and provenance paragraph.
3. **For Kimi:** Before K-DRAFT-v3 integration, remove or zone every empirical number in `S_theory_ensemble_hat.tex` and soften "exact analogy" language.
4. **For Gemini:** No rewrite needed; keep error-finding role. If asked for follow-up, audit whether ADC hook calibration is physically aligned with the intended ADC range/scale recovery story.
5. **For future code maintenance:** Add a safety guard or hard error for second-order STE when `1 < abs(NL) < 2`, before any future sweeps in that interval.

---

## 7. Current GPU/Eval Note

At the time of this review, `CX-FRESH-EVAL-MSERIES` clean runner is still active in two-way parallel mode on `CX-M5/CX-M6`, and `CX-PLOT-REFRESH` is waiting for completion. This review does not modify running code or checkpoint state.
