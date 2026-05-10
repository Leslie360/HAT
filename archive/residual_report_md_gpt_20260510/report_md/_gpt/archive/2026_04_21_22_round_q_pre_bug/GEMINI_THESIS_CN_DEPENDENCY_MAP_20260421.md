# GEMINI 中文 Thesis Dependency Map
**Date:** 2026-04-21
**Scope:** Phase α (G-HH3)

This map directs Kimi on which chapters of the Simplified Chinese (简体中文) PhD thesis can be written immediately, and which must wait for the resolution of the J1d/CX-K series ambiguity.

---

## 🟢 Safe to Write Now (Frozen Data / Number-Agnostic)
*These chapters do not depend on the outcome of the recent GPU diagnostics.*

- **第 1 章：引言 (Chapter 1)**
  - Depends on: General field context, `GEMINI_POSITIONING_V3_20260420.md`.
- **第 2 章：相关工作 (Chapter 2)**
  - Depends on: `KIMI_LIT_LANDSCAPE_20260420.md`.
- **第 3 章：方法论 (Chapter 3)**
  - Depends on: The core framework equations, noise models, and Ensemble HAT definitions (which are locked).
- **第 4 章：基准实验 (Chapter 4)**
  - Depends on: ResNet / ConvNeXt / Tiny-ViT V1-V6 baseline data, CrossSim comparison, which are **100% frozen** (`CANONICAL_RESULT_LOCK_gpt.md`).
- **第 7 章：部署包络 (Chapter 7)**
  - Depends on: ADC sweeps, noise contours, device profile transfers (literature/measured). All data is frozen.
- **第 8 章：展望 (Chapter 8)**
  - Depends on: `GEMINI_OPEN_PROBLEMS_20260420.md`. Pure forward-looking theory.

## 🟡 Proceed with Caution (Conditional Text Needed)
*These chapters can be scaffolded, but require `\if` blocks or placeholders for the final punchline.*

- **摘要 (Abstract)**
  - The core methodology summary is safe. The concluding sentence regarding the "structural limit" vs "bimodal basin" must be placeholder'd: `[此处填入基于 CX-K 最终确认的失效原因结论]`.
- **第 6 章：物理现实主义扩展 (Chapter 6)**
  - Depends on: Tier-2 experiments (CX-J2/J3/J4). These experiments have preliminary data but their *narrative framing* (whether they are the main contribution or just a defensive ablation) depends on the Branch A vs C outcome.

## 🔴 Wait for Loop Closure (Blocked)
*Do not write the prose for this chapter until Codex officially closes the CX-K queue.*

- **第 5 章：失效模式与非理想性诊断 (Chapter 5)**
  - This is the battlefield chapter. It hosts the J1b (QKV), J1c (Full-Attn), and J1d/K2-5 (Higher-Order) diagnostic results. It cannot be accurately drafted until the bimodal basin (Branch C) vs structural limit (Branch A) narrative is irrevocably decided by the final GPU JSONs.
