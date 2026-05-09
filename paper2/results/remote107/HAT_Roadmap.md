# HAT (Hardware-Aware Training) 实验任务清单

## 一、已完成实验

### 410M 规模（Pythia-410m-deduped, last1=layer23）
| 实验 | PPL after | PPL before | 步数 | 关键参数 | 结论 |
|------|-----------|------------|------|----------|------|
| fixed 500 (全模型) | **18.34** | 23.30 | 500 | fp32, 无freeze | 最强baseline |
| distill 500 | **18.13** | 23.30 | 500 | alpha=0.5, temp=2.0 | 410M上唯一有效新算法 |
| multi-noise uniform 500 | 18.57 | 23.30 | 500 | d2d_schedule=uniform | 无益 |
| multi-noise linear 500 | 18.34 | 23.30 | 500 | d2d_schedule=linear | 持平 |
| retention 500 | 18.51 | 22.72 | 500 | retention_step_time=0.01 | 影响极小 |
| bf16 freeze 500 | 21.35 | 23.30 | 500 | fp16+freeze | freeze是坑 |
| LoRA r8 100 | 23.23 | - | 100 | lora_rank=8 | 无效 |
| LoRA r32 100 | 23.14 | - | 100 | lora_rank=32 | 无效 |
| adaptive n_states 100 | 22.98 | - | 100 | linear:0.5:2.0 | 无效 |

**Downstream Eval (fixed500 fullmodel, lm-eval):**
| Task | Clean | Analog (σ_c2c=0.01, σ_d2d=0.02) | Δ |
|------|-------|----------------------------------|---|
| lambada PPL | 21.47 | 22.70 | +1.23 |
| lambada acc | 39.01% | 38.13% | -0.88% |
| hellaswag acc | 33.79% | 33.84% | +0.05% |
| hellaswag acc_norm | 40.08% | 40.31% | +0.23% |
| arc_easy acc | 49.49% | 50.04% | +0.55% |
| arc_easy acc_norm | 44.53% | 44.36% | -0.17% |

**结论：** HAT 训练后模型在 analog 噪声下下游任务基本无损，arc_easy/hellaswag 甚至略有提升（正则化效应）。

### 410M 层数 Sweep
| 配置 | PPL after | PPL before | vs last1 |
|------|-----------|------------|----------|
| last1 (layer 23) | 18.34 | 23.30 | — |
| last2 (layers 22-23) | 18.85 | 24.95 | +0.51 |
| last4 (layers 20-23) | 20.93 | 31.27 | +2.59 |
| last4 + distill 500 | 20.10 | 31.27 | distill救回0.83 |

### 2.8B 规模（Pythia-2.8b-deduped, last1=layer31）
| 实验 | PPL after | PPL before | 步数 | 结论 |
|------|-----------|------------|------|------|
| fixed 100 | 13.27 | 13.71 | 100 | baseline |
| fixed 500 | **12.69** | 13.71 | 500 | 核心scale-up数据 |
| distill 100 | 13.29 | 13.71 | 100 | 没拉开 |
| distill 500 | 12.80 | 13.71 | 500 | **比fixed差** |
| multi-noise uniform 100 | 13.24 | 13.71 | 100 | 微弱领先 |
| multi-noise uniform 500 | 12.67 | 13.71 | 500 | 微弱领先(0.02) |
| retention 100 | 13.29 | 13.75 | 100 | 没拉开 |
| retention 500 | 12.72 | 13.71 | 500 | 持平 |

### 2.8B 层数 Sweep
| 配置 | PPL after | PPL before | vs last1 | 结论 |
|------|-----------|------------|----------|------|
| last1 (layer 31) | **12.69** | 13.71 | — | 核心 baseline |
| last2 (layers 30-31) | **12.61** | 13.92 | **-0.08** | 负 degradation |
| last4 (layers 28-31) | **12.71** | 14.49 | +0.02 | 基本无损 |

### 6.9B 规模（Pythia-6.9b-deduped, last1=layer31）
| 实验 | PPL after | PPL before | 步数 | 关键参数 | 结论 |
|------|-----------|------------|------|----------|------|
| fixed 500 | **11.40** | 12.20 | 500 | fp16, last1 | 核心 scale-up 数据 |
| INT8 RTN KV baseline | 12.20 | — | — | post-hoc quant | HAT 优于 INT8 基线 |
| INT4 RTN KV baseline | 12.46 | — | — | post-hoc quant | HAT 显著优于 INT4 |
| downstream clean | — | — | — | lambada/hellaswag/arc | **运行中 (GPU 6)** |
| downstream analog | — | — | — | σ_c2c=0.01, σ_d2d=0.02 | **运行中 (GPU 7)** |

