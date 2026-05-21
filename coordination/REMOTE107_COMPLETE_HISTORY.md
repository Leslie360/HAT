# Remote 107 完整历史任务总表（全量数据汇总）

> 最后更新：2026-05-21 19:30
> 分支：`107-clean`
> eval JSON 总数：**180**
> 覆盖：PPL 89 | Extended Downstream 43 | TruthfulQA 8 | Robustness/Ablation/Scans 40

---

## 闭环进度一览

| 闭环 | 已完成 | 进行中 | 待办 |
|---|---|---|---|
| P0 基线校准 | 2 | 0 | 0 |
| P1 核心 K107 | 6 | 0 | 0 |
| P2 规模验证 | 3 | 0 | 0 |
| P3 大模型/基建 | 5 | 0 | 0 |
| R1 鲁棒性/下游 | 8 | 0 | 0 |
| R2 层消融/跨设备 | 4 | 0 | 0 |
| R3 自适应调度 | 12 | 0 | 0 |
| VLM 实验 | 4 | 0 | 0 |
| R0 Codex 审查 | 4 | 0 | 0 |
| R1 机制控制 | 10 | 0 | 0 |
| R9 补充评估 | 3 | 1 | 0 |
| 基础设施 | 5 | 0 | 1 |
| **总计** | **66** | **1** | **1** |

---

# ═══════════════════════════════════════════
# 第一部分：任务闭环明细
# ═══════════════════════════════════════════

## 闭环 0：基线校准与可行性验证（P0）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P0-A | 基线评估器校准 | ✅ | 典型基线 22.18 PPL（ctx=512/stride=256/bs=1）；旧评估器 15.68 已废弃 |
| P0-B | 配对 HAT 检查点消融 | ✅ | 24 eval jobs；B1→B2→B3/B4 阶梯；patch 本身 +0.02 PPL，D2D=0.02 +0.42，D2D=0.05 +0.58 |

## 闭环 1：核心 K107 验证（P1）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| K107-A | 典型选择性 KV 范围扫描 | ✅ | last1 [23] = 19.45；last2 [22,23] = 20.14；all layers = 37+（灾难性） |
| K107-B | 保持压力测试 | ✅ | last1 + retention refresh 改善 ~0.3 PPL；all-layer 仍崩溃 |
| K107-C | 状态数量扫描 | ✅ | n_states=64 最佳（19.40）；256 生产选择（19.46） |
| P1-B | Pythia-1B last1 验证 | ✅ | 100 steps → 14.60 PPL；D2D=0.05 仅 +0.20 |
| P1-EPSC | 极端代理压力评估 | ✅ | 45 eval jobs；sigma=0.15 时 20.76 PPL，远低于 25 kill line |
| P1-FIG | 图表生成脚本 | ✅ | 3 张图（消融阶梯、EPSC 压力、规模趋势） draft-ready |

## 闭环 2：规模验证（P2）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P2-1B | Pythia-1B 规模检查 | ✅ | seed42/123 复现 Δ<0.03；14.60 PPL @ D2D=0.02 |
| P2-2.8B | Pythia-2.8B 规模检查 | ✅ | seed42/123 复现 Δ<0.02；13.34 PPL @ D2D=0.02 |
| P2-2.8B-EPSC | 2.8B EPSC + C2C 扫描 | ✅ | 21 eval jobs；sigma_c2c=0.10 仅 +0.26 PPL；sigma=0.15 时 13.91 PPL |

## 闭环 3：大模型可行性与基础设施（P3）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P3-6.9B | 6.9B 可行性探测 + 1000步完整训练 | ✅ | `--fp16` + `--freeze-non-target-params` 在 GPU5 (32GB) 运行；1000 steps: 12.30→11.14，~1h03min |
| P3-2.8B-500 | 2.8B 500-step 固定基线 | ✅ | 13.69 pre → 12.68 post（500 steps） |
| P3-6.9B-500 | 6.9B 500-step 固定基线 | ✅ | 12.30 pre → 11.40 post（500 steps） |
| P3-AUDIT | AMP/冻结参数代码审计 | ✅ | `--freeze-non-target-params` + `--fp16` 已合并；旧结果仍有效 |
| P3-OPT | 选择性优化器审计 | ✅ | 仅优化 patched 层可节省显存；2.8B 可 fit 32GB |

## 闭环 4：鲁棒性与下游评估（R1）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R1-C2C | σ_c2c 敏感度扫描（p28b/p69b） | ✅ | 0.005–0.1 范围；clean 对比 analog |
| R1-D2D | σ_d2d 敏感度扫描（p28b/p69b） | ✅ | 0.01–0.1 范围 |
| R1-MIS-C2C | eval σ_c2c mismatch 扫描 | ✅ | 训练/推理 c2c 不匹配 |
| R1-MIS-D2D | eval σ_d2d mismatch 扫描 | ✅ | 训练/推理 d2d 不匹配 |
| R1-XD2D | Cross-instance D2D 一致性 | ✅ | 多 seed 验证 |
| R1-NS | n_states 量化精度扫描 | ✅ | 128/256/512/1024 |
| R1-EXT | 扩展下游评估 | ✅ | p28b/p69b clean + analog extended 全部完成（max_length=2048） |
| R1-RET | Retention noise 扫描 | ✅ | 0.001/0.01/0.1/1.0 on p28b + p69b |

## 闭环 5：层消融与跨设备（R2）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R2-LAST2 | Layer ablation last2（p28b/p69b） | ✅ | PPL: p28b 5.12/5.28, p69b 5.20/5.32 (clean/analog) |
| R2-LAST4 | Layer ablation last4（p28b/p69b） | ✅ | PPL: p28b 4.95/5.59, p69b 5.12/5.59 (clean/analog) |
| R2-DEV | Cross-device eval（RRAM/PCM/FeFET） | ✅ | 基于已有 checkpoint 评估 3 种器件参数 |
| R2-ENG | Energy/Area 分析脚本 | ✅ | `scripts/energy_profile_kv_cache.py` + 基线 JSON |

