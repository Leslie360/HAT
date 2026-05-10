# 5-Minute Lightning Talk: Ensemble HAT for Analog CIM

**Total time:** 5 minutes
**Audience:** Hardware-architecture community
**Tone:** Ultra-concise, no digressions

---

## Slide 1: The Problem

**Visual:** Split-screen—ideal MAC array on the left, noise-corrupted output on the right, with a single red "10.00%" badge.

**Speaker notes:**
Analog compute-in-memory promises massive energy efficiency by executing matrix-vector multiplications directly inside the memory array. But device noise—resistance drift, cycle-to-cycle variation, and device-to-device mismatch—destroys accuracy. A standard Vision Transformer deployed on noisy analog hardware collapses completely. The fixed-mask baseline, which bakes a single noise sample into training, recovers only 10.00% top-1 accuracy. That is not minor degradation; it is catastrophic failure. Without a fix, the chip is unusable for any real inference workload.

**Timing:** `[~60 sec]`

---

## Slide 2: The Method

**Visual:** Diagram of the training loop: a new noise mask is injected at every epoch into the same backbone, producing a single converged model.

**Speaker notes:**
We resample device noise every single training epoch. Instead of memorizing one lucky mask, the network sees an ensemble of hardware instances and learns weights robust to the full noise distribution. We call this Ensemble HAT. It adds zero inference cost: at test time we deploy one deterministic mask, exactly like standard HAT. The only difference is that training now simulates fresh hardware every epoch rather than overfitting to one broken instance. It is simple, cheap to implement, and surprisingly effective.

**Timing:** `[~60 sec]`

---

## Slide 3: The Result

**Visual:** Bar chart—fixed-mask collapse at 10.00% versus Ensemble HAT at 86.37 ± 1.54%, with error bars and fresh-instance label.

**Speaker notes:**
On fresh hardware instances—noise profiles never seen during training—Ensemble HAT achieves 86.37 ± 1.54% top-1 accuracy. The fixed-mask baseline remains stuck at 10.00%. That is not a marginal gain; it is the difference between a dead chip and a functional accelerator. The result replicates across multiple independent trials, and the tight confidence interval confirms the improvement is systematic, not a lucky draw. We turned an unusable system into a competitive one.

**Timing:** `[~60 sec]`

---

## Slide 4: The Limitation

**Visual:** Schematic of an array with three grayed-out ghost layers labeled "IR-drop," "Thermal gradient," and "Sneak paths."

**Speaker notes:**
Our model is first-order. We capture device-level noise, but we currently ignore IR-drop along word-lines, temperature gradients across the array, and sneak-path currents in dense crossbars. Each of these effects can re-correlate errors spatially and break the independence assumption that makes ensemble averaging powerful. Consequently, 86.37% is an upper bound under idealized non-idealities. Real silicon will be harder. We are honest about that gap, and it is exactly why the next step matters.

**Timing:** `[~60 sec]`

---

## Slide 5: The Next Step

**Visual:** Pipeline diagram of the upcoming joint MLP-linear + Ensemble HAT full run, with a bold target callout: "≥80%."

**Speaker notes:**
The immediate next step is a joint training run combining MLP-linear layers with Ensemble HAT on the full network. Pilot experiments suggest this architecture recovers most of the remaining accuracy gap. Our target is ≥80% top-1 accuracy on fresh hardware instances. If we hit it, we will have a complete, inference-cheap recipe for deploying transformers on analog CIM. That is the real goal: not just a neat training trick, but a deployable solution.

**Timing:** `[~60 sec]`

---

## Summary

| Slide | Focus | Key message |
|-------|-------|-------------|
| 1 | Problem | Device noise kills analog CIM; fixed-mask collapses to **10.00%**. |
| 2 | Method | Resample noise every epoch = **Ensemble HAT**, zero inference cost. |
| 3 | Result | **86.37 ± 1.54%** on fresh instances—usable accelerator. |
| 4 | Limitation | First-order model; IR-drop, thermal, sneak paths still excluded. |
| 5 | Next step | Joint MLP-linear + Ensemble HAT full run, target **≥80%**. |
