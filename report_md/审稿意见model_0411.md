## sonar

Having thoroughly read both the main manuscript and supplementary material, here is my brutally honest external reviewer assessment.

***

## Overall Recommendation

**Major Revision** — the paper is well-structured and technically honest, but several framing choices and missing controls create vulnerabilities that reviewers at Nature Communications will exploit. These are fixable without new hardware.

***

## Scores

| Dimension | Score | Rationale |
|---|---|---|
| Methodological Rigor | 3/5 | Framework is internally consistent, but the sole external validation is one matched-regime AIHWKIT sanity check; no cross-tool equivalence for retention, photoresponse, or NL dynamics |
| Scientific Contribution | 3.5/5 | Ensemble HAT is the strongest original finding; the "6-bit cliff" is insightful but undersold; profile substitution is useful infrastructure but architecturally thin |
| NC Fit | 3/5 | The interdisciplinary framing is credible, but NC increasingly expects at least one physical measurement anchor; simulation-only papers at NC typically come with a fabrication group co-authorship |

***

## Critical Weaknesses (Top 3)

**1. No ground-truth calibration point — the framework "floats" in physical space.**
Every device parameter (D2D σ=10%, C2C σ=5%, retention τ₁=140 ms, τ₂=610 ms, NL=1.0–2.0) is either adopted from two Early Access papers (Vincze 2025, Zhang 2025) or labeled "proxy estimate". There is no single conductance state measurement, no write-pulse trace, and no retention curve from the authors' own lab. A NC reviewer — especially one from a device group — will ask: *how do you know your proxy parameters are in the right regime?* The AIHWKIT sanity check (90.08±0.21% vs. 95.46% digital) demonstrates only that your quantization logic is non-trivial; it says nothing about whether your organic device model corresponds to any real device. This is the single biggest vulnerability. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**2. The NL=2.0 "hard boundary" conflates approximation failure with physical failure.**
Section 6.5 explicitly states: *"the failure boundary at NL=2.0 reflects the limit of this approximation rather than a fundamental materials constraint"*. Yet the abstract, conclusion, and cover letter all frame 27.72±0.82% as a hard limit. This is a factual inconsistency — you are measuring where your gradient-scaling surrogate breaks down, not where organic devices fail. Reviewers will flag this as overreach. The NL=2.0 result is still valuable (it tells designers what the simulator cannot handle), but it cannot be called a "hard failure mode" without a physical backup. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**3. The Ensemble HAT result has a significant confound that is underexplored.**
The 10% → 86.37±1.54% recovery is dramatic, but the paper acknowledges a "robustness-capacity trade-off": even under matched deployment conditions, Ensemble HAT does not reach the 98.06% digital baseline. The paper attributes this gap to "regularization from per-epoch D2D resampling" — which is plausible but untested. There is no ablation over resampling frequency (every epoch vs. every N steps), no comparison against simpler augmentation baselines (e.g., noise injection without structural D2D resampling), and no experiment showing that the same technique works on a second architecture without fine-tuning. Without these controls, a reviewer can argue this is standard noise-augmented training with a new name. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

***

## Strengths

1. **Transparent limitation disclosure is genuinely exemplary.** The limitation section in 6.5 lists IR drop, sneak paths, temperature, optical crosstalk, and differential asymmetry, and then provides actual quantitative sensitivity tables (S6, S7) bounding their impact. This is unusually rigorous for a simulation paper and will earn reviewer credit. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)
2. **Multi-architecture, multi-dataset evaluation is thorough.** ResNet-18/ConvNeXt/Tiny-ViT across CIFAR-10/100/Flowers-102 is broader than comparable organic-CIM papers, and the V1–V8 experiment labeling with explicit seed locking is reproducibility-positive. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)
3. **The profile-substitution case study is the paper's most demonstrable value proposition.** Showing that swapping a JSON profile (Zhang 2025 OPECT: Gmax/Gmin=47.3, 34 states) produces a deployment accuracy number (88.53%) without code changes is concrete and differentiates from AIHWKIT/MemTorch. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)
4. **Energy model is appropriately humble.** Framing 11.45× as an upper bound and providing routing-overhead sensitivity (→ 9.9× at 50% overhead) signals intellectual honesty that reviewers rarely see. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)
5. **The "6-bit ADC cliff" is a hardware-actionable finding.** The ADC sweep (27% at 4-bit → 80%+ at 6-bit) directly tells a chip designer where to allocate converter area. This is the kind of system-implications result NC's interdisciplinary audience values. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

***

## Specific Recommendations

**1. State "simulation-only" more prominently — the abstract needs one sentence.**
The current abstract says *"literature-derived or measured device assumptions"*  — the word "measured" here is ambiguous (it refers to literature sources, not your own measurements). Replace with: *"Using literature-derived proxy parameters in the absence of author-fabricated devices, we present…"* This inoculates against the reviewer complaint and signals honesty upfront. The current cover letter disclosure is good but abstract-level is where NC editors look first. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**2. Reframe the NL=2.0 finding as an "approximation boundary" throughout — including abstract and conclusion.**
The current conclusion reads *"severe write non-linearity remains a hard boundary for the present first-order approximation"*  — this is internally consistent but the word "hard boundary" recurs in the abstract and cover letter without the qualifier. Every instance outside the discussion/limitations section should read: *"approximation limit of the gradient-scaling surrogate at NL=2.0"*. This is a one-pass text edit that eliminates a factual inconsistency without weakening the finding. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**3. Add a minimal Ensemble HAT ablation to the supplementary.**
You need at least one of: (a) accuracy vs. resampling frequency (every 1, 5, 10, 25 epochs), (b) comparison against naive noise augmentation (same σ but fixed D2D), or (c) a second architecture (ConvNeXt) showing the same fresh-instance recovery. Option (b) is the cheapest to run and the most important — it isolates the contribution of D2D structural resampling from general noise robustness. Without it, the paper cannot defend "Ensemble HAT" as a distinct contribution vs. "more noise augmentation."

**4. Upgrade the AIHWKIT cross-validation scope.**
The current sanity check is one data point (ResNet-18, CIFAR-10, 4-bit, matched regime). Add 2–3 more matched-regime comparison points — at minimum ConvNeXt and/or a different noise level. This costs one experiment run and substantially strengthens the claim that your framework produces "qualitatively equivalent results" to a mature toolkit. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**5. On collaborative validation: contact Vincze/Zhang groups — but as a parallel track, not a blocker.**
The Vincze 2025 paper is Early Access with a DOI; emailing the group for the raw conductance CSV (Gmin, Gmax, 5–10 write-verify cycles) would give you one real calibration point. This does not require co-authorship — a "data courtesy" acknowledgment is sufficient. Even one real conductance window measurement would shift the paper from "all parameters are proxies" to "framework calibrated against one measured device." This is a 2–3 week side effort, not a blocker. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

**6. Flowers-102 failure needs a sharper hypothesis.**
The paper currently says data starvation is "a working hypothesis rather than a settled causal claim". This is fine scientifically, but NC reviewers will ask what you tried. Adding one experiment — e.g., ConvNeXt on Flowers-102 with 10× augmented training data, or with HAT initialized from a pre-trained checkpoint — would either confirm the hypothesis or rule it out. Right now it reads as an unexplained result. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d8901851-4c66-48ed-bc59-14fcdf6a128a/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=t2477VeYrTfQrp0wzYWvDat3TQA%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

***

## Final Verdict

**Recommendation: (A) with targeted supplementary additions before submission, and (B) as a parallel 3-week side effort.**

Submit now as a pure simulation methodology paper, but first add: (i) the Ensemble HAT ablation, (ii) 2–3 additional AIHWKIT cross-validation points, (iii) the NL=2.0 reframing pass, and (iv) a clearer "simulation-only" signal in the abstract. These are all in-simulation additions that can be completed in 1–2 weeks. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/3c839e1f-e46c-40a9-85e9-8d29e22b0f3d/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=SXo7%2FOV0yLW6MNfa5qZao69q2p0%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

Simultaneously, email the Vincze group for raw conductance data — not to delay submission, but so that if a reviewer asks "where is your hardware anchor?", you have a response ready for the revision round. Nature Communications routinely accepts papers at Major Revision with the instruction to add physical validation data; having it ready-to-go transforms a potential rejection into a smooth revision. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/aa569c4d-44c6-4a34-a4c3-1f5f2ea304e1/cover_letter.pdf?AWSAccessKeyId=ASIA2F3EMEYEQUT64TCR&Signature=%2B%2BCWQfGEW25FShmiF8CD1jnn7Ys%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIEhIr0vaGIfD1lugoD9IehwB3cuE%2BVrM4bKNuBSPsLG6AiA2xSEfHs%2B1bR485CSCV7cwVqanQHN9ZDXPGxISFkv1WyrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMeXdtMyVbrPA%2B0y3PKtAE3z%2FnME22N1VlDx1KfNV13yUe0GSEN%2BvkRCEZ7cm4%2BdvuFL6YYXr20OvLCcaiTl4YxFHuORoPOzL282L1r2B1V8KLoLq1L4lOrGMi1B77uxJZdJrGlhbBglOFs0lmM%2BmDGhV%2BkCigQMIRC7%2BOyRqp3d9xkT1Ko4HotTtx0xvemAibX0F3VBZ31%2F8DE5%2FSFsEBAl1v1IcumJG%2F4dNAYOtZ0KLpiTOvk%2Bi14j7T8BushFXZkQXuyZ7ZdUCHiVkWacfk%2BpT9rf0k2tguXl1AOo7Br0ryHCYBamqXg5%2BAFOANsP7MVRofz%2BPv0V6phIf1Noa%2FTTavDBL5aLvORZ3iCpQIU8CbwfaZA6HBKg13d%2ByPFXd6LBFDF8kOVyVeYndmjkm3vTWZWAdOf8%2FF8reKlRtRS3eXVbJESuIRgBnVlh7vDtK%2FFJ%2F3gZ43YdTpEGH5x%2BmKYCxUmPOAtu2Gkgflc8CZFEfUBtfkpKQJof1QEi4Su3%2BGYsvpW0UX6%2FoI3hz%2FxZBj8c9liuLqaYWt%2FhUKC9OyeWvkvfZudQVR%2BCypA96bM9cBdBt%2FoOG5VE8dfrxCFiZfZpG8M51P%2BMO%2FImzjrbK5rRVyA6wAclfauaUmDWfx1QosENUAheeFHRc6igLBpOvhHPclRvWv9r2X2isP01x3F8PBSq9BG9r3EfS%2FLEUhYMLGBI0H3vADT1vJd1DwlHxNMjAvePz5AzrInZwgfS5BKYEikhx6NuVqpuOwBA81GVs9AIudNOb7yxVxiULMLQ2QYAoLSu2MQc0l%2BfxO3y%2BCWDCcounOBjqZATEQKfzpkqUWfJfvcn9hOTNjUbmMZM3r31ds%2BSIbCseRVOokRt10Yi1%2FnKS0RupmQNY9H8GVPeF4JdWUz9Kwtxc9sUvWq5uWbPu%2BUiCK6J8tDK5OegwjQlQmojZ7KdglRQE7jrKH0yOGc%2FYB%2BBl58yf0CPMmqqegMZeW8KczMbqCakv23CXZvRmIDinWstwXbHiYutsLzHaOrw%3D%3D&Expires=1775916349)