### 410M 灵敏度与鲁棒性扫描（2026-05-09 新增）
| 实验 | 关键结果 | 结论 |
|------|---------|------|
| σ_c2c sweep (0.0→0.10) | PPL 17.86→18.48 | 线性退化，5×训练噪声退化+3.5% |
| σ_d2d sweep (0.0→0.10) | PPL 17.86→18.49 | 与C2C退化幅度相当 |
| eval σ_c2c mismatch | train=0.01, eval=0.10 → PPL 18.67 | 10×训练噪声退化+4.5% |
| eval σ_d2d mismatch | train=0.02, eval=0.10 → PPL 18.49 | D2D相对更鲁棒 |
| D2D seed cross-instance | 5 seeds, PPL 18.26-18.30, std=0.016 | 跨芯片一致性极好 |
| n_states sweep (128→1024) | 所有点 PPL 18.30 | 7-bit (128 states) 已足够 |

---

## 二、待办实验（近期）

### P0: 数据补全
- [x] 6.9B fixed 500（PPL 11.40，已完成）
- [x] 2.8B last2 fixed 500 结果读取（PPL 12.61）
- [x] 2.8B last4 fixed 500 结果读取（PPL 12.71）
- [x] 410M 超参灵敏度扫描（σ_c2c/σ_d2d sweep，已完成）
- [x] 410M n_states 扫描（128-1024，已完成）
- [ ] 2.8B fixed500 downstream eval（lm-eval，运行中 GPU 4/5）
- [ ] 6.9B fixed500 downstream eval（lm-eval，运行中 GPU 6/7）
- [ ] 2.8B/6.9B 超参灵敏度扫描

### P1: 基线对比（已完成代码实现）
- [x] INT4 RTN KV cache 量化baseline实现（`p3_hat_eval_quantized_baseline.py`）
- [x] INT8 RTN KV cache 量化baseline实现
- [x] 410M/2.8B/6.9B 上 HAT vs 量化 PPL 对比（6.9B: 11.40 vs 12.20/12.46）
- [x] lm-evaluation-harness 接入（`p3_hat_lm_eval.py`，含 `_sanitize` 修复）
- [x] 410M Lambada/HellaSwag/ARC 上 clean vs analog accuracy 对比
- [ ] 2.8B/6.9B downstream accuracy 对比（运行中）

### P2: 鲁棒性验证（已完成410M，待扩展2.8B/6.9B）
- [x] Train-eval mismatch（410M 已完成：C2C +4.5% @ 10×train, D2D +3.4% @ 5×train）
- [x] D2D seed cross-instance（410M 已完成：5 seeds, std=0.016）
- [x] n_states 灵敏度（410M 已完成：128-1024 完全平坦）
- [ ] Train-eval mismatch（2.8B/6.9B 待启动）
- [ ] Retention 极端测试（retention_step_time=0.1/1.0）

---

## 三、代码与文档基础设施（2026-05-09 更新）

### 已完成
- [x] `p3_hat_lm_eval.py` — lm-evaluation-harness 集成（含 `_sanitize` 修复 dtype/callable）
- [x] `p3_hat_eval_quantized_baseline.py` — INT4/INT8 RTN KV 量化基线
- [x] `CORE_MATH_REPRO_PACKET_20260509.md` — 11-section 交付文档（conductance mapping / STE / D2D/C2C / retention / selective layer / SDPA patch / baseline / unit tests）
- [x] GitHub `107-clean` 分支同步（含上述 3 个新文件 + 交付文档）

### 待开发功能（中期）
- [ ] `p3_hat_eval.py` 加 `--kv_bits 4/8` 支持量化baseline（已独立脚本实现，待合并）
- [ ] `p3_hat_eval.py` 加 `--eval_sigma_c2c` / `--eval_sigma_d2d` 支持mismatch测试
- [ ] 多器件模型支持（RRAM/PCM/FeFET Config）
- [ ] Weight HAT 原型（从KV扩展到weights）

---

## 四、数据整理（本周可启动）

- [ ] 层数 tradeoff 曲线图（410M last1/2/4 + 2.8B last1/2/4）
- [ ] 模型规模曲线图（410M/2.8B/6.9B fixed baseline）
- [ ] 算法对比柱状图（410M 各算法 vs fixed）
- [ ] 超参扫描热力图（sigma vs PPL）

---

## 五、长期规划（3-6个月）

### 论文发表路线
- [ ] **NeurIPS/ICML 2026**（截稿通常在5月/9月）
  - 核心故事：HAT 使 analog KV cache 在 LLM 上首次达到 negligible PPL degradation
  - 需要数据：410M/2.8B/6.9B 完整 scale-up 曲线 + 下游任务 accuracy + 量化 baseline 对比
  - 风险：如果 distill/multi-noise 始终无效，故事变简单（"fixed noise is enough"），需强化理论解释
