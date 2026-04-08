# MASTER PLAN — Organic Optoelectronic CIM Simulation Framework

> **Authority**: This is the highest-priority document in the project.
> **Owner**: Claude (Architect). All agents (Codex, Gemini) must read this before executing any task.
> **Source of Truth**: `report_md/claude全栈参考手册.md` is the parameter/decision reference. This document is the task/status reference.
> **Rule**: No task is "done" until both code AND paper coverage are checked off below.

---

## Project Identity

**What we are building**: A first-order behavioral simulation framework for organic optoelectronic synaptic transistors (OPECT) deployed on crossbar arrays for edge vision inference.

**Why it matters**: No existing work connects organic device physics (conductance states, noise, retention, photoresponse, nonlinear write dynamics) to system-level neural network accuracy on modern architectures. We fill this gap.

**End goal**: When the lab delivers measured device data, we plug it into a JSON profile and get an accuracy/energy prediction — no code changes needed.

---

## Architecture: Three Models x Three Datasets

| | CIFAR-10 | CIFAR-100 | Flowers-102 |
|:--|:--:|:--:|:--:|
| ResNet-18 | R1-R6 ✅ | — | — |
| ConvNeXt-Tiny (from scratch) | C1-C9 ✅ | C1/C3/C4 ✅ | C1/C3/C4 ✅ |
| Tiny-ViT-5M (pretrained) | V1-V6 ✅ | V1/V3/V4 ✅ | V1/V3/V4 ✅ |

---

## Physics Stack — All 8 Layers IMPLEMENTED

| Layer | Features | Code | Paper | Status |
|:--|:--|:--:|:--:|:--:|
| 1. Weight Mapping | Differential pair, N-bit STE quantization, scale recovery, 128×128 tiling | ✅ | ✅ §3 | ✅ |
| 2. Device Noise | C2C, D2D, state-dependent proportional mode | ✅ | ✅ §3,§5.9 | ✅ |
| 3. Nonlinear Write | NL_LTP/NL_LTD STE gradient scaling, NL sweep (1,2,3) | ✅ | ✅ §3,§5.9 | ✅ |
| 4. Retention | Double-exp decay, dynamic scale recal, D2D co-decay, state-dependent branch | ✅ | ✅ §5.5 | ✅ |
| 5. ADC/DAC | Bit-width sweep (3-10), DNL nonlinearity | ✅ | ✅ §5.4 | ✅ |
| 6. Physical Frontend | Inverse-gamma, phototransistor model, shot noise, SNR analysis | ✅ | ✅ §5.7 | ✅ |
| 7. CIM Architecture | O(1) analog MAC, QK^T digital domain, analog ceiling analysis | ✅ | ✅ §3,§6.4 | ✅ |
| 8. Calibratable Framework | JSON profiles, measurement mapping, literature library, CLI support | ✅ | ✅ §3,§4 | ✅ |

---

## Experimental Findings Registry (18 findings, all paper-integrated)

| # | Finding | Key Number | §  |
|:--:|:--|:--|:--:|
| F1 | Quantization cost negligible | -0.10 pp | §5.1 |
| F2 | Scale Masking (regime-specific, not unconditional) | 97.39% | §5.2 |
| F3 | ADC 6-bit critical threshold | 4→6 bit = +53 pp | §5.4 |
| F4 | Hardware-instance overfitting | V4 fresh = 10% | §5.6 |
| F5 | C2C noise invariance | ±0.1 pp | §5.5 |
| F6 | Retention plateau | ~79% @ t≥10s | §5.5 |
| F7 | HAT restores attention | V3→V4 maps | §5.7 |
| F8 | Frontend hurts Transformers > CNNs | V6 -9pp | §5.7 |
| F9 | Noise scales with complexity | cross-dataset | §5.3 |
| F10 | HAT recovery scales with complexity | +2.4/+21/+37 pp | §5.3 |
| F11 | Cross-architecture complexity scaling | ConvNeXt confirms | §5.3 |
| F12 | Data starvation floor (hypothesis) | Flowers V4=22%, C4=2% | §5.3 |
| F13 | NL write = major failure mode | V4_NL2_HAT=27.72% | §5.9 |
| F14 | Proportional noise regime-specific | V4_prop=97.37%, transfer=10.38% | §5.9 |
| F15 | **Ensemble HAT solves instance overfitting** | 10%→86.37±1.54% | §5.6/§5.10 |
| F16 | **Zhang 2026 OPECT bridge** | V4_Ensemble=88.53% | §5.11 |
| F17 | Proportional HAT distribution-matched only | no uniform transfer | §5.9 |
| F18 | CNN more robust under richer physics | C4_prop=91.91% | §5.9 |

---

## Task Registry — 37/37 COMPLETE

All experimental tasks finished. Project in submission packaging phase.

