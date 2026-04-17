## KP-FIX-3: ConvNeXt ADC 无敏感性分析

**状态**: 问题确认 ✅  
**发现时间**: 2026-04-15  

---

### 问题现象

`convnext_adc_sweep_results.json` 显示：
- ADC 4-bit: 89.65%
- ADC 6-bit: 89.65%  
- ADC 8-bit: 89.65%
- **所有结果完全相同** (raw: [89.53, 89.69, 89.74])

这不可能正确，因为Tiny-ViT显示明显的6-bit cliff。

---

### 根因诊断

**假设**: `cfg.adc_bits` 设置未实际传递到ConvNeXt推理路径

**证据**:
1. 所有bit宽度的raw值完全相同
2. 标准差异常小 (0.09%)
3. 与Tiny-ViT行为完全不符

**可能原因**:
1. `convert_to_hybrid()` 未正确处理ConvNeXt的ADC参数
2. ConvNeXt的forward路径绕过analog layers
3. 评估时加载了错误的config

---

### 验证计划

需要检查：
1. ConvNeXt的analog layer是否实际创建了ADC quantization
2. `cfg.adc_bits` 是否被正确写入model config
3. Forward pass中ADC是否真的被应用

---

### 建议修复

**短期**: 在论文中删除ConvNeXt ADC结果，注明"待修复"  
**中期**: 修复ConvNeXt的ADC路径bug，重新运行  
**长期**: 如果修复后仍无敏感性，讨论CNN vs Transformer的ADC差异

---

**结论**: 数据确实有问题，不应引用。需要debug ConvNeXt的ADC路径。