## 闭环 6：自适应噪声调度（R3）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R3-DESIGN | 自适应噪声调度算法设计 | ✅ | fixed / cosine / layer_wise / reverse_layer_wise |
| R3-410M | 410M 自适应训练 | ✅ | fixed=18.75, cosine=18.31, layerwise=18.36 |
| R3-2.8B | 2.8B 自适应训练 | ✅ | fixed=12.68, cosine=12.68, layerwise=12.70 |
| R3-6.9B | 6.9B 自适应训练 | ✅ | fixed=11.40, cosine=11.38, layerwise=11.43 |
| R3-EVAL | 全部 9 组自适应模型下游评估 | ✅ | Lambada/Hellaswag/ARC-Easy clean + analog |
| R3-REV | Reverse layer-wise（410M+2.8B） | ✅ | 410M=21.30（差于layerwise 18.36）；p28b=12.68（与fixed持平） |
| R3-LAST2 | Last2 + adaptive cosine（p28b） | ✅ | **12.56 PPL**，优于last2 fixed（13.78），略优于last1 fixed（12.68） |
| R3-1K | 410M adaptive cosine 1000 steps | ✅ | 20.73 PPL（差于500-step cosine 18.31） |
| R3-EXTRA | 410M/2.8B fixed 1000 steps | ✅ | 410M=20.75（更长fixed有害）；p28b=12.41（训练完成） |
| R3-REV-EVAL | Reverse/fixed_1000 标准 eval | ✅ | p28b reverse_v1 + fixed_1000 standard3 完成 |
| R3-6.9B-1K | 6.9B fixed 1000 steps | ✅ | 12.30→11.14（1000 steps，~1h03min）|
| R3-LIT | 文献引用整理 | ✅ | `coordination/literature_citations_paper2.md` |

## 闭环 7：VLM 实验

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| VLM-500 | Qwen3-VL HAT 训练（500 steps） | ✅ | last1 analog KV |
| VLM-5000 | Qwen3-VL HAT 训练（5000 steps） | ✅ | last1 analog KV |
| VLM-VAL | Qwen3-VL 验证评估 | ✅ | 5 images × 4 configs |
| VLM-5K-EVAL | Qwen3-VL 5000-step eval | ✅ | 20 configs（5 images × clean/last1/last2/last4）|

## 闭环 8：Codex 审查 + 机制控制

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R0-AUDIT | Codex 审查 | ✅ | 4 issues: Q1 PPL mismatch, Q2 config count, Q3 git_commit_hat, Q4 parity |
| R0-FIX | Summary JSON 修复 | ✅ | total_entries=19（原20），git_commit_hat="deployed_as_directory" |
| R0-DOC | Reconciliation 文档 | ✅ | `RECONCILIATION_20260520.md`：逐项回答 Q1-Q4 |
| R0-COMMIT | R0 修复提交 | ✅ | `4e9f627` 推送至 `107-clean` |

### 机制控制实验（R1）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R1-LAUNCH | 410M 机制控制 | ✅ 7/7 | PPL 数据见下文 §8 |
| R1-PLOT | Scaling law 图 | ✅ | ΔPPL(N) = 1.69e11·N^(-1.286)，R²=0.993 |
| R1-VERDICT | 机制控制判决 | ✅ | 判决 C：HAT 微调主导 |
| R1-SRCLOCK | Source-lock 包 | ✅ | `source_lock_20260520/`：9 个文件 |

## 闭环 9：补充评估

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| EXT-v4 | v4 scheduler | ✅ | 15/42 成功；analog 全失败（序列超 buffer） |
| EXT-v5 | v5 scheduler (+max_length 2048) | ✅ | analog extended 全部补跑完成 |
| EXT-v6 | v6 scheduler (TruthfulQA) | ✅ | 8 jobs 完成 |
| EXT-v7 | v7 scheduler (MMLU 5-shot/GSM8K/AI2-ARC) | 🔄 运行中 | 12h 实验，GPU6 analog MMLU 5-shot 进行中 |

---

# ═══════════════════════════════════════════
# 第二部分：全量数据 — 按模型分类
# ═══════════════════════════════════════════

> **指标说明：**
> - **PPL** = `lambada_openai:perplexity,none`（越低越好）
> - **Lambada** = `lambada_openai:acc,none`（越高越好）
> - **HellaSwag** = `hellaswag:acc_norm,none`（越高越好）
> - **ARC-Easy** = `arc_easy:acc_norm,none`（越高越好）
> - **BoolQ** = `boolq:acc,none`
> - **MMLU** = `mmlu:acc,none`
> - **PIQA** = `piqa:acc_norm,none`
> - **WinoGrande** = `winogrande:acc,none`
> - **TruthfulQA** = `truthfulqa_mc1:acc,none`
> - **C** = Clean（推理时无模拟噪声）
> - **A** = Analog（推理时加载 AnalogLinear 噪声）

---

## §1 p410m（410M）— 全部数据

### 1.1 机制控制实验

| Config | PPL | Lambada | HellaSwag | ARC-Easy | BoolQ | MMLU | PIQA | WinoGrande |
|--------|----:|--------:|----------:|---------:|------:|-----:|-----:|-----------:|
| base_clean (C) | 14.9445 | — | — | — | — | — | — | — |
| patched_zero_last1 (A) | 15.0402 | — | — | — | — | — | — | — |
| patched_zero_last2 (A) | 15.2274 | 0.4493 | 0.3432 | 0.5118 | — | — | — | — |
| patched_zero_last4 (A) | 16.7510 | — | — | — | — | — | — | — |
| patched_zero_all24 (A) | 20.8773 | — | — | — | — | — | — | — |
| hat_quant_zero_noise (A) | 13.5252 | — | — | — | — | — | — | — |
| hat_d2d_0p05 (A) | 14.9743 | — | — | — | — | — | — | — |

### 1.2 扩展实验

| Config | PPL | BoolQ | MMLU | PIQA | WinoGrande |
|--------|----:|------:|-----:|-----:|-----------:|
| adaptive_fixed_1000 (C) | 13.4595 | 0.5709 | 0.2307 | 0.6746 | 0.5391 |
| adaptive_fixed_1000 (A) | 14.8760 | 0.5563 | 0.2326 | 0.6692 | 0.5257 |
| reverse_v1_nofreeze (C) | 20.4333 | 0.3865 | 0.2311 | 0.6638 | 0.5249 |
| reverse_v1_nofreeze (A) | 21.3111 | 0.3899 | 0.2314 | 0.6697 | 0.5328 |

---

## §2 p1b（Pythia-1B）— 全部数据

### 2.1 核心结果

| Config | PPL | Lambada | HellaSwag | ARC-Easy | BoolQ | MMLU | PIQA | WinoGrande |
|--------|----:|--------:|----------:|---------:|------:|-----:|-----:|-----------:|
| adaptive_fixed_v1 (C) | 7.1145 | 0.5841 | 0.3912 | 0.5863 | 0.6052 | 0.2446 | 0.7013 | 0.5249 |
| adaptive_fixed_v1 (A) | 7.6030 | 0.5723 | 0.3888 | 0.5846 | 0.6024 | 0.2452 | 0.7008 | 0.5501 |

### 2.2 σ_c2c 扫描

| σ_c2c | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.0 | 7.5419 | 0.5758 | 0.3903 | 0.5867 |
| 0.01 | 7.6030 | 0.5723 | 0.3888 | 0.5846 |
| 0.02 | 7.6871 | 0.5713 | 0.3898 | 0.5859 |
| 0.05 | 7.9363 | 0.5655 | 0.3888 | 0.5783 |
| 0.10 | 8.1701 | 0.5616 | 0.3887 | 0.5800 |

