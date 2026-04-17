# ResNet-18 补充实验计划 (方案A)

> **日期**: 2026-04-13  
> **目标**: 实现三架构实验对称性  
> **总GPU时间**: ~6-8小时

---

## 需要补充的实验

### 1. CIFAR-100 基线

| 实验ID | 描述 | 预期时间 | 必要性 |
|:-------|:-----|:---------|:-------|
| **R1** | ResNet-18 CIFAR-100 FP32 Digital | 0.5h | P0 - 必须 |

**预期结果**: ~65-70% (参考ConvNeXt 64.12%)

---

### 2. 噪声与HAT实验 (对标Tiny-ViT V3/V4)

| 实验ID | 描述 | 预期时间 | 必要性 |
|:-------|:-----|:---------|:-------|
| **R2** | ResNet-18 CIFAR-100 V3 (Canonical Noise) | 1.5h | P0 - 必须 |
| **R3** | ResNet-18 CIFAR-100 V4 (Canonical HAT) | 1.5h | P0 - 必须 |

**预期结果**: 
- R2: ~45-50% (对标Tiny-ViT 44.06%)
- R3: ~60-65% (对标Tiny-ViT 65.48%)

---

### 3. Flowers-102 (可选但推荐)

| 实验ID | 描述 | 预期时间 | 必要性 |
|:-------|:-----|:---------|:-------|
| **R4** | ResNet-18 Flowers-102 FP32 | 0.5h | P1 - 推荐 |
| **R5** | ResNet-18 Flowers-102 V3/V4 | 3h | P1 - 推荐 |

**说明**: Flowers-102对小CNN可能太难，但数据完整性好。

---

## 实验配置

### 使用现有脚本

```bash
# 基线
python train_resnet18.py --dataset cifar100 --epochs 200 --seed 42

# V3: Canonical Noise
python train_resnet18.py --dataset cifar100 --analog --noise-std 0.1 --epochs 200

# V4: Canonical HAT
python train_resnet18.py --dataset cifar100 --analog --noise-std 0.1 --hat --epochs 200
```

### 关键参数 (与Tiny-ViT保持一致)

| 参数 | 值 | 说明 |
|:-----|:---|:-----|
| `--epochs` | 200 | 与ConvNeXt一致 |
| `--seed` | 42, 123, 2026 | 三种子验证 |
| `--noise-std` | 0.1 | canonical D2D=10% |
| `--adc-bits` | 8 | 默认，除非测试ADC扫描 |

---

## 时间表

### 如果立即启动 (单GPU顺序)

| 时间 | 实验 | 产出 |
|:-----|:-----|:-----|
| T+0h | R1 (CIFAR-100 FP32) | 基线数字 |
| T+0.5h | R2 (CIFAR-100 V3) | 噪声退化 |
| T+2h | R3 (CIFAR-100 V4) | HAT恢复 |
| T+3.5h | R4 (Flowers FP32) | 扩展基线 |
| T+4h | R5 (Flowers V3/V4) | 完整矩阵 |
| **T+7h** | **全部完成** | **对称表格** |

### 如果双GPU并行

- GPU 0: R1 → R2 → R3 (CIFAR-100主线)
- GPU 1: R4 → R5 (Flowers扩展)
- **总时间: ~4小时**

---

## 表格更新预览

### Table 1 (FP32 Baseline) — 补充后

| Dataset | ResNet-18 | ConvNeXt-Tiny | Tiny-ViT-5M |
|:--------|:----------|:--------------|:------------|
| CIFAR-10 | 94.98% | 90.74% | 98.06% |
| **CIFAR-100** | **~68%** | 64.12% | 86.94% |
| **Flowers-102** | **~45%*** | 33.22%* | 97.97% |

*ResNet-18 Flowers可能需要从随机初始化训练，可能低于预训练Transformer。

### Table 2 (Result Summary) — 补充后

| Architecture | Regime | CIFAR-10 | CIFAR-100 | Flowers-102 |
|:-------------|:-------|:---------|:----------|:------------|
| ResNet-18 | FP32 Digital | 94.98 | **~68** | **~45*** |
| ResNet-18 | **V3 (Noise)** | — | **~48 ± ?** | — |
| ResNet-18 | **V4 (HAT)** | — | **~62 ± ?** | — |
| ... | ... | ... | ... | ... |

---

## 风险与缓解

| 风险 | 可能性 | 缓解 |
|:-----|:-------|:-----|
| ResNet-18 Flowers表现极差(<20%) | 中 | Flowers对小CNN确实难；可只报CIFAR-100作为"完整验证" |
| GPU时间超预期 | 低 | 使用--resume-existing断点续训 |
| 结果与Tiny-ViT趋势不一致 | 低 | CNN vs Transformer差异是合理发现，可讨论 |

---

## 成功标准

- [ ] ResNet-18 CIFAR-100 FP32完成
- [ ] ResNet-18 CIFAR-100 V3/V4完成
- [ ] 结果填入Table 1和Table 2
- [ ] 正文添加ResNet-100讨论段落

---

**Ready for Gemini execution.**