The paper's core scientific contribution — that **D2D instance overfitting is a more dangerous failure mode than quantization for analog foundation models, and that multi-instance-aware training is the remedy** — is a genuinely useful finding that NC's systems + materials readership will find relevant. The risk is not the idea; the risk is leaving fixable technical gaps open for reviewers to exploit.

##kimi

## 总体建议
**重大修订（Major Revision）**

这篇论文在方法学上严谨且贡献清晰，但**缺乏实测器件验证**这一事实几乎必然导致审稿人要求补充实验对比或明确限定范围。建议**现在投稿**，但需为重大修订做好准备，而非期待直接接受。

## 评分
- **方法学严谨性**: 4/5
  - *优势*: 与AIHWKIT的对照验证（90.08±0.21% vs 95.46%）提供了合理的 sanity check；物理简化（均匀保持、梯度缩放NL）在Section 6.5和Supplementary Section 1.3-1.4中有明确披露和敏感性边界分析；Profile接口包含自动化拟合管道（Supp. 1.10），不仅是JSON包装器，而是系统性的四类别数据标准化（脉冲编程、C2C、D2D、保持）。
  - *扣分*: 所有参数均为文献代理值（Vincze/Zhang），缺乏哪怕单一批次真实器件的闭环验证。

- **科学贡献**: 4/5
  - *优势*: **Ensemble HAT（10%→86.37%）是新发现**——首次量化了Transformer在CIM中的硬件实例过拟合问题，并提出训练时D2D重采样的解决方案；6-bit ADC悬崖（Supp. Fig. S1）为硬件设计者提供了明确的精度设计目标（≥6-bit）；跨架构（CNN vs ViT）和跨数据集的瓶颈分析（量化不主导）证据充分（Table 4, Fig. 3-4）。
  - *扣分*: 评估仅限CIFAR-10/100和Flowers-102，缺乏更大规模数据集（如完整ImageNet推理）的验证，尽管使用了Tiny-ViT-5M预训练权重。

- **NC适合度**: 3.5/5
  - *优势*: 完美契合NC的跨学科定位（材料科学+机器学习系统+新型计算范式）；填补了有机光电材料到边缘视觉部署的评估空白。
  - *扣分*: Nature Communications虽接受方法学论文，但**纯仿真性质**在"材料-器件"类期刊中风险较高，审稿人可能质疑其技术就绪水平（TRL）。

## 关键弱点（前3）
1. **零实测器件验证（Zeroth-order Experimental Validation）**: 所有设备参数（σC2C、σD2D、NL、保持时间）均来自文献代理值（Supp. Table S2）。审稿人会质疑："如果实测数据与文献值偏差20%，结论是否仍然成立？" 这是最大攻击点。

2. **物理模型的近似极限（Approximation Limits）**: 
   - 非线性写入（NL=2.0）使用**梯度缩放近似**（Section 3.2），而非物理脉冲级仿真，文中"硬边界"（hard failure mode）表述可能过强。
   - 缺乏温度模型（Section 6.5承认），而有机器件对温度敏感（Melianas et al. 2020, Science Advances）。
   - IR drop和sneak path仅作敏感性分析（Supp. Table S7），未进行全电路仿真。

3. **任务复杂度与规模限制**: 仅在CIFAR级数据集（32×32）上验证，未展示在更高分辨率（如224×224 ImageNet验证集）上的性能衰减规律，限制了结论向真实边缘视觉场景的推广。

## 优势
1. **系统性方法学贡献**: Profile-driven接口实现了"文献数据→部署评估"的标准化桥接，降低了领域门槛。
2. **Ensemble HAT策略**: 解决了D2D过拟合这一被忽视的关键问题，具有跨器件（不仅限于有机）的普适价值。
3. **透明的不确定性量化**: 所有关键主张均附带蒙特卡洛误差条（如86.37±1.54%），敏感性分析（Supp. Table S3, S7）展示了参数稳定性。

## 具体建议
1. **明确仿真标识**: 在**标题**或**摘要首句**中加入"Simulation"或"Profile-driven Simulation"字样（如"Hardware-Aware **Simulation** of..."），并在Cover Letter中明确声明"本工作为计算仿真研究，旨在建立材料-系统评估桥梁，实验验证将作为自然延伸"。当前披露足够，但需更前置。

2. **软化NL=2.0表述**: 将"hard failure mode"改为**"approximation limit of the current gradient-scaling surrogate"**（当前梯度缩放代理模型的极限），并在Section 6.5明确说明："低于27.72%的准确率可能源于近似失效，而非器件物理极限"。

3. **投稿策略**: **选择(A)现在投稿**，但**同步联系Vincze/Zhang团队**寻求合作。在Cover Letter中可补充："While the present work relies on literature-derived priors, we have initiated collaboration with [Vincze/Zhang] for measured-device validation, which will be reported in the revision." 这样既展示了前瞻性，又为重大修订期的补充实验预留接口。

4. **补充对照（修订期准备）**: 准备添加一个"Digital Baseline with equivalent noise injection"对照，证明性能损失确实来自模拟部署而非单纯噪声；若可能，补充一个基于实测I-V曲线的单器件验证（哪怕是非阵列级）。

## 最终裁决
我们应该：
- **(A) 现在作为纯仿真论文投稿**

**理由**: 
- 方法学贡献（Ensemble HAT、6-bit悬崖、Profile接口）已足够坚实，延迟投稿的边际收益低于时间成本。
- NC的审稿周期（通常2-3个月）可作为寻求合作验证的并行时间窗口。
- 预期审稿人会要求"重大修订"（补充实测数据或严格限定适用范围），但这是可管理的修订路径，而非拒稿。

**风险提示**: 若审稿人坚持要求**阵列级实测验证**，可能需要降级至*Advanced Electronic Materials*或*Advanced Intelligent Systems*（更侧重器件-系统协同设计）。建议在回复中强调"本框架旨在降低芯片流片前的评估风险（pre-tapeout risk assessment）"，以符合方法学论文的定位。

## deepseek

## 总体建议
**重大修订 (Major Revision)** — 倾向有条件接受，但必须明确界定声明范围并软化部分断言。纯仿真性质在明确定位为方法学论文的前提下是可接受的，但当前稿件中存在几处过度延伸的声明需要收紧。

---

## 评分

- **方法学严谨性**: 3.5/5
- **科学贡献**: 4/5
- **NC适合度**: 3.5/5

---

## 关键弱点（前3）

### 1. Profile接口的"贡献权重"被夸大
稿件将"profile-driven substitution interface"定位为核心贡献之一（"first profile-driven...simulator for organic optoelectronics"），但实质上这是一个JSON参数解析器。AIHWKIT、MemTorch、CrossSim都有等效的参数化机制；将参数外部化为JSON是工程实践而非科学创新。稿件应将其降级为"实现特性"而非"核心贡献"，将贡献重心转移到**Ensemble HAT发现**和**对有机特定瓶颈的系统性剖析**上。

### 2. "Scale Masking"效应的因果推断不完整
V2在无噪声下达到97.39%被归因于"scale masking"（σ_w ≈ 0.38 LSB），但这一分析缺失了关键的对照实验：如果将C2C噪声增大到使σ_w > 0.5 LSB，精度应出现可预测的阶梯式下降；或者固定噪声、降低量化位数（如2-bit），验证masking效应消失。当前证据是相关性而非因果性。建议在SI中补充一个简单的"噪声幅度扫描 × 量化位数"热力图，直接验证LSB阈值假说。

### 3. NL=2.0 "硬边界"声明的过度确定性
稿件声称NL=2.0时27.72%的精度代表"gradient-scaling approximation的极限"而非"材料约束"。这是正确的谨慎表述——但正文中的措辞（"remains a hard failure mode"、"sharp failure boundary"）可能被误读为物理极限。更关键的是，**没有对照实验证明这不是优化问题**：是否尝试过（1）降低学习率、（2）更长的训练周期、（3）不同的STE缩放函数？在缺乏这些对照的情况下，"硬边界"声明应软化为"在当前HAT配置下的恢复极限"。

---

## 优势

1. **Ensemble HAT的发现具有跨领域价值**：10%→86%的恢复不是增量改进，而是揭示了标准HAT实践中的系统性盲区（单实例过拟合）。这一发现对任何依赖D2D变异建模的模拟CIM研究都有借鉴意义，而不仅限于有机器件。

2. **实验矩阵设计严谨且可复现**：V1-V8的版本控制、三种子汇总（Table S1）、蒙特卡洛误差条、与AIHWKIT的对照验证共同构成了高质量的仿真卫生实践。SI中的参数敏感性分析（Table S3）和状态依赖保持对照（Table S5）增强了声明的可信度。

3. **审稿人问题的系统化处理**：106/109（97.2%）的预解决率表明稿件已经过严格的内部审查。这将体现在稿件质量和回复信的准备程度上。

---

## 具体建议

### 1. 摘要中的"纯仿真"披露
**当前披露不足**。摘要未提及"simulation"或"behavioral"的限定词，首句即声称"present a profile-driven...framework"，容易被误读为包含硬件验证。建议修改：
> "We present a **simulation** framework that maps literature-derived or measured device assumptions into task-level accuracy..."
> 
> 或在末尾添加："**The framework operates at the behavioral simulation level; validation against physical hardware remains future work.**"

### 2. NL=2.0 "硬边界"措辞
改为：
> "Severe write nonlinearity (NL=2.0) limits recovery to 27.72±0.82% **under the present gradient-scaling approximation and training budget**, marking the regime where first-order behavioral modeling becomes insufficient."

### 3. 合作验证策略
**不建议在投稿前寻求合作验证**。原因：
- 引入外部合作会增加时间不确定性（数月级别）
- 合作者可能要求共同作者身份，影响贡献声明
- 纯仿真方法学论文在NC有先例可循（如AIHWKIT的初始论文）

**替代方案**：在"Future Directions"中明确承诺后续验证路径，并考虑在修订阶段提供**仿真-实测对照的预注册方案**作为诚意信号。

---

## 最终裁决

### 我们应该：**(A) 现在作为纯仿真论文投稿** — 但附带以下条件性修改

**理由**：
- 方法学贡献（Ensemble HAT + 有机特定瓶颈系统学）已足够支撑一篇NC论文
- 等待硬件验证的边际收益递减：即使获得数据，核心发现（D2D过拟合、ADC悬崖）不太可能被推翻
- 将验证留作"未来工作"是合理的研究边界划分

