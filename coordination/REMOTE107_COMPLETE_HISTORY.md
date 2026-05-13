# Remote 107 完整历史任务总表（按闭环分段）

> 最后更新：2026-05-13  
> 分支：`107-clean`

---

## 闭环 0：基线校准与可行性验证（P0）

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| P0-A | 基线评估器校准 | ✅ | 典型基线 22.18 PPL（ctx=512/stride=256/bs=1）；旧评估器 15.68 已废弃 |
| P0-B | 配对 HAT 检查点消融 | ✅ | 24 eval jobs：B1→B2→B3/B4 阶梯；patch 本身 +0.02 PPL，D2D=0.02 加 +0.42，D2D=0.05 加 +0.58 |

---

## 闭环 1：核心 K107 验证（P1）

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| K107-A | 典型选择性 KV 范围扫描 | ✅ | last1 [23] = 19.45；last2 [22,23] = 20.14；all layers = 37+（灾难性） |
| K107-B | 保持压力测试 | ✅ | last1 + retention refresh 改善 ~0.3 PPL；all-layer 仍崩溃 |
| K107-C | 状态数量扫描 | ✅ | n_states=64 最佳（19.40）；256 生产选择（19.46） |
| P1-B | Pythia-1B last1 验证 | ✅ | 100 steps → 14.60 PPL；D2D=0.05 仅 +0.20 |
| P1-EPSC | 极端代理压力评估 | ✅ | 45 eval jobs；sigma=0.15 时 20.76 PPL，远低于 25 kill line |
| P1-FIG | 图表生成脚本 | ✅ | 3 张图（消融阶梯、EPSC 压力、规模趋势） draft-ready |

---

## 闭环 2：规模验证（P2）

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| P2-1B | Pythia-1B 规模检查 | ✅ | seed42/123 复现 Δ<0.03；14.60 PPL @ D2D=0.02 |
| P2-2.8B | Pythia-2.8B 规模检查 | ✅ | seed42/123 复现 Δ<0.02；13.34 PPL @ D2D=0.02 |
| P2-2.8B-EPSC | 2.8B EPSC + C2C 扫描 | ✅ | 21 eval jobs；sigma_c2c=0.10 仅 +0.26 PPL；sigma=0.15 时 13.91 PPL |

---

## 闭环 3：大模型可行性与基础设施（P3）

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| P3-6.9B | 6.9B 可行性探测 | ❌ Blocked | 32GB VRAM + fp32 无法安全运行；需 AMP/BF16/多 GPU |
| P3-2.8B-500 | 2.8B 500-step 固定基线 | ✅ | 13.69 pre → 12.68 post（500 steps） |
| P3-6.9B-500 | 6.9B 500-step 固定基线 | ✅ | 12.30 pre → 11.40 post（500 steps） |
| P3-AUDIT | AMP/冻结参数代码审计 | ✅ | `--freeze-non-target-params` + `--fp16` 已合并；旧结果仍有效 |
| P3-OPT | 选择性优化器审计 | ✅ | 仅优化 patched 层可节省显存；2.8B 可 fit 32GB |

---

## 闭环 4：Paper 2 第一轮 — 鲁棒性与下游评估

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| R1-C2C | σ_c2c 敏感度扫描（p28b/p69b） | ✅ | 0.005–0.1 范围；clean 对比 analog |
| R1-D2D | σ_d2d 敏感度扫描（p28b/p69b） | ✅ | 0.01–0.1 范围 |
| R1-MIS-C2C | eval σ_c2c mismatch 扫描 | ✅ | 训练/推理 c2c 不匹配 |
| R1-MIS-D2D | eval σ_d2d mismatch 扫描 | ✅ | 训练/推理 d2d 不匹配 |
| R1-XD2D | Cross-instance D2D 一致性 | ✅ | 多 seed 验证 |
| R1-NS | n_states 量化精度扫描 | ✅ | 128/256/512/1024 |
| R1-EXT | 扩展下游评估 | ✅ | MMLU/Winogrande/PIQA/BoolQ on p28b/p69b |
| R1-RET | Retention noise 扫描 | ✅ | 0.001/0.01/0.1/1.0 on p28b + p69b |

---

## 闭环 5：Paper 2 第二轮 — 层消融与跨设备

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| R2-LAST2 | Layer ablation last2（p28b/p69b） | ✅ | p28b last2: 13.78；p69b last2: 11.56 |
| R2-LAST4 | Layer ablation last4（p28b/p69b） | ✅ | p28b last4: 14.12；p69b last4: 11.85 |
| R2-DEV | Cross-device eval（RRAM/PCM/FeFET） | ✅ | 基于已有 checkpoint 评估 3 种器件参数 |
| R2-ENG | Energy/Area 分析脚本 | ✅ | `scripts/energy_profile_kv_cache.py` + 基线 JSON |

