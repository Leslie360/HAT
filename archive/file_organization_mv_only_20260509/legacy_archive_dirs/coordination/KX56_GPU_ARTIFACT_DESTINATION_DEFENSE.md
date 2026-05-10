# KX56: GPU Artifact Destination Defense Memo

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Goal**: 帮 Codex 判断 GPU 产物该进哪里

---

## Artifact Routing Matrix

### 1. `ablation_ensemble_results.json`

| 属性 | 评估 |
|:-----|:-----|
| **内容** | Ensemble HAT vs 标准 HAT，10 fresh-instance评估 |
| **结果** | 86.567 ± 1.658% (Ensemble) vs ~10% (标准) |
| **Best Destination** | **主文 (Main Text)** |
| **Why** | 核心贡献支柱；审稿人RC4攻击的直接防御 |
| **Overclaim Risk** | 低；结果稳健，MC误差小 |
| **Insertion Point** | `05_results.tex` Section 5.6 |

---

### 2. `pure_digital_adc_sweep.json`

| 属性 | 评估 |
|:-----|:-----|
| **内容** | 纯数字量化4/6/8-bit扫描（无模拟噪声） |
| **结果** | 待确认（预期：验证6-bit悬崖是否ViT固有） |
| **Best Destination** | **补充材料 (Supplementary)** |
| **Why** | 支持性证据，分离变量控制；主文保持精简 |
| **Overclaim Risk** | 中；若结果显示悬崖纯由ViT量化引起，需弱化有机CIM特异性主张 |
| **Insertion Point** | `supplementary.tex` Table S6 / Fig S6 |
| **Condition** | 结果有意义时插入；若0%或异常则入backlog |

---

### 3. `retention_sensitivity_results.json`

| 属性 | 评估 |
|:-----|:-----|
| **内容** | τ₁, τ₂ ±50% 变化对精度影响 |
| **结果** | 待生成 |
| **Best Destination** | **Revision-only / Supplementary** |
| **Why** | 防御RC1代理参数质疑；当前非核心主张 |
| **Overclaim Risk** | 低；仅用于证明参数鲁棒性 |
| **Insertion Point** | Revision response letter + Supplementary Table S7 |
| **Condition** | Major Revision收到后作为响应数据 |

---

### 4. `combined_stress_results.json` (NL scan)

| 属性 | 评估 |
|:-----|:-----|
| **内容** | NL=1.5, 1.8, 2.0, 2.5 扫描 |
| **结果** | 待生成；需要重新训练checkpoints |
| **Best Destination** | **Revision-only** |
| **Why** | 强化NL=2.0作为"渐进失效"非"硬边界"；当前单点数据已够 |
| **Overclaim Risk** | 低；但训练成本高，非阻塞 |
| **Insertion Point** | Revision response + 可选Supplementary Fig S8 |
| **Condition** | 仅当审稿人质疑NL边界绝对性时 |

---

### 5. Tiny-ImageNet Exploratory Output

| 属性 | 评估 |
|:-----|:-----|
| **内容** | 200类Tiny-ImageNet零样本迁移 |
| **结果** | **0.00%** (当前失败，类别空间不匹配) |
| **Best Destination** | **Framework / Exploratory Backlog** |
| **Why** | 非可发布结果；技术调试问题 |
| **Overclaim Risk** | **高**；绝不可作为证据引用 |
| **Action** | Debug class-space映射；成功后重新评估 |
| **Reassessment Trigger** | 非零结果出现后 → 考虑Supplementary |

---

### 6. ImageNet-1K Validation (Future)

| 属性 | 评估 |
|:-----|:-----|
| **内容** | 1000类完整验证 |
| **结果** | 待下载/执行 |
| **Best Destination** | **Paper-2 Backlog** |
| **Why** | 超出当前论文学术范围；适合作为第二篇扩展 |
| **Overclaim Risk** | 中；若结果差会削弱当前主张 |
| **Condition** | Paper-1提交后或Major Revision期间执行 |

---

## Summary Routing Table

| Artifact | Destination | Priority | Condition |
|:---------|:------------|:---------|:----------|
| Ensemble ablation | Main Text | P0 | 立即插入 |
| Pure-digital ADC | Supplementary | P1 | 结果有效时 |
| Retention sensitivity | Revision-only | P2 | Major Rev收到后 |
| NL scan | Revision-only | P2 | 审稿人质疑时 |
| Tiny-ImageNet | **Backlog** | - | Debug后重评 |
| ImageNet-1K | Paper-2 | P3 | Paper-1后 |

---

## Decision Rules for Codex

1. **Main Text准入**: 仅核心贡献直接支撑 (Ensemble ablation)
2. **Supplementary准入**: 支持性证据且结果稳健
3. **Revision-only**: 防御性数据，响应特定审稿质疑
4. **Backlog**: 技术失败或超范围探索
5. **Paper-2**: 规模扩展，自然延伸

---

## Risk Flags

🚩 **绝不可做的事**:
- 引用Tiny-ImageNet 0.00%结果作为任何证据
- 将未完成的NL扫描作为已声明贡献
- 在主文过度强调纯数字ADC控制（削弱有机特异性）

✅ **安全做法**:
- Ensemble ablation作为核心成果 prominently展示
- 其他工件作为"支持性/防御性"材料低调呈现
- 所有未成熟结果明确标记为"exploratory"

---

**Ready for Codex artifact-routing decisions.**
