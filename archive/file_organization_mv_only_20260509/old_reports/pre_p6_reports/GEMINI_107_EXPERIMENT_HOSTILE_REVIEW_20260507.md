# GEMINI-107-A: Pre-Run Hostile Review

**Date:** 2026-05-07
**Status:** COMPLETE
**Reviewer:** Gemini (Hostile Experimental Reviewer)

---

## 1. Matrix Sufficiency (Seed Robustness)

**Verdict:** ⚠️ **Provisional.**

**Analysis:**
The plan (K-107-A) expands to 3 training seeds and 5 evaluation D2D seeds. This is a massive improvement over "seed 42 only". However, the 107 route claims to be "the only line with clearly improving new signal". If we are to bank the paper on this, 3 training seeds might still be low if the training is unstable.

**Weakness:**
We haven't defined what "robust" means numerically. If Seed 42 gives PPL 18.4 but Seed 123 gives PPL 21.0, is it still "canonical"?

**Recommendation:**
- Explicitly report the **Standard Deviation across training seeds**, not just across eval instances.
- If $\sigma_{train} > 0.5$ PPL, the result should be downgraded to "Provisional" because the training recipe is not yet stable.

---

## 2. Retention Stress Design

**Verdict:** ✅ **Sound.**

**Analysis:**
The double-exponential decay applied in the conductance domain (G_pos/G_neg) is physically accurate for PCM/ReRAM. The age computation `(L-1-i) * step_time` correctly captures the autoregressive nature of KV-cache (older tokens decay more).

**Stress levels:**
- 0.1s/step: 51.2s total window. (Real-time chat proxy)
- 1.0s/step: 8.5m total window. (Thoughtful composition proxy)
- 10.0s/step: 1.4h total window. (Extreme stress test)

This range is sufficient to prove the "retention-aware" benefit of HAT.

---

## 3. Comparison Fairness

**Verdict:** ⚠️ **Critical Risk on "All-Layer" Baseline.**

**Analysis:**
1. **Hyperparameters:** Is the learning rate ($1 \times 10^{-5}$) and step count (e.g., 1000 steps) sufficient for the "all-layer" analog trainer? Training 24 layers of analog noise is fundamentally harder than training 1 layer. If we use the same budget, we might be unfairly handicapping the all-layer baseline to make `last1` look better.
2. **Quantization:** Ensure `n_states` is identical across all comparisons. K-107-C sweeps this, which is good.
3. **Stride:** The evaluation uses `stride=None` (non-overlapping). This is fair for *internal* comparisons but will produce PPL values ~1.5-2.0 higher than standard benchmarks (e.g., WikiText-2 PPL on Pythia-410m is usually ~13.5 with stride, while we see ~15.7). This must be clearly footnoted.

---

## 4. Kill Criteria Strictness

**Verdict:** ❌ **Too Loose.**

Current K-107-A Criterion: `PPL > 22 @ D2D=0.02 → Kill`.

**Hostile Critique:**
If the baseline digital PPL is 15.68 and the current best `last1` is 18.42, a jump to 22.0 is a failure. 22.0 is closer to the *untrained* all-layer performance.

**Proposed Stricter Criteria:**
1. **K-107-A (Stability):** If any training seed (123, 456) yields mean PPL > **19.5** at D2D=0.02, pause. We should not settle for a "lucky seed" result.
2. **K-107-B (Retention):** If the retention-aware HAT does not outperform a non-retention-aware baseline (trained with step=0) by at least **2.0 PPL** at `step_time=10.0`, the retention-aware claim is weak.
3. **Metadata (Hard Kill):** If any JSON in the re-run is missing the `git_commit` or `eval_d2d_seed`, the run is automatically **KILL** status. No exceptions for "urgent" data.

---

## 5. The "Abandon Ship" Result

**Which single result makes us abandon 107?**

If **K-107-C (State Sweep)** shows that PPL is insensitive to `n_states` (e.g., 4-bit vs 8-bit gives the same result), it implies the noise is so dominant that our "analog" resolution doesn't matter, OR there is a bug in the quantization STE.

**The "Red Line":**
If `last1` trained @ D2D=0.02 does not beat `last1` **Zero-Shot** (digital weights + noise) by at least **3.0 PPL**, the HAT training benefit is marginal and not worth a paper headline.

---

## Final Recommendation to User

Proceed with K-107-A/B but **adopt the 19.5 PPL Kill Criterion**.
Ask DS to verify the learning rate sensitivity for the `all-layer` control case to ensure we aren't "beating a straw man".