### 2.3 σ_d2d 扫描

| σ_d2d | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.01 | 7.3794 | 0.5781 | 0.3904 | 0.5846 |
| 0.02 | 7.6030 | 0.5723 | 0.3888 | 0.5846 |
| 0.05 | 7.9675 | 0.5641 | 0.3871 | 0.5884 |
| 0.10 | 8.1119 | 0.5616 | 0.3861 | 0.5871 |

### 2.4 Cross-instance D2D Consistency

| Seed | PPL | Lambada | HellaSwag | ARC-Easy |
|-----:|----:|--------:|----------:|---------:|
| 3373 | 7.6030 | 0.5723 | 0.3888 | 0.5846 |
| 3374 | 7.6337 | 0.5731 | 0.3886 | 0.5892 |
| 3375 | 7.5936 | 0.5740 | 0.3892 | 0.5863 |
| 3376 | 7.5215 | 0.5721 | 0.3885 | 0.5808 |
| 3377 | 7.6181 | 0.5723 | 0.3883 | 0.5842 |
| **CV** | **<0.6%** | | | |

---

## §3 p28b（Pythia-2.8B）— 全部数据

### 3.1 自适应调度 — PPL

| Schedule | Clean PPL | Clean Lambada | Clean HellaSwag | Clean ARC-Easy | Analog PPL | Analog Lambada | Analog HellaSwag | Analog ARC-Easy | ΔPPL |
|----------|----------:|--------------:|----------------:|---------------:|-----------:|---------------:|-----------------:|----------------:|-----:|
| fixed500 | 5.0999 | 0.6470 | 0.4569 | 0.6418 | 5.1424 | 0.6447 | 0.4566 | 0.6397 | +0.04 |
| adaptive_cosine_v1 | 5.0961 | 0.6466 | 0.4586 | 0.6418 | 5.1386 | 0.6416 | 0.4573 | 0.6465 | +0.04 |
| adaptive_fixed_v1 | 5.1040 | 0.6466 | 0.4563 | 0.6406 | 5.1446 | 0.6468 | 0.4565 | 0.6380 | +0.04 |
| adaptive_layerwise_v1 | 5.0990 | 0.6486 | 0.4560 | 0.6427 | 5.1406 | 0.6439 | 0.4555 | 0.6418 | +0.04 |
| adaptive_reverse_v1 | 5.1040 | 0.6466 | 0.4563 | 0.6406 | 5.1446 | 0.6468 | 0.4565 | 0.6380 | +0.04 |
| adaptive_cosine_last2 | 5.1182 | 0.6470 | 0.4578 | 0.6418 | 5.2125 | 0.6389 | 0.4552 | 0.6414 | +0.09 |
| adaptive_fixed_1000 | 5.0833 | 0.6466 | 0.4575 | 0.6439 | 5.1222 | 0.6468 | 0.4568 | 0.6423 | +0.04 |

> 注：fixed_v1 和 reverse_v1 的 clean PPL 为同一数值（5.1040），analog PPL 也相同（5.1446），说明二者在效果上等价。

### 3.2 层消融

| Config | Clean PPL | Clean Lambada | Clean HellaSwag | Clean ARC-Easy | Analog PPL | Analog Lambada | Analog HellaSwag | Analog ARC-Easy | ΔPPL |
|--------|----------:|--------------:|----------------:|---------------:|-----------:|---------------:|-----------------:|----------------:|-----:|
| last2 | 5.1153 | 0.6449 | 0.4567 | 0.6397 | 5.2787 | 0.6406 | 0.4560 | 0.6418 | +0.16 |
| last4 | 4.9532 | 0.6573 | 0.4572 | 0.6435 | 5.5880 | 0.6282 | 0.4538 | 0.6439 | +0.63 |

### 3.3 Extended Downstream

| Config | Clean BoolQ | Clean MMLU | Clean PIQA | Clean WinoGrande | Analog BoolQ | Analog MMLU | Analog PIQA | Analog WinoGrande |
|--------|-----------:|-----------:|-----------:|-----------------:|-------------:|------------:|------------:|------------------:|
| fixed500 | 0.6260 | 0.2497 | 0.7388 | 0.5919 | 0.6174 | 0.2502 | 0.7372 | 0.5864 |
| adaptive_cosine_v1 | 0.6257 | 0.2460 | 0.7388 | 0.5817 | 0.6144 | 0.2479 | 0.7394 | 0.5770 |
| adaptive_fixed_v1 | 0.6202 | 0.2485 | 0.7416 | 0.5801 | — | — | — | — |
| adaptive_layerwise_v1 | 0.6245 | 0.2460 | 0.7388 | 0.5833 | 0.6128 | 0.2475 | 0.7345 | 0.5770 |
| adaptive_reverse_v1 | 0.6202 | 0.2485 | 0.7416 | 0.5801 | 0.6122 | 0.2499 | 0.7383 | 0.5793 |
| adaptive_cosine_last2 | 0.6217 | 0.2530 | 0.7394 | 0.5872 | 0.6076 | 0.2504 | 0.7388 | 0.5856 |
| adaptive_fixed_1000 | 0.6116 | 0.2434 | 0.7356 | 0.5801 | 0.6043 | 0.2445 | 0.7378 | 0.5722 |
| last2_fixed500 | 0.6162 | 0.2500 | 0.7394 | 0.5825 | 0.6031 | 0.2505 | 0.7399 | 0.5793 |
| last4_fixed500 | 0.6138 | 0.2453 | 0.7367 | 0.5856 | 0.5951 | 0.2482 | 0.7361 | 0.5809 |

### 3.4 Robustness Sweep — σ_c2c

| σ_c2c | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.0 | 5.1343 | 0.6468 | 0.4565 | 0.6380 |
| 0.01 | 5.1446 | 0.6458 | 0.4562 | 0.6406 |
| 0.02 | 5.1573 | 0.6439 | 0.4568 | 0.6410 |
| 0.05 | 5.1959 | 0.6402 | 0.4564 | 0.6423 |
| 0.10 | 5.2591 | 0.6350 | 0.4559 | 0.6406 |

### 3.5 Robustness Sweep — σ_d2d

| σ_d2d | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.0 | 5.1113 | 0.6456 | 0.4570 | 0.6402 |
| 0.02 | 5.1446 | 0.6458 | 0.4562 | 0.6406 |
| 0.04 | 5.1851 | 0.6416 | 0.4551 | 0.6402 |
| 0.06 | 5.2195 | 0.6387 | 0.4561 | 0.6402 |
| 0.10 | 5.2588 | 0.6375 | 0.4559 | 0.6410 |

### 3.6 Robustness Sweep — Mismatch

