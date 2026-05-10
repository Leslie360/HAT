# Claude 工作自查报告 — 供 Gemini 审阅

**Date:** 2026-04-28
**Scope:** R11D PCM multi-seed validation pipeline + related scripts
**Purpose:** Third-party bug hunt on Claude's work after two critical errors were found

---

## 1. 执行摘要

Claude 负责 R11D 实验 suite 的 multi-seed validation 和后续优先级任务。在 Codex 审阅前，Claude 连续犯下 **两个 critical bug**。

本报告列出 Claude 的所有代码/脚本修改，供 Gemini 独立审阅是否存在 **第三个未被发现的 bug**。

---

## 2. 已发现的 Bug（Claude 自检 + Codex 发现）

### Bug #1: modifier_std_dev 配置错误

| Item | Detail |
|:---|:---|
| **位置** | `paper2_aihwkit_baseline/run_pcm_multi_seed_validation.sh` line 33 |
| **错误** | `--modifier-std-dev 0.0001`（从 R11D-6b pure baseline 脚本复制，未修正） |
| **正确值** | `0.10`（原始 R11D-5a/R11D-7 使用默认值 0.10） |
| **影响** | seed=123 跑出 85.72%，与原始 76.96% 完全不可比 |
| **发现者** | Claude（通过检查原始 checkpoint 的 fresh_eval.json） |
| **修复** | `Edit` 将 0.0001 → 0.10 |

### Bug #2: 训练脚本选择错误（P0，更严重）

| Item | Detail |
|:---|:---|
| **位置** | `paper2_aihwkit_baseline/run_pcm_multi_seed_validation.sh` line 8 |
| **错误** | 调用 `train_aihwkit_baseline.py`（`InferenceRPUConfig` + `ADD_NORMAL` + **默认 `IdealDevice`**） |
| **正确脚本** | `r11d4_train_pcm.py`（`PCMPresetUnitCell` + `AnalogSGD` + `post_update_step()`） |
| **影响** | 所谓的 "PCM multi-seed" 实际上是 pure ADD_NORMAL baseline，**完全没有 PCM device physics** |
| **发现者** | Codex 审阅 |
| **修复** | 重写 `run_pcm_multi_seed_v2.sh`，调用 `r11d4_train_pcm.py` |

**关键区别：**
```python
# train_aihwkit_baseline.py (BUG 脚本)
cfg = InferenceRPUConfig()
cfg.forward.inp_res = inp_res
cfg.forward.out_res = out_res
# cfg.device 未设置 → 默认 IdealDevice
# 优化器可能是 AdamW 或普通 SGD

# r11d4_train_pcm.py (正确脚本)
cfg = InferenceRPUConfig()
cfg.device = pcm_device  # PCMPresetUnitCell
# 优化器 = AnalogSGD → 触发 post_update_step() 的 pulse-update 物理
```

---

## 3. Claude 的所有文件修改清单

### 3.1 新建文件

| 文件 | 用途 | 风险等级 |
|:---|:---|:---|
| `run_pcm_multi_seed_validation.sh` | 原始 multi-seed 脚本（含 Bug #1 + #2）| **已废弃** |
| `run_pcm_multi_seed_v2.sh` | 修正版 multi-seed（`r11d4_train_pcm.py`）| 待审阅 |
| `run_pcm_preset_comparison.sh` | T1-3 PCM preset 对比脚本 | 待审阅 |
| `R11D_EXPERIMENT_AUDIT_SUMMARY_20260428.md` | 审计总结文档 | N/A |
| `CLAUDE_SELF_AUDIT_GEMINI_REVIEW_20260428.md` | 本文件 | N/A |

### 3.2 修改文件

| 文件 | 修改内容 | 行号 |
|:---|:---|:---|
| `r11d4_train_pcm.py` | `_resolve_pcm_preset()` 添加 `preferred` 参数 | 49-67 |
| `r11d4_train_pcm.py` | `make_rpu_config()` 添加 `pcm_preset=None` 参数 | 122-125 |
| `r11d4_train_pcm.py` | `build_model()` 添加 `pcm_preset=None` 参数 | 151-160 |
| `r11d4_train_pcm.py` | Argparser 添加 `--pcm-preset` | 206 |
| `r11d4_train_pcm.py` | 主函数 `make_rpu_config()` 调用传递 `pcm_preset` | 241-246 |
| `r11d4_train_pcm.py` | 主函数 `build_model()` 调用传递 `pcm_preset` | 258-264, 275-281 |
| `AGENT_INTERCOM_HUB_20260428.md` | 追加审计和状态更新 | 83-112, 117-127 |

---

## 4. 请 Gemini 重点审查的潜在风险点

### 🔴 P0: `r11d4_train_pcm.py` 的 `--pcm-preset` 修改

**修改动机：** 支持 T1-3 PCM preset 对比（`PCMPresetUnitCell` vs `PCMPresetDevice`）。

**修改代码：**
```python
def _resolve_pcm_preset(preferred=None):
    registry = PCM_PRESET_REGISTRY
    if preferred:
        preferred_tuple = None
        for item in registry:
            if item[1] == preferred:
                preferred_tuple = item
                break
        if preferred_tuple:
            registry = [preferred_tuple] + [i for i in registry if i != preferred_tuple]
    # ... try registry in order
```

**审阅问题：**
1. `if preferred:` 对字符串 `""` 或 `"PCMPresetUnitCell"` 的行为是否正确？
2. `preferred_tuple` 不在 registry 中时， silently fallback 到默认顺序。是否应该改为 **报错**？
3. `registry = [preferred_tuple] + [i for i in registry if i != preferred_tuple]` 中 `i != preferred_tuple` 对 tuple 的比较是否可靠？（Python tuple 比较是按元素的，这里应该正确，但需确认）
4. **multi-seed v2 脚本没有传递 `--pcm-preset`**，因此 `_resolve_pcm_preset(preferred=None)` 路径被调用。此路径行为是否与修改前完全一致？

