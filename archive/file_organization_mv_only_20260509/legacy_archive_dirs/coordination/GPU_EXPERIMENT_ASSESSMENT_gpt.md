# GPU 实验评估：低优先问题是否值得追

> Kimi 诚实评估 (2026-04-11)

---

## 当前状态：8个未覆盖问题

| # | 问题 | 当前理由 | GPU可解？ | 价值评估 |
|:--:|:-----|:---------|:---------:|:---------|
| 5 | Activation function coverage | 低优先，非核心 | ✅ 容易 | 🟡 中等 |
| 15 | Differential pair asymmetry ablation | 低优先 | ✅ 容易 | 🔴 **高** |
| 16 | Digital operator split ablation | 低优先 | ✅ 中等 | 🟡 中等 |
| 45 | Missing ablation studies | 部分覆盖 | ⚠️ 需设计 | 🟡 中等 |
| 49 | Optical linearization | 低优先 | ❌ 需新模块 | 🟢 低 |
| 53 | NL vs COMSOL validation | 超出scope | ❌ 需物理仿真 | 🟢 低 |
| 59 | **Physical non-ideality sensitivity** | §6.6只定性 | ✅ 可量化 | 🔴 **高** |
| 62 | Proportional+NL coupled | 超出scope | ❌ 需大量实验 | 🟢 低 |

---

## 真正值得GPU追的3个实验

### 1. Differential Pair Asymmetry Sensitivity (#15) ⭐⭐⭐

**Why now valuable:**
- §6.6 承认 "systematic branch asymmetry... not isolated" 是局限性
- Reviewer可能追问：多大的asymmetry会break系统？
- 我们声称differential mapping提供噪声抵消，但未验证tolerance

**Experiment design:**
```python
# 在 device_profile 中添加 branch_asymmetry 参数
# G_pos = G_nominal * (1 + asymmetry)
# G_neg = G_nominal * (1 - asymmetry)

asymmetry_levels = [0.0, 0.05, 0.10, 0.20]  # 0%, 5%, 10%, 20% mismatch
# Run Tiny-ViT V4 inference on each
# Expected: <5% asymmetry tolerable, >10% degrades
```

**Cost:** 1-2 GPU hours (4 conditions × 10 MC runs)  
**Impact：** 把 §6.6 的定性 limitation 变成定量 insight，显著加强说服力

---

### 2. Physical Non-Ideality Sensitivity Sweep (#59) ⭐⭐⭐

**Why now valuable:**
- §6.6 列了 IR drop, sneak path, temperature 等未建模效应
- Reviewer会问：这些效应有多大影响？10%？50%？
- 当前只有文字说明，无量化bound

**Experiment design:**
```python
# 对当前canonical profile添加penalty模型
# 基于ReRAM文献的1-3% estimate做sensitivity sweep

ir_drop_factors = [1.00, 1.01, 1.02, 1.03]  # 0%, 1%, 2%, 3% weight distortion
sneak_factors = [1.00, 1.01, 1.02]  # 0-2% leakage effect
# Run V4 inference, show accuracy vs. non-ideality level
```

**Cost:** 2-4 GPU hours  
**Impact：** 把模糊的"out-of-scope"变成具体的"tolerable up to X%"

---

### 3. Activation Function Ablation (#5) ⭐⭐

**Why marginal:**
- 当前框架只测试了GELU (Tiny-ViT default)
- Sonar reviewer问：ReLU, SiLU, GELU在analog域表现是否一致？

**Experiment design:**
```python
# 在 train_tinyvit.py 中切换activation
# Tiny-ViT default: GELU
# Test: ReLU, SiLU, GELU
# Train V4-equivalent (4-bit + HAT) for each
```

**Cost：** 3× training runs = ~12-18 GPU hours  
**Impact：** 中等。可能发现GELU确实最合适，或发现ReLU更robust

---

### 4. ConvNeXt C4 Three-Seed Completeness ⭐⭐

**Current state：** C4 (ConvNeXt CIFAR-10 HAT) 只有single-seed checkpoint  
**Why marginal now：** P14已经提供其他controls，C4是supporting evidence

**Cost：** 2 seeds × 100 epochs = ~16-20 GPU hours  
**Impact：** 低。Nice to have but not blocking

---

## 我的建议

### 如果 GPU < 6 hours 可用：
**只做 Experiment #1 (Differential asymmetry)**
- 最高性价比
- 直接回应§6.6 limitation
- 可声称"quantified tolerance up to X%"

### 如果 GPU 6-12 hours 可用：
**做 #1 + #2 (Asymmetry + Non-ideality sensitivity)**
- 把两个定性limitation都变成定量bound
- 论文从"we acknowledge"升级到"we quantified"

### 如果 GPU > 20 hours 可用：
**考虑 #3 (Activation)** 或 **重跑 C4 three-seed**
- 但边际收益递减

---

## Honest Assessment: 审稿意见能满足吗？

### 当前状态 (92.7% coverage)

**Tier 1 (4+ reviewers)：** ✅ 全部解决
- AIHWKIT comparison: 有
- Energy bounds: 有routing sensitivity
- Ensemble HAT: 有

**Tier 2 (2-3 reviewers)：** ✅ 全部解决
- ADC 6-bit: 已解释
- C2C p-values: 已加
- CrossSim citation: 已补

**Tier 3 (单reviewer)：** ⚠️ 8个未覆盖

### 那8个真的能过关吗？

**能过关的 (rebuttal可解释)：**
- #5 Activation: "Focus on core operators; standard scope"
- #49 Optical linearization: "Addressed via frontend compensation"
- #53 COMSOL: "Device physics beyond behavioral simulation scope"
- #62 Coupled effects: "Complex interaction for future work"

**有风险被追问的：**
- #15 Differential asymmetry: "We acknowledge but didn't quantify"
- #59 Physical non-ideality: "We listed but didn't estimate impact"
- #16 Operator split: "We justified but didn't ablate"

**结论：** 如果reviewer很nice，8个都能过关。如果遇到aggressive reviewer，#15和#59可能会被追问"why not quantify?"

---

## 最终建议

**保守路径 (推荐)：**
- 不跑新实验
- 在 §6.6 加一句："Quantitative sensitivity to these effects remains future work"
- 依赖 92.7% coverage + 诚实的limitations disclosure

**激进路径 (如果GPU可用且你想惊喜reviewer)：**
- 跑 differential asymmetry (#1) — 2 hours
- 跑 physical non-ideality sweep (#2) — 4 hours  
- 更新 §6.6: "We quantified tolerance up to 10% asymmetry and 3% IR drop"
- Coverage 提升到 ~95%，aggressive reviewer也无话可说

---

**你选哪条路？** 如果告诉我GPU可用时长，我可以给出具体的实验脚本。
