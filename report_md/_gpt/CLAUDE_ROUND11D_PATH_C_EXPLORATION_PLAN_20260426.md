# CLAUDE ROUND-11D — Path C Exploration: AIHWKit at Severe-NL + Method-Comparison Map
**Date:** 2026-04-26 16:50 CST
**From:** Claude (Chief Architect)
**Trigger:** User decision: "Path C 比较好，我们应该更多探索"
**Authority:** This file
**Status:** ACTIVE — Multi-track exploration to find regime where Ensemble HAT > AIHWKit (or honestly accept that it doesn't)

---

## 0. The motivating finding

R10E result:
- AIHWKit (per-batch noise injection): **87.34 ± 0.14%** fresh-instance
- Ensemble HAT (our per-epoch resample): **86.16 ± 0.19%** fresh-instance
- AIHWKit beats us by 1.18 pp at canonical NL=1.0, σ=0.10, 8-bit ADC

User wants exploration. Two questions:
1. **Does AIHWKit collapse in any regime where Ensemble HAT survives?**
2. **What's the underlying mechanism difference between per-batch and per-epoch resampling?**

If we find a regime where Ensemble HAT wins → method-superiority story.
If we don't find → reframe via Path A as "two equivalent approaches; we contribute diagnosis + theory + substrate".

Either way: the exploration itself is publishable as a "comparison study under varied stress regimes".

---

## 1. Sub-tracks (5 + 1)

### R11D-1 — AIHWKit at matched 4-bit precision (DS, ~12 GPU-h)

**Why**: Current AIHWKit uses 8-bit (`inp_res=1/256`); our paper uses 4-bit. Apples-to-apples needs same precision.

**Spec**:
- Same config as R10E baseline but `cfg.forward.inp_res = 1.0/16` and `cfg.forward.out_res = 1.0/16` (4-bit)
- Train 100 epochs CIFAR-10 same recipe
- Fresh-eval 10 instances × 5 MC

**Hypothesis**: AIHWKit may collapse at 4-bit (paper-1's iso-accuracy 4-bit cliff for our Tiny-ViT shows ~10pp degradation; AIHWKit may degrade similarly or worse).

### R11D-2 — AIHWKit at high noise σ=0.20 (DS, ~12 GPU-h)

**Why**: Paper-1 iso-accuracy map shows D2D 20% breaks our system. Does AIHWKit handle it?

**Spec**:
- `cfg.modifier.std_dev = 0.20` (was 0.10)
- 100 epochs, CIFAR-10
- Fresh-eval at matching σ_D2D = 0.20

**Hypothesis**: AIHWKit per-batch noise might saturate at high σ; theoretical limit is σ < 0.5 for Wager-style implicit regularization to hold.

### R11D-3 — AIHWKit at extreme noise σ=0.30 (DS, ~12 GPU-h, conditional on R11D-2)

**Why**: If R11D-2 still strong, push to σ=0.30 (paper-1 system marginally collapses here).

**Spec**: Same as R11D-2 but σ=0.30. Fire only if R11D-2 still > 80%.

### R11D-4 — AIHWKit with PCM device model (DS, ~15 GPU-h)

**Why**: AIHWKit has built-in PCM/RRAM device models with realistic non-linear pulse-update. Closer to our NL=2.0 abstraction.

**Spec**:
- Use `aihwkit.simulator.presets.PCMPresetUnitCell` (from inference RPU configs)
- 100 epochs Tiki-Taka or AnalogSGD
- Fresh-eval matching device profile

**Hypothesis**: Realistic PCM device may break AIHWKit where ADD_NORMAL noise didn't.

### R11D-5 — Cadence ablation revisit with AIHWKit context (Kimi text + DS data, ~6 hours)

**Why**: Paper §5.7 reports our cadence ablation: per-epoch 88.41% / fixed 87.18% / per-batch 86.16%. **But AIHWKit per-batch got 87.34%** — better than our per-batch (86.16%). What's the difference?

**Spec**:
- Read existing JSON for our per-batch cadence ablation (Round-7 sprint Phase 2)
- Compare schedules: how often does AIHWKit resample noise vs our per-batch implementation?
- Hypothesis: AIHWKit may use independent noise per forward pass (every minibatch sees different noise); our per-batch may have used a single mask per training-step
- Resolve via code inspection: `aihwkit/simulator/parameters/.../weight_modifier.py` vs our `analog_layers_ensemble.py`
- Output: 1-page mechanism comparison; quantifies "what differs operationally"

### R11D-6 — Ensemble HAT trained with AIHWKit-matched noise schedule (DS + Kimi, ~12 GPU-h)

**Why**: If R11D-5 reveals AIHWKit resamples per-MINIBATCH (not per-batch as we did), retrain Ensemble HAT with that resample cadence and see if our framework matches.

**Spec**: Modify `analog_layers_ensemble.py` resample hook to per-minibatch. Train 1 seed canonical. Fresh-eval. Compare to AIHWKit 87.34%.

**Hypothesis**: Our framework + AIHWKit-matched cadence converges to AIHWKit accuracy → confirms cadence is the lever, not the architectural choice.

---

## 2. Theoretical exploration (Kimi, parallel ~2 days)

### R11D-T1 — Why does per-batch AIHWKit beat our per-batch by 1.18 pp?

KIMI-THEORY-1/2 explained per-epoch as implicit gradient-L2 + SAM-along-D2D-direction. **What does per-batch (AIHWKit-style) imply theoretically?**

Sketch: per-batch noise = SGD-with-noise injection per gradient step. This is closer to **stochastic regularization** (e.g. dropout-as-L2) than to **distribution-matching** (Ensemble HAT).

Hypothesis: in canonical noise regime, both converge to similar implicit regularizers. **Different in what regime?**
- High learning rate → per-batch noise becomes signal (averages out gradient signal)
- Long training → per-epoch sampling may underfit (only 100 mask realizations seen vs per-batch's 100*N_batches)
- Low data → per-epoch may overfit (one mask per epoch is correlated across mini-batches)

Output: 1-page theoretical addendum to KIMI-THEORY-2 — `S_cadence_comparison.tex`.

### R11D-T2 — Operating envelope per method

For each method (Standard HAT / per-batch / per-epoch / fixed-mask), characterize at what (σ_D2D, ADC_bits) each breaks. Build "operating envelope" comparison plot — superset of paper-1 iso-accuracy.

Output: text — Discussion §6.x or new Supp Note S-Method-Comparison.

---

## 3. Decision rules + outcomes

After R11D-1 through R11D-4 land:

| Outcome | Story |
|:--|:--|
| AIHWKit collapses at high σ / 4-bit / PCM, Ensemble HAT survives | **Path B revival** — method-superiority in stress regime; novelty strong |
| Both collapse together | Honest "noise-injection class limit"; submit Path A reframing with operating-envelope context |
| AIHWKit survives everywhere we tested | Pure Path A; Ensemble HAT contribution = diagnosis + theory + substrate (NOT method) |
| AIHWKit collapses at one specific regime (e.g., 4-bit) | Targeted method-superiority — focus paper claim there |

**Most likely outcome (my prediction)**: at least one regime (4-bit or PCM device model) will break AIHWKit while Ensemble HAT survives — because our framework was specifically tested at 4-bit and we report comparable accuracy. Probability: ~70%.

---

## 4. Resource budget

| Track | Owner | Time | GPU |
|:--|:--|--:|--:|
| R11D-1 (AIHWKit 4-bit) | DS | 1 day | ~12h |
| R11D-2 (AIHWKit σ=0.20) | DS | 1 day | ~12h |
| R11D-3 (AIHWKit σ=0.30) conditional | DS | 1 day | ~12h |
| R11D-4 (AIHWKit PCM) | DS | 1.5 days | ~15h |
| R11D-5 (cadence comparison text) | Kimi | 4h | 0 |
| R11D-6 (per-mini-batch Ensemble) conditional | DS | 1 day | ~12h |
| R11D-T1 (theory addendum) | Kimi | 1 day | 0 |
| R11D-T2 (envelope plot) | Gemini | 1 day | 0 |

**Total**: ~7-10 days, 60-75 GPU-h on local GPU. Larger budget; submission timeline pushes back ~1 week.

**Trade-off acknowledgment**: this is a substantive scientific exploration that may strengthen OR honestly weaken the novelty story. Worth doing before submission — pre-submission honest reframing always beats post-revision mandatory experiments.

---

## 5. Sequencing

```
Day 1:
  DS: launch R11D-1 (4-bit) and R11D-2 (σ=0.20) in series (or parallel if VRAM allows)
  Kimi: starts R11D-T1 theory addendum
  Gemini: starts R11D-T2 envelope plot design

Day 2-3:
  DS: R11D-3 conditional + R11D-4 PCM
  Kimi: R11D-T1 finishes; starts R11D-5 cadence text
  Gemini: continues plotting

Day 4-5:
  DS: any retraining (R11D-6 if R11D-5 reveals cadence mismatch)
  Kimi: finishes cadence comparison text
  
Day 6-7:
  Claude: integrates all R11D outputs
  Decision: which Path (A / B / hybrid) does the data support?
  Kimi: rewrites Discussion §6 + cover letter according to Path

Day 8-10:
  Final read + Gemini hostile-v2 (now informed by R11D)
```

R11D + R11C run partially in parallel:
- Kimi splits ~50/50 between R11C paper fix-it and R11D theory
- DS focuses ~80% on R11D experiments + ~20% Round-8 W2 P2 monitoring

---

## 6. R10E + R11D integration

When R11D-1 through R11D-4 lands, build the **AIHWKit comparison table** with all stress regimes:

| Method | σ=0.10, 8-bit | σ=0.10, 4-bit | σ=0.20, 8-bit | σ=0.30, 8-bit | PCM device |
|:--|--:|--:|--:|--:|--:|
| Standard HAT (ours) | 10% | ? | ? | ? | ? |
| AIHWKit baseline | **87.34%** | R11D-1 | R11D-2 | R11D-3 | R11D-4 |
| Ensemble HAT (ours) | **86.16%** | (existing) | (existing iso-acc map shows ~80%) | (~70%) | NEW |

This builds the methodological narrative honestly.

---

## 7. Frozen decisions reaffirmed

- NARRATIVE_PIVOT (zone partition + 3-scenario evidence spine)
- Nature Electronics venue target
- PhD-graduation submission gate (R11D extends ~1 week)
- All numerical claims preserved

**New (R11D-specific)**:
- Discussion will include AIHWKit comparison (no longer optional)
- Novelty framing depends on R11D outcome
- Operating envelope plot becomes a paper figure

---

## 8. Dispatches

- `DISPATCH_DS_R11D_AIHWKIT_EXPLORATION_20260426.md` — DS GPU experiments (R11D-1/2/3/4/6)
- `DISPATCH_KIMI_R11D_THEORY_TEXT_20260426.md` — Kimi cadence + theory addendum (R11D-5/T1)
- `DISPATCH_GEMINI_R11D_ENVELOPE_PLOT_20260426.md` — Gemini operating envelope plot (R11D-T2)
- `BROADCAST_ROUND11D_LAUNCH_20260426.md` — master broadcast

---

## 9. One-line

Path C exploration: 5 AIHWKit stress regimes (4-bit / σ=0.20/0.30 / PCM / cadence-matched Ensemble) + theoretical comparison + operating envelope plot. ~7-10 days, 60-75 GPU-h. May restore method-superiority narrative OR honestly reframe Path A. Either outcome is publishable.