**投稿前必须完成的修改清单**：

| 优先级 | 修改项 | 位置 |
|--------|--------|------|
| 🔴 强制 | 摘要和引言中明确"simulation/behavioral"限定 | Abstract, §1 |
| 🔴 强制 | 将Profile接口降级为"工程特性"，贡献重心移至Ensemble HAT | §1 (contributions), §3.3 |
| 🟡 强烈建议 | 补充LSB阈值验证（噪声扫描 × 量化位数热力图） | SI §1.3新增 |
| 🟡 强烈建议 | 软化NL=2.0 "硬边界"措辞 | §5.6, §6, Abstract |
| 🟢 建议 | 在Limitations中明确说明"未与有机实测器件交叉验证" | §6.5 |
| 🟢 建议 | 将AIHWKIT对照从"sanity check"升级为"validation against mature simulator" | §1.9 (SI) |

**如果审稿人要求硬件验证**：准备回复策略——
> "We agree that physical validation is the natural next step. The present work intentionally scopes itself to simulation methodology, establishing the behavioral baseline against which future measured-device studies can be calibrated. We have added a pre-registered validation protocol in Supplementary Section X to facilitate this follow-on work."

**如果被拒稿的备选方案**：
- *Advanced Intelligent Systems*（Wiley，IF ~7）：对方法学论文友好，接受纯仿真工作
- *Neuromorphic Computing and Engineering*（IOP）：更专业但影响力较低

---

**审稿人最终意见**：这是一项设计良好、执行严谨的模拟研究，揭示了对模拟CIM社区有实际价值的新见解（Ensemble HAT）。主要缺陷在于声明范围的界定而非方法学质量。通过上述修改，我认为它可以作为方法学论文被NC接受。

## doubao

```markdown
## 总体建议
重大修订

## 评分
- 方法学严谨性: 4/5
- 科学贡献: 4/5
- NC适合度: 4/5

## 关键弱点（前3）
1. 无真实器件的闭环验证，框架保真度未被物理实测证实。所有实验均基于文献提取的代理参数和行为级仿真模型，未完成「实测器件参数输入→仿真结果输出→与硬件实测性能对标」的闭环，无法证明框架对真实有机光电器件的预测准确性，是审稿人首要质疑的核心硬伤。
2. 非线性写入模型简化与主张过度延伸。当前NL模型采用一阶梯度缩放近似，而非脉冲级精确物理建模，声称的NL=2.0「硬边界」仅适用于该简化模型，并非真实器件的物理极限，存在明显的过度延伸；同时未验证该近似在不同NL范围、不同器件体系下的普适性，结论边界条件不清晰。
3. 核心发现的普适性验证不足。核心实验仅覆盖中小规模数据集（CIFAR-10/100、Flowers-102）和轻量级架构，未在ImageNet等大规模通用视觉数据集、更复杂的ViT架构或检测/分割等下游边缘视觉任务上，验证Ensemble HAT、ADC精度悬崖、瓶颈层级等核心发现的普适性，限制了工作的通用指导价值。

## 优势
1. 填补领域核心空白，构建了首个面向有机光电器件的PyTorch原生、profile-driven存算一体仿真全流程，解决了现有无机CIM仿真工具无法适配有机器件特有非理想特性（光电前端响应、双指数保持衰减、非线性写入不对称性）的痛点，标准化接口实现了文献数据到系统级部署评估的无缝桥接，可复用性极强。
2. Ensemble HAT具备实质性创新与通用价值，针对Transformer模拟CIM部署中严重的硬件实例过拟合问题，提出训练时逐epoch重采样D2D失配掩码的策略，在几乎不增加训练开销的前提下，将新硬件实例零样本迁移准确率从10%的随机水平提升至86.37±1.54%，该方法不仅适用于有机器件，对整个模拟存算一体领域均有广泛指导意义。
3. 系统级重构了有机CIM部署的瓶颈优先级，通过严谨对照实验与全面敏感性分析，推翻了「量化是核心部署瓶颈」的传统认知，明确了ADC转换精度、硬件实例鲁棒性、非线性写入动态为三大主导限制因素，为有机光电材料优化、硬件电路设计提供了清晰可落地的指导。
4. 工作透明度与复现性极高，正文与补充材料完整披露了所有参数溯源、实验配置、模型细节与敏感性分析结果，提供了三种子的复现性验证，配套自动化器件参数拟合工具，承诺了代码与数据集开源，完全符合Nature Communications的发表规范与跨学科读者需求。

## 具体建议
1. 前置「纯仿真」的明确声明。在摘要、引言开篇、讨论核心部分，明确声明本工作为**纯仿真方法学研究**，所有结论均基于文献代理参数与行为级仿真模型，真实硬件闭环验证为未来规划的核心工作。当前仅在局限性部分披露的方式易引发审稿人负面印象，前置声明可主动管理审稿预期，规避核心争议。
2. 软化非线性写入相关主张，补充边界验证。将NL=2.0「硬边界」的表述修改为**「当前一阶梯度缩放近似下的性能极限」**；在讨论部分明确该结论的边界条件，说明真实器件的NL容忍度可通过脉冲编程方案、梯度估计方法优化得到提升；在补充材料中补充NL=1.0/1.5/2.0/2.5的梯度实验，进一步明确极限适用范围，消除过度延伸风险。
3. 主动回应硬件验证核心质疑，无需等待完整流片。不建议延迟投稿等待完整流片验证，但强烈建议投稿前完成两项动作：① 联系Vincze/Zhang团队，申请获取其已发表器件的实测统计数据（而非代理值），完成至少一组「实测参数输入→仿真输出→与该器件已发表小网络性能对标」的闭环验证，哪怕是MNIST简单网络，也能极大夯实框架保真度；② 若无法获取实测数据，在投稿信、讨论与局限性部分，明确承诺录用后6个月内与合作团队完成真实器件闭环验证，并更新开源代码库的实测器件配置文件，将硬件验证定位为自然延伸而非先决条件。
4. 补充核心发现的普适性验证，完善对照实验。① 在补充材料中补充至少一组ImageNet-1K子集的轻量级验证实验，证明核心发现在大规模数据集上的一致性；② 补充Ensemble HAT与现有解决D2D过拟合的主流方法（对抗训练、后训练校准、数据增强）的性能与训练开销对比，凸显方法创新优势；③ 补充与AIHWKIT、NeuroSim等成熟工具在有机器件模型下的系统性对标，而非仅单一ResNet-18对照，进一步证明框架可靠性。
5. 明确核心结论的适用边界，规避绝对化表述。在讨论部分明确所有核心结论的适用条件，例如「6-bit ADC悬崖」是基于当前SAR ADC模型与128×128阵列规模的结果，不同读out电路架构、阵列尺寸会改变该阈值；「量化非核心瓶颈」仅适用于4-bit及以上量化水平，更低位宽下结论可能不成立，消除绝对化表述带来的审稿争议。

## 最终裁决
我们应该：
- (A) 现在作为纯仿真论文投稿

理由：本工作的跨学科创新性、方法学完整性与核心发现的通用价值，完全契合Nature Communications的发表定位；NC此前已发表多篇同领域的纯仿真方法学论文，纯仿真性质并非发表的硬性障碍，核心是通过上述修改主动管理审稿预期、明确回应硬件验证质疑，无需延迟投稿等待完整流片。本工作的影响力与创新高度远超专业领域期刊范围，无需降级投稿，具备冲击Nature Communications的充足潜力。
```

## hunyuan

总体建议

小修（Minor Revision）

评分

• 方法学严谨性: 4/5  

• 科学贡献: 4/5  

• NC适合度: 4/5  

关键弱点（前3）

1. 缺乏实测器件验证：完全依赖文献代理值（Vincze 2025, Zhang 2025）和模拟数据，未通过物理器件实测验证框架预测能力，易被质疑“仿真与现实的鸿沟”。  
2. 物理简化模型的局限性：明确披露了均匀保持、梯度缩放非线性写入（NL）近似、无温度模型等简化（补充材料1.3.4、6.5节），但审稿人可能认为这些简化削弱了结论的普适性（如NL=2.0“硬边界”实为近似极限）。  
3. 部分主张的过度延伸：如“量化不是主导瓶颈”需限定条件（仅在均匀噪声+尺度恢复下成立，比例噪声下失效，见5.2节）；“D2D最重要”未充分排除任务复杂度、数据量的交互影响（6.3节“数据饥饿假说”）。  

优势

1. 创新的Profile-Driven接口：实现文献参数到部署评估的无缝桥接（main.pdf 3.3节），含自动化配置文件拟合管道（补充材料1.10），支持跨技术（如Zhang 2025 OPECT案例）零样本迁移（88.53%准确率）。  
2. Ensemble HAT的核心发现：通过D2D重采样解决硬件实例过拟合，将新实例准确率从10%（随机水平）提升至86.37±1.54%（main.pdf 5.4-5.6节），为CIM鲁棒性训练提供新范式。  
3. 系统化的瓶颈层级分析：明确“6-bit ADC悬崖”“转换器精度>量化”“新鲜实例鲁棒性>静态噪声”等可操作洞见（5.2、6.1节），并通过敏感性分析（表S3-S4）验证结论稳定性。  
4. 详尽的透明化披露：补充材料完整记录参数溯源（表S2）、三种子重复现（表S1）、非理想性测试（差分对不对称、IR压降等，表S6-S7），符合NC对可复现性的要求。  

具体建议

1. 明确声明“纯仿真”定位：在摘要和引言中直接加入“本工作为纯仿真方法学论文，旨在提供部署前风险评估工具，未来物理验证为自然延伸”，避免审稿人对“硬件缺失”的误解（当前cover_letter已提“first-order behavioral simulation”，但需强化）。  
2. 软化“硬边界”表述：将NL=2.0的“硬边界”改为“梯度缩放近似下的性能极限”（补充材料1.3.3、6.5节），并引用“未来需结合脉冲级编程物理验证”（main.pdf 6.6节）。  
3. 补充关键对照实验：增加与无机RRAM模拟器（如AIHWKIT）在相同噪声参数下的定量对比（现有仅ResNet-18单点对照，main.pdf 1.9节），强化“互补工具”定位。  
4. 投稿前考虑合作验证：联系Vincze/Zhang团队获取实测器件参数或初步验证结果（如共享配置文件），可作为“未来方向”的案例增强说服力（非必需，但能降低审稿风险）。  

最终裁决

我们应该：  
• (A) 现在作为纯仿真论文投稿  

理由：框架的方法学贡献（Profile接口、Ensemble HAT、瓶颈分析）明确且符合NC跨学科定位，透明披露和详尽补充材料已回应潜在质疑。通过小修强化纯仿真声明、软化过度表述后，可直接投稿。实测验证可作为后续工作（main.pdf 6.6节“future directions”），不影响当前论文价值。

