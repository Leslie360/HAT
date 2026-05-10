# 硕士论文 Work 2 方向调研计划

**Date:** 2026-04-23
**Owner:** Kimi (Moonshot) — literature & strategy
**Partner:** Codex (OpenAI) — technical feasibility review
**Scope:** Four candidate directions for Work 2 (Master's thesis second contribution)

## Direction A: Multi-Tile Organic CIM Array Mapping
**Agent:** Kimi-A (literature sweep)
**Key questions:**
- How do existing CIM simulators (NeuroSim, AIHWKIT, CrossSim) handle tiled arrays?
- What is the state-of-the-art in tile partitioning for ViT/Transformer inference?
- What communication models exist for analog-to-analog tile transfer?
- What is the break-even point (array size vs communication cost)?

## Direction B: Continual Learning on Organic CIM
**Agent:** Kimi-B (literature sweep)
**Key questions:**
- What is known about write-erase cycling in organic optoelectronic synapses?
- How does device noise affect catastrophic forgetting in analog neural networks?
- What CL algorithms (EWC, replay, regularization) have been tested on RRAM/CIM?
- Can Ensemble HAT be extended to incremental learning?

## Direction C: LLM KV-Cache Mapping to Organic CIM
**Agent:** Kimi-C (literature sweep)
**Key questions:**
- What is the current landscape of KV-cache compression/offloading?
- Has anyone mapped KV-cache to analog CIM arrays?
- What are the retention requirements for KV-cache (seconds vs minutes)?
- What model sizes are feasible (GPT-2, LLaMA-7B)?

## Direction D: Optical-Electronic Co-Design Frontend
**Agent:** Kimi-D (literature sweep)
**Key questions:**
- What photodiode/OLED response models are used in optoelectronic CIM literature?
- How does illumination intensity affect signal-to-noise ratio in organic arrays?
- What joint optimization frameworks exist (optical + electronic)?
- What are realistic deployment lighting conditions (indoor, outdoor, varying)?

## Deliverables
1. One-page summary per direction (motivation, SOTA, gap, feasibility, timeline)
2. Key citation list per direction (5-10 papers)
3. Kimi synthesis: ranked recommendation with rationale
4. Codex review: technical feasibility assessment for top-2 candidates
