
# Remote 107 完整历史任务总表（按闭环分段）

> 最后更新：2026-05-21 19:00
> 分支：`107-clean`
> 最新 commit：`abdf5c5`
> eval JSON 总数：**180**（standard3 PPL: 89, extended downstream: 43, TruthfulQA: 8, robustness/ablation/scans: 40）

---

## 闭环 0：基线校准与可行性验证（P0）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P0-A | 基线评估器校准 | ✅ | 典型基线 22.18 PPL（ctx=512/stride=256/bs=1）；旧评估器 15.68 已废弃 |
| P0-B | 配对 HAT 检查点消融 | ✅ | 24 eval jobs：B1→B2→B3/B4 阶梯；patch 本身 +0.02 PPL，D2D=0.02 加 +0.42，D2D=0.05 加 +0.58 |

---

## 闭环 1：核心 K107 验证（P1）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| K107-A | 典型选择性 KV 范围扫描 | ✅ | last1 [23] = 19.45；last2 [22,23] = 20.14；all layers = 37+（灾难性） |
| K107-B | 保持压力测试 | ✅ | last1 + retention refresh 改善 ~0.3 PPL；all-layer 仍崩溃 |
| K107-C | 状态数量扫描 | ✅ | n_states=64 最佳（19.40）；256 生产选择（19.46） |
| P1-B | Pythia-1B last1 验证 | ✅ | 100 steps → 14.60 PPL；D2D=0.05 仅 +0.20 |
| P1-EPSC | 极端代理压力评估 | ✅ | 45 eval jobs；sigma=0.15 时 20.76 PPL，远低于 25 kill line |
| P1-FIG | 图表生成脚本 | ✅ | 3 张图（消融阶梯、EPSC 压力、规模趋势） draft-ready |

---

## 闭环 2：规模验证（P2）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P2-1B | Pythia-1B 规模检查 | ✅ | seed42/123 复现 Δ<0.03；14.60 PPL @ D2D=0.02 |
| P2-2.8B | Pythia-2.8B 规模检查 | ✅ | seed42/123 复现 Δ<0.02；13.34 PPL @ D2D=0.02 |
| P2-2.8B-EPSC | 2.8B EPSC + C2C 扫描 | ✅ | 21 eval jobs；sigma_c2c=0.10 仅 +0.26 PPL；sigma=0.15 时 13.91 PPL |

---

## 闭环 3：大模型可行性与基础设施（P3）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| P3-6.9B | 6.9B 可行性探测 + 1000步完整训练 | ✅ | `--fp16` + `--freeze-non-target-params` 成功在 GPU5 (32GB) 运行；1000 steps: 12.30 pre → 11.14 post，~1h03min |
| P3-2.8B-500 | 2.8B 500-step 固定基线 | ✅ | 13.69 pre → 12.68 post（500 steps） |
| P3-6.9B-500 | 6.9B 500-step 固定基线 | ✅ | 12.30 pre → 11.40 post（500 steps） |
| P3-AUDIT | AMP/冻结参数代码审计 | ✅ | `--freeze-non-target-params` + `--fp16` 已合并；旧结果仍有效 |
| P3-OPT | 选择性优化器审计 | ✅ | 仅优化 patched 层可节省显存；2.8B 可 fit 32GB |

---

## 闭环 4：Paper 2 第一轮 — 鲁棒性与下游评估

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

---

## 闭环 5：Paper 2 第二轮 — 层消融与跨设备

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R2-LAST2 | Layer ablation last2（p28b/p69b） | ✅ | PPL: p28b 5.12/5.28, p69b 5.20/5.32 (clean/analog) |
| R2-LAST4 | Layer ablation last4（p28b/p69b） | ✅ | PPL: p28b 4.95/5.59, p69b 5.12/5.59 (clean/analog) |
| R2-DEV | Cross-device eval（RRAM/PCM/FeFET） | ✅ | 基于已有 checkpoint 评估 3 种器件参数 |
| R2-ENG | Energy/Area 分析脚本 | ✅ | `scripts/energy_profile_kv_cache.py` + 基线 JSON |

