# Remote 107 总任务清单（Master Task List）

> 最后更新：2026-05-13  
> 分支：`107-clean`

---

## 一、核心训练实验（HAT Adaptive Noise Schedule）

| # | 任务 | 模型 | 状态 | 结果位置 |
|---|---|---|---|---|
| 1 | Fixed noise baseline | 410M | ✅ | `p410m_adaptive_fixed_v4_seed42.json` |
| 2 | Cosine decay schedule | 410M | ✅ | `p410m_adaptive_cosine_v4_seed42.json` |
| 3 | Layer-wise schedule | 410M | ✅ | `p410m_adaptive_layerwise_v4_seed42.json` |
| 4 | Fixed noise baseline | 2.8B | ✅ | `p28b_adaptive_fixed_v1_seed42.json` |
| 5 | Cosine decay schedule | 2.8B | ✅ | `p28b_adaptive_cosine_v1_seed42.json` |
| 6 | Layer-wise schedule | 2.8B | ✅ | `p28b_adaptive_layerwise_v1_seed42.json` |
| 7 | Fixed noise baseline | 6.9B | ✅ | `p69b_adaptive_fixed_v1_seed42.json` |
| 8 | Cosine decay schedule | 6.9B | ✅ | `p69b_adaptive_cosine_v1_seed42.json` |
| 9 | Layer-wise schedule | 6.9B | ✅ | `p69b_adaptive_layerwise_v1_seed42.json` |
| 10 | Reverse layer-wise schedule | 410M | ✅ | 21.30 PPL（差于layerwise） |
| 11 | Reverse layer-wise schedule | 2.8B | ✅ | 12.68 PPL（与fixed持平） |
| 12 | Last2 + cosine schedule | 2.8B | ✅ | **12.56 PPL**（优于last2 fixed 13.78） |
| 13 | Cosine 1000 steps | 410M | ✅ | 20.73 PPL（差于500-step cosine） |
| 13b | **Fixed 1000 steps** | 410M | ✅ | 20.75 PPL（验证更长fixed有害） |
| 13c | **Fixed 1000 steps** | 2.8B | ⏳ GPU7 | `train_p28b_adaptive_fixed_1000.log` |

---

## 二、层消融实验（Layer Ablation）

| # | 任务 | 模型 | 状态 | 备注 |
|---|---|---|---|---|
| 14 | Last1 (baseline) | 410M/2.8B/6.9B | ✅ | 已包含在核心训练中 |
| 15 | Last2 | 2.8B | ✅ | `p28b_hat_last2_fixed500_seed42_seed42.json` |
| 16 | Last4 | 2.8B | ✅ | `p28b_hat_last4_fixed500_seed42_seed42.json` |
| 17 | Last2 | 6.9B | ✅ | `p69b_hat_last2_fixed500_seed42_seed42.json` |
| 18 | Last4 | 6.9B | ✅ | `p69b_hat_last4_fixed500_seed42_seed42.json` |

---

## 三、下游评估（Downstream Eval）

### 3.1 标准三项（Lambada / Hellaswag / ARC-Easy）

| # | 任务 | 模型 | 状态 |
|---|---|---|---|
| 19 | Clean + Analog eval | 410M adaptive ×3 | ✅ |
| 20 | Clean + Analog eval | 2.8B adaptive ×3 | ✅ |
| 21 | Clean + Analog eval | 6.9B adaptive ×3 | ✅ |
| 22 | Clean + Analog eval | 2.8B last2/last4 | ✅ |
| 23 | Clean + Analog eval | 6.9B last2/last4 | ✅ |
| 24 | p28b last2 cosine eval | ⏳ GPU4/5 | clean + analog 评估中 |
| 24b | **Reverse / 1000steps eval** | 待跑 | 训练已完成，待排期 |

### 3.2 扩展评估（MMLU / Winogrande / PIQA / BoolQ）