### 🔴 P0: multi-seed v2 脚本参数核对

**脚本：** `run_pcm_multi_seed_v2.sh`

**请 Gemini 逐项核对以下参数是否与原始 R11D-5a/R11D-7 一致：**

| 参数 | v2 脚本值 | 原始 R11D-5a | 原始 R11D-7 | 一致？ |
|:---|:---|:---|:---|:---|
| 训练脚本 | `r11d4_train_pcm.py` | `r11d4_train_pcm.py` | `r11d4_train_pcm.py` | ✅ |
| seed | 123, 456 | 42 | 42 | N/A (多 seed 目的) |
| epochs | 100 | 100 | 100 | 待确认 |
| batch-size | 64 | 64 | 64 | 待确认 |
| lr | 0.001 | 1e-3 | 1e-3 | 待确认 |
| wd | 0.05 | 0.05 | 0.05 | 待确认 |
| momentum | 0.0 | 0.0 (default) | 0.0 (default) | 待确认 |
| device | cuda | cuda | cuda | 待确认 |
| workers | 0 | 0 | 0 | 待确认 |
| inp-res | 0.00390625 / 0.0625 | 1/256=0.00390625 | 1/16=0.0625 | ✅ |
| out-res | 同上 | 同上 | 同上 | ✅ |
| modifier-std-dev | 0.10 | 0.10 (default) | 0.10 (default) | ✅ |
| early-stop-patience | 0 | ??? | ??? | **待确认** |

**关键问题：** 原始 R11D-5a 的 `training_history.json` 显示 100 epochs，`best_acc=76.96%`，`last_epoch_acc=76.91%`。这是否意味着：
- (a) 没有使用 early-stop，完整跑了 100 epochs？
- (b) 使用了 early-stop 但 patience 很大（如 50+），未触发？

 Claude 假设 (a)，因此 v2 脚本设置了 `--early-stop-patience 0`（禁用早停）。**如果原始实验实际使用了 early-stop，v2 脚本的行为将不一致。**

### 🟡 P1: `run_pcm_preset_comparison.sh` 设计审查

**设计：** 用 seed=42 分别跑 8-bit 和 4-bit 的 `PCMPresetDevice`，与已有的 `PCMPresetUnitCell` 结果对比。

**问题：**
1. 只用 seed=42 是否足够？如果两个 preset 在 seed=42 下差异很小，是否需要多 seed？
2. `PCMPresetDevice` 和 `PCMPresetUnitCell` 的区别是什么？Claude 未在脚本中记录。
3. 比较时是否需要控制其他变量（如 identical seed sequence）？

### 🟡 P1: 叙事文档的准确性

`R11D_EXPERIMENT_AUDIT_SUMMARY_20260428.md` 中的实验矩阵和 narrative 是否基于 **作废的错误数据**？

- R11D-5a seed=123 (v1) 的 85.72% 已明确标记作废
- 但 audit doc 中的 "Core narrative" 部分仍使用了 seed=42 的单 seed 数据
- **这些数据本身是有效的**（来自正确的 `r11d4_train_pcm.py`），但 "single seed" 仍是 reviewer 攻击面

---

## 5. Claude 的验证清单（已做 / 未做）

| 验证项 | 状态 | 方法 |
|:---|:---|:---|
| v2 脚本调用的是 `r11d4_train_pcm.py` | ✅ | `ps aux` 确认 PID=39551 的命令行 |
| v2 脚本使用了 PCMPresetUnitCell | ✅ | 日志输出 `[PCM] Resolved preset: aihwkit.simulator.presets.PCMPresetUnitCell` |
| v2 脚本使用了 AnalogSGD | ✅ | `r11d4_train_pcm.py` 源码确认 line 279 |
| v2 脚本 modifier_std_dev=0.10 | ✅ | 命令行参数确认 |
| 原始 R11D-5a 的 early-stop 配置 | ❓ | **未确认** — training_history.json 有 100 epochs，但不确定是否禁用早停 |
| `r11d4_train_pcm.py` 修改后语法正确 | ✅ | Python 可正常启动（已在训练） |
| `--pcm-preset` 参数传递链完整 | ❓ | **未验证** — 只测试了 `None` 路径，`PCMPresetDevice` 路径未测试 |

---

## 6. 当前 GPU 状态

| 实验 | 状态 | 配置 |
|:---|:---|:---|
| R11D-7 seed=123 | epoch 3/100, test 24.09% | 4-bit PCM, PCMPresetUnitCell, AnalogSGD |

**Pipeline 队列：**
```
R11D-7 seed=123 → R11D-7 seed=456 → R11D-5a seed=123 → R11D-5a seed=456
```

---

## 7. 请 Gemini 回答

1. **是否还有第三个 hidden bug？** 重点检查 `_resolve_pcm_preset(preferred)` 逻辑和参数传递链。
2. **multi-seed v2 脚本的 early-stop-patience=0 是否与原始实验一致？** 如何确认原始 R11D-5a/R11D-7 的早停配置？
3. **T1-3 preset 对比的设计是否足够严谨？** 是否需要多 seed 或更长的训练？
4. **Claude 修改 `r11d4_train_pcm.py` 的方式是否安全？** 是否应该在副本上修改而非原文件？

---

*Produced by Claude for Gemini independent review. All claims subject to verification.*
