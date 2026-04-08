# Phase A1.1 & A1.2 实现计划

## Context
为有机光电突触晶体管在交叉阵列上的硬件感知仿真框架搭建基础模块。第一步是对 Tiny-ViT-5M 进行逐层剖析和阵列映射（A1.1），然后实现模拟线性层 AnalogLinear（A1.2）。

---

## 关键发现：Tiny-ViT-5M 真实架构

timm 中 `tiny_vit_5m_224` 的实际结构（与用户描述有偏差）：

- **Config**: `embed_dims=[64,128,160,320], depths=[2,2,6,2], num_heads=[2,4,5,10], mlp_ratio=4.0`
- **PatchEmbed (stem)**: Conv2d(3→32, k=3, s=2) + Conv2d(32→64, k=3, s=2)，各带 BN
- **Stage 0 (ConvLayer)**: 2个 MBConv 块 (dim=64)，每块含 1×1扩展→3×3DW→1×1投影+BN+GELU
- **Stage 1**: PatchMerging(64→128) + 2个 TinyVitBlock(dim=128, 4 heads)
- **Stage 2**: PatchMerging(128→160) + 6个 TinyVitBlock(dim=160, 5 heads)
- **Stage 3**: PatchMerging(160→320) + 2个 TinyVitBlock(dim=320, 10 heads)
- **Head**: LayerNorm2d(320) → GlobalAvgPool → Linear(320→1000)

每个 **TinyVitBlock** 含：Attention(qkv Linear + proj Linear) + local_conv(DWConv+BN) + MLP(fc1 Linear + GELU + fc2 Linear)

每个 **PatchMerging** 含：Conv2d 1×1 + DWConv 3×3 s=2 + Conv2d 1×1，各带 BN

---

## 层分类规则（依据参考手册 §1.1）

### ANALOG（映射到交叉阵列）
| 层类型 | 匹配规则 |
|:---|:---|
| Attention Q/K/V 投影 | `*.attn.qkv` (Linear) |
| Attention 输出投影 | `*.attn.proj` (Linear) |
| FFN/MLP 第一层 | `*.mlp.fc1` (Linear) |
| FFN/MLP 第二层 | `*.mlp.fc2` (Linear) |
| Patch Embedding 卷积 | `patch_embed.*.conv` (Conv2d, groups=1, 可展开为密集矩阵) |

### DIGITAL（数字协处理器）
| 层类型 | 原因 |
|:---|:---|
| MBConv 全部 Conv2d（含1×1点卷积） | BWQ 2023：整个 MBConv 块利用率低 |
| PatchMerging 全部 Conv2d | 含 DwConv，整块保留数字域 |
| local_conv (DWConv) | 逐通道卷积，交叉阵列利用率极低 |
| BatchNorm / LayerNorm | 非 VMM 操作 |
| GELU / Softmax | 激活函数 |
| Q·Kᵀ 动态矩阵乘 | 每次输入不同，无法固化权重 |
| 分类头 Linear(320→1000) | 参数量小，不值得映射 |

---

## Task 1: `model_profiling.py`

**文件路径**: `/home/qiaosir/projects/compute_vit/model_profiling.py`

### 实现步骤

1. **加载模型**
   ```python
   model = timm.create_model('tiny_vit_5m_224', pretrained=False)
   ```

2. **classify_layer(name, module)** — 分类函数
   - 按优先级匹配层名：`patch_embed.*.conv` → analog；`*.attn.qkv/proj` → analog；`*.mlp.fc1/fc2` → analog；其余 → digital
   - 检测 DwConv：`module.groups == module.in_channels and module.groups > 1`

3. **遍历 named_modules()**，仅处理 Conv2d / Linear 类型
   - Linear: M=out_features, N=in_features
   - Conv2d (groups=1): M=C_out, N=C_in×kH×kW（展开为密集矩阵）
   - DwConv: 记录但标记 digital

4. **交叉阵列计算**（仅 analog 层）
   ```
   n_row_tiles = ceil(M / 128)
   n_col_tiles = ceil(N / 128)
   arrays_diff_pair = n_row_tiles × n_col_tiles × 2
   ```

