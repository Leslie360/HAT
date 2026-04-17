# CX-3: ResNet-18 Deep Bug Investigation Report

## 1. 现象 (Symptom)
执行 `eval_resnet18_checkpoints.py` 评估 `R4_4bit_noise_HAT_best.pt` 时，测试集准确率仅为 **10.00%**，而其训练时的预期准确率（Best Acc）为 **90.37%**。此问题具有极高的迷惑性，表现出类似模型崩溃的特征。

## 2. 诊断排查 (Diagnosis & Debugging)
我们进行了系统性的代码及权重排查：
- 确认了 `w_abs_max` 并不是作为一个 `register_buffer` 保存在模型中，而是每次前向传播时由 `W_fp32.abs().max().detach()` 动态计算出来的。
- 确认了 checkpoint `exp_cfg` 字典的完整性。发现旧版的 CIFAR-10 checkpoint 的 config 中**缺失**了 `restore_weight_scale` 这个字段。

## 3. 根因分析 (Root Cause)
问题的核心在于 `eval_resnet18_checkpoints.py` 脚本本身存在解析漏洞：
- 该脚本在加载 `ExperimentConfig` 时，只是简单提取已有字段：`ExperimentConfig(**filtered)`。
- 由于旧版 R4 checkpoint 的 `exp_cfg` 中没有 `restore_weight_scale`，`ExperimentConfig` 自动应用了它的当前默认值：`restore_weight_scale = True`。
- 然而，该模型在最初训练时（基于旧版代码的默认行为），实际上使用的是 `restore_weight_scale = False`。
- 这个不一致导致评估时模拟器错误地应用了一层缩放恢复，打乱了所有 analog weight 的数值范围，致使最终分类完全失效（10% chance level）。

## 4. 修复方案 (Fix)
在 `eval_resnet18_checkpoints.py` 中引入 `train_resnet18.py` 里已有的针对 legacy checkpoint 的解析逻辑：
```python
from train_resnet18 import load_experiment_config_from_checkpoint

def load_exp_cfg(ckpt: dict) -> ExperimentConfig:
    return load_experiment_config_from_checkpoint(ckpt)
```
该函数内部包含了向下兼容机制，如果在原始 config 中找不到 `restore_weight_scale`，会正确地将其回退为 `False`。

## 5. 验证 (Validation)
应用上述修复后，重新运行 `eval_resnet18_checkpoints.py`：
- `checkpoints/R4_4bit_noise_HAT_best.pt` on cifar10 
  - **Expected**: 90.37%
  - **Eval**: 89.83%
  - **Delta**: -0.54% (符合正常的 C2C noise stochastic 波动)
问题彻底解决，证明 ResNet-18 的物理转换和训练逻辑本身没有问题，纯粹是配置反序列化阶段的向前兼容性 bug。