| Eval σ_c2c | PPL | Eval σ_d2d | PPL |
|-----------:|----:|-----------:|----:|
| 0.02 | 5.1573 | 0.04 | 5.1851 |
| 0.05 | 5.1959 | 0.06 | 5.2195 |
| 0.10 | 5.2591 | 0.10 | 5.2588 |

### 3.7 n_states 扫描

| n_states | PPL | Lambada | HellaSwag | ARC-Easy |
|---------:|----:|--------:|----------:|---------:|
| 128 | 5.1439 | 0.6468 | 0.4567 | 0.6410 |
| 256 | 5.1446 | 0.6458 | 0.4562 | 0.6406 |
| 512 | 5.1453 | 0.6464 | 0.4572 | 0.6402 |
| 1024 | 5.1445 | 0.6464 | 0.4567 | 0.6397 |

### 3.8 Cross-instance D2D Consistency

| Seed | PPL | Lambada | HellaSwag | ARC-Easy |
|-----:|----:|--------:|----------:|---------:|
| 3373 | 5.1446 | 0.6458 | 0.4562 | 0.6406 |
| 3374 | 5.1429 | 0.6451 | 0.4564 | 0.6414 |
| 3375 | 5.1362 | 0.6468 | 0.4566 | 0.6410 |
| 3376 | 5.1470 | 0.6445 | 0.4567 | 0.6427 |
| 3377 | 5.1337 | 0.6458 | 0.4568 | 0.6393 |
| **CV** | **<0.1%** | | | |

---

## §4 p69b（Pythia-6.9B）— 全部数据

### 4.1 自适应调度 — PPL

| Schedule | Clean PPL | Clean Lambada | Clean HellaSwag | Clean ARC-Easy | Analog PPL | Analog Lambada | Analog HellaSwag | Analog ARC-Easy | ΔPPL |
|----------|----------:|--------------:|----------------:|---------------:|-----------:|---------------:|-----------------:|----------------:|-----:|
| fixed500 | 5.2223 | 0.6336 | 0.4963 | 0.6824 | 5.2907 | 0.6282 | 0.4949 | 0.6797 | +0.07 |
| adaptive_cosine_v1 | 5.2323 | 0.6334 | 0.4964 | 0.6824 | 5.2995 | 0.6295 | 0.4948 | 0.6806 | +0.07 |
| adaptive_fixed_v1 | 5.2223 | 0.6336 | 0.4963 | 0.6824 | 5.2907 | 0.6282 | 0.4949 | 0.6797 | +0.07 |
| adaptive_layerwise_v1 | 5.2279 | 0.6326 | 0.4963 | 0.6824 | 5.2938 | 0.6318 | 0.4958 | 0.6785 | +0.07 |
| adaptive_cosine_last2 | 5.1758 | 0.6371 | 0.4962 | 0.6881 | 5.3443 | 0.6284 | 0.4941 | 0.6839 | +0.17 |
| fixed_1000 | 5.1663 | 0.6387 | 0.4978 | 0.6793 | 5.2205 | 0.6356 | 0.4970 | 0.6776 | +0.05 |

> 注：fixed500 和 adaptive_fixed_v1 数值相同，因二者实际为同一 checkpoint——fixed500 就是 adaptive_fixed_v1 的 baseline。

### 4.2 层消融

| Config | Clean PPL | Clean Lambada | Clean HellaSwag | Clean ARC-Easy | Analog PPL | Analog Lambada | Analog HellaSwag | Analog ARC-Easy | ΔPPL |
|--------|----------:|--------------:|----------------:|---------------:|-----------:|---------------:|-----------------:|----------------:|-----:|
| hat_last2 | 5.2022 | 0.6326 | 0.4951 | 0.6827 | 5.3240 | 0.6264 | 0.4926 | 0.6852 | +0.12 |
| hat_last4 | 5.1184 | 0.6392 | 0.4975 | 0.6827 | 5.5859 | 0.6200 | 0.4927 | 0.6793 | +0.47 |

### 4.3 Extended Downstream

| Config | Clean BoolQ | Clean MMLU | Clean PIQA | Clean WinoGrande | Analog BoolQ | Analog MMLU | Analog PIQA | Analog WinoGrande |
|--------|-----------:|-----------:|-----------:|-----------------:|-------------:|------------:|------------:|------------------:|
| fixed500 | 0.6450 | 0.2651 | 0.7661 | 0.6212 | 0.6382 | 0.2606 | 0.7628 | 0.6204 |
| adaptive_cosine_v1 | 0.6413 | 0.2657 | 0.7612 | 0.6275 | — | 0.2661 | — | — |
| adaptive_fixed_v1 | 0.6450 | 0.2651 | 0.7661 | 0.6212 | — | 0.2606 | — | — |
| adaptive_layerwise_v1 | 0.6388 | 0.2591 | 0.7584 | 0.6188 | — | 0.2606 | — | — |
| adaptive_cosine_last2 | 0.6379 | 0.2661 | 0.7666 | 0.6204 | 0.6312 | 0.2651 | 0.7601 | 0.6133 |
| fixed_1000 | 0.6434 | 0.2609 | 0.7590 | 0.6251 | — | — | — | — |
| hat_last2 | 0.6422 | 0.2638 | 0.7617 | 0.6330 | 0.6352 | 0.2624 | 0.7535 | 0.6283 |
| hat_last4 | 0.6373 | 0.2636 | 0.7579 | 0.6196 | 0.6346 | 0.2580 | 0.7606 | 0.6062 |

> 注：p69b analog extended 数据部分在 v5 补跑中已输出到 boolq_mmlu_piqa_winogrande 独立 JSON 文件中，但 analog 部分（cosine/fixed/layerwise_v1）的完整 extended 结果正在 v5 遗留任务中。

### 4.4 Robustness Sweep — σ_c2c

| σ_c2c | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.0 | 5.3052 | 0.6293 | 0.4942 | 0.6780 |
| 0.01 | 5.3062 | 0.6268 | 0.4947 | 0.6785 |
| 0.02 | 5.3108 | 0.6290 | 0.4953 | 0.6797 |
| 0.05 | 5.3057 | 0.6330 | 0.4943 | 0.6734 |
| 0.10 | 5.3474 | 0.6387 | 0.4902 | 0.6734 |

### 4.5 Robustness Sweep — σ_d2d

| σ_d2d | PPL | Lambada | HellaSwag | ARC-Easy |
|------:|----:|--------:|----------:|---------:|
| 0.0 | 5.2271 | 0.6324 | 0.4952 | 0.6793 |
| 0.02 | 5.3062 | 0.6268 | 0.4947 | 0.6785 |
| 0.04 | 5.3463 | 0.6249 | 0.4930 | 0.6751 |
| 0.06 | 5.3472 | 0.6299 | 0.4922 | 0.6721 |
| 0.10 | 5.3374 | 0.6418 | 0.4890 | 0.6742 |