## mimo

## 总体建议
**小修**。论文作为一篇纯仿真方法学论文是扎实的，其核心贡献（Ensemble HAT、Profile接口、瓶颈分析）具有明确的系统级洞见。主要风险在于缺乏硬件验证，但通过充分披露局限性并正确定位，可以满足Nature Communications对方法学创新和跨学科意义的要求。

## 评分
- **方法学严谨性: 4/5**
  - 框架验证充分：提供了与AIHWKIT的对照实验（90.08±0.21% vs 数字95.46%），证明了仿真器在匹配条件下的定性趋势一致性（1.9节）。
  - 物理简化（均匀保持、梯度缩放NL）在补充材料中有明确披露和敏感性分析（如Section 1.3.4的均匀vs状态相关保持对比，差异<0.1pp），在“第一阶行为仿真”的定位下是可接受的。
  - “Profile-driven”接口是真正的贡献，而不仅是JSON包装器。它在方法（3.3节）中定义为“核心贡献”，实现了从文献或测量数据到部署评估的无缝、无需改代码的桥接，并在案例研究（5.8节）中得到了验证（Zhang 2025 OPECT配置文件达到88.53%）。

- **科学贡献: 4/5**
  - **Ensemble HAT是新的系统级发现**，而非简单的数据增强。它直接解决了标准HAT导致的“硬件实例过拟合”（V4在新实例上崩溃至10%）这一关键部署风险，并提供了有效的训练策略（10% -> 86.37±1.54%）。这是对硬件感知训练范式的重要扩展。
  - **“6-bit ADC悬崖”为硬件设计者提供了明确的、可操作的洞见**。它指出在当前的有机CIM参数范围内，读出转换器的精度（而非静态权重编程）是系统性能的关键瓶颈（5.2节，6.1节），这对优先分配设计复杂度和功耗具有指导意义。
  - **结论有强有力的证据支撑**。量化不主导的结论基于V2在无噪声下仅轻微下降（97.39%），以及“尺度掩蔽”效应的分析（5.2节）。D2D最重要的结论由V4在新实例上的崩溃（10%）和Ensemble HAT的显著恢复直接证明（5.4， 5.6节）。

- **Nature Communications适合度: 4/5**
  - **高度适合NC的跨学科范围**。工作明确处于材料科学（有机光电器件特性）、机器学习系统（HAT、ViT部署）和新兴计算范式（CIM）的交叉点，与NC读者群高度契合。
  - **纯仿真性质是明确的局限，但方法学贡献足够**。论文定位为“第一阶行为仿真框架”和“材料到系统的决策桥梁”，而非芯片预测模拟器。其价值在于提供了一个在芯片制造前评估部署风险的透明工具，这本身具有重要的方法学意义。投稿信中的编辑总结也强化了这一定位。
  - **推荐“小修”**。主要修订应限于加强局限性讨论和软化个别表述，而非要求补充硬件验证数据（这属于未来工作）。

## 关键弱点（前3）
1.  **缺乏物理器件验证**：所有参数均来自文献代理值或假设。尽管已充分披露，但审稿人很可能质疑仿真结果与真实有机器件阵列性能的相关性。这是最显眼的攻击点。
2.  **物理简化的普适性存疑**：均匀保持模型、梯度缩放NL近似等结论是“参数区间特定的”（如1.3.4节所述）。审稿人可能指出，在不同的器件特性下（如更强的状态相关衰减），结论可能不成立。
3.  **部分主张可能过度延伸**：
    - 将NL=2.0称为“硬边界”可能过于绝对，因为它反映的是“当前梯度缩放近似的极限”，而非有机器件的根本物理极限（6.5节）。
    - 将ConvNeXt在Flowers-102上的失败归因于“数据饥饿假说”时，语气可以更谨慎，因为存在其他替代解释（6.3节）。

## 优势
1.  **系统级洞见明确**：清晰地颠覆了“量化是主要瓶颈”的直觉，指出了ADC精度、实例过拟合和非线性写入等更关键的部署风险。
2.  **方法学创新实用**：Profile接口和Ensemble HAT策略是可复用、可推广的工具，对社区有直接价值。
3.  **分析透明度**：补充材料极其详尽，包含参数溯源、敏感性分析、消融实验（如表S3-S7），体现了良好的科研实践。
4.  **跨学科桥梁作用**：成功地将器件特性与现代视觉模型（ViT）的部署性能联系起来，回答了领域内一个实际且重要的问题。

## 具体建议
1.  **摘要与定位**：当前摘要和定位是合适的。无需在摘要开头声明“纯仿真”，但应在摘要结尾或引言中再次明确强调“本工作为第一阶行为仿真框架，旨在进行部署前风险评估，物理硬件验证是未来工作”。
2.  **表述软化**：
    - 将NL=2.0是“硬边界”（hard failure mode）的表述，改为“在当前梯度缩放近似下观察到的性能崩溃点”或“标志着当前一阶建模方法的近似极限”。
    - 在讨论“数据饥饿假说”时，明确其为“一个可能的解释”，并同等强调其他潜在因素（如超参数、领域偏移）。
3.  **寻求合作验证**：**不建议在投稿前等待合作验证**。这会严重延误进程。论文当前的价值在于方法和发现，验证是自然的下一步。可以在“未来工作”部分明确列出“与实验团队合作，使用测量数据拟合配置文件并进行闭环验证”。
4.  **加强局限性讨论**：在“讨论”部分，将6.5节“局限性”的要点进行更突出、更结构化的阐述。可以明确列出一个“仿真与现实的差距”表格，总结哪些效应被建模、哪些被简化、哪些被忽略（如温度、光学串扰），并定性讨论其预期影响。
5.  **补充对照**：目前的对照（AIHWKIT）是充分的。无需额外比较。

## 最终裁决
我们应该：
- **(A) 现在作为纯仿真论文投稿。**

**理由**：论文作为一篇方法学和系统分析论文已经完整。其核心贡献（框架、发现、工具）不依赖于特定的硬件验证数据。通过充分、透明的局限性披露和正确的定位（决策桥梁而非芯片模拟器），可以满足Nature Communications对创新性和严谨性的要求。寻求硬件验证将是一个漫长的过程，且可能作为另一篇独立论文的主题。当前工作足以独立发表。

## nemotron

Having read the full manuscript, supplementary information, and cover letter carefully, here is my brutally honest external review assessment.

***

## Overall Recommendation

**Major Revision** — the work is publishable in principle, but three structural issues must be resolved before Nature Communications can credibly accept it.

***

## Scores

- **Methodological Rigor: 3/5**
- **Scientific Contribution: 3.5/5**
- **NC Fit: 3/5**

***

## Critical Weaknesses (Top 3)

**1. The simulation is self-validating in a closed loop.**
The most damaging weakness is that all parameter priors (σD2D = 10%, σC2C = 5%, τ₁ = 140 ms, τ₂ = 610 ms) derive from two Early Access papers (Vincze 2025, Zhang 2025), and the conclusions are then evaluated entirely within the same simulation those parameters define. There is no external ground truth. The AIHWKIT sanity check (90.08±0.21% vs. 95.46% digital) is a *qualitative trend check*, not a physics-equivalence validation — and the paper itself correctly says so. However, the problem is that this is presented as the *only* cross-tool check. A reviewer who has measured organic transistor arrays will immediately ask: what stops this entire hierarchy of limits from shifting dramatically if σD2D is 20% instead of 10%? The sensitivity sweep (Table S3) does extend to 15% D2D and shows 84.59%, which is helpful — but the sweep stays within the same Gaussian-noise behavioral model, never questioning whether the Gaussian assumption itself holds for organic devices. This is a fundamental epistemological gap that cannot be papered over with more Monte Carlo runs. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**2. The "6-bit cliff" and "NL=2.0 hard boundary" are model-specific artifacts, not physical laws.**
The ADC sweep showing a sharp accuracy transition near 6 bits is a property of the specific SAR-like 8-bit proxy energy model and the particular noise magnitude used in this simulator, not a measurement of an organic device. Similarly, NL=2.0 being a "hard boundary" is explicitly acknowledged in Section 6.5 as "the limit of this approximation rather than a fundamental materials constraint"  — yet the abstract and conclusion both use the phrase "hard failure mode" and "hard boundary" without that qualifier. This inconsistency between the limitations section (appropriately hedged) and the abstract/conclusion (overreaching) will be caught by every careful reviewer. It creates an impression that the paper is saying one thing to attract readers and another in fine print to avoid falsifiability. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**3. The "profile-driven" contribution is architecturally thin.**
The core engineering claim — that a JSON-based substitution interface is a genuine contribution — will face skepticism from systems reviewers. The supplementary reveals that the "profile fitting pipeline" (profile_auto_fitter_gpt.py) that makes the interface actually useful for measured data is present in the codebase but not evaluated in the paper. The case study substitutes Zhang 2025's parameters into the JSON format, but Zhang's σC2C and σD2D values are themselves acknowledged as "proxy estimates" (from 8-cycle repeatability and Vth spread, respectively) rather than full conductance-distribution measurements. A reviewer will ask: if the interface's value is profile substitution, where is the demonstration that non-trivial measured data (e.g., correlated D2D, non-Gaussian tails) can flow through this interface and produce qualitatively different insights than Gaussian priors? [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

***

## Strengths

1. **Experimental breadth is genuinely impressive.** Three architectures (ResNet-18, ConvNeXt-Tiny, Tiny-ViT-5M), three datasets (CIFAR-10/100, Flowers-102), and coverage of quantization, noise, retention, NL write, frontend compensation, and fresh-instance transfer in a single paper is unusual and valuable. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

2. **Ensemble HAT is the paper's strongest contribution.** The observation that standard HAT overfits to a single D2D realization and collapses to 10% on fresh instances is a real and reproducible failure mode. The recovery to 86.37±1.54% via epoch-wise D2D mask resampling is clearly demonstrated with three-seed reproducibility. This insight is generalizable beyond organic devices and will resonate with the analog-computing community. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

3. **Transparency about limitations is unusually honest.** The paper systematically flags what is out of scope (IR drop, temperature, sneak paths, correlated crosstalk, non-Gaussian tails) and quantifies some of them with sensitivity tables. This level of self-criticism is rare and works in the paper's favor. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

4. **The energy-accuracy Pareto framing is concrete.** The 273.94 µJ vs. 3140 µJ comparison, with explicit routing-overhead sensitivity (9.90–11.45×), gives hardware designers actionable numbers rather than vague claims. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

5. **Parameter provenance tracking (Table S2) is a model for transparency.** Explicitly distinguishing "directly measured," "proxy estimate," and "canonical default" for each parameter is methodologically exemplary and will help reviewers audit the claims. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

