
# Remote 107 完整历史任务总表（按闭环分段）

> 最后更新：2026-05-20  
> 分支：`107-clean`
> 最新 commit：`abdf5c5`

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
| P3-6.9B | 6.9B 可行性探测 + 1000步完整训练 | ✅ | `--fp16` + `--freeze-non-target-params` 成功在 GPU5 (32GB) 运行；1000 steps: 12.30 pre → 11.14 post，~1h03min |
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
| R1-EXT | 扩展下游评估 | ✅ | p28b/p69b clean + analog extended 全部完成（max_length=2048）；p28b clean: MMLU24.97/WG59.19/PIQA73.39/BoolQ62.60；p69b clean: MMLU26.51/WG62.12/PIQA75.73/BoolQ64.50；analog 最大退化 <0.86% |
| R1-RET | Retention noise 扫描 | ✅ | 0.001/0.01/0.1/1.0 on p28b + p69b |

---

## 闭环 5：Paper 2 第二轮 — 层消融与跨设备

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| R2-LAST2 | Layer ablation last2（p28b/p69b） | ✅ PPL + ⏳ downstream | PPL: p28b 13.78 / p69b 11.56；standard3 downstream eval 正在 GPU5/6 运行中 |
| R2-LAST4 | Layer ablation last4（p28b/p69b） | ✅ PPL + ⏳ downstream | PPL: p28b 14.12 / p69b 11.85；standard3 downstream eval 正在 GPU5/6 运行中 |
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
| R3-EXTRA | **410M/2.8B fixed 1000 steps** | ✅ | 410M fixed 1000=20.75（验证更长fixed有害）；p28b fixed 1000=12.41（训练完成） |
| R3-REV-EVAL | **Reverse / fixed_1000 标准 eval** | ✅ | p28b reverse_v1 clean/analog standard3 完成；p28b fixed_1000 clean/analog standard3 完成 |
| R3-6.9B-1K | **6.9B fixed 1000 steps** | ✅ | 12.30 pre → 11.14 post（1000 steps，~1h03min 训练）|
| R3-LIT | 文献引用整理（Energy/Theory） | ✅ | `coordination/literature_citations_paper2.md` |

---

## 闭环 7：VLM 实验

| # | 任务 | 状态 | 关键结果 |
|---|---|:---|:---|
| VLM-500 | Qwen3-VL HAT 训练（500 steps） | ✅ | last1 analog KV |
| VLM-5000 | Qwen3-VL HAT 训练（5000 steps） | ✅ | last1 analog KV |
| VLM-VAL | Qwen3-VL 验证评估 | ✅ | 5 images × 4 configs |
| VLM-5K-EVAL | **Qwen3-VL 5000-step checkpoint eval** | ✅ | 20 configs 全部完成（5 images × clean/last1/last2/last4）；manifest 已生成 |

---

## 闭环 8：Paper 2 第四轮 — Codex 审查与机制控制

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R0-AUDIT | Codex 审查（远程107 vs 论文 claim） | ✅ | 发现 4 个问题：Q1 PPL mismatch、Q2 config count、Q3 git_commit_hat、Q4 parity framing |
| R0-FIX | Summary JSON 修复 | ✅ | total_entries=19（原错误20），git_commit_hat="deployed_as_directory" |
| R0-DOC | Reconciliation 文档 | ✅ | `results/remote107/RECONCILIATION_20260520.md`：逐项回答 Codex Q1-Q4 |
| R0-COMMIT | R0 修复提交 | ✅ | `4e9f627` 已推送至 `107-clean`，含 summary 修正 + RECONCILIATION |