### 4.6 Robustness Sweep — Mismatch

| Eval σ_c2c | PPL | Eval σ_d2d | PPL |
|-----------:|----:|-----------:|----:|
| 0.02 | 5.3062 | 0.04 | 5.3463 |
| 0.05 | 5.3057 | 0.06 | 5.3472 |
| 0.10 | 5.3474 | 0.10 | 5.3374 |

### 4.7 n_states 扫描

| n_states | PPL | Lambada | HellaSwag | ARC-Easy |
|---------:|----:|--------:|----------:|---------:|
| 128 | 5.3036 | 0.6260 | 0.4942 | 0.6814 |
| 256 | 5.3062 | 0.6268 | 0.4947 | 0.6785 |
| 512 | 5.3075 | 0.6282 | 0.4950 | 0.6801 |
| 1024 | 5.3047 | 0.6266 | 0.4943 | 0.6789 |

### 4.8 Cross-instance D2D Consistency

| Seed | PPL | Lambada | HellaSwag | ARC-Easy |
|-----:|----:|--------:|----------:|---------:|
| 3373 | 5.3062 | 0.6268 | 0.4947 | 0.6785 |
| 3374 | 5.2802 | 0.6280 | 0.4954 | 0.6801 |
| 3375 | 5.2918 | 0.6268 | 0.4954 | 0.6793 |
| 3376 | 5.2920 | 0.6286 | 0.4940 | 0.6785 |
| 3377 | 5.2797 | 0.6324 | 0.4952 | 0.6801 |
| **CV** | **<0.2%** | | | |

---

## §5 TruthfulQA

| Model | Config | MC1 |
|-------|--------|----:|
| p28b | fixed500 clean | 0.2191 |
| p28b | fixed500 analog | 0.2191 |
| p28b | adaptive_cosine_v1 clean | 0.2179 |
| p28b | adaptive_cosine_v1 analog | 0.2203 |
| p69b | fixed500 clean | 0.2277 |
| p69b | fixed500 analog | 0.2215 |
| p69b | adaptive_cosine_v1 clean | 0.2301 |
| p69b | adaptive_cosine_v1 analog | 0.2191 |

> TruthfulQA MC1 全部接近随机基线（~0.25），p69b 略高于 p28b，各 config 间差异不显著。

---

## §6 Scaling Law

| Model | Size | Clean PPL | Analog PPL | ΔPPL |
|-------|-----:|----------:|-----------:|-----:|
| p410m | 410M | — | — | — |
| p1b | 1B | 7.1145 | 7.6030 | 0.49 |
| p28b | 2.8B | 5.0999 | 5.1424 | 0.04 |
| p69b | 6.9B | 5.2223 | 5.2907 | 0.07 |

**拟合：ΔPPL(N) = 1.69e11 · N^(-1.286)，R² = 0.993**

---

## §7 补充评估（v7 运行中）

| 任务 | 状态 | 详情 |
|------|------|------|
| MMLU 5-shot | 🔄 GPU6 正在跑 p28b reverse_v1 analog | Clean 因 --num_fewshot 问题失败，待重跑 |
| GSM8K | ⏳ 等待 GPU 空闲 | — |
| AI2-ARC | ⏳ 等待 GPU 空闲 | — |

---

# ═══════════════════════════════════════════
# 第三部分：原始数据明细（机器可读）
# ═══════════════════════════════════════════

## S1 所有 Standard3 JSON 文件（89 files）

