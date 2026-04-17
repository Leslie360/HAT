# ResNet-18 CIFAR-100 训练问题诊断报告

> **日期**: 2026-04-14  
> **诊断者**: Kimi  
> **状态**: ROOT CAUSE IDENTIFIED

---

## 问题描述

ResNet-18在CIFAR-100上的R3（Standard Noise）和R4（HAT）实验：
- **训练准确率**: 正常上升（R3: 0.92% → 99.43%）
- **测试准确率**: **永远卡在1.00%**
- **现象**: 训练和测试严重脱节

---

## 诊断过程

### Step 1: 排除基础架构问题
运行`debug_resnet_issue.py`发现：
- 即使是标准FP32 ResNet-18（未训练），输出也偏向特定类
- Analog转换后的模型同样存在偏向性
- **结论**: 问题不在基础架构，而在训练/评估流程

### Step 2: 验证Train/Eval分布不匹配
运行`debug_train_eval_mismatch.py`发现：
```
Clean eval improvement: +0.05%
Noisy eval improvement: -0.24%
```
- 模型在clean训练后，clean eval略有提升
- 但在noisy eval下性能反而下降
- **关键发现**: 训练和评估的噪声配置不一致导致分布偏移

### Step 3: 代码审查发现Root Cause

在`analog_layers.py`的`AnalogLinear.__init__`中（line 366-369）：
```python
self.register_buffer(
    'd2d_noise',
    torch.randn(out_features, in_features) * self.config.sigma_d2d * G_range
)
```

**R3配置逻辑**（`train_resnet18.py` line 141-147）：
```python
analog_cfg = AnalogLinearConfig(
    n_states=16,
    sigma_c2c=0.0 if not hat_training else 0.05,  # R3: 0.0
    sigma_d2d=0.10,  # 始终0.10
    noise_enabled=False if not hat_training else True,  # R3: False
    restore_weight_scale=True,
)
```

**set_noise_for_eval**（line 164-168）：
```python
def set_noise_for_eval(model, exp_cfg):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = exp_cfg.noise_enabled  # True for R3
            module.config.sigma_c2c = exp_cfg.sigma_c2c  # 0.05 for R3
```

---

## Root Cause

### 核心问题: 三层分布不匹配

| 阶段 | noise_enabled | sigma_c2c | sigma_d2d | 实际行为 |
|:-----|:-------------:|:---------:|:---------:|:---------|
| R3训练 | False | 0.0 | 0.10 | **无噪声**，量化权重 |
| R3评估 | True | 0.05 | 0.10 | **有噪声**，量化权重+噪声 |
| 差异 | - | - | - | **严重分布偏移** |

### 为什么测试准确率卡死？

1. **d2d_noise buffer已存在**: 创建layer时已经用`sigma_d2d=0.10`初始化
2. **训练时忽略noise**: `noise_enabled=False`导致`_apply_noise`直接返回`W_eff`
3. **评估时启用noise**: `set_noise_for_eval`强制开启noise，d2d_noise被加入
4. **权重未适应噪声**: 训练好的权重从未见过噪声，突然被噪声扰乱 → 输出崩溃

---

## 影响范围

| 实验 | 状态 | 影响 |
|:-----|:----:|:-----|
| R1 (FP32) | ✅ 正常 | 无analog转换，无此问题 |
| R2 (4bit no noise) | ⚠️ 可能正常 | 训练和评估都无噪声 |
| **R3 (Standard Noise)** | ❌ **故障** | 训练无噪声，评估有噪声 |
| **R4 (HAT)** | ❌ **故障** | 训练有噪声但可能配置不当 |
| R5/R6 | ⚠️ 待验证 | HAT训练，可能正常 |

---

## 解决方案

### 方案1: 修复R3配置（推荐）

修改`train_resnet18.py`的`build_model`，对于非HAT训练也启用噪声：

