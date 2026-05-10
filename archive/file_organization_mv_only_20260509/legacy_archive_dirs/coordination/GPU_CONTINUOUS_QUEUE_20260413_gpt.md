# GPU Continuous Queue Plan (2026-04-13)

> **Core rule:** GPU should not sit idle if there is high-ROI scientific work available.
>
> **The queue now serves three goals at once:**
> 1. strengthen the current paper when reviewer payoff is high,
> 2. improve simulator realism / measured-data readiness / open-source value,
> 3. generate seeds for a second paper.

---

## A. Queue Philosophy

We no longer treat GPU time as a submission-only resource.

Every accepted GPU run should ideally contribute to at least one of:
- current-paper defense,
- framework realism,
- second-paper discovery,

and preferably two or more.

---

## B. Current Priority Bands

### Tier A — Immediate high-ROI runs

1. **Ensemble HAT control package**
   - provenance-checked `GM-E1`
   - purpose: separate fixed-mask resampling from generic i.i.d. noise
   - expected destination: supplementary or main-text one-line pointer

2. **Pure-digital ADC control**
   - finalized `GM-E2`
   - purpose: separate digital quantization cliff from hybrid analog-digital degradation
   - expected destination: supplementary with optional main-text pointer

3. **Retention sensitivity sweep**
   - purpose: quantify which retention parameters materially move deployment conclusions
   - likely destination: supplementary / future measured-data calibration logic

4. **Lightweight NL scan**
   - purpose: turn the single `NL=2.0` point into a graded failure landscape
   - likely destination: supplementary now, stronger asset for second paper later

### Tier B — Framework realism runs

5. **Measured-profile dry-run pipeline**
   - raw curve -> fitter -> JSON profile -> inference

6. **State-dependent retention regime library**
   - broader canonical profiles for future release

7. **Cross-noise composition tests**
   - uniform + proportional + retention + asymmetry interactions

### Tier C — Paper-2 exploration

8. **Alternative structural-randomization strategies vs Ensemble HAT**

9. **Cross-architecture mitigation transfer**

10. **Profile-family phase maps**

---

## C. Governance

### Kimi
- ranks runs by scientific/project value
- connects runs to measured-data readiness and paper-2 opportunities

### Gemini
- proposes queue order
- prepares insertion maps / artifact triage
- helps turn finished runs into manuscript or backlog assets

### Codex
- accepts or rejects runs
- verifies artifacts
- decides whether each output goes to:
  - main text,
  - supplementary,
  - framework backlog,
  - second-paper backlog

---

## D. Required Output Per GPU Run

Each accepted run should produce:
- a machine-readable artifact (`json`, `csv`, or checkpoint metadata),
- a short markdown summary,
- an insertion recommendation:
  - `main text`
  - `supplementary`
  - `future paper only`

---

## E. Non-Goals

Do **not** burn GPU on:
- redundant reruns of locked numbers,
- broad unfocused sweeps with no manuscript or platform value,
- experiments that only look useful because they are easy.
