# 15-Minute Conference Talk Script

**Title:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision (compute-ViT)
**Speaker:** Songqiao Li, [Affiliation]
**Venue:** [Conference Name]
**Date:** 2026-04-20
**Total time:** ~12 min delivery + 3 min buffer / Q&A
**Word count:** ~1,150 words (speaker notes)

---

## Slide 1: Title

**Visual description:** Title slide with project wordmark, speaker photo, and affiliation logo.

**Speaker notes:**
Good morning. I'm Songqiao Li from [Affiliation]. This is compute-ViT: Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision. We are building a decision bridge between reported organic device physics and real vision accuracy. The question is simple. Before anyone spends millions fabricating a full chip, which device parameters actually kill deployment? And which ones are harmless? This talk walks through how we answer that, and why the standard training recipe breaks in a very surprising way. [pause] Spoiler: the problem is not the device. It is how we train.

**Timing note:** [~60 sec]

---

## Slide 2: Motivation

**Visual description:** Bar chart comparing energy per MAC: digital CMOS vs. analog CIM.

**Speaker notes:**
Let's start with why analog compute-in-memory matters. Digital CMOS is hitting an energy wall. A single MAC in advanced node costs roughly one picojoule. Analog CIM promises to cut that by two orders of magnitude. [emphasis] That is one hundred times efficiency potential. It is the prize. But the prize comes with a catch. Real analog arrays are messy. Conductance drifts. Masks mismatch. And if you ignore that mess during training, your beautiful floating-point model dies on the first real device instance. We need a framework that trains through the noise, not around it.

**Timing note:** [~60 sec]

---

## Slide 3: The challenge

**Visual description:** Side-by-side schematic: clean ideal crossbar vs. messy real crossbar with drift arrows and noise clouds.

**Speaker notes:**
Here is the reality gap. On the left, an ideal crossbar. Perfect conductance, linear response, infinite retention. On the right, a real organic array. Device-to-device mismatch spreads the programmed weights. Photoresponse is nonlinear. And after programming, conductance drifts within seconds. We model all three effects inside compute-ViT. Nonlinearity as a gradient-scaling surrogate. Retention as exponential decay. And mismatch as Gaussian noise on every single cell. The question is not whether these effects exist. They do. The question is which ones dominate accuracy, and which ones we can train around.

**Timing note:** [~60 sec]

---

## Slide 4: Framework

**Visual description:** Three-layer stack diagram: device profile → PyTorch analog layers → task accuracy.

**Speaker notes:**
Enter compute-ViT. The framework has three layers. Bottom, a replaceable device profile that encodes literature-derived metrics like conductance range and mismatch sigma. Middle, PyTorch-native mixed analog-digital layers with noise injection, ADC quantization, and energy profiling. Top, task-level accuracy on standard vision benchmarks. Everything is validated against CrossSim for shared-regime sanity. [pause] The key idea is profile-driven simulation. Swap the JSON, and the same model tells you what a new material means for ResNet, ConvNeXt, or Tiny-ViT. No tape-out required. That is the bridge we are selling.

**Timing note:** [~60 sec]

---

## Slide 5: HAT taxonomy

**Visual description:** 2D design plane with axes: mask cadence (fixed / per-epoch / per-batch) vs. protected layers (all / MLP / QKV / none).

**Speaker notes:**
Hardware-aware training is not one thing. It is a design plane. On one axis, how often you resample the mismatch mask. Fixed-mask commits to one instance for the entire run. Per-epoch changes it every epoch. Per-batch changes it every batch. On the other axis, which layers you protect. All-linear, MLP-only, QKV-only, or full analog. We swept this plane systematically on CIFAR-10, CIFAR-100, and Flowers-102. And one corner produced a result so strange we had to stop and check our code for autocast bugs. I will show you that result now.

**Timing note:** [~60 sec]

---

## Slide 6: The 10% collapse

**Visual description:** Dual-bar chart: V4 canonical HAT at 87.95 ± 0.27% vs. fresh-instance transfer at 10.00%.

**Speaker notes:**
Standard HAT uses a fixed mask. You train with one deterministic mismatch pattern, and you validate on the exact same pattern. Looks great. Eighty-seven point nine five plus or minus zero point two seven percent — 87.95 ± 0.27% — on the canonical V4 regime. But here is the honest test. When we evaluate that exact checkpoint on ten fresh device instances, accuracy collapses. [pause] Ten point zero zero percent. Exactly 10.00%. That is not a typo. It is deterministic. We ran it ten times. The model has memorized one specific broken hardware signature. It is instance-overfitting. And that means standard HAT is cheating, not solving.