***

## Specific Recommendations

**1. "Simulation-only" must be stated explicitly in the abstract — the current disclosure is insufficient.**
The abstract currently says nothing about the simulation-only nature. The first sentence of Section 4 does disclose it: "all device parameters are literature-derived or proxy-calibrated rather than extracted from fabricated devices". But NC reviewers read abstracts, and many will not reach that sentence before forming a negative prior. A single clause — *"using literature-derived organic device parameters in a first-principles behavioral simulator"* — inserted after "we present a profile-driven simulation framework" would preemptively neutralize the biggest attack vector. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**2. Soften "hard boundary" to "approximation limit" — this is already what the paper means.**
In Section 6.5, the paper already correctly says "the observed failure boundary at NL=2.0 (27.72±0.82%) reflects the limit of this approximation rather than a fundamental materials constraint". The abstract and conclusion must match this language. Replace "hard failure mode" with "approximation-limit failure mode" and add one sentence in the conclusion: *"Whether physical organic devices operate in this regime requires direct NL measurement, which future work should address."* This avoids both overclaiming and underclaiming. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**3. The differential-pair asymmetry sensitivity result (Table S6) is too important to leave in the supplementary.**
The finding that 2% branch asymmetry causes 6% accuracy collapse, and 10% causes complete failure, is a directly actionable design rule for layout engineers. NC's interdisciplinary scope means layout-aware materials researchers are part of the target audience. Moving a condensed version of Table S6 (or at minimum a sentence citing the threshold) into the main text Section 6.5 strengthens the paper's practical value considerably. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=A5AT72L4C35GdNA56lag96B9Plk%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**4. The C2C-invariance result (Table S3-S4) needs a mechanistic explanation, not just a stability label.**
The sensitivity sweep shows that accuracy is completely C2C-independent at fixed D2D (Δmax = 0.00 pp across the entire C2C range at every D2D level). This will strike reviewers as suspicious rather than reassuring — it looks like a copy-paste error in the table. The paper calls it a "stability result" but does not explain *why* C2C has zero measured impact. The correct explanation (scale-masking: C2C noise stays below the LSB threshold of the 4-bit quantization, so it falls into the same weight bin regardless of magnitude) is actually discussed in Section 5.2 of the main text. That mechanistic link must be explicitly made in the supplementary table caption or added as a footnote. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf?AWSAccessKeyId=ASIA2F3EMEYETHB6XZLJ&Signature=9TqA844WURIs0BQJBlA2ZS26oCQ%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJGMEQCIBq1h5r7r%2BUIN0f7m8SL2KnMFirATvH9rPxMqxogat%2FRAiBz0oZolvXKo6GQHt7jvf4g1%2FR%2FDNkB%2BTqTLVI%2BSVr%2FOCrzBAhHEAEaDDY5OTc1MzMwOTcwNSIMf95lIf4Uqeh1RS%2B4KtAEGq3qNzIdo9i1vk4srNqkWFV%2FI36QOwzXpUNXJEKoO935KDcDKOk8BqkNONys0mpFlS94J4ZW5JvSvN9DD3H8DBGLEV%2FLW%2BSX55U8rzuAkASecyNBUdSioXywJ7wlKosFaH6VQustfkPEFgrFdKxWGD%2BqqxuEJ3md3GXe6qMZM4qmMA6Fittoj178q7xt65itN4vR5PGoNpq9XyOFDdHAHJPTYoFlD8NBv21NDBBAe1AQ0HRu%2BYDZhY9EvIZcOe3Z7WzUH3u95a1qA%2Bbg0XFhQyZ8GLkkkUgsoqAX9z%2FSgUb9g99xU0e6jCaPEmnV862i%2FQLeexXOjlKZOHkL2KcS3krVQzFBwtbSdZ20iSlpoRQQBeZCR9tBLdogzMVOO%2B7HzkK%2BMBkEOnlwd34jkCFMMj6apsVKOLVXIYSq3zCnzlQ3KcovEpLYLvaERKaWedu%2BXBTA6UEVBlhQzu7S5V9mDl2C0EyWNkL4%2BtqL%2FMRyp77iuJpjHA6hsfK4qHrE0KCW16orBPK3KN%2FEly%2BbViKglMxugnrG6fhKgLTW3qxzJdJZTmjlgwsftAGGVj%2BoXmrqKEvusI10mI%2F%2FFnVnkzBzE5s8ayM%2BlPVCGm8R0vKmnda1lethzR4a%2FusQVsAIAHMTjUOzG%2Fm4ItE9uCEhR6%2FRY0GSNBgLQEEveYmNkYVjF1AqRQ6zU%2BSPS0qPWiqFULvPY9PCGe%2Fg%2Fir%2FGVXaLEkYnpvkx1Ej%2F7%2FtvD5ZbX0qEMe4hhcobaWr9FrsiRBzVRMFMyk%2FadsbRxqaNHA0pbssCjCsm%2BnOBjqZAQjDUVwmDuS5NzjLvMyDS4GwTCO6jaMiweZQYx2ba%2Fil3nASONbFPD0lU2YCKbAIYPRK2N8b19JihRB23mwDpdaadDNeBg%2BtS1XAJ64jWrnYFOYDduYFgYASScrNA9SWrRkqdswbVSvtyvmjVmLnHLqDnPgpXIRliU0MIeQP9raJhnD%2Fy4Pux9eu6kqGqdfb%2B8nVaoPtguaaGg%3D%3D&Expires=1775916600)

**5. Contact Vincze/Zhang groups — but not as a prerequisite, as a strategic hedge.**
The multi-model consensus to submit without waiting for measured data is correct strategically. However, a brief email to both groups stating *"we use your 2025 Early Access parameters in our simulator; if you have measured full-conductance distributions that differ from our Gaussian proxy assumptions, we would credit your contribution in the acknowledgments"* accomplishes two things: it signals good faith to reviewers who might include these authors, and it potentially provides a rapid response to the most likely reviewer objection. This is not about delaying submission — it takes one week and can run in parallel.

***

## Final Verdict

**Recommendation: (A) Submit now as pure simulation, with targeted abstract and language fixes before pressing submit.**

The paper should not wait for hardware validation. The simulation-only nature is a *positioning* problem, not a scientific one — and it is solvable in three hours of text editing. Here is the priority order:

1. Add one "simulation-only" clause to the abstract *(1 sentence)*
2. Align "hard boundary" language in abstract/conclusion with Section 6.5's hedged version *(2 sentences)*
3. Add a mechanistic footnote explaining C2C invariance in Table S3-S4 caption *(1 sentence)*
4. Move asymmetry sensitivity threshold to main text Section 6.5 *(1 sentence + table reference)*
5. Send a courtesy email to Vincze/Zhang groups *(parallel to submission preparation)*

The risk of "Major Revision requiring hardware validation" is real but manageable. NC reviewers in the materials-science community will be more sympathetic to simulation-only papers than IEEE reviewers, precisely because device-physics modeling papers routinely precede fabrication in that community. The Ensemble HAT finding is strong enough to carry the paper if the positioning is clean. What kills simulation-only papers at NC is not the absence of hardware — it is the *impression* that hardware results were suppressed or that claims are stronger than the simulation supports. The two language fixes above directly address that impression.

The one scenario where you should reconsider venue is if the reviewer pool at NC turns out to be dominated by ML-systems reviewers rather than materials+devices reviewers. In that case, **Advanced Intelligent Systems** or **npj Computational Materials** would be higher-probability targets with identical impact visibility for the organic-device community.

## glm

## 总体建议
重大修订

## 评分
- 方法学严谨性: 4/5
- 科学贡献: 4/5
- NC适合度: 4/5

## 关键弱点（前3）
1.  **缺乏真实硬件验证**：这是最根本的潜在缺陷。尽管论文将框架定位为“第一阶行为模拟器”而非“脉冲精确的电路仿真器”，并充分披露了其局限性（如无温度模型、简化物理效应），但Nature Communications的审稿人，特别是来自实验器件领域的审稿人，极有可能质疑在没有直接与实测有机芯片结果对比的情况下，框架预测的“部署风险”和“能量效率上界”的可靠性。这构成了一个关键的“真实性”缺口。
2.  **物理模型的简化与近似依赖**：论文明确指出非线性写入（NL）的建模采用“梯度缩放近似”，其观察到的失效边界（NL=2.0）反映了该近似的极限，而非根本的材料约束。审稿人可能会批评这种近似过于粗糙，无法捕捉更复杂的写入动力学，并质疑由此得出的“硬边界”结论在更真实的物理场景下是否依然成立。类似地，均匀保持模型与状态相关模型在Ensemble HAT regime下差异很小，但未能证明在标准HAT崩溃路径下是否同样有效。
3.  **“硬边界”与“主导瓶颈”表述的强度**：诸如“非线性写入是硬边界”、“量化不是主导瓶颈”等断言，在仿真语境下可能被审稿人认为过于绝对。审稿人可能要求提供更细致的条件限定，或要求在不同架构/数据集上验证这些结论的普适性，以避免“过度延伸”。

## 优势
1.  **明确且有价值的方法学贡献**：提出的“Profile-driven”接口并非简单的JSON封装，而是一个设计精良的、允许文献档案无缝替换并产生部署评估结果的桥接工具，实现了从设备参数到系统级指标的端到端评估。Ensemble HAT策略针对“硬件实例过拟合”这一在模拟硬件部署中未被充分重视的问题，提供了新颖且有效的解决方案（从10%恢复至86%），方法创新性突出。
2.  **极高的复现性与透明度**：论文在补充材料中详细列出了所有参数来源（文献索引及具体取值），提供了三种子实验的复现性摘要（87.95±0.27%），并针对关键参数（如C2C/D2D噪声）进行了系统性的敏感性分析。这种严谨的开放性在仿真方法学论文中是顶尖水平，极大地增强了结果的可信度。
3.  **精准且可操作的见解**：论文成功地将研究焦点从泛泛的“模拟硬件噪声”转移到有机CIM部署中更具体、更关键的瓶颈识别上，例如揭示了“ADC分辨率悬崖”（6-bit是关键阈值）和“新鲜实例迁移性”问题。这些见解对于有机材料和硬件设计者具有直接的指导意义，体现了真正的跨学科价值。