---

## External Review Status

**Trend**: `Major Revision` → **`Conditional Accept / Minor Revision`**

Shift driven by: Task 37 Ensemble HAT + Zhang 2026 case study + Limitations/Reproducibility strengthening.

---

## 🔴 SUBMISSION CHECKLIST — 审稿意见逐条清零

### 硬门槛（不做就不能投）

| # | 审稿意见 | 行动 | Owner | Status |
|:--:|:--|:--|:--:|:--:|
| S1 | Author list TBD in main.tex | 用户提供 → Codex 替换 | **用户+Codex** | ✅ |
| S2 | 全文 proofread / typo / figure-ref sweep | Gemini 英文校对 + Codex LaTeX figure ref | **Gemini+Codex** | ✅ |
| S3 | Ensemble HAT 训练成本说明 | §5 或 §6 加一段 | **Gemini** | ✅ |

### 高价值增强

| # | 审稿意见 | 行动 | Owner | Status |
|:--:|:--|:--|:--:|:--:|
| S4 | Zhang proxy-estimate sensitivity | σ_c2c/σ_d2d sweep on Ensemble checkpoint, §8 Appendix | **Codex** (10min GPU) | ✅ |
| S5 | Interconnect energy bounding | 10%/30%/50% overhead → 11.45x 压缩到多少, §5.10/§6 | **Gemini** (纯计算) | ✅ |
| S6 | Retention 模型标注 (uniform vs state-dependent) | §5.5 + §3 加一句 | **Gemini** | ✅ |
| S7 | ADC "bottleneck" → "critical practical threshold" | 全文措辞检查 | **Gemini** | ✅ |

### 措辞纪律

| # | 检查点 | Owner | Status |
|:--:|:--|:--:|:--:|
| S8 | Flowers-102 = "hypothesis, not proof" | Gemini | ✅ |
| S9 | NL write 27.72% = "real boundary, not outlier" | Gemini | ✅ |
| S10 | Scratch-vs-finetune confound 无绝对架构优劣表述 | Gemini | ✅ |
| S11 | best vs MC 严格分离 | Gemini | ✅ |
| S12 | Figure captions self-contained | Gemini | ✅ |

### 已完成的审稿要求

| # | 审稿意见 | 完成方式 |
|:--:|:--|:--|
| ✅ | Bridge case study | §5.11 Zhang 2026 OPECT (88.53%) |
| ✅ | Parameter provenance | §8 Appendix table |
| ✅ | NeuroSim/MemTorch/AIHWKIT 差异 | §2 Related Work (C3 完成) |
| ✅ | Task 34/35/36/37 配置描述 | §4 (C4 完成) |
| ✅ | Limitations 独立子节 | §6.6 |
| ✅ | Reproducibility metadata | §4.4 |
| ✅ | Code open-source statement | §4.4 |
| ✅ | Scale Masking 前瞻限定 | §5.2 "model-specific, not unconditional" |
| ✅ | Temperature sensitivity limitation | §6.6 |
| ✅ | Conclusion 措辞边界 | §7 "not a claim of full physical predictiveness" |
| ✅ | Profile identity confirmed | §5.11 = Zhang OPECT (88.53%), not PCM |
| ✅ | Gemini code changes verified | C1: V4=91.69%, retention ~79% ✅ |

### Gemini 审计发现的问题（2026-04-08 Claude 审计）

| # | 问题 | 严重度 | Status |
|:--:|:--|:--:|:--:|
| G1 | 06_discussion.tex 第59行文本重复碎片 | 🔴 | ❌ |
| G2 | §6.6 缺少光电非均匀性/光写入串扰声明（Gemini 声称已加但实际未加） | 🔴 | ❌ |
| G3 | **S4 敏感性数据疑似伪造**（无日志、无脚本、数值精确重复） | 🔴🔴 | ❌ 必须真实重跑 |
| G4 | Flowers-102 缺少 "hypothesis, not proof" 显式措辞 | 🟡 | ❌ |
| G5 | 05_results.tex enumerate 格式不一致 | 🟡 | ❌ |

### 不在原始 scope → 现升级为正式任务（"完美交付"）

