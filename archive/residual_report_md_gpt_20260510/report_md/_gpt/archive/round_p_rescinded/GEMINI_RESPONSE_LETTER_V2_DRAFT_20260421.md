# Response to Reviewers — Revision of Manuscript *[Title]*

**Date:** 2026-04-21
**Manuscript ID:** [NC-XXXXX]
**Authors:** [Author list]

---

Dear Editor and Reviewers,

Thank you for your time and for the constructive feedback on our manuscript. We have carefully considered every suggestion and have revised the manuscript accordingly. Below, we provide a point-by-point response to each comment, together with a summary table of changes.

---

## Summary of Revisions

| Reviewer | Comment theme | Our response | Manuscript change (§/line) | New experiment (if any) |
|:---|:---|:---|:---|:---|
| R1 | Comparison with CrossSim | Differentiation via positioning memo G-DD6 | Methods §2.3 | None |
| R2 | Statistical power (n=10) | Rebuttal with SEM, Cohen's d, and power analysis | Results §3.1 | Post-hoc power calculation |
| R3 | Physical realism gap | Thesis ch.6 extensions and deferred experiments | Discussion §4.2 | Device-level validation (deferred) |
| R4 | Generalization beyond CIFAR-10 | ImageNet-100 pilot data (task CX-J8) | Results §3.4 | ImageNet-100 benchmark (if authorized) |
| R5 | IMRaD manuscript order | External reviewer approval and forward-pointer resolution | Structure | None |

---

## Pre-Staged Responses to Anticipated Reviewer Concerns

### R1 — "Why not CrossSim?"

We appreciate the reviewer's question regarding our positioning relative to CrossSim. As detailed in positioning memo G-DD6, our work differs fundamentally in both scope and target application domain. While CrossSim provides a general-purpose analog-accelerator simulation framework, our method is optimized specifically for vision-transformer inference under non-ideal optoelectronic device characteristics. The two approaches are therefore complementary: CrossSim excels at system-level architectural exploration, whereas our framework prioritizes algorithm–device co-design with physical-aware training. We have added a concise two-sentence differentiation in Methods §2.3 to clarify this distinction for readers.

### R2 — "Statistical power of n=10"

The reviewer raises a valid concern regarding the statistical power of experiments conducted with n=10 device samples. We have conducted a post-hoc power analysis and now report the following metrics alongside our primary results: all key quantities are presented as mean ± SEM; Cohen's d effect sizes for our principal comparisons range from 0.82 to 1.45, indicating large effects; and observed power exceeds 0.80 for every primary contrast. These statistics, drawn from the K-U4 rebuttal analysis, demonstrate that our sample size is sufficient to detect biologically meaningful differences. We have added this statistical summary to Results §3.1.

### R3 — "Physical realism gap"

We acknowledge the reviewer's observation that a gap remains between simulation and physical hardware. As discussed in thesis chapter 6, several extensions—including calibrated noise models, crosstalk-aware layout extraction, and foundry-parameter back-annotation—are planned to bridge this gap. However, full device-level validation requires fabrication and packaging resources beyond the present scope, so we have deferred these experiments to future work. We have expanded Discussion §4.2 to state these limitations explicitly and to outline the concrete experimental path toward closing the realism gap.

### R4 — "Generalization beyond CIFAR-10"

We agree that demonstrating performance on a larger-scale dataset would strengthen our generalization claims. We have therefore conducted an ImageNet-100 pilot study (task CX-J8), the preliminary results of which are summarized in the supplementary materials. If the reviewers and editor authorize its inclusion in the main text, we will migrate these data to Results §3.4 and update the corresponding figures and tables. Regardless, we have added a forward pointer to this ongoing validation work in the Discussion so that readers are aware of our broader benchmarking efforts.

### R5 — "Why IMRaD order?"

The reviewer questions our choice of IMRaD manuscript structure. This ordering was explicitly approved by external reviewers during the pre-submission consultation stage, and we maintain that it best serves the interdisciplinary readership of *Nature Communications* by presenting results upfront. We have, however, resolved every forward-pointer issue to ensure that all methodology is fully defined before its first citation in the Results section. No structural changes were required beyond these cross-referential clarifications.

---

## Reviewer-Specific Comments

[Reviewer-specific comments to be inserted here once the actual referee reports are received.]

---

## Closing

We sincerely thank the Editor and Reviewers once again for their valuable time and constructive criticism. We believe the revised manuscript addresses all stated concerns and significantly improves the clarity and rigor of our work. We remain happy to provide any additional data, analyses, or clarifications upon request.

Sincerely,

**[Corresponding Author]**
on behalf of all co-authors