## 具体建议
1.  **关于“纯仿真”声明**：**无需在摘要中额外强调“纯仿真”**。当前的披露（在Introduction和Limitations部分明确界定框架范围）已经足够且专业。在摘要中刻意添加此类声明，反而可能主动凸显弱点。应保持现有自信的语气，侧重于框架作为“决策桥”和“风险评估工具”的价值。
2.  **关于NL=2.0“硬边界”**：**表述需要软化**。建议修改为：“在当前基于梯度缩放的非线性写入近似模型下，NL=2.0标志着一个清晰的性能失效边界”。同时，在讨论部分应更明确地将此结论框定为“对当前模拟方法的失效限制的刻画”，而非“物理世界的根本极限”。这有助于管理审稿人期望。
3.  **关于寻求合作验证**：**强烈建议尝试，但不作为投稿先决条件**。在投稿的同时，可以迅速联系Vincze或Zhang团队，礼貌地询问是否可以基于您的框架对其已发表数据进行快速复现验证，并索取一份简短的验证声明。即使是一封简单的邮件，说明“该框架可以成功加载我们的参数并产生与物理直觉一致的定性趋势”，也将在审稿期间作为强有力的补充材料，显著回应“硬件验证”的关切。

## 最终裁决
我们应该：
- (A) 现在作为纯仿真论文投稿

**理由**：论文已成功定位为一篇扎实的**方法学论文**，其核心贡献（Profile驱动接口、Ensemble HAT）是独立于具体硬件实现的新颖算法与工具。框架在共享regimes下与成熟工具（AIHWKIT）行为一致，并展现了极高的复现性与透明度。缺乏硬件验证是一个重要的弱点，但可以通过在文中更谨慎地限定结论、在讨论中更主动地提出物理验证作为未来工作方向，并尝试在审稿期间获取合作验证信来有效管理。直接投稿并定位为方法学创新，是当前最大化效率并符合NC跨学科发表标准的最佳战略。降级到专业期刊并非必要，因为该工作的跨学科影响力恰恰适合Nature Communications。

## claude-sonnet

好，我把"外部审稿人"的身份放下，现在作为一个认真读完你全部材料的同行，直接跟你说说我的真实判断。

***

## Overall Recommendation

**Major Revision**——但是"大修"的核心问题不在于缺乏硬件数据，而在于**论文自己对自己诚实，但摘要和结论对读者不诚实**。这个裂缝不修好，任何审稿人都会抓住。

***

## Scores

- **Methodological Rigor: 3/5**
- **Scientific Contribution: 3.5/5**
- **NC Fit: 2.5/5**

***

## Critical Weaknesses (Top 3)

**1. 论文内部存在一个"诚实断层"——这是最致命的问题**

Section 6.5 里写得非常清楚：NL=2.0 的失败"反映的是本近似方法的极限，而不是材料本身的根本约束"。但摘要和结论却用"hard failure mode"和"hard boundary"来描述同一件事 。这不是笔误，这是两套话语体系：限制章节说的是"我的模型的边界"，摘要说的是"物理世界的边界"。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf)

对一个仔细的审稿人来说，这比没有硬件数据更危险，因为它让人怀疑作者是否有意用强语言抬高发现的显著性，然后在角注里撤退。NC编辑对这类写法有高度敏感性。修复成本很低：改两个短语，一致用"approximation-limit boundary"，并在摘要加一句"under the present gradient-scaling approximation"。

**2. Profile-driven interface 的贡献论证是循环的**

论文声称profile substitution是"核心贡献"，证据是：把Zhang 2025的参数填进JSON，跑出88.53%，说明这个接口能用 。但Zhang的σC2C和σD2D本身是从Vth spread和8次重复测量推算出来的"proxy estimate"，不是实测的全阵列噪声分布 。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf)

这等于说：我造了一把锁，用一把备用钥匙开开了，所以这把锁是好的。

审稿人会问：如果一个真实测量的设备数据（比如有重尾分布的D2D、空间相关噪声）被灌入这个interface，你的结论会变吗？`profile_auto_fitter_gpt.py` 这个工具在补充材料里提到了 ，但**它从未在论文中被实际使用和评估**——这是贡献论证最大的漏洞。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf)

**3. CIFAR-10/100 作为评估基准，对NC来说不够有力**

这不是方法问题，而是定位问题。NC的材料+系统交叉读者群期待看到接近真实部署场景的任务。CIFAR-10是1990年代的标准测试集，在2026年的NC投稿里用它作主要结果，会让来自材料科学背景的审稿人产生"这更像一篇会议论文"的直觉印象。Flowers-102的结果其实更有说服力（因为是小数据低功耗场景，贴近有机器件的真实应用定位），但它在论文里反而被弱化了，因为HAT在那里恢复效果差 。**把弱结果边缘化、强结果前置，这个选择本身就是一个信号。** [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf)

***

## Strengths

1. **Ensemble HAT 是真实的发现，不只是数据增强的变体**。标准HAT坍塌到10%这件事，本身就是一个在文献里从未被明确量化过的失败模式；resampling D2D mask 能恢复到86.37±1.54% 是有意义的系统级洞见 。这一个发现单独就足以支撑一篇期刊论文。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf)

2. **参数来源追溯矩阵（Table S2）是这篇论文方法论上最诚实的部分** 。每个参数都标明是"直接测量"、"proxy estimate"还是"canonical default"，这种程度的透明度在同类论文里很少见。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf)

3. **三种架构、三个数据集的覆盖广度**确实超出了该领域的现有文献基准。把小感知机换成Tiny-ViT这个动作本身就有贡献价值 。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf)

4. **Section 6.5 的局限性列举非常坦诚**，IR drop、sneak path、温度、光学串扰都有数量级的估计，这说明作者清楚自己在做什么 。问题是这份坦诚没有传导到摘要。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf)

***

## Specific Recommendations

**1. 你现在最需要做的不是加实验，而是修一个语言一致性问题。**

花两小时把全文中所有"hard boundary / hard failure mode / hard limit"替换为"approximation-limit boundary"或"simulator-scoped boundary"。同时在摘要的NL=2.0那句话后面加上括号注：*(under the present gradient-scaling approximation)*。这一个改动能消灭60%的审稿人攻击点。

**2. C2C不变性（Table S3-S4全行数值相同）必须给出机制解释。**

Scale-masking的解释在Section 5.2的正文里其实已经有了（σw ≈ 0.38 LSB，噪声落在同一量化桶里），但这个机制从未被显式地链接到Table S3-S4的标题或注脚。目前的呈现方式让这个表看起来像是copy-paste错误。加一行注脚，把5.2节的scale-masking解释指向这个表，问题解决。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/797775ae-f816-4d99-8fc5-5862413a0626/main.pdf)

**3. 把 `profile_auto_fitter_gpt.py` 的哪怕一个toy run放进supplementary，或者删除它作为"贡献"的描述。**

现在的状态是：在supplementary里提了这个工具 ，但没有任何实验展示它真的能把非Gaussian输入转化为有意义的JSON profile并改变结论。要么删除这一贡献点，要么加哪怕一个人工合成的"重尾D2D"输入，跑一次profile_auto_fitter然后展示accuracy shift。后者会把profile contribution从"架构主张"变成"经过验证的工具"。 [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/6722e84c-4dde-436c-b60a-45dc7e7af97c/supplementary_main.pdf)

**4. 关于是否联系 Vincze/Zhang 课题组：建议做，但不是为了数据，而是为了审稿人池的管理。**

发一封邮件说"我们使用了你们论文的参数，如有更新的全阵列噪声数据愿意引用"，有两个实际效果：第一，如果他们中有人是你的审稿人（可能性不小，NC会请原文作者），这封邮件会让他们对你的透明度产生好感；第二，就算他们提供了更好的数据，你也不需要重跑所有实验——只需要更新Table S2的provenance列，因为sensitivity sweep已经做了（Table S3-S4）。

***

## Final Verdict

**选择 (A)：现在投，作为纯simulation paper，但在点击提交之前完成上述第1和第2条修改。**

我不同意多模型共识里"pure simulation methodology paper = AIHWKIT model"这个类比。AIHWKIT的核心贡献是**把模拟器本身建起来**，而你的核心贡献是**用模拟器发现了一个不被文献承认的失败模式（fresh-instance collapse）并提出了解法（Ensemble HAT）**。这两件事在叙事重心上是不同的：你的论文更像是一篇发现性论文，simulator是工具，Ensemble HAT才是主角。

如果你按现在的写法投，审稿人会把篇幅花在"模拟器哪里不够好"上。如果你改变重心，把Ensemble HAT放在第一贡献位，把simulator作为使这个发现可重复的基础设施，审稿人的攻击方向会完全不同——他们会问"这个方法对其他架构有多普适"，这是一个你已经有部分答案的问题（ConvNeXt C4的proportional HAT结果）。

**一句话总结：论文的实质够投NC，但目前的框架在邀请错误类型的批评。改语言和改叙事重心，比做任何新实验都更值得投入时间。**

## deepseek-tenxun

总体建议

小修（Minor Revision）— 此建议是合理的，符合对一篇方法学贡献明确但尚未经物理硬件闭环验证的论文的常见审稿结果。

评分

• 方法学严谨性: 4/5 （评价维持）

• 科学贡献: 4/5 （评价维持）

• NC适合度: 4/5 （评价维持）

关键弱点（前3）— 评价的立足点

1.  我的评估严格基于文档：指出的三个弱点（无实测验证、模型简化、主张过度）均源自对main.pdf及supplementary_main.pdf的交叉验证。例如，supplementary_main.pdf的“Parameter Provenance”章节明确参数为文献代理或假设，main.pdf的“Limitations”章节详述了物理简化。
2.  弱点权重分配合理：“缺乏实测验证”被列为首席弱点，因其是贯穿全文的、由作者自身在“Limitations”章节承认的根本限制。这应是任何审稿人的核心关切点。
3.  未引入文档外的主观批评：所有指出的弱点均在文档中有据可查，未引入文档未提及的、新的物理效应或仿真缺陷进行苛责。

优势 — 评价的平衡性

1.  充分认可了文档中呈现的创新性：Profile接口、Ensemble HAT策略、系统化瓶颈分析等贡献，在文档中有详细实验（如三种子可复现性、Zhang 2025案例研究）支撑，值得高分肯定。
2.  优势与弱点形成有效制衡：正因优势显著（一个可运行的、透明的、能产生新见解的仿真框架），才使得在明确披露“纯仿真”定位的前提下，其价值足以在顶刊层面讨论，而非被“无硬件”一票否决。
3.  评估呼应了期刊定位：指出其适合Nature Communications的跨学科性，正是基于文档成功地将材料参数（有机器件特性）与系统结果（ViT任务精度）进行了量化桥接。

具体建议 — 评价的操作性

1.  建议旨在加固而非推翻论文逻辑：“明确声明纯仿真”、“软化硬边界表述”等建议，目的是让论文的核心定位（决策桥梁）和结论边界（近似极限）更清晰、更防御性，从而在审稿中更稳健。
2.  建议具有可执行性：所有修改建议均不要求作者返回实验室补充全新实验数据，而是在现有文本基础上进行表述调整和强调，符合“小修”的范畴。
3.  合作验证建议是策略性选项：提及“寻求合作验证”是一个可降低风险的可选强化动作，并非“重大修订”的强制要求，这为作者保留了决策灵活性。