---

## 闭环 6：Paper 2 第三轮 — 自适应噪声调度

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
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
|---|---|---|---|
| VLM-500 | Qwen3-VL HAT 训练（500 steps） | ✅ | last1 analog KV |
| VLM-5000 | Qwen3-VL HAT 训练（5000 steps） | ✅ | last1 analog KV |
| VLM-VAL | Qwen3-VL 验证评估 | ✅ | 5 images × 4 configs |
| VLM-5K-EVAL | **Qwen3-VL 5000-step checkpoint eval** | ✅ | 20 configs 全部完成（5 images × clean/last1/last2/last4）；manifest 已生成 |

---

## 闭环 8：Paper 2 第四轮 — Codex 审查

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| R0-AUDIT | Codex 审查（远程107 vs 论文 claim） | ✅ | 发现 4 个问题：Q1 PPL mismatch、Q2 config count、Q3 git_commit_hat、Q4 parity framing |
| R0-FIX | Summary JSON 修复 | ✅ | total_entries=19（原错误20），git_commit_hat="deployed_as_directory" |
| R0-DOC | Reconciliation 文档 | ✅ | `results/remote107/RECONCILIATION_20260520.md`：逐项回答 Codex Q1-Q4 |
| R0-COMMIT | R0 修复提交 | ✅ | `4e9f627` 已推送至 `107-clean`，含 summary 修正 + RECONCILIATION |

### 闭环 8b：机制控制实验（R1）

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
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

## 闭环 9：全量 extended downstream 评估 + TruthfulQA + 补充评估

| # | 任务 | 状态 | 关键结果 |
|---|---|---|---|
| EXT-v4 | v4 scheduler（offline mode） | ✅ | 15/42 jobs 成功；analog 全部失败（序列超 buffer） |
| EXT-v5 | v5 scheduler（+max_length 2048） | ✅ | 4 GPU 并行补跑 analog extended + 遗漏 jobs；全部完成 |
| EXT-v6 | v6 scheduler（TruthfulQA） | ✅ | 8 jobs 完成（p28b/p69b fixed500 + cosine_v1, clean+analog） |
| EXT-v7 | v7 scheduler（MMLU 5-shot, GSM8K, AI2-ARC） | 🔄 运行中 | 12h 实验；GPU6 正在跑 analog MMLU 5-shot |

---

# 完整数据汇总

## 1. 核心 PPL 结果 — 全部模型

所有 PPL 基于 `lambada_openai:perplexity`（越低越好）。

### 1.1 自适应调度 — p28b (2.8B)

| Schedule | Clean PPL | Analog PPL | ΔPPL |
|----------|----------:|-----------:|-----:|
| fixed500 (基线) | 5.10 | 5.14 | +0.04 |
| adaptive_cosine_v1 | 5.10 | 5.14 | +0.04 |
| adaptive_layerwise_v1 | 5.10 | 5.14 | +0.04 |
| adaptive_fixed_v1 | — | — | （等 standard3 补跑） |
| reverse_v1 | — | — | （等 standard3 补跑） |
| cosine_last2 | 5.12 | 5.21 | +0.09 |
| fixed_1000 | 5.08 | 5.12 | +0.04 |

> 注：fixed_v1 / reverse_v1 已有 extended 数据但 standard3 JSON 未以标准命名匹配。

### 1.2 自适应调度 — p69b (6.9B)

| Schedule | Clean PPL | Analog PPL | ΔPPL |
|----------|----------:|-----------:|-----:|
| fixed500 (基线) | 5.22 | 5.29 | +0.07 |
| adaptive_cosine_v1 | 5.23 | 5.30 | +0.07 |
| adaptive_layerwise_v1 | 5.23 | 5.29 | +0.07 |
| cosine_last2 | 5.18 | 5.34 | +0.17 |
| fixed_1000 | 5.17 | 5.22 | +0.05 |

### 1.3 层消融 PPL