---

## 闭环 6：Paper 2 第三轮 — 自适应噪声调度（当前）

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| R3-DESIGN | 自适应噪声调度算法设计 | ✅ | fixed / cosine / layer_wise / reverse_layer_wise |
| R3-410M | 410M 自适应训练（fixed/cosine/layerwise） | ✅ | fixed=18.75, cosine=18.31, layerwise=18.36 |
| R3-2.8B | 2.8B 自适应训练（fixed/cosine/layerwise） | ✅ | fixed=12.68, cosine=12.68, layerwise=12.70 |
| R3-6.9B | 6.9B 自适应训练（fixed/cosine/layerwise） | ✅ | fixed=11.40, cosine=11.38, layerwise=11.43 |
| R3-EVAL | 全部 9 组自适应模型下游评估 | ✅ | Lambada/Hellaswag/ARC-Easy clean + analog |
| R3-REV | **Reverse layer-wise**（410M + 2.8B） | ✅ | 410M=21.30（差于layerwise 18.36）；p28b=12.68（与fixed持平） |
| R3-LAST2 | **Last2 + adaptive cosine**（p28b） | ✅ | **12.56 PPL**，优于last2 fixed（13.78），甚至略优于last1 fixed（12.68） |
| R3-1K | **410M adaptive cosine 1000 steps** | ✅ | 20.73 PPL（差于500-step cosine 18.31） |
| R3-EXTRA | **410M/2.8B fixed 1000 steps** | ⏳ GPU7 | 410M fixed 1000=20.75（验证更长fixed有害）；p28b fixed 1000训练中 |
| R3-LIT | 文献引用整理（Energy/Theory） | ✅ | `coordination/literature_citations_paper2.md` |

---

## 闭环 7：VLM 实验

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| VLM-500 | Qwen3-VL HAT 训练（500 steps） | ✅ | last1 analog KV |
| VLM-5000 | Qwen3-VL HAT 训练（5000 steps） | ✅ | last1 analog KV |
| VLM-VAL | Qwen3-VL 验证评估 | ✅ | 5 images × 4 configs |
| VLM-5K-EVAL | **Qwen3-VL 5000-step checkpoint eval** | ⏳ GPU6 | 5 images × 4 configs 评估中 |

---

## 代码修复与基础设施

| # | 任务 | 状态 | 备注 |
|---|---|:---|:---|
| INF-META | Metadata patch（JSON envelope） | ✅ | 所有输出包含完整 metadata |
| INF-OFFLINE | Offline sharded model loading | ✅ | `_resolve_local_path` |
| INF-CLOSURE | Adaptive schedule closure capture bug 修复 | ✅ | `p3_hat_train.py` |
| INF-CLAIM | Claim-lock manifests | ✅ | p28b/p69b downstream + 自适应模型 |
| INF-PUSH | 大型 eval JSON 压缩/清理 | ❌ | 66MB 文件需清理或转 LFS |

---

## 阻塞 / 长期待办

| # | 任务 | 状态 | 阻塞原因 |
|---|---|:---|:---|
| BLK-MMLU | p69b clean MMLU eval | ❌ Blocked | `datasets` cache corruption |
| BLK-THEORY | 理论数学推导（PAC-Bayes 界） | ✅ Draft | `coordination/HAT_THEORETICAL_FRAMEWORK.md` 已起草 |
| BLK-FIG | Paper 2 图表生成 | ⏸️ Deferred | 用户指定非本 agent 任务 |
| BLK-6.9B | 6.9B 完整训练（非 500 steps） | ⏸️ Deferred | 需 AMP/BF16 或更大 GPU |

---

## 统计

| 闭环 | 已完成 | 进行中 | 阻塞/待办 |
|---|---:|---:|---:|
| P0 基线 | 2 | 0 | 0 |
| P1 核心 K107 | 6 | 0 | 0 |
| P2 规模 | 3 | 0 | 0 |
| P3 大模型/基建 | 3 | 0 | 1 |
| R1 鲁棒性/下游 | 8 | 0 | 0 |
| R2 层消融/跨设备 | 4 | 0 | 0 |
| R3 自适应调度 | 9 | 2 | 0 |
| VLM | 3 | 1 | 0 |
| 基础设施 | 4 | 0 | 1 |
| 阻塞/长期 | 0 | 1 | 3 |
| **总计** | **42** | **4** | **6** |

---

## 当前 GPU 占用（2026-05-13）

| GPU | 任务 | 状态 |
|---|---|---|
| 4 | p28b last2 cosine **clean eval** | 运行中 |
| 5 | p28b last2 cosine **analog eval** | 运行中 |
| 6 | Qwen3-VL 5000-step **checkpoint eval** | 运行中 |
| 7 | p28b fixed 1000 steps **训练** | 进行中（约20min剩余） |
