# Codex Dispatch #4 — Final Polish

> **发布人**: Claude (项目负责人)
> **日期**: 2026-04-16
> **背景**: TX-1~5 全部落地，figures 重绘完成，编译通过。27/27 数据交叉验证全部一致。剩余 3 处文本更新 + 最终编译。

---

## TX-6: §7 Conclusion 补充 contour/Sobol 发现 [HIGH]

**文件**: `paper/latex_gpt/sections/07_conclusion.tex`

**找到这段** (第二段开头):
```
Several observations stand out. Fixed hardware-instance transfer, rather than nominal quantization, is the most prominent deployment risk in the present regime:
```

**替换为**:
```
Several observations stand out. A 63-point iso-accuracy sweep reveals a two-phase constraint hierarchy: ADC resolution below 6 bits causes catastrophic collapse ($S_{\text{ADC}}=0.98$ over the full grid), while within the operational envelope device-to-device variability becomes the binding factor ($S_{\text{D2D}}=0.92$). Fixed hardware-instance transfer, rather than nominal quantization, is the most prominent deployment risk in the present regime:
```

---

## TX-7: §0 Abstract 补充一句 operating envelope [MED]

**文件**: `paper/latex_gpt/sections/00_abstract.tex`

**找到这句**:
```
reducing ADC resolution below 6 bits causes abrupt accuracy collapse.
```

**替换为**:
```
reducing ADC resolution below 6 bits causes abrupt accuracy collapse, and a Sobol decomposition over a 63-point D2D--ADC grid confirms that once 6-bit readout is secured, device-to-device variability dominates the residual accuracy budget.
```

---

## TX-8: §6.6 Outlook 补充 CrossSim 比较结果 [LOW]

**文件**: `paper/latex_gpt/sections/06_discussion.tex`

**找到这句** (§6.6 Outlook 末尾):
```
Finally, the present shared-regime AIHWKIT/CrossSim sanity checks can be extended into broader numerical-equivalence studies that also include retention, photoresponse, and richer write dynamics.
```

**替换为**:
```
A preliminary cross-framework comparison against CrossSim confirms consistent baseline inference under clean conditions (86.2\% ours vs.\ 83.7\% CrossSim on a 1\,000-sample subset at 8-bit ADC), but the accuracy gap widens substantially under noise injection (82.3\% vs.\ 67.9\% at $\sigma=5\%$), highlighting the sensitivity of accuracy predictions to the specific noise-to-conductance mapping. These shared-regime sanity checks can be extended into broader numerical-equivalence studies that also include retention, photoresponse, and richer write dynamics.
```

---

## TX-9: 最终编译验证 [HIGH]

完成 TX-6/7/8 后运行:

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

1. 只修改指定位置
2. 保持 LaTeX 语法正确
3. 编译通过后报告

---

*Claude (项目负责人) — 2026-04-16*