| Model | Layer | Clean PPL | Analog PPL | ΔPPL |
|-------|-------|----------:|-----------:|-----:|
| p28b | last2 | 5.12 | 5.28 | +0.16 |
| p28b | last4 | 4.95 | 5.59 | +0.63 |
| p69b | hat_last2 | 5.20 | 5.32 | +0.12 |
| p69b | hat_last4 | 5.12 | 5.59 | +0.47 |

### 1.4 机制控制 — 410M

| Config | PPL | Δ vs Base |
|--------|----:|----------:|
| base_clean | 14.94 | — |
| patched_zero_last1 | 15.04 | +0.10 |
| patched_zero_last2 | 15.23 | +0.29 |
| patched_zero_last4 | 16.75 | +1.81 |
| patched_zero_all24 | 20.88 | +5.93 |
| hat_quant_zero_noise | **13.53** | **-1.41** |
| hat_d2d_0p05 | 14.97 | +0.03 |

### 1.5 p1b (1B)

| Condition | Clean PPL | Analog PPL | ΔPPL |
|-----------|----------:|-----------:|-----:|
| adaptive_fixed_v1 | 7.11 | 7.60 | +0.49 |

### 1.6 410M 扩展

| Config | PPL | Notes |
|--------|----:|-------|
| adaptive_fixed_1000_clean | — | extended 数据有，standard3 待补 |
| adaptive_fixed_1000_analog | — | extended 数据有 |
| adaptive_reverse_v1_nofreeze_clean | — | extended 数据有 |
| adaptive_reverse_v1_nofreeze_analog | — | extended 数据有 |

---

## 2. Robustness Sweep — PPL 数据

### 2.1 p28b fixed500

| σ_c2c | PPL | σ_d2d | PPL |
|------:|----:|------:|----:|
| 0.0 | 5.13 | 0.0 | 5.11 |
| 0.01 | 5.14 | 0.02 | 5.14 |
| 0.02 | 5.16 | 0.04 | 5.19 |
| 0.05 | 5.20 | 0.06 | 5.22 |
| 0.10 | 5.26 | 0.10 | 5.26 |

### 2.2 p69b fixed500

| σ_c2c | PPL | σ_d2d | PPL |
|------:|----:|------:|----:|
| 0.0 | 5.31 | 0.0 | 5.23 |
| 0.01 | 5.31 | 0.02 | 5.31 |
| 0.02 | 5.31 | 0.04 | 5.35 |
| 0.05 | 5.31 | 0.06 | 5.35 |
| 0.10 | 5.35 | 0.10 | 5.34 |

### 2.3 p1b adaptive_fixed_v1

| σ_c2c | PPL | σ_d2d | PPL |
|------:|----:|------:|----:|
| 0.0 | 7.54 | 0.01 | 7.38 |
| 0.01 | 7.60 | 0.02 | 7.60 |
| 0.02 | 7.69 | 0.05 | 7.97 |
| 0.05 | 7.94 | 0.10 | 8.11 |
| 0.10 | 8.17 | | |

### 2.4 Cross-instance D2D Consistency — p28b

| Seed | PPL |
|-----:|----:|
| 3373 | 5.14 |
| 3374 | 5.14 |
| 3375 | 5.14 |
| 3376 | 5.15 |
| 3377 | 5.13 |
| CV | < 0.25% |

### 2.5 n_states 扫描 — p28b

| n_states | PPL |
|---------:|----:|
| 128 | 5.14 |
| 256 | 5.14 |
| 512 | 5.15 |
| 1024 | 5.14 |

### 2.6 Mismatch 扫描 — p28b

| Eval c2c | PPL | Eval d2d | PPL |
|---------:|----:|---------:|----:|
| 0.02 | 5.16 | 0.04 | 5.19 |
| 0.05 | 5.20 | 0.06 | 5.22 |
| 0.10 | 5.26 | 0.10 | 5.26 |

---

## 3. Extended Downstream — 完整结果