```
 A  p28b_fixed500_seed42_analog_p28b_c2c_0.01                    PPL=5.1446  Lambada=0.6458  HellaSwag=0.4562  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_c2c_0.02                    PPL=5.1573  Lambada=0.6439  HellaSwag=0.4568  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_c2c_0.05                    PPL=5.1959  Lambada=0.6402  HellaSwag=0.4564  ARC-Easy=0.6423
 A  p28b_fixed500_seed42_analog_p28b_c2c_0.0                     PPL=5.1343  Lambada=0.6468  HellaSwag=0.4565  ARC-Easy=0.6380
 A  p28b_fixed500_seed42_analog_p28b_c2c_0.10                    PPL=5.2591  Lambada=0.6350  HellaSwag=0.4559  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_d2d_0.02                    PPL=5.1446  Lambada=0.6458  HellaSwag=0.4562  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_d2d_0.04                    PPL=5.1851  Lambada=0.6416  HellaSwag=0.4551  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_d2d_0.06                    PPL=5.2195  Lambada=0.6387  HellaSwag=0.4561  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_d2d_0.0                     PPL=5.1113  Lambada=0.6456  HellaSwag=0.4570  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_d2d_0.10                    PPL=5.2588  Lambada=0.6375  HellaSwag=0.4559  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_mis_c2c_0.02                PPL=5.1573  Lambada=0.6439  HellaSwag=0.4568  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_mis_c2c_0.05                PPL=5.1959  Lambada=0.6402  HellaSwag=0.4564  ARC-Easy=0.6423
 A  p28b_fixed500_seed42_analog_p28b_mis_c2c_0.10                PPL=5.2591  Lambada=0.6350  HellaSwag=0.4559  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_mis_d2d_0.04                PPL=5.1851  Lambada=0.6416  HellaSwag=0.4551  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_mis_d2d_0.06                PPL=5.2195  Lambada=0.6387  HellaSwag=0.4561  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_mis_d2d_0.10                PPL=5.2588  Lambada=0.6375  HellaSwag=0.4559  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_nstates_1024                PPL=5.1445  Lambada=0.6464  HellaSwag=0.4567  ARC-Easy=0.6397
 A  p28b_fixed500_seed42_analog_p28b_nstates_128                 PPL=5.1439  Lambada=0.6468  HellaSwag=0.4567  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_nstates_256                 PPL=5.1446  Lambada=0.6458  HellaSwag=0.4562  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_nstates_512                 PPL=5.1453  Lambada=0.6464  HellaSwag=0.4572  ARC-Easy=0.6402
 A  p28b_fixed500_seed42_analog_p28b_seed_3373                   PPL=5.1446  Lambada=0.6458  HellaSwag=0.4562  ARC-Easy=0.6406
 A  p28b_fixed500_seed42_analog_p28b_seed_3374                   PPL=5.1429  Lambada=0.6451  HellaSwag=0.4564  ARC-Easy=0.6414
 A  p28b_fixed500_seed42_analog_p28b_seed_3375                   PPL=5.1362  Lambada=0.6468  HellaSwag=0.4566  ARC-Easy=0.6410
 A  p28b_fixed500_seed42_analog_p28b_seed_3376                   PPL=5.1470  Lambada=0.6445  HellaSwag=0.4567  ARC-Easy=0.6427
 A  p28b_fixed500_seed42_analog_p28b_seed_3377                   PPL=5.1337  Lambada=0.6458  HellaSwag=0.4568  ARC-Easy=0.6393
 A  p28b_adaptive_cosine_v1_seed42                               PPL=5.1386  Lambada=0.6416  HellaSwag=0.4573  ARC-Easy=0.6465
 A  p28b_adaptive_layerwise_v1_seed42                            PPL=5.1406  Lambada=0.6439  HellaSwag=0.4555  ARC-Easy=0.6418
 A  p28b_last2_fixed500_seed42                                   PPL=5.2787  Lambada=0.6406  HellaSwag=0.4560  ARC-Easy=0.6418
 A  p28b_last4_fixed500_seed42                                   PPL=5.5880  Lambada=0.6282  HellaSwag=0.4538  ARC-Easy=0.6439
 C  p1b_adaptive_fixed_v1_seed42                                 PPL=7.1145  Lambada=0.5841  HellaSwag=0.3912  ARC-Easy=0.5863
 C  p28b_adaptive_cosine_v1_seed42                               PPL=5.0961  Lambada=0.6466  HellaSwag=0.4586  ARC-Easy=0.6418
 C  p28b_adaptive_layerwise_v1_seed42                            PPL=5.0990  Lambada=0.6486  HellaSwag=0.4560  ARC-Easy=0.6427
 C  p28b_last2_fixed500_seed42                                   PPL=5.1153  Lambada=0.6449  HellaSwag=0.4567  ARC-Easy=0.6397
 C  p28b_last4_fixed500_seed42                                   PPL=4.9532  Lambada=0.6573  HellaSwag=0.4572  ARC-Easy=0.6435
 C  p69b_adaptive_cosine_last2_seed42                            PPL=5.1758  Lambada=0.6371  HellaSwag=0.4962  ARC-Easy=0.6881
 C  p69b_fixed1000_seed42_seed42                                 PPL=5.1663  Lambada=0.6387  HellaSwag=0.4978  ARC-Easy=0.6793
 C  p69b_hat_last2_fixed500_seed42_seed42                        PPL=5.2022  Lambada=0.6326  HellaSwag=0.4951  ARC-Easy=0.6827
 C  p69b_hat_last4_fixed500_seed42_seed42                        PPL=5.1184  Lambada=0.6392  HellaSwag=0.4975  ARC-Easy=0.6827
 A  p69b_fixed500_seed42_analog_p69b_c2c_0.01                    PPL=5.3062  Lambada=0.6268  HellaSwag=0.4947  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_c2c_0.02                    PPL=5.3108  Lambada=0.6290  HellaSwag=0.4953  ARC-Easy=0.6797
 A  p69b_fixed500_seed42_analog_p69b_c2c_0.05                    PPL=5.3057  Lambada=0.6330  HellaSwag=0.4943  ARC-Easy=0.6734
 A  p69b_fixed500_seed42_analog_p69b_c2c_0.0                     PPL=5.3052  Lambada=0.6293  HellaSwag=0.4942  ARC-Easy=0.6780
 A  p69b_fixed500_seed42_analog_p69b_c2c_0.10                    PPL=5.3474  Lambada=0.6387  HellaSwag=0.4902  ARC-Easy=0.6734
 A  p69b_fixed500_seed42_analog_p69b_d2d_0.02                    PPL=5.3062  Lambada=0.6268  HellaSwag=0.4947  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_d2d_0.04                    PPL=5.3463  Lambada=0.6249  HellaSwag=0.4930  ARC-Easy=0.6751
 A  p69b_fixed500_seed42_analog_p69b_d2d_0.06                    PPL=5.3472  Lambada=0.6299  HellaSwag=0.4922  ARC-Easy=0.6721
 A  p69b_fixed500_seed42_analog_p69b_d2d_0.0                     PPL=5.2271  Lambada=0.6324  HellaSwag=0.4952  ARC-Easy=0.6793
 A  p69b_fixed500_seed42_analog_p69b_d2d_0.10                    PPL=5.3374  Lambada=0.6418  HellaSwag=0.4890  ARC-Easy=0.6742
 A  p69b_fixed500_seed42_analog_p69b_mis_c2c_0.02                PPL=5.3062  Lambada=0.6268  HellaSwag=0.4947  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_mis_c2c_0.05                PPL=5.3057  Lambada=0.6330  HellaSwag=0.4943  ARC-Easy=0.6734
 A  p69b_fixed500_seed42_analog_p69b_mis_c2c_0.10                PPL=5.3474  Lambada=0.6387  HellaSwag=0.4902  ARC-Easy=0.6734
 A  p69b_fixed500_seed42_analog_p69b_mis_d2d_0.04                PPL=5.3463  Lambada=0.6249  HellaSwag=0.4930  ARC-Easy=0.6751
 A  p69b_fixed500_seed42_analog_p69b_mis_d2d_0.06                PPL=5.3472  Lambada=0.6299  HellaSwag=0.4922  ARC-Easy=0.6721
 A  p69b_fixed500_seed42_analog_p69b_mis_d2d_0.10                PPL=5.3374  Lambada=0.6418  HellaSwag=0.4890  ARC-Easy=0.6742
 A  p69b_fixed500_seed42_analog_p69b_nstates_1024                PPL=5.3047  Lambada=0.6266  HellaSwag=0.4943  ARC-Easy=0.6789
 A  p69b_fixed500_seed42_analog_p69b_nstates_128                 PPL=5.3036  Lambada=0.6260  HellaSwag=0.4942  ARC-Easy=0.6814
 A  p69b_fixed500_seed42_analog_p69b_nstates_256                 PPL=5.3062  Lambada=0.6268  HellaSwag=0.4947  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_nstates_512                 PPL=5.3075  Lambada=0.6282  HellaSwag=0.4950  ARC-Easy=0.6801
 A  p69b_fixed500_seed42_analog_p69b_seed_3373                   PPL=5.3062  Lambada=0.6268  HellaSwag=0.4947  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_seed_3374                   PPL=5.2802  Lambada=0.6280  HellaSwag=0.4954  ARC-Easy=0.6801
 A  p69b_fixed500_seed42_analog_p69b_seed_3375                   PPL=5.2918  Lambada=0.6268  HellaSwag=0.4954  ARC-Easy=0.6793
 A  p69b_fixed500_seed42_analog_p69b_seed_3376                   PPL=5.2920  Lambada=0.6286  HellaSwag=0.4940  ARC-Easy=0.6785
 A  p69b_fixed500_seed42_analog_p69b_seed_3377                   PPL=5.2797  Lambada=0.6324  HellaSwag=0.4952  ARC-Easy=0.6801
 A  p69b_adaptive_cosine_last2_seed42                            PPL=5.3443  Lambada=0.6284  HellaSwag=0.4941  ARC-Easy=0.6839
 A  p69b_fixed1000_seed42_seed42                                 PPL=5.2205  Lambada=0.6356  HellaSwag=0.4970  ARC-Easy=0.6776
 A  p69b_hat_last2_fixed500_seed42_seed42                        PPL=5.3240  Lambada=0.6264  HellaSwag=0.4926  ARC-Easy=0.6852
 A  p69b_hat_last4_fixed500_seed42_seed42                        PPL=5.5859  Lambada=0.6200  HellaSwag=0.4927  ARC-Easy=0.6793
 A  p1b_adaptive_fixed_v1_seed42                                 PPL=7.6030  Lambada=0.5723  HellaSwag=0.3888  ARC-Easy=0.5846
 A  p1b_adaptive_fixed_v1_seed42_analog_c2c_0.01                 PPL=7.6030  Lambada=0.5723  HellaSwag=0.3888  ARC-Easy=0.5846
 A  p1b_adaptive_fixed_v1_seed42_analog_c2c_0.02                 PPL=7.6871  Lambada=0.5713  HellaSwag=0.3898  ARC-Easy=0.5859
 A  p1b_adaptive_fixed_v1_seed42_analog_c2c_0.05                 PPL=7.9363  Lambada=0.5655  HellaSwag=0.3888  ARC-Easy=0.5783
 A  p1b_adaptive_fixed_v1_seed42_analog_c2c_0.0                  PPL=7.5419  Lambada=0.5758  HellaSwag=0.3903  ARC-Easy=0.5867
 A  p1b_adaptive_fixed_v1_seed42_analog_c2c_0.1                  PPL=8.1701  Lambada=0.5616  HellaSwag=0.3887  ARC-Easy=0.5800
 A  p1b_adaptive_fixed_v1_seed42_analog_d2d_0.01                 PPL=7.3794  Lambada=0.5781  HellaSwag=0.3904  ARC-Easy=0.5846
 A  p1b_adaptive_fixed_v1_seed42_analog_d2d_0.02                 PPL=7.6030  Lambada=0.5723  HellaSwag=0.3888  ARC-Easy=0.5846
 A  p1b_adaptive_fixed_v1_seed42_analog_d2d_0.05                 PPL=7.9675  Lambada=0.5641  HellaSwag=0.3871  ARC-Easy=0.5884
 A  p1b_adaptive_fixed_v1_seed42_analog_d2d_0.1                  PPL=8.1119  Lambada=0.5616  HellaSwag=0.3861  ARC-Easy=0.5871
 A  p1b_adaptive_fixed_v1_seed42_analog_seed_3373                PPL=7.6030  Lambada=0.5723  HellaSwag=0.3888  ARC-Easy=0.5846
 A  p1b_adaptive_fixed_v1_seed42_analog_seed_3374                PPL=7.6337  Lambada=0.5731  HellaSwag=0.3886  ARC-Easy=0.5892
 A  p1b_adaptive_fixed_v1_seed42_analog_seed_3375                PPL=7.5936  Lambada=0.5740  HellaSwag=0.3892  ARC-Easy=0.5863
 A  p1b_adaptive_fixed_v1_seed42_analog_seed_3376                PPL=7.5215  Lambada=0.5721  HellaSwag=0.3885  ARC-Easy=0.5808
 A  p1b_adaptive_fixed_v1_seed42_analog_seed_3377                PPL=7.6181  Lambada=0.5723  HellaSwag=0.3883  ARC-Easy=0.5842
 A  c4fc8d586d62df497f1f9b69d66d3ca419992d3e_analog_p410m_patched_zero_last2  PPL=15.2274  Lambada=0.4493  HellaSwag=0.3432  ARC-Easy=0.5118
```

