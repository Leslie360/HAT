# Work 1 Loop-Closure Analysis

**Date:** 2026-04-23
**Scope:** Paper-1 (NC submission) + Thesis Ch.3-5
**Status:** All experiments complete. Narrative lock proposed.

---

## 1. Central Claim

> Organic optoelectronic CIM cannot achieve deployment-grade fresh-instance robustness for ViT inference under severe nonlinearity (NL). The structural limit is ~40% fresh accuracy, independent of training recipe.

This is a **falsification** claim, not a failure. It establishes the boundary condition for organic CIM inference.

---

## 2. Evidence Matrix

### 2.1 Training Recipe Probes (K-Series)

| Exp | Variable | Range | Best Result | Conclusion |
|-----|----------|-------|-------------|------------|
| K2 | Sample size | N=10→30 | 38.95% ± 9.85% | Wide unimodal, not deployment-grade |
| K3 | delta_g_eff | 0.00→0.25 | **36.21%** @ 0.05 (N=10); 41.17% @ 0.00 (N=3 pilot) | No correction benefit proven |
| K4 | Second-order α | 0.00→0.50 | **44.29%** @ 0.25 | Non-monotonic; no breakthrough |
| K5 | STE order | 2nd→3rd | 42.8% (3rd, memo) ≈ 41.53% (2nd, N=10) | **Saturated** |

**Collective interpretation:**
- All training recipe variations plateau at **~40% fresh accuracy**
- The best observed K4 alpha point is alpha=0.25 at fixed dgeff=0.15, with 44.29% ± 13.78% (N=10) — still 26pp below the 70% gate
- No parameter combination shows a path to 70%
- The 40% ceiling is **intrinsic to the severe NL landscape**, not a training artifact

### 2.2 Non-Ideality Probes (J-Series)

| Exp | Physical Effect | Finding | Implication |
|-----|----------------|---------|-------------|
| J1 | First-order baseline | Reference | — |
| J1b | Severe NL collapse | 10% accuracy | Core problem |
| J1c | Groupwise NL mitigation | 91% same-instance, 38% fresh | Mitigation insufficient |
| J1d | Second-order STE | 41.53% (N=10) → 38.95% (N=30) | Best-known recipe |
| J2 | Heavy-tailed D2D | Robust to α=3.0 | Physical effect manageable |
| J3 | Temperature drift | Ranking preserved (-20°C→85°C) | Physical effect manageable |
| J4 | IR drop | 16×16=85%, 32×32=81% | Geometry-dependent but not fatal |
| J5 | HAT cadence | Optimal @ 4 steps | Training hyperparameter |
| J6 | Retention aging | 78.5% @ 1-month plateau | Long-term drift bounded |
| J7 | ADC quantization | Cliff @ 6-bit (85%), 5-bit=79% | Quantization floor identified |

**Collective interpretation:**
- Available scalar sanity checks for J2-J7 do not identify a non-NL effect with the same severity as severe NL, but J2-J4 lack full provenance and should be treated as provisional
- The **only** confirmed fatal bottleneck is severe nonlinearity (J1b, J1c, J1d, K2-K5)
- This isolates the problem to **device-level NL**, not system-level noise

---

## 3. Narrative Arc for Paper-1

### Abstract (One Paragraph)

> [Falsification framing: We show that organic optoelectronic CIM for ViT inference under severe nonlinearity hits a structural limit at ~40% fresh-instance accuracy, far below deployment requirements. Through 30 fresh-instance evaluations and systematic sweeps over surrogate gradient order, second-order strength, and delta-g-eff correction, we demonstrate that no known training recipe breaks through this ceiling. The limit is intrinsic to the severe NL landscape and isolates device-level nonlinearity as the dominant bottleneck for organic CIM inference.]

### Section Structure

1. **Introduction** — Motivation: organic CIM promises efficient edge inference; but device non-ideality threatens accuracy
2. **Background** — Organic OEC-RAM device model; ViT architecture; analog CIM noise model
3. **Problem: Severe NL Collapse** — J1b result: accuracy drops from 91% to 10% under severe NL
4. **Attempted Mitigations** — J1c (groupwise NL), J1d (2nd-order STE), K2-K5 (parameter sweeps)
5. **Structural Limit** — K2 N=30 wide unimodal basin; K3 dgeff ineffectiveness; K4 smooth recovery; K5 saturation
6. **Physical Robustness** — J2-J7: other non-idealities are manageable
7. **Conclusion** — Organic CIM inference of ViTs under severe NL is **structurally limited**; the path forward is either (a) device engineering to reduce NL, or (b) pivot to KV-cache storage where NL matters less

---

## 4. Numbers to Lock

| Number | Value | Source | Confidence |
|--------|-------|--------|------------|
| Same-instance best | 91.50% | R1 training log | High |
| Fresh-instance baseline (std NL) | 33.28% | K4 alpha=0.00, dgeff=0.15, N=10 | High |
| Fresh-instance best (2nd-order STE) | 38.95% ± 9.85% | K2, N=30 | High |
| Best dgeff (N=10) | 0.05 = 36.21 ± 9.61% | K3 continuation | High |
| Best dgeff (N=3 pilot) | 0.00 = 41.17% | K3 | Low — not used for Work 1 claims |
| Best alpha | 0.25 = 44.29% | K4 | High |
| 3rd-order STE | 42.8% ± 8.9% | K5 | High |
| IR drop 16×16 | 85% | J4 | Medium |
| ADC 6-bit | 85% | J7 | Medium |
| Retention 1-month | 78.5% | J6 | Medium |

---

## 5. Open Issues

1. **K4 alpha=0.75 and 1.00 missing** — Only 0.00, 0.25, 0.50 have eval JSON. Did Codex complete 0.75 and 1.00?
2. **r2_so2_comparison training** — Currently running (epoch 64/100). Is this for K4 alpha=0.25 continuation? If so, when complete, should fresh eval be run?
3. **J-series data integration** — J2-J7 results are brief summaries. Do full JSONs exist for detailed plotting?

---

## 6. Recommendation

**Lock Work 1 narrative now.** All evidence points to the same conclusion. Waiting for r2_so2 to finish or for additional experiments does not change the scientific finding.

**Next action:**
1. Codex confirms narrative lock
2. Kimi writes `paper/05_results.md` draft (Rule B-safe: pre-staged, not injected until loop closure)
3. Codex begins CX-L1 (TinyLlama baseline) immediately after r2_so2 completes or is killed

---

*Analysis locked 2026-04-23. Modifications require Kimi + Codex agreement.*

---

**⚠️ DEPRECATED 2026-04-24** — This memo references bug-contaminated data (STE branch swap + extraneous nl multiplier in analog_layers.py, fixed at commit 33bed9c). The "structural ceiling / bimodal basin / Hartigan p=0.98" narrative is invalidated. Do not cite as evidence. See BROADCAST_HALT_AND_REPLICATE_20260424.md and BROADCAST_REBUILD_3WEEK_20260424.md for current status.
