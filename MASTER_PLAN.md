# MASTER PLAN — Organic Optoelectronic CIM Simulation Framework

> **Authority**: This is the highest-priority document in the project.
> **Owner**: Claude (Architect, historical) / Codex (current active coordinator).
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
| F16 | **Zhang 2025 OPECT bridge** | V4_Ensemble=88.53% | §5.11 |
| F17 | Proportional HAT distribution-matched only | no uniform transfer | §5.9 |
| F18 | CNN more robust under richer physics | C4_prop=84.75±0.72% (3-seed) | §5.9 |

---

## Task Registry — 37/37 COMPLETE

All originally planned experimental tasks are complete. As of `2026-04-12`,
the project is no longer treated as a pure submission-closeout sprint.
Instead, it has moved into a **multi-track strategy phase** that balances
venue diversification, selective high-ROI supplementary experiments, and
measured-data readiness.

### Current Strategic Phase (2026-04-12)

| Track | Scope | Owner | Status |
|:--|:--|:--:|:--:|
| T-STRAT-1 | Strategy reset + source-of-truth sync (`MASTER_PLAN`, `CLAUDE_TASK`, `AGENT_SYNC`) | Codex | ✅ |
| T-STRAT-2 | Reviewer-facing manuscript hardening and selective patch integration | Codex | 🔄 |
| T-STRAT-3 | Venue diversification and rebuttal/positioning support | Kimi | 🔄 |
| T-STRAT-4 | Supplementary-experiment prioritization and insertion planning | Gemini | 🔄 |
| T-STRAT-5 | Measured-data readiness (doctor request, profile ingest, manuscript insertion map) | Kimi + Gemini | 🔄 |
| T-STRAT-6 | High-ROI supplementary experiment slate (design first, execution optional) | Gemini + Codex review | 🔄 |
| T-STRAT-7 | Long-horizon project value track (toolchain, case-study strengthening, measured calibration path) | Codex + sidecars | 🔄 |

---

## External Review Status

**Trend**: `Major Revision` → `Submission-ready` baseline established, but the project is now intentionally operating in a **multi-track / not-rushed** mode rather than forcing immediate submission.

Current tracker summary after folding in the 2026-04-10 reviewer batch:
- **109** reviewer issues tracked
- **106** completed
- **0** partially addressed
- **3** low-priority / acknowledged-as-scope-boundary items

### 2026-04-12 Delegation-First Mode

To preserve Codex quota for final verification and manuscript integration, the
project is now running in **delegation-first closeout mode**:

- **Kimi** owns the high-quota `submission / release / source-data / rebuttal`
  lane via `KX19–KX40`
- **Gemini** owns the high-quota `main-text / caption / bibliography /
  wording / NC-density` lane via `GM-X1–GM-X23`
- **Codex** only accepts, patches, compiles, and updates source-of-truth docs

The shift was driven by: Ensemble HAT, the Zhang 2025 OPECT case study,
AIHWKIT shared-regime validation, energy-bound qualification, and the expanded
limitations / reproducibility disclosures.

### 2026-04-11 External-Review Hardening Layer

After reading `report_md/审稿意见model_0411.md`, the active closeout strategy is:

- **submit now as a simulation-first NC paper**
- **do not reopen GPU-heavy experiments**
- **fix reviewer-facing language consistency**
- **promote Ensemble HAT to the lead contribution**
- **treat the simulator/profile stack as enabling infrastructure**
- **soften NL=2.0 from physical-sounding boundary to approximation-limited boundary**

Canonical broadcast:

- `report_md/_gpt/REVIEW_0411_ACCEPTANCE_AND_DISPATCH_gpt.md`

### 2026-04-12 External-Review Hardening Layer

After reading `report_md/审稿意见0412.md`, the active closeout strategy is further refined as:

- keep the paper on a **simulation-first methodology** track
- do **not** reopen GPU-heavy experiments
- further front-load simulation-only / behavioral-simulation disclosure
- soften any residual NL=2.0 language into an **approximation-boundary** statement
- reframe AIHWKIT as a **methodological consistency check** rather than physical validation
- promote the **6-bit ADC cliff** as a leading system conclusion
- reframe the simulator contribution around **organic-specific joint modeling**, not a generic profile interface
- use `favorable-stochastic-basin sensitivity` as an additional argument for organic-specific deployment risk

