# Story Rewrite Brief (2026-04-08)

## Current Judgment

The paper is no longer "experimentally empty", but the **storytelling is still weaker than the evidence**. Right now the manuscript reads like:

1. build simulator
2. run many experiments
3. discuss many caveats

What a stronger journal narrative needs is:

1. there is a concrete unmet problem
2. existing device papers and existing CIM simulators each leave a gap
3. we build exactly the missing bridge
4. we use it to answer a small number of high-value system questions
5. those answers change what a materials/device team should optimize next

## What Problem We Actually Solved

The clearest formulation is:

> Existing organic optoelectronic synapse papers can measure device behaviors, but they usually cannot tell whether those behaviors are already good enough for modern edge-vision deployment. Existing CIM simulators are mostly tuned for inorganic memories and do not cleanly expose the organic-device questions that matter here. We therefore build a profile-driven, first-order behavioral bridge from partial organic-device characterization to system-level deployment risk.

That is stronger than simply saying "we built a simulator."

## The Most Important Questions the Paper Answers

The results section should feel like it answers 4 concrete questions:

1. Is nominal quantization the main bottleneck?
- Answer: no; under canonical uniform-noise assumptions, quantization alone is often not the dominant failure mode once scale recovery and HAT are included.

2. What actually breaks first as tasks get harder?
- Answer: task complexity amplifies deployment fragility; CIFAR-100 exposes a much larger gap than CIFAR-10, and Flowers-102 exposes a failure boundary for the current recipe.

3. Is same-instance robustness enough?
- Answer: no; fresh-instance transfer is a separate deployment problem, and standard HAT can overfit to one D2D realization.

4. Can richer physical stress be retrained around?
- Answer: sometimes. Proportional-noise HAT can recover within a matched regime; strong nonlinear write remains a hard failure mode for the current transformer deployment.

## The Cleanest "Then We Improved It" Arc

The strongest improvement arc in the current manuscript is:

1. canonical HAT improves same-instance noisy deployment
2. but fresh-instance transfer collapses
3. Ensemble HAT fixes a large part of that problem
4. literature-derived profile transfer shows the bridge can actually be used on an external device paper

This arc is much stronger than trying to treat every result family as equally central.

## What Still Feels Weak

### 1. The background is still too compressed

The introduction should spend more time making the pain explicit:
- device papers often report multilevel states / retention / power, but not deployment viability
- system teams need deployment-facing answers earlier than full chip availability
- existing inorganic-focused CIM frameworks are not wrong, but they are not organized around organic optoelectronic profile substitution, optical frontends, and hybrid transformer deployment

### 2. The manuscript sometimes reads like a catalog

The current sectioning is thorough, but the emotional hierarchy is weak. Not every experiment deserves equal narrative weight.

Priority order should be:
- cross-dataset canonical results
- fresh-instance transfer + Ensemble HAT
- physical-stress limits
- literature-derived case study
- energy / analog ceiling

### 3. The engineering pain points are not yet vivid enough

The paper should explicitly foreground these engineering pain points:
- same-instance success can be misleading
- analog robustness is regime-dependent rather than universal
- dynamic attention remains a digital energy ceiling
- partial device characterization is common, but direct system judgment is still needed

### 4. The "solved how much" statement should be more quantified

The paper already has the numbers, but the prose should foreground them more deliberately:
- fresh-instance accuracy improved from 10.00% to 86.37 ± 1.54% with Ensemble HAT
- literature-derived profile transfer reached 88.53% vs 10.00% for standard HAT
- proportional-noise retraining recovered Tiny-ViT to 97.37 ± 0.05% in the matched regime
- nonlinear-write retraining remained stuck near 27.72 ± 0.82%, defining a clear current boundary

## Recommended Story Spine

Use this as the paper's high-level spine:

### Background
- Organic optoelectronic CIM is attractive for edge vision because of multilevel conductance, optical sensitivity, and low static power.
- But device metrics do not directly answer deployment viability on modern CNN/Transformer backbones.
- Existing simulators mostly target inorganic memories or do not expose the right organic-specific abstractions.

### Gap
- The field lacks a practical bridge from partial device characterization to system-level deployment decisions.

### Method
- We build a profile-driven first-order behavioral simulation framework with hybrid analog/digital mapping, device-profile substitution, and hardware-aware training support.

### Main Findings
- Quantization is not the dominant bottleneck in the canonical regime.
- Complexity, converter precision, fresh-instance transfer, and richer physics are more decisive.
- Standard HAT helps, but same-instance robustness is not enough.
- Ensemble HAT substantially mitigates hardware-instance overfitting.
- Matched physical retraining can recover proportional-noise robustness, but nonlinear write remains a hard boundary.

### Practical Value
- The framework can ingest a literature-derived profile and produce a deployment-facing answer without changing the evaluation code path.

### Limits
- This is a first-order behavioral bridge, not a chip-predictive emulator.

## Suggested Writing Tone Shift

Move slightly away from:
- "we simulated many non-idealities"

Move toward:
- "we used a profile-driven simulator to determine which measured device characteristics actually matter for deployment"

## What To Emphasize In Revision

1. The paper solved the **decision problem**, not just the simulation problem.
2. Ensemble HAT is the strongest "we actually fixed something important" result.
3. The literature-derived case study is the strongest evidence that the bridge is usable.
4. Nonlinear-write failure is not embarrassing; it is a valuable boundary result.

## Concrete Writing Method

If Claude decides to do one more real story pass, the cleanest way is to rewrite only three sections with the same rhetorical template:

1. `Abstract`
2. `Introduction`
3. `Conclusion`

Use this paragraph logic:

### Opening Problem
- device papers can report conductance states, retention, variability, and photoresponse
- but they usually still cannot answer the deployment question:
  - "is this already good enough for modern edge-vision models?"

### Gap Against Existing Tools
- inorganic-focused CIM simulators are useful, but they do not directly organize the problem around:
  - organic optoelectronic profile substitution
  - optical frontend effects
  - hybrid CNN / transformer deployment decisions

### Our Method
- we introduce a profile-driven first-order behavioral bridge
- it keeps the evaluation code path fixed while letting device assumptions change

### Questions Answered
- not every result family deserves equal weight
- the paper should explicitly say it answers four system questions:
  1. is nominal quantization the main bottleneck?
  2. what fails first as tasks get harder?
  3. is same-instance robustness enough?
  4. which richer physical stresses can training recover from?

### Quantified Resolution
- foreground the highest-value numbers, not all numbers:
  - fresh-instance transfer:
    - `10.00% -> 86.37 ± 1.54%`
  - literature-profile transfer:
    - `88.53%`
  - matched proportional-noise retraining:
    - `97.37 ± 0.05%`
  - nonlinear-write boundary:
    - `27.72 ± 0.82%`
  - corrected retention:
    - `~79% plateau`

### Bounded Final Claim
- the paper's final claim should stay:
  - a transparent behavioral bridge for deployment-facing decision support
- not:
  - a chip-predictive emulator

## What Not To Do

- do **not** let the paper read like a chronological lab notebook
- do **not** present every experiment as equally central
- do **not** over-promote reproducibility add-ons such as the `V1` multi-seed result into the main scientific headline
- do **not** hide the nonlinear-write failure; it is one of the most valuable boundaries in the current draft
