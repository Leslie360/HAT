# Committee-Specific Q&A Skeleton

**Date:** 2026-04-25  
**Status:** Skeleton — populate when committee names are known

---

## Instructions

When committee member names and research areas are provided, draft 2-4 anticipated questions per member based on their published work. Below is a generic skeleton organized by common committee specializations.

---

## Category A: Analog / Mixed-Signal Circuit Experts

**Typical background:** CMOS analog design, ADC/DAC, memory circuits, neuromorphic hardware

### A.1: "Your ADC model is a hook diagnostic. What would change with a real SAR ADC or sigma-delta front end?"
**Skeleton answer:** Physical ADCs add comparator offset, reference noise, and sampling jitter. Our hook diagnostic captures quantization and range-clipping but not these non-idealities. A SAR ADC would likely worsen the 6-bit cliff due to comparator mismatch; sigma-delta would trade resolution for latency. The framework is extensible: the ADC surrogate can be replaced with a behavioral SAR or sigma-delta model in the JSON profile.

### A.2: "Why differential-pair encoding and not single-ended with virtual ground?"
**Skeleton answer:** Differential pairs suppress common-mode noise (C2C variations, temperature drift) and double the dynamic range for a given conductance window. Single-ended would require tighter Common-Mode Rejection Ratio specifications. The trade-off is 2× array area; we accept this for robustness.

### A.3: "Have you modeled the access transistor non-ideality?"
**Skeleton answer:** Not explicitly. Access transistor variation is implicitly absorbed into the effective D2D mismatch parameter. For organic devices with lower mobility, access transistor IR drop may be non-negligible and would require explicit modeling in a future circuit-aware layer.

---

## Category B: Machine Learning / Optimization Experts

**Typical background:** Deep learning theory, optimization, generalization, robustness

### B.1: "Your Ensemble HAT resembles dropout or Shake-Shake. What is formally different?"
**Skeleton answer:** Three differences: (1) Dropout masks are i.i.d. per activation; D2D masks are spatially structured and fixed per instance. (2) Dropout rate is a tunable hyperparameter; Ensemble HAT's regularization strength is set by physical σ_D2D. (3) Shake-Shake interpolates between two network branches; Ensemble HAT resamples one perturbation field. The structural analogue to dropout-as-L2 (Wager et al. 2013) is illuminating but not an equivalence.

### B.2: "Could you prove that epoch-level is optimal among all resampling cadences?"
**Skeleton answer:** No formal proof. We have empirical evidence (88.41% epoch vs. 86.16% per-batch vs. 87.18% fixed) and theoretical intuition (optimizer needs stable curvature within an epoch). A formal optimization of resampling cadence would require modeling the optimizer's forgetting rate, which is architecture- and task-dependent.

### B.3: "The PAC-Bayes bound is likely vacuous. Why include it?"
**Skeleton answer:** The bound's value is structural, not numerical. It connects Ensemble HAT's implicit regularizer to established generalization theory, providing a principled narrative for why fresh-instance accuracy tracks the training average. We explicitly note the bound is likely vacuous in absolute terms (Supplementary Note S-Theory §S.8). Its inclusion signals theoretical depth without overstating predictive power.

---

## Category C: Device Physics / Materials Experts

**Typical background:** Organic electronics, memristors, phototransistors, device characterization

### C.1: "Your NL=2.0 is a behavioral proxy. What do measured organic devices actually exhibit?"
**Skeleton answer:** We do not have measured NL fits for the specific organic devices in this study. The NL=2.0 value is a stress-test boundary anchored to DNTT transistor literature (Vincze et al. 2025). Direct pulse-level write characterization of organic crossbars is a high-priority next step. If measured NL differs, the surrogate can be recalibrated.

### C.2: "Retention in organic devices is often much worse than 140 ms. How sensitive are your results?"
**Skeleton answer:** The 140/610 ms retention times are canonical values from Vincze 2025. We tested retention sensitivity: at 1000 seconds, the uniform model stays within 0.1 pp of the state-dependent model (Supplementary Table 6). If physical retention is worse, the framework can substitute new τ1/τ2 values via the JSON profile.

### C.3: "Have you considered iontronic or electrochemical devices instead of organic phototransistors?"
**Skeleton answer:** The framework is substrate-agnostic. Iontronic or electrochemical device parameters would enter through the same JSON profile interface. The organic focus reflects our collaboration's device availability, not a fundamental limitation.

---

## Category D: Systems / Architecture Experts

**Typical background:** Computer architecture, accelerator design, edge computing

### D.1: "What is the area overhead of your hybrid mapping?"
**Skeleton answer:** Not modeled. The analog crossbar area depends on device pitch, access transistor size, and routing overhead. The 812-array count under 128×128 tiling is a structural lower bound, not an area estimate. Full area modeling would require a layout-aware tool like NeuroSim.

### D.2: "How does your framework compare to a full-stack tool like NeuroSim + PyTorch?"
**Skeleton answer:** NeuroSim estimates architecture-level performance and energy; our framework evaluates task-level accuracy under device non-idealities. They are complementary. We explicitly frame our energy numbers as first-order estimates that would benefit from NeuroSim validation (Supplementary Note S-Tooling).

### D.3: "Would your results change with a different architecture like DeiT or Swin?"
**Skeleton answer:** Plausible but untested. The failure-mode ranking (ADC cliff, instance overfitting) reflects analog-CIM fundamentals, but the exact thresholds may shift. Cross-architecture validation (ViT-Small, DeiT-Small on TinyImageNet) is queued on an 8×40GB remote.

---

## Category E: Thesis Advisor Questions

**Typically deepest on methodology, student ownership, and project evolution**

### E.1: "Walk me through how you discovered the bug and what you learned from the process."
**Skeleton answer:** (Personal narrative — student should customize.) The bug was discovered during a routine audit of the second-order STE backward pass. The positive signs in LTP/LTD second-order terms acted as curvature accelerators rather than brakes, causing the optimizer to exploit fragile minima. The key lesson was the importance of symbolic verification before empirical interpretation: the bimodal K2 distribution that looked like a physical phenomenon was actually a mathematical artifact.

### E.2: "What is your personal contribution versus the advisors' / collaborators'?"
**Skeleton answer:** (Student should customize.) Personal contributions: framework design, Ensemble HAT formulation, empirical evaluation protocol, theory derivation, and paper writing. Advisor contributions: research direction, organic device expertise, and simulation discipline. PhD collaborator: measured device parameters (pending). Code assistance: automated agents for audit and cleanup.

---

## Usage

When committee names are known:
1. Identify each member's top 2-3 research areas from their recent publications.
2. Map to categories A-E above.
3. Customize the skeleton answers with specific citations to their work.
4. Add 1-2 questions unique to their specific research trajectory.