Canonical broadcast:

- `report_md/_gpt/REVIEW_0412_ACCEPTANCE_AND_DISPATCH_gpt.md`

### 2026-04-12 Strategic Reset

User direction now supersedes the earlier "NC-first immediate closeout" bias:

- **do not lock the project to NC only**
- **allow selective new experiments if GPU ROI is high**
- **do not rush submission while self-owned measured data is still pending**
- **treat the project as a long-horizon platform effort, not just a near-term paper sprint**
- **Codex remains review/coordination-first; Kimi and Gemini carry the heavy planning workload**

Canonical broadcast:

- `report_md/_gpt/STRATEGY_RESET_20260412_gpt.md`

### 2026-04-13 GPU-First Long-Horizon Rule

User direction is now further clarified:

- **GPU should not sit idle if there is high-ROI scientific work available**
- GPU time should serve **three simultaneous goals**:
  - strengthen the current manuscript when payoff is high
  - improve realism / measured-data readiness / open-source value
  - generate exploratory assets for a second paper
- do **not** optimize GPU only for near-term rebuttal
- do **not** spend GPU on broad unfocused reruns with no manuscript or platform value

Canonical broadcast:

- `report_md/_gpt/GPU_CONTINUOUS_QUEUE_20260413_gpt.md`

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
| ✅ | Bridge case study | §5.11 Zhang 2025 OPECT (88.53%) |
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
| G1 | 06_discussion.tex 第59行文本重复碎片 | 🔴 | ✅ Gemini 修复 |
| G2 | §6.6 缺少光电非均匀性/光写入串扰声明 | 🔴 | ✅ Gemini(.tex) + Claude(.md) |
| G3 | S4 敏感性数据真实重跑 | 🔴🔴 | ✅ GPU 19min, 日志已存 |
| G4 | Flowers-102 "hypothesis, not proof" 措辞 | 🟡 | ✅ Gemini 修复 |
| G5 | 05_results.tex enumerate 格式 | 🟡 | ✅ 可接受 |
| G6 | SYNC-2: 05_results.md Ensemble HAT 成本 | 🟡 | ✅ Claude 补修 |

### 不在原始 scope → 现升级为正式任务（"完美交付"）

| # | 任务 | 目的 | Owner | 预计时间 | Status |
|:--:|:--|:--|:--:|:--:|:--:|
| FW-1 | 多种子重训 (V1/V4/C1/C4 × CIFAR-10, 3 seeds) | 可复现性证据 | **Codex** | ~8h GPU | ✅ 已锁定到主文/补充材料 |
| FW-2 | State-dependent retention canonical 实验 | 完善物理覆盖 | Gemini | ~1h GPU | ✅ 数据与文字均已同步 |
| FW-3 | Raw measurement → profile 自动拟合工具 | 框架实用性 | **Codex** | ~2h 代码 | ✅ round-trip 质量已达可用阈值并写入 Appendix |
| FW-4 | Conductance INL lookup table | 完善物理层 | Gemini | ~1h 代码 | ✅ 73 tests pass |
| FW-5 | V8 retention-aware retraining | 修正后代码下验证 | **Codex** | ~4h GPU | ✅ 已完成并锁定 `89.67 ± 0.08%` |
| FW-6 | Git init + full commit | 版本管理 | 用户/Claude | 30min | ❌ |
| FW-7 | CITATION_BACKLOG 完全清理 | 引用规范化 | Gemini | 1h | ✅ |
| FW-8 | AIHWKIT 对照实验（至少设计方案） | reviewer 要求 | Gemini | 视情况 | ✅ 方案 + full benchmark 已闭环 |
| FW-9 | 全文最终 proofread | 投稿级质量 | **Codex** | 2h | ✅ PROOFREAD_LOG 已补 |

---

## LaTeX 移植状态