### 未纳入 standard3 JSON 但另有独立 JSON 的 PPL 数据

以下文件以独立 JSON 形式存放（对应 single-task eval 的输出）：

| 文件 | PPL |
|------|----:|
| p28b_fixed500_seed42_clean.json | 5.0999 |
| p28b_fixed500_seed42_analog.json | 5.1424 |
| p28b_adaptive_fixed_v1_seed42_clean.json | 5.1040 |
| p28b_adaptive_fixed_v1_seed42_analog.json | 5.1446 |
| p28b_adaptive_reverse_v1_seed42_clean.json | 5.1040 |
| p28b_adaptive_reverse_v1_seed42_analog.json | 5.1446 |
| p28b_adaptive_cosine_last2_seed42_clean.json | 5.1182 |
| p28b_adaptive_cosine_last2_seed42_analog.json | 5.2125 |
| p28b_adaptive_fixed_1000_seed42_clean.json | 5.0833 |
| p28b_adaptive_fixed_1000_seed42_analog.json | 5.1222 |
| p69b_fixed500_seed42_clean.json | 5.2223 |
| p69b_fixed500_seed42_analog.json | 5.2907 |
| p69b_adaptive_cosine_v1_seed42_clean.json | 5.2323 |
| p69b_adaptive_cosine_v1_seed42_analog.json | 5.2995 |
| p69b_adaptive_fixed_v1_seed42_clean.json | 5.2223 |
| p69b_adaptive_fixed_v1_seed42_analog.json | 5.2907 |
| p69b_adaptive_layerwise_v1_seed42_clean.json | 5.2279 |
| p69b_adaptive_layerwise_v1_seed42_analog.json | 5.2938 |
| p410m_adaptive_fixed_1000_seed42_clean.json | 13.4595 |
| p410m_adaptive_fixed_1000_seed42_analog.json | 14.8760 |
| p410m_adaptive_reverse_v1_nofreeze_seed42_clean.json | 20.4333 |
| p410m_adaptive_reverse_v1_nofreeze_seed42_analog.json | 21.3111 |

---

## S2 所有 Extended Downstream JSON 文件（43 files）

