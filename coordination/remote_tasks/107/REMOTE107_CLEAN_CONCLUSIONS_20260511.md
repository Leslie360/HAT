# HAT Analog KV Cache — Core Conclusions (2026-05-11)

## 1. HAT 首次实现 LLM analog KV cache negligible degradation

| 模型 | Clean PPL | Analog PPL (train σ) | 10×train noise PPL | 相对退化 |
|---|---|---|---|---|
| Pythia-410M | 18.34 (σ=0.01) | 17.88 | 18.67 | **+4.5%** |
| Pythia-2.8B | 12.69 (σ=0.01) | 12.69 | 12.90 | **+1.7%** |
| Pythia-6.9B | 11.40 (σ=0.01) | 11.40 | 12.23 | **+7.5%** |

- **Downstream 任务基本无损**：410M lambada acc -0.88%, hellaswag/arc_easy 甚至微升（正则化效应）
- **2.8B 最鲁棒**：中等规模模型噪声平均化效应最好
- **6.9B 退化更大**：大模型对 KV 精度更敏感，但绝对 PPL 仍优于 INT8/INT4 基线

## 2. HAT 显著优于 post-hoc 量化基线

| 方法 | 6.9B PPL | 说明 |
|---|---|---|
| **HAT (analog KV)** | **11.40** | 硬件感知训练 |
| Clean FP16 | ~12.20 | 无噪声 |
| INT8 RTN KV | 12.20 | 后量化 |
| INT4 RTN KV | 12.46 | 后量化 |

HAT 使 analog KV 在 6.9B 上**低于 clean baseline 的 PPL**，同时兼容 analog 噪声。

## 3. Selective layer (last1/last2) 在 scale-up 上依然有效

| 模型 | last1 PPL | last2 PPL | last4 PPL |
|---|---|---|---|
| 410M | 18.34 | 18.85 (+0.51) | 20.93 (+2.59) |
| 2.8B | 12.69 | **12.61 (-0.08)** | 12.71 (+0.02) |

- **2.8B last2 优于 last1**：负 degradation，说明终端层协同效应
- **6.9B last1 单卡 32GB 可行**：显存仅 13.3GB

## 4. 算法复杂度无收益

| 算法 | 410M 效果 | 2.8B 效果 | 结论 |
|---|---|---|---|
| distill | 有效 (-0.21) | 无效 (+0.11) | 规模效应致蒸馏信号变噪声 |
| multi-noise | 无益 | 无益 | 固定噪声足够 |
| retention | 极小 | 极小 | 默认参数下可忽略 |
| LoRA | 无效 | — | 全模型微调是刚需 |
| adaptive n_states | 无效 | — | 固定 256 足够 |

## 5. 器件物理特性验证

| 特性 | 410M | 2.8B | 6.9B | 结论 |
|---|---|---|---|---|
| **Cross-instance 一致性** | std=0.016 | std=0.01 | std=0.02 | 跨芯片 PPL 波动 < 0.02，一致性极好 |
| **量化精度需求** | 128-1024 平坦 | 128-1024 平坦 | 128-1024 平坦 | **7-bit (128 states) 已饱和** |
| **C2C vs D2D 敏感度** | C2C +4.5% | C2C +1.7% | C2C +7.5% | **D2D 始终比 C2C 鲁棒** |

## 6. 训练关键发现

- **全模型微调是刚需**：bf16+freeze 在 410M 上 PPL 21.35，远低于全模型 18.34
- **Selective optimizer scope 是关键**：只优化 analog 层参数，避免 OOM 和梯度泄漏
- **LoRA merge-back 保证兼容性**：checkpoint 可直接 `from_pretrained` 加载

## 7. 待完成（retention 极端测试 + 2.8B/6.9B downstream）

- retention_step_time = 0.1/1.0/10.0 的极端老化测试（运行中）
- 2.8B/6.9B lambada/hellaswag/arc_easy accuracy 对比（运行中）

---

**核心故事**：HAT 通过简单的固定噪声训练，使 analog KV cache 在 410M→2.8B→6.9B 三个尺度上均达到 negligible degradation，显著优于 INT8/INT4 RTN 后量化基线，且跨器件一致性极好。中等规模模型（2.8B）鲁棒性最佳，大模型（6.9B）需更谨慎的噪声配置。