| Section | .tex file | Status |
|:--|:--|:--:|
| §00 Abstract | `00_abstract.tex` | ✅ synced |
| §01 Introduction | `01_introduction.tex` | ✅ synced |
| §02 Related Work | `02_related_work.tex` | ✅ synced |
| §03 Methodology | `03_methodology.tex` | ✅ synced |
| §04 Experimental Setup | `04_experimental_setup.tex` | ✅ synced |
| §05 Results | `05_results.tex` | ✅ synced (G5 修复) |
| §06 Discussion | `06_discussion.tex` | ✅ synced (G1/G2 修复) |
| §07 Conclusion | `07_conclusion.tex` | ✅ synced |
| §08 Appendix | `08_appendix.tex` | ✅ synced (G3 真实数据) |
| Figures | `latex_gpt/figures/` | ✅ populated（含 Fig.1/Fig.2） |
| Bibliography | `refs_gpt.bib` | ✅ clean |

---

## 完美交付任务分配 (2026-04-08 更新)

### 紧急修复 (今天)

| # | 任务 | Owner | Status |
|:--:|:--|:--:|:--:|
| FIX-1 | 06_discussion.tex 第59行删除重复文本 | **Gemini** | ✅ |
| FIX-2 | §6.6 添加光电非均匀性/光写入串扰限制声明 | **Gemini+Claude** | ✅ |
| FIX-3 | S4 敏感性扫描真实 GPU 重跑 | **Gemini** | ✅ |
| FIX-4 | Flowers-102 加 "hypothesis, not proof" 显式限定 | **Gemini** | ✅ |
| FIX-5 | 05_results.tex enumerate 格式统一 | **Gemini** | ✅ |

### Gemini 完成状态（已下线）

| Phase | # | 任务 | Status |
|:--:|:--:|:--|:--:|
| ~~修复~~ | 1 | FIX-1/2/3/4/5 + SYNC-1/2/3 | ✅ |
| 代码 | 2 | FW-3: Auto-fitting 工具 | ✅ round-trip 已过线并写入 Appendix |
| 代码 | 3 | FW-4: INL lookup table | ✅ 73 tests |
| 文字 | 4 | FW-7: CITATION_BACKLOG | ✅ |
| GPU | 5 | FW-1: 多种子重训 | ✅ 已锁定三种子结果 |
| GPU | 6 | FW-2: Retention 对比 | ✅ 已同步到主文/补充 |
| GPU | 7 | FW-5: V8 Retraining | ✅ 已锁定 `89.67 ± 0.08%` |
| 设计 | 8 | FW-8: AIHWKIT 方案 | ✅ |
| 文字 | 9 | FW-9: Proofread | ✅ `PROOFREAD_LOG_20260408_gpt.md` |

### Codex 接力任务（归档 + 当前）

| # | 任务 | 类型 | Status |
|:--:|:--|:--:|:--:|
| P1 | FW-1: 修 `--seed` + 重跑 12 个训练 | GPU ~8h | ✅ 已闭环 |
| P2 | FW-5: V8 继续/重跑到 50 epochs | GPU ~4h | ✅ 已闭环 |
| P3 | FW-2: Retention 对比 `.tex` 同步 | 文字 5min | ✅ Codex |
| P4 | FW-3: Auto-fitter 修 demo（误差<2%） | 代码 1h | ✅ Codex |
| P5 | FW-9: 真正做一遍 proofread | 文字 2h | ✅ Codex |
| **P6** | **Fig.1 系统架构图（脚本生成矢量图）** | 代码+图 | ✅ Codex |
| **P7** | **Fig.2 权重映射流程图（脚本生成矢量图）** | 代码+图 | ✅ Codex |
| **P8** | **README.md（开源门面）** | 文字 | ✅ Codex |
| **P9** | **防御性代码（参数验证）** | 代码 | ✅ Codex |
| **P10** | **Git init + .gitignore + RELEASE_CHECKLIST** | 运维 | ✅ Codex（repo 已存在 `.git`） |
| **P11** | **关键文档归档（docs/ 目录）** | 文字 | ✅ Codex |
| **P12** | **NC 级细节打磨（DPI/字体/颜色/caption）** | 审核 | 🔄 当前主线 |

### 2026-04-09 跨模型审稿共识优先级覆盖说明

