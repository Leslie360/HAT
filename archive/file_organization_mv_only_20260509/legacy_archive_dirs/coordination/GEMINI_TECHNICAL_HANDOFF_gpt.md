# Gemini 技术接手 — GPU实验调试

> **From:** Kimi (hit technical wall)  
> **To:** Gemini (technical expert)  
> **Date:** 2026-04-11  
> **Task:** Fix EXP-A implementation

---

## 问题概述

我们需要实现一个**差分对不对称性**实验，将 Reviewer Issue #15 从定性 limitation 升级为定量 bound。

### 物理模型
```
G_pos_effective = G_pos × (1 + α)
G_neg_effective = G_neg × (1 - α)
```
其中 α 是 asymmetry factor (0%, 5%, 10%, 20%)

### 目标
运行 Tiny-ViT V4 checkpoint，在不同 asymmetry 水平下评估 CIFAR-10 准确度。

---

## 当前状态：4次尝试均失败

### Attempt 1-4 记录
详见: `EXPERIMENT_AUDIT_TRAIL_gpt.md`

**Attempt 1:** 子类化替换 — import错误、架构不匹配  
**Attempt 2:** 配置参数修正 — 结果异常(6.39% = random chance)  
**Attempt 3:** Monkey-patching forward — method binding失败  
**Attempt 4:** Context manager — self绑定错误

---

## 推荐方案 (Attempt 5)

### 核心思路
**在 `AnalogLinearConfig` 层面注入 asymmetry，不修改模块类。**

### 实施步骤

#### Step 1: 修改 `analog_layers.py`

**添加字段到 AnalogLinearConfig:**
```python
@dataclass
class AnalogLinearConfig:
    # ... 现有字段 ...
    asymmetry_factor: float = 0.0  # 新增，默认0表示无不对称
```

**修改 `AnalogLinear._weight_to_conductance`:**
```python
def _weight_to_conductance(self, weight):
    cfg = self.config
    # ... 现有代码计算 G_pos, G_neg ...
    
    # 新增: 应用 asymmetry
    if hasattr(cfg, 'asymmetry_factor') and cfg.asymmetry_factor != 0.0:
        alpha = cfg.asymmetry_factor
        G_pos = G_pos * (1.0 + alpha)
        G_neg = G_neg * (1.0 - alpha)
    
    return G_pos, G_neg
```

同样修改 `AnalogConv2d._weight_to_conductance`。

#### Step 2: 创建实验脚本

创建 `experiment_asymmetry_gemini.py`:

```python
#!/usr/bin/env python3
"""
EXP-A: Differential Asymmetry Sweep
Uses config-based asymmetry injection
"""

import torch
import numpy as np
import json
from train_tinyvit import build_model, evaluate, get_dataloaders, set_seed
from analog_layers import AnalogLinearConfig

def run_experiment():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _, test_loader = get_dataloaders("cifar10", batch_size=256, num_workers=4)
    
    # Load checkpoint
    ckpt = torch.load("checkpoints/V4_hybrid_standard_noise_hat_best.pt", map_location=device)
    exp_cfg_dict = ckpt['exp_cfg']
    
    asymmetry_levels = [0.0, 0.05, 0.10, 0.20]
    num_runs = 10
    results = {}
    
    for asym in asymmetry_levels:
        print(f"\n{'='*60}")
        print(f"Testing asymmetry = {asym}")
        print(f"{'='*60}")
        
        accuracies = []
        
        for run in range(num_runs):
            set_seed(42 + run)
            
            # 关键：创建带有 asymmetry 的 config
            config = AnalogLinearConfig(
                n_states=16,
                G_min=1.0,
                G_max=10.0,
                sigma_c2c=0.05,
                sigma_d2d=0.10,
                noise_mode="uniform",
                noise_enabled=True,
                asymmetry_factor=asym,  # 注入 asymmetry
            )
            
            # 构建模型时传入 config
            # 需要确认 build_model 如何接受 analog_config
            # 可能需要修改 build_model 或使用不同的模型构建方式
            
            # ... 加载权重 ...
            # ... 评估 ...
            
        results[str(asym)] = {
            "mean": float(np.mean(accuracies)),
            "std": float(np.std(accuracies)),
            "accuracies": accuracies,
        }
    
    # 保存结果
    with open("report_md/_gpt/asymmetry_sweep_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    run_experiment()
```

#### Step 3: 验证点

**需要验证的关键问题:**

1. `build_model` 如何接受 `analog_config`？
   - 查看 `train_tinyvit.py` 中的 `build_model` 函数签名
   - 可能需要传递 config 给模型中的 AnalogLinear/AnalogConv2d 层

2. 如何确保加载的 checkpoint 权重与新的 config 兼容？
   - checkpoint 包含 `model_state_dict`
   - 需要确保层名称匹配

3. 如何验证 asymmetry 确实被应用？
   - 添加 debug print 在 `_weight_to_conductance` 中
   - 验证 G_pos/G_neg 被正确修改

---

## 可用资源

### 文件位置
- Checkpoint: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Analog layers: `analog_layers.py`
- Training script: `train_tinyvit.py`
- Audit trail: `report_md/_gpt/EXPERIMENT_AUDIT_TRAIL_gpt.md`

### 环境
```
Python: 3.11.0
PyTorch: 2.10.0+cu128
CUDA: RTX 5070 Ti
```

### 激活命令
```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate LLM
```

---

## 成功标准

实验成功当且仅当：

1. **0% asymmetry:** 准确度 ~97.5% (与 V4 原始结果一致)
2. **5% asymmetry:** 准确度 ~96-97% (<1% 下降)
3. **10% asymmetry:** 准确度 ~94-96% (1-3% 下降)
4. **20% asymmetry:** 准确度 ~85-90% (7-12% 下降)

如果所有 asymmetry 水平都返回 ~6.39% (random chance)，说明模型未正确加载或 analog 模式未启用。

---

## 完成后的工作

1. 更新 `EXPERIMENT_AUDIT_TRAIL_gpt.md` 记录 Attempt 5 成功
2. 广播成功到 `AGENT_SYNC_gpt.md`
3. 更新 §6.6 文本，添加定量结果
4. 启动 EXP-B (Physical Non-Ideality Sweep)

---

## Kimi 的协助

我可以同时：
- 准备 Nano Banana 图像生成的英文 prompts
- 更新论文文本
- 准备 §6.6 的更新草稿
- 验证 Perplexity 文献引用

Gemini 专注：
- 实现 Attempt 5
- 调试 PyTorch model loading
- 验证实验结果

---

*Handoff time: 2026-04-11 23:15*  
*Expected completion: 2-3 hours*  
*Collaboration mode: Active*
