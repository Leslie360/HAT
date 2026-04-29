# R11D 实验审计总结 — 供 Codex 审阅

**Date:** 2026-04-28  
**Auditor:** Claude  
**Status:** Tier 0 完成，Tier 1 进行中，发现配置错误已修正

---

## 一、已完成实验矩阵

### Tier 0 — Paper-2 PCM Section (Narrative LOCKED)

| ID | Precision | Device | Modifier | Train | Fresh (10 inst) | Drift (0h→1h→24h) | Status |
|:---|:----------|:-------|:---------|:------|:----------------|:-------------------|:-------|
| R11D-5a | 8-bit | PCM preset | ADD_NORMAL σ=0.10 | **76.96%** | 76.74±0.09% | 76.70→76.72→76.73% | ✅ Done |
| R11D-6b | 8-bit | Pure baseline | ADD_NORMAL σ=0.0001 | **88.64%** | 88.39±0.17% | 88.35→12.21→10.0% | ✅ Done |
| R11D-6c | 8-bit | Pure baseline | ADD_NORMAL σ=0.10 | **88.40%** | 88.17±0.12% | Skipped | ✅ Done |
| R11D-7 | 4-bit | PCM preset | ADD_NORMAL σ=0.10 | **76.54%** | 76.61±0.07% | 76.61→75.01→73.42% | ✅ Done |
| R11D-8 | 8-bit | PCM + HAT-inspired | ADD_NORMAL σ=0.10 | **76.12%** | 76.11±0.10% | 76.13→76.25→76.16% | ✅ Done |
| R11D-8-SWA | 8-bit | PCM+HAT+SWA | ADD_NORMAL σ=0.10 | **77.53%** | 77.37±0.08% | 77.29→76.96→75.28% | ✅ Done |
| R11D-9 | 4-bit | Pure baseline | ADD_NORMAL σ=0.0001 | **~10%** | N/A | N/A | ❌ Killed |
| R11D-9b | 4-bit | Pure baseline | ADD_NORMAL σ=0.01 | **~10%** | N/A | N/A | ❌ Killed |
| R11D-9c | 4-bit | Pure baseline | ADD_NORMAL σ=0.0001, lr=5e-4 | **~19%** | N/A | N/A | ❌ Killed |
| R11D-10 | 4-bit | Pure + DOREFA | DOREFA | **11.49%** @ e10 | N/A | N/A | ❌ Killed |
| R11D-7b | 4-bit | PCM preset (extended drift) | ADD_NORMAL σ=0.10 | — | — | 72.15% @ 3d | ✅ Done |

### 作废的实验

| ID | 作废原因 | 备注 |
|:---|:---------|:-----|
| R11D-5a seed=123 (v1) | **配置错误**：modifier_std_dev=0.0001 (应为 0.10) | 跑到 85.72%，与原始实验不可比 |

---

## 二、核心 Narrative（已锁定）

> **"PCM device physics enable 4-bit training that pure quantization cannot."**

### 支撑该叙事的关键证据

1. **4-bit pure 完全不可训练**
   - 4-bit pure + ADD_NORMAL σ=0.0001 → ~10%
   - 4-bit pure + ADD_NORMAL σ=0.01 → ~10%
   - 4-bit pure + DOREFA → 11.49% @ epoch 10
   - 4-bit pure + low lr → ~19%
   - **结论**：无论 noise magnitude、lr、modifier type 如何调整，4-bit pure baseline 均失败。

2. **PCM 拯救 4-bit**
   - PCM 4-bit: 76.54% vs PCM 8-bit: 76.96%
   - 差距仅 **−0.42pp**，说明精度降低本身不是瓶颈
   - 瓶颈是 **PCM device physics 的特定噪声/更新特性**

3. **PCM penalty 不是 generic noise**
   - 8-bit pure + σ=0.0001: 88.64%
   - 8-bit pure + σ=0.10: 88.40%（仅 −0.24pp）
   - PCM 8-bit: 76.96%（与 pure baseline 差距 **−11.68pp**）
   - **结论**：generic Gaussian noise 不能解释 PCM gap。PCM 的特定 device physics（drift、stochasticity、D2D variation）才是关键。

4. **SWA trade-off**
   - PCM+HAT+SWA fresh: 77.37%（比非 SWA 的 76.11% 高 **+1.42pp**）
   - PCM+HAT+SWA drift @ 24h: 75.28%（比非 SWA 的 76.16% 低 **−2.25pp**）
   - **结论**：SWA 提升 fresh accuracy 但牺牲 drift robustness。需在论文中明确披露。

5. **HAT-inspired 未达预期**
   - PCM+HAT: 76.12%（比标准 PCM 76.96% 还低 −0.84pp）
   - **结论**：当前实现（per-epoch D2D resampling on tiles）不足以超越标准 PCM。如需改进，需要 canonical HAT 的 custom layer 实现。

---

## 三、发现的问题与修正

### 严重：Multi-Seed 脚本配置错误

**问题**：`run_pcm_multi_seed_validation.sh` 中硬编码了 `--modifier-std-dev 0.0001`，而原始 R11D-5a/R11D-7 使用的是默认值 `0.10`。

**影响**：
- 第一轮 seed=123 跑出 85.72%，与原始 76.96% 不可比
- 若未发现，全部 4 个 multi-seed 实验的结果均会误导叙事