| R1-LAUNCH | **410M 机制控制实验** | ✅ 7/7 完成 | 验证 HAT 精度损失来源（模拟patch vs 量化+噪声）|
| R1-BASE | base_clean（基线） | ✅ | raw HF 410M，无噪声，无模拟；PPL=14.94 |
| R1-PZ-L1 | patched_zero_last1 | ✅ | 1 层模拟 patch，零噪声；PPL=15.04（+0.10） |
| R1-PZ-L2 | patched_zero_last2 | ✅ | 2 层模拟 patch，零噪声；PPL=15.23（+0.29） |
| R1-PZ-L4 | patched_zero_last4 | ✅ | 4 层模拟 patch，零噪声；PPL=16.75（+1.81） |
| R1-PZ-ALL | patched_zero_all24 | ✅ | 24 层全模拟 patch，零噪声；PPL=20.88（+5.93） |
| R1-HAT-ZERO | hat_quant_zero_noise | ✅ | HAT checkpoint + 零噪声；PPL=13.53（-1.41，改善！） |
| R1-HAT-D2D | hat_d2d_0p05 | ✅ | HAT checkpoint + sigma_d2d=0.05；PPL=14.97（+0.03） |
| R1-PLOT | Scaling law 图 | ✅ | ΔPPL(N) = 1.69e11·N^(-1.286)，R²=0.993；figures/scaling_law.pdf |
| R1-VERDICT | **机制控制判决** | ✅ | 判决 C：HAT 微调主导。零噪声 HAT 改善基线 PPL (-1.41)，纯 patch 仅 +0.10~+0.29 |
| R1-SRCLOCK | **Source-lock 包** | ✅ | `source_lock_20260520/`：9 个文件，含 R1 CSV/json/csv/manifest/sha256 |

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
| BLK-MMLU | p69b clean MMLU eval | ✅ 已完成 | `lm_eval_p69b_fixed500_seed42_clean_boolq_mmlu_piqa_winogrande.json` 已存在（max_length=2048）；Task #76 待关闭 |
| BLK-THEORY | 理论数学推导（PAC-Bayes 界） | ✅ Draft | `coordination/HAT_THEORETICAL_FRAMEWORK.md` 已起草 |
| BLK-FIG | Paper 2 图表生成 | ✅ 已完成 | Scaling law 图：ΔPPL = α·N^(-β)，β=1.286，R²=0.993 |
| BLK-6.9B | 6.9B 完整训练（1000 steps） | ✅ 已完成 | 12.30→11.14 PPL，1h03min，GPU5 int4 32GB |

---

## 统计

| 闭环 | 已完成 | 进行中 | 阻塞/待办 |
|---|---:|---:|---:|
| P0 基线 | 2 | 0 | 0 |
| P1 核心 K107 | 6 | 0 | 0 |
| P2 规模 | 3 | 0 | 0 |
| P3 大模型/基建 | 4 | 0 | 0 |
| R1 鲁棒性/下游 | 8 | 0 | 0 |
| R2 层消融/跨设备 | 2 | 0 | 0 |
| R3 自适应调度 | 13 | 0 | 0 |
| VLM | 4 | 0 | 0 |
| R0 Codex 审查 | 4 | 0 | 0 |
| R1 机制控制 | 10 | 0 | 0 |
| 基础设施 | 4 | 0 | 1 |
| 阻塞/长期 | 4 | 0 | 0 |
| **总计** | **63** | **0** | **3** |

> 注：p69b_fixed1000 clean eval 仍在 GPU5 运行。

---

## 当前 GPU 占用（2026-05-20 17:00 更新）

| GPU | 任务 | 状态 | 备注 |
|---|---|---|---|
| 4 | 空闲 | — | R1 全部完成 |
| 5 | **p69b fixed1000 clean eval** | 运行中 | 6.9B 1000-step checkpoint clean（完成后自动跑 analog）|
| 6 | 空闲 | — | 待安排 |
| 7 | 空闲 | — | 待安排 |

> **Robustness sweep 已完成**（2026-05-15~2026-05-18）：
> - 42 个 robustness eval jobs 全部完成（p28b 21 + p69b 21），零崩溃
> - 4 卡并行切片部署成功，从预估 8-10 天压缩至 ~2.5 天
> - 后台 monitor + 4 份 recovery 脚本保障容错

---

## 待补缺口与后续实验

| # | 缺口/任务 | 状态 | 备注 |
|---|---|---|---|
| GAP-1 | p28b adaptive cosine last2 **extended eval** | ✅ 已完成 | 所有 extended eval 全部完成 |
| GAP-2 | p69b fixed500 clean MMLU（统一协议重跑） | ✅ 已完成 | `lm_eval_p69b_fixed500_seed42_clean_boolq_mmlu_piqa_winogrande.json` |
| GAP-3 | VLM 5K eval claim-lock manifest | ⏳ 待生成 | 待最终关闭前处理 |
| GAP-4 | 全量结果 commit + push | ✅ 已执行 | `4e9f627` 推送到 `107-clean`；R0 修复 + R1 部分结果 + scaling law |
| GAP-5 | 大型 eval JSON 压缩/清理 | ⏳ 待处理 | LFS 已上线 |

---

## 时间线预警

- **GPU4**：空闲（R1 全部完成，7/7）
- **GPU5**：p69b fixed1000 clean eval（较大模型，预计还需 ~1h）→ analog
- **GPU6/7**：空闲，可安排补充实验
- 之后：等待 GPU5 完成后更新 summary + 最终 commit/push

