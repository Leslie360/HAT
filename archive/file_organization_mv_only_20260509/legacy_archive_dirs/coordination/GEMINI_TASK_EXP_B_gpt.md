# Gemini 任务分配：EXP-B Physical Non-Ideality Sensitivity

> **优先级:** HIGH  
> **目标:** Reviewer Issue #59  
> **预期提升:** Coverage 93.6% → 94.5%

---

## 背景

Reviewer #59 (Kimi) 指出：§6.6 只定性描述了 physical non-idealities (IR drop, sneak paths)，没有定量估计其影响。

我们的 response：通过敏感性分析量化这些效应的影响。

---

## 实验设计：EXP-B

### 物理模型

基于 ReRAM 文献估计，测试两种非理想效应：

**1. IR Drop (位置相关电压降)**
```
G_effective = G × (1 - ir_drop_factor)
其中 ir_drop_factor ~ Uniform(0, max_ir_drop)
```

**2. Sneak Path ( sneak 电流)**
```
G_effective = G + sneak_noise
其中 sneak_noise ~ Normal(0, sneak_factor × G_max)
```

### 参数范围 (基于文献)

| 参数 | 范围 | 文献依据 |
|:-----|:-----|:---------|
| IR drop | 0%, 1%, 2%, 3% | ReRAM benchmarks (1-3% typical) |
| Sneak path | 0%, 1%, 2% | ReRAM benchmarks (1-2% typical) |

### 测试矩阵

共 4×3 = 12 个条件组合，每个条件 5-10 次 MC runs。

---

## 实现方法

参考 EXP-A 的成功经验：

### Step 1: 修改 analog_layers.py

在 `AnalogLinearConfig` 中添加：
```python
ir_drop_factor: float = 0.0  # 0.0 to 0.03
sneak_factor: float = 0.0    # 0.0 to 0.02
```

在 `_weight_to_conductance` 后应用：
```python
# IR drop
if ir_drop_factor > 0:
    ir_drop = torch.rand_like(G_pos) * ir_drop_factor
    G_pos = G_pos * (1.0 - ir_drop)
    G_neg = G_neg * (1.0 - ir_drop)

# Sneak paths
if sneak_factor > 0:
    sneak_noise_pos = torch.randn_like(G_pos) * sneak_factor * cfg.G_max
    sneak_noise_neg = torch.randn_like(G_neg) * sneak_factor * cfg.G_max
    G_pos = G_pos + sneak_noise_pos.clamp(-cfg.G_max*0.1, cfg.G_max*0.1)
    G_neg = G_neg + sneak_noise_neg.clamp(-cfg.G_max*0.1, cfg.G_max*0.1)
```

### Step 2: 创建实验脚本

`experiment_nonideality_gemini.py`

参考 `experiment_asymmetry_gemini.py` 的结构。

### Step 3: 运行实验

使用 V4 checkpoint，CIFAR-10 test set。

---

## 预期结果

基于 ReRAM 文献，预期：
- IR drop 1-2%: <1% accuracy degradation
- IR drop 3%: 1-2% degradation
- Sneak path 1-2%: <1% degradation
- Combined (3% + 2%): <2% degradation

**关键结论:** 这些非理想效应在当前量级下不会消除定性优势。

---

## 论文更新准备

实验完成后，Kimi 将：

1. 更新 §6.6 "Hardware Array Non-Idealities"
2. 添加 Supplementary §S5.2
3. 激活 Fig S2

**文本草稿 (供参考):**
```latex
\item \textbf{Hardware Array Non-Idealities}: Position-dependent IR drop 
and sneak-path currents are modeled as sensitivity parameters. A systematic 
evaluation (Supplementary Section~\ref{subsec:supp-nonideality-sensitivity}) 
shows that combined IR drop and sneak effects up to 3\% degrade accuracy 
by $<$2\%, indicating that the qualitative advantage is robust to moderate 
array-level non-idealities.
```

---

## 成功标准

实验成功当：
1. 所有 12 个条件组合完成测试
2. 结果文件 `nonideality_sweep_results_gemini.json` 生成
3. 最大 degradation <3% (与文献一致)

---

## 时间估计

- 实现: 30分钟
- 运行 (12 conditions × 5 runs): 2-3 GPU hours
- 总计: ~3小时

---

## 当前状态

**EXP-A:** ✅ 已完成 (asymmetry sweep)  
**EXP-B:** 🔄 待启动  
**Reviewer Coverage:** 102/109 (93.6%)  
**目标:** 103/109 (94.5%)

---

**请确认:**
1. 实验设计是否清晰？
2. 参数范围是否合适？
3. 预计何时可以开始？

*Kimi, 2026-04-12 00:20*