5. **输出**
   - 逐层详细表格（层名、类型、维度、参数量、标签、阵列数）
   - 汇总统计（总参数、analog/digital参数、占比、总阵列数）
   - Paper 用 Markdown 表格
   - JSON 导出（供后续脚本使用）

6. **校验**：汇总参数量 vs `sum(p.numel() for p in model.parameters())`，确保无遗漏

### 需注意
- Attention 中的 `attention_biases` 小参数需额外扫描 `named_parameters()` 捕获
- BN 只计 weight+bias（不含 running_mean/var buffer）

---

## Task 2: `analog_layers.py`

**文件路径**: `/home/qiaosir/projects/compute_vit/analog_layers.py`

### 模块结构

#### 2.1 `AnalogLinearConfig` (dataclass)
```
n_states=16, G_min=1.0, G_max=10.0
NL_LTP=+1.0, NL_LTD=-1.0
sigma_c2c=0.05, sigma_d2d=0.10
retention_enabled=False, tau_1=0.14, tau_2=0.61, A_0=0.6
inference_time=0.0
```

#### 2.2 `StraightThroughQuantize` (torch.autograd.Function)
- forward: clamp → normalize to [0,1] → round to n_states 级 → denormalize
- backward: STE，梯度直通

#### 2.3 `AnalogLinear(nn.Module)`

**__init__**: 同 nn.Linear 参数 + config。`register_buffer('d2d_noise', randn * sigma_d2d * G_range)` 固定 D2D 噪声。

**forward 流程**:
1. `_weight_to_conductance(W)`: W → W⁺/W⁻ → normalize by detached w_abs_max → map to [G_min, G_max] → STE quantize → 返回 G⁺, G⁻
2. `_apply_retention(G⁺, G⁻)`: 若启用，双指数衰减 `G(t) = G_min + (G-G_min) × [A₁·exp(-t/τ₁) + A₂·exp(-t/τ₂) + A₀]`，其中 A₁=A₂=(1-A₀)/2
3. `_apply_noise(G⁺, G⁻)`: W_eff = G⁺-G⁻ + d2d_noise + N(0, σ_c2c²)（C2C 每次前向重采样）
4. `F.linear(x, W_eff, bias)` → output

**训练 vs 推理**:
- 训练 (HAT)：量化+噪声全开，STE 传梯度，D2D 固定，C2C 每步重采样，retention OFF
- 推理：可选关闭 C2C 做确定性推理，或保持开启做 Monte Carlo 评估
- 通过 `noise_enabled` flag 独立控制

#### 2.4 数值稳定性
- normalize 分母加 eps=1e-8 防除零
- w_abs_max 用 `.detach()` 阻止梯度流过归一化因子
- D2D 噪声的 scale = sigma_d2d × G_range（相对于电导范围的比例噪声）

#### 2.5 `convert_to_hybrid(model, config)` 工具函数
- 递归遍历 model，匹配 analog 层名
- 将 nn.Linear 替换为 AnalogLinear，拷贝预训练权重
- 返回混合模型

---

## 实施顺序

| 步骤 | 内容 | 依赖 |
|:---:|:---|:---|
| 1 | `pip install timm`（若未安装） | — |
| 2 | 实现 `model_profiling.py` 并运行验证 | timm |
| 3 | 实现 `analog_layers.py` (Config + STE + AnalogLinear) | — |
| 4 | 简单测试：创建 AnalogLinear，验证量化级数、噪声行为、梯度流 | Step 3 |

---

## 验证方法

### model_profiling.py
- 运行脚本，确认总参数量 ≈ 5.4M
- 确认所有 MBConv/PatchMerging/DwConv/BN/LN/head 标记为 digital
- 确认 attn.qkv, attn.proj, mlp.fc1, mlp.fc2, patch_embed conv 标记为 analog
- 确认 analog ratio 在 55-70% 区间（参考手册 §1.1 预期）

### analog_layers.py
- 构造 AnalogLinear(64, 128)，前向传播验证输出 shape
- 验证量化：检查 weight_to_conductance 输出只有 n_states 个唯一电导值
- 验证 D2D 固定：两次 forward，d2d_noise 不变
- 验证 C2C 重采样：两次 forward，输出略有不同
- 验证 STE：`loss.backward()` 后 weight.grad 非零
- 验证 retention：设 inference_time=1000s，确认输出与 t=0 不同