**Timing note:** [~60 sec]

---

## Slide 7: Ensemble HAT fix

**Visual description:** Recovery arrow from 10.00% up to 86.37 ± 1.54% with error bars across ten fresh instances.

**Speaker notes:**
The fix is Ensemble HAT. Instead of one fixed mask, we resample a fresh device instance every single epoch. The model never sees the same mismatch realization twice. Accuracy on fresh instances recovers to eighty-six point three seven plus or minus one point five four percent. That is 86.37 ± 1.54%. [emphasis] That is a seventy-six point gap recovered by a one-line training change. Why does it work? Diversity. The model learns an average over the noise ensemble rather than memorizing one realization. It is domain randomization applied to device mismatch. Simple, cheap, and surprisingly effective.

**Timing note:** [~60 sec]

---

## Slide 8: Fresh-instance protocol

**Visual description:** Schematic showing training array locked during evaluation, with ten fresh arrays plugged in for honest testing.

**Speaker notes:**
Let me stress why the fresh-instance protocol matters. Training-array evaluation is cheating. You optimize weights for the same noise you test on. That is not deployment. Deployment means weights frozen, new chip plugged in, no gradient updates. We enforce that honestly. Ten fresh arrays, zero retraining. Now, some ablations look good under training-array metrics but fail this test. For example, linearizing only the MLP layers hits thirty-two point one two plus or minus seven point seven two percent — 32.12 ± 7.72% — fresh. [pause] That is not deployment-grade. It is a diagnostic ceiling, not a product.

**Timing note:** [~60 sec]

---

## Slide 9: Correlated-D2D robustness

**Visual description:** Error-bar plot: i.i.d. baseline vs. ρ = 0.3 vs. ρ = 0.5, showing bounded degradation.

**Speaker notes:**
Real wafers are worse than independent noise. Mismatch is spatially correlated across the array. We tested separable AR-one structure with rho equals zero point five. Ensemble HAT still reaches eighty-two point one two plus or minus three point nine five percent. That is 82.12 ± 3.95%. [emphasis] Rank ordering is preserved. No single instance drops below seventy-four percent. The degradation is bounded and predictable. That is the difference between a fragile lab demo and a deployable system. Spatial correlation hurts, but it does not kill the recipe. This is why the ensemble approach is deployment-relevant.

**Timing note:** [~60 sec]

---

## Slide 10: Limitations

**Visual description:** Scope-boundary diagram with "In Model" and "Not in Model" columns.

**Speaker notes:**
I want to be honest about what is not in this model. We use first-order behavioral approximations. IR drop and sneak paths are scalar placeholders, not spatial solvers. Thermal drift is absent. Heavy-tailed conductance distributions are not modeled. Our framework ranks deployment risks; it does not predict a specific chip. [pause] Stating those boundaries up front builds trust. A simulation that claims too much is worse than no simulation at all. We are precise about our limits so that the community can improve them rather than doubt them. Honesty is a feature here.

**Timing note:** [~60 sec]

---

## Slide 11: Thesis next steps

**Visual description:** Three-panel roadmap: joint training icon, ImageNet logo, and theory equation.

**Speaker notes:**
Where do we go next? Three directions. First, joint training. Co-optimize the analog frontend and the digital backend instead of fixing one and tuning the other. Second, scale to ImageNet. CIFAR is a sandbox. The real test is a thousand-class task with genuine visual complexity. Third, theory. Can we bound the ensemble variance analytically instead of running ten Monte Carlo draws every time? [pause] These three bullets will keep me busy for the next two years. I hope some of you will join the effort. The framework is open source and the profiles are replaceable.

**Timing note:** [~60 sec]

---

## Slide 12: Q&A prompt

**Visual description:** Contact slide with email, project repository QR code, and open-position note.

**Speaker notes:**
Thank you. We are actively looking for collaborators on measured array validation, circuit-level co-design, and robust training theory. If you work on organic devices, analog circuits, or vision transformers at the edge, please come talk to us. [pause] I will take questions now.

**Timing note:** [~60 sec]

---

*End of script.*