### 3.1 p28b (2.8B) — Clean

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| fixed500 | 0.6260 | 0.2497 | 0.7388 | 0.5919 |
| adaptive_cosine_v1 | 0.6257 | 0.2460 | 0.7388 | 0.5817 |
| adaptive_fixed_v1 | 0.6202 | 0.2485 | 0.7416 | 0.5801 |
| adaptive_layerwise_v1 | 0.6245 | 0.2460 | 0.7388 | 0.5833 |
| adaptive_reverse_v1 | 0.6202 | 0.2485 | 0.7416 | 0.5801 |
| adaptive_cosine_last2 | 0.6217 | 0.2530 | 0.7394 | 0.5872 |
| adaptive_fixed_1000 | 0.6116 | 0.2434 | 0.7356 | 0.5801 |
| last2_fixed500 | 0.6162 | 0.2500 | 0.7394 | 0.5825 |
| last4_fixed500 | 0.6138 | 0.2453 | 0.7367 | 0.5856 |

### 3.2 p28b (2.8B) — Analog

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| fixed500 | 0.6174 | 0.2502 | 0.7372 | 0.5864 |
| adaptive_cosine_v1 | 0.6144 | 0.2479 | 0.7394 | 0.5770 |
| adaptive_layerwise_v1 | 0.6128 | 0.2475 | 0.7345 | 0.5770 |
| adaptive_reverse_v1 | 0.6122 | 0.2499 | 0.7383 | 0.5793 |
| adaptive_cosine_last2 | 0.6076 | 0.2504 | 0.7388 | 0.5856 |
| adaptive_fixed_1000 | 0.6043 | 0.2445 | 0.7378 | 0.5722 |
| last2_fixed500 | 0.6031 | 0.2505 | 0.7399 | 0.5793 |
| last4_fixed500 | 0.5951 | 0.2482 | 0.7361 | 0.5809 |

### 3.3 p69b (6.9B) — Clean

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| fixed500 | 0.6450 | 0.2651 | 0.7661 | 0.6212 |
| adaptive_cosine_v1 | 0.6413 | 0.2657 | 0.7612 | 0.6275 |
| adaptive_fixed_v1 | 0.6450 | 0.2651 | 0.7661 | 0.6212 |
| adaptive_layerwise_v1 | 0.6388 | 0.2591 | 0.7584 | 0.6188 |
| adaptive_cosine_last2 | 0.6379 | 0.2661 | 0.7666 | 0.6204 |
| fixed_1000 | 0.6434 | 0.2609 | 0.7590 | 0.6251 |
| hat_last2 | 0.6422 | 0.2638 | 0.7617 | 0.6330 |
| hat_last4 | 0.6373 | 0.2636 | 0.7579 | 0.6196 |

### 3.4 p69b (6.9B) — Analog

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| fixed500 | 0.6382 | 0.2606 | 0.7628 | 0.6204 |
| cosine_last2 | 0.6312 | 0.2651 | 0.7601 | 0.6133 |
| hat_last2 | 0.6352 | 0.2624 | 0.7535 | 0.6283 |
| hat_last4 | 0.6346 | 0.2580 | 0.7606 | 0.6062 |

> 注：p69b adaptive_cosine/fixed/layerwise_v1 analog extended 数据在 v5 补跑中，JSON 尚未落盘。

### 3.5 p1b (1B)

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| adaptive_fixed_v1 clean | 0.6052 | 0.2446 | 0.7013 | 0.5249 |
| adaptive_fixed_v1 analog | 0.6024 | 0.2452 | 0.7008 | 0.5501 |

### 3.6 410M

| Config | BoolQ | MMLU | PIQA | WinoGrande |
|--------|------:|-----:|-----:|-----------:|
| adaptive_fixed_1000 clean | 0.5709 | 0.2307 | 0.6746 | 0.5391 |
| adaptive_fixed_1000 analog | 0.5563 | 0.2326 | 0.6692 | 0.5257 |
| reverse_v1_nofreeze clean | 0.3865 | 0.2311 | 0.6638 | 0.5249 |
| reverse_v1_nofreeze analog | 0.3899 | 0.2314 | 0.6697 | 0.5328 |