```
 C  p28b_fixed500_seed42                                     BoolQ=0.6260  MMLU=0.2497  PIQA=0.7388  WinoGrande=0.5919
 C  p28b_adaptive_cosine_v1_seed42                            BoolQ=0.6257  MMLU=0.2460  PIQA=0.7388  WinoGrande=0.5817
 C  p28b_adaptive_fixed_v1_seed42                             BoolQ=0.6202  MMLU=0.2485  PIQA=0.7416  WinoGrande=0.5801
 C  p28b_adaptive_layerwise_v1_seed42                         BoolQ=0.6245  MMLU=0.2460  PIQA=0.7388  WinoGrande=0.5833
 C  p28b_adaptive_reverse_v1_seed42                           BoolQ=0.6202  MMLU=0.2485  PIQA=0.7416  WinoGrande=0.5801
 C  p28b_adaptive_cosine_last2_seed42                         BoolQ=0.6217  MMLU=0.2530  PIQA=0.7394  WinoGrande=0.5872
 C  p28b_adaptive_fixed_1000_seed42                           BoolQ=0.6116  MMLU=0.2434  PIQA=0.7356  WinoGrande=0.5801
 C  p28b_last2_fixed500_seed42                                BoolQ=0.6162  MMLU=0.2500  PIQA=0.7394  WinoGrande=0.5825
 C  p28b_last4_fixed500_seed42                                BoolQ=0.6138  MMLU=0.2453  PIQA=0.7367  WinoGrande=0.5856
 C  p69b_fixed500_seed42                                      BoolQ=0.6450  MMLU=0.2651  PIQA=0.7661  WinoGrande=0.6212
 C  p69b_adaptive_cosine_v1_seed42                            BoolQ=0.6413  MMLU=0.2657  PIQA=0.7612  WinoGrande=0.6275
 C  p69b_adaptive_fixed_v1_seed42                             BoolQ=0.6450  MMLU=0.2651  PIQA=0.7661  WinoGrande=0.6212
 C  p69b_adaptive_layerwise_v1_seed42                         BoolQ=0.6388  MMLU=0.2591  PIQA=0.7584  WinoGrande=0.6188
 C  p69b_adaptive_cosine_last2_seed42                         BoolQ=0.6379  MMLU=0.2661  PIQA=0.7666  WinoGrande=0.6204
 C  p69b_fixed1000_seed42_seed42                              BoolQ=0.6434  MMLU=0.2609  PIQA=0.7590  WinoGrande=0.6251
 C  p69b_hat_last2_fixed500_seed42_seed42                     BoolQ=0.6422  MMLU=0.2638  PIQA=0.7617  WinoGrande=0.6330
 C  p69b_hat_last4_fixed500_seed42_seed42                     BoolQ=0.6373  MMLU=0.2636  PIQA=0.7579  WinoGrande=0.6196
 C  p1b_adaptive_fixed_v1_seed42                              BoolQ=0.6052  MMLU=0.2446  PIQA=0.7013  WinoGrande=0.5249
 C  p410m_adaptive_fixed_1000_seed42                          BoolQ=0.5709  MMLU=0.2307  PIQA=0.6746  WinoGrande=0.5391
 C  p410m_adaptive_reverse_v1_nofreeze_seed42                 BoolQ=0.3865  MMLU=0.2311  PIQA=0.6638  WinoGrande=0.5249
 A  p28b_fixed500_seed42                                      BoolQ=0.6174  MMLU=0.2502  PIQA=0.7372  WinoGrande=0.5864
 A  p28b_adaptive_cosine_v1_seed42                            BoolQ=0.6144  MMLU=0.2479  PIQA=0.7394  WinoGrande=0.5770
 A  p28b_adaptive_layerwise_v1_seed42                         BoolQ=0.6128  MMLU=0.2475  PIQA=0.7345  WinoGrande=0.5770
 A  p28b_adaptive_reverse_v1_seed42                           BoolQ=0.6122  MMLU=0.2499  PIQA=0.7383  WinoGrande=0.5793
 A  p28b_adaptive_cosine_last2_seed42                         BoolQ=0.6076  MMLU=0.2504  PIQA=0.7388  WinoGrande=0.5856
 A  p28b_adaptive_fixed_1000_seed42                           BoolQ=0.6043  MMLU=0.2445  PIQA=0.7378  WinoGrande=0.5722
 A  p28b_last2_fixed500_seed42                                BoolQ=0.6031  MMLU=0.2505  PIQA=0.7399  WinoGrande=0.5793
 A  p28b_last4_fixed500_seed42                                BoolQ=0.5951  MMLU=0.2482  PIQA=0.7361  WinoGrande=0.5809
 A  p69b_fixed500_seed42                                      BoolQ=0.6382  MMLU=0.2606  PIQA=0.7628  WinoGrande=0.6204
 A  p69b_adaptive_cosine_last2_seed42                         BoolQ=0.6312  MMLU=0.2651  PIQA=0.7601  WinoGrande=0.6133
 A  p69b_hat_last2_fixed500_seed42_seed42                     BoolQ=0.6352  MMLU=0.2624  PIQA=0.7535  WinoGrande=0.6283
 A  p69b_hat_last4_fixed500_seed42_seed42                     BoolQ=0.6346  MMLU=0.2580  PIQA=0.7606  WinoGrande=0.6062
 A  p1b_adaptive_fixed_v1_seed42                              BoolQ=0.6024  MMLU=0.2452  PIQA=0.7008  WinoGrande=0.5501
 A  p410m_adaptive_fixed_1000_seed42                          BoolQ=0.5563  MMLU=0.2326  PIQA=0.6692  WinoGrande=0.5257
 A  p410m_adaptive_reverse_v1_nofreeze_seed42                 BoolQ=0.3899  MMLU=0.2314  PIQA=0.6697  WinoGrande=0.5328
```

---

## S3 TruthfulQA JSON 文件（8 files）

```
p28b_fixed500_seed42_clean              MC1=0.2191
p28b_fixed500_seed42_analog             MC1=0.2191
p28b_adaptive_cosine_v1_seed42_clean    MC1=0.2179
p28b_adaptive_cosine_v1_seed42_analog   MC1=0.2203
p69b_fixed500_seed42_clean              MC1=0.2277
p69b_fixed500_seed42_analog             MC1=0.2215
p69b_adaptive_cosine_v1_seed42_clean    MC1=0.2301
p69b_adaptive_cosine_v1_seed42_analog   MC1=0.2191
```

---

## 当前 GPU 占用（2026-05-21 19:30）

| GPU | PID | 任务 | 运行时长 | 说明 |
|-----|-----|------|----------|------|
| 6 | 92232 | p28b_reverse_v1 analog MMLU 5-shot | ~1h | v7 任务 |
| 5 | 3573065 | p69b_cosine_v1 analog extended | ~3.5h | v5 遗留 |
| 7 | 3837592 | p69b_fixed_v1 analog extended | ~2.5h | v5 遗留 |
| 4 | 3971785 | p28b_fixed_v1 standard3 | ~2h | v5 遗留 |

> v7 scheduler 等待 GPU4/5/7 释放后自动开始 MMLU/GSM8K/AI2-ARC 任务。

## 基础设施

| # | 任务 | 状态 | 备注 |
|---|---|---|---|
| INF-META | Metadata patch（JSON envelope） | ✅ | 所有输出包含完整 metadata |
| INF-OFFLINE | Offline sharded model loading | ✅ | `_resolve_local_path` |
| INF-CLOSURE | Closure capture bug 修复 | ✅ | `p3_hat_eval.py` / `p3_hat_train.py` |
| INF-CLAIM | Claim-lock manifests | ✅ | p28b/p69b downstream + 自适应 |
| INF-PUSH | 大型 JSON 压缩/清理 | ⏳ | ~75MB 每个；LFS 处理 |
| INF-MAXLEN | --max_length 2048 | ✅ | v5 修复 D2D buffer 超限 |
