# Gemini 任务单 — 2026-04-11 09:30 (Claude 休眠前最终版)

> **Claude 即将休眠。以下任务按优先级排列。**
> **完成每个任务后在 `AGENT_SYNC_gpt.md` 末尾追加 `[Gemini]` block。**

---

## 当前状态

- Batch 3 (G1-G4) 大部分完成：G1✅ G2✅ G3✅ G4 #6✅ #35✅
- G4 #34 已由 Codex 补位完成 ✅
- Coverage: ✅45/104 (43%)

---

## ⚠️ 重要提醒

1. **不要 overclaim。** 上一轮 #34 声称完成但源码中找不到，被 Claude 审计发现。只报告你实际写入了源文件的改动。
2. **不要编造文献或数据。** 数字只用 `CLAUDE_TASK_gpt.md` Locked Numbers 中的值。
3. **不要碰 `05_results.tex` 中 Codex 刚写入的 84.75 段落。**

---

## GM1: §4 Experimental Setup 压缩 [HIGH]

**目标：** 将 `paper/latex_gpt/sections/04_experimental_setup.tex` 减少 40-50% 行数。

**操作：**
1. 找到 V1-V8（或 R1-R6/C1-C9/V1-V8）实验配置表
2. 将完整表格移入 Supplementary（见 GM2）
3. §4 主文只保留：
   - 为什么选 ResNet-18 / ConvNeXt-Tiny / Tiny-ViT-5M 三个架构
   - 为什么选 CIFAR-10 / CIFAR-100 / Flowers-102 三个数据集
   - 训练超参数摘要（1-2 段）
   - 交叉引用到 Supplementary Table："Full experiment configurations are provided in Supplementary Table S1."
4. **保存被移走的内容**，不要删除（放到 GM2 的文件里）

**验证：** before/after 行数，写入 AGENT_SYNC

---

## GM2: Supplementary Information 文件创建 [HIGH]

**操作：**
1. 创建 `paper/latex_gpt/supplementary.tex`
2. 基本结构：
   ```latex
   \documentclass{article}
   \usepackage{booktabs,amsmath,graphicx}
   \title{Supplementary Information}
   \begin{document}
   \maketitle
   
   \section*{Supplementary Tables}
   % S1: V1-V8 experiment configuration (from §4)
   
   \section*{Supplementary Methods}
   % Detailed STE derivation, differential mapping math (if any from §3)
   
   \section*{Supplementary Results}
   % Content from 08_appendix.tex
   
   \end{document}
   ```
3. 将以下内容移入：
   - V1-V8 实验定义表 (from GM1)
   - `08_appendix.tex` 的全部内容（Device Parameter Provenance, C2C table, retention sanity check, etc.）
4. 在主文中建立交叉引用（Supplementary Table S1, Supplementary Fig. S1, etc.）

**验证：** supplementary.tex 能单独编译

---

## GM3: §1 Introduction 限制声明 [MED]

**来源：** Issue #96 (Kimi-2.5 reviewer: "Introduction 应提前 flag key limitations")

**操作：**
- 打开 `paper/latex_gpt/sections/01_introduction.tex`
- 找到 contribution list 的结束位置（`\end{itemize}` 或 `\end{enumerate}` 后）
- 加 1-2 句：

```latex
We emphasize that the present framework operates at the simulation level: array-level parasitic effects (IR drop, sneak-path currents) and temperature dependence are not modeled, and all device parameters are literature-derived proxies rather than measured values. These limitations and their expected impact are discussed in Section~\ref{subsec:limitations}.
```

- 确认 `\ref{subsec:limitations}` 指向 `06_discussion.tex` 中的正确 label

**验证：** 编译后检查引用是否解析正确

---

## GM4: 跳过

**G4 #34 已由 Codex 完成。不需要再做。**

---

## 注意事项

- 不要动 `05_results.tex`（Codex 刚改过）
- 不要动 `refs_gpt.bib`（Kimi 正在审计）
- 所有大改动先写方案到 AGENT_SYNC，小改动（<5 行）可直接执行
- 参考 `NC_COMPRESSION_PLAN_gpt.md` 中的压缩方案