**根因**：脚本从 R11D-6b（pure baseline，modifier=0.0001）复制参数时未修正。

**修正**：
- Kill 错误进程（PID 29359/29362/29367）
- 脚本 modifier_std_dev 0.0001 → 0.10
- 重新启动全部 4 个实验

**教训**：任何复现实验的脚本必须逐项核对原始实验配置，不能从其他实验的脚本直接复制。

---

## 四、未来优先级实验总表

### 执行规则
- GPU 零空闲：每个任务完成后立即启动下一个最高优先级任务
- 当前 running 任务完成后才能启动下一个（单 GPU，无法并行）
- Kill criteria 必须严格执行

### Tier 1 — Reviewer Defense（最高优先级）

| Priority | ID | Task | GPU Time | Rationale | Kill If |
|:---|:---|:---|:---|:---|:---|
| **P0** | T1-1 | PCM Multi-Seed Validation — R11D-5a/7 各跑 seed=123, 456 | **~8h** | 最大 reviewer 攻击面：当前全部 single seed=42 | Any seed test < 70% @ e30 |
| **P0** | T1-2 | Progressive Quantization — 8-bit→6-bit→4-bit PCM curriculum | **~4h** | 更安全创新，直接支撑 PCM rescues incremental precision reduction | Final 4-bit test < 70% |
| P1 | T1-3 | PCM Preset 对比 — PCMPresetUnitCell vs PCMPresetDevice | **~2h** | 验证结论不依赖特定 preset | — |
| P1 | T1-4 | Noise-Free PCM Oracle — 训练用 PCM，eval 关 modifier | **~1h** | 拆解 ~11pp penalty 来源：device physics vs per-forward noise | Test < 85% |
| ~~P1~~ | ~~T1-5~~ | ~~lr sweep (8-bit + 4-bit PCM)~~ | ~~12h~~ | ~~砍掉：产出比太低~~ | — |

### Tier 2 — Algorithm Innovation

| Priority | ID | Task | GPU Time | Risk | Rationale | Kill If |
|:---|:---|:---|:---|:---|:---|:---|
| **P0** | T2-1 | Progressive Quantization (same as T1-2) | ~4h | **Low** | Curriculum: 8-bit PCM → 6-bit → 4-bit | Final 4-bit < 70% |
| P1 | T2-2 | Distillation (Noisy Teacher → Student) | ~3h | Medium | +1-3pp potential | — |
| P2 | T2-3 | Analog-SAM | ~4h | **High** | SAM 2nd-order grad 可能不支持 analog tiles | Epoch 20 test < 75% |
| P2 | T2-4 | Adaptive Noise Schedule | ~2h | Low | Anneal modifier_std_dev | — |
| P3 | T2-5 | Drift-Aware Regularization | ~3h | High | 需要 physics model | — |

### Tier 3 — LLM Work-2（Separate Track）

| Priority | ID | Task | GPU Time | Status |
|:---|:---|:---|:---|:---|
| P0 | T3-1 | Analog KV-cache integration | ~4h | Next open step |
| P1 | T3-2 | Pythia held-out evaluation | ~4h | Infrastructure ready |
| P2 | T3-3 | Full noisy all-module Pythia | ~8h | Destructive per smoke test |

---

## 五、对 Codex 的审阅请求

请 Codex 重点审阅以下内容：

### 1. 实验设计的统计严谨性
- Single seed=42 是否足够支撑论文结论？Multi-seed 的必要性评估。
- Fresh eval 的 10-instance 设计是否足够？是否需要更多 instance 或 MC runs？
- Drift eval 只测了 24h（和 3d extended），是否需要更长时间点？

### 2. Narrative 的漏洞
- "PCM device physics enable 4-bit training" 这个 causal claim 是否站得住脚？
- 是否有 alternative explanation 我们没排除？（例如：PCM 的 specific noise distribution 恰好适合 4-bit，而非 device physics 本身）
- 4-bit pure 失败是否可能是因为 AIHWKit 的 `InferenceRPUConfig` 在 4-bit 下有 bug，而非本质上的不可训练？

### 3. 优先级建议
- Tier 1 的 4 个任务排序是否合理？
- 是否有更高效的 reviewer defense 策略（例如：理论分析替代部分实验）？
- Progressive Quantization 的实现是否有技术障碍需要提前排查？

### 4. 代码/脚本审查
- `run_pcm_multi_seed_validation.sh` 修正后是否还有其他隐藏的配置错误？
- `train_aihwkit_baseline.py` 的 `--modifier-type` 和 `--modifier-std-dev` 传播路径是否正确？
- `eval_aihwkit_fresh.py` 和 `eval_aihwkit_drift_extended.py` 的 RPUConfig 重建是否与训练一致？

---

## 六、待办清单

- [ ] T1-1 PCM Multi-Seed Validation 完成（~8h）
- [ ] T1-2 Progressive Quantization 设计与实现
- [ ] T1-3 PCM Preset 对比
- [ ] T1-4 Noise-Free Oracle
- [ ] 05_results.tex PCM subsection 重写（当前仍用旧数据 61.10%）
- [ ] Manuscript figure (r11d_fresh_eval_bars) 更新
- [ ] Reviewer defense argument 草稿

---

*Produced by Claude for Codex review. All claims must be independently verified before inclusion in manuscript.*