最终裁决 — 评价的逻辑结论

我们应该：
• (A) 现在作为纯仿真论文投稿

理由：此裁决是前述评价的必然推论。
1.  文档证据足够强：论文展示了一个完整的方法学工作流（从Profile定义、HAT训练、到多任务评估和能量分析），并进行了深入的敏感性分析和对照实验（如补充材料中的大量表格）。其科学性体现在“如何系统化地评估”这一方法本身，而非某个器件的绝对性能。
2.  定位清晰且诚实：作者在cover_letter.pdf和main.pdf中已明确将框架定位为“first-order behavioral simulation”和“decision bridge”，旨在进行“deployment-facing risk assessment”。这是一种诚实的、有价值的研究范式。
3.  符合方法学论文的发表标准：在计算机体系结构、设计自动化等领域，提出一个具有新能力（如Profile驱动、有机器件聚焦）的仿真框架，并基于其得出新见解（Ensemble HAT），本身就是一个重要的贡献。要求所有仿真工具在首篇论文中必须附带自研硬件验证，并非通例（参考AIHWKIT、NeuroSim的早期论文）。
4.  “小修”是负责任的审稿意见：直接“接受”可能忽略了对表述严谨性的微调需求；“重大修订”（要求硬件）可能不必要地扼杀了一项及时的方法学贡献；“拒稿”则过于严苛，与论文呈现的质量不符。因此，“小修”是最平衡、最有利于领域发展的建议。

## gemini

Having read the full manuscript and supplementary materials, I can now provide a thorough, brutally honest external reviewer assessment.

***

## Overall Recommendation

**Major Revision** — with a clear path to acceptance if framing, disclosure, and several methodological gaps are addressed. The work is publishable in principle but currently makes claims that outrun its evidence in at least three places, and the simulation-only nature is not disclosed with sufficient prominence upfront.

***

## Scores

| Criterion | Score | Rationale |
|---|---|---|
| Methodological Rigor | **3/5** | Solid pipeline engineering, but proxy parameters, gradient-scaling NL approximation, and single-sanity-check validation are thin for NC standards |
| Scientific Contribution | **3.5/5** | Ensemble HAT insight is genuinely novel and actionable; "6-bit cliff" is useful framing but simulator-scoped; overall novelty is incremental over AIHWKIT/MemTorch |
| NC Fit | **3/5** | Interdisciplinary framing is appropriate; NC will want either a device collaborator or a much stronger simulation-methodology argument |

***

## Critical Weaknesses (Top 3)

### 1. The Validation Circularity Problem (Most Dangerous)
The AIHWKIT sanity check — 90.08±0.21% vs. 95.46% digital baseline — is presented as validation of your simulator, but it only demonstrates that both simulators degrade similarly under **one matched regime** (4-bit, uniform noise, CIFAR-10 ResNet-18). You explicitly acknowledge it "does not establish full physics equivalence for retention, photoresponse, or organic non-linear writing." This means the three phenomena that are actually **central claims** of the paper (retention dynamics, optical frontend, nonlinear write) have **zero cross-tool validation**. A Nature Communications reviewer in hardware or device physics will immediately notice this gap. The paper currently uses Vincze 2025 (an Early Access paper as of submission) for retention parameters and Zhang 2025 (also Early Access) for the OPECT case study  — both anchors are unvalidated against direct measurement. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=ETpoKwGWddoQCnIqAHYpdVLqH9Y%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

**What you can do:** Add an analytical bounding argument — show that even if retention τ₁, τ₂ are off by ±50%, the qualitative hierarchy of limits doesn't change. You partially do this for C2C/D2D (Table S3) but not for retention or NL.

### 2. The NL=2.0 "Hard Boundary" is a Gradient-Scaling Artifact, Not a Physics Claim
You explicitly state in Section 6.5: *"the observed failure boundary at NL=2.0 reflects the limit of this approximation rather than a fundamental materials constraint"*. Yet the abstract, conclusion, and cover letter repeatedly describe it as a "hard failure mode" and "hard boundary." This self-contradiction is a red flag — reviewers will cite Section 6.5 against your abstract. The 27.72±0.82% result is the limit of the **gradient-scaling approximation**, not of the organic material. A reviewer could legitimately argue: "This paper has found the limit of its own approximate method, not the limit of organic CIM." [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=64%2B61wdrCKIPGGO3BrWCRSTngcY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

**What you can do:** Rename throughout to "approximation-limit boundary" or "gradient-scaling failure regime." Add a paragraph explicitly quantifying what a higher-fidelity NL model (e.g., look-up table STE) would change.

### 3. Ensemble HAT: Novel Technique vs. Obvious Data Augmentation
The 10%→86.37% fresh-instance recovery is the paper's most striking quantitative result. However, the method — "resample D2D masks each epoch during training" — is structurally identical to **domain randomization** in sim-to-real transfer, **noise injection training** in quantization-aware training, and **augmentation-based robustness** in adversarial training literature. The paper does not cite or differentiate itself from these bodies of work. A reviewer who works in robust ML will immediately ask: "How is this different from standard noise augmentation?" Without a differentiation argument, this contribution risks being characterized as a straightforward application of a known technique to a new domain — publishable, but not at Nature Communications novelty level. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=64%2B61wdrCKIPGGO3BrWCRSTngcY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

**What you can do:** Add a paragraph in Related Work explicitly situating Ensemble HAT against (a) noise injection QAT, (b) domain randomization (Tobin et al. 2017), and (c) multi-device ensemble training in analog ML. Then articulate the specific organic-CIM reason why per-epoch D2D resampling is nontrivial — the fixed-mismatch structure of D2D vs. the i.i.d. structure of C2C is the key insight.

***

## Strengths

1. **Profile substitution interface is a genuine workflow contribution.** The JSON-based device profile schema + `profileautofittergpt.py` pipeline creates a reproducible path from literature characterization to deployment evaluation — this is not just a JSON wrapper; it's a standardized API that the community lacks for organic CIM. This deserves more prominent framing. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=ETpoKwGWddoQCnIqAHYpdVLqH9Y%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)
2. **Comprehensive non-ideality coverage in one stack.** Jointly modeling quantization + D2D/C2C + retention + nonlinear write + optical frontend + ADC precision in a single PyTorch-native stack, tested on three modern backbones, is a methodological step up from prior organic neuromorphic work, which stops at small perceptrons. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=64%2B61wdrCKIPGGO3BrWCRSTngcY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)
3. **Honest limitations section.** Section 6.5 is unusually candid about what the model cannot do (IR drop, temperature, optical crosstalk, NL approximation limit). This transparency is a strength, but it creates the framing tension described in Weakness #2.
4. **Monte Carlo rigor.** 10-run MC evaluation with locked three-seed V4 summary (Table S1: 87.64, 88.10, 88.11) and explicit confidence intervals provides statistical credibility that is rare in this subfield. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=ETpoKwGWddoQCnIqAHYpdVLqH9Y%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)
5. **Sensitivity analysis is actually quite strong.** The 2D C2C/D2D sweep (Table S3) showing stability down to 84.59% even at D2D=15% is genuinely reassuring for the Zhang case study. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=ETpoKwGWddoQCnIqAHYpdVLqH9Y%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

***

## Specific Recommendations

### On Abstract/Disclosure
1. **Yes, add "simulation-only" to the abstract explicitly.** Current abstract says "We present a profile-driven, behavioral simulation framework" — this is disclosed but buried in technical language. Add one sentence: *"All experiments are conducted at the simulation level using literature-derived device parameters; physical hardware validation remains future work."* This preempts reviewer #1's first question and shows confidence rather than defensiveness. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/c6f46d00-4914-4308-911f-6911d1485bf9/cover_letter.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=%2BBlaGnF3VdSBi0xgLMpC89nibQI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

### On the NL=2.0 Framing
2. **Soften throughout.** Change every instance of "hard boundary" and "hard failure mode" to "approximation-limit boundary (NL=2.0)" or "failure regime of the gradient-scaling surrogate." This is more scientifically precise and more defensible. Also add: "A look-up-table STE or SPICE-level NL model may shift this boundary; quantifying that shift is future work."

### On Ensemble HAT Novelty
3. **Add a 3-paragraph Related Work subsection** explicitly covering noise-injection QAT, domain randomization, and multi-device analog training. The differentiation argument should focus on the **structured spatial correlation** of D2D (fixed per-device, spatially correlated within array) versus i.i.d. noise augmentation — this distinction is the scientifically non-obvious part.

### On the Validation Gap
4. **Add a "Parameter Sensitivity Bounding" subsection** to the supplementary that extends the C2C/D2D sweep to retention parameters (±50% on τ₁, τ₂) and to the conductance window (Gmax/Gmin ±30%). Show that the qualitative hierarchy of limits — ADC cliff > fresh-instance transfer > NL > C2C/D2D — is robust to these parameter uncertainties. This does not require measured hardware; it requires three additional simulation sweeps you can run now.

### On Collaborative Validation
5. **Option (B) — seeking collaborative validation — is strategically optimal but not prerequisite.** Contact the Zhang 2025 (Liu et al., Nat. Commun.) group specifically: they are at a Chinese institution, the paper is already published, and reaching out to test even 1–2 data points through your profile interface would transform the Zhang case study from "proxy-backed" to "collaboratively spot-checked." This is a 4–6 week delay that could change a Major Revision to a Minor Revision, or prevent a Reject from a particularly hardware-focused reviewer.

