# Defense Wild-Card Q&A Prep

*10 questions outside standard ML / device-physics. Each answer: exactly 3 sentences (direct answer + evidence + nuance).*

---

## 1. Philosophical

**What makes this a PhD and not a Master's?**

This work is a PhD because it solves a methodological gap—the materials-to-system disconnect in organic CIM—through both a new conceptual framework and a new algorithm, Ensemble HAT. The scientific question is whether literature-derived device metrics can predict vision accuracy accurately enough to rank fabrication priorities before a chip exists. A Master's could build the simulator; the PhD lies in proving the rankings generalize across architectures and exposing the fresh-instance overfitting that standard HAT conceals.

**What is the "scientific question" here?**

The core question is whether organic CIM can be evaluated at the vision-task level using only literature-derived device profiles, and which non-ideality dominates the accuracy budget. We show this is possible for first-order behavioral prediction: ADC resolution dominates below 6 bits, while D2D variability dominates above. This reframes priorities from "better conductance states" to "secure readout first, then mismatch"—a ranking invisible at the device level alone.

## 2. Career-Strategic

**What's next after the PhD—industry or academia?**

I want a postdoc or research-scientist role at the intersection of ML systems and emerging hardware, because open questions—multi-instance HAT, hardware-in-the-loop validation, ImageNet-scale analog deployment—require dedicated resources. I am drawn to places where simulation and fabrication coexist, since this thesis is deliberately incomplete without chip-level closure. The choice between academia and industry depends on which institution is building the organic-array testbed I need to validate these predictions.

**How does this work fit into your 10-year plan?**

Over the next decade I want to build hardware-software co-design where device physics shapes training objectives directly, moving from one-way simulation to closed-loop co-optimization. This thesis establishes the interface language—device profiles as differentiable constraints—between materials scientists and ML engineers. The arc ends with automated training curricula generated from foundry metrology, so every process node ships with a matched neural-network recipe.

## 3. Ethical

**Could this technology be used for surveillance or military applications?**

Any efficient edge-vision accelerator carries dual-use risk, and low-power organic optoelectronics could enable surveillance where batteries currently limit deployment. However, the technology remains years from foundry readiness, giving the community time to develop governance frameworks before mass fabrication. I commit to publishing all profiles and code openly so that capability and oversight advance together.

## 4. Pedagogical

**How would you teach this to undergraduates, and what's the one concept they must grasp?**

I would use one hands-on lab: students train a tiny perceptron, watch accuracy collapse under a fixed conductance mismatch map, then recover by retraining with resampled mismatch each epoch. The key concept is that hardware noise is spatially structured and fixed per chip, making it dangerously easy to overfit. Once they feel that collapse viscerally, ADC cliffs and inverse-gamma compensation become motivated engineering rather than abstract theory.

## 5. Meta-Scientific

**Why simulation and not experiment? Is this "real" science if there's no chip?**

Simulation is the only tool that can systematically decompose five coupled non-idealities while holding all others constant, a control impossible in a first fabrication run. The predictions are falsifiable: Ensemble HAT should transfer above 86% to fresh OPECT instances, and NL=2.0 should bottleneck the MLP path—both testable once arrays arrive. Real science here is not the absence of a chip but the presence of specific, risky predictions that tie credibility to future measurement.

**What would it take to convince a skeptic?**

A single hardware-in-the-loop experiment where the simulator's ranking—ADC > D2D > C2C under matched HAT—matches measured degradation when each non-ideality is modulated should convince a skeptic. I do not claim absolute accuracy numbers are chip-predictive; I claim the relative rankings are stable enough to guide experimental investment. Until then, the CrossSim consistency check and zero-shot OPECT transfer provide the strongest circumstantial evidence.

## 6. Personal

**What was the hardest moment in this PhD, and what would you do differently?**

The hardest moment was discovering my first Ensemble HAT implementation had a silent bug that made it equivalent to standard HAT, so the "improvement" I celebrated for weeks was illusory. I would start locked-number checks and unit tests from month one rather than treating them as post-draft cleanup. That mistake taught me that in simulation-driven research, reproducibility infrastructure is the only firewall against self-deception.

## 7. Collaboration

**How did you work with your advisor, and what was your biggest disagreement?**

We operated in structured autonomy: I owned code and daily experiments, while weekly meetings stress-tested the narrative and locked results into the manuscript. Our biggest disagreement was over the CrossSim comparison, which I saw as essential validation and he initially saw as a distraction; we compromised with a brief supplementary note. That tension forced me to articulate why cross-framework grounding matters for credibility.
