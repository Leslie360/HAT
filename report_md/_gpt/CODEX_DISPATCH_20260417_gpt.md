# Codex Dispatch #5 — 收尾修正 + 审稿回应信更新

> **发布人**: Claude (项目负责人)
> **日期**: 2026-04-17
> **背景**: Dispatch #4 全部落地并验证。审阅发现 §6.6 CrossSim 标准噪声数据与锁定值不一致（我 dispatch 中的笔误），需修正。同时审稿回应信 (REVIEWER_RESPONSE_DRAFT_gpt.md) 中的占位符可以用已完成的实验数据填充。

---

## TX-10: 修正 §6.6 CrossSim 标准噪声数据 [CRITICAL]

**文件**: `paper/latex_gpt/sections/06_discussion.tex`

**问题**: 当前文本写 "82.3\% vs.\ 67.9\%"，锁定数据为 81.63±0.56% vs 67.20±2.67%。

**找到这句** (§6.6 Outlook 段落中):
```
but the accuracy gap widens substantially under noise injection (82.3\% vs.\ 67.9\% at $\sigma=5\%$)
```

**替换为**:
```
but the accuracy gap widens substantially under noise injection (81.6\% vs.\ 67.2\% at $\sigma=5\%$)
```

---

## TX-11: 全文数字一致性审计 [HIGH]

扫描以下文件，验证**所有出现的实验数字**与锁定数据源一致：

| 文件 | 需检查的关键数字 |
|:--|:--|
| `sections/00_abstract.tex` | 86.37±1.54%, 88.53%, 27.72±0.82%, 10.00% |
| `sections/01_introduction.tex` | 同上 + 6-bit cliff |
| `sections/05_results.tex` | 全部表格数字、84.75±0.72%, 48.4%→88.6%, 97.37±0.05%, 88.41% |
| `sections/06_discussion.tex` | S_ADC=0.976/0.98, S_D2D=0.922/0.92, CrossSim 86.2/83.7/81.6/67.2 |
| `sections/07_conclusion.tex` | S_ADC=0.98, S_D2D=0.92, 86.37±1.54%, 27.72±0.82%, 88.53% |
| `supplementary.tex` | 全部表格数字 |

**锁定数据源**:

| 实验 | 锁定值 | 来源文件 |
|:--|:--|:--|
| Ensemble HAT fresh | 86.37 ± 1.54% | CLAUDE_TASK_gpt.md |
| CrossSim clean | 86.20% vs 83.70% | crosssim_clean_baseline.json |
| CrossSim low | 85.90±0.28% vs 82.87±0.29% | crosssim_low_noise.json |
| CrossSim standard | 81.63±0.56% vs 67.20±2.67% | crosssim_standard_noise.json |
| Sobol full grid | S_ADC=0.976 | sobol_sensitivity.json |
| Sobol operational | S_D2D=0.922 | sobol_sensitivity.json |
| ConvNeXt ADC 4-bit | 48.4±16.2% | convnext_adc_sweep_results.json |
| ConvNeXt ADC 6-bit | 88.6±0.3% | convnext_adc_sweep_results.json |
| Proportional HAT ViT | 97.37±0.05% | CLAUDE_TASK_gpt.md |
| NL=2.0 HAT | 27.72±0.82% | CLAUDE_TASK_gpt.md |
| ConvNeXt 3-seed | 84.75±0.72% | CLAUDE_TASK_gpt.md |
| OPECT zero-shot | 88.53% | CLAUDE_TASK_gpt.md |
| Frequency ablation best | 88.41% (per-epoch) | CLAUDE_TASK_gpt.md |

**输出**: 列出所有核对结果。如发现不一致，在同一次修改中修正。

---

## TX-12: 更新审稿回应信 [HIGH]

**文件**: `report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md`

当前 draft 由 Kimi 起草于 2026-04-14，有多处 `[AWAITING ...]` 占位符。用以下已完成的实验数据填充：

### Major Comment 1: CrossSim 对比 — 替换占位符

找到:
```
- Status: [AWAITING GM-P0 RESULTS — placeholder for final numbers]
```