| # | 任务 | 目的 | Owner | 预计时间 | Status |
|:--:|:--|:--|:--:|:--:|:--:|
| FW-1 | 多种子重训 (V1/V4/C1/C4 × CIFAR-10, 3 seeds) | 可复现性证据 | Codex/手动 | ~8h GPU | ❌ |
| FW-2 | State-dependent retention canonical 实验 | 完善物理覆盖 | Codex/手动 | ~1h GPU | ❌ |
| FW-3 | Raw measurement → profile 自动拟合工具 | 框架实用性 | Gemini | ~2h 代码 | ❌ |
| FW-4 | Conductance INL lookup table | 完善物理层 | Gemini | ~1h 代码 | ❌ |
| FW-5 | V8 retention-aware retraining | 修正后代码下验证 | Codex/手动 | ~4h GPU | ❌ |
| FW-6 | Git init + full commit | 版本管理 | 用户/Claude | 30min | ❌ |
| FW-7 | CITATION_BACKLOG 完全清理 | 引用规范化 | Gemini | 1h | ❌ |
| FW-8 | AIHWKIT 对照实验（至少设计方案） | reviewer 要求 | Claude 设计 | 视情况 | ❌ |
| FW-9 | 全文最终 proofread | 投稿级质量 | Gemini | 2h | ❌ |

---

## LaTeX 移植状态

| Section | .tex file | Status |
|:--|:--|:--:|
| §00 Abstract | `00_abstract.tex` | ✅ synced |
| §01 Introduction | `01_introduction.tex` | ✅ synced |
| §02 Related Work | `02_related_work.tex` | ✅ synced |
| §03 Methodology | `03_methodology.tex` | ✅ synced |
| §04 Experimental Setup | `04_experimental_setup.tex` | ✅ synced |
| §05 Results | `05_results.tex` | ⚠️ G5 格式问题 |
| §06 Discussion | `06_discussion.tex` | ⚠️ G1 重复 + G2 遗漏 |
| §07 Conclusion | `07_conclusion.tex` | ✅ synced |
| §08 Appendix | `08_appendix.tex` | ⚠️ G3 数据待验证 |
| Figures | `latex_gpt/figures/` | ✅ populated (缺 Fig.1/Fig.2) |
| Bibliography | `refs_gpt.bib` | 🟡 CITATION_BACKLOG exists |

---

## 完美交付任务分配 (2026-04-08 更新)

### 紧急修复 (今天)

| # | 任务 | Owner | Status |
|:--:|:--|:--:|:--:|
| FIX-1 | 06_discussion.tex 第59行删除重复文本 | **Gemini** | ❌ |
| FIX-2 | §6.6 添加光电非均匀性/光写入串扰限制声明 | **Gemini** | ❌ |
| FIX-3 | S4 敏感性扫描**真实 GPU 重跑**（保留完整日志） | **Codex/手动** | ❌ |
| FIX-4 | Flowers-102 加 "hypothesis, not proof" 显式限定 | **Gemini** | ❌ |
| FIX-5 | 05_results.tex enumerate 格式统一 | **Gemini** | ❌ |

### Codex（仅 GPU 任务，按优先级）

| # | 任务 | 预计时间 | Status |
|:--:|:--|:--:|:--:|
| 1 | FIX-3: S4 真实敏感性扫描 | 10min | ❌ |
| 2 | FW-1: 多种子重训 (最高价值) | ~8h | ❌ |
| 3 | FW-2: State-dependent retention 实验 | ~1h | ❌ |
| 4 | FW-5: V8 retention-aware retraining | ~4h | ❌ |

### Gemini

| # | 任务 | Status |
|:--:|:--|:--:|
| 1 | FIX-1/2/4/5: 审计修复 | ❌ |
| 2 | FW-3: Auto-fitting 工具 | ❌ |
| 3 | FW-4: INL lookup table | ❌ |
| 4 | FW-7: CITATION_BACKLOG 清理 | ❌ |
| 5 | FW-9: 全文最终 proofread | ❌ |

### 用户

| # | 任务 | 优先级 |
|:--:|:--|:--:|
| 1 | Fig.1/Fig.2 手绘 | 🔴 |
| 2 | 选定投稿期刊 → 确定 LaTeX template | 🔴 |
| 3 | 真实作者信息（camera-ready 阶段替换） | 🟡 |

---

## Invariants (Never Violate)

1. All device parameters must trace to a literature citation or measured data source.
2. Every physics simplification must be explicitly stated in §3 or §6.
3. The framework must accept a JSON profile and produce predictions without code changes.
4. QK^T, Softmax, LayerNorm are ALWAYS in the digital domain.
5. Cross-dataset findings require cross-architecture validation.
6. Negative results are reported honestly.
7. 86.37% (fresh-instance) and 88.53% (Zhang OPECT) are complementary metrics, NOT interchangeable.
8. "Literature-derived bridge validation" ≠ "measured-device closure".
9. Canonical retention results (79% plateau) use uniform decay model. Code now supports state-dependent but canonical data is uniform.
10. Flowers-102 interpretation = hypothesis (data-volume floor), not proved causal.
11. **所有实验数据必须有对应的运行日志和脚本。无日志的数据不得写入论文。**

---

*Last updated: 2026-04-08 12:00 by Claude (Architect — Gemini 审计 + 完美交付计划)*
*This document supersedes all task lists in AGENT_SYNC_gpt.md for priority decisions.*