- [ ] **备选：DAC/ISSCC Circuit领域会议**（如果与器件组合作）
  - 强调能效收益（analog MAC 100fJ vs digital 0.4pJ）+ 面积优势
  - 需要：Energy profiling 数据 + 阵列级仿真

### 模型与架构扩展
- [ ] **支持非Pythia架构**：LLaMA-2/3、Mistral、Qwen（GQA/MQA不同KV结构）
  - Llama用GQA，KV head数≠query head数，analogize逻辑需适配
  - 影响：GQA减少KV参数量，analog化收益可能降低
- [ ] **Instruction-tuned模型验证**：Pythia-instruct 或 Llama-chat
  - HAT在base模型有效≠instruct模型有效，对话长上下文对retention更敏感
- [ ] **多模态扩展**：视觉-语言模型（LLaVA-style）的analog KV cache
  - 图像token数量多（576+），对D2D/C2C噪声的累积效应不同

### 多模态扩展（Qwen-VL）
- [ ] **最小可行性验证**：Qwen2-VL-2B/7B 单图 clean vs analog KV 生成质量对比
  - 目标：确认视觉特征对 conductance noise 的鲁棒性是否高于文本
  - 需改：p3_hat_eval.py 支持 Qwen2Attention（GQA + 独立 q/k/v proj）
  - 输入：单张图 + 简单 prompt，肉眼/指标对比输出质量
  - 风险：视觉 token 数大（576~1024），显存可能吃紧；动态分辨率需动态 buffer
- [ ] **多模态 HAT 训练**：在 LLaVA/ShareGPT4V 数据上训练 Qwen-VL
  - 核心问题：纯文本 HAT 权重直接用于多模态是否足够？还是需要 vision-language 联合 HAT？
  - 评估：MMMU / MMBench / TextVQA 上 clean vs analog accuracy 对比
  - 研究价值：Multimodal Analog KV Cache 是全新方向，现有工作均集中在 CNN 图像分类

### 实际系统集成
- [ ] **FPGA/硬件原型验证**（与器件组合作）
  - 将HAT-trained权重部署到实际RRAM/PCM阵列
  - 测量真实inference PPL vs 仿真PPL的gap
  - 关键：器件非理想性（IR drop、sneak path）在实际中可能比仿真更严重
- [ ] **多器件Config验证**：RRAM/PCM/FeFET各一套参数
  - 当前默认参数偏向有机光电器件（tau_1=0.14s），RRAM retention可能好得多
  - 需从器件组获取真实sigma_c2c/sigma_d2d/retention参数
- [ ] **On-device training验证**：是否能在阵列上做in-situ HAT
  - 目前HAT是在GPU上模拟器件噪声训练，真实in-situ训练有写入非线性、耐久性限制

### 开源与社区
- [ ] **代码开源**：整理clean repo（当前monkey-patch较hacky）
  - 理想形态：transformers-compatible `AnalogKVCache` 类，pip install即可用
  - 需要重构：用Hook替代monkey-patch，支持任意模型架构
- [ ] **Benchmark release**：建立analog KV cache的标准评测集
  - 类似SmoothQuant/GPTQ的community benchmark，包含PPL + downstream tasks

---

## 六、关键发现总结

1. **全模型微调是刚需**：之前bug版只优化attention模块导致PPL ~21.3，修正后~18.3
2. **简单fixed噪声足够好**：distill/multi-noise/retention在2.8B上均无实质收益
3. **distill在410M有效、2.8B失效**：规模效应导致蒸馏信号变为噪声
4. **freeze是坑**：bf16+freeze在410M上PPL 21.35，远不如全模型
5. **2.8B单卡32GB完全可行**：bf16+freeze仅占用~10GB显存
6. **HAT 显著优于 INT8/INT4 RTN 量化基线**：6.9B 上 HAT PPL 11.40，INT8 12.20，INT4 12.46
7. **Downstream 任务基本无损，甚至正则化提升**：410M analog 下 arc_easy acc +0.55%，hellaswag acc_norm +0.23%
8. **Selective layer 在 scale-up 上依然有效**：2.8B last2 PPL 12.61（优于 last1 的 12.69），last4 12.71 基本无损
9. **6.9B 单卡 32GB 可行**：bf16 + last1 约占 13.3GB 显存，fixed500 训练成功
10. **HAT 对 ±2× 训练噪声基本鲁棒**：410M eval σ=0.02（2× train）时 PPL 仅 +0.7%，5× 时 +3.5%
11. **C2C 比 D2D 更敏感**：相同倍数超训练噪声时，C2C 退化幅度 > D2D
12. **跨器件实例一致性极好**：5 个不同 D2D seed 间 PPL 标准差仅 0.016
13. **量化精度需求极低**：410M 上 n_states 128→1024 对 PPL 完全无影响，7-bit 已饱和