| # | 任务 | 模型 | 状态 | 备注 |
|---|---|---|---|---|
| 25 | Extended eval | p28b clean/analog | ✅ | MMLU+Winogrande+PIQA+BoolQ |
| 26 | Extended eval | p69b analog | ✅ | 同上 |
| 27 | **MMLU only** | p69b clean | ❌ Blocked | datasets cache corruption |

---

## 四、鲁棒性扫描（Robustness Sweeps）

| # | 任务 | 状态 | 备注 |
|---|---|---|---|
| 28 | σ_c2c 敏感度扫描 | ✅ | 0.005–0.1 |
| 29 | σ_d2d 敏感度扫描 | ✅ | 0.01–0.1 |
| 30 | σ_c2c mismatch 扫描 | ✅ | 训练/推理不匹配 |
| 31 | σ_d2d mismatch 扫描 | ✅ | 同上 |
| 32 | Cross-instance D2D 一致性 | ✅ | 多 seed |
| 33 | n_states 量化精度扫描 | ✅ | 128/256/512/1024 |
| 34 | Retention noise 扫描 | ✅ | 0.001/0.01/0.1/1.0 |
| 35 | Cross-device 评估 (RRAM/PCM/FeFET) | ✅ | 基于已有 checkpoint |

---

## 五、Qwen3-VL 实验

| # | 任务 | 状态 | 备注 |
|---|---|---|---|
| 36 | Qwen3-VL HAT 训练 (500 steps) | ✅ | 已完成 |
| 37 | Qwen3-VL HAT 训练 (5000 steps) | ✅ | 已完成 |
| 38 | Qwen3-VL 验证 eval | ✅ | 5 images × 4 configs |
| 39 | **Qwen3-VL 5000-step checkpoint eval** | ⏳ GPU6 | 5 images × 4 configs 评估中 |
| 40 | Qwen3-VL claim-lock metadata | ❌ Pending | 依赖 #39 |

---

## 六、系统与分析

| # | 任务 | 状态 | 产出 |
|---|---|---|---|
| 41 | Energy profiling 脚本 | ✅ | `scripts/energy_profile_kv_cache.py` |
| 42 | Energy profiling 基线数据 | ✅ | `results/paper2/energy_profile_kv_cache.json` |
| 43 | 文献引用整理 (Energy/Theory) | ✅ | `coordination/literature_citations_paper2.md` |
| 44 | **理论数学推导 (PAC-Bayes)** | ✅ Draft | `coordination/HAT_THEORETICAL_FRAMEWORK.md` 已起草 |
| 45 | 生成 Paper 2 图表 | ❌ Deferred | 用户指定非本 agent 任务 |

---

## 七、代码修复与基础设施

| # | 任务 | 状态 | 备注 |
|---|---|---|---|
| 46 | Adaptive schedule closure capture bug 修复 | ✅ | `p3_hat_train.py` |
| 47 | Offline sharded model loading | ✅ | `_resolve_local_path` |
| 48 | Claim-lock manifests | ✅ | p28b/p69b downstream |
| 49 | Coordination 文档归档 | ✅ | 多个 RETURN/MD 文件 |

---

## 统计

| 类别 | 已完成 | 进行中 | 待办/Blocked |
|---|---:|---:|---:|
| 核心训练 | 11 | 1 | 0 |
| 层消融 | 4 | 0 | 0 |
| 下游评估 | 8 | 2 | 0 |
| 鲁棒性扫描 | 7 | 0 | 0 |
| VLM | 3 | 1 | 1 |
| 系统/分析 | 4 | 0 | 1 |
| 基础设施 | 4 | 0 | 0 |
| **总计** | **41** | **4** | **2** |

---

## 当前 GPU 占用

| GPU | 任务 | 状态 |
|---|---|---|
| 4 | p28b last2 cosine clean eval | 运行中 |
| 5 | p28b last2 cosine analog eval | 运行中 |
| 6 | Qwen3-VL 5000-step checkpoint eval | 运行中 |
| 7 | p28b fixed 1000 steps 训练 | 进行中 |
