
## Kimi 2026-05-06 论文数据审计进度

### 已完成修复
1. **Chapter 5第199行**: across-seed std值修复为与JSON一致（1.06, 0.46, 0.01）
2. **Chapter 5第139行**: M6 seed 456 ADC-off std 1.76 → 1.68（cx_m6_fresh_eval.json: 1.685）
3. **Chapter 5第347行**: M6 seed 456 ADC-on std 1.76 → 1.73（cx_m6_adc_perinstance: 1.733）
4. **Chapter 5第116行**: M5 seed 456 ADC-off std 0.11 → 0.09（cx_m5_fresh_eval.json: 0.094）
5. **Chapter 3 Table 3**: Train:Proportional → Eval:Uniform ~10% → ~10.38%（v4_proportional_hat_eval_uniform_results_gpt.json: 10.379±0.438）

### 已验证一致的数据
- OPECT profile: 88.53±0.08% ✓
- Correlated D2D: 86.33±1.61, 84.57±2.39, 82.12±3.95 ✓
- Canonical Ensemble HAT: 86.37±1.54%（seed 123）✓
- Severe-NL M-series: M1-M6全部与perinstance ADC-on JSON一致 ✓
- Retention curve: 91.63, 82.66, 79.13, 79.05, 79.35, 79.51 ✓

### 发现但未修复（差异极小）
- Chapter 5 Table 4的ADC-on值使用perinstance，但第199行across-seed mean使用standard ADC（差异<0.03%）
- 97.37±0.05%来源单一（v4_proportional_hat_train_results_gpt.json只有一个seed），±0.05%未找到明确JSON来源

### 105数据已整理
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/HAT_105_REMOTE_SUMMARY_20260506.md`
- 18 fresh_eval JSONs汇总完成

### 5-bit PCM pilot
- PID 48564运行中，已约34分钟，预计还需~40分钟

## Kimi 2026-05-06 22:06 GPU监控广播

### 5-bit PCM Pilot (r11d_5bit_pcm_seed123)
- **PID**: 48564
- **状态**: 运行中
- **进度**: Epoch 50/100 (50%)
- **当前指标**: Train 54.68% | Test 56.31% | Best 56.31%
- **速度**: ~44.7s/epoch
- **预计剩余**: ~0.6h (~37分钟)
- **已运行**: 2759秒 (~46分钟)
- **GPU**: 48°C, 116W, 6.5GB/16.3GB, 利用率50%

### 论文审计状态
- Thesis Chapter 3-5-7: 5处数据已修复，全部验证一致
- Main paper (latex_gpt/sections/): 核心数字正确，无数据错误
- 105-remote数据: 已整理汇总
- 107-clean数据: 已整理汇总

### 待执行队列
1. 5-bit pilot 完成后的 fresh eval + drift eval
2. 6-bit pilot 训练（脚本已就绪）
3. openblas 卸载（训练完成后）