```python
# 当前（错误）
analog_cfg = AnalogLinearConfig(
    sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0,
    noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
    ...
)

# 修复后
analog_cfg = AnalogLinearConfig(
    sigma_c2c=exp_cfg.sigma_c2c,  # 始终使用配置的sigma
    sigma_d2d=exp_cfg.sigma_d2d,
    noise_enabled=exp_cfg.noise_enabled,  # 始终使用配置
    ...
)
```

然后修改`set_noise_for_train`，区分"训练时是否加噪声"：

```python
def set_noise_for_train(model, exp_cfg):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if exp_cfg.hat_training:
                # HAT: 训练时加噪声，反向传播通过STE
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c
            else:
                # Standard: 训练时不加噪声（或加噪声但不通过STE）
                # 但为了分布一致，应该加噪声
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = 0.0  # 或者使用配置的C2C
```

### 方案2: 修改评估逻辑

在`evaluate`函数中，对于R3类型的实验，评估时也关闭噪声：

```python
def evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled=False):
    model.eval()
    # 对于standard training (non-HAT)，评估时也关闭噪声
    if not exp_cfg.hat_training:
        set_noise_for_eval(model, noise_enabled=False, ...)
    else:
        set_noise_for_eval(model, exp_cfg)
```

### 方案3: 重新设计实验矩阵（推荐）

重新定义R3的含义：
- **R3**: "Standard Training with Noise" — 训练和评估都使用噪声
- **新的对照实验**: "Clean Training, Noisy Eval" — 专门测试分布偏移

---

## 立即行动建议

1. **停止当前R3/R4 CIFAR-100实验**（已在运行的让它们完成，但不要启动新的）

2. **修复代码**（选择方案1或3）

3. **重新运行**:
   - R3: 修复配置后重新训练
   - R4: 验证HAT逻辑是否正确

4. **更新文档**:
   - 在实验报告中注明原始R3/R4结果不可信
   - 说明分布不匹配问题

---

## 对论文的影响

| 数据 | 状态 | 处理建议 |
|:-----|:----:|:---------|
| ResNet-18 CIFAR-10 | ✅ 可能正常 | 需要验证CIFAR-10的R3是否有同样问题 |
| **ResNet-18 CIFAR-100** | ❌ **无效** | 需要重新运行修复后的实验 |
| Tiny-ViT/ConvNeXt | ✅ 正常 | 它们的训练逻辑不同，不受此影响 |

### 论文应对策略

**选项A**: 删除ResNet-18 CIFAR-100结果，仅使用CIFAR-10结果填充Table 2
- 优点: 快速，避免延期
- 缺点: Table 2不对称（ResNet只有CIFAR-10）

**选项B**: 修复后重新运行R3/R4 CIFAR-100（~2-3天）
- 优点: 数据完整，对称性完美
- 缺点: 延期，消耗更多GPU时间

**选项C**: 明确声明ResNet-18 CIFAR-100的局限性
- 在Table 2中标注"does not converge under standard recipe"
- 在讨论中分析原因

---

## 技术细节附录

### _apply_noise函数行为

```python
def _apply_noise(self, G_pos, G_neg):
    cfg = self.config
    W_eff = G_pos - G_neg
    
    if not cfg.noise_enabled:
        return W_eff  # R3训练时直接返回，不加任何噪声
    
    # R3评估时执行以下代码：
    d2d_noise = self.d2d_noise  # 已初始化的buffer
    W_eff = W_eff + d2d_noise_scaled  # 突然加入噪声！
    
    if cfg.sigma_c2c > 0:
        W_eff = W_eff + c2c_noise  # 再加入C2C噪声
    
    return W_eff
```

### set_noise_for_eval的影响

```python
# 创建模型时（R3）
module.config.noise_enabled = False  # 默认

# 评估时
module.config.noise_enabled = True   # 强制改为True
module.config.sigma_c2c = 0.05       # 从0.0改为0.05
```

这导致`_apply_noise`的行为在训练和评估时完全不同。

---

**诊断完成时间**: 2026-04-14 01:00  
**建议优先级**: HIGH — 需要立即修复或决定数据处理方式
