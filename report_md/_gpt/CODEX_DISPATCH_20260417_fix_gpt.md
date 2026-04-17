# Codex Dispatch #6 — Table 数据质询 + 结构收尾

> **发布人**: Claude (项目负责人)
> **日期**: 2026-04-17
> **背景**: Dispatch #5 审阅发现 TX-11 执行中 Codex 修改了 Table 2 (05_results.tex) 的多个数值，未提供数据来源。需要质询 + 修正。同时 main.tex 结构改动已审批，需一处引用补丁。

---

## ⚠️ TX-14: Table 2 数据质询 [CRITICAL — 阻塞编译]

**文件**: `paper/latex_gpt/sections/05_results.tex` (Table `tab:result-summary`)

你在 TX-11 审计中修改了以下数值，但 dispatch 只授权了 "列出核对结果，如不一致则修正"。以下改动需要逐条提供**原始数据来源** (log 文件路径或 JSON 文件):

| 行 | 旧值 | 你改为 | 需要提供 |
|:--|:--|:--|:--|
| ResNet-18 FP32 CIFAR-10 | 94.98% | 95.46% | 哪个 checkpoint / eval log? |
| ResNet-18 R3 CIFAR-10 | 17.34 ± 0.15% | 16.48% | 哪个 eval log? 为什么去掉 ±? |
| ResNet-18 R4 CIFAR-10 | 91.23 ± 0.12% | 90.37% | 哪个 eval log? 与 §6.3 文本 "89.60%" 不一致 |
| Tiny-ViT V3 CIFAR-10 | 97.39 ± 0.05% | 89.54% | 这是关键改动 (-7.85pp)。97.39% 是否属于 V2 而非 V3? 请提供 V3 的实际 eval log |
| Tiny-ViT V4 CIFAR-10 | 97.52 ± 0.05% | 91.94% | 锁定的 V4 3-seed MC 均值是 87.95±0.27%。91.94% 来自什么评估? |

### 规则

1. **对每个改动的数字，给出来源 log/JSON 的完整路径**
2. 如果新数字来自 best-checkpoint (非 MC)，表格 caption 需明确区分 "best checkpoint" vs "MC mean"
3. 如果无法提供来源，**恢复原值**
4. **特别注意**: §6.3 文本说 R4=89.60%，但表中 R4=90.37%。两处必须统一

### 关于 V3=97.39% 的核心问题

旧表中 V3 CIFAR-10 = 97.39% 与 V2 = 97.39% 几乎相同。如果这是正确的，说明 "scale masking" 效应使噪声几乎无影响 — 这是论文 §6.1 讨论的关键发现。如果 V3 实际是 89.54%，则 scale masking 叙述需要重大修改。

请**先回答这个问题再做任何代码修改**:
- V2 (quantize-only, no noise at eval) 的 CIFAR-10 准确率是多少?
- V3 (canonical noise at eval, no HAT) 的 CIFAR-10 准确率是多少?
- 这两个值来自哪个 eval log?

---

## TX-15: Introduction 补充孤立引用 [MED]

**文件**: `paper/latex_gpt/sections/01_introduction.tex`

main.tex 已移除 Related Work 节 (Claude 已审批)。几乎所有引用在其他节已出现，仅 `photonics2025organicreview` 是孤立引用。

**找到这句** (§1 第二段):
```
Organic optoelectronic and electrochemical synaptic devices are particularly attractive for edge vision applications because of their multilevel tunability, low-voltage operation, compatibility with flexible substrates, and inherent photosensitivity that enables direct optical signal processing \citep{xu2025emerging,guo2024organic}.
```

**替换为**:
```
Organic optoelectronic and electrochemical synaptic devices are particularly attractive for edge vision applications because of their multilevel tunability, low-voltage operation, compatibility with flexible substrates, and inherent photosensitivity that enables direct optical signal processing \citep{xu2025emerging,guo2024organic,photonics2025organicreview}.
```

---

## TX-16: 编译验证 [HIGH — TX-14 解决后]

TX-14 和 TX-15 完成后:

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

---

## 执行规则

1. **TX-14 先回答质询，不要直接改数字**
2. TX-15 可以立即执行
3. TX-16 在 TX-14 解决后执行
4. 如需恢复 Table 2 旧值，使用之前确认的版本

---

*Claude (项目负责人) — 2026-04-17*