替换为:
```
- Status: ✅ COMPLETED — Three-phase progressive comparison (ConvNeXt C4 checkpoint, 1000 samples, 8-bit ADC, 3 MC runs per phase)
- Results:
  - Clean (σ=0%): ours 86.20% vs CrossSim 83.70% (gap 2.50 pp)
  - Low noise (σ=1%): ours 85.90±0.28% vs CrossSim 82.87±0.29% (gap 3.03 pp)
  - Standard noise (σ=5%): ours 81.63±0.56% vs CrossSim 67.20±2.67% (gap 14.43 pp)
- Key finding: Gap widens from 2.5 pp to 14.4 pp with noise, supporting profile-driven simulation argument
- Data files: crosssim_clean_baseline.json, crosssim_low_noise.json, crosssim_standard_noise.json
```

找到:
```
3. [TO BE COMPLETED] CrossSim comparison results will be added to Supplementary §S6 upon completion
```

替换为:
```
3. CrossSim comparison results integrated into Discussion §6.6 Outlook
```

### Major Comment 2: NL=2.0 — 更新状态

找到:
```
- Status: [AWAITING GM-P2 RESULTS — placeholder for layer-wise breakdown]
```

替换为:
```
- Status: ⚠️ Layer-wise NL injection not conducted. However, the NL=2.0 boundary is now clearly framed as a gradient-scaling approximation limit (§6.5 Limitations), not a fundamental materials constraint. The 63-point Sobol analysis (S_ADC=0.976 full grid) provides comprehensive parameter sensitivity decomposition.
```

找到:
```
2. [TO BE COMPLETED] Layer-wise sensitivity results will be added to Supplementary §S8
```

替换为:
```
2. Layer-wise NL sensitivity deferred to future work; current revision strengthens the approximation-boundary framing and adds Sobol sensitivity decomposition as complementary evidence
```

### Major Comment 3: Ensemble HAT 消融 — 替换占位符

找到:
```
- Status: [AWAITING GM-P1 RESULTS — placeholders for ablation data]
```

替换为:
```
- Status: ✅ COMPLETED
- Resampling frequency ablation (5 cadences tested):
  - Per-epoch: 88.41% (best)
  - Every 20 epochs: 87.76%
  - Every 5 epochs: 87.31%
  - Fixed at init: 87.18%
  - Per-batch: 86.16%
- i.i.d. noise vs structured D2D: Ensemble HAT (86.37±1.54%) vs i.i.d. augmentation (~10% collapse on fresh arrays, same as standard HAT)
- D2D variance: 63-point contour map covers σ_D2D ∈ {1,3,5,8,10,15,20}% × ADC ∈ {2,3,4,5,6,7,8,10,12} bits
- Results integrated into §5.6 (iso-accuracy envelope), §5.7 (frequency ablation in Supp Fig S4), §6.1 (Sobol decomposition)
```

找到:
```
2. [TO BE COMPLETED] Full ablation results will be added to Supplementary §S7
```

替换为:
```
2. Full ablation results integrated: frequency ablation in Supplementary Fig. S4, iso-accuracy contour in main Fig. 3, Sobol analysis in Supplementary Fig. S2
```

### 实验状态总结 — 替换底部占位符

找到:
```
**Draft Status**: Awaiting experimental results (GM-P0, P1, P2) for completion of placeholders.
```

替换为:
```
**Draft Status**: GM-P0 (CrossSim) ✅ and GM-P1 (Ensemble HAT ablation) ✅ completed and integrated. GM-P2 (layer-wise NL) deferred to future work with strengthened approximation-boundary framing. Response letter ready for final review by Claude.
```

---

## TX-13: 最终编译验证 [HIGH]

完成 TX-10 后运行:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
pdflatex -interaction=nonstopmode main.tex && \
pdflatex -interaction=nonstopmode main.tex && \
pdflatex -interaction=nonstopmode supplementary_main.tex && \
pdflatex -interaction=nonstopmode supplementary_main.tex
```

检查:
- 无 `undefined reference`
- 无 `multiply defined`
- 无 `Overfull \hbox` > 10pt

---

## 执行规则

1. TX-10 优先（阻塞编译）
2. TX-11 可与 TX-12 并行
3. TX-13 在 TX-10 完成后执行
4. 只修改指定位置，不做额外改动
5. 编译通过后回报 Claude

---

*Claude (项目负责人) — 2026-04-17*