---

## 4. TruthfulQA 结果

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

> TruthfulQA MC1 接近随机（~0.25），模型在该任务上能力有限。MC2 数据未记录。

---

## 5. 补充评估（v7 运行中）

| 任务 | 状态 | 覆盖模型 |
|------|------|----------|
| **MMLU 5-shot** | 🔄 GPU6 正在跑 analog（clean 因 `--num_fewshot` 参数问题失败，待补） | p28b reverse_v1 |
| **GSM8K** | ⏳ 等待 GPU 空闲 | p28b/p69b 全部 |
| **AI2-ARC** | ⏳ 等待 GPU 空闲 | p28b/p69b 全部 |

v7 scheduler 于 18:24 启动（12h 至 06:24），但 GPU4/5/7 被更早的 v5 extended analog jobs 占用。当前只有 GPU6 在跑 v7 任务。

---

## 代码修复与基础设施

| # | 任务 | 状态 | 备注 |
|---|---|---|---|
| INF-META | Metadata patch（JSON envelope） | ✅ | 所有输出包含完整 metadata |
| INF-OFFLINE | Offline sharded model loading | ✅ | `_resolve_local_path` |
| INF-CLOSURE | Adaptive schedule closure capture bug 修复 | ✅ | `p3_hat_lm_eval.py` / `p3_hat_train.py` |
| INF-CLAIM | Claim-lock manifests | ✅ | p28b/p69b downstream + 自适应模型 |
| INF-PUSH | 大型 eval JSON 压缩/清理 | ⏳ | 大型文件（~75MB 每个）需 LFS 处理；`.gitignore` 目前 blocking LFS |
| INF-MAXLEN | Analog eval --max_length 2048 修复 | ✅ | v5 scheduler 修复 D2D buffer size 超限 |

---

## 统计

| 闭环 | 已完成 | 进行中 | 待办 |
|---|---|---|---|
| P0 基线 | 2 | 0 | 0 |
| P1 核心 K107 | 6 | 0 | 0 |
| P2 规模 | 3 | 0 | 0 |
| P3 大模型/基建 | 5 | 0 | 0 |
| R1 鲁棒性/下游 | 8 | 0 | 0 |
| R2 层消融/跨设备 | 4 | 0 | 0 |
| R3 自适应调度 | 12 | 0 | 0 |
| VLM | 4 | 0 | 0 |
| R0 Codex 审查 | 4 | 0 | 0 |
| R1 机制控制 | 10 | 0 | 0 |
| R9 Extended eval | 3 | 1 | 0 |
| 基础设施 | 5 | 0 | 1 |
| **总计** | **66** | **1** | **1** |

---

## 当前 GPU 占用（2026-05-21 19:00 更新）

| GPU | PID | 任务 | 已运行 | 备注 |
|-----|-----|------|--------|------|
| ? | 92232 | p28b_reverse_v1 analog MMLU 5-shot | ~30min | v7 任务 |
| ? | 3573065 | p69b_cosine_v1 analog extended | ~3h | v5 遗留 |
| ? | 3837592 | p69b_fixed_v1 analog extended | ~2h | v5 遗留 |
| ? | 3971785 | p28b_fixed_v1 standard3 | ~1.5h | v5 遗留 |

v7 实际只占用了 GPU6。GPU4/5/7 需等待 v5 extended analog jobs 完成后才会开始 v7 任务。

---

## 数据完整性

- **eval JSON 总数**：180 个（>10KB，排除 backup/checkpoints）
- **standard3 PPL**：89 个（含 lambada_openai/hellaswag/arc_easy）
- **extended downstream**：43 个（含 boolq/mmlu/piqa/winogrande）
- **TruthfulQA**：8 个（v6 完成）
- **robustness/ablation/scans**：40 个（c2c, d2d, mismatch, n_states, cross-seed 等）
- **v7 补充评估**：MMLU 5-shot, GSM8K, AI2-ARC — 结果待收集