> 来源：`report_md/审稿人意见from_model.md`  
> 结论：`Major Revision`（7/8），但总体态度积极，修后可接收。

这份共识**不推翻**当前 `FW-* / P*` 状态表，但会改变后续优先级解释：

1. `FW-1` 多种子重训继续保持最高正在执行优先级  
   - 这是 reviewer 共识中的 `C2` 直接修复
2. **新增 reviewer-driven 最高优先级任务：AIHWKIT shared-regime 对比实验**
   - 当前 `FW-8` 仅完成方案/讨论，不等于实验已闭环
   - 因此新增实际执行任务：
     - `FW-10`: AIHWKIT shared-regime benchmark（至少 ResNet-18）
3. **新增 reviewer-driven 高优先级任务：Flowers-102 noise-magnitude ablation**
   - 目标是给 `data-floor hypothesis` 至少一个最小受控验证
4. `FW-5` V8 retraining 相对降级
   - 不再先于 `FW-10 / Flowers ablation`

| # | 任务 | 目的 | Owner | 预计时间 | Status |
|:--:|:--|:--|:--:|:--:|:--:|
| FW-10 | AIHWKIT shared-regime 对比实验（至少 ResNet-18） | 回应 reviewer 共识 C1 | **Codex** | ~2-3d GPU | ✅ Full CIFAR-10 result locked (`95.46%` digital / `90.08 ± 0.21%` AIHWKIT) |
| FW-11 | Flowers-102 noise-magnitude ablation | 回应 reviewer 共识 C5 | **Codex** | ~1d GPU | ✅ 已用 zero-noise hybrid control 与文本限定闭环 |

其余 reviewer 共识高优先级非 GPU 修补：
- `C3`：`11.45x` wording 继续 upper-bound 化
- `C4`：placeholder citations 清理
- `C6`：attention 图定量指标已部分修复（entropy）
- `C10`：Ensemble HAT training-cost 段落
- `C14`：前端图号错引修复

### 用户

| # | 任务 | 优先级 |
|:--:|:--|:--:|
| 1 | ~~Fig.1/Fig.2 手绘~~ → 改为脚本生成（P6/P7） | ✅ 转交 |
| 2 | 选定投稿期刊 → **Nature Communications** | ✅ 已确认 |
| 3 | 真实作者信息（camera-ready 阶段替换） | 🟡 |
| 4 | ~~确认开源 License~~ → **Apache 2.0** | ✅ 已确认 |

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

*Last updated: 2026-04-08 19:00 by Claude (Architect — Apache 2.0 确认 + Codex P3/P4 审核通过 + P6-P12 下发)*
*This document supersedes all task lists in AGENT_SYNC_gpt.md for priority decisions.*

---

## 2026-04-13 Codex Strategic Addendum

### Current truth override

- The project is **not locked to NC**.
- Current strategy is **multi-venue + GPU-continuous + measured-data-ready**.
- GPU time should serve three goals in parallel:
  1. current-paper strengthening,
  2. framework realism / measured-data readiness / open-source growth,
  3. second-paper discovery.

### Role split while Gemini validates

- **Gemini**
  - GPU / exploratory validation line
  - current active exploratory direction: Tiny-ImageNet / ImageNet-scale bridge
- **Kimi**
  - non-GPU defense / venue / measured-data communication / artifact-destination line
- **Codex**
  - review / merge gatekeeper
  - patch / compile / truth-board sync
  - final decision on whether new artifacts go to:
    - main manuscript
    - supplementary
    - revision-only evidence
    - second-paper backlog

### Immediate non-GPU tasks (active)

- Codex:
  - `CX-C17` sync stale `MASTER_PLAN.md` language to current multi-venue truth
  - `CX-C18` produce artifact-destination ruling for GM-E1 / GM-E2 / retention / ImageNet exploratory outputs
  - `CX-C19` finalize doctor-facing measured-data request chain
  - `CX-C20` review Gemini ImageNet exploratory assets if/when they land
- Kimi:
  - `KX55` doctor-facing data ask compression
  - `KX56` GPU artifact destination defense memo
  - `KX57` multi-venue strategy memo v2
  - `KX58` minimal open-source + measured-data onboarding audit