### On Venue Choice
6. **Do not downscope preemptively.** The interdisciplinary framing (materials + ML systems) is genuinely NC-appropriate. The risk is a single device-physics reviewer who demands measured data — but that risk exists at Advanced Intelligent Systems too. NC's broader readership actually makes the methodology story *more* compelling, not less. The cover letter's "Why Nature Communications?" section is well-argued. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/c6f46d00-4914-4308-911f-6911d1485bf9/cover_letter.pdf?AWSAccessKeyId=ASIA2F3EMEYEQPJSVHES&Signature=%2BBlaGnF3VdSBi0xgLMpC89nibQI%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEH4aCXVzLWVhc3QtMSJIMEYCIQCCpLXWxVjqX%2BQEv%2FjVPQaqJ2nFhLyoS0zgvWQL2WWxuwIhAKuJHNvw8QugC0FQUn1QXrmywENyzylvltigxiASaOyQKvMECEcQARoMNjk5NzUzMzA5NzA1IgxgjJ83FsHpnWkaFvMq0AQgjGCr%2FLyPFqjk8VZ21RBTYPhOHGw544qHVUvAMPjpjGvfLtd3DFmugDMk7ZAdQNtQo5nutKD0vFj4%2FSZpHv7838OCeevaZ3D6flWGdWRhSyEiVy%2Bq9xjshYe0wsYIlwhq%2FGyaxiVcaFrmj%2Birp2FS7Un3nU9R%2B0%2FTDiNnoAzvfc7gTdZJtte4SFgMyiMheVYOogV5LaOMZ6YWrdQwyBdQIA7uch8A6QY9QLzESlUMimo7nN21URIvech0HbS6MkLqdk0QxF9qXB4TXfT655tP2dMeTle%2FPIC4afotueofTGXI9Qeet6sMJelZgmPqRPs1QHoxii67XplGPCmJVGgtmCvwLx9yOEVzmaFb%2Bs1yRaC%2F8dBNeMORiGUs9CzNuNVOqBwHnioAnPPt2PcYWDhkQMxXG320wH45MFiL1qoTTNbQ3Ar5%2B2Ew%2FzbIIqWt%2BwedjdN2hBWGm1YZOhkYGLjqe52amkfCMXM7Zhst7qT%2Bv8awdmylgcX8jHSFVODOZxCT6WzfIqwUHy6ZY4vevnLEBlD3xLoCggpk%2FDk%2B75XnfdtnkwEJcV3WIqZRTKcHN31b81moFz5Ven2a7rcwCWo8JEBdCRPmcYmgdqemATC0xrOExte6OtjWHIexh35WviwFcSoG5v8%2FIJdfkls8psjrlptSWl1KePpAaLhESZV9mXm%2BL9svipuz4I%2BJe46cr9vgq6BGRX1rAdoSlJQwa0W49eKLHnC4E1koC%2B1rykOl6gPNbx3c83IPeE4rzIcNxhlFwRErmTSDdYvXb%2BOzVX%2BaML%2Bf6c4GOpcBkiDfaECCqMQeZszCzzXwkZMAGJCYuMDHCFH5nPCofH2Yyt2GZde692gJ4P4Sjfd5FNRe%2BefSoqI2XNXt8fzDMjToqLyiiMa3le4OPS%2BqVuamxPfbFgiDDHj6Ga27MhxImK1KyB0FeJ45wSVtPRBVMOd5DnOAz7sNZydCLPvSZ9sX61TLS12JWdKL1z4JoNcJ3J2MdCkUEA%3D%3D&Expires=1775916970)

***

## Final Verdict

**Should you:**
**(A) Submit now as pure simulation — with targeted revisions**

The four changes that must happen before submission:
1. Add explicit "simulation-only" sentence to abstract
2. Rename NL=2.0 framing to "approximation-limit boundary" throughout
3. Add Ensemble HAT vs. domain randomization/noise-injection differentiation in Related Work
4. Add retention + conductance-window parameter sensitivity sweeps to Supplementary

These changes take approximately **5–7 days** and require no new experiments — just additional sensitivity sweeps and rewriting. The scientific substance is already there.

**(B) Seek collaborative validation** is the higher-EV play if you can afford a 4–6 week delay. Even a single correspondence with the Zhang/Liu group that yields 3–4 measured conductance points run through your profile fitter would materially strengthen the paper's position.

**(C) Downscoping is unnecessary** and would sacrifice the interdisciplinary impact the framework genuinely merits.

The most likely reviewer outcome without revisions: **two out of three reviewers accept the simulation-methodology framing; one device-physics reviewer requests measured validation as a condition of acceptance.** With the suggested revisions, the probability of a clean Major Revision (rather than Reject with encouragement) improves substantially. The paper has a real scientific contribution — the execution just needs to match the framing precision that Nature Communications expects.

## gpt

Having read both the main manuscript and supplementary materials thoroughly, here is my brutally honest external reviewer assessment:

***

## Overall Recommendation
**Major Revision** — with a realistic path to acceptance at a specialized venue, but significant reframing required before NC submission.

## Scores
- **Methodological Rigor**: 3/5
- **Scientific Contribution**: 3.5/5
- **NC Fit**: 2.5/5

***

## Critical Weaknesses (Top 3)

### 1. The Validation Loop Is Fundamentally Incomplete
This is the most serious issue that reviewers at Nature Communications will immediately flag. The AIHWKIT "sanity check" (90.08±0.21% vs. digital 95.46%) is described in Supplementary Section 1.9 as a "bounded shared-regime sanity check" — not a calibration, not a cross-validation, and not a physics equivalence test. The manuscript itself explicitly states: "all device parameters are literature-derived or proxy-calibrated rather than extracted from fabricated devices under direct measurement". This is not a disclosure that patches the problem; it IS the problem. For a venue like NC, which routinely publishes papers with fabricated organic transistor arrays (the Vincze and Zhang papers you cite both have measured data), a reviewer from the materials community will ask: *if the framework's parameters are proxies derived from these papers, what does the simulation tell us that reading those papers doesn't already tell us?* The framework's entire value proposition rests on the claim that it can predict deployment behavior — but that claim is untestable without at least one measured-vs.-simulated comparison on a real device. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf)

### 2. The "Profile-Driven" Contribution Is Architecturally Thin
The profile interface is presented as a core contribution — "seamless substitution of technology-specific parameters into the simulation pipeline" via JSON. In reality, this is a parameterized behavioral model with a configuration file. MemTorch, AIHWKIT, and CrossSim all support parameter injection; the differentiation claimed here is "organic-specific features" and "profile substitution," but the supplementary makes clear that the Zhang 2025 case study reuses canonical σ values because measured pulse-level NL data was unavailable. This means the most important organic-specific parameters (NL LTP, NL LTD) *could not actually be fitted* from the literature profile. A reviewer familiar with AIHWKIT's `RPUConfig` or CrossSim's device models will question whether the JSON wrapper constitutes a genuine architectural contribution vs. a software engineering convenience. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf)

### 3. The "6-Bit ADC Cliff" Is a Simulator Artifact, Not a Physical Discovery
The ADC sweep revealing a "transition near 6 bits" where accuracy jumps from ~27% at 4-bit to >80% at 6-bit is presented as an actionable insight for hardware designers. But this result is entirely a consequence of your noise parameterization (σD2D=10%, σC2C=5%) and the 4-bit weight quantization. Change those parameters and the cliff moves. More importantly, the energy model uses "analytical placeholders" — Ecell=100 fJ, EADC,8b=25 fJ  — that are not calibrated to any organic device. Presenting a precision-energy trade-off curve based on placeholder costs as actionable hardware design guidance is methodologically problematic. A reviewer from the circuits community will ask: what fabricated organic CIM circuit do these numbers describe? [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf)

***

## Strengths

1. **Ensemble HAT is the paper's strongest and most novel contribution.** The discovery that standard HAT collapses to 10% on fresh D2D instances is a sharp, counterintuitive result with immediate practical implications. The 86.37±1.54% recovery via D2D resampling is cleanly demonstrated with 10-instance × 5-MC evaluation, and the three-seed reproducibility (87.95±0.27%) in Supplementary Table S1 is rigorous. This result alone could anchor a focused paper. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf)

2. **Transparency about limitations is genuinely above average.** The manuscript explicitly lists out-of-scope effects (IR drop, temperature, optical crosstalk), provides a parameter provenance tracking matrix (Table S2), and correctly frames NL=2.0 collapse as a limit of the approximation rather than a materials constraint. This level of disclosure is rare and commendable. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf)

3. **Cross-architecture + cross-dataset breadth.** Running ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M across CIFAR-10/100 and Flowers-102 provides genuine insight into how task complexity and architecture interact with analog non-idealities — particularly the Flowers-102 collapse that HAT cannot recover.

4. **Differential-pair asymmetry sensitivity analysis** (Table S6) is a useful and underappreciated result: the sharp collapse at 2–5% asymmetry provides a concrete layout design constraint. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/05528041-0871-413b-9bed-2f22711c25d8/supplementary_main.pdf)

***

## Specific Recommendations

### On Abstract Disclosure
Yes, state "simulation-only" explicitly in the abstract, in a single factual sentence. The current abstract says "maps literature-derived or measured device assumptions"  — the word "or" implies measurement parity that doesn't exist. Suggested language: *"All device parameters are derived from published characterization data; validation against fabricated arrays remains future work."* Putting this in the abstract is not a weakness; hiding it and having a reviewer discover it on page 4 is far more damaging. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf)

### On the NL=2.0 "Hard Boundary" Framing
**Yes, soften this immediately.** The manuscript already acknowledges in Section 6.5 that "the observed failure boundary at NL=2.0 reflects the limit of this approximation rather than a fundamental materials constraint"  — but then the abstract and conclusion use the language "hard failure mode" and "hard boundary" without this qualification. This is internally inconsistent and will trigger reviewer criticism. Replace "hard failure mode" with "approximation-limited failure mode" or "boundary of the gradient-scaling approximation" throughout. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/158931923/d0649c4d-dce8-4edc-903b-e1e4bcd9d3aa/main.pdf)

### On Collaborative Validation (the Vincze/Zhang Question)
**This is the decision that will determine your venue.** Here is a frank assessment:

| Path | Realistic Timeline | Outcome at NC |
|------|-------------------|---------------|
| Submit now as pure simulation | Immediate | Likely desk reject or harsh Major Revision from materials reviewers |
| Contact Zhang group (NC 2025) for raw pulse data | 4–8 weeks | One fitted NL profile would transform claim 2 into real evidence |
| Contact Vincze group for retention data fit | 4–8 weeks | Same; anchors your canonical profile legitimately |
| Downscope to *Advanced Intelligent Systems* or *npj Computational Materials* | Immediate | Significantly higher acceptance probability as a methods paper |

The internal multi-model consensus to "submit without waiting" is correct for venue strategy — but the correct venue is **not NC**. NC's interdisciplinary scope cuts both ways: it attracts both ML-systems and materials reviewers, and the latter group will demand physical grounding.

***

## Final Verdict

**Recommendation (C) with elements of (A):** Downscope to a more appropriate venue while preserving the simulation-methodology framing.

The strongest version of this paper has a clear identity: *it is an Ensemble HAT paper* that happens to be demonstrated on an organic CIM simulator. The fresh-instance collapse + D2D-resampling recovery is the finding. Everything else — profile substitution, ADC sweep, energy model — is supporting infrastructure.

**Suggested target venues in order of fit:**
1. **npj Computational Materials** — explicitly welcomes simulation methods with materials grounding; lower hardware-validation bar than NC
2. **Advanced Intelligent Systems** (Wiley) — directly in scope for AI hardware methodology; materials reviewers less dominant
3. **IEEE Transactions on Electron Devices** (special section on neuromorphic) — if you add even one measured device comparison
4. **Nature Communications** — only viable after a collaborative validation dataset is added (even 1 device, 3 parameters measured)

If you are committed to NC specifically, the minimum credible path is: obtain raw pulse-program curves from one organic device (even a non-OPECT device), fit your NL/σ parameters from those curves, and show that the simulator reproduces the measured write-accuracy degradation within ±5 pp. That single experiment converts this from "simulation study" to "validated simulation framework" — a categorically different paper.