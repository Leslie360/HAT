# Gemini Dispatch — 2026-04-16

> **发布人**: Claude (项目负责人)
> **背景**: Codex 完成了 3 项关键实验 (Contour Map 63/63, ConvNeXt ADC 全补齐, ResNet-18 bug fix) + Sobol 分析。现在需要将新数据写入论文 .tex。
> **Gemini 角色**: 文本编辑 — 将 Claude 提供的段落精确插入 .tex 文件

---

## GM-TX-1: §5 新增 "Iso-Accuracy Operating Envelope" 小节 [HIGH]

**文件**: `paper/latex_gpt/sections/05_results.tex`

**位置**: 在 `\subsection{Non-Linear Writing and Hardware-Aware Training}` (line 62) 之前，即 §5.5 `Physical Front-end Compensation` 之后。

**操作**: 插入以下新小节:

```latex
\subsection{Iso-Accuracy Operating Envelope}
\label{subsec:iso-accuracy}

To characterize the joint tolerance of the Ensemble HAT model to device variability and readout precision, we sweep $\sigma_{\text{D2D}} \in \{1, 3, 5, 8, 10, 15, 20\}\%$ and ADC resolution $\in \{2, 3, 4, 5, 6, 7, 8, 10, 12\}$ bits across 63 grid points (10 Monte Carlo runs each, $\sigma_{\text{C2C}}=5\%$, $NL=1.0$). Figure~\ref{fig:contour-map} presents the resulting iso-accuracy contour map.

Three regimes emerge. Below 5-bit ADC, accuracy collapses to near-chance regardless of D2D magnitude. The transition from 5-bit to 6-bit yields a consistent $\sim$7~pp jump across all D2D levels, identifying 6-bit readout as the minimum viable precision. Above 6-bit, accuracy saturates and the remaining degradation is dominated by D2D variability: at $\sigma_{\text{D2D}} \leq 10\%$ the model maintains $>$84\%, while $\sigma_{\text{D2D}} = 20\%$ reduces it to 71--77\%.

A first-order Sobol sensitivity analysis confirms this two-phase structure. Over the full parameter space the ADC index $S_{\text{ADC}} = 0.98$, reflecting the catastrophic sub-6-bit collapse. Within the operational region ($\geq$6-bit, $\sigma_{\text{D2D}} \leq 15\%$), the D2D index $S_{\text{D2D}} = 0.92$, confirming that device variability becomes the binding constraint once minimum readout precision is satisfied. The interaction term is negligible in both regimes ($<$4\%), indicating that ADC and D2D impairments decouple to first order.

\begin{figure}[t]
    \centering
    \includegraphics[width=0.92\textwidth]{fig_contour_map}
    \caption{\textbf{Iso-accuracy contour map} for the Ensemble HAT Tiny-ViT model under joint $\sigma_{\text{D2D}}$ and ADC precision sweep ($\sigma_{\text{C2C}}=5\%$, $NL=1.0$, 10 MC runs per point). The 6-bit ADC cliff and the D2D-dominated degradation in the operational regime are clearly visible.}
    \label{fig:contour-map}
\end{figure}
```

**注意**:
- 不要修改任何其他段落
- 图片文件 `fig_contour_map` 尚未生成，Codex 会做

---

## GM-TX-2: §6.1 补充 Sobol 解读 [HIGH]

**文件**: `paper/latex_gpt/sections/06_discussion.tex`

**位置**: 在 §6.1 `Principal Accuracy Bottlenecks` 的第一段末尾 ("Three constraints dominate instead.") 之后，"The first is ADC resolution." 之前。

**操作**: 在 "Three constraints dominate instead." 和 "The first is ADC resolution." 之间插入:

```latex
A quantitative decomposition supports this ordering. First-order Sobol indices computed from a $7 \times 9$ D2D--ADC grid show that, over the full parameter space, ADC precision accounts for 97.6\% of accuracy variance ($S_{\text{ADC}}=0.98$), while D2D contributes only 1.8\%. However, conditioning on the operational envelope ($\geq$6-bit ADC, $\sigma_{\text{D2D}} \leq 15\%$), the hierarchy inverts: D2D variability accounts for 92.2\% of residual variance ($S_{\text{D2D}}=0.92$). This two-phase structure has a direct hardware implication: designers should first secure 6-bit readout, then invest the remaining error budget in reducing device-to-device mismatch.
```

**注意**: 不改动现有段落的任何文字。仅插入。

---

## GM-TX-3: §6.3 更新 ResNet-18 段落 [MED]

**文件**: `paper/latex_gpt/sections/06_discussion.tex`

**位置**: §6.3 `Task Complexity and Data Starvation`，ResNet-18 相关句子。

当前文本 (line 28 附近):
```
Investigation traced this collapse to a limitation in the current analog conversion pipeline when applied to the ResNet-18 architecture; the resulting weight mapping does not preserve the learned representations under noise injection.
```

**替换为**:
```
Investigation traced this collapse to a backward-compatibility issue in the checkpoint loader: the \texttt{restore\_weight\_scale} flag was not serialized in older ResNet-18 checkpoints, causing the current default (\texttt{True}) to override the original training setting (\texttt{False}) and corrupt the weight reconstruction path at load time. After patching the loader to fall back to \texttt{False} for legacy checkpoints, CIFAR-10 accuracies were recovered (R2: 94.12\%, R4: 89.60\%), while the CIFAR-100 result (1.00\%) was confirmed as a genuine training failure.
```

---

## GM-TX-4: §5 ADC sweep 段落更新 [MED]

**文件**: `paper/latex_gpt/sections/05_results.tex`

**位置**: line 44 附近的 ADC sweep 段落。

当前文本:
```
The ADC sweep (Supplementary Fig.~S1) reveals a transition around 6 bits: accuracy is $\sim$27\% at 4-bit ADC and recovers to $>80\%$ at 6-bit. Pure-digital controls confirm this transition is amplified by hybrid analog summation.
```

**替换为**:
```
An extended ADC sweep over five bit-widths (4, 6, 8, 10, 12 bits; 10 Monte Carlo runs each) confirms the 6-bit threshold on ConvNeXt-Tiny as well: accuracy jumps from 48.4\% at 4-bit ($\pm$16.2\%) to 88.6\% at 6-bit ($\pm$0.3\%), saturating at 89.7\% by 12-bit (Supplementary Fig.~S1). The iso-accuracy contour analysis (Section~\ref{subsec:iso-accuracy}) further shows that this 6-bit cliff is orthogonal to device variability, producing a consistent $\sim$7~pp transition across all tested $\sigma_{\text{D2D}}$ levels.
```

---

## GM-TX-5: Ensemble HAT 频率消融 补充 [LOW]

**文件**: `paper/latex_gpt/sections/05_results.tex`

**位置**: §5.6 `Non-Linear Writing and Hardware-Aware Training`, 在 "Resampling D2D masks during training alleviates instance overfitting" 句子之后。

**插入**:
```latex
A frequency ablation confirms per-epoch resampling as optimal: epoch-level resampling yields 88.41\%, compared with 87.76\% (every 20 epochs), 87.31\% (every 5), 87.18\% (fixed at init), and 86.16\% (per-batch). The single-epoch cadence balances sufficient exposure to diverse mismatch maps against training stability.
```

---

## 执行规则

1. **逐条执行**, 每完成一条立即报告
2. **只插入/替换指定文本**, 不改动任何其他段落
3. 不修改图表编号、引用标签或表格数据
4. 保持 LaTeX 语法正确
5. 完成后运行 `pdflatex main.tex` 验证编译

## 文件路径

```
/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex
/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex
```

---

*Claude (项目负责人) — 2026-04-16*
